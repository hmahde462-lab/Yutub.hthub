"""Fight soundtrack: driving beat + slashes/thuds per weapon, pickup chimes, heal sparkle, bomb, KO, win fanfare."""
import json, sys, wave
import numpy as np
SR = 44100; ep = sys.argv[1]
d = json.load(open(f'out/{ep}_events.json')); dur = d['duration'] + .6; N = int(dur * SR); out = np.zeros(N, np.float32); rng = np.random.default_rng(8)
def add(s, t, gain):
    i = int(t * SR); j = min(N, i + len(s))
    if 0 <= i < N: out[i:j] += (np.asarray(s[:j - i]) * gain).astype(np.float32)
def band(n, lo, hi):
    x = rng.normal(0, 1, n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; x = np.fft.irfft(X, n); return x / (np.abs(x).max() + 1e-9)
def env(n, a, dcy): x = np.arange(n) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x * dcy)
def tone(f, L, dcy=6, br=.3): n = int(L * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) + br * np.sin(4 * np.pi * f * x)) * env(n, .003, dcy)
fin = d['info'].get('finaleT') or dur
# beat (128 bpm) until finale
beat = 60 / 128; kick_n = int(.25 * SR); kx = np.arange(kick_n) / SR; KICK = np.sin(2 * np.pi * (50 + 90 * np.exp(-kx * 35)) * kx) * np.exp(-kx * 12)
HAT = band(int(.05 * SR), 6000, 12000) * env(int(.05 * SR), .001, 80); BASS = [55, 55, 65.4, 49]
k = 0; t = .2
while t < fin:
    add(KICK, t, .45 if k % 2 == 0 else .3); add(HAT, t + beat / 2, .12)
    if k % 2 == 0: add(tone(BASS[(k // 4) % 4], beat * 1.8, 3, .5), t, .2)
    t += beat; k += 1
SL = band(int(.18 * SR), 1500, 9000) * env(int(.18 * SR), .002, 22)
def thud(): n = int(.35 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * (60 + 120 * np.exp(-x * 30)) * x) * np.exp(-x * 10) + band(n, 100, 1500) * np.exp(-x * 30) * .5
TH = thud()
slots = {}
for e in d['events']:
    kd, t = e['kind'], e['t']; key = (int(t / .04), kd)
    if slots.get(key, 0) >= 2: continue
    slots[key] = slots.get(key, 0) + 1
    if kd == 'hit':
        w = e.get('w')
        if w in ('axe', 'hammer'): add(TH, t, .7); add(SL, t, .3)
        elif w == 'bump': add(TH, t, .25)
        elif w == 'bomb': pass
        else: add(SL, t, .55); add(tone(2400 + 300 * (e['v'] % 5), .12, 25), t, .12)
    elif kd == 'pick': [add(tone(f, .3, 9), t + .06 * i, .18) for i, f in enumerate([880, 1175, 1568])]
    elif kd == 'heal': [add(tone(f, .5, 6), t + .05 * i, .14) for i, f in enumerate([1046, 1318, 1568, 2093])]
    elif kd == 'block': add(tone(1800, .4, 8, .6), t, .25)
    elif kd == 'boom': n = int(1.3 * SR); x = np.arange(n) / SR; add(np.sin(2 * np.pi * (45 + 60 * np.exp(-x * 8)) * x) * np.exp(-x * 2.5) + band(n, 60, 3000) * np.exp(-x * 5) * .6, t, .9)
    elif kd == 'ko': add(TH, t, .9); [add(tone(f, .35, 5), t + .1 * i, .2) for i, f in enumerate([660, 520, 400, 300])]
    elif kd == 'bump': add(TH, t, .12 * e.get('v', .5))
    elif kd == 'win': [add(tone(f, 1.2, 2.2, .5), t + .15 * i, .28) for i, f in enumerate([523, 659, 784, 1046])]
out = np.tanh(out * 1.2) / np.tanh(1.2); out *= .89 / max(1e-6, np.abs(out).max())
w = wave.open(f'audio/{ep}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print(ep, 'audio ok')
