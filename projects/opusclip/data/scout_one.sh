#!/bin/bash
# usage: scout_one.sh <videoId> <name>
YT=~/tools/ytdlp-venv/bin/yt-dlp; FF=/home/williamdownard/openclaw-sites/bin/ffmpeg
S=~/.openclaw/workspace/projects/opusclip/screens/scout
id="$1"; n="$2"; d=~/dl/$n; mkdir -p "$d"
$YT --ffmpeg-location $FF -f 'bv*[height<=480]+ba/b[height<=480]' -o "$d/v.%(ext)s" --merge-output-format mp4 -- "$id" >/dev/null 2>&1
ls "$d"
$YT --skip-download --print '%(upload_date)s %(duration)s age=%(age_limit)s' -- "$id" 2>/dev/null
$YT --skip-download --print '%(description).700s' -- "$id" 2>/dev/null | head -10
$FF -y -loglevel error -i "$d/v.mp4" -vf "fps=1/10,scale=180:-1,tile=8x6" -frames:v 1 "$S/$n.png"
ls -la "$S/$n.png"
