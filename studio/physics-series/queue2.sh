#!/bin/bash
cd /home/user/yt-studio/physics-series
until [ $(grep -c "^b0" out/batch.log 2>/dev/null) -ge 9 ]; do sleep 10; done
{ echo "b10 final/s2-battles/battle-10.mp4"
  for i in 01 02 03 04 05 06 07 08 09 10; do echo "d$i final/s3-fights/fight-$i.mp4"; done
  for i in 01 02 03 04 05 06 07 08 09 10; do echo "c$i final/s1-cutting/cutting-$i.mp4"; done; } | xargs -P 3 -n 2 ./render_ep.sh
echo ALLDONE >> out/batch.log
