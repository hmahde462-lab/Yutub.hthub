import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from app.config import Settings
from app.crypto import TokenCipher, generate_key
from app.db import Database
from app.uploader import Uploader

CHANNEL_A = "UCaaaaaaaaaaaaaaaaaaaaaa"
CHANNEL_B = "UCbbbbbbbbbbbbbbbbbbbbbb"


class _Exec:
    def __init__(self, value):
        self.value = value

    def execute(self):
        return self.value


class FakeInsertRequest:
    def __init__(self, yt):
        self.yt = yt

    def next_chunk(self):
        return None, {"id": "VIDEO123"}


class FakeYouTube:
    """Minimal stand-in for the YouTube client. `owner` is whose credentials it was built from."""

    def __init__(self, owner: str):
        self.owner = owner
        self.calls: list[str] = []
        self.inserted: list[dict] = []

    def channels(self):
        return self

    def videos(self):
        return self

    def list(self, **kw):
        self.calls.append("channels.list")
        return _Exec({"items": [{"id": self.owner, "snippet": {"title": "x"}}]})

    def insert(self, part, body, media_body):
        self.calls.append("videos.insert")
        self.inserted.append(body)
        return FakeInsertRequest(self)


class FakeServices:
    def __init__(self):
        self.clients: list[FakeYouTube] = []

    def youtube(self, creds):
        yt = FakeYouTube(owner=creds["owner"])
        self.clients.append(yt)
        return yt

    @property
    def all_calls(self):
        return [c for yt in self.clients for c in yt.calls]


@pytest.fixture
def settings(tmp_path) -> Settings:
    (tmp_path / "uploads").mkdir()
    return Settings(data_dir=tmp_path, encryption_key=generate_key(), client_secrets_file=tmp_path / "none.json",
                    redirect_uri="http://localhost:8000/oauth/callback", live_uploads_enabled=False,
                    daily_quota=10000, upload_quota_cost=1600)


@pytest.fixture
def db(settings):
    return Database(settings.db_path)


@pytest.fixture
def cipher(settings):
    return TokenCipher(settings.encryption_key)


@pytest.fixture
def connected(db, cipher):
    """Two channels. Credential 'owner' simulates whose Google account the token really belongs to."""
    db.upsert_channel(CHANNEL_A, "قناة أ", "@a", None, cipher.encrypt('{"owner": "%s"}' % CHANNEL_A), [])
    db.upsert_channel(CHANNEL_B, "Channel B", "@b", None, cipher.encrypt('{"owner": "%s"}' % CHANNEL_B), [])


def fake_loader(db, cipher, channel_id):
    import json
    return json.loads(cipher.decrypt(db.get_channel(channel_id).credentials_enc))


@pytest.fixture
def services():
    return FakeServices()


@pytest.fixture
def make_uploader(settings, db, cipher, services):
    def _make(**overrides):
        s = replace(settings, **overrides)
        return Uploader(s, db, cipher, services, credentials_loader=fake_loader, sleep=lambda _: None)
    return _make


def _video(path: Path, w: int, h: int, seconds: float) -> Path:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={w}x{h}:d={seconds}",
                    "-pix_fmt", "yuv420p", str(path)], check=True)
    return path


@pytest.fixture(scope="session")
def videos(tmp_path_factory):
    d = tmp_path_factory.mktemp("media")
    return {
        "vertical": _video(d / "vertical.mp4", 360, 640, 2),
        "horizontal": _video(d / "horizontal.mp4", 640, 360, 2),
        "square": _video(d / "square.mp4", 400, 400, 1),
    }
