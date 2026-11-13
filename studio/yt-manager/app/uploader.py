"""Upload pipeline with channel guards. Dry-run is the default and never calls videos.insert.

Guards against publishing to the wrong channel:
  1. The request must name a channel explicitly (there is no default channel).
  2. Credentials are loaded only from that channel's own row.
  3. Right before upload, channels.list(mine=true) is called with those exact credentials and the
     returned channel id must equal the selected id; otherwise the upload is blocked.
  4. Live uploads additionally need LIVE_UPLOADS_ENABLED=true AND the channel title typed exactly.
"""
from __future__ import annotations

import mimetypes
import random
import time
from dataclasses import dataclass, field
from typing import Callable, Literal

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from . import auth
from .config import Settings
from .crypto import TokenCipher
from .db import Database
from .media import MediaError, MediaInfo, probe
from .metadata import VideoMetadata, validate
from .services import ServiceFactory

VideoKind = Literal["short", "long"]
RETRIABLE_STATUS = {500, 502, 503, 504}
CHUNK_SIZE = 8 * 1024 * 1024


class ChannelMismatchError(RuntimeError):
    pass


@dataclass
class UploadRequest:
    channel_id: str
    file_path: str
    kind: VideoKind
    metadata: VideoMetadata
    live: bool = False
    confirm_channel_title: str | None = None


@dataclass
class UploadOutcome:
    mode: str
    status: str                       # blocked | validated | uploaded | failed
    channel_id: str
    channel_title: str | None = None
    media: MediaInfo | None = None
    body: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    video_id: str | None = None
    job_id: int | None = None
    quota_used_today: int = 0
    quota_cost: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def verify_channel_identity(youtube, expected_channel_id: str) -> dict:
    """Ask YouTube which channel these credentials belong to; raise if it is not the expected one."""
    resp = youtube.channels().list(part="snippet", mine=True).execute()
    ids = [item["id"] for item in resp.get("items", [])]
    if ids != [expected_channel_id]:
        raise ChannelMismatchError(
            f"حماية القناة: بيانات الدخول تعود إلى {ids or 'لا شيء'} وليس إلى القناة المختارة {expected_channel_id}. تم إيقاف العملية."
        )
    return resp["items"][0]


class Uploader:
    def __init__(self, settings: Settings, db: Database, cipher: TokenCipher, services: ServiceFactory,
                 credentials_loader: Callable | None = None, sleep: Callable[[float], None] = time.sleep):
        self.settings = settings
        self.db = db
        self.cipher = cipher
        self.services = services
        self.load_credentials = credentials_loader or auth.load_credentials
        self.sleep = sleep

    def run(self, req: UploadRequest, progress: Callable[[float], None] | None = None) -> UploadOutcome:
        mode = "live" if req.live else "dry_run"
        out = UploadOutcome(mode=mode, status="blocked", channel_id=req.channel_id,
                            quota_cost=self.settings.upload_quota_cost)

        # 1. explicit, connected channel
        channel = self.db.get_channel(req.channel_id) if req.channel_id else None
        if channel is None:
            out.errors.append("يجب اختيار قناة مربوطة قبل الرفع.")
            return self._finish(out, req)
        out.channel_title = channel.title

        # 2. media
        is_short = req.kind == "short"
        try:
            out.media = probe(req.file_path)
            if is_short and not out.media.short_eligible:
                out.errors.append(
                    f"اخترت Short لكن الفيديو {out.media.orientation} ومدته {out.media.duration_seconds:.0f} ث. "
                    "الـ Short يجب أن يكون عمودياً أو مربعاً ومدته 3 دقائق أو أقل."
                )
            if not is_short and out.media.short_eligible:
                out.warnings.append("اخترت فيديو طويل، لكن الملف عمودي/مربع وقصير، فقد يصنّفه YouTube كـ Short.")
        except MediaError as exc:
            out.errors.append(str(exc))

        # 3. metadata
        result, out.body = validate(req.metadata, is_short=is_short)
        out.errors += result.errors
        out.warnings += result.warnings

        # 4. quota
        out.quota_used_today = self.db.quota_used_today()
        if out.quota_used_today + self.settings.upload_quota_cost > self.settings.daily_quota:
            out.errors.append(
                f"الحصة اليومية لا تكفي: مستخدم {out.quota_used_today} من {self.settings.daily_quota}، والرفع يحتاج {self.settings.upload_quota_cost}."
            )

        # 5. live-only gates (checked before any network call)
        if req.live:
            if not self.settings.live_uploads_enabled:
                out.errors.append("النشر الفعلي معطّل. فعّله بـ LIVE_UPLOADS_ENABLED=true بعد الموافقة.")
            if (req.confirm_channel_title or "").strip() != channel.title:
                out.errors.append(f"للتأكيد اكتب اسم القناة كما هو بالضبط: «{channel.title}».")

        if out.errors:
            return self._finish(out, req)

        # 6. channel identity check with this channel's own credentials
        try:
            creds = self.load_credentials(self.db, self.cipher, req.channel_id)
            youtube = self.services.youtube(creds)
            verify_channel_identity(youtube, req.channel_id)
            self.db.log_quota("channels.list", 1, req.channel_id)
        except (auth.ChannelAuthError, ChannelMismatchError) as exc:
            out.errors.append(str(exc))
            return self._finish(out, req)
        except HttpError as exc:
            out.errors.append(f"خطأ من YouTube أثناء التحقق من القناة: {exc}")
            return self._finish(out, req)

        if not req.live:
            out.status = "validated"
            return self._finish(out, req)

        # 7. live upload (only reached when every gate above passed)
        out.job_id = self._record(out, req, status="uploading")
        try:
            out.video_id = self._upload(youtube, req, out.body, progress)
            out.status = "uploaded"
        except Exception as exc:  # noqa: BLE001
            out.status = "failed"
            out.errors.append(f"فشل الرفع: {exc}")
        finally:
            self.db.log_quota("videos.insert", self.settings.upload_quota_cost, req.channel_id)
        self.db.update_job(out.job_id, out.status, out.video_id, out.errors + out.warnings)
        return out

    def _upload(self, youtube, req: UploadRequest, body: dict, progress) -> str:
        mimetype = mimetypes.guess_type(req.file_path)[0] or "application/octet-stream"
        media = MediaFileUpload(req.file_path, mimetype=mimetype, chunksize=CHUNK_SIZE, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response, retries = None, 0
        while response is None:
            try:
                status, response = request.next_chunk()
                if status and progress:
                    progress(status.progress())
            except HttpError as exc:
                if exc.resp.status not in RETRIABLE_STATUS or retries >= 5:
                    raise
                retries += 1
                self.sleep(min(2 ** retries + random.random(), 60))
            except (ConnectionError, TimeoutError, OSError):
                if retries >= 5:
                    raise
                retries += 1
                self.sleep(min(2 ** retries + random.random(), 60))
        if "id" not in response:
            raise RuntimeError(f"استجابة غير متوقعة: {response}")
        return response["id"]

    def _record(self, out: UploadOutcome, req: UploadRequest, status: str) -> int:
        return self.db.create_job(req.channel_id or "-", req.file_path, req.kind, out.mode, status,
                                  out.body, out.errors + out.warnings)

    def _finish(self, out: UploadOutcome, req: UploadRequest) -> UploadOutcome:
        out.job_id = self._record(out, req, status=out.status)
        return out
