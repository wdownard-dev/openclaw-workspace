#!/bin/bash
# usage: scout_dl.sh <videoId> <name>  -> ~/dl/<name>/src.* and screens/scout/<name>.png
FF=/home/williamdownard/openclaw-sites/bin/ffmpeg
Y=$HOME/tools/ytdlp-venv/bin/yt-dlp
S=$HOME/.openclaw/workspace/projects/opusclip/screens/scout
mkdir -p "$HOME/dl/$2" "$S"
$Y -q -f 'bv*[height<=480]+ba/b[height<=480]' --ffmpeg-location $FF -o "$HOME/dl/$2/src.%(ext)s" "https://youtu.be/$1" 2>&1 | grep -v WARNING
f=$(ls $HOME/dl/$2/src.* | head -1)
$FF -y -loglevel error -i "$f" -vf "fps=1/10,scale=180:-1,tile=8x6" -frames:v 1 "$S/$2.png"
ls -la "$HOME/dl/$2" "$S/$2.png"
