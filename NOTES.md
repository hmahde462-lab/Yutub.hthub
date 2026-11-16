# ملاحظات مهمة (اقرأها أول كل جلسة)

## المستخدم
- عراقي — رد باللهجة العراقية، **ردود قصيرة جداً** (توفير توكن). لا تعيد الكليشات إلا إذا طلب. لا تبدأ شغل كبير بدون طلب.
- لا تنشر أي فيديو بدون موافقته. لا تصرف كردت vidIQ/Higgsfield بدون موافقة.
- لا تقبل مفاتيح API بالمحادثة — تنحط بـ Settings → Network secrets.

## قاعدة الشورتات (مهم)
- الشورت ما يقبل صورة مصغّرة مرفوعة → الثمبنيل لازم يكون **جوه الفيديو**: فريم قصير جداً بالبداية (~0.2 ثانية) أو نص ثانية بالنهاية. سويه بصيغة عمودية 1080x1920.
- أداة: `studio/tools/add_cover.sh in.mp4 cover.jpg out.mp4 [0.2] [start|end]`.

## قاعدة ريلز القرآن (مهم)
- أي نص قرآني يطلع على الشاشة: الشيخ يقرأه **كامل وبصوت واضح** بدون انقطاع، والكتابة تطلع وتختفي على توقيت التلاوة بالضبط (ما تبقى الآية بدون صوت، ولا الصوت يوگف قبل ما تخلص الآية).
- استخدم تلاوة متصلة (ملف سورة كامل، قص على وقفات الشيخ الطبيعية) بدل لصق مقاطع آيات منفصلة؛ خلي هامش قبل وبعد حتى ما ينقص المد بالنهاية.
- أثناء التلاوة: لا مطر ولا أي صوت ثاني (أو خافت جداً)، وما تطلع كتابة غير قرآنية فوق التلاوة.
- مصدر: everyayah.com (Alafasy_128kbps/SSSAAA.mp3) — بس للنص القرآني الحقيقي، لا TTS أبداً للقرآن.

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
- `videos/extra/hamoudi-mama-gta-part2.mp4`: جزء 2 كارتون 2D (ماما تلعب وتاخذ 6 نجوم). كود: `studio/hamoudi-2d/` (animation-studio starter gully-cricket).
- `videos/long/top10-iraqi-food-ukiyoe.mp4`: فيديو طويل أطيب 10 أكلات عراقية بستايل أوكيو-إيه (3:15). كود: `studio/top10-ukiyoe/`. ونسخة الألعاب: `videos/long/top10-iraqi-games-ukiyoe.mp4` (2:30)، كود `studio/top10-ukiyoe/games/`.
- `videos/egypt/`: 5 حاجات بس المصريين بيعملوها (دمج فيديوين للمستخدم + صوت مصري Gemini Puck + ثمبنيل).

## معركة الأعلام (Countryballs) — 20 شورت
- كود: `studio/flag-battles/` (flagduel.html + rec.js + sound_duel.py، `make_one.sh N`). الحلقات والفايز ثابتين بـ episodes.json (seed)، لا تعيد tune.js. الفيديوهات: `videos/flags/flag-battle-NN.mp4`.
- براند Metricool الجديد: blogId 8090968، Asia/Baghdad، يوتيوب فقط (WOW SHOTS UCgsQ6WAsgA8rk0X3H4ifWPg). الخطة المجانية 20 منشور/شهر.
- الجدول: حلقتين يومياً 17:00 و 21:00 من 14/11 إلى 23/11/2026، Short عام، autoPublish. ثبّت أول تعليق بعد ما ينزل كل فيديو.

  1. العراق ضد السعودية — الفايز العراق — 2026-11-14 17:00
  2. مصر ضد المغرب — الفايز مصر — 2026-11-14 21:00
  3. البرازيل ضد الأرجنتين — الفايز البرازيل — 2026-11-15 17:00
  4. العراق ضد الأردن — الفايز الأردن — 2026-11-15 21:00
  5. الجزائر ضد تونس — الفايز تونس — 2026-11-16 17:00
  6. فرنسا ضد ألمانيا — الفايز ألمانيا — 2026-11-16 21:00
  7. الكويت ضد قطر — الفايز الكويت — 2026-11-17 17:00
  8. العراق ضد مصر — الفايز العراق — 2026-11-17 21:00
  9. إسبانيا ضد البرتغال — الفايز البرتغال — 2026-11-18 17:00
  10. السعودية ضد الإمارات — الفايز الإمارات — 2026-11-18 21:00
  11. المغرب ضد البرتغال — الفايز البرتغال — 2026-11-19 17:00
  12. العراق ضد اليابان — الفايز العراق — 2026-11-19 21:00
  13. إنجلترا ضد إيطاليا — الفايز إنجلترا — 2026-11-20 17:00
  14. سوريا ضد لبنان — الفايز سوريا — 2026-11-20 21:00
  15. أمريكا ضد المكسيك — الفايز المكسيك — 2026-11-21 17:00
  16. العراق ضد البرازيل — الفايز العراق — 2026-11-21 21:00
  17. الأرجنتين ضد فرنسا — الفايز فرنسا — 2026-11-22 17:00
  18. السعودية ضد الأرجنتين — الفايز الأرجنتين — 2026-11-22 21:00
  19. الجزائر ضد مصر — الفايز الجزائر — 2026-11-23 17:00
  20. العراق ضد الأرجنتين — الفايز العراق — 2026-11-23 21:00
