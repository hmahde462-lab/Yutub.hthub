# Ask Gemini for start time of each script line in the TTS audio, then snap to nearest silence. usage: python3 align.py n... -> audio/kNN.align.json
import json, sys, base64, urllib.request, subprocess
D = json.load(open('questions.json'))
def lines(e):
    return [f"تلات أسئلة يسألها أطفال {e['c']}… والكبار يحتارون!"] + [t for qa in e['q'] for t in qa] + ["إنت من وين؟ اكتب دولتك بالتعليقات، حتى نسويلها حلقة!"]
for n in map(int, sys.argv[1:]):
    e = D[n - 1]; L = lines(e)
    mp3 = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', f'audio/k{n:02d}.wav', '-ac', '1', '-b:a', '48k', '-f', 'mp3', '-'])
    prompt = ("This audio is an Arabic narration of these 8 lines in order:\n" + "\n".join(f"{i+1}. {l}" for i, l in enumerate(L)) +
              "\nReturn ONLY JSON: a list of 8 numbers, the start time in seconds (with 2 decimals) where each line begins in the audio.")
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(mp3).decode()}}, {"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    for model in ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-flash-latest']:
        try:
            req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', data=json.dumps(body).encode(),
                                         headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
            r = json.load(urllib.request.urlopen(req, timeout=120)); t = json.loads(r['candidates'][0]['content']['parts'][0]['text'])
            json.dump(t, open(f'audio/k{n:02d}.align.json', 'w')); print(n, model, t); break
        except Exception as ex: print(n, model, 'ERR', str(ex)[:100])
