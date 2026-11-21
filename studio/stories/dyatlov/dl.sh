#!/bin/bash
# usage: dl.sh  (reads new "N url" lines from stdin, appends to urls.txt, saves img_jpg/N.jpg)
while read n u; do echo "$n $u" >> urls.txt; curl -sSfL "$u" -o /tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad/t.png && ffmpeg -nostdin -v error -y -i /tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad/t.png -q:v 2 img_jpg/$n.jpg || echo FAIL $n; done
ls img_jpg | wc -l
