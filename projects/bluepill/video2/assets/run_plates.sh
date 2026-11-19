#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f run_r4.sh >/dev/null; do sleep 5; done
python3 -u gen.py batch jobs_plates.json > logs/plates.log 2>&1
