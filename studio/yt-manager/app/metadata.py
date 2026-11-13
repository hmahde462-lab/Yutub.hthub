"""Validation and assembly of title / description / tags / hashtags."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

TITLE_MAX_CHARS = 100
DESCRIPTION_MAX_BYTES = 5000
TAGS_MAX_CHARS = 500
HASHTAGS_HARD_LIMIT = 60       # above this YouTube ignores ALL hashtags on the video
HASHTAGS_RECOMMENDED = 15
PRIVACY_VALUES = {"private", "unlisted", "public"}
_HASHTAG_RE = re.compile(r"#[^\s#]+")
_FORBIDDEN = ("<", ">")


@dataclass
class VideoMetadata:
    title: str
    description: str = ""
    tags: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    privacy: str = "private"
    category_id: str = "22"            # People & Blogs
    made_for_kids: bool = False
    default_language: str | None = None
    add_shorts_hashtag: bool = True    # only applied to Shorts


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_list(raw: str | list[str] | None) -> list[str]:
    """Accept comma / newline separated text or a list; strip and de-duplicate (case-insensitive)."""
    if raw is None:
        return []
    items = raw if isinstance(raw, list) else re.split(r"[,\n،]", raw)
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        item = item.strip()
        if item and item.lower() not in seen:
            seen.add(item.lower())
            out.append(item)
    return out


def normalize_hashtag(tag: str) -> str:
    tag = re.sub(r"\s+", "", tag.strip().lstrip("#"))
    return f"#{tag}" if tag else ""


def tags_length(tags: list[str]) -> int:
    """Length as YouTube counts it: tags containing spaces are wrapped in quotes, joined by commas."""
    total = sum(len(t) + (2 if " " in t else 0) for t in tags)
    return total + max(len(tags) - 1, 0)


def build_description(meta: VideoMetadata, is_short: bool) -> str:
    hashtags = [h for h in (normalize_hashtag(t) for t in meta.hashtags) if h]
    if is_short and meta.add_shorts_hashtag and "#shorts" not in {h.lower() for h in hashtags} \
            and "#shorts" not in meta.description.lower() and "#shorts" not in meta.title.lower():
        hashtags.append("#Shorts")
    existing = {h.lower() for h in _HASHTAG_RE.findall(meta.description)}
    hashtags = [h for h in hashtags if h.lower() not in existing]
    description = meta.description.rstrip()
    if hashtags:
        description = f"{description}\n\n{' '.join(hashtags)}" if description else " ".join(hashtags)
    return description


def validate(meta: VideoMetadata, is_short: bool) -> tuple[ValidationResult, dict]:
    """Validate metadata and return (result, snippet/status body for videos.insert)."""
    result = ValidationResult()
    title = meta.title.strip()
    description = build_description(meta, is_short)
    tags = parse_list(meta.tags)

    if not title:
        result.errors.append("العنوان مطلوب.")
    if len(title) > TITLE_MAX_CHARS:
        result.errors.append(f"العنوان {len(title)} حرف، والحد الأقصى {TITLE_MAX_CHARS}.")
    for label, text in (("العنوان", title), ("الوصف", description)):
        if any(c in text for c in _FORBIDDEN):
            result.errors.append(f"{label} يحتوي على < أو > وهذا غير مسموح في YouTube.")
    desc_bytes = len(description.encode("utf-8"))
    if desc_bytes > DESCRIPTION_MAX_BYTES:
        result.errors.append(f"الوصف {desc_bytes} بايت، والحد الأقصى {DESCRIPTION_MAX_BYTES} (الحرف العربي = 2 بايت).")

    for tag in tags:
        if any(c in tag for c in _FORBIDDEN):
            result.errors.append(f"الكلمة المفتاحية «{tag}» تحتوي على < أو >.")
    tlen = tags_length(tags)
    if tlen > TAGS_MAX_CHARS:
        result.errors.append(f"مجموع الكلمات المفتاحية {tlen} حرف، والحد الأقصى {TAGS_MAX_CHARS}.")

    hashtag_count = len({h.lower() for h in _HASHTAG_RE.findall(f"{title} {description}")})
    if hashtag_count > HASHTAGS_HARD_LIMIT:
        result.errors.append(f"عدد الهاشتاغات {hashtag_count}؛ فوق {HASHTAGS_HARD_LIMIT} يتجاهلها YouTube كلها.")
    elif hashtag_count > HASHTAGS_RECOMMENDED:
        result.warnings.append(f"عدد الهاشتاغات {hashtag_count}؛ يُنصح بـ {HASHTAGS_RECOMMENDED} أو أقل.")

    if meta.privacy not in PRIVACY_VALUES:
        result.errors.append(f"قيمة الخصوصية غير صحيحة: {meta.privacy}")
    elif meta.privacy == "public":
        result.warnings.append("الخصوصية «عام»: سيظهر الفيديو للجميع فور الرفع الفعلي.")

    snippet: dict = {"title": title, "description": description, "categoryId": meta.category_id}
    if tags:
        snippet["tags"] = tags
    if meta.default_language:
        snippet["defaultLanguage"] = meta.default_language
    body = {
        "snippet": snippet,
        "status": {"privacyStatus": meta.privacy, "selfDeclaredMadeForKids": meta.made_for_kids},
    }
    return result, body
