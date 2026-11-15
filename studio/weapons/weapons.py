"""Procedural FPS weapon models. Run:  python3 weapons.py [m4 ak lmg sniper shotgun smg optics] [--preview] [--mobile]
Outputs glb/<Name>.glb (2K textures) and glb_mobile/<Name>.glb (1K textures)."""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *  # noqa
import lib

OUT = os.path.join(lib.HERE, 'glb')
OUTM = os.path.join(lib.HERE, 'glb_mobile')
PREV = os.path.join(lib.HERE, 'preview')


# ============================================================== shared sub-parts
def pistol_grip(name, top_y, mat_='polymer', angle=18, length=105, width=30, x=0):
    pts = [(-14, 8), (16, 8), (12, -20), (8, -50), (6, -90), (2, -104), (-24, -108), (-32, -98),
           (-28, -60), (-26, -30), (-22, -8)]
    pts = [(p[0] * length / 105, p[1] * length / 105) for p in pts]
    return profile(name, [(top_y + y, z) for y, z in pts], width, mat_, x=x, bevel=4, segs=3,
                   rot=(-angle + 8, 0, 0), origin=(0, top_y, 0))


def trigger(name, y, z, scale=1.0):
    s = scale
    pts = [(-2 * s, 0), (2.5 * s, 0), (4 * s, -8 * s), (3 * s, -15 * s), (0, -19 * s), (-2.5 * s, -18 * s),
           (-0.5 * s, -14 * s), (0.5 * s, -8 * s)]
    return profile(name, [(y + a, z + b) for a, b in pts], 6, 'steel', bevel=0.8, segs=2)


def trigger_guard(name, y0, y1, zt, mat_='anodized', w=12, drop=20):
    pts = [(y0, zt), (y0 + 4, zt), (y0 + 6, zt - drop + 4), (y1 - 6, zt - drop + 4), (y1 - 3, zt), (y1, zt),
           (y1, zt - drop + 2), (y1 - 4, zt - drop), (y0 + 2, zt - drop), (y0, zt - drop + 4)]
    return profile(name, pts, w, mat_, bevel=1.2)


def muzzle_birdcage(name, y, B, r=11, L=45):
    m = tube(name, r, 3.0, L, (0, y, B), 'gunmetal', seg=24)
    cut = box('cut', (40, 26, 4), (0, y + 24, B + 0), 'gunmetal', bevel=0)
    cut2 = box('cut2', (4, 26, 40), (0, y + 24, B + 0), 'gunmetal', bevel=0)
    cut3 = box('cut3', (30, 26, 4), (0, y + 24, B), 'gunmetal', bevel=0, rot=(0, 45, 0))
    for c in (cut, cut2, cut3):
        boolean(m, c)
    return m


def magazine_curved(name, top_y, depth, length, curve, width, mat_, ribs=True, top_z=3):
    """Curved box magazine side profile: top at z=top_z between top_y..top_y+depth, bends forward by `curve` mm."""
    n = 8; front, back = [], []
    for i in range(n + 1):
        t = i / n; z = top_z - length * t
        off = curve * t * t
        back.append((top_y + off, z)); front.append((top_y + depth + off + 4 * t, z))
    pts = back[::-1][:-0 or None]
    poly = [back[0]] + [front[i] for i in range(n + 1)] + [back[i] for i in range(n, 0, -1)]
    m = profile(name, poly, width, mat_, bevel=1.6, segs=2)
    parts = [m]
    fy = front[-1][0]; by = back[-1][0]; zb = top_z - length
    parts.append(profile(name + '_floor', [(by - 3, zb + 3), (fy + 4, zb + 3), (fy + 4, zb - 5), (by - 3, zb - 5)],
                         width + 3, mat_, bevel=1.5))
    if ribs:
        for k in (0.35, 0.65):
            i = int(k * n)
            yb, zb_ = back[i]; yf, _ = front[i]
            parts.append(profile(name + f'_rib{k}', [(yb + 4, zb_ + 6), (yf - 4, zb_ + 6), (yf - 4, zb_ - 6), (yb + 4, zb_ - 6)],
                                 width + 1.6, mat_, bevel=1.0))
    # top cartridge
    parts.append(cyl(name + '_round', 4.5, depth * 0.8, (0, top_y + 4, top_z + 3), 'brass', r2=2.8, seg=16))
    return join(name, parts)


