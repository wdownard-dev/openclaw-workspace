import json, os
STYLE = open('../video2/tests/stickfig/prompts/STYLE.txt').read().strip()
TAIL = " Thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels."
C = {}
C['odysseus'] = "Odysseus, a small human man: round cream face, two small black dot eyes and no nose, short brown hair, short brown beard, a gold laurel wreath on his head, bare-headed otherwise (no helmet), a deep blue tunic with a gold belt and a gold Greek meander pattern along the hem, a red cloak pinned at one shoulder with a gold brooch, leather sandals with straps up the calves, a short sword at his hip."
POLY = "Polyphemus, a huge muscular giant with one single large eye centred in the middle of his forehead (exactly one eye, no other eyes), shaggy brown hair and shaggy brown beard, a patched wool mantle draped over one shoulder with the other shoulder and chest bare, holding a tall wooden shepherd's crook, huge bare feet."
C['polyphemus'] = POLY
BL = "Polyphemus, a huge muscular giant, shaggy brown hair and shaggy brown beard, a patched wool mantle draped over one shoulder with the other shoulder and chest bare, holding a tall wooden shepherd's crook, huge bare feet. He has been blinded: the single eye in the middle of his forehead is a closed, dark, scarred hollow (exactly one scarred socket, no open eyes anywhere)."
C['polyphemus_blinded'] = BL
C['crewman'] = "a Greek sailor crewman, a small human man: round cream face, two small black dot eyes and no nose, a plain grey-brown tunic, a rope belt, a cloth headband, brown hair, leather sandals."
C['crewman_b'] = "a Greek sailor crewman, a small human man: round cream face, two small black dot eyes and no nose, a plain grey-brown tunic, a rope belt, a cloth headband, short curly brown hair and a stubble beard, a stocky build, leather sandals."
C['crewman_c'] = "an older Greek sailor crewman, a small human man: round cream face, two small black dot eyes and no nose, a plain grey-brown tunic, a rope belt, a cloth headband, thinning grey hair and a long grey beard, slightly stooped, leather sandals."
EXP = ["neutral","determined","sly smile","alarmed","shouting","exhausted"]
EXPP = ["neutral","suspicious","drunk-happy","roaring","pained","tender"]
WARD = {'odysseus':"the costume pieces of Odysseus laid out separately and neatly spaced, no body or person wearing them: a gold laurel wreath, a deep blue tunic with gold meander hem, a red cloak with gold brooch, a gold belt, a short sword in its scabbard, a pair of strapped leather sandals. ",
 'polyphemus':"the costume pieces of Polyphemus laid out separately and neatly spaced, no body or person wearing them: a patched wool mantle, a tall wooden shepherd's crook, a thick rope belt. ",
 'crewman':"the costume pieces of a sailor crewman laid out separately and neatly spaced, no body or person wearing them: a plain grey-brown tunic, a cloth headband, a rope belt, a pair of leather sandals. "}
P = {}
def add(i,out,prompt,size,ref=None): P[i]=(out,STYLE+" "+prompt+TAIL,size,ref)
for k,d in C.items():
    ff = k.startswith('polyphemus')
    base = f"characters/{k}/"
    add(f"{k}_turn", base+"turnaround.png", f"Character model sheet turnaround, three views of the same character: front view, three-quarter view and back view side by side, same height, full body, all feet on one shared baseline, even spacing. The character: {d}", "1536x1024")
    if k in ('crewman_b','crewman_c'): continue
    add(f"{k}_face", base+"face.png", f"Head and shoulders close-up portrait, neutral expression, facing front. The character: {d}", "1024x1024", base+"turnaround.png")
    ex = EXPP if ff else EXP
    add(f"{k}_expr", base+"expressions.png", f"Expression sheet: exactly six heads in a single row, evenly spaced, same character same size, expressions left to right: {', '.join(ex)}. The character: {d}", "1536x1024", base+"turnaround.png")
    add(f"{k}_sil", base+"silhouette.png", f"A solid flat dark ink-black body silhouette of the character, front view, full body, filled completely black with no inner detail, standing on plain cream. The character: {d}", "1024x1024", base+"turnaround.png")
    wk = 'polyphemus' if ff else ('crewman' if k=='crewman' else k)
    if k!='polyphemus_blinded':
        add(f"{k}_ward", base+"wardrobe.png", WARD[wk], "1536x1024", base+"turnaround.png")
