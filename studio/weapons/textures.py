"""Tileable PBR texture sets (albedo, ORM [R=AO,G=rough,B=metal], normal) generated procedurally.
Usage: python3 textures.py [size]  -> writes tex/<mat>_{albedo,orm,normal}.png
"""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tex')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)


def fnoise(scale, aniso=(1.0, 1.0), seed=None):
    """Tileable band-limited noise via FFT filtering. scale ~ feature size in pixels."""
    r = np.random.default_rng(seed) if seed is not None else rng
    w = r.standard_normal((S, S))
    fy = np.fft.fftfreq(S)[:, None] * aniso[1]
    fx = np.fft.fftfreq(S)[None, :] * aniso[0]
    f = np.sqrt(fx * fx + fy * fy)
    filt = np.exp(-(f * scale) ** 2 * 6.0)
    n = np.real(np.fft.ifft2(np.fft.fft2(w) * filt))
    n -= n.mean(); n /= (n.std() + 1e-9)
    return n


def fbm(base, octaves=4, aniso=(1, 1), seed=0):
    acc = np.zeros((S, S)); amp = 1; tot = 0
    for i in range(octaves):
        acc += amp * fnoise(base / (2 ** i), aniso, seed + i); tot += amp; amp *= 0.5
    return acc / tot


def scratches(count, maxlen, width=1, seed=1):
    """Tileable scratch mask 0..1."""
    r = np.random.default_rng(seed)
    im = Image.new('L', (S, S), 0); d = ImageDraw.Draw(im)
    for _ in range(count):
        x, y = r.uniform(0, S, 2)
        ang = r.uniform(0, math.pi) if r.random() < 0.5 else r.normal(0.2, 0.25)
        L = r.uniform(maxlen * 0.15, maxlen)
        v = int(r.uniform(25, 150) if r.random()<0.85 else r.uniform(150,230))
        wd = max(1, int(r.choice([width, width, width + 1])))
        # slightly curved scratch as polyline
        pts = []
        cur = r.normal(0, 0.002)
        for t in np.linspace(0, 1, 6):
            a = ang + cur * t * L
            pts.append((x + math.cos(a) * L * t, y + math.sin(a) * L * t))
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                d.line([(p[0] + ox, p[1] + oy) for p in pts], fill=v, width=wd)
    return np.asarray(im, np.float32) / 255.0


def pits(count, rad, seed=2):
    r = np.random.default_rng(seed)
    im = Image.new('L', (S, S), 0); d = ImageDraw.Draw(im)
    for _ in range(count):
        x, y = r.uniform(0, S, 2); rr = r.uniform(rad * 0.3, rad)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                d.ellipse([x + ox - rr, y + oy - rr, x + ox + rr, y + oy + rr], fill=int(r.uniform(80, 255)))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(1)), np.float32) / 255.0


