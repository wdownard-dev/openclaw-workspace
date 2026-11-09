#!/bin/bash
# usage: dlcase.sh <case> <id>...
Y=~/tools/ytdlp-venv/bin/yt-dlp
F='bv*[height<=480]+ba/b[height<=480]'
d=$1; shift
mkdir -p ~/dl/$d
for id in "$@"; do
  $Y -q --ffmpeg-location /home/williamdownard/openclaw-sites/bin -f "$F" --merge-output-format mp4 -o "$HOME/dl/$d/$id.%(ext)s" "https://www.youtube.com/watch?v=$id" >/dev/null 2>&1 &
done
wait
