# yt-studio

مساحة العمل لإدارة قنوات YouTube وصناعة الـ Shorts.

| المجلد | المحتوى |
|---|---|
| `yt-manager/` | نظام ربط عدة قنوات والرفع (OAuth لكل قناة، وضع تجربة افتراضي، حماية من النشر بقناة غلط) |
| `afkar-video/` | مولّد فيديو الوايت بورد (HarfBuzz + Playwright + ffmpeg) وأول Short لقناة أفكار غريبة |
| `.claude/skills/` | مهارات Claude: `tiktok-reel-hook-generator` و `video-comprehend` |
| `.claude/agents/` | وكيل `video-analyzer` |

## جلسة جديدة
```bash
./setup.sh
```

لا تُرفع الأسرار أبداً: `.env` و`client_secret.json` وقاعدة بيانات التوكنات مستثناة في `.gitignore`.