# ============================================================== M4
def build_m4():
    reset(); B = 45; W = 'M4'
    S = []  # static parts
    # lower receiver
    lower = profile('lower', [(-75, 30), (-75, 10), (-66, 2), (-30, 0), (34, 0), (40, -46), (108, -46), (116, -8), (128, 8), (128, 30)],
                    22, 'anodized', bevel=1.5)
    S.append(lower)
    S.append(profile('magwell_flare', [(38, -34), (110, -34), (113, -50), (36, -50)], 25, 'anodized', bevel=2))
    S.append(profile('buffer_ring', [(-80, 52), (-72, 52), (-72, 24), (-80, 24)], 26, 'anodized', bevel=2))
    # upper receiver
    S.append(profile('upper', [(-75, 30), (-75, 60), (104, 60), (104, 30), (60, 30), (60, 34), (-60, 34), (-60, 30)],
                     24, 'anodized', bevel=2.2, segs=3))
    S.append(rail('upper_rail', 176, -73, 60))
    # ejection port recess + brass deflector + forward assist
    S.append(box('port_recess', (2, 58, 15), (11.6, 18, 45), 'bore', bevel=0.3))
    S.append(box('deflector', (8, 14, 14), (14, -12, 46), 'anodized', bevel=3))
    S.append(cyl('fwd_assist', 6.5, 26, (14, -48, 50), 'anodized', axis='Y', seg=20, bevel=1.5))
    S.append(cyl('fwd_assist_btn', 7.5, 6, (14, -54, 50), 'anodized', axis='Y', seg=20, bevel=1.2))
    # buffer tube + stock
    S.append(lathe('buffer_tube', [(0, 0), (14.5, 0), (14.5, 180), (13, 186), (0, 186)], 'anodized', (0, -80, 42), axis='-Y', seg=28))
    S.append(profile('stock', [(-195, 62), (-300, 66), (-306, 60), (-306, -44), (-296, -50), (-270, -48), (-250, -15),
                               (-205, 18), (-195, 30)], 42, 'polymer', bevel=5, segs=3))
    S.append(profile('buttpad', [(-306, 64), (-318, 64), (-318, -50), (-306, -46)], 44, 'rubber', bevel=4, segs=3))
    S.append(box('stock_latch', (10, 30, 8), (0, -230, 22), 'polymer', bevel=2))
    # pistol grip + guard + controls
    S.append(pistol_grip('grip', -8, 'grip'))
    S.append(trigger_guard('guard', -4, 46, 2, 'anodized', 12, 22))
    S.append(box('selector', (2.5, 6, 16), (-12.5, -12, 20), 'steel', bevel=0.8, rot=(30, 0, 0)))
    S.append(cyl('selector_hub', 5, 3, (-11, -12, 20), 'steel', axis='X', seg=16, bevel=0.6))
    S.append(cyl('mag_release', 4.5, 4, (11, 34, 12), 'steel', axis='X', seg=16, bevel=0.8))
    S.append(box('bolt_catch', (3, 20, 9), (-12, 30, 24), 'steel', bevel=1))
    for py in (-55, 117):
        S.append(cyl(f'pin{py}', 3, 25, (-12.5, py, 24 if py > 0 else 22), 'steel', axis='X', seg=12, bevel=0.5))
    # barrel + gas block + handguard
    S.append(lathe('barrel', [(0, 0), (11, 0), (11, 20), (8.5, 30), (8.5, 210), (7.6, 230), (7.6, 368), (0, 368)],
                   'gunmetal', (0, 104, B), seg=24))
    S.append(box('gas_block', (22, 18, 28), (0, 300, B + 2), 'gunmetal', bevel=2))
    hg = lathe('handguard', [(21, 0), (25, 0), (25, 270), (21, 270)], 'anodized', (0, 106, B), seg=8, rot_offset=22.5,
               smooth_angle=20)
    # M-LOK slots
    cutters = []
    for i in range(5):
        for side in (-1, 1):
            cutters.append(box(f'mlok{i}{side}', (14, 32, 7), (side * 23, 140 + i * 48, B - 2), 'anodized', bevel=3))
        cutters.append(box(f'mlokb{i}', (7, 32, 14), (0, 140 + i * 48, B - 23), 'anodized', bevel=3))
    cut = join('mlok_cut', cutters)
    boolean(hg, cut)
    S.append(hg)
    S.append(rail('hg_rail', 268, 107, B + 23))
    S.append(lathe('barrel_nut', [(0, 0), (19, 0), (19, 8), (17, 10), (0, 10)], 'anodized', (0, 100, B), seg=24))
    S.append(muzzle_birdcage('muzzle', 470, B))
    # folding back-up iron sights
    S.append(profile('rear_sight', [(-70, 64), (-48, 64), (-50, 80), (-56, 84), (-64, 84), (-68, 76)], 18, 'anodized', bevel=1.5))
    S.append(lathe('rear_aperture', [(1.2, 0), (4.5, 0), (4.5, 3), (1.2, 3)], 'steel', (0, -58, 79), seg=16))
    S.append(profile('front_sight', [(342, B + 29), (368, B + 29), (365, B + 44), (358, B + 52), (352, B + 52), (346, B + 40)],
                     16, 'anodized', bevel=1.5))
    S.append(cyl('front_post', 1.4, 10, (0, 356, B + 50), 'steel', axis='Z', seg=10, bevel=0.3))

    # moving parts
    mag = magazine_curved('mag', 43, 63, 178, 26, 21.5, 'polymer', top_z=0)
    charging = join('charging', [box('ch_bar', (10, 60, 6), (0, -72, 57), 'anodized', bevel=1),
                                 box('ch_t', (40, 9, 7), (0, -104, 57), 'anodized', bevel=2.5),
                                 box('ch_latch', (8, 10, 6), (-18, -100, 57), 'anodized', bevel=2)])
    bolt = join('bolt', [box('bcg', (2, 52, 12), (10.4, 20, 45), 'steel', bevel=0.6),
                         cyl('bolt_head', 4, 8, (10.4, 46, 46), 'steel', axis='X', seg=12, bevel=0.6)])
    dust = box('dust_cover', (1.6, 60, 16), (12.6, 18, 45), 'anodized', bevel=0.6)
    trig = trigger('trigger', 14, 6)
    moving = {'Magazine': (mag, (75, 0, 0)), 'ChargingHandle': (charging, (0, -75, 57)),
              'BoltCarrier': (bolt, (10, 20, 45)), 'DustCover': (dust, (13, 18, 38)), 'Trigger': (trig, (14, 4, 4))}
    sockets = {'Optic': (0, 0, 66.6), 'Muzzle': (0, 515, B), 'Eject': (14, 18, 46),
               'LeftHand': (0, 230, B - 26), 'RightHand': (0, -10, -20), 'IronSight': (0, -58, 80.5),
               'MagWell': (0, 75, 0)}
    return assemble(W, S, moving, sockets)



