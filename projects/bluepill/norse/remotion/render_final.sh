#!/usr/bin/env bash
# Stage 8: silent 1080p + 540p renders of the current cut (muxing done separately with the final mix)
set -euo pipefail
cd "$(dirname "$0")"
export SLICE_NAME=norse_full SLICE_END=615.344 SLICE_TAIL=1.5
node slice.js prep ../scenes/full/cuts.json
node -p "require('./src/slice_timeline.json').total" > out/final_total_frames.txt
date +%s > out/final_start.txt
if [ "${RESUME:-0}" != 1 ] || [ ! -s out/final_1080_silent.mp4 ]; then
  npx remotion render src/index.ts Slice out/final_1080_silent.mp4 --scale=1 --codec=h264 --crf=16 --muted --concurrency="${CONC:-8}" --log=warn
fi
date +%s > out/final_1080_end.txt
if [ "${RESUME:-0}" != 1 ] || [ ! -s out/final_540_silent.mp4 ]; then
  npx remotion render src/index.ts Slice out/final_540_silent.mp4 --scale=0.5 --codec=h264 --crf=18 --muted --concurrency="${CONC:-8}" --log=warn
fi
date +%s > out/final_end.txt
echo done > out/final_done.txt
