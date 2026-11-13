#!/usr/bin/env bash
# make_one.sh N -> out/flag-battle-NN.mp4 (video + synced sound)
set -e; cd "$(dirname "$0")"; n=$1; nn=$(printf %02d $n); mkdir -p out/tmp
node rec.js $n events out/tmp/ev_$nn.json >/dev/null
python3 sound_duel.py out/tmp/ev_$nn.json out/tmp/a_$nn.wav >/dev/null
node rec.js $n video out/tmp/v_$nn.mp4
ffmpeg -v error -y -i out/tmp/v_$nn.mp4 -i out/tmp/a_$nn.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out/flag-battle-$nn.mp4
echo done $nn