- إنستا: نفس الـ20 ريلز مجدولة عبر vidIQ على @wowshotsiq بنفس المواعيد (14–23/11، 17:00 و 21:00). vidIQ ما يدعم أول تعليق ولا إلغاء المجدول.
- `videos/hamoudi/`: حمودي وماما الأجزاء 2–7 (3 راوتر، 4 شهادة، 5 ماما پرو، 6 كهرباء، 7 عيدية). كود الحلقات: `studio/hamoudi-2d/eps/` (film.js واحد، score لكل حلقة، صوت gemini-2.5-flash-preview-tts).

## الموسم 2 (معارك 21–81 + معلومات غريبة 1–61) — مجدول بالكامل عبر vidIQ
- يوتيوب WOW SHOTS (UCgsQ6WAsgA8rk0X3H4ifWPg) + إنستا @wowshotsiq (platformAccountId 29328143896822808).
- 24/11/2026 → 23/01/2027 يومياً: معركة 17:00، معلومات 21:00 (بغداد). 122 منشور كلها scheduled (ما تنلغي بـ vidIQ).
- معارك: `studio/flag-battles/` (episodes2.json، تتناوب دول/فرق، بدون أندية عراقية). معلومات: `studio/facts-series/` (facts.json، صوت ElevenLabs pNInz6obpgDQGcFmaJgB، `make_fact.sh N`). الفيديوهات `videos/flags/`, `videos/facts/`.
- ملفات الحالة: `studio/state/` (todo.json/todo2.json = النصوص والعناوين والأوقات، ids_b/ids_f = uploadIds بـ vidIQ، allev.json = جدول كل الحلقات).
- أول تعليق: vidIQ ما يدعمه.

## التجميعات الأسبوعية (فيديو طويل 16:9، يوتيوب فقط، 19:00 بغداد)
- كود: `studio/weekly/` — `plan.py` → comps.json (العناوين/الوصف بالفصول/التاغات/الوقت)، `render_art.js` (اللوحات الجانبية + الثمبنيل)، `build.sh kind week` / `all.sh`.
- الفيديوهات + الثمبنيلات: `videos/weekly/` (battle-weekNN.mp4، facts-weekNN.mp4، *-thumb.jpg).
- الثلاثاء: تجميعة المعارك (11 أسبوع، 17/11 → 26/01). الجمعة: تجميعة المعلومات (8، 04/12 → 29/01؛ الأسبوع الأول مدموج 1–10، والأخير 53–61).
- الحالة: يُحدَّث بـ `studio/state/weekly_progress.txt`.
- `studio/kahraba30/`: سلسلة «انقطاع الكهرباء ٣٠ يوم» ح١ — script.json، أصوات ElevenLabs (c0-c5.mp3، صوت Ahmed عبر Flows لأن الـAPI ممنوع بالمجاني)، cuts.json، build.py. الصور من Figma (ملف 1uwwhl4Z0MO9FAwkAy2cFz) — urls.txt (تنتهي بعد 7 أيام). ناقص صورتين (58,59) لأن كريدت Figma خلص.

## انقطاع الكهرباء ٣٠ يوم (سلسلة POV — ستايل راس أبيض داخل صورة واقعية)
- ح١ جاهزة: `videos/long/kahraba30-ep1.mp4` (4:50). ناقص صورتين (مشهد 58 الزقاق باللايت، 59 الظل) — مستبدلة بالمشهد 57. لإعادة البناء: `studio/kahraba30/build.py` (يحتاج img/ من urls.txt — روابط Figma تنتهي بعد 7 أيام).
- ح٢ «المدرسة والامتحانات»: السكربت `studio/kahraba30/ep2/ep2.json` (54 مشهد، 45 صورة جديدة) + الصوت جاهز e2c0..e2c4.mp3. الباقي: الصور (Figma) + تقطيع الصوت (gts.py بـ Gemini timestamps + تصحيح يدوي بالسكتات) + build.
- الصوت: ElevenLabs Flows (creative_generate_speech, eleven_v3, voice 6cFz1T5FQxQS8Xk88qQi, generations_count=1). الـAPI المباشر ممنوع للأصوات المكتبية بالخطة المجانية. رصيد باقي ≈3,000.
- الصور: Figma generate_image gpt-image-2.5-flare 1920x1080، نفس قالب البرومت (بـ script.json حقل prompt). كريدت الحساب القديم يخلص بسرعة (~52 صورة/يوم).
- الشبكة: أضفت elevenlabsusercontent.com و www.figma.com للبيئة.

