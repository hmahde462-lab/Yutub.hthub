# TTS 3 illusions per request, split into 9 paragraphs by silence+text DP. usage: python3 tts_batch.py <first_n> (does n,n+1,n+2)
import json, sys, os, subprocess, wave
import numpy as np
sys.path.insert(0, '.'); from scripts import S
sys.path.insert(0, '../../kids-countries')
src = open('../../kids-countries/render_q.py').read().split('if __name__')[0]; g = {}; exec(src.replace("D = json.load(open('questions.json'))", "D=[]"), g)
E = json.load(open('ill.json')); MODELS = ['gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts', 'gemini-3.8-flash-lite-tts']
n0 = int(sys.argv[1]); ns = [n for n in range(n0, n0 + 3) if n <= len(E)]
if all(os.path.exists(f'audio/i{n:02d}_c.wav') for n in ns): sys.exit()
paras = [p for n in ns for p in S(E[n - 1])['vo']]
txt = f'audio/b{n0:02d}.txt'; open(txt, 'w').write('\n\n'.join(paras)); wav = f'audio/b{n0:02d}.wav'
if not os.path.exists(wav):
    tts = open('../../whiteboard-p3/tts.py').read()
    for m in MODELS:
        r = subprocess.run(['python3', '-c', tts.replace("model = 'gemini-3.8-flash-tts'", f"model = '{m}'"), 'Puck', wav, txt], capture_output=True, text=True)
        if r.returncode == 0: print(n0, m, r.stdout.strip()); break
        print(n0, m, 'FAIL', r.stderr.strip().splitlines()[-1][:90])
    else: sys.exit(1)
x, sr = g['load'](wav); seg = g['segments'](x, sr, len(paras), paras)
for k, (a, b) in enumerate(seg):
    n = ns[k // 3]; part = 'abc'[k % 3]; y = x[int(a * sr):int(b * sr)]
    # trim silence edges
    env = np.abs(y); idx = np.where(env > 0.02)[0]
    if len(idx): y = y[max(0, idx[0] - int(.05 * sr)):idx[-1] + int(.12 * sr)]
    w = wave.open(f'audio/i{n:02d}_{part}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print(n0, 'split', [round(b, 1) for _, b in seg])
