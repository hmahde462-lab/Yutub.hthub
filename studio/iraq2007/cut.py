# Cut each narration chunk into per-scene wavs: DP-align silences to char-proportional targets.
import json, re, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
sc = json.load(open('script.json')); ch = json.load(open('chunks.json'))
os.makedirs('lines', exist_ok=True)
def probe(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
out = []
for k, c in enumerate(ch):
    f = f'chunk{k}.mp3'; idx = c['idx']; n = len(idx); dur = probe(f)
    err = subprocess.run(['ffmpeg','-i',f,'-af','silencedetect=noise=-32dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    sil = [((s+e)/2, e-s) for s, e in zip(st, en) if s > 0.3 and e < dur - 0.1]
    w = [len(re.sub(r'[\s.…،؟?!:]', '', sc[i]['vo'])) + 4 for i in idx]; tot = sum(w)
    t0, t1 = 0.2, dur - 0.2
    tg = []; a = 0
    for x in w[:-1]: a += x; tg.append(t0 + (t1-t0)*a/tot)
    if os.path.exists('align.json'):  # Gemini start times (more accurate than char proportion)
        al = json.load(open('align.json')).get(str(k))
        if al and len(al) == n: tg = [float(t) - 0.15 for t in al[1:]]
    m = len(sil); INF = 1e18
    # dp[j][s] = min cost placing boundary j at silence s
    dp = [[INF]*m for _ in range(n-1)]; bk = [[-1]*m for _ in range(n-1)]
    for s in range(m): dp[0][s] = (sil[s][0]-tg[0])**2 - 0.5*sil[s][1]
    for j in range(1, n-1):
        for s in range(m):
            best, bi = INF, -1
            for p in range(s):
                if dp[j-1][p] < best: best, bi = dp[j-1][p], p
            if bi >= 0: dp[j][s] = best + (sil[s][0]-tg[j])**2 - 0.5*sil[s][1]; bk[j][s] = bi
    s = min(range(m), key=lambda q: dp[n-2][q]); path = [s]
    for j in range(n-2, 0, -1): s = bk[j][s]; path.append(s)
    cuts = [0] + [sil[q][0] for q in reversed(path)] + [dur]
    ov = json.load(open('overrides.json')) if os.path.exists('overrides.json') else {}
    for j, i in enumerate(idx[1:]):  # manual fixes: line i starts at given time
        if str(i) in ov: cuts[j+1] = ov[str(i)]
    for j, i in enumerate(idx):
        a, b = cuts[j], cuts[j+1]; o = f'lines/line{i:02d}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',f,'-ar','48000','-ac','1',o],check=True)
        d = probe(o); out.append({'i': i, 'dur': round(d, 3)})
        print(i, f'{a:.2f}-{b:.2f}', round(d,2), sc[i]['vo'][:28])
json.dump(out, open('lines.json','w'))
