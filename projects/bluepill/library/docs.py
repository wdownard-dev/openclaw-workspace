import json, os, shutil, glob
STYLE_TAIL="Style (append to every prompt): the STYLE.txt block (video2/tests/stickfig/prompts/STYLE.txt) plus: thick dark ink outline, flat warm shading."
D={
'odysseus':"Odysseus, a small human man: round cream face, two small black dot eyes and no nose, short brown hair, short brown beard, a gold laurel wreath on his head, bare-headed otherwise (NO helmet), a deep blue tunic with a gold belt and a gold Greek meander pattern along the hem, a red cloak pinned at one shoulder with a gold brooch, leather sandals with straps up the calves, a short sword at his hip.",
'polyphemus':"Polyphemus, a huge muscular giant with one single large eye centred in the middle of his forehead (exactly one eye), shaggy brown hair and shaggy brown beard, a patched wool mantle (cream wool with teal patches stitched in ochre thread) draped over one shoulder over a ragged red-orange hide kilt, the other shoulder and chest bare, holding a tall wooden shepherd's crook, huge bare feet.",
'polyphemus_blinded':"Polyphemus, blinded: the same huge muscular giant (shaggy brown hair and beard, cream patched wool mantle over one shoulder, ragged red-orange hide kilt, tall wooden shepherd's crook, huge bare feet) but the single eye in the middle of his forehead is a closed, dark, scarred hollow with a puckered lid and a dark scar line (no open eye anywhere). Variant: the hollow is covered by a pale linen cloth band tied across the forehead.",
'crewman':"A Greek sailor crewman, a small human man: round cream face, two small black dot eyes and no nose, a plain grey-brown tunic, a rope belt, a cloth headband, brown hair, leather sandals. Variant B (turnaround_b): short curly brown hair, stubble beard, stocky build. Variant C (turnaround_c): older, thinning grey hair, long grey beard, slightly stooped. Same costume for all three."}
ROLES={'turnaround':"front / three-quarter / back, same height, feet on one baseline",'turnaround_band':"turnaround, eye covered by cloth band",'turnaround_b':"variant B turnaround",'turnaround_c':"variant C turnaround",'face':"head and shoulders, neutral",'expressions':"six heads in a row",'silhouette':"solid dark front silhouette (derived from turnaround front view)",'wardrobe':"costume pieces laid out separately",'sheet':"composed labelled model sheet"}
EXPR={'polyphemus':"neutral, suspicious, drunk-happy, roaring, pained, tender",'polyphemus_blinded':"neutral, suspicious, drunk-happy, roaring, pained, tender"}
for k,d in D.items():
    f=f'characters/{k}/'; files=sorted(os.path.basename(x) for x in glob.glob(f+'*') if x.endswith(('.png','.jpg')))
    man=[]
    for n in files:
        r=n.rsplit('.',1)[0]
        man.append(dict(file=n,role=r,canonical=(r in('turnaround','turnaround_b','turnaround_c','turnaround_band')) and n.endswith('.png')))
    json.dump(man,open(f+'manifest.json','w'),indent=1)
    open(f+'CHARACTER.md','w').write(f"# {k}\n\nPrompt-ready description (always include in text):\n\n> {d}\n\nExpression set: {EXPR.get(k,'neutral, determined, sly smile, alarmed, shouting, exhausted')}.\n\n{STYLE_TAIL} Plain flat cream background, no scenery, no text, no labels.\n\nCanonical reference: `turnaround.png` (pass this one when the character is present). "+("`turnaround_b.png` / `turnaround_c.png` for crew variety. " if k=='crewman' else "")+("`turnaround_band.png` for the cloth-band variant. " if k=='polyphemus_blinded' else "")+"\n\nFiles:\n"+"\n".join(f"- {n}: {ROLES.get(n.rsplit('.',1)[0],'')}" for n in files)+"\n")
PD={'cave_exterior':("A sea cliff coast: tall sandstone cliff with a dark cave mouth in its face, a huge round grey boulder resting beside the cave mouth, blue Aegean sea below, rocky ground in front.",'day_wide'),
'cave_interior':("Inside a huge rough stone cave: wooden racks of round cheeses, woven lamb pens, clay pails, a stone fire pit, and the huge round grey boulder sealing the entrance at the back.",'day_shaft_of_light'),
'beach_and_ship':("A wide beach below tall sandstone cliffs, a Greek wooden ship (single mast, painted prow eye, oars) beached on the sand; at sea the ship has a blue-and-cream striped sail.",'morning'),
'hillside_pasture':("A grassy hillside pasture with a flock of white sheep, a worn dirt path with huge footprints winding up to a cave mouth in the cliff above, sea in the distance.",'dusk')}
for k,(d,can) in PD.items():
    f=f'places/{k}/'; files=sorted(os.path.basename(x) for x in glob.glob(f+'*') if x.endswith(('.png','.jpg')))
    json.dump([dict(file=n,role=n.rsplit('.',1)[0],canonical=(n==can+'.png')) for n in files],open(f+'manifest.json','w'),indent=1)
    open(f+'PLACE.md','w').write(f"# {k}\n\nPrompt-ready description (always include in text):\n\n> {d}\n\nLighting/variant is named by the file. No characters appear in these images; add them from the character library.\n\nCanonical reference: `{can}.png`.\n\n"+"\n".join(f"- {n}" for n in files)+"\n")
PR={'boulder':"A single huge round grey boulder of cave-door size.",'stake':"Three stages of the olive stake: raw olive trunk, the same trunk sharpened to a point, the sharpened trunk with a glowing red-orange fire-hardened tip.",'wine':"A dark goatskin wine bag with a tied neck beside a shallow clay bowl of dark red wine.",'ram':"A big woolly ram with huge curled gold-brown horns and thick cream fleece hanging to its knees."}
json.dump([dict(file=k+'.png',role=k,canonical=True) for k in PR],open('props/manifest.json','w'),indent=1)
open('props/PROPS.md','w').write("# Props\n\nOne image each on plain cream; each is canonical.\n\n"+"\n".join(f"- `{k}.png`: {v}" for k,v in PR.items())+"\n")
# refs
os.makedirs('refs',exist_ok=True)
for x in glob.glob('refs/*'): os.remove(x)
n=0
for m in glob.glob('*/*/manifest.json')+['props/manifest.json']:
    folder=os.path.dirname(m); name=os.path.basename(folder) if not m.startswith('props') else 'props'
    for e in json.load(open(m)):
        if e['canonical']: shutil.copy(f"{folder}/{e['file']}",f"refs/{name}__{e['role']}.png"); n+=1
print(n)