add("polyphemus_blinded_band", "characters/polyphemus_blinded/turnaround_band.png", "Character model sheet turnaround, three views of the same character: front, three-quarter and back, same height, full body, feet on one baseline. The character: "+BL.replace("is a closed, dark, scarred hollow","is covered by a cloth band wrapped across his forehead and eye")+" The cloth band is a pale strip of linen tied around his head across the eye.", "1536x1024", "characters/polyphemus_blinded/turnaround.png")
def pl(i,folder,name,prompt):
    P[i]=(f"places/{folder}/{name}.png",STYLE+" "+prompt+" No people, no characters. No text, no labels, no watermark.","1536x1024",None)
EXT="A sea cliff coast: tall sandstone cliff with a dark cave mouth in its face, a huge round grey boulder resting beside the cave mouth, blue Aegean sea below, rocky ground in front of the cave. "
pl("ext_day","cave_exterior","day_wide",EXT+"Wide establishing view, bright midday sun, clear sky.")
pl("ext_dusk","cave_exterior","dusk_wide",EXT+"Wide establishing view at dusk, orange and purple sky, long shadows.")
pl("ext_night","cave_exterior","night_wide",EXT+"Wide establishing view at night, full moon, deep blue light, faint firelight glowing from the cave mouth.")
pl("ext_sealed","cave_exterior","boulder_sealing_mouth",EXT.replace("a huge round grey boulder resting beside the cave mouth","the huge round grey boulder now rolled across the cave mouth and completely sealing it")+"Wide view at dusk.")
INT="Inside a huge rough stone cave: "
pl("int_day","cave_interior","day_shaft_of_light",INT+"wooden racks of round cheeses, woven lamb pens, a stone fire pit with cold ashes, and the huge round boulder sealing the entrance at the back. A single shaft of daylight falls from a hole in the ceiling. Wide view.")
pl("int_night","cave_interior","night_firelight",INT+"wooden racks of round cheeses, woven lamb pens, a stone fire pit with a big blazing fire, and the huge round boulder sealing the entrance at the back. Lit only by warm firelight, dark shadows. Wide view.")
pl("int_boulder","cave_interior","sealed_boulder_from_inside","Close view from inside a cave looking at the huge round grey boulder sealing the cave entrance, thin cracks of light around its edges, rough stone walls, firelight glow on the left.")
pl("int_cheese","cave_interior","cheese_racks_and_pens","Close detail view inside a cave: wooden racks stacked with round cheeses, woven pens of lambs behind them, clay milk pails on the floor, warm light.")
pl("beach_morning","beach_and_ship","morning","A wide beach below tall sandstone cliffs in morning light, a Greek wooden ship with a single mast and furled sail beached on the sand, oars stacked, calm sea, soft pink-gold sky.")
pl("beach_sea","beach_and_ship","ship_at_sea_wide","A Greek wooden ship with a striped sail and oars, sailing on open deep blue Aegean sea, wide view, cliffs far behind, no crew visible, bright day.")
pl("hill_dusk","hillside_pasture","dusk","A grassy hillside pasture at dusk with a flock of white sheep grazing, a worn dirt path with huge footprints winding up the hill to a cave mouth in a cliff at the top, warm orange sky, sea in the distance.")
def pr(i,name,prompt): P[i]=(f"props/{name}.png",STYLE+" "+prompt+TAIL,"1024x1024",None)
pr("boulder","boulder","A single huge round grey boulder, a big rock of cave-door size, standing alone on cream.")
pr("stake","stake","Three sharpened wooden stake pieces laid out on cream, side by side, no hands: a raw olive trunk, the same trunk sharpened to a point, and the sharpened trunk with a glowing red-orange fire-hardened tip.")
pr("wine","wine","A dark goatskin wine bag with a tied neck, beside a shallow clay drinking bowl filled with dark red wine, on cream.")
pr("ram","ram","A big woolly ram with huge curled horns, thick shaggy cream fleece hanging low to its knees, full body side view, standing on cream.")
os.makedirs('prompts',exist_ok=True)
jobs1=[];jobs2=[]
for i,(out,p,size,ref) in P.items():
    open(f'prompts/{i}.txt','w').write(p)
    j=dict(id=i,out=out,prompt_file=f'prompts/{i}.txt',size=size,refs=[ref] if ref else [])
    (jobs2 if ref else jobs1).append(j)
json.dump(jobs1,open('jobs1.json','w'));json.dump(jobs2,open('jobs2.json','w'))
print(len(jobs1),len(jobs2))