# ============================================================== AK-47
def build_ak():
    reset(); B = 40; W = 'AK47'
    S = []
    S.append(profile('receiver', [(-100, 36), (-100, 6), (-88, 0), (175, 0), (175, 36)], 28, 'akblued', bevel=1.5))
    S.append(profile('trunnion', [(150, 40), (190, 40), (190, 4), (150, 4)], 30, 'akblued', bevel=2))
    S.append(box('rear_sight_block', (26, 40, 16), (0, 205, B + 8), 'akblued', bevel=2))
    S.append(profile('rear_sight_leaf', [(190, B + 15), (240, B + 15), (240, B + 19), (200, B + 22)], 14, 'akblued', bevel=0.8))
    S.append(box('magwell_lip', (30, 8, 6), (0, 138, -2), 'akblued', bevel=1.5))
    # stock (wood) + buttplate
    S.append(profile('stock', [(-96, 32), (-470, -2), (-482, -6), (-482, -116), (-466, -120), (-170, -32), (-96, -4)],
                     36, 'wood', bevel=5, segs=3))
    S.append(profile('buttplate', [(-482, -4), (-490, -4), (-490, -118), (-482, -118)], 38, 'akblued', bevel=2))
    S.append(pistol_grip('grip', -30, 'polymer_red', angle=24, length=100, width=30))
    S.append(trigger_guard('guard', -14, 92, 1, 'akblued', 11, 20))
    # gas tube + upper handguard (wood) + lower handguard
    S.append(cyl('gas_tube', 9, 250, (0, 175, B + 17), 'akblued', seg=20, bevel=1))
    S.append(box('upper_hg', (30, 190, 22), (0, 340, B + 19), 'wood', bevel=9, segs=4))
    S.append(box('lower_hg', (46, 210, 42), (0, 300, B - 12), 'wood', bevel=12, segs=4))
    S.append(box('hg_retainer', (48, 10, 46), (0, 410, B - 6), 'akblued', bevel=2))
    S.append(box('hg_ferrule', (48, 10, 46), (0, 192, B - 8), 'akblued', bevel=2))
    # barrel, gas block, front sight, muzzle brake, cleaning rod
    S.append(lathe('barrel', [(0, 0), (12, 0), (12, 20), (9.5, 30), (9.5, 300), (8.5, 320), (8.5, 415), (0, 415)],
                   'akblued', (0, 175, B), seg=24))
    S.append(profile('gas_block', [(410, B - 10), (450, B - 10), (450, B + 26), (425, B + 28), (410, B + 18)], 22, 'akblued', bevel=2))
    S.append(profile('front_sight', [(530, B - 12), (560, B - 12), (560, B + 8), (552, B + 44), (538, B + 44), (532, B + 8)],
                     20, 'akblued', bevel=2))
    S.append(cyl('front_post', 1.6, 14, (0, 545, B + 36), 'steel', axis='Z', seg=10, bevel=0.3))
    br = tube('brake', 12, 4.5, 46, (0, 590, B), 'akblued', seg=24)
    boolean(br, box('slant', (40, 40, 30), (0, 640, B + 18), 'akblued', bevel=0, rot=(-30, 0, 0)))
    S.append(br)
    S.append(cyl('clean_rod', 3, 300, (0, 300, B - 15), 'steel', seg=10, bevel=0.8))
    S.append(box('sling_loop', (4, 14, 10), (-14, 425, B + 10), 'akblued', bevel=1))
    # moving
    mag = magazine_curved('mag', 98, 50, 215, 68, 26, 'akblued', top_z=0)
    cover = join('cover', [box('dust_cover', (28, 270, 16), (0, 30, 40), 'akblued', bevel=9, segs=4),
                           box('cover_tab', (12, 12, 10), (0, -108, 40), 'akblued', bevel=3)])
    for i in range(4):
        cover = join('cover', [cover, box(f'rib{i}', (29, 6, 13), (0, -40 + i * 40, 41), 'akblued', bevel=3)])
    carrier = join('carrier', [box('carrier_body', (4, 90, 12), (15, 100, 28), 'steel', bevel=1),
                               box('ch_arm', (14, 8, 6), (21, 145, 28), 'steel', bevel=1.5),
                               cyl('ch_knob', 6, 10, (26, 145, 28), 'steel', axis='X', seg=16, bevel=2)])
    sel = join('selector', [box('sel_plate', (2.5, 108, 10), (15.5, -10, 30), 'akblued', bevel=1, rot=(-6, 0, 0)),
                            box('sel_tab', (6, 10, 8), (17, 44, 25), 'akblued', bevel=2)])
    trig = trigger('trigger', 10, 6)
    moving = {'Magazine': (mag, (120, 0, 0)), 'DustCover': (cover, (0, -100, 40)), 'BoltCarrier': (carrier, (15, 100, 28)),
              'Selector': (sel, (15, -60, 32)), 'Trigger': (trig, (10, 4, 4))}
    sockets = {'Optic': (0, 210, B + 26), 'Muzzle': (0, 636, B), 'Eject': (16, 80, 34), 'LeftHand': (0, 300, B - 34),
               'RightHand': (0, -30, -20), 'IronSight': (0, 230, B + 21), 'MagWell': (0, 120, 0)}
    return assemble(W, S, moving, sockets)


