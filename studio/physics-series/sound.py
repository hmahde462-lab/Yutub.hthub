"""Synthesize the soundtrack from simulation events: pentatonic plinks on bounces,
bright chimes on escapes, a boom on the finale. Pure numpy, no samples, no credits."""
import json, sys, wave
import numpy as np
SR = 44100
ep = sys.argv[1]
d = json.load(open(f'out/{ep}_events.json'))
N = int((d['duration'] + 0.5) * SR)
out = np.zeros(N, np.float32)
PENTA = [0, 2, 4, 7, 9]
def freq(step, base=261.63):  # C4 major pentatonic, step can exceed 5
    o, k = divmod(step, 5); return base * 2 ** (o + PENTA[k] / 12)
def tone(f, dur, amp, bright=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.minimum(1, t / 0.003) * np.exp(-t / (dur / 4.5))
    w = np.sin(2 * np.pi * f * t) + bright * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3.01 * f * t)
    return (w * env * amp).astype(np.float32)
def add(sig, t):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: out[i:j] += sig[:j - i]
budget = {}  # thin out dense moments: max 4 sounds per 25 ms
cache = {}
for e in d['events']:
    slot = int(e['t'] / 0.025); k = (slot, e['kind'] == 'escape')
    if budget.get(k, 0) >= (3 if e['kind'] == 'escape' else 4): continue
    budget[k] = budget.get(k, 0) + 1
    if e['kind'] in ('ring', 'post'):
        step = int(((e['a'] + np.pi) / (2 * np.pi)) * 10) % 10 + 5
        key = ('r', step)
        if key not in cache: cache[key] = tone(freq(step), 0.32, 1.0, 0.25)
        add(cache[key] * (0.10 + 0.20 * e['v']), e['t'])
    elif e['kind'] == 'escape':
        step = 10 + int(((e['a'] + np.pi) / (2 * np.pi)) * 5) % 5
        key = ('e', step)
        if key not in cache: cache[key] = tone(freq(step), 0.5, 1.0, 0.5)
        add(cache[key] * 0.22, e['t'])
    elif e['kind'] == 'boom':
        n = int(1.6 * SR); t = np.arange(n) / SR
        boom = (np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 6)) * t) * np.exp(-t * 2.2)).astype(np.float32)
        noise = np.random.default_rng(1).normal(0, 1, n).astype(np.float32) * np.exp(-t * 5).astype(np.float32)
        add(boom * 0.9 + noise * 0.25, e['t'])
        for k2, st in enumerate([10, 12, 14, 15]):
            add(tone(freq(st), 1.2, 0.18, 0.4), e['t'] + 0.12 * k2)
# soft limiter + normalize to -1 dBFS peak
out = np.tanh(out * 1.4) / np.tanh(1.4)
out *= 0.89 / max(1e-6, np.abs(out).max())
w = wave.open(f'audio/{ep}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print('audio', round(N / SR, 2), 's, events', len(d['events']))
