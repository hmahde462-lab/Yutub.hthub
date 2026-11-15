# "3 أسئلة يسألها أطفال X" short. usage: python3 render_q.py n...  -> out/kNN.mp4 (with 0.2s cover frame)
import json, math, sys, wave, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
D = json.load(open('questions.json')); F = '../flag-battles/fonts/Cairo-ExtraBold.ttf'
def font(s): return ImageFont.truetype(F, s)
BG = (12, 12, 18); CARD = (24, 24, 32); YEL = (255, 214, 64); WHITE = (245, 245, 245); CY = (120, 220, 255)
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def load(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; return x, w.getframerate()
def segments(x, sr, n, texts=None):
    hop = sr // 100; db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) + 1e-9) for i in range(len(x) // hop)])
    sil = db < -38; runs = []; i = 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]: j += 1
            runs.append((j - i, i, j)); i = j
        else: i += 1
    inner = [r for r in runs if r[1] > 0 and r[2] < len(sil) and r[0] >= 15]
    T = len(x) / sr
    if texts is None or len(inner) < n - 1:
        cuts = sorted(sorted(inner, reverse=True)[:n - 1], key=lambda r: r[1])
        mids = [((s + e) / 2) * hop / sr for _, s, e in cuts]
    else:
        L = [len(t) + 12 for t in texts]; cum = np.cumsum(L)[:-1] / sum(L) * T
        C = sorted(inner, key=lambda r: r[1]); m = [((s + e) / 2) * hop / sr for _, s, e in C]; ln = [r[0] / 100 for r in C]
        INF = 1e9; K = n - 1; N = len(C)
        dp = [[INF] * N for _ in range(K)]; bk = [[-1] * N for _ in range(K)]
        cost = lambda k, j: abs(m[j] - cum[k]) - 2.0 * ln[j]
        for j in range(N): dp[0][j] = cost(0, j)
        for k in range(1, K):
            best, bi = INF, -1
            for j in range(N):
                if j > 0 and dp[k - 1][j - 1] < best: best, bi = dp[k - 1][j - 1], j - 1
                if bi >= 0: dp[k][j] = best + cost(k, j); bk[k][j] = bi
        j = min(range(N), key=lambda j: dp[K - 1][j]); idx = []
        for k in range(K - 1, -1, -1): idx.append(j); j = bk[k][j]
        mids = [m[j] for j in reversed(idx)]
    b = [0.0] + mids + [T]
    return list(zip(b[:-1], b[1:]))

import re, difflib
def parse_tr(path):
    out = []
    for ln in open(path, encoding='utf-8'):
        m = re.match(r'\s*\[?([\d:.]+)\s*-\s*([\d:.]+)\]?\s*(.*)', ln)
        if not m: continue
        def sec(s):
            if ':' in s:
                p = s.split(':'); return float(p[-2]) * 60 + float(p[-1]) if len(p) >= 2 else float(p[0])
            p = s.split('.')
            if len(p) == 3: return int(p[0]) * 60 + int(p[1]) + int(p[2]) / 100
            return float(s)
        out.append((sec(m.group(1)), m.group(3).strip()))
    return out
def tr_bounds(path, texts, x, sr):
    ph = parse_tr(path); norm = lambda t: re.sub(r'[^\u0621-\u064A ]', '', t.replace('گ', 'ق').replace('ة', 'ه'))
    starts = []; j = 0
    for k in range(1, len(texts)):
        best, bj = 0, None
        for jj in range(j, len(ph)):
            r = difflib.SequenceMatcher(None, norm(ph[jj][1])[:25], norm(texts[k])[:25]).ratio()
            if r > best: best, bj = r, jj
            if r > 0.75: break
        if bj is None or best < 0.4: return None
        starts.append(ph[bj][0]); j = bj + 1
    hop = sr // 100; db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) + 1e-9) for i in range(len(x) // hop)])
    sil = db < -38; mids = []; i = 0
    while i < len(sil):
        if sil[i]:
            jj = i
            while jj < len(sil) and sil[jj]: jj += 1
            if i > 0 and jj < len(sil) and jj - i >= 12: mids.append(((i + jj) / 2 * hop / sr, (jj - i) / 100))
            i = jj
        else: i += 1
    out = []
    for st in starts:
        c = [m for m in mids if abs(m[0] - st) < 1.2 and (not out or m[0] > out[-1] + 0.5)]
        out.append(max(c, key=lambda m: m[1] - abs(m[0] - st) * 0.5)[0] if c else st)
    T = len(x) / sr; b = [0.0] + out + [T]
    return list(zip(b[:-1], b[1:]))
