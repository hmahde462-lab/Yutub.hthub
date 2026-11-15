# Quran reel #1 — الشرح ٥-٦. python3 render.py
import math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS, DUR = 1080, 1920, 30, 16.5
AM = 'fonts/Amiri-Bold.ttf'; AMR = 'fonts/Amiri-Regular.ttf'; KUF = '../flag-battles/fonts/Cairo-ExtraBold.ttf'
def f(p, s): return ImageFont.truetype(p, s)
GOLD = (236, 200, 120); WHITE = (245, 240, 230); SOFT = (200, 200, 220)
# background gradient + glow
y = np.linspace(0, 1, H)[:, None]
top, bot = np.array([8, 10, 28]), np.array([38, 22, 52])
bg = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1)
yy, xx = np.mgrid[0:H, 0:W]
glow = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 960) / 620) ** 2))[..., None]
bg = np.clip(bg + glow * np.array([60, 45, 30]), 0, 255)
BG = Image.fromarray(bg.astype(np.uint8))
random.seed(3)
STARS = [(random.uniform(0, W), random.uniform(0, H * 0.9), random.uniform(1, 3.2), random.uniform(0, 6.28), random.uniform(0.6, 2)) for _ in range(140)]
def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def alpha(t, a, b, fade=0.6):  # visible between a..b with fades
    return ease((t - a) / fade) * (1 - ease((t - (b - fade)) / fade))
def txt(layer, cy, s, font, col, a):
    if a <= 0: return
    d = ImageDraw.Draw(layer)
    w = d.textlength(s, font=font, direction='rtl', language='ar')
    bb = d.textbbox((0, 0), s, font=font, direction='rtl', language='ar')
    d.text(((W - w) / 2, cy - (bb[1] + bb[3]) / 2), s, font=font, fill=col + (int(255 * a),), direction='rtl', language='ar')
def frame(t):
    im = BG.copy(); d = ImageDraw.Draw(im)
    for x, yv, r, ph, sp in STARS:
        b = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(ph + t * sp))
        c = int(255 * b); d.ellipse([x - r, yv - r, x + r, yv + r], fill=(c, c, int(c * 0.95)))
    # moon
    d.ellipse([780, 210, 900, 330], fill=(250, 238, 200)); d.ellipse([815, 195, 935, 315], fill=tuple(int(v) for v in bg[255, 870]))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); G = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # hook
    txt(L, 900, 'إذا ضاق صدرك…', f(KUF, 82), WHITE, alpha(t, 0.2, 3.0))
    txt(L, 1030, 'اقرأ هاي', f(KUF, 70), GOLD, alpha(t, 0.7, 3.0))
    # ayah
    a1, a2 = alpha(t, 3.0, 10.6, 0.8), alpha(t, 5.0, 10.6, 0.8)
    for lay in (G, L):
        txt(lay, 800, 'فَإِنَّ  مَعَ  الْعُسْرِ  يُسْرًا', f(AM, 112), GOLD, a1)
        txt(lay, 1000, 'إِنَّ  مَعَ  الْعُسْرِ  يُسْرًا', f(AM, 112), GOLD, a2)
    txt(L, 1160, '﴿ سورة الشرح : ٥ - ٦ ﴾', f(AMR, 48), SOFT, alpha(t, 6.2, 10.6))
    # reflection
    txt(L, 860, 'ذكر العُسر مرّة…', f(KUF, 72), WHITE, alpha(t, 10.8, 14.4))
    txt(L, 980, 'واليُسر مرّتين', f(KUF, 72), GOLD, alpha(t, 11.6, 14.4))
    txt(L, 1120, 'ولن يغلبَ عُسرٌ يُسرين', f(AM, 70), WHITE, alpha(t, 12.4, 14.4))
    # cta
    txt(L, 930, 'أرسلها لشخص', f(KUF, 76), WHITE, alpha(t, 14.4, DUR + 1))
    txt(L, 1050, 'محتاج يسمعها اليوم', f(KUF, 76), GOLD, alpha(t, 14.7, DUR + 1))
    G = G.filter(ImageFilter.GaussianBlur(16))
    im = im.convert('RGBA'); im.alpha_composite(G); im.alpha_composite(G); im.alpha_composite(L)
    ImageDraw.Draw(im).text((W / 2, 1800), '@7ll.ajr', font=f(KUF, 34), fill=(200, 190, 210, 150), anchor='mm')
    return im.convert('RGB')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'fast', 'video.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): p.stdin.write(frame(n / FPS).tobytes())
p.stdin.close(); p.wait(); print('ok')
