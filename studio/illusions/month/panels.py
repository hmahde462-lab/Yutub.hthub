# Panel drawers for illusions. Each: draw(e, t, phase, u) -> RGB image (W x PH). phase: 'stare'|'after'|'reveal'
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
W, PH = 1080, 820
GRAY = (190, 190, 190)
def star(d, cx, cy, r, pts=5, inner=0.45, fill=(255, 255, 255), rot=-math.pi / 2):
    P = []
    for i in range(pts * 2):
        rr = r if i % 2 == 0 else r * inner; a = rot + i * math.pi / pts
        P.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(P, fill=fill)
def crescent(d, cx, cy, r, col, bg, off=0.25, toward=1):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); o = r * off * 2 * toward; r2 = r * 0.82
    d.ellipse([cx - r2 + o, cy - r2, cx + r2 + o, cy + r2], fill=bg)
def flag(name, w=860, h=430):
    im = Image.new('RGB', (w, h), (255, 255, 255)); d = ImageDraw.Draw(im)
    G, Wh, B, R = (0, 122, 61), (255, 255, 255), (0, 0, 0), (206, 17, 38)
    def h3(c1, c2, c3):
        for i, c in enumerate((c1, c2, c3)): d.rectangle([0, i * h / 3, w, (i + 1) * h / 3], fill=c)
    if name == 'kuwait': h3(G, Wh, R); d.polygon([(0, 0), (w * .25, h / 3), (w * .25, 2 * h / 3), (0, h)], fill=B)
    elif name == 'uae': h3(G, Wh, B); d.rectangle([0, 0, w * .25, h], fill=R)
    elif name in ('jordan', 'palestine'):
        h3(B, Wh, G); d.polygon([(0, 0), (w * .5 if name == 'jordan' else w * .38, h / 2), (0, h)], fill=R)
        if name == 'jordan': star(d, w * .17, h / 2, h * .09, 7, .45, Wh)
    elif name == 'syria':
        h3(G, Wh, B)
        for k in (-1, 0, 1): star(d, w / 2 + k * w * .16, h / 2, h * .1, 5, .4, R)
    elif name == 'yemen': h3(R, Wh, B)
    elif name == 'algeria':
        d.rectangle([0, 0, w / 2, h], fill=G); d.rectangle([w / 2, 0, w, h], fill=Wh)
        bgc = None; crescent(d, w / 2 + h * .02, h / 2, h * .25, R, (255, 255, 255), .2, 1)
        d.rectangle([0, 0, w / 2, h], fill=G); d.pieslice([w / 2 - h * .25, h / 2 - h * .25, w / 2 + h * .25, h / 2 + h * .25], 90, 270, fill=R)
        d.ellipse([w / 2 - h * .17, h / 2 - h * .2, w / 2 + h * .23, h / 2 + h * .2], fill=None)
        # inner cut: green on left half, white on right
        cx2 = w / 2 + h * .06; r2 = h * .2
        d.pieslice([cx2 - r2, h / 2 - r2, cx2 + r2, h / 2 + r2], 90, 270, fill=G); d.pieslice([cx2 - r2, h / 2 - r2, cx2 + r2, h / 2 + r2], 270, 90, fill=Wh)
        d.pieslice([w / 2 - h * .25, h / 2 - h * .25, w / 2 + h * .25, h / 2 + h * .25], 270, 90, fill=R)
        d.pieslice([cx2 - r2, h / 2 - r2, cx2 + r2, h / 2 + r2], 270, 90, fill=Wh)
        d.rectangle([w / 2, 0, w / 2 + 1, 0], fill=Wh); star(d, w / 2 + h * .2, h / 2, h * .1, 5, .4, R, rot=math.pi)
    elif name == 'tunisia':
        d.rectangle([0, 0, w, h], fill=(231, 0, 19)); r = h * .25; d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=Wh)
        crescent(d, w / 2 - h * .02, h / 2, h * .19, (231, 0, 19), Wh, .14, 1); star(d, w / 2 + h * .06, h / 2, h * .09, 5, .4, (231, 0, 19), rot=math.pi)
    elif name == 'morocco':
        d.rectangle([0, 0, w, h], fill=(193, 39, 45)); r = h * .22
        P = [(w / 2 + r * math.cos(-math.pi / 2 + i * 4 * math.pi / 5), h / 2 + r * math.sin(-math.pi / 2 + i * 4 * math.pi / 5)) for i in range(6)]
        d.line(P, fill=(0, 98, 51), width=int(h * .035), joint='curve')
    elif name in ('qatar', 'bahrain'):
        col = (138, 21, 56) if name == 'qatar' else (206, 17, 38); n = 9 if name == 'qatar' else 5; x0 = w * (.3 if name == 'qatar' else .25)
        d.rectangle([0, 0, w, h], fill=col); P = [(0, 0)]
        for i in range(n):
            P += [(x0, i * h / n), (x0 + w * .08, (i + .5) * h / n)]
        P += [(x0, h), (0, h)]; d.polygon(P, fill=Wh)
    elif name == 'libya':
        for (a, b, c) in ((0, .25, (231, 0, 19)), (.25, .75, B), (.75, 1, (35, 158, 70))): d.rectangle([0, a * h, w, b * h], fill=c)
        crescent(d, w / 2 - h * .03, h / 2, h * .14, Wh, B, .14, 1); star(d, w / 2 + h * .1, h / 2, h * .06, 5, .4, Wh)
    return im
