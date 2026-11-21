# usage: python3 gimg.py N [N...]  -> img_jpg/N.jpg via Gemini image (style ref = img_jpg/7.jpg)
import sys, json, base64, urllib.request, subprocess, os
SP = '/tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad'
s = json.load(open('script.json')); M = os.environ.get('GM', 'gemini-3.1-flash-image')
ref = base64.b64encode(open('img_jpg/7.jpg', 'rb').read()).decode()
for n in map(int, sys.argv[1:]):
    p = s[n]['prompt']
    txt = ("Generate one 16:9 landscape image. Match the art style of the reference image exactly (round white-head cartoon characters composited into photorealistic scenes) "
           "but use a completely new scene: " + p)
    body = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": ref}}, {"text": txt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
    req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json', 'x-goog-api-key': 'dummy'})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
        d = [x for x in r['candidates'][0]['content']['parts'] if 'inlineData' in x][0]['inlineData']['data']
        open(f'{SP}/g.png', 'wb').write(base64.b64decode(d))
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{SP}/g.png', '-vf', 'scale=1536:864:force_original_aspect_ratio=increase,crop=1536:864', '-q:v', '2', f'img_jpg/{n}.jpg'], check=True)
        print('ok', n)
    except Exception as e:
        print('FAIL', n, e, getattr(e, 'read', lambda: b'')()[:300])
