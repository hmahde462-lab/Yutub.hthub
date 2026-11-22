#!/bin/bash
# download ep2 images listed in urls.txt (scene-number asset-id) that are missing
cd "$(dirname "$0")"; mkdir -p img
while read n id; do [ -s img/e2_$n.png ] || curl -sf -L -o img/e2_$n.png "https://www.figma.com/api/mcp/asset/$id.png" && echo "$n ok"; done < urls.txt
