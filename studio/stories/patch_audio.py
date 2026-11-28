# Patch a story build.py: quiet, ducked, softened ambience under a dominant voice; AUDIO_ONLY remux mode.
import sys, re
for fn in sys.argv[1:]:
    p = open(fn).read()
    if 'AMB_DB' in p: print('already', fn); continue
    p = p.replace("for i, x in enumerate(s):\n    st, d = times[i]; n = int(round(d * FPS)); out = f'clips/{i:02d}.mp4'",
                  "for i, x in enumerate([] if os.environ.get('AUDIO_ONLY') else s):\n    st, d = times[i]; n = int(round(d * FPS)); out = f'clips/{i:02d}.mp4'")
    p = p.replace("subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'clips/list.txt', '-c', 'copy', 'video_noaudio.mp4'], check=True)",
                  "if not os.environ.get('AUDIO_ONLY'): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'clips/list.txt', '-c', 'copy', 'video_noaudio.mp4'], check=True)")
    p = re.sub(r"put\(mix, load\(f'lines/line\{i:02d\}\.wav'\) \* 1\.0, st \+ 0\.35\)", "put(voc, load(f'lines/line{i:02d}.wav') * 1.0, st + 0.35)", p)
    p = p.replace("mix = np.zeros(N, np.float32); amb = np.zeros(N, np.float32)", "mix = np.zeros(N, np.float32); amb = np.zeros(N, np.float32); voc = np.zeros(N, np.float32)")
    new = '''AMB_DB = float(os.environ.get('AMB_DB', '-32'))   # ambience level relative to the voice (dB)
amb = lfilter([0.35], [1, -0.65], amb).astype(np.float32)          # soften hiss (gentle lowpass)
def mavg(x, k):
    c = np.cumsum(np.concatenate([[0.0], x.astype(np.float64)])); y = (c[k:] - c[:-k]) / k
    pad = len(x) - len(y); return np.concatenate([np.full(pad // 2, y[0]), y, np.full(pad - pad // 2, y[-1])]).astype(np.float32)
fade = mavg((np.abs(amb) > 0).astype(np.float32), int(0.4 * SR)); amb *= np.clip(fade, 0, 1)
vr = np.sqrt(np.mean(voc[np.abs(voc) > 1e-4] ** 2)) if np.any(np.abs(voc) > 1e-4) else 0.1
ar = np.sqrt(np.mean(amb[np.abs(amb) > 1e-6] ** 2)) if np.any(np.abs(amb) > 1e-6) else 1.0
amb *= vr * 10 ** (AMB_DB / 20) / ar
env = mavg(np.abs(voc), int(0.25 * SR))
duck = 1 - 0.55 * np.clip(env / (vr * 0.5), 0, 1)                  # dip ambience further while speaking
mix = mix * 0.6 + voc + amb * duck'''
    p = p.replace("mix += amb", new, 1)
    p = p.replace("'-i', 'video_noaudio.mp4', '-i', 'audio.wav', '-c:v', 'copy',", "'-i', os.environ.get('VIDEO_IN', 'video_noaudio.mp4'), '-i', 'audio.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',")
    open(fn, 'w').write(p); print('patched', fn, p.count('AUDIO_ONLY'), p.count('voc'))
