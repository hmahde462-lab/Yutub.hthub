#!/bin/bash
# assemble narration -> render -> mix -> mp4
set -e
cd "$(dirname "$0")"
python3 assemble.py
python3 -c "h=open('board2.html').read().replace('__DATA__',open('scenes.json').read()).replace('__VOICE__',open('audio/voice_env.json').read());open('board2_built.html','w').write(h)"
node render2.js full | tail -1
python3 ../whiteboard-p4/mix.py
ffmpeg -v error -y -i out/video_noaudio.mp4 -i audio/mix_pres.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart afkar-ghariba-5questions-part4.mp4
echo FINAL_DONE
