import json,base64,urllib.request,os,sys
model=os.environ.get("TTS_MODEL","gemini-3.1-flash-tts-preview")
text="""Umm: واااو! هاي شنو هاللعبة الحلوة! يلا اركض اركض!

Hamoudi: يمّه! هاي لعبتي! وصلتي ست نجوم!

Umm: اسكت! روح نام، باچر عندك دوام!"""
body={"contents":[{"parts":[{"text":text}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"multiSpeakerVoiceConfig":{"speakerVoiceConfigs":[
 {"speaker":"Hamoudi","voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Puck"}}},
 {"speaker":"Umm","voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Sulafat"}}}]}}}}
req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":"dummy"})
try: r=json.load(urllib.request.urlopen(req,timeout=180))
except urllib.error.HTTPError as e: print(e.code,e.read()[:400]); sys.exit(1)
d=base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
mt=r["candidates"][0]["content"]["parts"][0]["inlineData"].get("mimeType")
if d[:4]==b"RIFF": open("dia.wav","wb").write(d)
else:
  open("dia.pcm","wb").write(d); os.system("ffmpeg -v error -y -f s16le -ar 24000 -ac 1 -i dia.pcm dia.wav")
print("ok",mt)
