"""Dark cinematic bed + event SFX for top10. Writes out/music.wav and out/sfx.wav (mono 44.1k)."""
import json, wave, numpy as np
SR = 44100; d = json.load(open('out/events.json')); dur = d['duration'] + .3; N = int(dur * SR)
rng = np.random.default_rng(3); tt = np.arange(N) / SR
def wav(name, x):
    x = x / (np.abs(x).max() + 1e-9) * .9; w = wave.open(name, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
def band(n, lo, hi):
    x = rng.normal(0, 1, n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; x = np.fft.irfft(X, n); return x / (np.abs(x).max() + 1e-9)
def env(n, a, dcy): x = np.arange(n) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x * dcy)
# ---------- music ----------
m = np.zeros(N)
ramp = np.clip(tt / dur, 0, 1)
for f, g_ in [(36.7, .5), (73.4, .35), (110.0, .2), (146.8, .08)]:
    m += g_ * np.sin(2 * np.pi * f * tt + .3 * np.sin(2 * np.pi * .07 * tt)) * (.7 + .3 * np.sin(2 * np.pi * .05 * tt + f))
m += .12 * band(N, 80, 400) * (.5 + .5 * np.sin(2 * np.pi * .03 * tt))
beat = 60 / 72
for k in range(int(dur / beat)):
    t0 = k * beat; n = int(.3 * SR); x = np.arange(n) / SR
    th = np.sin(2 * np.pi * (48 + 40 * np.exp(-x * 30)) * x) * np.exp(-x * 14)
    for off, gg in [(0, 1), (.22, .6)]:
        i = int((t0 + off) * SR); j = min(N, i + n)
        if i < N: m[i:j] += th[:j - i] * gg * (.35 + .5 * ramp[i])
m *= np.minimum(1, tt / .6) * np.minimum(1, (dur - tt) / 2)
# minor piano-ish motif (D minor) every 4 bars
notes = [293.7, 349.2, 440.0, 349.2, 311.1, 293.7]
for k in range(int(dur / (beat * 8))):
    for j, f in enumerate(notes):
        t0 = k * beat * 8 + j * beat * .66; n = int(1.4 * SR); x = np.arange(n) / SR
        s = (np.sin(2 * np.pi * f * x) + .4 * np.sin(4 * np.pi * f * x) + .15 * np.sin(6 * np.pi * f * x)) * np.exp(-x * 3)
        i = int(t0 * SR); jj = min(N, i + n)
        if i < N: m[i:jj] += s[:jj - i] * .12
wav('out/music.wav', m)
# ---------- sfx ----------
s = np.zeros(N)
def add(x, t, gain):
    i = int(t * SR); j = min(N, i + len(x))
    if 0 <= i < N: s[i:j] += x[:j - i] * gain
def boom(L=1.2):
    n = int(L * SR); x = np.arange(n) / SR
    return np.sin(2 * np.pi * (42 + 70 * np.exp(-x * 12)) * x) * np.exp(-x * 3.5) + band(n, 60, 2500) * np.exp(-x * 18) * .5
def whoosh(L=.45):
    n = int(L * SR); x = np.arange(n) / SR; k = x / L
    out = np.zeros(n); seg = band(n, 300, 6000)
    return seg * np.sin(np.pi * k) ** 2 * (.3 + .7 * k)
def click(): n = int(.04 * SR); return band(n, 1500, 8000) * env(n, .001, 120)
def thud(): n = int(.4 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * (70 + 90 * np.exp(-x * 25)) * x) * np.exp(-x * 10) + band(n, 150, 1200) * np.exp(-x * 30) * .5
def clang():
    n = int(1.4 * SR); x = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * x) * a for f, a in [(310, 1), (743, .6), (1311, .4), (2010, .25)]) * np.exp(-x * 3.5) / 2
def crackle(L):
    n = int(L * SR); out = band(n, 300, 3000) * .15
    for _ in range(int(L * 35)): i = rng.integers(0, n - 800); out[i:i + 800] += band(800, 1000, 7000) * env(800, .0005, 200) * rng.uniform(.3, 1)
    return out * np.minimum(1, np.arange(n) / SR / .3) * np.minimum(1, (L - np.arange(n) / SR) / .5)
def bell(f=880): n = int(1.5 * SR); x = np.arange(n) / SR; return (np.sin(2 * np.pi * f * x) + .5 * np.sin(2 * np.pi * f * 2.76 * x)) * np.exp(-x * 3)
def splash(): n = int(.5 * SR); return band(n, 400, 5000) * env(n, .005, 9)
def buzz(): n = int(.35 * SR); x = np.arange(n) / SR; return np.sign(np.sin(2 * np.pi * 110 * x)) * env(n, .005, 6) * .5
def popx(): n = int(.12 * SR); x = np.arange(n) / SR; return np.sin(2 * np.pi * (900 - 2500 * x) * x) * np.exp(-x * 30)
def chomp():
    out = np.zeros(int(1.0 * SR))
    for k in range(3): n = int(.12 * SR); i = int(k * .3 * SR); out[i:i + n] += band(n, 500, 4000) * env(n, .002, 30)
    return out
def ticks(L, rate=18):
    out = np.zeros(int(L * SR))
    for k in range(int(L * rate)): i = int(k / rate * SR); c = click(); out[i:i + len(c)] += c * (.6 + .4 * (k % 2))
    return out
def wind(L): n = int(L * SR); x = np.arange(n) / SR; return band(n, 150, 900) * (.5 + .5 * np.sin(2 * np.pi * .3 * x)) * np.minimum(1, x / .8) * np.minimum(1, (L - x) / .8)
for e in d['events']:
    t, k = e['t'], e['kind']
    if k == 'slam': add(whoosh(), max(0, t - .3), .35); add(boom(), t + .05, .7)
    elif k == 'whoosh': add(boom(1.6), t, .5)
    elif k == 'tick': add(click(), t, .35)
    elif k == 'hit': add(boom(1.8), t, .8)
    elif k == 'stake': add(thud(), t, .45)
    elif k == 'chomp': add(chomp(), t, .4)
    elif k == 'impact': add(boom(), t, .8); add(clang(), t, .2)
    elif k in ('ticks', 'ticks2'): add(ticks(2.6 if k == 'ticks' else 1.3), t, .25)
    elif k == 'ticks3': add(ticks(1.9, 24), t, .25)
    elif k == 'clang': add(clang(), t, .5)
    elif k == 'stamp': add(thud(), t, .6)
    elif k == 'pops': add(ticks(2.0, 14), t, .3)
    elif k == 'fire': add(crackle(4.6), t, .45)
    elif k == 'fire2': add(crackle(3.6), t, .45)
    elif k == 'boom': add(boom(), t, .6)
    elif k == 'splash': add(splash(), t, .3)
    elif k == 'x': add(buzz(), t, .3)
    elif k == 'drop': add(boom(), t, .5)
    elif k == 'wind': add(wind(9.0), t, .35)
    elif k == 'ding': add(bell(), t, .35)
    elif k == 'pop': add(popx(), t, .4)
    elif k == 'click': add(click(), t, .6); add(bell(1320), t + .05, .35)
wav('out/sfx.wav', s)
print('ok', len(d['events']), 'events')