def normal_from_height(h, strength):
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * strength
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * strength
    n = np.stack([-gx, gy, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return ((n * 0.5 + 0.5) * 255).astype(np.uint8)


def save(name, albedo, rough, metal, ao, height, nstr):
    a = np.clip(albedo, 0, 1)
    Image.fromarray((a ** (1 / 2.2) * 255).astype(np.uint8)).save(f'{OUT}/{name}_albedo.png', optimize=True)
    orm = np.stack([np.clip(ao, 0, 1), np.clip(rough, 0.03, 1), np.clip(metal, 0, 1)], -1)
    Image.fromarray((orm * 255).astype(np.uint8)).save(f'{OUT}/{name}_orm.png', optimize=True)
    Image.fromarray(normal_from_height(height, nstr)).save(f'{OUT}/{name}_normal.png', optimize=True)
    print('wrote', name)


def col(rgb):  # linear rgb from srgb 0..255
    return (np.array(rgb, np.float32) / 255.0) ** 2.2


def metal_finish(name, base_rgb, bare_rgb, rough0, metal0, scratch_n, dirt_amt, grain, seed):
    g = fbm(S / 6, 4, seed=seed)                 # large blotches
    fine = fnoise(1.2, seed=seed + 10)           # micro grain
    sc = scratches(scratch_n, S * 0.12, 1, seed + 20)
    sc2 = scratches(scratch_n // 3, S * 0.05, 2, seed + 21) * 0.6
    scr = np.clip(sc + sc2, 0, 1)
    wear = np.clip((fbm(S / 6, 4, seed=seed + 30) - 1.5) * 0.7, 0, 0.6)   # worn patches (bare metal)
    dirt = np.clip((fbm(S / 5, 4, seed=seed + 40) - 0.3) * 0.6, 0, 1) * dirt_amt
    pit = pits(int(S * 1.2), 2.2, seed + 50)
    base = col(base_rgb)[None, None] * (1 + 0.06 * g[..., None] + grain * 0.04 * fine[..., None])
    bare = col(bare_rgb)[None, None]
    k = np.clip(scr * 0.55 + wear * 0.5, 0, 1)[..., None]
    alb = base * (1 - k) + bare * k
    alb = alb * (1 - 0.45 * dirt[..., None]) + col((60, 52, 40))[None, None] * 0.45 * dirt[..., None]
    alb *= (1 - 0.25 * pit[..., None])
    rough = rough0 + 0.05 * g + grain * 0.04 * fine - 0.25 * k[..., 0] + 0.25 * dirt
    metal = metal0 + (1 - metal0) * k[..., 0] * 0.9 - 0.4 * dirt
    ao = 1 - 0.25 * pit - 0.2 * dirt
    height = 0.25 * fine * grain - 1.5 * scr - 1.2 * pit + 0.3 * g
    save(name, alb, rough, metal, ao, height, 1.2)


def polymer(name, rgb, seed, texture_amt=1.0):
    stip = fnoise(1.6, seed=seed)                  # stippled molded texture
    blot = fbm(S / 6, 4, seed=seed + 1)
    scr = scratches(90, S * 0.08, 1, seed + 2)
    scuff = np.clip((fbm(S / 12, 3, seed=seed + 3) - 1.0), 0, 1)
    dirt = np.clip((fbm(S / 5, 4, seed=seed + 4) - 0.4) * 0.5, 0, 1)
    alb = col(rgb)[None, None] * (1 + 0.05 * blot[..., None] + 0.03 * stip[..., None])
    alb = alb * (1 + 0.6 * scr[..., None] + 0.25 * scuff[..., None])
    alb = alb * (1 - 0.3 * dirt[..., None]) + col((70, 60, 45))[None, None] * 0.3 * dirt[..., None]
    rough = 0.62 + 0.08 * stip * texture_amt + 0.05 * blot - 0.15 * scuff + 0.12 * scr + 0.1 * dirt
    ao = 1 - 0.15 * dirt
    height = 0.5 * stip * texture_amt - 1.0 * scr
    save(name, alb, rough, np.zeros((S, S)), ao, height, 1.3)


def wood(name, seed):
    # grain runs along U (x); tileable since built from periodic noise
    warp = fbm(S / 1.2, 2, aniso=(6.0, 1.0), seed=seed)
    y = np.arange(S)[:, None] / S
    rings = np.sin((y * 9 + warp * 0.9 + 0.6 * fnoise(S / 3, aniso=(10.0, 1.0), seed=seed + 9) * 0.1) * 2 * math.pi)
    streak = fnoise(2, aniso=(30.0, 1.0), seed=seed + 1)
    pores = np.clip(fnoise(1.0, aniso=(6.0, 1.0), seed=seed + 2) - 1.4, 0, 1)
    t = 0.5 + 0.18 * rings + 0.22 * streak
    c1, c2 = col((122, 62, 30)), col((70, 33, 16))
    alb = c1[None, None] * t[..., None] + c2[None, None] * (1 - t[..., None])
    scr = scratches(80, S * 0.1, 1, seed + 3)
    dings = pits(300, 5, seed + 4)
    dirt = np.clip((fbm(S / 6, 4, seed=seed + 5) - 0.3) * 0.5, 0, 1)
    alb = alb * (1 - 0.45 * pores[..., None]) * (1 + 0.5 * scr[..., None]) * (1 - 0.3 * dings[..., None])
    alb = alb * (1 - 0.35 * dirt[..., None])
    rough = 0.45 + 0.12 * (1 - t) + 0.3 * pores + 0.2 * scr + 0.15 * dirt  # oiled/varnished wood
    ao = 1 - 0.3 * dings - 0.15 * dirt
    height = 0.4 * rings + 0.5 * streak - 1.5 * pores - 1.5 * scr - 2.0 * dings
    save(name, alb, rough, np.zeros((S, S)), ao, height, 1.2)


def rubber(name, seed):
    n = fnoise(1.3, seed=seed); b = fbm(S / 8, 3, seed=seed + 1)
    dust = np.clip(fbm(S / 4, 4, seed=seed + 2) - 0.5, 0, 1) * 0.4
    alb = col((24, 24, 24))[None, None] * (1 + 0.08 * n[..., None] + 0.05 * b[..., None])
    alb = alb + col((90, 85, 75))[None, None] * dust[..., None] * 0.3
    save(name, alb, 0.85 + 0.05 * n + 0.05 * dust, np.zeros((S, S)), 1 - 0.1 * dust, 1.2 * n, 1.5)


def checker_knurl(name, seed):
    """Diamond knurling for grips, rubber/polymer."""
    x = np.arange(S)[None, :]; y = np.arange(S)[:, None]
    p = S / 128
    a = np.abs(((x + y) / p) % 2 - 1); b = np.abs(((x - y) / p) % 2 - 1)
    h = np.minimum(a, b)
    n = fnoise(1.5, seed=seed)
    alb = col((30, 30, 30))[None, None] * (0.85 + 0.3 * h[..., None] + 0.04 * n[..., None])
    rough = 0.7 + 0.15 * (1 - h)
    save(name, alb, rough, np.zeros((S, S)), 0.7 + 0.3 * h, 2.5 * h + 0.3 * n, 2.0)


if __name__ == '__main__':
    metal_finish('gunmetal', (38, 39, 40), (150, 150, 152), 0.48, 0.85, 260, 0.8, 1.0, 100)        # parkerized steel
    metal_finish('anodized', (30, 31, 33), (175, 175, 178), 0.42, 0.75, 200, 0.6, 0.6, 200)        # black anodized aluminum
    metal_finish('steel', (120, 120, 124), (190, 190, 192), 0.30, 1.0, 180, 0.5, 0.6, 300)        # bare/blued steel (bolts, barrels)
    metal_finish('akblued', (34, 33, 35), (140, 138, 136), 0.40, 0.9, 380, 1.0, 1.0, 400)       # worn blued steel AK
    polymer('polymer', (33, 33, 34), 500)
    polymer('polymer_fde', (160, 132, 96), 600)
    wood('wood', 700)
    rubber('rubber', 800)
    checker_knurl('grip', 900)
    metal_finish('brass', (176, 132, 62), (215, 175, 100), 0.32, 1.0, 60, 0.3, 0.4, 1000)
    polymer('polymer_red', (140, 22, 18), 1100, 0.3)
