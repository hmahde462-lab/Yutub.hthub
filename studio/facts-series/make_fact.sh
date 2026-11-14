#!/usr/bin/env bash
# make_fact.sh N -> out/facts-NN.mp4  (TTS -> timeline -> video -> mix)
set -e; cd "$(dirname "$0")"; n=$1; nn=$(printf %02d $n); d=out/seg_$nn; mkdir -p $d; [ -f out/facts-$nn.mp4 ] && { echo done $nn; exit 0; }
flock /tmp/claude-0/-home-user-yutub-hthub/75479b81-b547-55a6-a2f8-a9ffc6cee05d/scratchpad/tts.lock python3 -I tts.py $d $n
node rec.js $n $d video $d/v.mp4
python3 -I mix.py $d $d/a.wav
ffmpeg -v error -y -i $d/v.mp4 -i $d/a.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out/facts-$nn.mp4
echo done $nn