# ============================================================== LMG (M249-style)
def build_lmg():
    reset(); B = 48; W = 'LMG'
    S = []
    S.append(profile('receiver', [(-130, 62), (-130, 8), (-115, 0), (195, 0), (195, 62)], 50, 'gunmetal', bevel=2))
    S.append(rail('cover_rail', 180, -30, 82))
    S.append(box('feed_tray', (56, 70, 6), (0, 120, 62), 'gunmetal', bevel=1.5))
    S.append(box('belt_guide', (20, 40, 26), (-34, 120, 52), 'gunmetal', bevel=2))
    S.append(box('mag_port', (22, 70, 36), (0, 60, -14), 'gunmetal', bevel=3))
    # stock
    S.append(profile('stock', [(-130, 58), (-430, 56), (-470, 60), (-482, 54), (-482, -78), (-466, -84), (-300, -40),
                               (-180, -10), (-130, 0)], 46, 'polymer', bevel=6, segs=3))
    cut = profile('stock_hole', [(-200, 34), (-400, 30), (-400, -30), (-320, -14), (-210, 14)], 60, 'polymer', bevel=0)
    S[-1] = boolean(S[-1], cut)
    S.append(profile('buttpad', [(-482, 56), (-494, 56), (-494, -84), (-482, -80)], 48, 'rubber', bevel=4))
    S.append(pistol_grip('grip', -40, 'grip', angle=20, length=110, width=32))
    S.append(trigger_guard('guard', -26, 40, 1, 'polymer', 14, 24))
    # heat shield, handguard, barrel, gas block, bipod, carry handle
    hs = box('heat_shield', (34, 160, 12), (0, 270, B + 19), 'gunmetal', bevel=4)
    vents = [box(f'v{i}', (40, 10, 4), (0, 210 + i * 22, B + 25), 'gunmetal', bevel=1.5) for i in range(6)]
    boolean(hs, join('vents', vents))
    S.append(hs)
    S.append(box('handguard', (54, 150, 34), (0, 268, B - 26), 'polymer', bevel=8, segs=3))
    S.append(lathe('barrel', [(0, 0), (14, 0), (14, 30), (12, 40), (12, 520), (0, 520)], 'gunmetal', (0, 190, B), seg=24))
    S.append(muzzle_birdcage('muzzle', 708, B, r=13, L=55))
    S.append(box('gas_block', (30, 46, 36), (0, 560, B - 12), 'gunmetal', bevel=3))
    S.append(box('front_sight', (12, 14, 40), (0, 690, B + 20), 'gunmetal', bevel=2))
    for sx in (-12, 12):
        S.append(cyl(f'bipod{sx}', 5.5, 230, (sx, 580, B - 30), 'gunmetal', axis='-Y', seg=12, bevel=1))
        S.append(box(f'foot{sx}', (12, 16, 10), (sx, 345, B - 30), 'rubber', bevel=3))
    S.append(box('bipod_yoke', (40, 24, 20), (0, 586, B - 30), 'gunmetal', bevel=3))
    S.append(box('carry_post', (16, 20, 30), (0, 370, B + 25), 'gunmetal', bevel=3))
    S.append(lathe('carry_handle', [(0, 0), (9, 0), (9, 120), (0, 120)], 'polymer', (0, 315, B + 44), seg=16))
    # moving: feed cover (hinged at front), ammo box + belt, charging handle, trigger
    cover = join('cover', [box('cover_body', (54, 200, 18), (0, 85, 72), 'gunmetal', bevel=5, segs=3),
                           box('cover_latch', (30, 12, 10), (0, -22, 70), 'gunmetal', bevel=3)])
    belt = []
    for i in range(7):
        belt.append(cyl(f'rnd{i}', 4.6, 55, (-30 - i * 11, 98, 52 - i * i * 1.6), 'brass', r2=3, seg=12, bevel=0.6))
        belt.append(box(f'link{i}', (8, 40, 4), (-30 - i * 11, 120, 47 - i * i * 1.6), 'steel', bevel=0.8))
    ammo = join('ammo', [box('ammo_box', (58, 120, 150), (-58, 80, -60), 'polymer_fde', bevel=10, segs=3),
                         box('box_lid', (60, 122, 10), (-58, 80, 18), 'polymer_fde', bevel=3)] + belt)
    ch = join('charging', [box('ch_rod', (8, 40, 8), (29, 150, 28), 'steel', bevel=1.5),
                           box('ch_handle', (20, 12, 22), (38, 168, 28), 'polymer', bevel=4)])
    trig = trigger('trigger', -4, 6, 1.1)
    moving = {'FeedCover': (cover, (0, 185, 80)), 'AmmoBox': (ammo, (-30, 80, 20)), 'ChargingHandle': (ch, (29, 150, 28)),
              'Trigger': (trig, (-4, 4, 4))}
    sockets = {'Optic': (0, 60, 88.6), 'Muzzle': (0, 763, B), 'Eject': (0, 60, -30), 'LeftHand': (0, 290, B - 44),
               'RightHand': (0, -40, -20), 'IronSight': (0, -20, 92), 'MagWell': (-30, 80, 20)}
    return assemble(W, S, moving, sockets)


