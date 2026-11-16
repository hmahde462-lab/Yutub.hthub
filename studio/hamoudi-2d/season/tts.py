import json,base64,urllib.request,os,sys,time
model=os.environ.get("TTS_MODEL","gemini-2.5-flash-preview-tts")
E=json.load(open('season.json'))
for ep in sys.argv[1:]:
  if os.path.exists(f"voice/e{ep}.wav"): continue
  text="Read in an Iraqi Baghdadi Arabic accent, lively comedy cartoon. Hamoudi is a cheeky teen boy, Umm is his strict funny mother.\n\n"+"\n\n".join(f"{s}: {t}" for s,t in E[ep]["l"])
  body={"contents":[{"parts":[{"text":text}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"multiSpeakerVoiceConfig":{"speakerVoiceConfigs":[
   {"speaker":"Hamoudi","voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Puck"}}},
   {"speaker":"Umm","voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Sulafat"}}}]}}}}
  req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":"dummy"})
  try: r=json.load(urllib.request.urlopen(req,timeout=300))
  except urllib.error.HTTPError as e: print(ep,e.code,e.read()[:300].decode(errors='ignore')); sys.exit(1)
  d=base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
  open(f"voice/e{ep}.pcm","wb").write(d); os.system(f"ffmpeg -v error -y -f s16le -ar 24000 -ac 1 -i voice/e{ep}.pcm voice/e{ep}.wav && rm voice/e{ep}.pcm"); print("ok",ep,flush=True)
