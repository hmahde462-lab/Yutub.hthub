"""Command line interface. Uploads are dry-run unless --live is passed (and enabled in settings)."""
from __future__ import annotations

import json

import typer

from . import auth
from .crypto import generate_key
from .metadata import VideoMetadata, parse_list

app = typer.Typer(help="إدارة عدة قنوات YouTube", no_args_is_help=True)
channels_app = typer.Typer(help="القنوات المربوطة", no_args_is_help=True)
app.add_typer(channels_app, name="channels")


def _ctx():
    from .context import build_context
    return build_context()


@app.command("init-key")
def init_key():
    """أنشئ مفتاح تشفير جديداً وضعه في .env كـ YTM_ENCRYPTION_KEY."""
    typer.echo(generate_key())


@channels_app.command("list")
def channels_list():
    ctx = _ctx()
    chans = ctx.db.list_channels()
    if not chans:
        typer.echo("لا توجد قنوات مربوطة. اربط قناة من لوحة الويب: /channels/connect")
    for c in chans:
        typer.echo(f"{c.channel_id}  {c.title}  {c.custom_url or ''}")


@channels_app.command("remove")
def channels_remove(channel_id: str, no_revoke: bool = typer.Option(False, help="لا تلغِ الصلاحية عند Google")):
    ctx = _ctx()
    ch = ctx.db.get_channel(channel_id)
    if not ch:
        raise typer.Exit("القناة غير موجودة")
    typer.confirm(f"فصل القناة «{ch.title}»؟", abort=True)
    revoked = auth.disconnect(ctx.db, ctx.cipher, channel_id, revoke=not no_revoke)
    typer.echo("تم الفصل" + (" وإلغاء الصلاحية عند Google." if revoked else "."))


@app.command()
def upload(
    channel: str = typer.Option(..., "--channel", "-c", help="معرّف القناة (إجباري، لا توجد قناة افتراضية)"),
    file: str = typer.Option(..., "--file", "-f"),
    kind: str = typer.Option(..., "--kind", "-k", help="short أو long"),
    title: str = typer.Option(..., "--title", "-t"),
    description: str = typer.Option("", "--description", "-d"),
    tags: str = typer.Option("", help="كلمات مفتاحية مفصولة بفواصل"),
    hashtags: str = typer.Option("", help="هاشتاغات مفصولة بفواصل"),
    privacy: str = typer.Option("private", help="private | unlisted | public"),
    made_for_kids: bool = typer.Option(False, "--made-for-kids"),
    no_shorts_tag: bool = typer.Option(False, "--no-shorts-tag", help="لا تضف #Shorts تلقائياً"),
    live: bool = typer.Option(False, "--live", help="نشر فعلي. بدونه يكون وضع تجربة فقط."),
):
    """ارفع فيديو. الافتراضي وضع تجربة (Dry-run) لا يرسل الفيديو."""
    if kind not in ("short", "long"):
        raise typer.BadParameter("kind يجب أن يكون short أو long")
    ctx = _ctx()
    ch = ctx.db.get_channel(channel)
    if not ch:
        raise typer.Exit(f"القناة {channel} غير مربوطة.")
    confirm = None
    if live:
        typer.secho(f"⚠️  نشر فعلي على القناة: {ch.title} ({ch.channel_id})", fg="yellow")
        confirm = typer.prompt("اكتب اسم القناة بالضبط للتأكيد")
    from .uploader import UploadRequest
    meta = VideoMetadata(title=title, description=description, tags=parse_list(tags),
                         hashtags=parse_list(hashtags), privacy=privacy, made_for_kids=made_for_kids,
                         add_shorts_hashtag=not no_shorts_tag)
    out = ctx.uploader.run(UploadRequest(channel, file, kind, meta, live=live, confirm_channel_title=confirm),
                           progress=lambda p: typer.echo(f"  {p:.0%}"))
    typer.echo(f"الوضع: {'نشر فعلي' if out.mode == 'live' else 'تجربة (لم يُرفع شيء)'} | الحالة: {out.status} | القناة: {out.channel_title}")
    if out.media:
        m = out.media
        typer.echo(f"الملف: {m.width}x{m.height} {m.orientation}، {m.duration_seconds:.1f} ث، {m.size_bytes / 1e6:.1f} MB")
    for e in out.errors:
        typer.secho(f"✗ {e}", fg="red")
    for w in out.warnings:
        typer.secho(f"! {w}", fg="yellow")
    typer.echo("الطلب الذي سيُرسل:")
    typer.echo(json.dumps(out.body, ensure_ascii=False, indent=2))
    if out.video_id:
        typer.secho(f"✓ رابط الفيديو: https://youtu.be/{out.video_id}", fg="green")
    raise typer.Exit(0 if out.ok else 1)


@app.command()
def stats(channel: str = typer.Option(..., "--channel", "-c")):
    """إحصائيات قناة واحدة."""
    from .stats import channel_stats
    ctx = _ctx()
    typer.echo(json.dumps(channel_stats(ctx.db, ctx.cipher, ctx.services, channel), ensure_ascii=False, indent=2))


@app.command()
def quota():
    ctx = _ctx()
    typer.echo(f"المستخدم اليوم: {ctx.db.quota_used_today()} / {ctx.settings.daily_quota}")


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000):
    """شغّل لوحة الويب (محلياً فقط افتراضياً)."""
    import uvicorn
    uvicorn.run("app.web.main:app", host=host, port=port)


if __name__ == "__main__":
    app()
