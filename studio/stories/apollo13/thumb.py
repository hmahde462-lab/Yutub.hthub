# YouTube thumbnail (1280x720) from scene images + bold Arabic text.
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
W, H = 1280, 720
F = 'NotoNaskhArabic-Bold.ttf'
def font(sz): return ImageFont.truetype(F, sz, layout_engine=ImageFont.Layout.RAQM)
def text(d, xy, t, sz, fill, stroke=10, anchor='ra'):
    d.text(xy, t, font=font(sz), fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0), direction='rtl', language='ar', anchor=anchor)
bg = Image.open('img_jpg/1.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
bg = ImageEnhance.Contrast(ImageEnhance.Color(bg).enhance(1.25)).enhance(1.1)
# dark gradient on the right for text
ov = Image.new('L', (W, H), 0); g = ImageDraw.Draw(ov)
for x in range(W):
    g.line([(x, 0), (x, H)], fill=int(max(0, (x - 520) / (W - 520)) * 190))
bg.paste(Image.new('RGB', (W, H), (0, 0, 0)), (0, 0), ov)
d = ImageDraw.Draw(bg)
text(d, (W - 40, 15), 'هيوستن', 140, (255, 255, 255), 12)
text(d, (W - 40, 190), 'عدنا', 150, (255, 214, 60), 12)
text(d, (W - 40, 365), 'مشكلة!', 160, (255, 80, 60), 11)
# small "قصة حقيقية" tag
tag = 'قصة حقيقية'; f = font(46); bb = d.textbbox((0, 0), tag, font=f, direction='rtl', language='ar')
tw, th = bb[2] - bb[0], bb[3] - bb[1]
d.rounded_rectangle([W - 40 - tw - 40, 600, W - 40, 600 + th + 34], 14, fill=(200, 20, 30))
d.text((W - 60, 612), tag, font=f, fill=(255, 255, 255), direction='rtl', language='ar', anchor='ra')
bg.save('thumb.jpg', quality=92)
