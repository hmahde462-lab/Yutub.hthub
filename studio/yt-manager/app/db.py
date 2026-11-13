"""SQLite storage: channels, encrypted credentials, upload jobs, quota usage, OAuth states."""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS channels (
    channel_id      TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    custom_url      TEXT,
    thumbnail_url   TEXT,
    credentials_enc BLOB NOT NULL,
    scopes          TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS oauth_states (
    state         TEXT PRIMARY KEY,
    code_verifier TEXT,
    created_at    REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS upload_jobs (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id       TEXT NOT NULL,
    file_path        TEXT NOT NULL,
    video_kind       TEXT NOT NULL,
    mode             TEXT NOT NULL,          -- dry_run | live
    status           TEXT NOT NULL,          -- validated | blocked | uploading | uploaded | failed
    request_body     TEXT NOT NULL,
    youtube_video_id TEXT,
    messages         TEXT NOT NULL DEFAULT '[]',
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS quota_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    day        TEXT NOT NULL,                -- Pacific-time day would be exact; UTC is close enough
    operation  TEXT NOT NULL,
    units      INTEGER NOT NULL,
    channel_id TEXT,
    created_at TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


@dataclass
class Channel:
    channel_id: str
    title: str
    custom_url: str | None
    thumbnail_url: str | None
    credentials_enc: bytes
    scopes: list[str]
    created_at: str
    updated_at: str


class Database:
    def __init__(self, path: Path | str):
        self.path = str(path)
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ---- channels -------------------------------------------------------
    def upsert_channel(self, channel_id: str, title: str, custom_url: str | None,
                       thumbnail_url: str | None, credentials_enc: bytes, scopes: list[str]) -> None:
        now = _now()
        with self.connect() as conn:
            conn.execute(
                """INSERT INTO channels (channel_id, title, custom_url, thumbnail_url, credentials_enc,
                                         scopes, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(channel_id) DO UPDATE SET
                     title=excluded.title, custom_url=excluded.custom_url,
                     thumbnail_url=excluded.thumbnail_url, credentials_enc=excluded.credentials_enc,
                     scopes=excluded.scopes, updated_at=excluded.updated_at""",
                (channel_id, title, custom_url, thumbnail_url, credentials_enc, json.dumps(scopes), now, now),
            )

    def update_credentials(self, channel_id: str, credentials_enc: bytes) -> None:
        with self.connect() as conn:
            conn.execute("UPDATE channels SET credentials_enc=?, updated_at=? WHERE channel_id=?",
                         (credentials_enc, _now(), channel_id))

    def get_channel(self, channel_id: str) -> Channel | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM channels WHERE channel_id=?", (channel_id,)).fetchone()
        return self._row_to_channel(row) if row else None

    def list_channels(self) -> list[Channel]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM channels ORDER BY title COLLATE NOCASE").fetchall()
        return [self._row_to_channel(r) for r in rows]

    def delete_channel(self, channel_id: str) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM channels WHERE channel_id=?", (channel_id,))

    @staticmethod
    def _row_to_channel(row: sqlite3.Row) -> Channel:
        return Channel(
            channel_id=row["channel_id"], title=row["title"], custom_url=row["custom_url"],
            thumbnail_url=row["thumbnail_url"], credentials_enc=row["credentials_enc"],
            scopes=json.loads(row["scopes"]), created_at=row["created_at"], updated_at=row["updated_at"],
        )

    # ---- oauth states ---------------------------------------------------
    def save_oauth_state(self, state: str, code_verifier: str | None) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM oauth_states WHERE created_at < ?", (time.time() - 900,))
            conn.execute("INSERT INTO oauth_states (state, code_verifier, created_at) VALUES (?, ?, ?)",
                         (state, code_verifier, time.time()))

    def pop_oauth_state(self, state: str) -> tuple[bool, str | None]:
        """Return (valid, code_verifier). States are single-use and expire after 15 minutes."""
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM oauth_states WHERE state=?", (state,)).fetchone()
            conn.execute("DELETE FROM oauth_states WHERE state=?", (state,))
        if not row or row["created_at"] < time.time() - 900:
            return False, None
        return True, row["code_verifier"]

    # ---- upload jobs ----------------------------------------------------
    def create_job(self, channel_id: str, file_path: str, video_kind: str, mode: str, status: str,
                   request_body: dict, messages: list[str]) -> int:
        now = _now()
        with self.connect() as conn:
            cur = conn.execute(
                """INSERT INTO upload_jobs (channel_id, file_path, video_kind, mode, status, request_body,
                                            messages, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (channel_id, file_path, video_kind, mode, status, json.dumps(request_body, ensure_ascii=False),
                 json.dumps(messages, ensure_ascii=False), now, now),
            )
            return int(cur.lastrowid)

    def update_job(self, job_id: int, status: str, youtube_video_id: str | None = None,
                   messages: list[str] | None = None) -> None:
        with self.connect() as conn:
            if messages is not None:
                conn.execute("UPDATE upload_jobs SET status=?, youtube_video_id=?, messages=?, updated_at=? WHERE id=?",
                             (status, youtube_video_id, json.dumps(messages, ensure_ascii=False), _now(), job_id))
            else:
                conn.execute("UPDATE upload_jobs SET status=?, youtube_video_id=?, updated_at=? WHERE id=?",
                             (status, youtube_video_id, _now(), job_id))

    def list_jobs(self, limit: int = 50) -> list[dict]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM upload_jobs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) | {"messages": json.loads(r["messages"])} for r in rows]

    # ---- quota ----------------------------------------------------------
    def log_quota(self, operation: str, units: int, channel_id: str | None = None) -> None:
        with self.connect() as conn:
            conn.execute("INSERT INTO quota_log (day, operation, units, channel_id, created_at) VALUES (?, ?, ?, ?, ?)",
                         (_today(), operation, units, channel_id, _now()))

    def quota_used_today(self) -> int:
        with self.connect() as conn:
            row = conn.execute("SELECT COALESCE(SUM(units), 0) AS s FROM quota_log WHERE day=?", (_today(),)).fetchone()
        return int(row["s"])
