"""Inspect video files with ffprobe and decide Short eligibility."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".wmv", ".flv", ".webm", ".mkv", ".mpeg", ".mpg", ".3gp"}
SHORT_MAX_SECONDS = 180  # Shorts: up to 3 minutes, square or vertical


class MediaError(RuntimeError):
    pass


@dataclass
class MediaInfo:
    path: Path
    size_bytes: int
    duration_seconds: float
    width: int
    height: int

    @property
    def orientation(self) -> str:
        if self.width == self.height:
            return "square"
        return "vertical" if self.height > self.width else "horizontal"

    @property
    def short_eligible(self) -> bool:
        return self.duration_seconds <= SHORT_MAX_SECONDS and self.orientation in {"vertical", "square"}


def probe(path: str | Path) -> MediaInfo:
    path = Path(path)
    if not path.is_file():
        raise MediaError(f"الملف غير موجود: {path}")
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise MediaError(f"امتداد غير مدعوم: {path.suffix}")
    try:
        proc = subprocess.run(
            ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
            capture_output=True, text=True, timeout=60, check=True,
        )
    except FileNotFoundError as exc:
        raise MediaError("ffprobe غير مثبت (ثبّت ffmpeg).") from exc
    except subprocess.CalledProcessError as exc:
        raise MediaError(f"تعذر قراءة الفيديو: {exc.stderr.strip()[:200]}") from exc
    data = json.loads(proc.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video:
        raise MediaError("لا يوجد مسار فيديو في الملف.")
    width, height = int(video.get("width", 0)), int(video.get("height", 0))
    rotation = _rotation(video)
    if rotation in (90, 270):
        width, height = height, width
    duration = float(data.get("format", {}).get("duration") or video.get("duration") or 0)
    return MediaInfo(path=path, size_bytes=path.stat().st_size, duration_seconds=duration,
                     width=width, height=height)


def _rotation(stream: dict) -> int:
    rot = stream.get("tags", {}).get("rotate")
    for sd in stream.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = sd["rotation"]
    try:
        return abs(int(float(rot))) % 360 if rot is not None else 0
    except ValueError:
        return 0
