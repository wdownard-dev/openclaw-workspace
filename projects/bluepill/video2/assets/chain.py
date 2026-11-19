#!/usr/bin/env python3
"""Sequential pose chain for one character: chain.py <char> <prev_white_or_-> <pose[:attempt]> ...
Each call uses refs = master + previous pose output on white (the chain's last output, or the given start). Outputs gen/<char>__<pose>__a<n>.png."""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from mk_jobs_lib import pose_job, flatten_white
char, prev = sys.argv[1], (None if sys.argv[2] == '-' else sys.argv[2])
for spec in sys.argv[3:]:
    pose, att = (spec.split(':') + ['1'])[:2]
    j = pose_job(char, pose, int(att), prev)
    r = gen.run(j['id'], j['out'], j['prompt_file'], j['refs'], j['size'])
    if r != 'ok': print('chain stop', char, pose, r); break
    prev = flatten_white(j['out'])
