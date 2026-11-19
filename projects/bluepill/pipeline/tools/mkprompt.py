#!/usr/bin/env python3
"""usage: mkprompt.py <char> <style A-D> <out.txt> [style_ref_note: 0/1]"""
import json, sys
R='/home/williamdownard/.openclaw/workspace/projects/bluepill/tests/chars_v3/prompts/'
ch, st, out = sys.argv[1:4]
anchor = len(sys.argv) > 4 and sys.argv[4] == '1'
S = json.load(open(R+'styles.json'))[st]; C = json.load(open(R+'chars.json'))[ch]
if anchor:
    pre = "Image 1 is the style anchor: another character of the same cast. Draw this NEW character in exactly the same art style, line treatment, shading, palette and level of finish as Image 1, but with its own design. "
    C = C.split(' Identity cues')[0]
else:
    pre = ""
t = (pre + "Single full-body character, standing in a neutral relaxed pose with arms slightly away from the body so the limbs are clearly separated, whole figure visible from head to feet, centred, on a plain flat pure white background, no ground, no shadow on the floor, no text, no letters, no watermark, no frame, nothing else in the image. " + C + " " + S)
open(out,'w').write(t)
