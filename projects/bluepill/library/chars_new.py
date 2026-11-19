import json, os
STYLE=open('../video2/tests/stickfig/prompts/STYLE.txt').read().strip()
TAIL=" Thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels."
EXP=["neutral","determined","sly smile","alarmed"]
C={
'neighbour_cyclops':"three DIFFERENT neighbouring Cyclops giants, each a huge muscular one-eyed giant with exactly ONE large eye centred in the middle of the forehead and no other eyes, each noticeably SMALLER than Polyphemus but still giants, a ragged hide kilt, bare feet. Giant 1: grey-green hide skin, long black braided hair, scruffy black beard. Giant 2: ochre-yellow hide skin, short bristly red hair, no beard, bald patch. Giant 3: pale blue-grey hide skin, long white unkempt hair and white beard, hunched",
'bard':"a very old blind stick-figure bard, Homer: round cream face, eyes closed shown as two short curved lines (no open eyes), long white beard and white hair with a thin laurel band, a plain white tunic with a simple belt, holding a wooden lyre with a curved tortoise-shell body, leather sandals, slightly stooped",
'hesiod':"Hesiod the shepherd-poet, a human man: round cream face, two small black dot eyes and no nose, short brown beard, a wide-brimmed straw sun hat, a rough brown wool tunic, holding a rolled papyrus scroll in one hand and a plain shepherd's staff in the other, leather sandals",
'abel':"Abel, a 1914 scholar, a human man: round cream face, two small black dot eyes and no nose, round wire spectacles, neat brown moustache, a dark charcoal frock coat, white shirt and dark tie, holding a quill pen; for the turnaround he stands holding the quill, in the wardrobe/face views shown seated writing at a small wooden desk with an inkwell and papers",
'pausanias':"Pausanias, an ancient Greek traveller, a human man: round cream face, two small black dot eyes and no nose, short grey-brown beard, a wide-brimmed petasos sun hat, a dusty ochre travelling tunic and short cloak, a tall walking staff, a leather satchel on a strap, sturdy leather sandals",
'hackman':"Hackman, a 1904 scholar, a human man: round cream face, two small black dot eyes and no nose, a bushy sandy moustache, a brown waistcoat over a white shirt with rolled sleeves, dark trousers, carrying a tall wobbling pile of old books in both arms",
'sailor':"an ancient Greek sailor for the Abel story, a small human man, same sailor build as the crewman: round cream face, two small black dot eyes and no nose, a plain grey-brown tunic, a rope belt, a cloth headband, brown hair, leather sandals, holding a lit wooden torch with an orange flame in one hand",
'workers':"two variants of Bronze Age labourers hauling a heavy stone block, small human men with round cream faces, two small black dot eyes and no nose, bare chests and simple ochre loincloths, rope harnesses over the shoulders, leather-wrapped hands. Worker A: strong stocky build, shaved head. Worker B: lean, with a short black beard and a cloth head wrap. Each shown pulling on a rope, bending forward as if hauling",
'ram':"a big woolly ram, a four-legged animal, huge curled gold-brown horns, thick shaggy cream fleece hanging low to its knees, dark small hooves, a calm patient face, sturdy enough to carry a man clinging underneath it",
'polyphemus_blinded':"Polyphemus, blinded: a huge muscular giant, shaggy brown hair and shaggy brown beard, a patched wool mantle (cream wool with teal patches stitched in ochre thread) draped over one shoulder over a ragged red-orange hide kilt, the other shoulder and chest bare, holding a tall wooden shepherd's crook, huge bare feet. A pale linen cloth band is wrapped and tied around his head, covering the single eye in the middle of his forehead completely. NO EYE is drawn anywhere: no open eye, no pupil, no hollow, no scar visible; only the cloth band across the forehead",
}
SHEET={ # which sheets per character
 'neighbour_cyclops':"Character model sheet turnaround, three DIFFERENT giants standing side by side, each shown full body front view, same scale between them as listed, all feet on one shared baseline, even spacing. The characters: ",
 'workers':"Character model sheet, two labourer variants side by side, each shown full body in side view hauling a rope, then a front view of each below, feet on baselines. The characters: ",
}
STD="Character model sheet turnaround, three views of the same character: front view, three-quarter view and back view side by side, same height, full body, all feet on one shared baseline, even spacing. The character: "
def P(name,body,desc): return STYLE+" "+body+desc+TAIL
JOBS=[]
def add(cid,out,prompt,size,refs=()):
    os.makedirs('prompts',exist_ok=True); open(f'prompts/{cid}.txt','w').write(prompt)
    JOBS.append(dict(id=cid,out=out,prompt_file=f'prompts/{cid}.txt',size=size,refs=list(refs)))
for k,d in C.items():
    b=f'characters/{k}/'
    if k=='polyphemus_blinded':
        add('pb2_expr',b+'expressions.png',P(k,"Expression sheet: exactly six heads in a single row, evenly spaced, same character same size, expressions left to right: neutral, suspicious, drunk-happy, roaring, pained, tender. The cloth band covering the eye is visible in EVERY head and NO eye is drawn on any head. The character: ",d),'1536x1024',[b+'turnaround_band.png'])
        add('pb2_face',b+'face.png',P(k,"Head and shoulders close-up portrait, neutral expression, facing front, cloth band across the forehead covering the eye. The character: ",d),'1024x1024',[b+'turnaround_band.png'])
        continue
    if k=='ram':
        add('ram_turn',b+'turnaround.png',P(k,"Character model sheet: two views of the same animal, front view and side view, same size, all hooves on one shared baseline. The character: ",d),'1536x1024',['props/ram.png'])
    else:
        add(f'{k}_turn',b+'turnaround.png',P(k,SHEET.get(k,STD),d),'1536x1024')
    add(f'{k}_face',b+'face.png',P(k,"Head and shoulders close-up portrait, neutral expression, facing front. The character (if several variants are listed show the first one only): ",d),'1024x1024',[b+'turnaround.png'])
    add(f'{k}_expr',b+'expressions.png',P(k,"Expression sheet: exactly four heads in a single row, evenly spaced, same character same size (if several variants listed use the first one only), expressions left to right: neutral, determined, sly smile, alarmed. The character: ",d),'1536x1024',[b+'turnaround.png'])
json.dump(JOBS,open('jobs_chars_new.json','w'),indent=1)
print(len(JOBS))
