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
- ح٢ جاهزة: `videos/long/kahraba30-ep2.mp4` (4:28). الصور بـ `studio/kahraba30/ep2/img_jpg/` (من ملف Figma OPYoRbmqbu2GXHLIhAOnje، حساب 462 + صلاحية للـMCP). القص: `ep2/cut.py` (سكتات + توزيع بالحروف، بدون Gemini، يطلع lines/*.wav). البناء: `ep2/build2.py`. مشهد 32 طلع البطل بدل المراهق. لم تُنشر.
- ح٢ نسخة القصة + المعلومات: `videos/long/kahraba30-ep2-story.mp4` (4:49). قصة «الورقة اللي نزلت بالليل» بصوت Allan (LBWTcQo7Ie6Rzp2s8Xff) + معلومات بصوت Tareq (S7CPkcJPABvw8oef8idX)، نفس صور ح٢. كود: `studio/kahraba30/ep2b/` (script.json فيه v=A/T، cut.py يستخدم align.json من Gemini gemini-3.5-flash + overrides.json، build2b.py). رصيد ElevenLabs باقي ≈340.
- قصص عراقية حقيقية ح١: `videos/long/iraq-asian-cup-2007.mp4` (3:19) — منتخب العراق بطل آسيا 2007. صوت Gemini (gemini-3.8-flash-tts، Algieba)، صور Figma (34). كود: `studio/iraq2007/` (script.json، align.py+cut.py، build.py). لم تُنشر.
- قصص حقيقية ح٢: ياماگوچي (نجا من قنبلتين ذريتين) — `videos/long/yamaguchi-two-bombs.mp4` (4:15) + ثمبنيل، و4 شورتات عمودية `videos/shorts/yamaguchi-part1..4.mp4`. كود `studio/yamaguchi/`: align3.py (Gemini gemini-3-flash-preview بنوافذ 30ث مع أسطر السكربت) + cut2.py (DP على السكتات + عدد الوقفات المتوقعة) → build.py (NOSUB=1 OUT=… للنسخة النظيفة) → shorts.py. لم تُنشر.
- vidIQ (21/11/2026): الحساب المربوط صار قناة يوتيوب «ورطة حمودي» (UCbJktdkRq1fn8PdAIlUl9Uw، @ورطةحمودي). WOW SHOTS وإنستا @wowshotsiq ما عادوا يطلعون بقائمة vidIQ.
- خطة النشر لقناة «ورطة حمودي» (بغداد): طويل أسبوعي 6 دقايق (قصة حقيقية) ينزل الجمعة 8:00م، وبعده ينقسم 12 شورت (~30ث، كل واحد ينتهي بـ"الفيديو كامل بالقناة") تنزل السبت–الخميس 5:30م و9:30م. الجمعة 5:30م شورت كهرباء/سؤال.
- مجدول على «ورطة حمودي» (21/11/2026 بغداد): ياماگوچي الطويل 20:00 (QITQSJAsN9k)، الجزء 1 21:30 (UXzfSt7N4XQ)، الجزء 2 23:00 (JAduoYgV8FE). الجزء 3 و4 جاهزين بـ videos/shorts ما نزلوا بعد.
- سلسلة القصص الأسبوعية (studio/stories/<slug>/، نفس خط yamaguchi: script.json فيه part 1..12، align3→cut2→build→NOSUB build→shorts.py→thumb.py). الترتيب: كوپكه 27/11، دياتلوف 4/12، جيسوب 11/12، شاكلتون 18/12، المتنبي 25/12، بيت الحكمة 1/1، حمورابي 8/1. الطويل الجمعة 20:00، الشورتات السبت–الخميس 17:30 و21:30.
- كوپكه جاهزة: videos/long/koepcke.mp4 (5:57) + koepcke-thumb.jpg + videos/shorts/koepcke/koepcke-part1..12.mp4.
- vidIQ المجاني: 3 رفعات يوتيوب باليوم (يتصفر 11:00 بغداد). كوپكه: 13 مسودة بـ studio/stories/koepcke/drafts.json، وتذكيرات send_later يومياً 12:00 من 22 لـ 26/11 تنشر 3 باليوم (المستخدم وافق على الجدولة).

## حالة الشغل (آخر تحديث 21/11/2026)
- ياماگوچي على «ورطة حمودي»: الطويل + الجزء 1 و2 مجدولين 21/11. الجزء 3 و4 جاهزين (videos/shorts/yamaguchi-part3/4) ما انرفعوا.
- كوپكه (طويل 27/11 + 12 شورت 28/11–3/12): 13 مسودة vidIQ بـ studio/stories/koepcke/drafts.json. موافق عليها. تذكيرات send_later يومياً 12:00 بغداد (22–26/11) تنشر 3 باليوم.
- الجاي حسب الترتيب: دياتلوف (4/12)، فيوليت جيسوب (11/12)، شاكلتون (18/12)، شارع المتنبي (25/12)، بيت الحكمة 1258 (1/1)، حمورابي (8/1). طريقة الشغل: studio/stories/README.md.
- كل قصة لازم تخلص وتنرفع مسوداتها قبل موعدها بـ5 أيام (بسبب حد 3 رفعات/يوم).
- رصيد: vidIQ ~125 كردت (يتجدد 21/12)، ElevenLabs ~340 حرف (ما يكفي، استعمل Gemini TTS).
- كوپكه دفعة 1 (22/11): الطويل M7HxpZrGYYM (27/11 20:00)، الجزء 1 PuPx662x3FA، الجزء 2 znReG9mtFyk — مرفوعة ومجدولة.
- دياتلوف جاهز: videos/long/dyatlov.mp4 + thumb + videos/shorts/dyatlov/ (12). ينتظر موافقة المستخدم للجدولة 27/11–1/12 (موعد الطويل 4/12 20:00).
- 22/11: حساب vidIQ تغيّر لحساب جديد (مجاني) بعد إعادة الربط. مسودات كوپكه 3–12 انعادت بالحساب الجديد (studio/stories/koepcke/drafts.json، القديمة drafts_oldacct.json ما تشتغل). ياماگوچي 3 و4 رفعهم المستخدم بنفسه (TecVe4TpE_4, MZalvq431Wo).
- طابور النشر: studio/state/publish_queue.json (كوپكه 6–12 + دياتلوف 13). تذكير يومي 12:00 بغداد ينشر أول 3 done=false بـ vidiq_social_post_publish ويعلّمها done ويرفع. كوپكه 3–5 انجدولت 22/11 (3 cu5KGhVOUXM).

## تسليم لجلسة جديدة (22/11/2026)
- جيسوب: خلص (videos/long/jessop.mp4 + 12 شورت)، مسوداته بالطابور (studio/stories/jessop/drafts.json). Figma الجديد: ملف PCT2vXT5xHQHTWtQvWRax9 (حساب rockabelleshop، session a4575d70-…).
- Figma: الحساب القديم hmahde462 خلص رصيده لحد 1/12. المستخدم ربط حساب Figma جديد مدفوع → بالجلسة الجديدة اعمل create_new_file وكمل عليه.
- vidIQ: الحساب الحالي 1e72ded1… (تغير 27/11) (مجاني، 3 رفعات/يوم). طابور النشر studio/state/publish_queue.json وتذكيره اليومي 12:07 بغداد (23–29/11) شغّال بالجلسة القديمة session_01QEbwXC1gCW2hrwMbMeGhu6 — لا تكرره.
- مواعيد جيسوب: الطويل 11/12 20:00، الشورتات 12–17/12 (17:30 و21:30). الرفع يبدي من 30/11 بعد ما يخلص الطابور.

## حالة 27/11/2026 (قبل compact)
- **vidIQ**: الحساب الجديد 1e72ded1 (hmahde462@gmail). حد مجاني 3 رفعات يوتيوب باليوم (يتصفر 11:00 بغداد). أول نشر احتاج تأكيد YouTube MFA (تم).
- **Metricool**: براند 8002575 (حساب ba770736) = قناة ورطة حمودي. خطة مجانية 20 منشور/شهر. براند 8090968 = WOW SHOTS. ما بيه أداة مسح بالـAPI.
- **الطابور** studio/state/publish_queue.json: كوبكه 10–12 + دياتلوف 1–12 + جيسوب 1–5 = 20 على Metricool. جيسوب 6–12 + شاكلتون 1–5 (12) على vidIQ عبر التريگر اليومي trig_01AYjkk5gCnr5Csf5kRPcVuC (12:07 بغداد، 3 باليوم). نسخهم بـ Metricool صارت Draft (لا ترجعها).
- **يدوي على المستخدم**: الطوال (دياتلوف 4/12، جيسوب 11/12، شاكلتون 18/12)، شاكلتون شورت 6–12، المتنبي (طويل 25/12 + 12 شورت، schedule.txt)، الكهرباء ح3/ح4 (videos/long/kahraba30-ep3.mp4, ep4 + 10 شورت لكل وحدة، ما انجدولت).
- **جاهز ومرسل**: GTA6 بالعراقي شورت (videos/shorts/gta6iq)، بيت الحكمة 4 شورتات (hikma, hikma4)، برومتات Flow للـGTA6 (السرقة، المعاملة، السباق) ولمبة حمودي.
- **شغل جاري**: بيت الحكمة طويل (studio/stories/hikma): نص+صوت+محاذاة جاهز، صور 13/48. حمورابي (studio/stories/hammurabi): نص+صوت+محاذاة جاهز، صور 0/48. تذكير send_later trig_01BJWtnZuYzCFiC87wcYGgck يوم 1/12 00:05 UTC يكمل الصور (رصيد فيغما الشهري خلص لحد 1/12). Higgsfield رصيده 0.
- **صوت**: Gemini TTS Algieba. ElevenLabs رصيده خلص.
- **ملاحظة خط**: NotoNaskh ما بيه حروف لاتينية ولا '-' ولا '…' ولا إيموجي — لا تحطها بالنصوص المحروقة على الفيديو.
- **اشتراك Claude** ينتهي حوالي 7/12.
- فحص ربط vidIQ اليومي: trig_01WvaxQkVEs8gmA3piFAHx34.

## حالة 27/11/2026 مساءً
- فيغما صار على حساب جديد (ba770736@gmail، ملف erUAT3EtVuvJwxYpSSYlQz). الحد اليومي يرجع 00:00 UTC.
- بيت الحكمة الطويل جاهز: videos/long/hikma.mp4 (5:36) + 12 شورت videos/shorts/hikma-long/ + schedule.txt بـ studio/stories/hikma (الجمعة 1/1/2027).
- حمورابي: 44 صورة من 48 نازلة؛ باقي 43، 44، 45، 46 (برومبتاتها بـ script.json). بعدها build.py (عنوان/شاشة سودة/section/OUT) + shorts + thumb + ضغط.
- طول الفيديو الطويل المطلوب 6–7 دقايق (≈3300–3500 حرف سرد). موساشي انطوّل يدوياً بـ script.json (لا تعيد gen.py).
- المحاذاة: gemini-3.6-flash يرجع 429؛ استخدم GM=gemini-3-flash-preview.

- **28/11**: كل الطوال انعادت بصوت خلفية واطي + مؤثرات Epidemic (studio/sfx/<slug>/map.json، الـmp3 ما ينرفع). الشورتات NOSFX. الإسبارطيين: المستخدم نشره بنفسه؛ النسخ القديمة (wTrjz-5J_2g، 3tDp3jFbh7o) خاص. نبوخذنصر الجديد يُنشر 29/11 (trig_011EAo89T2MnmbD8k2txVk6E) لموعد 30/11. أبولو 13 (6/12) وبرمودا (8/12) مسودات تُنشر 30/11 (trig_014kDEEt8t4QpR4n1ydaVhb4). الكهرباء ح3/ح4: المستخدم ينشرهن بنفسه بدون شورتات. فيغما الحالي: ملف nmNYTRHAhF6AHHGtcb3G10. محاذاة بدون Gemini: studio/stories/offalign.py ثم cut2.py.
