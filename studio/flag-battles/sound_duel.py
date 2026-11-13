"""Tournament soundtrack: driving beat bed, weapon hits, pickups, KOs, round stingers, VS impacts, champion fanfare + crowd."""
import json, wave, numpy as np
SR = 44100; import sys; d = json.load(open(sys.argv[1])); dur = d['total'] + .5; N = int(dur * SR)
out = np.zeros(N, np.float32); rng = np.random.default_rng(9)
def add(s, t, g):
    i = int(t * SR); j = min(N, i + len(s))
    if 0 <= i < N: out[i:j] += (np.asarray(s[:j - i]) * g).astype(np.float32)
def band(n, lo, hi):
    x = rng.normal(0, 1, n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; x = np.fft.irfft(X, n); return x / (np.abs(x).max() + 1e-9)
def env(n, a, k): x = np.arange(n) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x * k)
def tone(f, L, k=6, br=.3): n = int(L * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) + br * np.sin(4 * np.pi * f * x)) * env(n, .003, k)
beat = 60 / 124; kn = int(.25 * SR); kx = np.arange(kn) / SR; KICK = np.sin(2 * np.pi * (50 + 90 * np.exp(-kx * 35)) * kx) * np.exp(-kx * 12)
HAT = band(int(.05 * SR), 6000, 12000) * env(int(.05 * SR), .001, 80); BASS = [55, 55, 65.4, 49, 58.3, 58.3, 65.4, 73.4]
t = .3; k = 0
while t < dur - 3.6:
    add(KICK, t, .32 if k % 2 == 0 else .22); add(HAT, t + beat / 2, .08)
    if k % 2 == 0: add(tone(BASS[(k // 4) % 8], beat * 1.8, 3, .5), t, .14)
    t += beat; k += 1
SL = band(int(.18 * SR), 1500, 9000) * env(int(.18 * SR), .002, 22)
def thud(): n = int(.35 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * (60 + 120 * np.exp(-x * 30)) * x) * np.exp(-x * 10) + band(n, 100, 1500) * np.exp(-x * 30) * .5
TH = thud()
def crowd(L): n = int(L * SR); x = np.arange(n) / SR; c = band(n, 300, 3000) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * x)); return c * np.minimum(1, x / .5) * np.minimum(1, (L - x) / 1.5)
slots = {}
for e in d['events']:
    kd, t = e['kind'], e['t']; key = (int(t / .04), kd)
    if slots.get(key, 0) >= 2: continue
    slots[key] = slots.get(key, 0) + 1
    if kd == 'hit':
        w = e.get('w')
        if w in ('axe', 'hammer'): add(TH, t, .6); add(SL, t, .25)
        elif w == 'bump': add(TH, t, .15)
        elif w != 'bomb': add(SL, t, .45); add(tone(2400 + 300 * (e['v'] % 5), .12, 25), t, .1)
    elif kd == 'pick': [add(tone(f, .3, 9), t + .06 * i, .14) for i, f in enumerate([880, 1175, 1568])]
    elif kd == 'heal': [add(tone(f, .5, 6), t + .05 * i, .12) for i, f in enumerate([1046, 1318, 1568, 2093])]
    elif kd == 'boom': n = int(1.3 * SR); x = np.arange(n) / SR; add(np.sin(2 * np.pi * (45 + 60 * np.exp(-x * 8)) * x) * np.exp(-x * 2.5) + band(n, 60, 3000) * np.exp(-x * 5) * .6, t, .8)
    elif kd == 'ko': add(TH, t, .8); [add(tone(f, .35, 5), t + .1 * i, .18) for i, f in enumerate([660, 520, 400, 300])]
    elif kd == 'win': [add(tone(f, 1.0, 2.5, .5), t + .14 * i, .24) for i, f in enumerate([523, 659, 784, 1046])]; add(crowd(2.4), t, .25)
    elif kd == 'round': n = int(1.6 * SR); x = np.arange(n) / SR; add(band(n, 200, 4000) * np.minimum(1, x / 1.2) * np.exp(-np.maximum(0, x - 1.2) * 8), t - 1.0, .35); add(TH, t + .3, .9)
    elif kd == 'vs': add(TH, t + .15, .7); add(tone(220, .8, 3, .6), t + .15, .2)
    elif kd == 'champion': [add(tone(f, 2.0, 1.2, .5), t + .2 * i, .28) for i, f in enumerate([523, 659, 784, 1046, 1318])]; add(crowd(3.4), t, .4)
out = np.tanh(out * 1.2) / np.tanh(1.2); out *= .89 / max(1e-6, np.abs(out).max())
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('tour audio ok', round(dur, 1))
