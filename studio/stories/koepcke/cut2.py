# Boundary DP over detected silences: cost = timing error vs Gemini targets + mismatch in expected internal pauses ("...", "،", mid "." / "؟").
import json, re, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
sc = json.load(open('script.json')); f = 'chunk0.mp3'
def probe(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
dur = probe(f)
err = subprocess.run(['ffmpeg','-i',f,'-af','silencedetect=noise=-32dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
sil = [((s+e)/2, e-s) for s, e in zip(st, en) if s > 0.3 and e < dur - 0.1]
tg = json.load(open('align.json'))['0']
def internal(t):
    t = t.strip().rstrip('.!؟?…').strip()
    return len(re.findall(r'\.\.\.|…', t)) + t.count('،') + len(re.findall(r'(?<!\.)\.(?!\.)', t)) + t.count('؟') + t.count('?')
exp = [internal(x['vo']) for x in sc]
n = len(sc); m = len(sil); INF = 1e18; A, B = 0.35, 1.0
# dp[j][s]: boundary j (start of line j+1) placed at silence s; line j+1 spans silences between.
dp = [[INF]*m for _ in range(n-1)]; bk = [[-1]*m for _ in range(n-1)]
for s in range(m):  # line 0 internal = silences before s
    dp[0][s] = A*(sil[s][0]-tg[1])**2 + B*(s - exp[0])**2 - 0.3*sil[s][1]
for j in range(1, n-1):
    for s in range(j, m):
        best, bi = INF, -1
        for p in range(max(0, s-12), s):
            c = dp[j-1][p] + B*((s-p-1) - exp[j])**2
            if c < best: best, bi = c, p
        if bi >= 0: dp[j][s] = best + A*(sil[s][0]-tg[j+1])**2 - 0.3*sil[s][1]; bk[j][s] = bi
s = min(range(m), key=lambda q: dp[n-2][q] + B*((m-q-1) - exp[n-1])**2); path = [s]
for j in range(n-2, 0, -1): s = bk[j][s]; path.append(s)
path.reverse(); cuts = [0] + [sil[q][0] for q in path] + [dur]
os.makedirs('lines', exist_ok=True); out = []
for i in range(n):
    o = f'lines/line{i:02d}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(cuts[i]),'-to',str(cuts[i+1]),'-i',f,'-ar','48000','-ac','1',o],check=True)
    out.append({'i': i, 'dur': round(probe(o), 3)})
    print(f'{i}:{cuts[i]:.2f}({cuts[i+1]-cuts[i]:.1f}|tg {tg[i]})', end='  ' if (i+1) % 5 else '\n')
json.dump(out, open('lines.json','w'))
