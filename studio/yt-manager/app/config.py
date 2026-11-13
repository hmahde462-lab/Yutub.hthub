"""Settings loaded from environment variables (and an optional .env file)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    encryption_key: str | None
    client_secrets_file: Path
    redirect_uri: str
    # Live uploads are OFF unless explicitly enabled. Dry-run is the default.
    live_uploads_enabled: bool
    daily_quota: int
    upload_quota_cost: int

    @property
    def db_path(self) -> Path:
        return self.data_dir / "ytm.sqlite3"

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"


def get_settings() -> Settings:
    _load_dotenv(Path(os.environ.get("YTM_ENV_FILE", ".env")))
    data_dir = Path(os.environ.get("YTM_DATA_DIR", "./data")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "uploads").mkdir(exist_ok=True)
    redirect_uri = os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:8000/oauth/callback")
    if redirect_uri.startswith("http://localhost") or redirect_uri.startswith("http://127.0.0.1"):
        # oauthlib refuses plain http unless told this is a local dev redirect.
        os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")
    # Google may return scopes in a different order / with previously granted ones.
    os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "1")
    return Settings(
        data_dir=data_dir,
        encryption_key=os.environ.get("YTM_ENCRYPTION_KEY") or None,
        client_secrets_file=Path(os.environ.get("GOOGLE_CLIENT_SECRETS_FILE", "./client_secret.json")),
        redirect_uri=redirect_uri,
        live_uploads_enabled=_bool(os.environ.get("LIVE_UPLOADS_ENABLED"), False),
        daily_quota=int(os.environ.get("YTM_DAILY_QUOTA", "10000")),
        upload_quota_cost=int(os.environ.get("YTM_UPLOAD_QUOTA_COST", "1600")),
    )
