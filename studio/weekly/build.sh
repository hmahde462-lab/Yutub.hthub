#!/bin/bash
# build.sh <kind> <week>  -> out/<kind>-weekNN.mp4 (1920x1080, blurred bg, centered vertical, side panels)
set -e
K=$1; W=$2
python3 - "$K" "$W" > tmp/$K-$W.txt <<'PY'
import json,sys,os
c=[x for x in json.load(open('comps.json')) if x['kind']==sys.argv[1] and x['w']==int(sys.argv[2])][0]
for f in c['files']: print(f"file '{os.path.abspath(f)}'")
PY
OUT=$(printf "out/%s-week%02d.mp4" $K $W)
ffmpeg -nostdin -y -v error -f concat -safe 0 -i tmp/$K-$W.txt -i art/$K-$W-ov.png -filter_complex \
"[0:v]split[a][b];[a]scale=320:180:force_original_aspect_ratio=increase,crop=320:180,boxblur=8:2,eq=brightness=-0.18,scale=1920:1080:flags=bilinear[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0[v1];[v1][1:v]overlay=0:0,format=yuv420p[v]" \
-map "[v]" -map 0:a -c:v libx264 -preset veryfast -crf 23 -r 30 -c:a aac -b:a 160k -ar 44100 -movflags +faststart $OUT
echo done $OUT
