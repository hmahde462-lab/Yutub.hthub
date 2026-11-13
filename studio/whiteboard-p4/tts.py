# usage: python3 tts.py <voice> <out.wav> <text-file>   (Gemini TTS -> 24k mono wav)
import sys, json, base64, urllib.request, wave
voice, out, tf = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(tf, encoding='utf-8').read().strip()
import os; model = os.environ.get('TTS_MODEL', 'gemini-3.1-flash-tts-preview')
body = {"contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', data=json.dumps(body).encode(),
                             headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
r = json.load(urllib.request.urlopen(req, timeout=180))
part = r['candidates'][0]['content']['parts'][0]['inlineData']
pcm = base64.b64decode(part['data']); rate = 24000
if 'rate=' in part.get('mimeType', ''): rate = int(part['mimeType'].split('rate=')[1].split(';')[0])
if pcm[:4] == b'RIFF':
    open(out, 'wb').write(pcm)
else:
    w = wave.open(out, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm); w.close()
w = wave.open(out); print(out, round(w.getnframes() / w.getframerate(), 2), 's', w.getframerate(), 'Hz', w.getnchannels(), 'ch')
