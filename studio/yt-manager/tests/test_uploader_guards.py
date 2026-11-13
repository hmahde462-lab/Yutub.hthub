from app.metadata import VideoMetadata
from app.uploader import UploadRequest

from .conftest import CHANNEL_A, CHANNEL_B


def req(path, channel=CHANNEL_A, kind="short", live=False, confirm=None, **meta):
    return UploadRequest(channel, str(path), kind, VideoMetadata(title=meta.pop("title", "عنوان"), **meta),
                         live=live, confirm_channel_title=confirm)


def test_no_channel_selected_is_blocked(make_uploader, connected, videos, services):
    out = make_uploader().run(req(videos["vertical"], channel=""))
    assert out.status == "blocked" and "اختيار قناة" in out.errors[0]
    assert services.all_calls == []


def test_unknown_channel_is_blocked(make_uploader, connected, videos, services):
    out = make_uploader().run(req(videos["vertical"], channel="UCunknown"))
    assert out.status == "blocked"
    assert services.all_calls == []


def test_dry_run_never_uploads(make_uploader, connected, videos, services, db):
    out = make_uploader(live_uploads_enabled=True).run(req(videos["vertical"]))
    assert out.ok and out.status == "validated" and out.mode == "dry_run"
    assert "videos.insert" not in services.all_calls
    assert services.all_calls == ["channels.list"]
    assert db.list_jobs()[0]["status"] == "validated"


def test_token_belonging_to_other_channel_is_blocked(make_uploader, connected, videos, services, db, cipher):
    # Corrupt channel A's stored token so it actually belongs to channel B.
    db.update_credentials(CHANNEL_A, cipher.encrypt('{"owner": "%s"}' % CHANNEL_B))
    out = make_uploader(live_uploads_enabled=True).run(req(videos["vertical"], live=True, confirm="قناة أ"))
    assert out.status == "blocked"
    assert any("حماية القناة" in e for e in out.errors)
    assert "videos.insert" not in services.all_calls


def test_live_disabled_blocks_before_any_network_call(make_uploader, connected, videos, services):
    out = make_uploader(live_uploads_enabled=False).run(req(videos["vertical"], live=True, confirm="قناة أ"))
    assert out.status == "blocked" and any("LIVE_UPLOADS_ENABLED" in e for e in out.errors)
    assert services.all_calls == []


def test_live_requires_exact_channel_title(make_uploader, connected, videos, services):
    up = make_uploader(live_uploads_enabled=True)
    for wrong in (None, "", "Channel B", "قناة"):
        out = up.run(req(videos["vertical"], live=True, confirm=wrong))
        assert out.status == "blocked"
    assert services.all_calls == []


def test_live_upload_goes_only_to_selected_channel(make_uploader, connected, videos, services, db):
    out = make_uploader(live_uploads_enabled=True).run(
        req(videos["horizontal"], channel=CHANNEL_B, kind="long", live=True, confirm="Channel B",
            tags=["a"], hashtags=["b"]))
    assert out.status == "uploaded" and out.video_id == "VIDEO123", out.errors
    [client] = services.clients
    assert client.owner == CHANNEL_B
    assert client.calls == ["channels.list", "videos.insert"]
    assert client.inserted[0]["status"]["privacyStatus"] == "private"
    assert db.quota_used_today() == 1601


def test_short_must_be_vertical_and_short(make_uploader, connected, videos, services):
    out = make_uploader().run(req(videos["horizontal"], kind="short"))
    assert out.status == "blocked" and any("Short" in e for e in out.errors)
    out = make_uploader().run(req(videos["vertical"], kind="long"))
    assert out.ok and any("Short" in w for w in out.warnings)


def test_quota_exhausted_blocks(make_uploader, connected, videos, db, services):
    db.log_quota("videos.insert", 9000)
    out = make_uploader().run(req(videos["vertical"]))
    assert out.status == "blocked" and any("الحصة" in e for e in out.errors)
    assert services.all_calls == []
