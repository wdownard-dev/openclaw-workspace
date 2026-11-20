#!/bin/bash
# usage: scout_dl.sh <videoId> <name>  -> downloads low-res to ~/dl/<name>, contact sheet to screens/scout/<name>.png
Y=$HOME/tools/ytdlp-venv/bin/yt-dlp
F=/home/williamdownard/openclaw-sites/bin/ffmpeg
S=$HOME/.openclaw/workspace/projects/opusclip/screens/scout
mkdir -p "$HOME/dl/$2"
$Y -q -f 'bv*[height<=480]+ba/b[height<=480]' --ffmpeg-location "$F" -o "$HOME/dl/$2/src.%(ext)s" "https://youtu.be/$1" 2>&1 | tail -2
f=$(ls "$HOME"/dl/$2/src.* | head -1)
$F -loglevel error -y -i "$f" -vf "fps=1/10,scale=180:-1,tile=8x6" -frames:v 1 "$S/$2.png"
ls -la "$S/$2.png"
