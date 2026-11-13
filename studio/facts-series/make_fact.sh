#!/usr/bin/env bash
# make_fact.sh N -> out/facts-NN.mp4  (TTS -> timeline -> video -> mix)
set -e; cd "$(dirname "$0")"; n=$1; nn=$(printf %02d $n); d=out/seg_$nn; mkdir -p $d
python3 -I tts.py $d $n
node rec.js $n $d video $d/v.mp4
python3 -I mix.py $d $d/a.wav
ffmpeg -v error -y -i $d/v.mp4 -i $d/a.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out/facts-$nn.mp4
echo done $nn
