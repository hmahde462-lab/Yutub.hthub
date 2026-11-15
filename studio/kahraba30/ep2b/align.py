# Ask Gemini for the start time of each known line, then snap each boundary to the nearest silence.
import base64, json, urllib.request, re, subprocess, os, sys
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
sc = json.load(open('script.json')); ch = json.load(open('chunks.json'))
def probe(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
res = json.load(open('align.json')) if os.path.exists('align.json') else {}
for k, c in enumerate(ch):
    if str(k) in res: continue
    f = f'chunk{k}.mp3'
    lines = '\n'.join(f'{j+1}. {sc[i]["vo"]}' for j, i in enumerate(c['idx']))
    b = base64.b64encode(open(f, 'rb').read()).decode()
    prompt = ("This Arabic audio reads these numbered lines in order:\n" + lines +
              "\n\nFor each line, give the time in seconds (with two decimals) where that line STARTS being spoken. "
              "Reply with JSON only: a list of numbers, one per line, same order.")
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mpeg", "data": b}}, {"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": "dummy"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    txt = r['candidates'][0]['content']['parts'][-1]['text']
    res[str(k)] = json.loads(re.search(r'\[.*\]', txt, re.S).group(0))
    json.dump(res, open('align.json', 'w'))
    print(k, res[str(k)])
