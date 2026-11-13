# Join narration segments (trimmed) with gaps -> vo.wav, vo_final.wav (+0.3s lead), tight.json, voice_env.json
import wave, json, os, numpy as np
SR = 44100; GAP = [0.55] * 6
def load(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
    if sr != SR: x = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x).astype(np.float32)
    hop = SR // 100; db = np.array([20 * np.log10(np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) + 1e-9) for i in range(len(x) // hop)])
    on = np.where(db > -40)[0]; a, b = max(0, on[0] - 4) * hop, min(len(x), (on[-1] + 6) * hop); return x[a:b]
segs = [load(f'audio/seg{i}.wav') if os.path.exists(f'audio/seg{i}.wav') else np.zeros(int(7 * SR), np.float32) for i in range(7)]
out, bounds, t = [], [], 0.0
for i, s in enumerate(segs):
    if i: g = np.zeros(int(GAP[i - 1] * SR), np.float32); out.append(g); t += len(g) / SR; bounds.append(round(t - 0.15, 3))
    out.append(s); t += len(s) / SR
vo = np.concatenate(out); vo = vo / (np.abs(vo).max() + 1e-9) * 0.9
def save(p, x):
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
save('audio/vo.wav', vo); fin = np.concatenate([np.zeros(int(0.3 * SR), np.float32), vo]); save('audio/vo_final.wav', fin)
json.dump({'len': len(vo) / SR, 'bounds': bounds}, open('audio/tight.json', 'w'))
hop = SR // 30; env = [float(np.sqrt(np.mean(fin[i * hop:(i + 1) * hop] ** 2))) if (i + 1) * hop <= len(fin) else 0.0 for i in range(len(fin) // hop + 60)]
m = max(env) or 1; env = [round(min(1, e / m * 1.6), 3) for e in env]
json.dump(env, open('audio/voice_env.json', 'w'))
print('len', round(len(vo) / SR, 2), 'bounds', bounds)
