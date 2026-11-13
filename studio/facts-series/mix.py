# python3 mix.py <segdir> <out.wav>: narration segments at their timeline slots + soft music bed + whooshes/pops.
import sys, json, os, subprocess, wave, numpy as np
SR = 44100; d = sys.argv[1]; tl = json.load(open(os.path.join(d, 'timeline.json'))); N = int((tl['total'] + .3) * SR)
out = np.zeros(N, np.float32); rng = np.random.default_rng(3)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
def add(s, t, gn):
    i = int(t * SR); j = min(N, i + len(s))
    if 0 <= i < N: out[i:j] += s[:j - i] * gn
def env(n, a, k): x = np.arange(n) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x * k)
def tone(f, L, k=6): n = int(L * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * f * x) * env(n, .004, k)
def band(n, lo, hi):
    x = rng.normal(0, 1, n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; x = np.fft.irfft(X, n); return x / (np.abs(x).max() + 1e-9)
# music bed: gentle plucked arpeggio over a pad, 100 bpm, ducked under the voice
beat = 60 / 100; prog = [[220, 261.6, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6]]
bed = np.zeros(N, np.float32); t = 0; k = 0
while t < tl['total']:
    ch = prog[(k // 8) % 4]; f = ch[k % 3] * (2 if k % 4 == 3 else 1); s = tone(f, beat * 1.5, 5) * .5; s2 = tone(f * 2, beat, 9) * .15; s[:len(s2)] += s2
    i = int(t * SR); j = min(N, i + len(s)); bed[i:j] += s[:j - i]
    if k % 8 == 0:
        L = beat * 8; n = int(L * SR); x = np.arange(n) / SR; pad = sum(np.sin(2 * np.pi * q / 2 * x) for q in ch) * np.minimum(1, x / .8) * np.minimum(1, (L - x) / .8) * .18
        j = min(N, i + n); bed[i:j] += pad[:j - i]
    t += beat / 2; k += 1
voice = np.zeros(N, np.float32)
for i, (a, b) in enumerate(tl['segs']):
    s = load(os.path.join(d, f'seg{i}.mp3')); s = s / (np.abs(s).max() + 1e-9) * .9; j = min(N, int(a * SR) + len(s)); voice[int(a * SR):j] += s[:j - int(a * SR)]
    w = band(int(.35 * SR), 800, 6000) * np.sin(np.linspace(0, np.pi, int(.35 * SR))) ; add(w, a - .3, .12); add(tone(1318, .25, 14), a - .02, .08)
m = (np.abs(voice) > .02).astype(np.float32); K = int(.25 * SR); c = np.concatenate([[0], np.cumsum(m)]); idx = np.arange(N); lo = np.clip(idx - K // 2, 0, N); hi = np.clip(idx + K // 2, 0, N); duck = (c[hi] - c[lo]) / K
out += voice + bed * (.16 - .1 * np.clip(duck * 3, 0, 1))
out = np.tanh(out * 1.1) / np.tanh(1.1); out *= .92 / max(1e-6, np.abs(out).max())
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(tl['total'], 1))
