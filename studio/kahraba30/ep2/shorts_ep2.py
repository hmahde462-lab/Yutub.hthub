# 8 vertical shorts from kahraba30 ep2 long video (subs already burned): blurred bg + full 16:9 frame + header/part pill/end card.
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920; F = 'NotoNaskhArabic-Bold.ttf'; SRC = '../../../videos/long/kahraba30-ep2.mp4'
tl = json.load(open('timeline.json')); st = {x['i']: x['start'] for x in tl}; END = tl[-1]['start'] + tl[-1]['dur']
R = [(0, 4), (5, 12), (13, 18), (19, 27), (28, 35), (36, 42), (43, 48), (49, 53)]
AR = '٠١٢٣٤٥٦٧٨٩'; ar = lambda n: ''.join(AR[int(c)] if c.isdigit() else c for c in str(n))
def font(sz): return ImageFont.truetype(F, sz, layout_engine=ImageFont.Layout.RAQM)
def timg(t, sz, col=(255, 255, 255), stroke=7):
    f = font(sz); d = ImageDraw.Draw(Image.new('RGBA', (10, 10))); bb = d.textbbox((0, 0), t, font=f, stroke_width=stroke, direction='rtl', language='ar')
    im = Image.new('RGBA', (bb[2]-bb[0]+20, bb[3]-bb[1]+20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10-bb[0], 10-bb[1]), t, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0), direction='rtl', language='ar'); return im
OUT = '../../../videos/shorts/kahraba30-ep2'; os.makedirs(OUT, exist_ok=True); os.makedirs('sov', exist_ok=True)
for p, (a, b) in enumerate(R, 1):
    t0 = st[a]; t1 = st[b+1] if b+1 in st else END; d = t1 - t0
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    h = timg('العراق بدون كهرباء ٣٠ يوم', 84); ov.alpha_composite(h, ((W-h.width)//2, 230))
    tag = timg('الحلقة ٢ - الجزء ' + ar(p) + ' من ' + ar(len(R)), 58, (255, 214, 60), 6)
    pill = Image.new('RGBA', (tag.width + 50, tag.height + 10), (200, 20, 30, 230)); pill.alpha_composite(tag, (25, 5)); ov.alpha_composite(pill, ((W-pill.width)//2, 230 + h.height + 20))
    ov.save(f'sov/h{p}.png')
    e = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ec = timg('الحلقة كاملة بالقناة', 80, (255, 214, 60))
    box = Image.new('RGBA', (W, ec.height + 40), (0, 0, 0, 170)); box.alpha_composite(ec, ((W-ec.width)//2, 20)); e.alpha_composite(box, (0, 1480)); e.save(f'sov/e{p}.png')
    chain = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=25:2,eq=brightness=-0.2[bg];[b]scale={W}:-2[fg];"
             f"[bg][fg]overlay=0:(H-h)/2[v0];[v0][1:v]overlay=0:0[v1];[v1][2:v]overlay=0:0:enable='gte(t,{d-2.5:.2f})'[v]")
    out = f'{OUT}/kahraba30-ep2-part{p}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', SRC, '-i', f'sov/h{p}.png', '-i', f'sov/e{p}.png',
                    '-filter_complex', chain, '-map', '[v]', '-map', '0:a', '-af', f'afade=t=in:d=0.15,afade=t=out:st={d-0.4:.2f}:d=0.4',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-r', '30', out], check=True)
    print(out, round(d, 1))
