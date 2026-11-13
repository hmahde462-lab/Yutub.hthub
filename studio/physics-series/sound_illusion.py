"""Calm ambient bed for illusions (nothing sudden while the viewer stares), a soft chime
on the switch, a gentle whoosh + sparkle on the reveal, a pop on the call to action."""
import json, sys, wave
import numpy as np
SR = 44100; ep = sys.argv[1]
d = json.load(open(f'out/{ep}_events.json')); dur = d['duration'] + 0.5; N = int(dur * SR)
t = np.arange(N) / SR; rng = np.random.default_rng(3)
chord = [130.81, 196.0, 261.63, 329.63, 392.0]  # C major add9 pad
pad = sum(np.sin(2 * np.pi * f * t + i) * (0.5 + 0.5 * np.sin(2 * np.pi * (0.07 + 0.03 * i) * t)) for i, f in enumerate(chord))
pad *= np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 2.0) * 0.12
out = pad.astype(np.float32)
def add(sig, at, gain):
    i = int(at * SR); j = min(N, i + len(sig))
    if i < N: out[i:j] += (sig[:j - i] * gain).astype(np.float32)
def bell(f, length=2.0):
    n = int(length * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + .4 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt * 3)
    return s * np.minimum(1, tt / .004) * np.exp(-tt * 2.2)
def whoosh(length=0.9):
    n = int(length * SR); x = rng.normal(0, 1, n); X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR)
    X *= np.exp(-((fr - 1500) / 1200) ** 2); x = np.fft.irfft(X, n); x /= np.abs(x).max(); tt = np.arange(n) / SR
    return x * np.sin(np.pi * tt / length) ** 2
for e in d['events']:
    if e['kind'] == 'switch': add(bell(784.0), e['t'], .18); add(bell(1174.7), e['t'] + .08, .1)
    elif e['kind'] in ('reveal', 'reveal2'): add(whoosh(), e['t'] - .3, .25); [add(bell(f, 1.5), e['t'] + .1 * k, .12) for k, f in enumerate([1046.5, 1318.5, 1568.0])]
    elif e['kind'] == 'cta': add(bell(880.0, 1.0), e['t'], .15)
out = np.tanh(out * 1.2) / np.tanh(1.2); out *= 0.85 / max(1e-6, np.abs(out).max())
w = wave.open(f'audio/{ep}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('audio ok', round(dur, 2))
