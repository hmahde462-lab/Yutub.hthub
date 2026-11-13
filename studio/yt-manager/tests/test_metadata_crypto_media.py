import pytest

from app.crypto import CryptoError, TokenCipher, generate_key
from app.media import MediaError, probe
from app.metadata import VideoMetadata, build_description, parse_list, tags_length, validate


def test_cipher_roundtrip_and_wrong_key():
    c = TokenCipher(generate_key())
    token = c.encrypt('{"refresh_token": "secret"}')
    assert b"secret" not in token
    assert c.decrypt(token) == '{"refresh_token": "secret"}'
    with pytest.raises(CryptoError):
        TokenCipher(generate_key()).decrypt(token)
    with pytest.raises(CryptoError):
        TokenCipher(None)


def test_parse_list_handles_arabic_comma_and_duplicates():
    assert parse_list("طبخ، وصفات, Cooking,cooking\nأكل") == ["طبخ", "وصفات", "Cooking", "أكل"]


def test_hashtags_appended_and_shorts_only_for_shorts():
    meta = VideoMetadata(title="t", description="وصف", hashtags=["طبخ", "#وصفات سريعة"])
    assert build_description(meta, is_short=True) == "وصف\n\n#طبخ #وصفاتسريعة #Shorts"
    assert build_description(meta, is_short=False) == "وصف\n\n#طبخ #وصفاتسريعة"
    meta.add_shorts_hashtag = False
    assert "#Shorts" not in build_description(meta, is_short=True)


def test_existing_hashtags_not_duplicated():
    meta = VideoMetadata(title="t", description="hi #shorts #طبخ", hashtags=["طبخ"])
    assert build_description(meta, is_short=True) == "hi #shorts #طبخ"


def test_validation_limits():
    res, _ = validate(VideoMetadata(title="x" * 101), is_short=False)
    assert any("100" in e for e in res.errors)
    res, _ = validate(VideoMetadata(title="a <b>"), is_short=False)
    assert not res.ok
    res, _ = validate(VideoMetadata(title="ok", description="ع" * 2600), is_short=False)  # 5200 bytes
    assert any("بايت" in e for e in res.errors)
    res, _ = validate(VideoMetadata(title="ok", tags=[f"word{i}" * 20 for i in range(5)]), is_short=False)
    assert any("500" in e for e in res.errors)
    res, _ = validate(VideoMetadata(title="ok", hashtags=[f"h{i}" for i in range(61)]), is_short=False)
    assert any("60" in e for e in res.errors)
    res, _ = validate(VideoMetadata(title=""), is_short=False)
    assert not res.ok


def test_tags_length_counts_quotes():
    assert tags_length(["a b", "c"]) == 3 + 2 + 1 + 1


def test_body_shape():
    res, body = validate(VideoMetadata(title=" عنوان ", tags=["a"], privacy="unlisted"), is_short=False)
    assert res.ok
    assert body["snippet"]["title"] == "عنوان"
    assert body["status"] == {"privacyStatus": "unlisted", "selfDeclaredMadeForKids": False}


def test_probe(videos, tmp_path):
    v = probe(videos["vertical"])
    assert (v.width, v.height, v.orientation, v.short_eligible) == (360, 640, "vertical", True)
    assert probe(videos["horizontal"]).short_eligible is False
    assert probe(videos["square"]).short_eligible is True
    with pytest.raises(MediaError):
        probe(tmp_path / "missing.mp4")
    bad = tmp_path / "x.txt"
    bad.write_text("no")
    with pytest.raises(MediaError):
        probe(bad)
