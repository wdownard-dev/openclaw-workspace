#!/usr/bin/env bash
# Blue Pill v1 renderer. usage: bash render.sh animatic | final | mux-only
#   animatic: 960x540 silent picture via Remotion (--scale=0.5), then the narration muxed with the full ffmpeg -> out/animatic_540p.mp4
#   final:    1920x1080 -> out/video1_1080p.mp4 (same chain, crf 19)
# Picture is rendered silent; audio is muxed outside Remotion (FORMAT-BIBLE section 7: mix in full ffmpeg). Voice only, loudness left as delivered (-19 LUFS).
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=${FFMPEG:-/home/williamdownard/openclaw-sites/bin/ffmpeg}
NARR=../audio/narration_voice_only.wav
MODE=${1:-animatic}
CONC=${CONC:-11}
mkdir -p out
node resolve.js
if [ "$MODE" = animatic ]; then
  SILENT=out/animatic_540p_silent.mp4; OUT=out/animatic_540p.mp4; SCALE=0.5; CRF=20
elif [ "$MODE" = final ]; then
  SILENT=out/video1_1080p_silent.mp4; OUT=out/video1_1080p.mp4; SCALE=1; CRF=19
else
  SILENT=out/animatic_540p_silent.mp4; OUT=out/animatic_540p.mp4
fi
if [ "$MODE" != mux-only ]; then
  date +%s > out/render.start
  npx remotion render src/index.ts BluePill "$SILENT" --scale="$SCALE" --codec=h264 --crf="$CRF" --muted --concurrency="$CONC" --log=warn 2>&1 | tee out/render.log | grep -v '^\s*$' | tail -3
  date +%s > out/render.end
fi
# mux: copy the picture, AAC voice, stop at the shorter stream (video 641.76 s, narration 642.56 s)
"$FFMPEG" -y -loglevel error -i "$SILENT" -i "$NARR" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "wrote $OUT"; ls -la "$OUT"
