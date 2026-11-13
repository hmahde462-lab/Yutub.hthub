"""Music + SFX for the stickman story. Plucked-string (Karplus-Strong) melody in maqam Hijaz
over a soft drone, mixed low so a voice-over can sit on top. Cartoon SFX from the event log."""
import json, sys, wave
import numpy as np
SR = 44100; cid = sys.argv[1]; voice_ready = len(sys.argv) > 2
d = json.load(open(f'out/{cid}_events.json')); dur = d['duration'] + 0.4; N = int(dur * SR)
rng = np.random.default_rng(11); out = np.zeros(N, np.float32)
def add(sig, at, gain=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if 0 <= i < N: out[i:j] += (np.asarray(sig[:j - i]) * gain).astype(np.float32)
def pluck(f, length=1.2, bright=0.5):
    n = int(length * SR); p = int(SR / f); buf = rng.uniform(-1, 1, p); y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * (0.994 - 0.004 * (1 - bright))
    return y * np.exp(-np.arange(n) / SR * 1.6)
def noise_band(n, lo, hi):
    x = rng.normal(0, 1, n); X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR); X[(fr < lo) | (fr > hi)] = 0; x = np.fft.irfft(X, n); return x / (np.abs(x).max() + 1e-9)
# --- music: Hijaz on D: D Eb F# G A Bb C D
base = 146.83; steps = [0, 1, 4, 5, 7, 8, 10, 12]
hz = lambda k: base * 2 ** ((steps[k % 8] + 12 * (k // 8)) / 12)
tempo = 0.30  # seconds per eighth note
phrase = [7, 6, 5, 4, 5, 4, 2, 1, 2, 4, 5, 7, 8, 7, 5, 4]
cache = {}
t = 0.0; idx = 0
while t < dur - 1:
    k = phrase[idx % len(phrase)] + 8; f = hz(k)
    if k not in cache: cache[k] = pluck(f, 1.0)
    if idx % 16 not in (7, 15): add(cache[k], t, 0.16 if idx % 2 == 0 else 0.10)
    if idx % 4 == 0:  # darbuka-ish: doum on beats, tek on offbeats
        n = int(.18 * SR); tt = np.arange(n) / SR; add(np.sin(2 * np.pi * (90 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18), t, .28)
    if idx % 4 == 2: add(noise_band(int(.06 * SR), 2000, 7000) * np.exp(-np.arange(int(.06 * SR)) / SR * 60), t, .08)
    t += tempo; idx += 1
tt = np.arange(N) / SR
drone = (np.sin(2 * np.pi * base / 2 * tt) + .5 * np.sin(2 * np.pi * base * 1.5 / 2 * tt)) * 0.05
out += (drone * np.minimum(1, tt / 2) * np.minimum(1, (dur - tt) / 1.5)).astype(np.float32)
music_gain = 0.45 if voice_ready else 1.0
out *= music_gain
# --- SFX
def thud(): n = int(.35 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * (70 + 80 * np.exp(-x * 25)) * x) * np.exp(-x * 9) + noise_band(n, 200, 1500) * np.exp(-x * 30) * .4
def clink(f=2400): n = int(.5 * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) + .6 * np.sin(2 * np.pi * f * 2.7 * x)) * np.exp(-x * 9)
def boing(): n = int(.6 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(220 + 160 * np.sin(x * 40) * np.exp(-x * 4)) / SR) * np.exp(-x * 4)
def whoosh(L=.8): n = int(L * SR); x = np.arange(n) / SR; return noise_band(n, 400, 3000) * np.sin(np.pi * x / L) ** 2
def creak(): n = int(.9 * SR); x = np.arange(n) / SR; f = 180 + 120 * np.sin(x * 9); return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-x * 2) * .5
def wind(L): n = int(L * SR); x = np.arange(n) / SR; return noise_band(n, 150, 900) * (.6 + .4 * np.sin(x * 1.3)) * np.minimum(1, x / 1) * np.minimum(1, (L - x) / 1)
def chuckle(L=2.5):  # cartoon crowd chuckle: pulsed formant noise
    n = int(L * SR); x = np.arange(n) / SR; nb = noise_band(n, 500, 1800); pulses = np.clip(np.sin(2 * np.pi * 6.5 * x), 0, 1) ** 2
    return nb * pulses * np.minimum(1, x / .2) * np.minimum(1, (L - x) / .6)
for e in d['events']:
    k, t0 = e['kind'], e['t']
    if k == 'wind': add(wind(9.5), t0, .18)
    elif k == 'thud': add(thud(), t0, .5); add(clink(2600), t0 + .05, .12)
    elif k in ('laugh', 'laugh2'): add(chuckle(), t0, .22)
    elif k == 'boing': add(boing(), t0, .25)
    elif k == 'brick': add(thud(), t0, .22)
    elif k == 'heat': add(noise_band(int(9 * SR), 60, 300) * .5, t0, .12)
    elif k == 'clang': add(clink(900), t0, .3)
    elif k == 'door': add(creak(), t0, .18)
    elif k == 'mist': add(whoosh(1.6), t0, .3); [add(clink(f), t0 + .4 + .12 * i, .1) for i, f in enumerate([2093, 2637, 3136])]
    elif k == 'coins': [add(clink(2800 + 300 * (i % 3)), t0 + .17 * i, .12) for i in range(14)]
    elif k == 'coin1': add(clink(3000), t0, .2)
    elif k == 'whoosh': add(whoosh(), t0, .15)
    elif k == 'ding': add(clink(1760), t0, .25); add(clink(2637), t0 + .1, .18)
    elif k == 'cut': add(whoosh(.35), t0 - .1, .12)
out = np.tanh(out * 1.3) / np.tanh(1.3); out *= 0.89 / max(1e-6, np.abs(out).max())
w = wave.open(f'audio/{cid}_bed.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('bed ok', round(dur, 1))
