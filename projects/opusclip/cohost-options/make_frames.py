#!/usr/bin/env python
"""Render every character's transparent mouth/blink PNG set into ./<slug>/ (600x600 RGBA).
Usage: tts-venv/bin/python make_frames.py [slug ...]   (no args = all six)"""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "chars"))
from lib import save_set
ALL = ["volt", "quarter", "wisp", "null", "rascal", "orb"]
for s in (sys.argv[1:] or ALL):
    save_set(importlib.import_module(s), os.path.join(HERE, s))
    print("frames:", s)
