# Build "انقطاع الكهرباء ٣٠ يوم" episode 1: Ken Burns scenes + narration + synthesized ambience + Arabic subtitles/HUD.
import json, os, subprocess, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import wave

D = os.path.dirname(os.path.abspath(__file__))
os.chdir(D)
FONT = '../eg/NotoNaskhArabic-Bold.ttf'
W, H, FPS, SR = 1920, 1080, 30, 48000
s = json.load(open('script.json'))
lines = {x['i']: x['dur'] for x in json.load(open('lines.json'))}
os.makedirs('clips', exist_ok=True); os.makedirs('ov', exist_ok=True); os.makedirs('big', exist_ok=True)

# ---------- image per scene (reuse = previous scene's image) ----------
imgs = []
for i, x in enumerate(s):
    if x.get('file') == 's01': imgs.append('img/4.png')
    elif x.get('hud') == 'black': imgs.append(None)
    elif x.get('hud') == 'title': imgs.append('img/0.png')
    elif x.get('reuse'): imgs.append(imgs[-1])
    elif os.path.exists(f'img/{i}.png'): imgs.append(f'img/{i}.png')
    else: imgs.append(imgs[-1])  # missing image: hold the previous one

# ---------- timing ----------
LONG_GAP = {3, 14, 40, 47, 55, 61}
times = []; t = 0.0
for i, x in enumerate(s):
    lead = 0.35
    d = lines[i] + lead + (1.6 if i in LONG_GAP else 0.75)
    if x.get('hud') == 'title': d = max(d, 3.2)
    if x.get('hud') == 'black': d = lines[i] + 3.5
    times.append((t, d)); t += d
TOTAL = t
print('total', round(TOTAL, 1), 's')

# ---------- text overlays (PIL + raqm for Arabic) ----------
def font(sz): return ImageFont.truetype(FONT, sz, layout_engine=ImageFont.Layout.RAQM)
def text_img(txt, sz, color=(255, 255, 255), stroke=6, sc=(0, 0, 0)):
    f = font(sz); tmp = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    bb = tmp.textbbox((0, 0), txt, font=f, stroke_width=stroke, direction='rtl', language='ar')
    im = Image.new('RGBA', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=color, stroke_width=stroke, stroke_fill=sc, direction='rtl', language='ar')
    return im
AR = '٠١٢٣٤٥٦٧٨٩'
def ar(n): return ''.join(AR[int(c)] if c.isdigit() else c for c in str(n))

