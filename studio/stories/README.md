# سلسلة القصص الحقيقية الأسبوعية — طريقة الشغل

قناة: «ورطة حمودي» يوتيوب UCbJktdkRq1fn8PdAIlUl9Uw (vidIQ، حساب vidIQ: الحساب الجديد). ستايل: شخصية كارتون راس أبيض داخل صور واقعية، سرد عراقي، ترجمة عربية.
جدول: طويل ~6 دقايق الجمعة 20:00 بغداد، و12 شورت (~30ث) السبت–الخميس 17:30 و21:30. كل شورت ينتهي "القصة كاملة بالقناة".

## الخطوات (انسخ مجلد قصة سابقة، مثلاً koepcke، لمجلد جديد studio/stories/<slug>/)
1. script.json: قائمة مشاهد {vo, img, prompt, part(1..12), hud(title/black), reuse, sfx}. حوالي 49 مشهد، 4 لكل جزء، ~3000 حرف سرد (≈5 دقايق صوت ≈ 6 دقايق فيديو). المشهد 2 = title، الأخير = black.
2. الصوت: `python3 ../../whiteboard-p3/tts.py Algieba vo.wav vo.txt` (موديل gemini-3.8-flash-tts، طلب واحد) ثم `ffmpeg -i vo.wav -b:a 192k chunk0.mp3` و chunks.json = [{"v":"A","idx":[0..N-1]}].
3. المحاذاة: `python3 align3.py` (Gemini gemini-3-flash-preview، نوافذ 30ث) ثم `python3 cut2.py` (DP على السكتات + عدد الوقفات) → lines/*.wav + lines.json.
4. الصور: Figma generate_image بملف OPYoRbmqbu2GXHLIhAOnje (حساب hmahde462 + صلاحية للـMCP)، 1920x1080، gpt-image-2.5-flare. نزّلها بـ `./dl.sh` (سطور "N url") → img_jpg/N.jpg.
5. build.py: عدّل النصوص (العنوان بمشهد title، نص الشاشة السودة، LONG_GAP، section()، OUT) ثم `python3 build.py`. النسخة بدون ترجمة: `mv clips clips_main; NOSUB=1 FORCE=1 OUT=<slug>_clean.mp4 python3 build.py`.
6. الشورتات: shorts.py (HEAD/SLUG/CLEAN بالسطر 31) → videos/shorts/<slug>/<slug>-partN.mp4.
7. الثمبنيل: thumb.py (صورة + 3 سطور نص) → videos/long/<slug>-thumb.jpg. الطويل → videos/long/<slug>.mp4 (لازم <100MB، اضغط crf 25).
8. نظّف (clips ov big sov audio.wav *_clean.mp4 vo.wav)، commit + push.
9. vidIQ: vidiq_video_upload بـ url = raw.githubusercontent.com/hmahde462-lab/Yutub.hthub/ccr-1ee633ff-a1v2hu/<path> (الرفع المحلي محجوب)، الثمبنيل vidiq_upload_image بنفس الطريقة، ثم vidiq_social_post_draft_create لكل فيديو (public، publishAt، categoryId 27)، احفظ postId/revision بـ drafts.json، اعرض على المستخدم، وبعد موافقته vidiq_social_post_publish. حد المجاني: 3 رفعات يوتيوب باليوم (يتصفر 11:00 بغداد).
