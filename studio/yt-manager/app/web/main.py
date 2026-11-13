"""Local web dashboard (FastAPI + Jinja). Bind to 127.0.0.1 only."""
from __future__ import annotations

import json
import secrets
import shutil
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .. import auth
from ..context import AppContext, build_context
from ..media import ALLOWED_EXTENSIONS
from ..metadata import VideoMetadata, parse_list
from ..stats import channel_stats
from ..uploader import UploadRequest

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def create_app(ctx: AppContext | None = None) -> FastAPI:
    app = FastAPI(title="YT Manager")
    app.state.ctx = ctx

    def get_ctx() -> AppContext:
        if app.state.ctx is None:
            app.state.ctx = build_context()
        return app.state.ctx

    @app.middleware("http")
    async def same_origin_posts(request: Request, call_next):
        # Basic CSRF protection: reject cross-site form posts.
        if request.method == "POST":
            origin = request.headers.get("origin") or request.headers.get("referer")
            if origin and urlparse(origin).netloc != request.url.netloc:
                return HTMLResponse("طلب من مصدر غير موثوق", status_code=403)
        return await call_next(request)

    def render(request: Request, name: str, **kw):
        c = get_ctx()
        kw.setdefault("live_enabled", c.settings.live_uploads_enabled)
        kw.setdefault("quota_used", c.db.quota_used_today())
        kw.setdefault("quota_limit", c.settings.daily_quota)
        kw.setdefault("msg", request.query_params.get("msg"))
        return templates.TemplateResponse(request, name, kw)

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        c = get_ctx()
        return render(request, "index.html", channels=c.db.list_channels(), jobs=c.db.list_jobs(15))

    @app.get("/channels/connect")
    def connect():
        c = get_ctx()
        try:
            return RedirectResponse(auth.start_connect(c.settings, c.db))
        except auth.ChannelAuthError as exc:
            return RedirectResponse(f"/?msg={exc}", status_code=303)

    @app.get("/oauth/callback")
    def oauth_callback(request: Request, state: str = "", error: str | None = None):
        if error:
            return RedirectResponse(f"/?msg=تم إلغاء الربط: {error}", status_code=303)
        c = get_ctx()
        try:
            ch = auth.finish_connect(c.settings, c.db, c.cipher, c.services, state, str(request.url))
        except Exception as exc:  # noqa: BLE001
            return RedirectResponse(f"/?msg=فشل الربط: {exc}", status_code=303)
        return RedirectResponse(f"/?msg=تم ربط القناة: {ch.title}", status_code=303)

    @app.post("/channels/{channel_id}/remove")
    def remove(channel_id: str):
        c = get_ctx()
        auth.disconnect(c.db, c.cipher, channel_id)
        return RedirectResponse("/?msg=تم فصل القناة", status_code=303)

    @app.get("/channels/{channel_id}/stats", response_class=HTMLResponse)
    def stats(request: Request, channel_id: str):
        c = get_ctx()
        if not c.db.get_channel(channel_id):
            raise HTTPException(404)
        try:
            data, error = channel_stats(c.db, c.cipher, c.services, channel_id), None
        except Exception as exc:  # noqa: BLE001
            data, error = None, str(exc)
        return render(request, "stats.html", data=data, error=error, channel=c.db.get_channel(channel_id))

    @app.get("/upload", response_class=HTMLResponse)
    def upload_form(request: Request):
        return render(request, "upload.html", channels=get_ctx().db.list_channels())

    @app.post("/upload", response_class=HTMLResponse)
    def upload_dry_run(
        request: Request,
        channel_id: str = Form(""), kind: str = Form(...), title: str = Form(...),
        description: str = Form(""), tags: str = Form(""), hashtags: str = Form(""),
        privacy: str = Form("private"), made_for_kids: bool = Form(False),
        add_shorts_hashtag: bool = Form(False), file: UploadFile = File(...),
    ):
        c = get_ctx()
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            return render(request, "upload.html", channels=c.db.list_channels(), msg=f"امتداد غير مدعوم: {suffix}")
        token = secrets.token_urlsafe(16)
        path = c.settings.uploads_dir / f"{token}{suffix}"
        with path.open("wb") as fh:
            shutil.copyfileobj(file.file, fh)
        params = dict(channel_id=channel_id, kind=kind, title=title, description=description,
                      tags=parse_list(tags), hashtags=parse_list(hashtags), privacy=privacy,
                      made_for_kids=made_for_kids, add_shorts_hashtag=add_shorts_hashtag,
                      file_path=str(path), original_name=file.filename)
        # Parameters are kept server-side, so the live step cannot be pointed at another channel.
        (c.settings.uploads_dir / f"{token}.json").write_text(json.dumps(params, ensure_ascii=False), "utf-8")
        out = c.uploader.run(_request(params, live=False))
        return render(request, "result.html", out=out, token=token, params=params)

    @app.post("/upload/{token}/live", response_class=HTMLResponse)
    def upload_live(request: Request, token: str, confirm_channel_title: str = Form("")):
        c = get_ctx()
        if not token.replace("-", "").replace("_", "").isalnum():
            raise HTTPException(400)
        pfile = c.settings.uploads_dir / f"{token}.json"
        if not pfile.exists():
            raise HTTPException(404, "انتهت صلاحية هذه المعاينة")
        params = json.loads(pfile.read_text("utf-8"))
        out = c.uploader.run(_request(params, live=True, confirm=confirm_channel_title))
        if out.status == "uploaded":
            pfile.unlink(missing_ok=True)
            Path(params["file_path"]).unlink(missing_ok=True)
        return render(request, "result.html", out=out, token=token, params=params)

    return app


def _request(p: dict, live: bool, confirm: str | None = None) -> UploadRequest:
    meta = VideoMetadata(title=p["title"], description=p["description"], tags=p["tags"],
                         hashtags=p["hashtags"], privacy=p["privacy"], made_for_kids=p["made_for_kids"],
                         add_shorts_hashtag=p["add_shorts_hashtag"])
    return UploadRequest(p["channel_id"], p["file_path"], p["kind"], meta, live=live, confirm_channel_title=confirm)


app = create_app()