### Weekly compilations — scheduled (2026-11-15)
All 19 uploaded via vidIQ to YouTube (private until publishAt, 19:00 Baghdad). Battles every Tuesday 17/11/2026–26/01/2027,
facts every Friday 04/12/2026–29/01/2027. Video links + postIds in `studio/state/weekly_ids.txt`.

## Session notes (2026-11-15)

### Weekly compilations — DONE
19/19 scheduled on YouTube via vidIQ (see section above). Nothing pending.
Lesson: YouTube daily upload limit (uploadLimitExceeded) after many uploads in one day → a failed vidIQ
publication can't be retried; create a NEW draft with the same uploadId/imageId and publish.

### Gun sound effects — `studio/sfx/guns/`
ElevenLabs sound-generation API (api.elevenlabs.io is proxy-authenticated, use dummy xi-api-key):
- Shots: rifle, shotgun, sniper, ak, smg, lmg (.mp3), all_guns_demo.mp3
- Reloads: reload.mp3 (generic charging handle) + rifle_/shotgun_/sniper_/ak_/smg_/lmg_reload.mp3
- Post-process: ffmpeg silenceremove + loudnorm.

### FPS weapon models for game "Magic Forest" — `studio/weapons/`
Procedural Blender (`pip install bpy` 5.3, headless) — NOT AAA quality; user was told honestly.
Higgsfield credits = 0, so no AI image-to-3D. Options offered: buy credits / buy assets (Sketchfab/Fab) / refine.
- `textures.py` → tex/ (procedural 2K PBR, gitignored), `lib.py` helpers, `weapons.py` builders.
- Output: `glb/` (2K) + `glb_mobile/` (1K): M4, AK47, LMG, Sniper, Shotgun, SMG, Optic_RedDot, Optic_Scope4x, Optic_SniperScope.
- Separate moving parts + Socket_* empties; muzzle −Z, metres, origin at grip. README.md there.
- Rebuild: `python3 textures.py 2048 && python3 weapons.py --preview --mobile`

### Environment
- graphify (graphifyy) installed; Default env setup script now installs it every new session.

## حساب vidIQ الجديد (15/11)
- الـ connector صار على حساب vidIQ ثاني: يوتيوب **افكار غريبة** UC8ttgcX1m2LioxDGTINJLIw + انستا **@7ll.ajr** (آيه من القرآن، 9.4K) id 28858832390455960 (OAuth، ينشر). حساب wowshotsiq ومنشوراته الـ138 ما تبين بعد.
- فحص يومي للربط: trigger trig_015mttUgRtJjsruA55Zy68D9 (12:37 بغداد).
- جاهز (ما انشر): `videos/afkar/il06-lilac-chaser-part6.mp4` (كود studio/illusions/il06)، `videos/quran/quran-reel-01-alsharh.mp4` (كود studio/quran-reels، خط Amiri، صوت مطر بدون موسيقى).
- نشر 15/11: il06 يوتيوب https://www.youtube.com/watch?v=EEc3OxFGgf4 (post b653549a) — ريل قرآن 01 انستا https://www.instagram.com/reel/DfxlnZlkx2Y/ (post f23c04c6). YouTube MFA تم.
- vidIQ ما يگدر ينشر تعليق جديد/يثبّته (بس رد على تعليق) → التعليق المثبت يدوي.
- ريلز القرآن (شهر): 30 ريل `videos/quran/month/qr-NN.mp4` (كود studio/quran-reels/build.py، reels.json، خط AmiriQuran، نص عثماني من npm quran-json). مجدولة يومياً 21:00 بغداد 16/11 → 15/12 على @7ll.ajr. postIds بـ studio/quran-reels/posts.txt.
- افكار غريبة (شهر): 60 شورت. خطة `studio/afkar_month_plan.json` (خدعة 16:00 + أسئلة دول 20:00 بغداد، 16/11→15/12). فيديوهات `videos/afkar/illusions/ilNN.mp4` (أجزاء 7-36) و`videos/afkar/countries/kNN.mp4`. كل الـ60 مجدولة (16/11→15/12) — بـ studio/afkar_posts.txt.
- ملاحظة: نداءات vidIQ المتوازية الكثيرة تسبب restart للجلسة → سوّها 1-4 بالمرة.
