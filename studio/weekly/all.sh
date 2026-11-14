#!/bin/bash
cd "$(dirname "$0")"
python3 -c "import json;[print(c['kind'],c['w']) for c in json.load(open('comps.json'))]" | while read k w; do
  o=$(printf "out/%s-week%02d.mp4" $k $w); [ -s "$o" ] && continue; ./build.sh $k $w
done
echo ALLDONE
