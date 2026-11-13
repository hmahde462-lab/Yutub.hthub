#!/bin/bash
# usage: render_ep.sh <episode-id> <output.mp4>   (sound script chosen by template)
e=$1; out=$2; tpl=$(python3 -c "import json;print(json.load(open('episodes/$e.json'))['template'])")
case $tpl in battle.html) snd=sound_battle.py;; duel.html) snd=sound_duel.py;; *) snd=sound2.py;; esac
node record.js episodes/$e.json > out/$e.log 2>&1 && python3 $snd $e >> out/$e.log 2>&1 && \
ffmpeg -v error -y -i out/${e}_video.mp4 -i audio/$e.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "loudnorm=I=-14:TP=-1.5" -shortest -movflags +faststart "$out" && echo "$e OK" >> out/batch.log || echo "$e FAIL" >> out/batch.log
