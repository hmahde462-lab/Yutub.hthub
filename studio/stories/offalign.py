# Offline targets: Gemini anchors from a3.json (if any) + char-proportional estimates between them.
import json, re, subprocess, os, sys
os.chdir(sys.argv[1])
sc = json.load(open('script.json'))
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','chunk0.mp3']))
w = [len(re.sub(r'[\s.…،؟?!:]', '', x['vo'])) + 4 for x in sc]
cum = [sum(w[:i]) for i in range(len(sc)+1)]
cache = json.load(open('a3.json')) if os.path.exists('a3.json') else {}
anc = {0: 0.0}
for k, m in cache.items():
    for i, t in m.items():
        if t is not None and 0.2 < float(t) < 29.7: anc[int(i)] = int(k) + float(t)
anc[len(sc)] = dur
keys = sorted(anc)
# drop non-monotonic anchors
good = [keys[0]]
for k in keys[1:]:
    if anc[k] > anc[good[-1]]: good.append(k)
res = []
for i in range(len(sc)):
    a = max(k for k in good if k <= i); b = min(k for k in good if k >= i)
    res.append(anc[a] if a == b else anc[a] + (anc[b]-anc[a]) * (cum[i]-cum[a]) / (cum[b]-cum[a]))
json.dump({'0': [round(x, 2) for x in res]}, open('align.json', 'w'))
print(len(good)-2, 'anchors')
