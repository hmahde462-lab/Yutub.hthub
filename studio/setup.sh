#!/usr/bin/env bash
# Installs what this workspace needs in a fresh cloud session. Safe to re-run.
set -e
cd "$(dirname "$0")"
pip install -q yt-dlp numpy pillow
pip install -q -r yt-manager/requirements.txt
(cd afkar-video && npm install --silent)
echo "yt-studio setup done"
