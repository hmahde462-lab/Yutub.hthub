#!/bin/bash
# render one arena episode: video + audio + mux
e=$1; names=(x x x x x x x x x sword saw laser shuriken fan walls two-swords three-saws cross-laser final-boss)
n=${names[$((10#$e))]}
node record.js episodes/ep$e.json > out/ep$e.log 2>&1 && python3 sound2.py ep$e >> out/ep$e.log 2>&1 && \
ffmpeg -v error -y -i out/ep${e}_video.mp4 -i audio/ep$e.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "loudnorm=I=-14:TP=-1.5" -shortest -movflags +faststart ep$e-$n-part$((10#$e)).mp4 && echo "ep$e OK" >> out/series2.log || echo "ep$e FAIL" >> out/series2.log
