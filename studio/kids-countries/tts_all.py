# Gemini TTS per country video (one request each). usage: python3 tts_all.py [n...]
import json, sys, os, subprocess
D = json.load(open('questions.json'))
MODELS = ['gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts']
def script(e):
    L = [f"تلات أسئلة يسألها أطفال {e['c']}… والكبار يحتارون!"]
    for q, a in e['q']: L += [q, a]
    L.append("إنت من وين؟ اكتب دولتك بالتعليقات، حتى نسويلها حلقة!")
    return '\n\n'.join(L)
for n in map(int, sys.argv[1:]):
    out = f'audio/k{n:02d}.wav'
    if os.path.exists(out): continue
    open(f'audio/k{n:02d}.txt', 'w').write(script(D[n - 1]))
    for m in MODELS:
        r = subprocess.run(['python3', '-c', open('../whiteboard-p3/tts.py').read().replace("model = 'gemini-3.8-flash-tts'", f"model = '{m}'"), 'Puck', out, f'audio/k{n:02d}.txt'], capture_output=True, text=True)
        if r.returncode == 0: print(n, m, r.stdout.strip()); break
        print(n, m, 'FAIL', r.stderr.strip().splitlines()[-1][:120])