# ============================================================== Sniper (bolt action)
def build_sniper():
    reset(); B = 42; W = 'Sniper'
    S = []
    S.append(profile('stock', [(330, 26), (330, 0), (316, -10), (80, -12), (30, -14), (-6, -20), (-22, -98), (-44, -114),
                               (-76, -110), (-84, -92), (-70, -40), (-140, -58), (-560, -112), (-572, -106), (-572, 36),
                               (-490, 46), (-300, 46), (-270, 28), (-90, 28), (-60, 26)], 42, 'polymer_fde', bevel=6, segs=3))
    S.append(profile('buttpad', [(-572, 38), (-590, 38), (-590, -110), (-572, -106)], 44, 'rubber', bevel=5))
    S.append(box('grip_panel_l', (2, 50, 60), (-21.5, -50, -62), 'grip', bevel=1, rot=(14, 0, 0)))
    S.append(box('grip_panel_r', (2, 50, 60), (21.5, -50, -62), 'grip', bevel=1, rot=(14, 0, 0)))
    S.append(lathe('receiver', [(0, 0), (16, 0), (17, 4), (17, 226), (16, 230), (0, 230)], 'gunmetal', (0, -60, B), seg=32))
    S.append(rail('scope_rail', 210, -50, B + 15))
    S.append(box('eject_port', (2, 60, 14), (16.5, 40, B + 4), 'bore', bevel=0.5))
    S.append(lathe('barrel', [(0, 0), (14, 0), (14, 60), (12.5, 90), (11, 520), (10, 590), (0, 590)], 'gunmetal', (0, 170, B), seg=28))
    brk = lathe('brake', [(5, 0), (14.5, 0), (15, 3), (15, 57), (14.5, 60), (5, 60)], 'gunmetal', (0, 760, B), seg=28)
    ports = [box(f'port{i}', (40, 8, 14), (0, 772 + i * 12, B), 'gunmetal', bevel=1.5) for i in range(3)]
    boolean(brk, join('ports', ports))
    S.append(brk)
    S.append(trigger_guard('guard', -8, 44, -12, 'gunmetal', 12, 24))
    S.append(box('mag_well', (26, 70, 8), (0, 58, -14), 'gunmetal', bevel=2))
    S.append(box('sling_stud_f', (8, 10, 10), (0, 290, -14), 'steel', bevel=2))
    S.append(box('sling_stud_r', (8, 10, 10), (0, -480, -100), 'steel', bevel=2))
    S.append(lathe('bolt_shroud', [(0, 0), (13, 0), (14, 6), (13, 30), (8, 36), (0, 36)], 'gunmetal', (0, -60, B), axis='-Y', seg=24))
    # moving
    bolt = join('bolt', [cyl('bolt_body', 9.5, 60, (0, -60, B), 'steel', seg=20),
                         box('bolt_arm', (44, 8, 8), (22, -88, B), 'steel', bevel=2, rot=(0, 20, 0)),
                         lathe('bolt_knob', [(0, 0), (6, 1), (9, 5), (10, 10), (9, 15), (6, 19), (0, 20)], 'polymer',
                               (40, -88, B - 8), axis='X', seg=20)])
    mag = join('mag', [box('mag_body', (22, 66, 50), (0, 58, -30), 'gunmetal', bevel=2),
                       box('mag_base', (25, 70, 6), (0, 58, -56), 'polymer', bevel=2),
                       cyl('mag_round', 5, 60, (0, 30, -6), 'brass', r2=3.5, seg=14)])
    trig = trigger('trigger', 14, -10)
    moving = {'Bolt': (bolt, (0, -60, B)), 'Magazine': (mag, (0, 58, -10)), 'Trigger': (trig, (14, -12, -12))}
    sockets = {'Optic': (0, 55, B + 21.6), 'Muzzle': (0, 820, B), 'Eject': (17, 40, B + 6), 'LeftHand': (0, 200, -14),
               'RightHand': (0, -45, -30), 'IronSight': (0, -40, B + 24), 'MagWell': (0, 58, -10)}
    return assemble(W, S, moving, sockets)


