#!/bin/bash
# rebuild clean + shorts only (new quiet ambience, no licensed SFX)
d=$1; cd "$(dirname "$0")/$d" || exit 1
S=/tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad
rm -rf clips clips_main ov sov
NOSUB=1 FORCE=1 NOSFX=1 OUT=${d}_clean.mp4 python3 build.py > $S/${d}_clean.log 2>&1 && python3 shorts.py > $S/${d}_shorts.log 2>&1 && echo "$d shorts rebuilt" || echo "$d FAILED"
rm -rf clips clips_main ov sov big audio.wav video_noaudio.mp4 ${d}_clean.mp4
