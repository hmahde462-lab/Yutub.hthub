# Add a real-SFX layer (studio/sfx/<slug>/map.json: {scene: [[name, offset_s, dB_vs_voice], ...]}) to a patched build.py.
import sys
for fn in sys.argv[1:]:
    p = open(fn).read()
    if 'SFXDIR' in p: print('already', fn); continue
    new = '''SFXDIR = os.path.join(D, '..', '..', 'sfx', os.path.basename(D)); sfxb = np.zeros(N, np.float32)
if os.path.exists(os.path.join(SFXDIR, 'map.json')) and not os.environ.get('NOSFX'):
    for k, lst in json.load(open(os.path.join(SFXDIR, 'map.json'))).items():
        i = int(k)
        if i >= len(times): continue
        st, d = times[i]
        for name, off, db in lst:
            sig = load(os.path.join(SFXDIR, name + '.mp3'))
            L = max(1, min(len(sig), int((d - off + 0.3) * SR))); sig = sig[:L].copy()
            fi, fo = min(L // 3, int(0.25 * SR)), min(L // 2, int(0.8 * SR))
            sig[:fi] *= np.linspace(0, 1, fi); sig[L - fo:] *= np.linspace(1, 0, fo)
            r = np.sqrt(np.mean(sig[np.abs(sig) > 1e-4] ** 2)) if np.any(np.abs(sig) > 1e-4) else 1.0
            put(sfxb, sig / r * vr * 10 ** (db / 20), st + off)
'''
    p = p.replace("env = mavg(np.abs(voc), int(0.25 * SR))", new + "env = mavg(np.abs(voc), int(0.25 * SR))")
    p = p.replace("mix = mix * 0.6 + voc + amb * duck", "mix = mix * 0.5 + voc + amb * duck + sfxb * (1 - 0.4 * np.clip(env / (vr * 0.5), 0, 1))")
    p = p.replace("os.environ.get('AMB_DB', '-27')", "os.environ.get('AMB_DB', '-32')")
    open(fn, 'w').write(p); print('sfx patched', fn, p.count('sfxb'))
