#!/bin/bash
# usage: sheet.sh <mp4> <outdir> [fps_denominator]
FF=/home/williamdownard/openclaw-sites/bin/ffmpeg
f=$1; out=$2; den=${3:-8}
id=$(basename "$f" .mp4)
$FF -y -loglevel error -i "$f" -vf "fps=1/$den,scale=180:-1,tile=8x4" -frames:v 1 "$out/${id}_$den.jpg"
