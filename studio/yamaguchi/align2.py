# Gemini transcription in short windows -> per-line start times (align.json), matched by text similarity.
import base64, json, urllib.request, re, subprocess, os, difflib, time
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SP = '/tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad'
sc = json.load(open('script.json')); f = 'chunk0.mp3'; GM = os.environ.get('GM', 'gemini-3-flash-preview')
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
cache = json.load(open('phr.json')) if os.path.exists('phr.json') else {}
W, STEP = 45, 45
t0 = 0
while t0 < dur:
    key = str(t0)
    if key not in cache:
        seg = f'{SP}/w{t0}.mp3'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t0),'-t',str(W),'-i',f,seg], check=True)
        b = base64.b64encode(open(seg,'rb').read()).decode()
        prompt = ("Transcribe this Arabic audio sentence by sentence. For each sentence give its start time in seconds from the start of THIS clip "
                  "(two decimals). Reply with JSON only: a list of objects {\"t\": number, \"text\": string}.")
        body = {"contents":[{"parts":[{"inline_data":{"mime_type":"audio/mpeg","data":b}},{"text":prompt}]}],
                "generationConfig":{"responseMimeType":"application/json"}}
        for attempt in range(3):
            try:
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{GM}:generateContent",
                    data=json.dumps(body).encode(), headers={"Content-Type":"application/json","x-goog-api-key":"dummy"})
                r = json.load(urllib.request.urlopen(req, timeout=300)); break
            except Exception as e:
                print('retry', t0, e); time.sleep(15)
        txt = r['candidates'][0]['content']['parts'][-1]['text']
        cache[key] = json.loads(re.search(r'\[.*\]', txt, re.S).group(0))
        json.dump(cache, open('phr.json','w'), ensure_ascii=False)
    t0 += STEP
def norm(s):
    s = re.sub(r'[ً-ْـ]', '', s); s = re.sub(r'[^\w\s]', ' ', s)
    s = s.replace('گ','ك').replace('چ','ج').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه').replace('ى','ي')
    return ' '.join(s.split())
phr = []
for k, lst in cache.items():
    if int(k) % STEP: continue
    for p in lst:
        t = int(k) + float(p['t'])
        phr.append((t, norm(p['text'])))
phr.sort()
starts = [0.0]; last = 0.0
for i in range(1, len(sc)):
    head = ' '.join(norm(sc[i]['vo']).split()[:2])
    best = None
    for t, txt in phr:
        if t < last + 0.5: continue
        r = difflib.SequenceMatcher(None, head, ' '.join(txt.split()[:2])).ratio()
        if best is None or r > best[0] + 1e-9 and not (best[0] > 0.75 and t > best[1] + 15): best = (r, t) if (best is None or r > best[0]) else best
        if t > last + 25: break
    if best and best[0] > 0.5: starts.append(round(best[1], 2)); last = best[1]
    else: starts.append(None)
print(starts)
# fill gaps by interpolation
for i, v in enumerate(starts):
    if v is None:
        a = max(j for j in range(i) if starts[j] is not None); b = next((j for j in range(i+1, len(starts)) if starts[j] is not None), None)
        tb = starts[b] if b else dur; starts[i] = round(starts[a] + (tb - starts[a]) * (i - a) / ((b or len(starts)) - a), 2)
json.dump({'0': starts}, open('align.json','w'))
