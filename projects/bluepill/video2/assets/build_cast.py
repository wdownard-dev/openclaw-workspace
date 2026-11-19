#!/usr/bin/env python3
"""Builds sprites/<char>.cast.json from the accepted sprites and their sidecars, writes the storyboard alias copies
(names the storyboard uses for merged poses) and the code-filled silhouettes. Run after all sprite batches."""
import os, json, glob, csv, subprocess, time
A = os.path.dirname(os.path.abspath(__file__)); S = f'{A}/sprites'
SHARP = '/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp'
IMMUTABLE = {
 'odysseus': ['gold laurel wreath', 'blue sash over one shoulder with gold brooch', 'dark beard', 'rust-red tunic with gold hem'],
 'polyphemus': ['exactly one eye', 'no bells, nothing hanging from the rope belt', 'plain twisted rope belt', 'olive-brown skin, sheepskin wrap, hide kilt'],
 'cyc2': ['exactly one eye', 'no bells, nothing hanging from the rope belt', 'leather smith apron', 'grey cropped hair and short grey beard'],
 'crew': ['slate-blue sleeveless tunic', 'brown chest strap', 'rope belt', 'bare-headed, no weapon'],
 'empedocles': ['bald crown, long grey beard', 'cream himation', 'no wreath, no sash, no red'],
 'thucydides': ['close-cropped dark hair, short dark beard', 'grey himation', 'no wreath, no sash, no red'],
}
PALETTE = {
 'odysseus': {'tunic': '#b5432a', 'sash': '#2f5fa8', 'gold': '#e8b43a', 'skin': '#f1c9a0', 'ink': '#3a2412'},
 'polyphemus': {'skin': '#8e8a5a', 'hide': '#6b4a2b', 'rope': '#d8c08a', 'ink': '#3a2412'},
 'cyc2': {'skin': '#8b8c70', 'apron': '#7a4a27', 'rope': '#d8c08a', 'ink': '#3a2412'},
 'crew': {'tunic': '#5a6f86', 'strap': '#7a4a27', 'skin': '#f1c9a0', 'ink': '#3a2412'},
 'empedocles': {'himation': '#efe6d2', 'skin': '#f1c9a0', 'ink': '#3a2412'},
 'thucydides': {'himation': '#6b6b70', 'tunic': '#efe6d2', 'ink': '#3a2412'},
}
TAGS = {  # pose -> (emotion, hands, props)
 'neutral': ('calm', 'at sides', ''), 'point': ('urgent', 'pointing', ''), 'walk': ('determined', 'swinging', 'wineskin'),
 'talk': ('explaining', 'open', ''), 'shrug': ('puzzled', 'palms out', ''), 'think': ('thinking', 'chin', ''), 'flat': ('unimpressed', 'at sides', ''),
 'smug': ('smug', 'folded', ''), 'armscrossed': ('impatient', 'folded', ''), 'sworddraw': ('tense', 'on hilt', 'short sword'),
 'swordlower': ('deflated', 'holding', 'short sword'), 'offerbowl': ('deadpan', 'holding', 'bowl'), 'tiptoe': ('shouting', 'cupped', ''),
 'lookup': ('awed', 'hanging', ''), 'wave': ('shy', 'raised', ''), 'leandown': ('curious', 'on knees', ''), 'scorn': ('scornful', 'flicking', ''),
 'beam': ('tipsy', 'holding', 'bowl'), 'tender': ('tender', 'patting', ''), 'armswide': ('pleading', 'wide', ''), 'wounded': ('hurt', 'on chest', ''),
 'plead': ('pleading', 'clasped', 'sweat drop'), 'torch': ('wary', 'holding', 'torch'), 'alarmed': ('alarmed', 'up', ''),
 'back': ('dismissive', 'waving', ''), 'smith_hammer': ('intent', 'raised', 'hammer'), 'smith_tongs': ('working', 'holding', 'tongs'),
 'smith_flat': ('flat', 'hanging', 'hammer'), 'palmsup': ('uncertain', 'palms up', ''), 'silhouette': ('none', '', ''),
}
ALIASES = {  # storyboard name -> accepted pose file (renderer mirrors/tints where the storyboard says so)
 'odysseus__handsopen__a': 'odysseus__talk__a', 'odysseus__unamused__a': 'odysseus__flat__a', 'odysseus__smug_sideeye__a': 'odysseus__smug__a',
 'odysseus__tired_helm__a': 'odysseus__neutral__a', 'polyphemus__drunk__a': 'polyphemus__beam__a', 'polyphemus__lovesick__a': 'polyphemus__tender__a',
 'polyphemus__shrug__a': 'polyphemus__armswide__a', 'polyphemus__lamb_wave__a': 'polyphemus__wave__a',
 'crew__worried__a': 'crew__plead__a', 'crew__squint__a': 'crew__lookup__a', 'crew__torch_wave__a': 'crew__torch__a', 'crew__magnifier__a': 'crew__lookup__a',
 'cyc2__smith_hat_tip__a': 'cyc2__shrug__a', 'cyc2__trio_backs__a': 'cyc2__back__a', 'cyc2__trio_leaving__a': 'cyc2__back__a',
 'cyc2__smiths_trio_hammers_up__a': 'cyc2__smith_hammer__a', 'cyc2__smiths_trio_stare__a': 'cyc2__smith_tongs__a',
}
SILHOUETTES = {'polyphemus__silhouette__a': 'polyphemus__neutral__a', 'cyc2__trio_silhouette__a': 'cyc2__neutral__a'}

