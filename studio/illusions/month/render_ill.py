# Assemble illusion shorts. usage: python3 render_ill.py n... -> out/ilNN.mp4 (part = n+6)
import json, math, sys, subprocess, wave, os
sys.path.insert(0, '.')
from PIL import Image, ImageDraw, ImageFont
import panels; from scripts import S
W, H, FPS = 1080, 1920, 30
F = '../../flag-battles/fonts/Cairo-ExtraBold.ttf'
def font(s): return ImageFont.truetype(F, s)
BG = (10, 10, 14); CARD = (22, 22, 28); YEL = (255, 214, 64); RED = (240, 60, 80); CY = (120, 220, 255); WH = (255, 255, 255)
E = json.load(open('ill.json')); PY = 560
def dur(p): w = wave.open(p); return w.getnframes() / w.getframerate()
def ctext(d, y, s, f, col, stroke=0):
    d.text((W / 2, y), s, font=f, fill=col, direction='rtl', language='ar', anchor='ma', stroke_width=stroke, stroke_fill=(0, 0, 0))
def fit(d, s, size, maxw=940):
    while size > 30 and d.textlength(s, font=font(size), direction='rtl', language='ar') > maxw: size -= 2
    return font(size)
def pill(d, y, s):
    f = font(40); w = d.textlength(s, font=f, direction='rtl', language='ar')
    d.rounded_rectangle([(W - w) / 2 - 28, y, (W + w) / 2 + 28, y + 64], 32, fill=RED); ctext(d, y + 2, s, f, WH)
STARE = {'flag', 'lilac', 'spiral', 'troxler', 'bulb', 'waterfall', 'mib'}
AFTER = {'flag': 4.0, 'spiral': 0, 'bulb': 0, 'waterfall': 0}
def cover(e, s, part, path):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    p = panels.draw(e, 1.0, 'stare', 0); im.paste(p, (0, 560))
    ctext(d, 150, 'خدعة بصرية', font(110), WH, 6); pill(d, 300, f'الجزء {part}')
    lines = []; cur = ''
    for w in s['title'].replace('😳', '').replace('🤔', '').split():
        c = (cur + ' ' + w).strip()
        if d.textlength(c, font=font(84), direction='rtl', language='ar') <= 960 or not cur: cur = c
        else: lines.append(cur); cur = w
    lines.append(cur)
    for i, ln in enumerate(lines[:3]): ctext(d, 1410 + i * 125, ln, font(84), WH if i else YEL, 6)
    im.save(path, quality=93)
def build(n):
    e = E[n - 1]; s = S(e); part = n + 6; A, B, C = (f'audio/i{n:02d}_{k}.wav' for k in 'abc')
    la, lb, lc = dur(A), dur(B), dur(C); st = e['t'] in STARE
    ta = 0.3
    if st: tb = max(ta + la + 1.5, 8.5); TREV = max(tb + lb + 2.5, 18.5)
    else: tb = ta + la + 0.6; TREV = tb + lb + 0.4
    aft = AFTER.get(e['t'], 0); tc = TREV + 0.2; total = tc + lc + 1.2
    def frame(t):
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.rounded_rectangle([50, 250, W - 50, 520], 30, fill=CARD); ctext(d, 262, 'خدعة بصرية', font(72), WH); pill(d, 370, f'الجزء {part}')
        if t < TREV: ph, u = 'stare', 0
        else:
            u = t - TREV; ph = 'after' if (e['t'] in AFTER and (u < aft or aft == 0) and e['t'] != 'flag') or (e['t'] == 'flag' and u < aft) else 'reveal'
            if e['t'] in ('spiral', 'bulb', 'waterfall'): ph = 'after'
        im.paste(panels.draw(e, t, ph, u - (aft if e['t'] == 'flag' else 0)), (0, PY)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([50, 1420, W - 50, 1720], 30, fill=CARD)
        if t < TREV:
            ctext(d, 440, s['ins'], fit(d, s['ins'], 46), YEL)
            if st and t >= tb:
                ctext(d, 1450, s['q'], fit(d, s['q'], 58), WH); ctext(d, 1545, str(max(1, math.ceil(TREV - t))), font(96), YEL)
            elif not st and t >= tb:
                ctext(d, 1450, s['q'], fit(d, s['q'], 58), WH); ctext(d, 1545, str(max(1, min(3, math.ceil(TREV - t)))), font(96), YEL)
            else: ctext(d, 1470, s['q'] if not st else 'ركّز… ولا تحرك عيونك', fit(d, s['q'] if not st else 'ركّز… ولا تحرك عيونك', 58), WH)
        else:
            f = (t - tc) / lc if lc else 1
            ctext(d, 440, s['rev1'], fit(d, s['rev1'], 50), YEL)
            if f < 0.45: L1, L2, c2 = s['rev1'], s['rev2'], CY
            elif f < 0.8: L1, L2, c2 = s['exp1'], s['exp2'], CY
            else: L1, L2, c2 = s['cta'], '👇'.replace('👇', ''), YEL
            ctext(d, 1460, L1, fit(d, L1, 56), WH if f < 0.8 else YEL)
            if L2: ctext(d, 1560, L2, fit(d, L2, 54), c2)
        return im
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', A, '-i', B, '-i', C, '-filter_complex',
                          f'[1]adelay={int(ta*1000)}|{int(ta*1000)}[a];[2]adelay={int(tb*1000)}|{int(tb*1000)}[b];[3]adelay={int(tc*1000)}|{int(tc*1000)}[c];[a][b][c]amix=3:normalize=0,apad,loudnorm=I=-14:TP=-1.5,aresample=48000[o]',
                          '-map', '0:v', '-map', '[o]', '-t', f'{total:.2f}', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'fast', '-c:a', 'aac', '-b:a', '160k', f'out/il{n:02d}.raw.mp4'], stdin=subprocess.PIPE)
    for k in range(int(total * FPS)): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait()
    cover(e, s, part, f'out/il{n:02d}_cover.jpg')
    subprocess.run(['../../tools/add_cover.sh', f'out/il{n:02d}.raw.mp4', f'out/il{n:02d}_cover.jpg', f'out/il{n:02d}.mp4', '0.2', 'start'], check=True, capture_output=True)
    os.remove(f'out/il{n:02d}.raw.mp4'); print('done', n, e['t'], round(total, 1), flush=True)
if __name__ == '__main__':
    for n in map(int, sys.argv[1:]): build(n)
