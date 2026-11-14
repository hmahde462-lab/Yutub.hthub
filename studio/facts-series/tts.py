# usage: python3 tts.py <out_dir> <ep_index 1-based>  -> seg0..seg4.mp3 + segs.json (durations)
# ElevenLabs (multilingual v2) first; falls back to Gemini TTS if ElevenLabs refuses (quota etc).
import sys, json, os, subprocess, urllib.request, base64, wave
out, n = sys.argv[1], int(sys.argv[2]); os.makedirs(out, exist_ok=True)
E = json.load(open(os.path.join(os.path.dirname(__file__), 'facts.json'), encoding='utf-8'))[n - 1]
NUM = ['رقم واحد', 'رقم اثنين', 'رقم ثلاثة']
lines = [f"ثلاث معلومات غريبة عن سكان {E['c']}… الثالثة راح تصدمك!"] + [f"{NUM[i]}: {t}" for i, (t, _) in enumerate(E['x'])] + \
        ["إنت من وين؟ اكتب دولتك بالتعليقات حتى نسويلها حلقة، وتابعنا للحلقة الجاية!"]
VOICE = 'pNInz6obpgDQGcFmaJgB'
def el(text, path):
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35}}).encode()
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128', data=body,
                                 headers={'xi-api-key': 'dummy', 'Content-Type': 'application/json'})
    open(path, 'wb').write(urllib.request.urlopen(req, timeout=120).read())
def gem(text, path):
    for model in ['gemini-3.8-flash-tts', 'gemini-2.5-flash-preview-tts', 'gemini-3.1-flash-tts-preview', 'gemini-2.5-pro-preview-tts']:
        try:
            body = {"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Algieba"}}}}}
            req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
            r = json.load(urllib.request.urlopen(req, timeout=180)); pcm = base64.b64decode(r['candidates'][0]['content']['parts'][0]['inlineData']['data'])
            w = wave.open(path + '.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm); w.close()
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path + '.wav', path], check=True); return model
        except Exception as e: print('gemini fail', model, e, file=sys.stderr)
    raise SystemExit('no TTS available')
durs, engine = [], []
for i, t in enumerate(lines):
    p = os.path.join(out, f'seg{i}.mp3')
    if not os.path.exists(p):
        ok = False
        for k in range(8):
            try: el(t, p); engine.append('elevenlabs'); ok = True; break
            except Exception as e:
                print('elevenlabs retry', k, e, file=sys.stderr)
                if '429' not in str(e) and '5' != str(getattr(e, 'code', ''))[:1]: break
                import time; time.sleep(4 + 4 * k)
        if not ok: engine.append(gem(t, p))
    else: engine.append('cached')
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
    durs.append(round(d, 3))
json.dump({'durs': durs, 'lines': lines, 'engine': engine}, open(os.path.join(out, 'segs.json'), 'w'), ensure_ascii=False)
print(n, E['c'], durs, engine)
