#!/bin/bash
# usage: remix.sh slug [shorts]  — re-mix audio of the long (quiet ambience + real SFX); with "shorts", rebuild clean + shorts (no licensed SFX)
d=$1; cd "$(dirname "$0")/$d" || exit 1
S=/tmp/claude-0/-home-user-Yutub-hthub/b098f5c9-1e4c-5b52-821b-ca5d00028a8c/scratchpad
AUDIO_ONLY=1 VIDEO_IN=../../../videos/long/$d.mp4 OUT=$S/${d}_new.mp4 python3 build.py > $S/${d}_remix.log 2>&1 && mv $S/${d}_new.mp4 ../../../videos/long/$d.mp4 && echo "$d long remixed $(ls -la ../../../videos/long/$d.mp4 | awk '{print $5}')"
if [ "$2" = shorts ]; then
  rm -rf clips clips_main ov sov
  NOSUB=1 FORCE=1 NOSFX=1 OUT=${d}_clean.mp4 python3 build.py > $S/${d}_clean.log 2>&1 && python3 shorts.py > $S/${d}_shorts.log 2>&1 && echo "$d shorts rebuilt"
  rm -rf clips clips_main ov sov big audio.wav video_noaudio.mp4 ${d}_clean.mp4
fi