def wrap(d, s, f, maxw):
    out = []; cur = ''
    for w in s.split():
        c = (cur + ' ' + w).strip()
        if d.textlength(c, font=f, direction='rtl', language='ar') <= maxw or not cur: cur = c
        else: out.append(cur); cur = w
    return out + ([cur] if cur else [])
def ctext(d, cx, y, s, f, col, anchor='ma', stroke=0):
    d.text((cx, y), s, font=f, fill=col, direction='rtl', language='ar', anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
def block(d, cx, y, s, sz, col, maxw, lh=1.35):
    f = font(sz); lines = wrap(d, s, f, maxw)
    for i, ln in enumerate(lines): ctext(d, cx, y + i * sz * lh, ln, f, col)
    return len(lines) * sz * lh
EMB = {'العراق': 'text', 'سوريا': 'stars3', 'مصر': 'eagle'}
def flagbar(d, y, cols, w=600, h=26, c=None):
    x0 = (W - w) / 2
    for i, cc in enumerate(cols): d.rectangle([x0, y + i * h, x0 + w, y + (i + 1) * h], fill=hexc(cc))
    e = EMB.get(c); my = y + 1.5 * h
    if e == 'text': d.text((W / 2, my), 'الله أكبر', font=font(int(h * 0.8)), fill=(0, 122, 61), anchor='mm', direction='rtl', language='ar')
    elif e == 'stars3':
        for k in (-1, 0, 1):
            cx = W / 2 + k * h * 1.6; r = h * 0.42
            d.polygon([(cx + r * math.cos(math.pi / 2 + j * math.pi / 5) * (1 if j % 2 == 0 else 0.45), my - r * math.sin(math.pi / 2 + j * math.pi / 5) * (1 if j % 2 == 0 else 0.45)) for j in range(10)], fill=(206, 17, 38))
    elif e == 'eagle': d.ellipse([W / 2 - h * 0.4, my - h * 0.4, W / 2 + h * 0.4, my + h * 0.4], fill=(192, 147, 0))
def kid(d, x, y, mouth, mood, t):
    bob = math.sin(t * 3) * 6; y += bob; k = (250, 250, 250)
    d.ellipse([x - 70, y - 70, x + 70, y + 70], outline=k, width=10)
    d.ellipse([x - 32, y - 18, x - 16, y - 2], fill=k); d.ellipse([x + 16, y - 18, x + 32, y - 2], fill=k)
    mo = 6 + 26 * mouth
    if mood == 'happy': d.arc([x - 34, y + 4, x + 34, y + 40], 10, 170, fill=k, width=8)
    else: d.ellipse([x - 18, y + 22, x + 18, y + 22 + mo], outline=k, width=7)
    d.line([x, y + 70, x, y + 260], fill=k, width=10)
    d.line([x, y + 120, x - 90, y + 200], fill=k, width=10)
    if mood == 'ask': d.line([x, y + 120, x + 80, y + 40], fill=k, width=10)   # hand up
    else: d.line([x, y + 120, x + 90, y + 200], fill=k, width=10)
    d.line([x, y + 260, x - 70, y + 380], fill=k, width=10); d.line([x, y + 260, x + 70, y + 380], fill=k, width=10)
def cover(e, path):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im); cols = e['flag']
    flagbar(d, 0, cols, W, 90, e['c'])
    ctext(d, W / 2, 420, '3 أسئلة', font(170), YEL, stroke=8)
    ctext(d, W / 2, 660, 'يسألها أطفال', font(110), WHITE, stroke=6)
    ctext(d, W / 2, 830, e['c'], font(190), WHITE, stroke=10)
    ctext(d, W / 2, 1120, 'والكبار يحتارون!', font(90), CY, stroke=6)
    kid(d, W / 2, 1380, 0.4, 'ask', 0); ctext(d, W / 2 + 190, 1290, '؟', font(220), YEL, stroke=8)
    im.save(path, quality=93)
