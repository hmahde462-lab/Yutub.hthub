"""SFX for axe / grow episodes: wood-steel chops, pentatonic plinks, rising grow notes, finale."""
import json, sys, wave
import numpy as np
SR = 44100; ep = sys.argv[1]
d = json.load(open(f'out/{ep}_events.json')); N = int((d['duration'] + .6) * SR); out = np.zeros(N, np.float32); rng = np.random.default_rng(4)
def add(s, t, gain):
    i = int(t * SR); j = min(N, i + len(s))
    if 0 <= i < N: out[i:j] += (s[:j - i] * gain).astype(np.float32)
def env(n, dec): x = np.arange(n) / SR; return np.minimum(1, x / .002) * np.exp(-x / dec)
def tone(f, L=.35, br=.3): n = int(L * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) + br * np.sin(4 * np.pi * f * x)) * env(n, L / 4.5)
def chop(size):  # thunk + metallic ring
    n = int(.4 * SR); x = np.arange(n) / SR
    thunk = np.sin(2 * np.pi * (120 + 160 * np.exp(-x * 40)) * x) * np.exp(-x * 22)
    ring = (np.sin(2 * np.pi * (1800 + 900 * size) * x) + .5 * np.sin(2 * np.pi * (2700 + 1300 * size) * x)) * np.exp(-x * 14) * .35
    noise = rng.normal(0, 1, n) * np.exp(-x * 60) * .3
    return thunk + ring + noise
PENTA = [0, 2, 4, 7, 9]; f5 = lambda k: 261.63 * 2 ** ((k // 5) + PENTA[k % 5] / 12)
slots = {}
for e in d['events']:
    k, t = e['kind'], e['t']; key = (int(t / .03), k)
    if slots.get(key, 0) >= (2 if k == 'wall' else 3): continue
    slots[key] = slots.get(key, 0) + 1
    if k == 'split': add(chop(e['v']), t, .5)
    elif k == 'wall': step = int(((e['a'] + np.pi) / (2 * np.pi)) * 10) % 10 + 5; add(tone(f5(step)), t, .08 + .12 * e['v'])
    elif k == 'tink': add(tone(2600, .15, .1), t, .08)
    elif k == 'grow': add(tone(f5(5 + int(e['v'] * 12) + (0 if e['team'] == 0 else 2)), .4, .4), t, .2)
    elif k in ('boom', 'pop'):
        n = int(1.4 * SR); x = np.arange(n) / SR; add(np.sin(2 * np.pi * (55 + 45 * np.exp(-x * 6)) * x) * np.exp(-x * 2.4) + rng.normal(0, 1, n) * np.exp(-x * 6) * .3, t, .8)
    elif k == 'milestone':
        for i, st in enumerate([10, 12, 14, 17]): add(tone(f5(st), .9, .4), t + .09 * i, .3)
    elif k == 'win':
        for i, st in enumerate([10, 12, 14, 15]): add(tone(f5(st), 1.0, .4), t + .14 * i, .25)
out = np.tanh(out * 1.3) / np.tanh(1.3); out *= .89 / max(1e-6, np.abs(out).max())
w = wave.open(f'audio/{ep}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print(ep, 'audio ok')
