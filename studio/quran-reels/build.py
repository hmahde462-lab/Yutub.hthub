# Build Quran reels from reels.json. usage: python3 build.py [n ...]  -> out/qr-NN.mp4
# Rule: every Quranic text on screen is fully recited (Alafasy, everyayah) and shown exactly while recited; no other audio/text during recitation.
import json, math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1080, 1920, 30
Q = json.load(open('data_quran.json')); R = json.load(open('reels.json'))
QF = 'fonts/AmiriQuran.ttf'; AMR = 'fonts/Amiri-Regular.ttf'; KUF = '../flag-battles/fonts/Cairo-ExtraBold.ttf'
AR_DIG = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
PAL = [((8,10,28),(38,22,52),(60,45,30),'moon'), ((4,18,30),(10,48,60),(30,60,60),'stars'), ((26,12,8),(70,34,20),(80,50,20),'sun'),
       ((10,10,12),(34,30,40),(50,40,30),'moon'), ((6,14,34),(40,30,70),(50,40,70),'stars'), ((14,22,14),(30,52,34),(50,60,30),'stars')]
os.makedirs('out', exist_ok=True)
def dur(fn): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn]))
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def vis(t, a, b, fd=0.35): return ease((t - a) / fd) * (1 - ease((t - (b - fd)) / fd))
def wrap(d, text, font, maxw):
    words = text.split(); lines = []; cur = ''
    for w in words:
        c = (cur + ' ' + w).strip()
        if d.textlength(c, font=font, direction='rtl', language='ar') <= maxw or not cur: cur = c
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def text_layer(lines_spec, glow=False, direction='rtl'):
    """lines_spec: list of (text, fontpath, size, color, y_center). returns RGBA."""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for s, fp, sz, col, yc in lines_spec:
        f = ImageFont.truetype(fp, sz)
        d.text((W / 2, yc), s, font=f, fill=col + (255,), direction=direction, language='ar' if direction == 'rtl' else None, anchor='mm')
    if glow:
        G = L.filter(ImageFilter.GaussianBlur(14)); out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        out.alpha_composite(G); out.alpha_composite(G); out.alpha_composite(L); return out
    return L
def ayah_layer(text):
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    for sz in range(104, 40, -4):
        f = ImageFont.truetype(QF, sz); lines = wrap(d, text, f, 930); lh = sz * 1.9
        if len(lines) * lh <= 1050: break
    y0 = 960 - (len(lines) - 1) * lh / 2
    return text_layer([(ln, QF, sz, (238, 204, 128), y0 + i * lh) for i, ln in enumerate(lines)], glow=True)