# ============================================================== Shotgun (pump)
def build_shotgun():
    reset(); B = 40; W = 'Shotgun'
    S = []
    S.append(profile('receiver', [(-62, 44), (-62, 4), (-50, 0), (140, 0), (140, 52), (120, 58), (-40, 58)], 30, 'gunmetal',
                     bevel=4, segs=3))
    S.append(box('eject_port', (2, 66, 22), (15, 70, 34), 'bore', bevel=0.6))
    S.append(box('load_port', (22, 70, 2), (0, 70, -0.5), 'bore', bevel=0.6))
    S.append(lathe('barrel', [(9.4, 0), (11.5, 0), (11.5, 470), (9.4, 470)], 'gunmetal', (0, 140, B), seg=28))
    S.append(lathe('bore', [(0, 0), (9.4, 0), (9.4, 469), (0, 469)], 'bore', (0, 140.5, B), seg=16))
    S.append(lathe('bead', [(0, 0), (1.8, 0.5), (2.2, 2), (1.8, 3.5), (0, 4)], 'brass', (0, 595, B + 11), axis='Z', seg=12))
    S.append(lathe('mag_tube', [(0, 0), (11, 0), (11, 420), (0, 420)], 'gunmetal', (0, 140, B - 25), seg=24))
    S.append(lathe('mag_cap', [(0, 0), (12.5, 0), (12.5, 22), (10, 26), (0, 27)], 'gunmetal', (0, 560, B - 25), seg=24))
    S.append(box('barrel_lug', (20, 30, 20), (0, 560, B - 13), 'gunmetal', bevel=3))
    S.append(profile('stock', [(-60, 44), (-60, 2), (-84, -24), (-104, -58), (-132, -74), (-420, -112), (-432, -112),
                               (-432, 30), (-412, 32), (-150, 36), (-92, 44)], 36, 'wood', bevel=6, segs=3))
    S.append(profile('recoil_pad', [(-432, 32), (-456, 32), (-456, -114), (-432, -112)], 38, 'rubber', bevel=5))
    S.append(trigger_guard('guard', -4, 62, 1, 'polymer', 12, 24))
    S.append(cyl('safety', 4, 34, (-17, -2, -4), 'steel', axis='X', seg=12, bevel=1))
    S.append(box('slide_release', (6, 14, 4), (0, 58, -1), 'steel', bevel=1))
    # moving: pump forend (+ action bars), shell for reload animation, trigger
    pump = lathe('pump', [(11.5, 0), (20, 0), (24, 6), (24, 170), (20, 176), (11.5, 176)], 'wood', (0, 230, B - 25), seg=28)
    rings = [lathe(f'groove{i}', [(23.5, 0), (24.6, 1), (24.6, 4), (23.5, 5)], 'wood', (0, 252 + i * 12, B - 25), seg=28)
             for i in range(10)]
    bars = [box(f'bar{s}', (3, 200, 6), (s * 12, 160, B - 14), 'steel', bevel=0.8) for s in (-1, 1)]
    pump = join('pump', [pump] + rings + bars)
    shell = join('shell', [lathe('hull', [(0, 0), (9.3, 0), (9.3, 50), (8.3, 54), (0, 55)], 'polymer_red', (0, 0, 0), seg=18),
                           lathe('base', [(0, 0), (10.2, 0), (10.2, 2), (9.4, 3), (9.4, 14), (0, 14)], 'brass', (0, -0.5, 0), seg=18)])
    shell.location = (0.0, 0.07, 0.02)  # parked below loading port; reposition via animation
    trig = trigger('trigger', 22, 6)
    moving = {'Pump': (pump, (0, 230, B - 25)), 'Shell': (shell, (0, 0, 0)), 'Trigger': (trig, (22, 4, 4))}
    sockets = {'Optic': (0, 40, 58), 'Muzzle': (0, 610, B), 'Eject': (16, 70, 36), 'LeftHand': (0, 318, B - 50),
               'RightHand': (0, -45, -20), 'IronSight': (0, 597, B + 15), 'LoadPort': (0, 70, -2)}
    return assemble(W, S, moving, sockets)


