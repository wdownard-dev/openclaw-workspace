import os, subprocess, json
from prompts_def import *
G = f'{A}/gen'
SHARP = f'{ROOT}/pipeline/node_modules/sharp'
def job(cid, prompt, refs=(), size='1024x1024'):
    return dict(id=cid, out=f'{G}/{cid}.png', prompt_file=write(cid, prompt), refs=list(refs), size=size)
def pose_job(char, pose, attempt, prev=None, text=None):
    text = text or (MASTER_POSE[char] if pose == 'neutral' else dict(POSES[char])[pose])
    refs = [MASTER[char]] + ([prev] if prev else [])
    if os.environ.get('VARIANT') == '2':
        return job(f'{char}__{pose}__a{attempt}', sprite_prompt_v2(char, text), [MASTER[char]])
    return job(f'{char}__{pose}__a{attempt}', sprite_prompt(char, text, prev=bool(prev)), refs)
def flatten_white(png):
    """Return a path to an opaque on-white copy (edits refs with alpha are fine, but white keeps the 'on white' framing consistent)."""
    out = png.replace('.png', '_white.png')
    if not os.path.exists(out):
        subprocess.run(['node', '-e', f"require('{SHARP}')('{png}').flatten({{background:'#ffffff'}}).png().toFile('{out}').then(()=>{{}})"], check=True)
    return out
