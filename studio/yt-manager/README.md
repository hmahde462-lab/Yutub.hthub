# YT Manager — إدارة عدة قنوات YouTube

نظام محلي لربط عدة قنوات YouTube (حتى من حسابات Google مختلفة)، والرفع إلى قناة محددة، وعرض إحصائيات كل قناة.

## الحمايات
- **وضع التجربة افتراضي:** المعاينة تفحص كل شيء ولا تستدعي `videos.insert` أبداً.
- **النشر الفعلي** يحتاج `LIVE_UPLOADS_ENABLED=true` **و** كتابة اسم القناة بالضبط لكل فيديو. الخصوصية الافتراضية `private`.
- **لا توجد قناة افتراضية**، ويجب اختيار القناة صراحةً.
- **قبل الرفع مباشرة** نسأل YouTube عن القناة المالكة للتوكن (`channels.list mine=true`). إذا لم تطابق القناة المختارة، تُلغى العملية.
- في لوحة الويب، بيانات الرفع (ومنها القناة) تُحفظ على الخادم بعد المعاينة، فلا يمكن تغيير القناة عند خطوة النشر.
- صلاحيات كل قناة **مشفّرة** (Fernet) بمفتاح خارج قاعدة البيانات.

## التشغيل
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.cli init-key        # الصق الناتج في YTM_ENCRYPTION_KEY داخل .env
# ضع client_secret.json في مجلد المشروع
python -m app.cli serve           # افتح http://localhost:8000
```

## إعداد Google Cloud
1. أنشئ مشروعاً، وفعّل **YouTube Data API v3** و**YouTube Analytics API**.
2. شاشة الموافقة: اختر External، وأضف كل إيميل تريد ربط قناته كـ Test user.
3. أنشئ OAuth client من نوع **Web application**، وأضف Redirect URI: `http://localhost:8000/oauth/callback`.
4. نزّل ملف JSON وسمّه `client_secret.json`.

> ⚠️ ما دام التطبيق في وضع **Testing** تنتهي صلاحية الربط كل 7 أيام.
> ⚠️ الفيديوهات المرفوعة من مشروع **لم يجتز مراجعة YouTube API** تبقى خاصة إجبارياً.

## الأوامر
```bash
python -m app.cli channels list
python -m app.cli upload -c UC... -f video.mp4 -k short -t "العنوان" --hashtags "طبخ,وصفات"   # تجربة
python -m app.cli upload ... --live                                                         # نشر فعلي (بعد التفعيل)
python -m app.cli stats -c UC...
python -m app.cli quota
python -m pytest -q
```
