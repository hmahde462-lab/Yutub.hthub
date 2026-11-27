#!/bin/bash
# usage: relong.sh slug crf  — regenerate TTS/alignment and rebuild long + shorts for a story whose script.json vo changed
set -e
d=$1; crf=${2:-26}; cd "$(dirname "$0")/$d"
python3 ../../whiteboard-p3/tts.py Algieba vo.wav vo.txt > tts.log 2>&1
ffmpeg -nostdin -v error -y -i vo.wav -b:a 192k chunk0.mp3
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 chunk0.mp3); echo "$d audio $dur"
rm -f a3.json
for k in $(seq 1 12); do
  GM=gemini-3-flash-preview python3 align3.py > align.log 2>&1 || true
  ok=$(python3 -c "import json,math;c=json.load(open('a3.json'));print(int(len(c)>=math.ceil($dur/30)))" 2>/dev/null || echo 0)
  [ "$ok" = 1 ] && break; sleep 90
done
echo "$d windows $(python3 -c "import json;print(sorted(map(int,json.load(open('a3.json')))))")"
rm -rf lines; python3 cut2.py > cut.log 2>&1
rm -rf clips clips_main ov sov big
python3 build.py > build.log 2>&1
NOSUB=1 FORCE=1 OUT=${d}_clean.mp4 python3 build.py > build2.log 2>&1
python3 shorts.py > shorts.log 2>&1
ffmpeg -nostdin -v error -y -i $d.mp4 -c:v libx264 -crf $crf -preset medium -c:a copy ../../../videos/long/$d.mp4
ls -la ../../../videos/long/$d.mp4; ffprobe -v error -show_entries format=duration -of csv=p=0 ../../../videos/long/$d.mp4
rm -rf clips clips_main ov sov big audio.wav video_noaudio.mp4 $d.mp4 ${d}_clean.mp4 vo.wav timeline.json
echo "$d DONE"
