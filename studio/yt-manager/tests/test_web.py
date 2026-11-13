import json

from fastapi.testclient import TestClient

from app.context import AppContext
from app.uploader import Uploader
from app.web.main import create_app

from .conftest import CHANNEL_A, fake_loader


class Ctx(AppContext):
    @property
    def uploader(self):
        return Uploader(self.settings, self.db, self.cipher, self.services, credentials_loader=fake_loader)


def client(settings, db, cipher, services):
    return TestClient(create_app(Ctx(settings, db, cipher, services)))


def test_dashboard_lists_channels(settings, db, cipher, services, connected):
    r = client(settings, db, cipher, services).get("/")
    assert r.status_code == 200 and "قناة أ" in r.text and "Channel B" in r.text
    assert "وضع التجربة فقط" in r.text


def test_upload_form_has_no_default_channel(settings, db, cipher, services, connected):
    r = client(settings, db, cipher, services).get("/upload")
    assert 'value="" selected disabled' in r.text


def test_dry_run_via_web_does_not_upload_and_live_is_disabled(settings, db, cipher, services, connected, videos):
    c = client(settings, db, cipher, services)
    with open(videos["vertical"], "rb") as fh:
        r = c.post("/upload", data={"channel_id": CHANNEL_A, "kind": "short", "title": "تجربة",
                                    "hashtags": "طبخ", "add_shorts_hashtag": "true"},
                   files={"file": ("v.mp4", fh, "video/mp4")})
    assert r.status_code == 200, r.text
    assert "المعاينة ناجحة" in r.text and "#Shorts" in r.text
    assert "videos.insert" not in services.all_calls
    token = r.text.split("/upload/")[1].split("/live")[0]
    r = c.post(f"/upload/{token}/live", data={"confirm_channel_title": "قناة أ"})
    assert "LIVE_UPLOADS_ENABLED" in r.text
    assert "videos.insert" not in services.all_calls
    # the channel used at the live step comes from the server-side record, not the form
    params = json.loads((settings.uploads_dir / f"{token}.json").read_text("utf-8"))
    assert params["channel_id"] == CHANNEL_A


def test_cross_origin_post_rejected(settings, db, cipher, services, connected):
    r = client(settings, db, cipher, services).post(f"/channels/{CHANNEL_A}/remove",
                                                    headers={"origin": "https://evil.example"})
    assert r.status_code == 403
    assert db.get_channel(CHANNEL_A) is not None