def build(n):
    e = D[n - 1]; x, sr = load(f'audio/k{n:02d}.wav')
    TX = [f"تلات أسئلة يسألها أطفال {e['c']}… والكبار يحتارون!"] + [t for qa in e['q'] for t in qa] + ['إنت من وين؟ اكتب دولتك بالتعليقات، حتى نسويلها حلقة!']
    seg = None  # transcript timestamps drift; silence+text-length DP is more reliable
    if seg is None: seg = segments(x, sr, 8, [f"تلات أسئلة يسألها أطفال {e['c']}… والكبار يحتارون!"] + [t for qa in e['q'] for t in qa] + ['إنت من وين؟ اكتب دولتك بالتعليقات، حتى نسويلها حلقة!'])
    LEAD = 0.3; total = LEAD + len(x) / sr + 1.2
    env = np.array([np.sqrt(np.mean(x[int(i * sr / FPS):int((i + 1) * sr / FPS)] ** 2)) if int((i + 1) * sr / FPS) <= len(x) else 0 for i in range(int(total * FPS) + 2)])
    env = np.clip(env / (env.max() + 1e-9) * 1.8, 0, 1)
    def which(t):
        t -= LEAD
        for i, (a, b) in enumerate(seg):
            if t < b: return i, t - a
        return len(seg) - 1, t - seg[-1][0]
    p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
                          '-i', f'audio/k{n:02d}.wav','-filter_complex',f'[1]adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad,loudnorm=I=-14:TP=-1.5,aresample=48000[a]',
                          '-map','0:v','-map','[a]','-t',f'{total:.2f}','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-preset','fast','-c:a','aac','-b:a','160k',f'out/k{n:02d}.raw.mp4'], stdin=subprocess.PIPE)
    for k in range(int(total * FPS)):
        t = k / FPS; i, u = which(t); m = float(env[k - int(LEAD * FPS)]) if k >= LEAD * FPS else 0
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.rounded_rectangle([50, 150, W - 50, 400], 30, fill=CARD)
        ctext(d, W / 2, 165, f'3 أسئلة يسألها أطفال {e["c"]}', font(60), WHITE)
        flagbar(d, 262, e['flag'], 600, 36, e['c'])
        if i == 0:
            ctext(d, W / 2, 620, '3 أسئلة', font(150), YEL, stroke=4); ctext(d, W / 2, 820, f'يسألها أطفال {e["c"]}', font(80), WHITE)
            ctext(d, W / 2, 960, 'والكبار يحتارون!', font(76), CY)
            kid(d, W / 2, 1250, m, 'ask', t)
        elif i == 7:
            ctext(d, W / 2, 640, 'إنت من وين؟', font(120), YEL, stroke=4)
            block(d, W / 2, 830, 'اكتب دولتك بالتعليقات حتى نسويلها حلقة', 70, WHITE, 900)
            kid(d, W / 2, 1250, m, 'happy', t)
        else:
            qi = (i - 1) // 2; ans = (i - 1) % 2 == 1; q, a = e['q'][qi]
            ctext(d, W / 2, 440, f'السؤال {qi + 1} من 3', font(46), YEL)
            d.rounded_rectangle([300, 540, W - 50, 900], 40, fill=(250, 250, 250)); d.polygon([(320, 760), (320, 840), (250, 830)], fill=(250, 250, 250))
            hgt = len(wrap(d, q, font(64), 640)) * 64 * 1.35
            block(d, (300 + W - 50) / 2, 720 - hgt / 2, q, 64, (20, 20, 20), 640)
            kid(d, 170, 850, 0 if ans else m, 'happy' if ans else 'ask', t)
            if ans:
                al = min(1, u / 0.3)
                d.rounded_rectangle([50, 1330, W - 50, 1760], 36, fill=CARD, outline=YEL, width=4)
                ctext(d, W / 2, 1350, 'الجواب', font(50), YEL)
                block(d, W / 2, 1440, a, 60, tuple(int(c * al + 24 * (1 - al)) for c in WHITE), 900)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    cover(e, f'out/k{n:02d}_cover.jpg')
    subprocess.run(['../tools/add_cover.sh', f'out/k{n:02d}.raw.mp4', f'out/k{n:02d}_cover.jpg', f'out/k{n:02d}.mp4', '0.2', 'start'], check=True, capture_output=True)
    os.remove(f'out/k{n:02d}.raw.mp4'); print('done', n, round(total, 1), [round(b, 1) for _, b in seg], flush=True)
if __name__ == '__main__':
    for n in map(int, sys.argv[1:]): build(n)
