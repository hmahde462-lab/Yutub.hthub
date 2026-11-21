# Vertical 9:16 shorts from the clean (no-subtitle) long video: blurred bg + 4:3 crop + big Arabic subs + part header/end card.
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
W, H = 1080, 1920
F = 'NotoNaskhArabic-Bold.ttf'
sc = json.load(open('script.json')); tl = {x['i']: (x['start'], x['dur']) for x in json.load(open('timeline.json'))}
END = tl[len(sc)-1][0] + tl[len(sc)-1][1]
PN = sorted({x['part'] for x in sc}); PARTS = [(min(i for i, x in enumerate(sc) if x['part'] == p), max(i for i, x in enumerate(sc) if x['part'] == p)) for p in PN]
AR = '٠١٢٣٤٥٦٧٨٩'
def ar(n): return ''.join(AR[int(c)] if c.isdigit() else c for c in str(n))
def font(sz): return ImageFont.truetype(F, sz, layout_engine=ImageFont.Layout.RAQM)
def timg(t, sz, col=(255, 255, 255), stroke=7):
    f = font(sz); d = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    bb = d.textbbox((0, 0), t, font=f, stroke_width=stroke, direction='rtl', language='ar')
    im = Image.new('RGBA', (bb[2]-bb[0]+20, bb[3]-bb[1]+20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10-bb[0], 10-bb[1]), t, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0), direction='rtl', language='ar')
    return im
def wrap(t, sz, maxw):
    words = t.split(); rows = []; cur = ''
    for w in words:
        nxt = (cur + ' ' + w).strip()
        if cur and timg(nxt, sz).width > maxw: rows.append(cur); cur = w
        else: cur = nxt
    rows.append(cur); return rows
def stack(rows, sz, col, gap=6):
    ims = [timg(r, sz, col) for r in rows]; w = max(i.width for i in ims); h = sum(i.height for i in ims) + gap*(len(ims)-1)
    out = Image.new('RGBA', (W, h), (0, 0, 0, 0)); y = 0
    for i in ims: out.alpha_composite(i, ((W - i.width)//2, y)); y += i.height + gap
    return out
HEAD = 'وقعت من السما ونجت!'; SLUG = 'koepcke'; CLEAN = 'koepcke_clean.mp4'; OUTDIR = '../../../videos/shorts/' + SLUG
os.makedirs('sov', exist_ok=True); os.makedirs(OUTDIR, exist_ok=True)
FG_Y, FG_H = 470, 810
for p, (a, b) in enumerate(PARTS, 1):
    t0 = tl[a][0]; t1 = tl[b+1][0] if b+1 < len(sc) else END; d = t1 - t0
    head = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    h1 = stack([HEAD], 84, (255, 255, 255)); head.alpha_composite(h1, (0, 120))
    tag = timg('الجزء ' + ar(p) + ' من ' + ar(len(PARTS)), 60, (255, 214, 60), 6)
    pill = Image.new('RGBA', (tag.width + 50, tag.height + 10), (200, 20, 30, 230)); pill.alpha_composite(tag, (25, 5))
    head.alpha_composite(pill, ((W - pill.width)//2, 120 + h1.height + 20)); head.save(f'sov/head{p}.png')
    inputs = ['-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', CLEAN, '-i', f'sov/head{p}.png']
    chain = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=25:2,eq=brightness=-0.18[bg];"
             f"[b]crop=1440:1080,scale={W}:{FG_H}[fg];[bg][fg]overlay=0:{FG_Y}[v0];[v0][1:v]overlay=0:0[v1]")
    last = 'v1'; k = 2
    for i in range(a, b+1):
        x = sc[i]
        if x.get('hud') in ('title', 'black') or not x['vo']: continue
        s = stack(wrap(x['vo'], 70, W - 120), 70, (255, 255, 255)); s.save(f'sov/s{p}_{i}.png')
        st = tl[i][0] - t0; en = st + tl[i][1]
        inputs += ['-i', f'sov/s{p}_{i}.png']
        chain += f";[{last}][{k}:v]overlay=0:{FG_Y + FG_H + 60}:enable='between(t,{st:.2f},{en:.2f})'[v{k}]"; last = f'v{k}'; k += 1
    if True:
        e = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ec = stack(['القصة كاملة بالقناة'], 80, (255, 214, 60))
        box = Image.new('RGBA', (W, ec.height + 40), (0, 0, 0, 170)); box.alpha_composite(ec, (0, 20)); e.alpha_composite(box, (0, 1650)); e.save(f'sov/end{p}.png')
        inputs += ['-i', f'sov/end{p}.png']
        chain += f";[{last}][{k}:v]overlay=0:0:enable='gte(t,{d-2.5:.2f})'[v{k}]"; last = f'v{k}'
    out = OUTDIR + f'/{SLUG}-part{p}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', chain, '-map', f'[{last}]', '-map', '0:a',
                    '-af', f'afade=t=in:d=0.15,afade=t=out:st={d-0.4:.2f}:d=0.4', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-r', '30', out], check=True)
    print(out, round(d, 1))