def build(n):
    s, a, b, h1, h2 = R[n - 1]; sur = Q[s - 1]; rnd = random.Random(n)
    top, bot, glowc, deco = PAL[(n - 1) % len(PAL)]
    # timeline
    T0 = 2.6; segs = []; t = T0
    for v in range(a, b + 1):
        fn = f'recit/{s:03d}{v:03d}.mp3'; dd = dur(fn)
        segs.append((fn, t, dd, sur['verses'][v - 1]['text'])); t += dd + 0.35
    rec_end = t - 0.35; DUR = rec_end + 3.6
    # background
    y = np.linspace(0, 1, H)[:, None, None]
    bg = np.array(top) * (1 - y) + np.array(bot) * y; bg = np.repeat(bg, W, 1)
    yy, xx = np.mgrid[0:H, 0:W]
    bg += np.exp(-(((xx - W / 2) / 540) ** 2 + ((yy - 960) / 640) ** 2))[..., None] * np.array(glowc)
    BG = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)); bd = ImageDraw.Draw(BG)
    if deco == 'moon':
        bd.ellipse([790, 210, 910, 330], fill=(250, 238, 200)); bd.ellipse([825, 195, 945, 315], fill=tuple(int(c) for c in bg[255, 880]))
    elif deco == 'sun':
        sun = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sun).ellipse([340, 1560, 740, 1960], fill=(255, 190, 110, 90))
        BG = Image.alpha_composite(BG.convert('RGBA'), sun.filter(ImageFilter.GaussianBlur(90))).convert('RGB')
    stars = [(rnd.uniform(0, W), rnd.uniform(0, H * 0.92), rnd.uniform(1, 3), rnd.uniform(0, 6.3), rnd.uniform(.6, 2)) for _ in range(120 if deco != 'sun' else 40)]
    # layers
    hook = text_layer([(h1, KUF, 80 if len(h1) < 20 else 66, (245, 240, 230), 900), (h2, KUF, 72, (236, 200, 120), 1030)])
    ref = f'﴿ سورة {sur["name"]} : {a}' + (f' - {b}' if b > a else '') + ' ﴾'
    cta = text_layer([(ref.translate(AR_DIG), AMR, 56, (210, 205, 225), 820), ('أرسلها لشخص تحبه', KUF, 76, (245, 240, 230), 960), ('حتى ينال الأجر وياك', KUF, 62, (236, 200, 120), 1080)])
    AY = [ayah_layer(txt) for _, _, _, txt in segs]
    wm = text_layer([('@7ll.ajr', KUF, 34, (200, 190, 210), 1810)], direction='ltr')
    wm.putalpha(wm.getchannel('A').point(lambda v: v * 0.55))
    def blend(im, lay, al):
        if al <= 0.001: return
        if al < 0.999: lay = lay.copy(); lay.putalpha(lay.getchannel('A').point(lambda v: int(v * al)))
        im.alpha_composite(lay)
    p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
                          '-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-preset','fast',f'out/qr-{n:02d}.v.mp4'], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)):
        t = k / FPS; im = BG.copy(); d = ImageDraw.Draw(im)
        for x, yv, r, ph, sp in stars:
            c = int(255 * (0.45 + 0.55 * (0.5 + 0.5 * math.sin(ph + t * sp)))); d.ellipse([x - r, yv - r, x + r, yv + r], fill=(c, c, int(c * .95)))
        im = im.convert('RGBA')
        blend(im, hook, vis(t, 0.15, T0 - 0.1))
        for (fn, st, dd, _), lay in zip(segs, AY): blend(im, lay, vis(t, st - 0.2, st + dd + 0.3, 0.3))
        blend(im, cta, vis(t, rec_end + 0.5, DUR + 1)); im.alpha_composite(wm)
        p.stdin.write(im.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    # audio: rain only in hook/cta (faint), recitation alone in between
    ins = []; fl = []
    for i, (fn, st, dd, _) in enumerate(segs):
        ins += ['-i', fn]; ms = int(st * 1000); fl.append(f'[{i+2}]aresample=48000,adelay={ms}|{ms}[r{i}]')
    rn = ''.join(f'[r{i}]' for i in range(len(segs)))
    fl.append(f'{rn}amix={len(segs)}:normalize=0,loudnorm=I=-15:TP=-1.5[rec]')
    fl.append(f"[1]aresample=48000,aloop=loop=-1:size=2e6,atrim=0:{DUR:.2f},volume='if(between(t,{T0-0.4:.2f},{rec_end+0.4:.2f}),0,0.10)':eval=frame,afade=t=out:st={DUR-1.2:.2f}:d=1.2[rain]")
    fl.append('[rec][rain]amix=2:normalize=0:duration=longest[a]')
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'out/qr-{n:02d}.v.mp4','-i','rain_raw.mp3',*ins,'-filter_complex',';'.join(fl),
                    '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-t',f'{DUR:.2f}',f'out/qr-{n:02d}.mp4'], check=True)
    os.remove(f'out/qr-{n:02d}.v.mp4'); print('done', n, round(DUR, 1), flush=True)
if __name__ == '__main__':
    for n in map(int, sys.argv[1:]): build(n)
