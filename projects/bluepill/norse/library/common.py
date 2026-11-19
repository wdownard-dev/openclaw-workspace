import os
HERE=os.path.dirname(os.path.abspath(__file__))
STYLE=open('/home/williamdownard/.openclaw/workspace/projects/bluepill/video2/tests/stickfig/prompts/STYLE.txt').read().strip()
TAIL=" Thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels."
TURN="Character model sheet turnaround, two views of the same character: front view and three-quarter view side by side, same height, full body, all feet on one shared baseline, even spacing. The character: "
FACE="Head and shoulders close-up portrait, neutral expression, facing front, large and clear. The character: "
SIMPLE="Character card art, a single full-body front view, centred, feet on a baseline. The character: "
def P(body,desc): return STYLE+" "+body+desc+TAIL
def wp(cid,text):
    p=f'{HERE}/prompts/{cid}.txt'; open(p,'w').write(text); return p