# ============================================================== SMG (MP5-style)
def build_smg():
    reset(); B = 38; W = 'SMG'
    S = []
    S.append(box('receiver', (30, 290, 48), (0, 85, 24), 'gunmetal', bevel=10, segs=4))
    S.append(box('receiver_rib', (31, 250, 4), (0, 90, 14), 'gunmetal', bevel=1.2))
    S.append(lathe('cock_tube', [(0, 0), (11, 0), (11, 170), (9, 176), (0, 176)], 'gunmetal', (0, 225, B + 18), seg=20))
    S.append(box('handguard', (44, 150, 46), (0, 300, B - 6), 'polymer', bevel=12, segs=4))
    S.append(lathe('barrel', [(0, 0), (8, 0), (8, 30), (10, 30), (10, 34), (8, 34), (8, 60), (0, 60)], 'gunmetal', (0, 370, B), seg=20))
    for i in range(3):
        S.append(box(f'lug{i}', (5, 10, 6), (0, 412, B), 'gunmetal', bevel=1, rot=(0, i * 120, 0)))
    S.append(lathe('front_hood', [(10, 0), (13, 0), (13, 12), (10, 12)], 'gunmetal', (0, 380, B + 40), seg=24))
    S.append(box('front_post_base', (12, 16, 30), (0, 386, B + 22), 'gunmetal', bevel=3))
    S.append(cyl('front_post', 1.4, 10, (0, 386, B + 36), 'steel', axis='Z', seg=8, bevel=0.3))
    S.append(lathe('rear_drum', [(0, 0), (12, 0), (12, 16), (0, 16)], 'gunmetal', (-8, -30, B + 32), axis='X', seg=20))
    S.append(box('rear_mount', (22, 30, 14), (0, -30, B + 14), 'gunmetal', bevel=3))
    # trigger housing + grip (polymer)
    S.append(profile('housing', [(-58, 2), (100, 2), (100, -10), (64, -26), (-10, -26), (-58, -14)], 30, 'polymer', bevel=4))
    S.append(pistol_grip('grip', -36, 'polymer', angle=16, length=100, width=31))
    S.append(trigger_guard('guard', -6, 60, -10, 'polymer', 14, 22))
    S.append(box('mag_release', (10, 6, 12), (0, 92, -6), 'steel', bevel=2))
    # retractable stock: rods + butt
    for sx in (-15, 15):
        S.append(cyl(f'rod{sx}', 5, 220, (sx, -60, 26), 'steel', axis='-Y', seg=12, bevel=1))
    S.append(profile('butt', [(-272, 66), (-284, 66), (-284, -40), (-272, -36), (-268, 0)], 44, 'rubber', bevel=5))
    S.append(box('butt_frame', (40, 14, 20), (0, -272, 26), 'steel', bevel=3))
    # moving
    mag = magazine_curved('mag', 96, 30, 190, 40, 22, 'gunmetal', top_z=-8)
    ch = join('charging', [box('ch_arm', (8, 8, 30), (-14, 300, B + 18), 'steel', bevel=2, rot=(0, -40, 0)),
                           lathe('ch_knob', [(0, 0), (5, 1), (6, 6), (5, 11), (0, 12)], 'polymer', (-30, 300, B + 5), axis='Z', seg=14)])
    sel = join('selector', [cyl('sel_hub', 6, 3, (-16, -20, -10), 'steel', axis='X', seg=16),
                            box('sel_lever', (3, 26, 6), (-17, -30, -10), 'steel', bevel=1, rot=(20, 0, 0))])
    trig = trigger('trigger', 20, -10)
    moving = {'Magazine': (mag, (112, 0, -8)), 'ChargingHandle': (ch, (-14, 300, B + 18)), 'Selector': (sel, (-16, -20, -10)),
              'Trigger': (trig, (20, -12, -12))}
    sockets = {'Optic': (0, 40, 48), 'Muzzle': (0, 430, B), 'Eject': (16, 120, 34), 'LeftHand': (0, 300, B - 30),
               'RightHand': (0, -36, -20), 'IronSight': (0, -30, B + 44), 'MagWell': (0, 112, -8)}
    return assemble(W, S, moving, sockets)


# ============================================================== Optics (separate attachments)
def _rail_clamp(name, y0, length, mat_='anodized'):
    return join(name, [box(name + '_base', (30, length, 9), (0, y0 + length / 2, 4.5), mat_, bevel=2),
                       box(name + '_jaw', (6, length, 8), (14, y0 + length / 2, 2), mat_, bevel=1.5),
                       cyl(name + '_screw', 5, 6, (17, y0 + length / 2, 4), 'steel', axis='X', seg=16, bevel=1)])


def build_reddot():
    reset(); W = 'Optic_RedDot'; C = 38
    S = [_rail_clamp('mount', -22, 44)]
    S.append(box('riser', (22, 34, 16), (0, 0, 16), 'anodized', bevel=3))
    S.append(lathe('tube', [(17, 0), (20, 0), (20.5, 4), (20.5, 56), (20, 60), (17, 60)], 'anodized', (0, -30, C), seg=32))
    S.append(lathe('hood', [(18.5, 0), (21.5, 0), (21.5, 12), (18.5, 12)], 'rubber', (0, 30, C), seg=32))
    S.append(lathe('lens_f', [(0, 0), (17.5, 0), (17.5, 1.5), (0, 1.5)], 'lens', (0, 20, C), seg=32))
    S.append(lathe('lens_r', [(0, 0), (17.5, 0), (17.5, 1.5), (0, 1.5)], 'glass', (0, -26, C), seg=32))
    S.append(cyl('turret_top', 8, 9, (0, 0, C + 18), 'anodized', axis='Z', seg=20, bevel=1.5))
    S.append(cyl('turret_side', 8, 9, (18, 0, C), 'anodized', axis='X', seg=20, bevel=1.5))
    S.append(cyl('brightness', 9, 10, (-28, 0, C), 'anodized', axis='X', seg=20, bevel=1.5))
    dot = lathe('reticle', [(0, 0), (0.6, 0), (0.6, 0.3), (0, 0.3)], 'reticle', (0, 18, C), seg=12)
    root = assemble(W, S, {'Reticle': (dot, (0, 18, C))}, {'Eye': (0, -110, C), 'Mount': (0, 0, 0)})
    return root


