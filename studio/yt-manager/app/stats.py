"""Per-channel statistics. Every call uses only the selected channel's credentials."""
from __future__ import annotations

from datetime import date, timedelta

from googleapiclient.errors import HttpError

from . import auth
from .crypto import TokenCipher
from .db import Database
from .services import ServiceFactory
from .uploader import verify_channel_identity


def channel_stats(db: Database, cipher: TokenCipher, services: ServiceFactory, channel_id: str,
                  days: int = 28, recent: int = 10, credentials_loader=None) -> dict:
    load = credentials_loader or auth.load_credentials
    creds = load(db, cipher, channel_id)
    yt = services.youtube(creds)
    verify_channel_identity(yt, channel_id)

    ch = yt.channels().list(part="snippet,statistics,contentDetails", id=channel_id).execute()["items"][0]
    stats = ch.get("statistics", {})
    result: dict = {
        "channel_id": channel_id,
        "title": ch["snippet"]["title"],
        "subscribers": None if stats.get("hiddenSubscriberCount") else int(stats.get("subscriberCount", 0)),
        "views": int(stats.get("viewCount", 0)),
        "videos": int(stats.get("videoCount", 0)),
        "recent_videos": [],
        "analytics": None,
        "warnings": [],
    }
    calls = 2

    uploads = ch.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    if uploads:
        items = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=recent).execute()
        ids = [i["contentDetails"]["videoId"] for i in items.get("items", [])]
        calls += 1
        if ids:
            vids = yt.videos().list(part="snippet,statistics,status,contentDetails", id=",".join(ids)).execute()
            calls += 1
            for v in vids.get("items", []):
                s = v.get("statistics", {})
                result["recent_videos"].append({
                    "id": v["id"], "title": v["snippet"]["title"],
                    "published_at": v["snippet"].get("publishedAt"),
                    "privacy": v.get("status", {}).get("privacyStatus"),
                    "duration": v.get("contentDetails", {}).get("duration"),
                    "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                    "comments": int(s.get("commentCount", 0)),
                })
    db.log_quota("stats", calls, channel_id)

    end = date.today()
    start = end - timedelta(days=days)
    try:
        report = services.analytics(creds).reports().query(
            ids="channel==MINE", startDate=start.isoformat(), endDate=end.isoformat(),
            metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,comments",
        ).execute()
        headers = [h["name"] for h in report.get("columnHeaders", [])]
        rows = report.get("rows") or [[0] * len(headers)]
        result["analytics"] = {"days": days, **dict(zip(headers, rows[0]))}
    except HttpError as exc:
        result["warnings"].append(f"تعذر جلب YouTube Analytics: {exc.reason if hasattr(exc, 'reason') else exc}")
    return result
