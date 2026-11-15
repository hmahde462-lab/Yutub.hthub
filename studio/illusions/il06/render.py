# il06 — Lilac chaser. python3 render.py -> frames piped to ffmpeg
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS, DUR = 1080, 1920, 30, 32.0
F = '../../flag-battles/fonts/Cairo-ExtraBold.ttf'
def font(s): return ImageFont.truetype(F, s)
BG = (10, 10, 14); CARD = (22, 22, 28); YEL = (255, 214, 64); RED = (240, 60, 80); CY = (120, 220, 255)
PANEL = (0, 560, W, 1340); GRAY = (190, 190, 190)
cx, cy = W // 2, (PANEL[1] + PANEL[3]) // 2
R, N = 300, 12
def disc_layer(skip):
    im = Image.new('RGB', (W, PANEL[3] - PANEL[1]), GRAY); d = ImageDraw.Draw(im)
    for i in range(N):
        if i == skip: continue
        a = 2 * math.pi * i / N - math.pi / 2
        x, y = cx + R * math.cos(a), cy - PANEL[1] + R * math.sin(a)
        d.ellipse([x - 48, y - 48, x + 48, y + 48], fill=(230, 120, 220))
    im = im.filter(ImageFilter.GaussianBlur(22))
    d = ImageDraw.Draw(im); c = cy - PANEL[1]
    d.line([cx - 22, c, cx + 22, c], fill=(0, 0, 0), width=6); d.line([cx, c - 22, cx, c + 22], fill=(0, 0, 0), width=6)
    return im
CH = [disc_layer(k) for k in range(N)]
def rr(d, box, r, fill): d.rounded_rectangle(box, r, fill=fill)
def ctext(d, y, s, f, fill): 
    w = d.textlength(s, font=f, direction='rtl', language='ar'); d.text(((W - w) / 2, y), s, font=f, fill=fill, direction='rtl', language='ar')
def pill(d, y, s):
    f = font(40); w = d.textlength(s, font=f, direction='rtl', language='ar')
    rr(d, [(W - w) / 2 - 28, y, (W + w) / 2 + 28, y + 64], 32, RED); ctext(d, y + 2, s, f, (255, 255, 255))
REVEAL = 19.0
def frame(t):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    rr(d, [50, 250, W - 50, 520], 30, CARD)
    ctext(d, 262, 'خدعة بصرية', font(72), (255, 255, 255)); pill(d, 370, 'الجزء 6')
    if t < REVEAL:
        ctext(d, 440, 'ركّز على الصليب ولا تحرك عيونك', font(46), YEL)
        step = int(t / 0.1) % N
        im.paste(CH[step], (0, PANEL[1]))
        rr(d, [50, 1380, W - 50, 1640], 30, CARD)
        if t < 8.5:
            ctext(d, 1410, 'شوف شنو يصير للنقاط الوردية؟', font(60), YEL); ctext(d, 1520, 'باوع على الصليب بس', font(44), (230, 230, 230))
        else:
            ctext(d, 1410, 'استمر… لا تحرك عيونك!', font(60), (255, 255, 255))
            ctext(d, 1505, str(max(1, math.ceil(REVEAL - t))), font(90), YEL)
    else:
        u = t - REVEAL
        ctext(d, 440, 'شفت النقطة الخضرة؟!', font(52), YEL)
        # static demo: pink ring + green ghost dot rotating
        p = Image.new('RGB', (W, PANEL[3] - PANEL[1]), GRAY); pd = ImageDraw.Draw(p); c = cy - PANEL[1]
        k = int(t / 0.1) % N
        for i in range(N):
            a = 2 * math.pi * i / N - math.pi / 2; x, y = cx + R * math.cos(a), c + R * math.sin(a)
            if i == k: pd.ellipse([x - 44, y - 44, x + 44, y + 44], fill=(90, 220, 110))
            else: pd.ellipse([x - 44, y - 44, x + 44, y + 44], outline=(230, 120, 220), width=6)
        pd.line([cx - 22, c, cx + 22, c], fill=(0, 0, 0), width=6); pd.line([cx, c - 22, cx, c + 22], fill=(0, 0, 0), width=6)
        im.paste(p, (0, PANEL[1]))
        rr(d, [50, 1380, W - 50, 1720], 30, CARD)
        if u < 4.6:
            ctext(d, 1410, 'الوردي اختفى… وطلعت نقطة خضرة تدور!', font(50), (255, 255, 255))
            ctext(d, 1500, 'بس الخضرة أصلاً مو موجودة!', font(56), CY)
        elif u < 9.0:
            ctext(d, 1410, 'عيونك تعبت من الوردي', font(54), (255, 255, 255))
            ctext(d, 1500, 'فصارت تشوفلك لونه المعاكس', font(56), CY)
        else:
            ctext(d, 1410, 'شفت الخضرة؟', font(64), YEL)
            ctext(d, 1510, 'اكتب اي لو لا بالتعليقات', font(52), (255, 255, 255))
    return im
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'fast', 'video.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)):
    p.stdin.write(frame(n / FPS).tobytes())
p.stdin.close(); p.wait(); print('ok')
