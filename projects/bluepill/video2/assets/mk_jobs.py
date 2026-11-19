#!/usr/bin/env python3
"""Write prompt files + a jobs JSON for gen.py batch.
  mk_jobs.py masters                      -> jobs_masters.json (cyc2 master edit, empedocles + thucydides generations)
  mk_jobs.py pose <char> <pose> <attempt> [prev_white.png] -> prints a single job (stdout) and writes the prompt
  mk_jobs.py props [names...]             -> jobs_props.json
  mk_jobs.py plates [ids...]              -> jobs_plates.json
  mk_jobs.py maps                         -> jobs_maps.json
"""
import sys, json, os
from prompts_def import *
G = f'{A}/gen'
REFSTY = {'cy': f'{ROOT}/tests/stress_test/refs/cy_v4_flat.png', 'ody': f'{ROOT}/tests/stress_test/refs/odysseus_A_flat.png',
          'land': f'{ROOT}/video1/refs/sty_land.png', 'stone': f'{ROOT}/video1/refs/sty_stone.png', 'cave': f'{ROOT}/video1/refs/sty_cave.png'}

def job(cid, prompt, refs=(), size='1024x1024'):
    return dict(id=cid, out=f'{G}/{cid}.png', prompt_file=write(cid, prompt), refs=list(refs), size=size)

def pose_job(char, pose, attempt, prev=None, text=None):
    text = text or (MASTER_POSE[char] if pose == 'neutral' else dict(POSES[char])[pose])
    refs = [MASTER[char]] + ([prev] if prev else [])
    return job(f'{char}__{pose}__a{attempt}', sprite_prompt(char, text, prev=bool(prev)), refs)

cmd = sys.argv[1]
if cmd == 'masters':
    jobs = []
    # CYC2 master: one edit call from the Polyphemus master (G2: a recolour with a different eye shape, same species design)
    p = (f"Image 1 is the character design of {bm.CY} Redraw this SAME species design as a DIFFERENT individual of his people, keeping the drawing style, "
         "proportions of the body parts, the hide kilt and the plain rope belt with nothing hanging from it, but change only these things: the skin a cooler grey-olive tone, "
         "the hair short and cropped and grey, the beard short, trimmed and grey, a brown leather smith's apron worn over the kilt instead of the sheepskin wrap, "
         "a more symmetric build with two ordinary matching arms, bare feet, and the one eye a narrower half-lidded almond shape with a bored expression. "
         "He still has exactly ONE eye in the centre of his forehead and no other eyes.\n\n"
         f"SCENE: The character alone, full body with both feet visible, standing with arms loose at the sides, body turned a little toward the viewer's right, "
         f"on a plain pure white background with nothing else in the frame, {bm.INLINE_FLAT}.\n\n{SPRITE_KEEP}\n\n{bm.STYLE_ORIG}")
    jobs.append(job('cyc2__neutral__a1', p, [MASTER['polyphemus']]))
    jobs.append(job('empedocles__neutral__a1', newchar_prompt(EMPED, MASTER_POSE['empedocles'])))
    jobs.append(job('thucydides__neutral__a1', newchar_prompt(THUC, MASTER_POSE['thucydides'])))
    json.dump(jobs, open(f'{A}/jobs_masters.json', 'w'), indent=1); print(len(jobs))
elif cmd == 'pose':
    char, pose, att = sys.argv[2], sys.argv[3], int(sys.argv[4]); prev = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != '-' else None
    print(json.dumps(pose_job(char, pose, att, prev)))
elif cmd == 'props':
    names = sys.argv[2:] or list(PROPS)
    jobs = [job(f'prop__{n}__a1', prop_prompt(PROPS[n])) for n in names]
    json.dump(jobs, open(f'{A}/jobs_props.json', 'w'), indent=1); print(len(jobs))
elif cmd == 'plates':
    ids = sys.argv[2:] or list(PLATES)
    jobs = []
    for i in ids:
        d = PLATES[i]; refs = [REFSTY.get(r, r) for r in d['refs']]
        rp = [r if r in ('cy', 'ody', 'land', 'stone', 'cave') else 'a finished scene plate from this episode: reuse its layout, palette and drawing language as the base' for r in d['refs']]
        if i == 'board_base':
            p = f"SCENE: {d['scene']}\n\n{bm.FLAT} {bm.KEEP_BG}\n\n{bm.STYLE_NP}"
        else:
            p = bm.prompt_t0(rp, d['scene'])
            if not refs or not any(r in ('cy', 'ody') for r in d['refs']):
                p = p.replace(bm.KEEP_T0, bm.KEEP_BG)
        jobs.append(job(i + '__a1', p, refs, '1536x864'))
    json.dump(jobs, open(f'{A}/jobs_plates.json', 'w'), indent=1); print(len(jobs))
elif cmd == 'maps':
    jobs = [job(f'{m}__a1', map_prompt(MAPS[m]), [], '1536x864') for m in MAPS]
    json.dump(jobs, open(f'{A}/jobs_maps.json', 'w'), indent=1); print(len(jobs))
