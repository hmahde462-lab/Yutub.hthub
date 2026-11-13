"""Soundtrack for the colour battle: ball 'kicks' on hits, a pitched pop per conversion
(each team has its own note), a referee whistle on each elimination, crowd roar at the end."""
import json, sys, wave
import numpy as np
SR = 44100; ep = sys.argv[1]
d = json.load(open(f'out/{ep}_events.json')); N = int((d['duration'] + 0.6) * SR)
out = np.zeros(N, np.float32); rng = np.random.default_rng(5)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: out[i:j] += sig[:j - i] * g
def env(n, a=0.002, dec=0.05): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / dec)
def kick():  # leather thump: low sine sweep + short noise click
    n = int(0.12 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (150 * np.exp(-t * 18) + 70) * t) * env(n, .001, .035)
    click = rng.normal(0, 1, n) * env(n, .0005, .006)
    return (body * 0.9 + click * 0.25).astype(np.float32)
KICKS = [kick() for _ in range(6)]
NOTES = [523.25, 659.25, 783.99, 880.0]  # team notes C5 E5 G5 A5
def pop(f):
    n = int(0.28 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)
    return (s * env(n, .002, .07)).astype(np.float32)
POPS = [pop(f) for f in NOTES]
def whistle(dur=0.55):
    n = int(dur * SR); t = np.arange(n) / SR
    trill = 1 + 0.5 * np.sign(np.sin(2 * np.pi * 28 * t))
    s = np.sin(2 * np.pi * 2900 * t) * 0.6 + np.sin(2 * np.pi * 3050 * t) * 0.4
    e = np.minimum(1, t / .02) * np.minimum(1, (dur - t) / .05)
    return (s * trill * e * 0.5).astype(np.float32)
def crowd(dur=3.5):
    n = int(dur * SR); x = rng.normal(0, 1, n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X *= np.exp(-((f - 900) / 700) ** 2); x = np.fft.irfft(X, n)
    t = np.arange(n) / SR; e = np.minimum(1, t / .5) * np.minimum(1, (dur - t) / 1.2)
    x = x / np.abs(x).max(); return (x * e).astype(np.float32)
slots = {}
for k, e in enumerate(d['events']):
    kind, t = e['kind'], e['t']
    key = (int(t / 0.03), kind); lim = {'hit': 3, 'wall': 2, 'convert': 2}.get(kind, 9)
    if slots.get(key, 0) >= lim: continue
    slots[key] = slots.get(key, 0) + 1
    if kind in ('hit', 'wall'): add(KICKS[k % 6], t, 0.10 + 0.25 * e['v'])
    elif kind == 'convert': add(POPS[e['team'] % len(POPS) % 4], t, 0.22)
    elif kind == 'elim': add(whistle(), t, 0.55)
    elif kind == 'win':
        add(whistle(0.35), t, .5); add(whistle(0.35), t + .45, .5); add(whistle(0.9), t + .9, .5)
        add(crowd(), t + .2, 0.35)
        for i, f in enumerate([523.25, 659.25, 783.99, 1046.5]): add(pop(f), t + 0.15 * i, 0.25)
out = np.tanh(out * 1.3) / np.tanh(1.3); out *= 0.89 / max(1e-6, np.abs(out).max())
w = wave.open(f'audio/{ep}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('audio ok', round(N / SR, 2))