def build_scope4x():
    reset(); W = 'Optic_Scope4x'; C = 34
    S = [_rail_clamp('mount', -40, 80)]
    S.append(box('body', (34, 100, 30), (0, 0, C - 4), 'anodized', bevel=9, segs=3))
    S.append(box('riser', (26, 70, 10), (0, 0, 12), 'anodized', bevel=2))
    S.append(lathe('objective', [(14, 0), (20, 0), (21, 3), (21, 30), (14, 30)], 'anodized', (0, 40, C), seg=32))
    S.append(lathe('eyepiece', [(12, 0), (18, 0), (18, 26), (12, 26)], 'anodized', (0, -66, C), seg=32))
    S.append(lathe('eye_rubber', [(13, 0), (19, 0), (19, 8), (13, 8)], 'rubber', (0, -72, C), seg=32))
    S.append(lathe('lens_f', [(0, 0), (19.5, 0), (19.5, 1.5), (0, 1.5)], 'lens', (0, 66, C), seg=32))
    S.append(lathe('lens_r', [(0, 0), (12.5, 0), (12.5, 1.5), (0, 1.5)], 'glass', (0, -70, C), seg=32))
    S.append(cyl('turret_top', 9, 8, (0, 0, C + 11), 'anodized', axis='Z', seg=20, bevel=1.5))
    S.append(cyl('turret_side', 9, 8, (17, 0, C - 4), 'anodized', axis='X', seg=20, bevel=1.5))
    S.append(box('fiber', (8, 70, 6), (0, 0, C + 12), 'polymer_red', bevel=2))
    dot = lathe('reticle', [(0, 0), (0.5, 0), (0.5, 0.3), (0, 0.3)], 'reticle', (0, -60, C), seg=12)
    return assemble(W, S, {'Reticle': (dot, (0, -60, C))}, {'Eye': (0, -140, C), 'Mount': (0, 0, 0)})


def build_scope_sniper():
    reset(); W = 'Optic_SniperScope'; C = 42
    S = []
    for y in (-55, 55):
        S.append(_rail_clamp(f'ring_base{y}', y - 12, 24))
        S.append(box(f'ring_post{y}', (18, 22, 14), (0, y, 15), 'anodized', bevel=3))
        S.append(lathe(f'ring{y}', [(15, 0), (20, 0), (20, 20), (15, 20)], 'anodized', (0, y - 10, C), seg=28))
    S.append(lathe('tube', [(0, 0), (22, 0), (22, 8), (30, 50), (30, 70), (28, 72), (15, 90), (15, 250), (20, 270),
                            (21, 330), (21, 345), (0, 345)], 'anodized', (0, 200, C), axis='-Y', seg=36))
    S.append(lathe('sunshade', [(27, 0), (30.5, 0), (30.5, 40), (27, 40)], 'anodized', (0, 200, C), seg=36))
    S.append(lathe('eye_rubber', [(17, 0), (22, 0), (22, 10), (17, 10)], 'rubber', (0, -155, C), seg=32))
    S.append(lathe('lens_f', [(0, 0), (27, 0), (27, 1.5), (0, 1.5)], 'lens', (0, 196, C), seg=36))
    S.append(lathe('lens_r', [(0, 0), (18, 0), (18, 1.5), (0, 1.5)], 'glass', (0, -150, C), seg=32))
    S.append(lathe('turret_elev', [(0, 0), (14, 0), (14, 4), (13, 5), (13, 20), (14, 21), (14, 24), (0, 24)], 'anodized',
                   (0, 0, C + 14), axis='Z', seg=24))
    S.append(lathe('turret_wind', [(0, 0), (13, 0), (13, 20), (0, 20)], 'anodized', (14, 0, C), axis='X', seg=24))
    S.append(lathe('turret_par', [(0, 0), (12, 0), (12, 18), (0, 18)], 'anodized', (-32, 0, C), axis='X', seg=24))
    S.append(lathe('mag_ring', [(21, 0), (23, 0), (23, 26), (21, 26)], 'grip', (0, -110, C), seg=32))
    cross = join('reticle', [box('rh', (40, 0.3, 0.4), (0, -120, C), 'reticle', bevel=0),
                             box('rv', (0.4, 0.3, 40), (0, -120, C), 'reticle', bevel=0)])
    return assemble(W, S, {'Reticle': (cross, (0, -120, C))}, {'Eye': (0, -240, C), 'Mount': (0, 0, 0)})


BUILDERS = {'m4': build_m4, 'ak': build_ak, 'lmg': build_lmg, 'sniper': build_sniper, 'shotgun': build_shotgun,
            'smg': build_smg, 'reddot': build_reddot, 'scope4x': build_scope4x, 'sniperscope': build_scope_sniper}

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')] or list(BUILDERS)
    stats = {}
    for k in args:
        root = BUILDERS[k]()
        name = root.name
        stats[name] = lib.tri_count(root)
        export(root, f'{OUT}/{name}.glb')
        if '--preview' in sys.argv:
            os.makedirs(PREV, exist_ok=True)
            preview(root, f'{PREV}/{name}.png')
        if '--mobile' in sys.argv:
            export(root, f'{OUTM}/{name}.glb', tex_size=1024)
        print(name, 'tris', stats[name])
    print(json.dumps(stats))