def put(bg, im, cx=W / 2, cy=PH / 2):
    bg.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def dot(d, cx=W / 2, cy=PH / 2, r=12, col=(0, 0, 0)): d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
def cross(d, cx=W / 2, cy=PH / 2, s=22, col=(0, 0, 0)): d.line([cx - s, cy, cx + s, cy], fill=col, width=6); d.line([cx, cy - s, cx, cy + s], fill=col, width=6)
CACHE = {}
def draw(e, t, phase, u):
    T = e['t']; im = Image.new('RGB', (W, PH), (255, 255, 255)); d = ImageDraw.Draw(im)
    if T == 'flag':
        if 'f' not in CACHE.get('k', {}): CACHE['k'] = {}
        F = CACHE['k'].get(e['f'])
        if F is None: F = flag(e['f']); CACHE['k'][e['f']] = F
        if phase == 'stare': im.paste((235, 235, 235), [0, 0, W, PH]); put(im, ImageChops.invert(F)); dot(d, r=17, col=(255, 255, 255)); dot(d, r=11, col=(0, 0, 0))
        elif phase == 'after': im.paste((250, 250, 250), [0, 0, W, PH]); dot(d, r=11, col=(0, 0, 0))
        else: im.paste((235, 235, 235), [0, 0, W, PH]); put(im, F)
    elif T == 'lilac':
        im.paste(GRAY, [0, 0, W, PH]); key = ('lilac', tuple(e['col']))
        if key not in CACHE:
            fr = []
            for k in range(12):
                L = Image.new('RGB', (W, PH), GRAY); dd = ImageDraw.Draw(L)
                for i in range(12):
                    if i == k: continue
                    a = 2 * math.pi * i / 12 - math.pi / 2; x, y = W / 2 + 300 * math.cos(a), PH / 2 + 300 * math.sin(a)
                    dd.ellipse([x - 48, y - 48, x + 48, y + 48], fill=tuple(e['col']))
                fr.append(L.filter(ImageFilter.GaussianBlur(22)))
            CACHE[key] = fr
        k = int(t / 0.1) % 12
        if phase == 'stare': im = CACHE[key][k].copy()
        else:
            d = ImageDraw.Draw(im); comp = tuple(255 - c for c in e['col'])
            for i in range(12):
                a = 2 * math.pi * i / 12 - math.pi / 2; x, y = W / 2 + 300 * math.cos(a), PH / 2 + 300 * math.sin(a)
                if i == k: d.ellipse([x - 44, y - 44, x + 44, y + 44], fill=comp)
                else: d.ellipse([x - 44, y - 44, x + 44, y + 44], outline=tuple(e['col']), width=6)
        cross(ImageDraw.Draw(im))
    elif T == 'mib':
        im.paste((0, 0, 0), [0, 0, W, PH]); d = ImageDraw.Draw(im); a0 = t * 0.9
        for gx in range(-8, 9):
            for gy in range(-8, 9):
                x, y = gx * 70, gy * 70; ca, sa = math.cos(a0), math.sin(a0)
                X, Y = W / 2 + x * ca - y * sa, PH / 2 + x * sa + y * ca
                if 0 < X < W and 0 < Y < PH: d.line([X - 10, Y, X + 10, Y], fill=(70, 110, 255), width=5); d.line([X, Y - 10, X, Y + 10], fill=(70, 110, 255), width=5)
        for (x, y) in ((W / 2 - 230, PH / 2 - 160), (W / 2 + 230, PH / 2 - 160), (W / 2, PH / 2 + 250)):
            d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(255, 40, 40))
            if phase == 'reveal': d.ellipse([x - 36, y - 36, x + 36, y + 36], outline=(120, 255, 140), width=5)
        dot(d, r=9, col=(255, 255, 255))
    elif T == 'troxler':
        if 'trox' not in CACHE:
            L = Image.new('RGB', (W, PH), (205, 205, 205)); dd = ImageDraw.Draw(L)
            cols = [(255, 140, 180), (140, 200, 255), (160, 240, 160), (255, 220, 120), (200, 160, 255), (255, 170, 120)]
            for i, c in enumerate(cols):
                a = 2 * math.pi * i / 6; x, y = W / 2 + 280 * math.cos(a), PH / 2 + 260 * math.sin(a); dd.ellipse([x - 110, y - 110, x + 110, y + 110], fill=c)
            CACHE['trox'] = L.filter(ImageFilter.GaussianBlur(45))
        im = CACHE['trox'].copy(); dot(ImageDraw.Draw(im), r=10, col=(255, 255, 255))
    elif T == 'spiral':
        if phase == 'stare':
            if 'spir' not in CACHE:
                yy, xx = np.mgrid[0:PH, 0:W]; CACHE['spir'] = (np.hypot(xx - W / 2, yy - PH / 2), np.arctan2(yy - PH / 2, xx - W / 2))
            r, th = CACHE['spir']; v = np.sin(r / 18 + 4 * th - t * 6) > 0
            im = Image.fromarray(np.where(v, 255, 20).astype(np.uint8)).convert('RGB'); dot(ImageDraw.Draw(im), r=12, col=(220, 30, 30))
        else:
            im.paste((230, 222, 205), [0, 0, W, PH]); d = ImageDraw.Draw(im)
            for y in range(0, PH, 60):
                for x in range(-60 if (y // 60) % 2 else 0, W, 120): d.rectangle([x + 4, y + 4, x + 116, y + 56], fill=(178, 90, 60))
    elif T == 'waterfall':
        im.paste((20, 20, 20), [0, 0, W, PH]); d = ImageDraw.Draw(im); off = (t * 160) % 60 if phase == 'stare' else 0
        for y in range(-60, PH + 60, 60): d.rectangle([0, y + off, W, y + off + 30], fill=(235, 235, 235))
        dot(d, r=14, col=(220, 30, 30))
    elif T == 'bulb':
        if phase == 'stare':
            im.paste((15, 15, 25), [0, 0, W, PH]); g = Image.new('RGBA', (W, PH), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            gd.ellipse([W / 2 - 170, PH / 2 - 230, W / 2 + 170, PH / 2 + 110], fill=(255, 230, 120, 255)); g = g.filter(ImageFilter.GaussianBlur(30))
            im = Image.alpha_composite(im.convert('RGBA'), g).convert('RGB'); d = ImageDraw.Draw(im)
            d.ellipse([W / 2 - 140, PH / 2 - 210, W / 2 + 140, PH / 2 + 70], fill=(255, 245, 190)); d.rectangle([W / 2 - 70, PH / 2 + 60, W / 2 + 70, PH / 2 + 170], fill=(150, 150, 160))
            dot(d, col=(0, 0, 0))
        else: im.paste((250, 250, 250), [0, 0, W, PH]); dot(ImageDraw.Draw(im))
    elif T == 'ebbinghaus':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); r = 55
        k = 0 if phase != 'reveal' else min(1, u / 1.5); s = 1 - k
        L, R = (300, PH / 2), (790, PH / 2)
        if s > 0.01:
            g = tuple(int(150 + 100 * k) for _ in range(3))
            for i in range(6):
                a = 2 * math.pi * i / 6; d.ellipse([L[0] + 175 * math.cos(a) - 85, L[1] + 175 * math.sin(a) - 85, L[0] + 175 * math.cos(a) + 85, L[1] + 175 * math.sin(a) + 85], fill=g)
            for i in range(8):
                a = 2 * math.pi * i / 8; d.ellipse([R[0] + 95 * math.cos(a) - 22, R[1] + 95 * math.sin(a) - 22, R[0] + 95 * math.cos(a) + 22, R[1] + 95 * math.sin(a) + 22], fill=g)
        for c in (L, R): d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(245, 140, 30))
        if phase == 'reveal' and u > 1.6:
            for yy in (PH / 2 - r, PH / 2 + r): d.line([150, yy, 930, yy], fill=(220, 30, 30), width=4)
    elif T == 'cafe':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); tw, th = 90, 70
        for row in range(PH // th + 1):
            off = [0, 22, 44, 22][row % 4]
            for x in range(-tw * 2, W + tw, tw * 2): d.rectangle([x + off, row * th, x + off + tw, row * th + th], fill=(10, 10, 10))
            d.line([0, row * th, W, row * th], fill=(128, 128, 128), width=4)
        if phase == 'reveal' and u > 0.6:
            for row in range(1, PH // th + 1): d.line([0, row * th, W, row * th], fill=(230, 30, 30), width=5)
    elif T == 'ponzo':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); k = 0 if phase != 'reveal' else min(1, u / 1.2)
        if k < 1:
            c = tuple(int(60 + 190 * k) for _ in range(3))
            d.line([W / 2 - 60, 20, W / 2 - 380, PH - 20], fill=c, width=8); d.line([W / 2 + 60, 20, W / 2 + 380, PH - 20], fill=c, width=8)
            for i in range(9):
                y = 40 + i * 90; hw = 60 + (y - 20) / (PH - 40) * 320; d.line([W / 2 - hw - 20, y, W / 2 + hw + 20, y], fill=c, width=4)
        y1, y2 = 200, 640; d.rectangle([W / 2 - 110, y1 - 12, W / 2 + 110, y1 + 12], fill=(250, 200, 0)); d.rectangle([W / 2 - 110, y2 - 12, W / 2 + 110, y2 + 12], fill=(250, 200, 0))
        if phase == 'reveal' and u > 1.3:
            for x in (W / 2 - 110, W / 2 + 110): d.line([x, 120, x, PH - 100], fill=(220, 30, 30), width=4)
    elif T == 'kanizsa':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); cx, cy, R = W / 2, PH / 2 + 30, 260; k = 0 if phase != 'reveal' else min(1, u / 1.2)
        for i in range(3):
            a = -math.pi / 2 + i * 2 * math.pi / 3; x, y = cx + R * math.cos(a), cy + R * math.sin(a); ad = math.degrees(a) + 180
            gap = 60 * (1 - k); d.pieslice([x - 75, y - 75, x + 75, y + 75], ad + gap / 2 if gap > 0 else 0, ad - gap / 2 + 360 if gap > 0 else 360, fill=(20, 20, 20))
        for i in range(3):
            a = math.pi / 2 + i * 2 * math.pi / 3; x, y = cx + R * .9 * math.cos(a), cy + R * .9 * math.sin(a)
            for j in (-1, 1):
                b = a + math.pi + j * math.pi / 6; d.line([x, y, x + 110 * math.cos(b), y + 110 * math.sin(b)], fill=(20, 20, 20), width=6)
    elif T == 'hermann':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); s, g = 120, 28
        for gx in range(8):
            for gy in range(6):
                x, y = 30 + gx * (s + g), 20 + gy * (s + g); d.rectangle([x, y, x + s, y + s], fill=(0, 0, 0))
        if phase == 'reveal' and u > 0.8:
            for gx in range(1, 7):
                for gy in range(1, 5):
                    x, y = 30 + gx * (s + g) - g / 2, 20 + gy * (s + g) - g / 2; d.ellipse([x - 22, y - 22, x + 22, y + 22], outline=(230, 30, 30), width=4)
    elif T == 'zollner':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); k = 0 if phase != 'reveal' else min(1, u / 1.2)
        for i in range(7):
            x0 = -200 + i * 190; d.line([x0, 0, x0 + 500, PH], fill=(0, 0, 0), width=7)
            if k < 1:
                c = tuple(int(250 * k) for _ in range(3)); dirn = 1 if i % 2 else -1
                for j in range(12):
                    tt = (j + .5) / 12; x, y = x0 + 500 * tt, PH * tt; d.line([x - 28, y - 28 * dirn * -1, x + 28, y + 28 * dirn * -1], fill=c, width=4) if True else None
    elif T == 'jastrow':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); k = 0 if phase != 'reveal' else min(1, u / 1.5)
        def arc(cy, col):
            P = []; Ro, Ri = 560, 380
            for a in np.linspace(-0.55, 0.55, 30): P.append((W / 2 + Ro * math.sin(a), cy - Ro * math.cos(a) + Ro))
            for a in np.linspace(0.55, -0.55, 30): P.append((W / 2 + Ri * math.sin(a), cy - Ri * math.cos(a) + Ro))
            d.polygon(P, fill=col)
        arc(170 + 240 * k, (230, 50, 50) + ((),)[0:0] and (230, 50, 50)); arc(410, (40, 110, 230))
        if k >= 1: arc(410, (40, 110, 230, )); d2 = ImageDraw.Draw(im); arc(410, (230, 50, 50))
    elif T == 'breathing':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); a = t * 1.4; s = 200
        P = [(W / 2 + s * math.cos(a + i * math.pi / 2), PH / 2 + s * math.sin(a + i * math.pi / 2)) for i in range(4)]; d.polygon(P, fill=(245, 140, 30))
        if not (phase == 'reveal' and u > 0.8):
            for (x, y) in ((W / 2 - 200, PH / 2 - 200), (W / 2 + 200, PH / 2 - 200), (W / 2 - 200, PH / 2 + 200), (W / 2 + 200, PH / 2 + 200)):
                d.ellipse([x - 120, y - 120, x + 120, y + 120], fill=(40, 90, 220))
    elif T == 'hering':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im); k = 0 if phase != 'reveal' else min(1, u / 1.2)
        if k < 1:
            c = tuple(int(30 + 220 * k) for _ in range(3))
            for i in range(36):
                a = i * math.pi / 18; d.line([W / 2, PH / 2, W / 2 + 900 * math.cos(a), PH / 2 + 900 * math.sin(a)], fill=c, width=3)
        for x in (W / 2 - 150, W / 2 + 150): d.line([x, 0, x, PH], fill=(220, 30, 30), width=8)
    elif T == 'stepping':
        im.paste((250, 250, 250), [0, 0, W, PH]); d = ImageDraw.Draw(im)
        if not (phase == 'reveal' and u > 0.8):
            for x in range(0, W, 40): d.rectangle([x, 0, x + 20, PH], fill=(0, 0, 0))
        x = (t * 90) % (W + 300) - 300
        d.rectangle([x, PH / 2 - 160, x + 220, PH / 2 - 100], fill=(255, 230, 0)); d.rectangle([x, PH / 2 + 100, x + 220, PH / 2 + 160], fill=(10, 20, 110))
    elif T == 'fraser':
        im.paste((230, 230, 230), [0, 0, W, PH]); d = ImageDraw.Draw(im)
        for R in range(60, 400, 55):
            n = int(2 * math.pi * R / 26)
            for i in range(n):
                a = 2 * math.pi * i / n; x, y = W / 2 + R * math.cos(a), PH / 2 + R * math.sin(a); tng = a + math.pi / 2 + 0.5
                c = (0, 0, 0) if i % 2 else (255, 255, 255)
                d.line([x - 12 * math.cos(tng), y - 12 * math.sin(tng), x + 12 * math.cos(tng), y + 12 * math.sin(tng)], fill=c, width=6)
        if phase == 'reveal' and u > 0.8: d.ellipse([W / 2 - 225, PH / 2 - 225, W / 2 + 225, PH / 2 + 225], outline=(230, 30, 30), width=6)
    return im
