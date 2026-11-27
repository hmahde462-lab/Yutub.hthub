# Constrained alignment: 30s windows, Gemini gives start time of each expected script line present in the window.
import base64, json, urllib.request, re, subprocess, os, time
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SP = '/tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad'
sc = json.load(open('script.json')); f = 'chunk0.mp3'; GM = os.environ.get('GM', 'gemini-3-flash-preview')
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
w = [len(re.sub(r'[\s.…،؟?!:]', '', x['vo'])) + 4 for x in sc]; tot = sum(w)
est = [sum(w[:i]) / tot * dur for i in range(len(sc))]
cache = json.load(open('a3.json')) if os.path.exists('a3.json') else {}
W = 30; t0 = 0
while t0 < dur:
    key = str(t0)
    cand = [i for i in range(len(sc)) if t0 - 12 <= est[i] <= t0 + W + 8]
    if key not in cache and cand:
        seg = f'{SP}/a{t0}.mp3'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t0),'-t',str(W),'-i',f,seg], check=True)
        b = base64.b64encode(open(seg,'rb').read()).decode()
        lines = '\n'.join(f'{i}: {sc[i]["vo"]}' for i in cand)
        prompt = ("This is a 30-second clip cut from a longer Arabic narration. Some of these numbered lines are spoken in it, in order "
                  "(a line may be cut off at the clip start or end):\n" + lines +
                  "\n\nFor every line whose BEGINNING is spoken inside this clip, give the time in seconds from the start of the clip (two decimals) when it begins. "
                  "Reply with JSON only: an object mapping line number to start time; omit lines whose beginning is not in the clip.")
        body = {"contents":[{"parts":[{"inline_data":{"mime_type":"audio/mpeg","data":b}},{"text":prompt}]}],
                "generationConfig":{"responseMimeType":"application/json"}}
        r = None
        for attempt in range(6):
            try:
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{GM}:generateContent",
                    data=json.dumps(body).encode(), headers={"Content-Type":"application/json","x-goog-api-key":"dummy"})
                r = json.load(urllib.request.urlopen(req, timeout=300)); break
            except Exception as e:
                print('retry', t0, e); time.sleep(20)
        if r is None: t0 += W; continue
        txt = r['candidates'][0]['content']['parts'][-1]['text']
        cache[key] = json.loads(re.search(r'\{.*\}', txt, re.S).group(0))
        json.dump(cache, open('a3.json','w'))
    t0 += W
starts = {}
for k, m in cache.items():
    for i, t in m.items():
        if t is None: continue
        t = float(t)
        if 0.2 < t < W - 0.3: starts[int(i)] = round(int(k) + t, 2)  # skip edge-cut ones
starts[0] = 0.0
res = [starts.get(i) for i in range(len(sc))]
print(res)
for i, v in enumerate(res):  # fill gaps
    if v is None:
        a = max(j for j in range(i) if res[j] is not None); b = next((j for j in range(i+1, len(res)) if res[j] is not None), None)
        tb = res[b] if b else dur; res[i] = round(res[a] + (tb - res[a]) * (i - a) / ((b or len(res)) - a), 2)
json.dump({'0': res}, open('align.json','w'))
