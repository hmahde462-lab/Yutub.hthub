#!/bin/bash
# usage: brand.sh file.mp4 ...  -> overlays channel avatar + @handle in place (clean copy kept in scratchpad)
B=$(dirname "$(readlink -f "$0")")
CLEAN=/tmp/claude-0/-home-user-yutub-hthub/0cc65cae-c7c9-58db-a31c-a39d3be99e8d/scratchpad/hm/clean; mkdir -p $CLEAN
for f in "$@"; do
  n=$(basename "$f"); [ -f "$CLEAN/$n" ] || cp "$f" "$CLEAN/$n"
  ffmpeg -v error -y -i "$CLEAN/$n" -i "$B/overlay.png" -filter_complex "[0:v][1:v]overlay=0:0" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f" && echo "branded $n"
done
