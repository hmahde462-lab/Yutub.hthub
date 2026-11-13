# ملاحظات مهمة (اقرأها أول كل جلسة)

## المستخدم
- عراقي — رد باللهجة العراقية، **ردود قصيرة جداً** (توفير توكن). لا تعيد الكليشات إلا إذا طلب. لا تبدأ شغل كبير بدون طلب.
- لا تنشر أي فيديو بدون موافقته. لا تصرف كردت vidIQ/Higgsfield بدون موافقة.
- لا تقبل مفاتيح API بالمحادثة — تنحط بـ Settings → Network secrets.

## القنوات
راجع `studio/CHANNELS.md`.
- **لقطة WOW | WOW SHOTS** (@WowShotsIQ): كرات فقط. نشر عبر Metricool (براند 7ll.ajr، blogId 7966173، Asia/Baghdad) يوتيوب + تيك توك + إنستا ريلز.
- **Strange thoughts افكار غريبة** (@افكارغريبة2002): خدع بصرية + أسئلة أطفال (ستيك مان بصوت) فقط. المستخدم ينشر يدوي 4 يومياً: 12:30 خدعة، 4:30 أسئلة، 8:00 خدعة، 11:00 أسئلة.

## المجدول (Metricool)
- 30 شورت كرات (تقطيع/قتال/معارك 1–10): من 9/11 إلى 18/11، الساعة 15:00 / 19:00 / 22:00.
- فيديو البطولة الطويل (كأس عالم الكرات، 8 دقائق) يوتيوب فقط — الثلاثاء 10/11 20:30. البطل: أمريكا.
- روابط الميديا: `https://raw.githubusercontent.com/hmahde462-lab/Yutub.hthub/main/videos/...`

## افكار غريبة — الجاهز والمطلوب
- جاهز: خدع il01–il05، أسئلة جزء 3 و 4 (`videos/afkar/`).
- مطلوب: أسئلة 5,6,7,8 + خدع il06,il07,il08.

## الصوت (Gemini TTS)
- Network secret: host `generativelanguage.googleapis.com`، header `x-goog-api-key` (البروكسي يحقن المفتاح؛ ابعث dummy).
- مجاني ~10 طلبات/يوم لكل موديل → طلب واحد لكل فيديو ثم قصّ عند السكتات.
- موديل افتراضي: `gemini-3.1-flash-tts-preview` (بدائل: gemini-2.5-flash-preview-tts، gemini-2.5-pro-preview-tts).
- لا تكتب تعليمات أسلوب بالنص (يقرأها). أصوات: Puck (ولد)، Algieba (قصص)، Sulafat (أم). يدعم multiSpeakerVoiceConfig.
- كود: `studio/whiteboard-p3/tts.py`.

## الكود
`studio/physics-series/`: محركات الكرات (arena/battle/duel/tour) — رندر Playwright → ffmpeg. `studio/whiteboard-p*/`: فيديوهات الأسئلة.

## أخرى
- `videos/extra/gta6-hamoudi-voiced.mp4`: مقطع كوميدي (حمودي و GTA 6) بصوت Gemini.
- `videos/extra/top10-worst-people-stickman.mp4`: غير مخصص لقناة.
- Kling (klingai.com) مجاني محدود لتوليد 3D.
