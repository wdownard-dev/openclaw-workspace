#!/usr/bin/env bash
# Norse animatic. usage: bash render.sh slice   -> out/norse_slice_540p.mp4 + out/norse_slice_sheet.jpg
#                       bash render.sh full [cuts.json] -> out/norse_full_540p.mp4 + out/norse_full_sheet.jpg
# env: CONC (default 8)
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=${FFMPEG:-/home/williamdownard/openclaw-sites/bin/ffmpeg}
NARR=../audio-n/narration_voice_only.wav
MODE=${1:-slice}; mkdir -p out
case "$MODE" in
  slice) CUTS=${2:-../scenes/slice/cuts.json}; NAME=norse_slice; export SLICE_END=155.0 SLICE_TAIL=0;;
  full)  CUTS=${2:-../scenes/full/cuts.json};  NAME=norse_full
         export SLICE_END=${FULL_END:?set FULL_END=<last beat end seconds, from beats_timing.json>} SLICE_TAIL=${SLICE_TAIL:-1.5};;
  *) echo "usage: render.sh slice|full [cuts.json]" >&2; exit 64;;
esac
export SLICE_NAME=$NAME
node slice.js prep "$CUTS"
SFR=$(node -p "require('./src/slice_timeline.json').total")
DUR=$(node -p "($SFR/30).toFixed(3)")
npx remotion render src/index.ts Slice out/${NAME}_540p_silent.mp4 --scale=0.5 --codec=h264 --crf=20 --muted --concurrency="${CONC:-8}" --log=warn
"$FFMPEG" -y -loglevel error -i out/${NAME}_540p_silent.mp4 -i "$NARR" -map 0:v -map 1:a -c:v copy \
  -af "atrim=end=$SLICE_END,afade=t=out:st=$(node -p "($SLICE_END-0.5).toFixed(3)"):d=0.5,apad" -t "$DUR" -c:a aac -b:a 160k -movflags +faststart out/${NAME}_540p.mp4
echo "wrote out/${NAME}_540p.mp4 (${DUR}s)"
NAME=$NAME ~/.venvs/refwatch/bin/python full_sheets.py