def overlay(i, x):
    """Full-frame transparent PNGs: subtitle + day HUD (+ event pop, handled separately)."""
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if x.get('hud') not in ('title', 'black'):
        sub = text_img(x['vo'], 56)
        if sub.width > W - 160:
            r = (W - 160) / sub.width; sub = sub.resize((int(sub.width * r), int(sub.height * r)), Image.LANCZOS)
        base.alpha_composite(sub, ((W - sub.width) // 2, H - sub.height - 70))
    if i >= 4 and x.get('hud') not in ('title', 'black'):
        day = text_img('اليوم ' + ar(1) + ' من ' + ar(30), 46, (255, 214, 90), 5)
        pill = Image.new('RGBA', (day.width + 40, day.height + 10), (0, 0, 0, 150))
        pill.alpha_composite(day, (20, 5)); base.alpha_composite(pill, (W - pill.width - 50, 40))
    base.save(f'ov/sub{i:02d}.png')
    hud = x.get('hud', '')
    pop = None
    if hud.startswith('-') or hud.endswith('%🔋') or hud.endswith('°C') or hud.endswith('🕯️'):
        import re as _re
        m = _re.match(r'^([-0-9,%°C]+)\s*(.*)$', hud.replace('🔋', '').replace('🕯️', ''))
        num, word = m.group(1), m.group(2)
        word = {'⚡': 'كهرباء', '': {'%': 'بطارية', 'C': 'حرارة'}.get(num[-1], 'شموع')}.get(word, word)
        col = (255, 80, 70) if hud.startswith('-') else (255, 214, 90)
        fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 84)
        tmp = ImageDraw.Draw(Image.new('RGBA', (10, 10))); bb = tmp.textbbox((0, 0), num.replace('-', '−'), font=fn, stroke_width=7)
        ni = Image.new('RGBA', (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
        ImageDraw.Draw(ni).text((10 - bb[0], 10 - bb[1]), num.replace('-', '−'), font=fn, fill=col, stroke_width=7, stroke_fill=(0, 0, 0))
        wi = text_img(word, 84, col, 7)
        p = Image.new('RGBA', (W, H), (0, 0, 0, 0)); p.alpha_composite(ni, (90, 160 + (wi.height - ni.height) // 2)); p.alpha_composite(wi, (90 + ni.width + 10, 160))
        p.save(f'ov/pop{i:02d}.png'); pop = f'ov/pop{i:02d}.png'
    if hud == '30':
        p = Image.new('RGBA', (W, H), (0, 0, 0, 0)); im = text_img('٣٠ يوم', 220, (255, 214, 90), 10)
        p.alpha_composite(im, ((W - im.width) // 2, 300)); p.save(f'ov/pop{i:02d}.png'); pop = f'ov/pop{i:02d}.png'
    if hud == 'title':
        p = Image.new('RGBA', (W, H), (0, 0, 0, 170)); a = text_img('انقطاع الكهرباء', 150, (255, 255, 255), 8); b = text_img('٣٠ يوم', 190, (255, 214, 90), 9); c = text_img('اليوم الأول', 80, (230, 230, 230), 6)
        p.alpha_composite(a, ((W - a.width) // 2, 230)); p.alpha_composite(b, ((W - b.width) // 2, 420)); p.alpha_composite(c, ((W - c.width) // 2, 700))
        p.save(f'ov/pop{i:02d}.png'); pop = f'ov/pop{i:02d}.png'
    if hud == 'day':
        p = Image.new('RGBA', (W, H), (0, 0, 0, 0)); im = text_img('اليوم ' + ar(1) + ' — الصباح', 90, (255, 214, 90), 7)
        p.alpha_composite(im, ((W - im.width) // 2, 140)); p.save(f'ov/pop{i:02d}.png'); pop = f'ov/pop{i:02d}.png'
    if hud == 'black':
        p = Image.new('RGBA', (W, H), (0, 0, 0, 0)); im = text_img('باقي ' + ar(29) + ' يوم', 170, (255, 255, 255), 0)
        p.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2 - 40)); p.save(f'ov/pop{i:02d}.png'); pop = f'ov/pop{i:02d}.png'
    return pop

# ---------- clips ----------
def bigimg(path):
    out = 'big/' + os.path.basename(path)
    if not os.path.exists(out):
        Image.open(path).convert('RGB').resize((3840, 2160), Image.LANCZOS).save(out)
    return out

moves = ['in', 'out', 'panr', 'panl', 'in2', 'up']
for i, x in enumerate(s):
    st, d = times[i]; n = int(round(d * FPS)); out = f'clips/{i:02d}.mp4'
    pop = overlay(i, x)
    if os.path.exists(out) and not os.environ.get('FORCE'): continue
    fade = f"fade=t=in:st=0:d=0.25,fade=t=out:st={d-0.25:.3f}:d=0.25"
    if imgs[i] is None:
        src = ['-f', 'lavfi', '-t', f'{d:.3f}', '-i', f'color=black:s={W}x{H}:r={FPS}']
        vf = f"[0:v]format=yuv420p[bg]"
    else:
        mv = moves[i % len(moves)]
        z = {'in': "1+0.10*on/{n}", 'in2': "1.05+0.10*on/{n}", 'out': "1.12-0.10*on/{n}", 'panr': "1.12", 'panl': "1.12", 'up': "1.10"}[mv].format(n=n)
        xx = {'panr': "(iw-iw/zoom)*on/{n}", 'panl': "(iw-iw/zoom)*(1-on/{n})"}.get(mv, "(iw-iw/zoom)/2").format(n=n)
        yy = {'up': "(ih-ih/zoom)*(1-on/{n})"}.get(mv, "(ih-ih/zoom)/2").format(n=n)
        src = ['-loop', '1', '-framerate', str(FPS), '-t', f'{d:.3f}', '-i', bigimg(imgs[i])]
        vf = f"[0:v]zoompan=z='{z}':x='{xx}':y='{yy}':d={n}:s={W}x{H}:fps={FPS},format=yuv420p[bg]"
    inputs = src + ['-i', f'ov/sub{i:02d}.png']; chain = vf + ";[bg][1:v]overlay=0:0[a]"; last = 'a'
    if pop:
        inputs += ['-i', pop]
        pin = 0.35 if x.get('hud') not in ('title', 'black') else 0.2
        pdur = d - pin - 0.2 if x.get('hud') in ('title', 'black', '30', 'day') else min(2.6, d - pin - 0.2)
        chain += f";[2:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={max(0.3,pdur-0.3):.2f}:d=0.3:alpha=1,setpts=PTS+{pin}/TB[p];[a][p]overlay=0:0:eof_action=pass[b]"; last = 'b'
        inputs[-2:-2] = ['-loop', '1', '-t', f'{pdur:.2f}']
    chain += f";[{last}]{fade}[v]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', chain, '-map', '[v]', '-frames:v', str(n), '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], check=True)
    print('clip', i, round(d, 2))

with open('clips/list.txt', 'w') as f:
    for i in range(len(s)): f.write(f"file '{i:02d}.mp4'\n")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'clips/list.txt', '-c', 'copy', 'video_noaudio.mp4'], check=True)

# ---------- audio: narration + synthesized ambience/SFX (no music) ----------
N = int(TOTAL * SR) + SR
mix = np.zeros(N, np.float32); amb = np.zeros(N, np.float32)
rng = np.random.default_rng(7)
def load(fn):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', fn, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(r, np.float32)
def put(buf, sig, t, g=1.0):
    a = int(t * SR); b = min(len(buf), a + len(sig)); buf[a:b] += sig[:b - a] * g
def lp(x, a): # one-pole lowpass
    y = np.empty_like(x); acc = 0.0
    for k in range(len(x)): acc += a * (x[k] - acc); y[k] = acc
    return y
def noise(sec, a=0.05):
    from scipy.signal import lfilter
    n = rng.standard_normal(int(sec * SR)).astype(np.float32)
    return lfilter([a], [1, a - 1], n).astype(np.float32)
try:
    import scipy  # noqa
except ImportError:
    subprocess.run(['pip', 'install', '-q', 'scipy'])
from scipy.signal import lfilter
def crickets(sec):
    t = np.arange(int(sec * SR)) / SR; out = np.zeros_like(t, dtype=np.float32)
    for c in range(3):
        f = 4200 + c * 600; rate = 14 + c * 3; ph = rng.random() * 6
        gate = (np.sin(2 * np.pi * rate * t + ph) > 0.6).astype(np.float32)
        burst = (np.sin(2 * np.pi * 0.5 * t + c) > -0.2).astype(np.float32)
        out += np.sin(2 * np.pi * f * t) * gate * burst * 0.02
    return out
def wind(sec, g=0.08):
    n = noise(sec, 0.02); t = np.arange(len(n)) / SR
    return n * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t)) * g * 6
def murmur(sec, g=0.05):
    n = rng.standard_normal(int(sec * SR)).astype(np.float32)
    b = lfilter([0.08], [1, -0.92], n); b = b - lfilter([0.01], [1, -0.99], b)
    t = np.arange(len(b)) / SR
    return (b * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * t)) * g * 3).astype(np.float32)
def horn(t0, buf, f=420, d=0.5, g=0.08):
    t = np.arange(int(d * SR)) / SR; env = np.minimum(1, t * 30) * np.minimum(1, (d - t) * 20)
    sig = (np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * 1.26 * t) * 0.5) * env
    put(buf, lfilter([0.3], [1, -0.7], sig).astype(np.float32), t0, g)
def flies(sec, g=0.04):
    t = np.arange(int(sec * SR)) / SR; f = 210 + 25 * np.sin(2 * np.pi * 0.9 * t) + 15 * np.sin(2 * np.pi * 3.1 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR; s_ = (np.mod(ph, 2 * np.pi) / np.pi - 1)
    return (s_ * (0.5 + 0.5 * np.sin(2 * np.pi * 0.4 * t) ** 2) * g).astype(np.float32)
def ding(g=0.25):
    t = np.arange(int(0.7 * SR)) / SR
    return ((np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 6) + np.sin(2 * np.pi * 1760 * t) * np.exp(-(t - 0.15).clip(0) * 6) * (t > 0.15)) * g).astype(np.float32)
def thump(f=55, d=0.35, g=0.6):
    t = np.arange(int(d * SR)) / SR; fr = f * (1 + 1.5 * np.exp(-t * 30))
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 12) * g).astype(np.float32)
def knock(g=0.7):
    t = np.arange(int(0.25 * SR)) / SR; n = rng.standard_normal(len(t))
    return ((lfilter([0.2], [1, -0.8], n) * np.exp(-t * 40) * 2 + np.sin(2 * np.pi * 140 * t) * np.exp(-t * 25)) * g).astype(np.float32)
