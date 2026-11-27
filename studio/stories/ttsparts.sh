#!/bin/bash
# usage: ttsparts.sh  (in a story dir) — TTS vo.txt in 4 parts with TTS_MODEL, concat to vo.wav
set -e
python3 - <<'P'
import json
s=json.load(open('script.json')); n=len(s); k=4
for j in range(k):
    a,b=j*n//k,(j+1)*n//k
    open(f'vo_p{j}.txt','w').write('\n\n'.join(x['vo'] for x in s[a:b])+'\n')
P
for j in 0 1 2 3; do
  for t in 1 2 3; do python3 ../../whiteboard-p3/tts.py Algieba vo_p$j.wav vo_p$j.txt > tts_p$j.log 2>&1 && break; sleep 20; done
done
ffmpeg -nostdin -v error -y -f lavfi -t 0.6 -i anullsrc=r=24000:cl=mono s.wav
ffmpeg -nostdin -v error -y -i vo_p0.wav -i s.wav -i vo_p1.wav -i s.wav -i vo_p2.wav -i s.wav -i vo_p3.wav -filter_complex "[0][1][2][3][4][5][6]concat=n=7:v=0:a=1" -ar 24000 -ac 1 vo.wav
rm -f vo_p*.txt vo_p*.wav s.wav
