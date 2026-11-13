"""OAuth 2.0: connecting channels and loading per-channel credentials.

Each channel gets its own consent + its own refresh token. A token is only ever
used for the channel it was stored under (see uploader.verify_channel_identity).
"""
from __future__ import annotations

import json
import secrets

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from .config import SCOPES, Settings
from .crypto import TokenCipher
from .db import Channel, Database
from .services import ServiceFactory


class ChannelAuthError(RuntimeError):
    pass


def _flow(settings: Settings, state: str | None = None, code_verifier: str | None = None) -> Flow:
    if not settings.client_secrets_file.is_file():
        raise ChannelAuthError(
            f"ملف OAuth غير موجود: {settings.client_secrets_file} — نزّله من Google Cloud Console."
        )
    return Flow.from_client_secrets_file(
        str(settings.client_secrets_file), scopes=SCOPES, redirect_uri=settings.redirect_uri,
        state=state, code_verifier=code_verifier, autogenerate_code_verifier=code_verifier is None,
    )


def start_connect(settings: Settings, db: Database) -> str:
    """Return the Google consent URL. `select_account` lets the user pick any Google account,
    and YouTube then asks which channel (incl. Brand Accounts) to authorize."""
    state = secrets.token_urlsafe(32)
    flow = _flow(settings, state=state)
    url, _ = flow.authorization_url(
        access_type="offline", prompt="select_account consent", include_granted_scopes="false",
    )
    db.save_oauth_state(state, flow.code_verifier)
    return url


def finish_connect(settings: Settings, db: Database, cipher: TokenCipher, services: ServiceFactory,
                   state: str, authorization_response: str) -> Channel:
    valid, verifier = db.pop_oauth_state(state)
    if not valid:
        raise ChannelAuthError("طلب الربط منتهي أو غير صالح. أعد المحاولة.")
    flow = _flow(settings, state=state, code_verifier=verifier)
    flow.fetch_token(authorization_response=authorization_response)
    creds: Credentials = flow.credentials
    if not creds.refresh_token:
        raise ChannelAuthError("لم يُرجع Google رمز تحديث (refresh token). ألغِ وصول التطبيق من حساب Google وأعد الربط.")
    granted = set(creds.granted_scopes or creds.scopes or [])
    missing = [s for s in SCOPES if s not in granted]
    if missing:
        raise ChannelAuthError("لم تُمنح كل الصلاحيات المطلوبة: " + ", ".join(missing))

    resp = services.youtube(creds).channels().list(part="snippet", mine=True).execute()
    db.log_quota("channels.list", 1)
    items = resp.get("items", [])
    if len(items) != 1:
        raise ChannelAuthError("الحساب المختار لا يملك قناة YouTube (أو أرجع أكثر من قناة).")
    item = items[0]
    snippet = item.get("snippet", {})
    thumbs = snippet.get("thumbnails", {})
    thumb = (thumbs.get("default") or thumbs.get("medium") or {}).get("url")
    db.upsert_channel(
        channel_id=item["id"], title=snippet.get("title", item["id"]), custom_url=snippet.get("customUrl"),
        thumbnail_url=thumb, credentials_enc=cipher.encrypt(creds.to_json()), scopes=sorted(granted),
    )
    channel = db.get_channel(item["id"])
    assert channel is not None
    return channel


def load_credentials(db: Database, cipher: TokenCipher, channel_id: str) -> Credentials:
    channel = db.get_channel(channel_id)
    if channel is None:
        raise ChannelAuthError(f"القناة {channel_id} غير مربوطة.")
    info = json.loads(cipher.decrypt(channel.credentials_enc))
    creds = Credentials.from_authorized_user_info(info, SCOPES)
    if not creds.valid:
        try:
            creds.refresh(Request())
        except RefreshError as exc:
            raise ChannelAuthError(
                f"انتهت صلاحية ربط القناة «{channel.title}». أعد ربطها. "
                "(إذا كان التطبيق في وضع Testing فالربط ينتهي كل 7 أيام.)"
            ) from exc
        db.update_credentials(channel_id, cipher.encrypt(creds.to_json()))
    return creds


def disconnect(db: Database, cipher: TokenCipher, channel_id: str, revoke: bool = True) -> bool:
    """Delete stored credentials; optionally revoke them at Google. Returns True if revoked."""
    channel = db.get_channel(channel_id)
    if channel is None:
        return False
    revoked = False
    if revoke:
        try:
            info = json.loads(cipher.decrypt(channel.credentials_enc))
            token = info.get("refresh_token") or info.get("token")
            r = requests.post("https://oauth2.googleapis.com/revoke", params={"token": token}, timeout=15)
            revoked = r.status_code == 200
        except Exception:  # noqa: BLE001 - we still delete locally
            revoked = False
    db.delete_channel(channel_id)
    return revoked
