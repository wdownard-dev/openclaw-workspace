#!/bin/bash
cd "$(dirname "$0")"
python3 -u gen.py batch jobs_props.json > logs/props.log 2>&1
python3 -u gen.py batch jobs_maps.json > logs/maps.log 2>&1