spend = {r['call_id']: r for r in csv.DictReader(open(f'{A}/SPEND.csv'))} if os.path.exists(f'{A}/SPEND.csv') else {}
today = time.strftime('%Y-%m-%d')
cast = {}
for p in sorted(glob.glob(f'{S}/*__*__a.png')):
    name = os.path.basename(p)[:-4]; char, pose, var = name.split('__')
    side = json.load(open(p[:-4] + '.json')) if os.path.exists(p[:-4] + '.json') else {}
    src = os.path.basename(side.get('source', ''))
    call = next((k for k in spend if src.startswith(k)), None)
    e = TAGS.get(pose, ('', '', ''))
    cast.setdefault(char, {'character': char, 'palette': PALETTE.get(char, {}), 'immutable_features': IMMUTABLE.get(char, []), 'master': f'{char}__neutral__a.png', 'poses': []})
    cast[char]['poses'].append({'file': os.path.basename(p), 'pose': pose, 'variant': var, 'facing': 'right' if pose != 'back' else 'away',
        'emotion': e[0], 'hands': e[1], 'props': e[2], 'width': side.get('width'), 'height': side.get('height'), 'feet': side.get('feet'),
        'height_px_at_1080': side.get('height_px_at_1080'), 'accepted': today, 'source_call': call or ('no-spend reuse: ' + src)})
for char, c in cast.items():
    c['aliases'] = {k: v + '.png' for k, v in ALIASES.items() if k.startswith(char + '__')}
    json.dump(c, open(f'{S}/{char}.cast.json', 'w'), indent=1)
    print(char, len(c['poses']), 'poses')
# alias copies (so the storyboard's src names resolve) and silhouettes
import shutil
for k, v in ALIASES.items():
    if os.path.exists(f'{S}/{v}.png'):
        shutil.copy(f'{S}/{v}.png', f'{S}/{k}.png'); shutil.copy(f'{S}/{v}.json', f'{S}/{k}.json')
for k, v in SILHOUETTES.items():
    if os.path.exists(f'{S}/{v}.png'):
        subprocess.run(['node', '-e', f"""const s=require('{SHARP}');s('{S}/{v}.png').ensureAlpha().raw().toBuffer({{resolveWithObject:true}}).then(({{data,info}})=>{{for(let p=0;p<info.width*info.height;p++){{data[p*4]=26;data[p*4+1]=18;data[p*4+2]=4}}return s(data,{{raw:{{width:info.width,height:info.height,channels:4}}}}).png().toFile('{S}/{k}.png')}})"""], check=True)
        shutil.copy(f'{S}/{v}.json', f'{S}/{k}.json')
print('aliases + silhouettes written')
