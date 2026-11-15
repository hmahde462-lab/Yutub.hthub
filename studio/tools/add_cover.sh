#!/bin/bash
# Shorts cover: put the thumbnail image as a very short first frame (default 0.2s) so YouTube can pick it as the Short's cover.
# usage: add_cover.sh in.mp4 cover.jpg out.mp4 [seconds=0.2] [start|end]
set -e
IN=$1; IMG=$2; OUT=$3; D=${4:-0.2}; POS=${5:-start}
read W H FPS < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0:s=' ' "$IN")
V="scale=$W:$H:force_original_aspect_ratio=decrease,pad=$W:$H:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=$FPS,format=yuv420p"
if [ "$POS" = start ]; then ORD="[c][ca][v][a]"; else ORD="[v][a][c][ca]"; fi
ffmpeg -v error -y -i "$IN" -loop 1 -t "$D" -i "$IMG" -f lavfi -t "$D" -i anullsrc=r=48000:cl=stereo -filter_complex \
 "[1]$V[c];[2]aformat=sample_rates=48000:channel_layouts=stereo[ca];[0:v]$V[v];[0:a]aresample=48000,aformat=channel_layouts=stereo[a];${ORD}concat=n=2:v=1:a=1[ov][oa]" \
 -map "[ov]" -map "[oa]" -c:v libx264 -crf 19 -preset fast -c:a aac -b:a 160k "$OUT"
echo "$OUT"