def boom(g=0.9):
    t = np.arange(int(2.5 * SR)) / SR; fr = 40 + 80 * np.exp(-t * 6)
    s_ = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 1.6); n = lfilter([0.05], [1, -0.95], rng.standard_normal(len(t))) * np.exp(-t * 3) * 3
    return ((s_ + n) * g).astype(np.float32)
def hit(g=0.5):
    t = np.arange(int(1.0 * SR)) / SR; fr = 60 + 60 * np.exp(-t * 10)
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 4) * g).astype(np.float32)

def section(i):
    if i <= 13 or i == 54: return 'night_out'
    if i <= 19 or 23 <= i <= 35 or i == 38: return 'street'
    if i in (20, 21, 22): return 'kitchen'
    if i in (36, 37, 39, 45, 46): return 'wind'
    if 40 <= i <= 44: return 'murmur'
    if 47 <= i <= 53: return 'night_in'
    if 55 <= i <= 60: return 'alley'
    return 'none'
for i, x in enumerate(s):
    st, d = times[i]; sec = section(i)
    if sec == 'night_out': put(amb, crickets(d) + wind(d, 0.03), st)
    elif sec == 'street':
        put(amb, murmur(d, 0.06) + wind(d, 0.02), st)
        for k in range(int(d // 2.5)):
            if rng.random() < 0.6: horn(st + 0.5 + k * 2.5 + rng.random(), amb, f=rng.choice([380, 440, 520]), d=0.3 + rng.random() * 0.4, g=0.05)
    elif sec == 'kitchen': put(amb, flies(d, 0.05 if i in (20, 21) else 0.02) + wind(d, 0.01), st)
    elif sec == 'wind': put(amb, wind(d, 0.05), st)
    elif sec == 'murmur': put(amb, murmur(d, 0.05), st)
    elif sec == 'night_in': put(amb, crickets(d) * 0.5 + wind(d, 0.015), st)
    elif sec == 'alley': put(amb, crickets(d) * 0.35 + wind(d, 0.04), st)
    if i == 54: put(amb, flies(d, 0.03) * 1.0, st)  # mosquitoes
    sfx = x.get('sfx')
    if sfx == 'sms': put(mix, ding(), st + 0.1)
    if sfx == 'hit' or (x.get('hud', '').startswith('-')): put(mix, hit(0.35), st + 0.35)
    if sfx == 'heart':
        for k in range(int(d / 0.8)): put(mix, thump(50, 0.3, 0.5), st + k * 0.8); put(mix, thump(46, 0.3, 0.35), st + k * 0.8 + 0.22)
    if sfx == 'knock':
        for k, dt in enumerate([0.2, 0.5, lines[i] * 0.55 + 0.4, lines[i] * 0.55 + 0.7]): put(mix, knock(), st + dt)
    if sfx == 'boom': put(mix, boom(), st + 0.05)
    if x.get('hud') == 'title': put(mix, boom(0.6), st + 0.05)
# narration
for i, x in enumerate(s):
    st, d = times[i]; put(mix, load(f'line{i:02d}.wav') * 1.0, st + 0.35)
# black scene: everything silent except boom + narration
st, d = times[-1]; amb[int(st * SR):] = 0
# fades between scenes for ambience
mix += amb
mix = mix[:int(TOTAL * SR)]
mix /= max(1e-6, np.abs(mix).max()) / 0.9
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'video_noaudio.mp4', '-i', 'audio.wav', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', 'episode1.mp4'], check=True)
json.dump([{'i': i, 'start': round(t0, 3), 'dur': round(dd, 3)} for i, (t0, dd) in enumerate(times)], open('timeline.json', 'w'))
print('done', TOTAL)
