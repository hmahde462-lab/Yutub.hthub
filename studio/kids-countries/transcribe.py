# Transcribe each kNN.wav with Gemini (phrase timestamps) -> audio/kNN.tr.txt
import json, sys, base64, urllib.request, subprocess, time, os
def tr(path):
    mp3 = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-b:a', '48k', '-f', 'mp3', '-'])
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(mp3).decode()}},
            {"text": "Transcribe with timestamps per phrase, format exactly: SS.ss - SS.ss text (seconds with 2 decimals), one phrase per line."}]}],
            "generationConfig": {"temperature": 0}}
    for m in ['gemini-3.5-flash', 'gemini-flash-latest', 'gemini-3.8-flash']:
        for _ in range(2):
            try:
                req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent', data=json.dumps(body).encode(),
                                             headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
                r = json.load(urllib.request.urlopen(req, timeout=120)); return r['candidates'][0]['content']['parts'][0]['text']
            except Exception as e: time.sleep(3)
    return None
if __name__ == '__main__':
    pre = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        out = f'{pre}{n:02d}.tr.txt'
        if os.path.exists(out): continue
        t = tr(f'{pre}{n:02d}.wav')
        if t: open(out, 'w').write(t); print(n, 'ok', t.splitlines()[0][:60])
        else: print(n, 'FAIL')
