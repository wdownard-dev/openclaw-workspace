#!/bin/bash
# usage: hunt2_dl.sh ID NAME
mkdir -p ~/dl/hunt2/$2
~/tools/ytdlp-venv/bin/yt-dlp -q -f 'bv*[height<=480]+ba/b[height<=480]' --merge-output-format mp4 --ffmpeg-location /home/williamdownard/openclaw-sites/bin/ffmpeg -o "$HOME/dl/hunt2/$2/v.%(ext)s" "https://www.youtube.com/watch?v=$1" > ~/dl/hunt2/$2/log.txt 2>&1
