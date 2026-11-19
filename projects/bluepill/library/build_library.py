#!/usr/bin/env python3
"""Rebuilds sheets, manifests, MD docs, refs/ from the images on disk. Run from library/."""
import json, os, glob, shutil
from PIL import Image, ImageDraw, ImageFont
from chars_new import C as NEWC
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=lambda s: ImageFont.truetype(FB,s)
BG=(250,238,215)
STYLE_TAIL="Style (append to every prompt): the STYLE.txt block (video2/tests/stickfig/prompts/STYLE.txt) plus: thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels."
def fit(p,w,h):
    im=Image.open(p).convert('RGB'); im.thumbnail((w,h)); c=Image.new('RGB',(w,h),BG); c.paste(im,((w-im.width)//2,(h-im.height)//2)); return c
# ---------------- characters
OLD={'odysseus':"Odysseus, a small human man: round cream face, two small black dot eyes and no nose, short brown hair, short brown beard, a gold laurel wreath on his head, bare-headed otherwise (NO helmet), a deep blue tunic with a gold belt and a gold Greek meander pattern along the hem, a red cloak pinned at one shoulder with a gold brooch, leather sandals with straps up the calves, a short sword at his hip.",
'polyphemus':"Polyphemus, a huge muscular giant with one single large eye centred in the middle of his forehead (exactly one eye), shaggy brown hair and shaggy brown beard, a patched wool mantle (cream wool with teal patches stitched in ochre thread) draped over one shoulder over a ragged red-orange hide kilt, the other shoulder and chest bare, holding a tall wooden shepherd's crook, huge bare feet.",
'crewman':"A Greek sailor crewman, a small human man: round cream face, two small black dot eyes and no nose, a plain grey-brown tunic, a rope belt, a cloth headband, brown hair, leather sandals. Variant B (turnaround_b): short curly brown hair, stubble beard, stocky build. Variant C (turnaround_c): older, thinning grey hair, long grey beard, slightly stooped. Same costume for all three."}
BLIND="Polyphemus, blinded: the same huge muscular giant as `polyphemus` (shaggy brown hair and beard, cream patched wool mantle over one shoulder, ragged red-orange hide kilt, tall wooden shepherd's crook, huge bare feet) but a pale linen cloth band is tied around his head across the middle of his forehead, covering the eye completely. LOCKED CHOICE: the cloth band. No eye is ever drawn on him (no open eye, no hollow, no scar visible); the band is visible in every image."
V3={'sheep':"The Cyclops flock: adult sheep with thick rounded cream-white fleece in soft clumps outlined in dark ink, a small dark grey-brown face with dark drooping ears and two small dot eyes, short thin dark legs, dark hooves, a calm placid deadpan look; lambs are smaller with the same fleece and longer legs. Group image: a flock of six (five adults + a lamb) and three sheep tied in a row side by side with a rope looped round their bodies. Matches the sheep in places/cave_interior.",
'maron':"Maron, priest of Apollo (the vineyard flashback): a small human man, round cream face, two small black dot eyes and no nose, short white-grey beard, a wreath of ivy leaves, a long flowing cream-white robe with a purple band at the hem, a wooden walking staff (head height), a small gold sun brooch pinning the robe at one shoulder, leather sandals."}
DESC={**OLD,**NEWC,**V3,'polyphemus_blinded':BLIND}
NOTE={'sheep':"Files: turnaround (adult front/side/back + lamb side/front), group (flock of 6; three sheep tied in a row side by side), face (deadpan). Use group.png for the tied-in-threes staging (script beats 'three woolly sheep side by side, roped').",
'maron':"Appears small among the vines in places/vineyard_golden.",'neighbour_cyclops':"One sheet, three DIFFERENT one-eyed giants left to right: 1 grey-green hide, long black braids and black beard; 2 ochre hide, short bristly red hair, no beard; 3 pale blue-grey hide, long white hair and beard, hunched. All smaller than Polyphemus. Expressions sheet is a 3x4 grid (row per giant): neutral, angry, sly smile, alarmed.",
'workers':"v3: regenerated so all bare skin is one uniform pale cream matching the crew's skin (the earlier tan-body / pale-face version is in _superseded/v3). Two variants: A strong stocky shaved head; B lean, short black beard, cloth head wrap. Turnaround shows them hauling a block (side) and standing (front). Expressions: row per worker, neutral / straining / sly smile / exhausted.",
'ram':"Character-grade sheet of the ram that carries Odysseus (front + side) plus expressions.png: neutral, deadpan, straining, trotting (head close-ups). Derived from props/ram.png (same ram).",
'abel':"Wears the same dark frock coat in every image; the desk is added in the shot, not in the sheet.",
'polyphemus_blinded':"`turnaround_scarred_hollow.png` is an earlier option, kept for the record, NON-canonical: do not use it as a reference (it draws a hollow where the eye was)."}
CH={ # title, left column items, right column items
 'odysseus':("ODYSSEUS",['turnaround','expressions','wardrobe'],['face','silhouette']),
 'polyphemus':("POLYPHEMUS",['turnaround','expressions','wardrobe'],['face','silhouette']),
 'polyphemus_blinded':("POLYPHEMUS (BLINDED, CLOTH BAND)",['turnaround_band','expressions'],['face','silhouette']),
 'crewman':("CREWMAN",['turnaround','expressions','wardrobe'],['face','silhouette','turnaround_b','turnaround_c']),
}
for k in NEWC:
    if k=='polyphemus_blinded': continue
    CH[k]=(k.upper().replace('_',' '),['turnaround']+(['expressions'] if k not in('sheep','maron') else []),['face'])
CH['workers']=('WORKERS',['turnaround','expressions','expressions_b'],['face'])
CH['sheep']=('SHEEP',['turnaround','group'],['face'])
CH['maron']=('MARON',['turnaround'],['face'])
CH['odysseus']=("ODYSSEUS",['turnaround','turnaround_helmet','expressions','wardrobe'],['face','silhouette'])
LABEL={'expressions_b':'EXPRESSIONS  worker B','group':'FLOCK OF SIX + THREE TIED SIDE BY SIDE','turnaround_helmet':'HELMETED VARIANT (script: bronze crested helmet)','turnaround':'TURNAROUND','turnaround_band':'TURNAROUND  cloth band (canonical)','expressions':'EXPRESSIONS','wardrobe':'WARDROBE','face':'FACE','silhouette':'SILHOUETTE','turnaround_b':'VARIANT B  curly hair, stubble','turnaround_c':'VARIANT C  older, grey beard'}
ROLES={'expressions_b':'worker B expression heads (expressions.png is worker A)','group':"flock of six and three sheep tied side by side",'turnaround_helmet':"Odysseus with the bronze crested helmet the script names (derived from his turnaround)",'turnaround':"front / three-quarter / back, same height, feet on one baseline",'turnaround_band':"turnaround, eye covered by cloth band (CANONICAL for the blinded giant)",'turnaround_scarred_hollow':"earlier option, NON-canonical",'turnaround_b':"variant B turnaround",'turnaround_c':"variant C turnaround",'face':"head and shoulders, neutral",'expressions':"expression heads",'silhouette':"solid dark front silhouette (cut from the turnaround front view in code)",'wardrobe':"costume pieces laid out separately",'sheet':"composed labelled model sheet"}
def chars():
    for k,(title,left,right) in CH.items():
        d=f'characters/{k}/'
        left=[n for n in left if os.path.exists(d+n+'.png')]; right=[n for n in right if os.path.exists(d+n+'.png')]
        LW,LH,RW=1500,1000,900; pad=20; head=110; lab=44
        rh=lambda n:RW if n in('face','silhouette') else 600
        LH=1000 if k!='odysseus' else 800
        H=head+max(len(left)*(LH+lab+pad),sum(rh(n)+lab+pad for n in right))+pad
        S=Image.new('RGB',(LW+RW+3*pad,H),BG); dr=ImageDraw.Draw(S)
        dr.text((pad,20),title+'  -  model sheet',fill=(31,58,95),font=font(64)); y=head
        for n in left: dr.text((pad,y),LABEL[n],fill=(60,40,20),font=font(32)); S.paste(fit(d+n+'.png',LW,LH),(pad,y+lab)); y+=LH+lab+pad
        y=head
        for n in right: dr.text((LW+2*pad,y),LABEL[n],fill=(60,40,20),font=font(32)); S.paste(fit(d+n+'.png',RW,rh(n)),(LW+2*pad,y+lab)); y+=rh(n)+lab+pad
        S.save(d+'sheet.jpg',quality=88)
        files=sorted(os.path.basename(x) for x in glob.glob(d+'*') if x.endswith(('.png','.jpg')))
        CAN={'turnaround','turnaround_b','turnaround_c','group'} if k!='polyphemus_blinded' else {'turnaround_band'}
        man=[dict(file=n,role=n.rsplit('.',1)[0],canonical=(n.rsplit('.',1)[0] in CAN and n.endswith('.png')),**({'variant':True,'note':'NON-canonical: use only for helmet beats (script 329,448,551,588)'} if n=='turnaround_helmet.png' else {})) for n in files]
        json.dump(man,open(d+'manifest.json','w'),indent=1)
        can_name='turnaround_band.png' if k=='polyphemus_blinded' else 'turnaround.png'
        exp="neutral, suspicious, drunk-happy, roaring, pained, tender" if k.startswith('polyphemus') else ("neutral, deadpan, straining, trotting" if k=='ram' else "none (animal, deadpan face only)" if k=='sheep' else "none (face only)" if k=='maron' else "neutral, determined, sly smile, alarmed" if k in NEWC else "neutral, determined, sly smile, alarmed, shouting, exhausted")
        open(d+'CHARACTER.md','w').write(f"# {k}\n\nPrompt-ready description (always include in text):\n\n> {DESC[k]}\n\n"+(f"{NOTE[k]}\n\n" if k in NOTE else "")+f"Expression set: {exp}.\n\n{STYLE_TAIL}\n\nCanonical reference: `{can_name}` (pass this one when the character is present). "+("`turnaround_b.png` / `turnaround_c.png` for crew variety. " if k=='crewman' else "")+"\n\nFiles:\n"+"\n".join(f"- {n}: {ROLES.get(n.rsplit('.',1)[0],'')}" for n in files)+"\n")
# ---------------- places
PL={ # folder: (description, master, [(file,label,derived_from)])
 'cave_exterior':("A sea cliff coast: tall sandstone cliff with a dark cave mouth in its face, a huge round grey boulder resting against the cliff immediately to the LEFT of the mouth (as seen from outside; it rolls right to seal it), an olive tree overhanging at top right, blue Aegean sea below left, rocky ground in front.",'day_wide',[('day_wide','MASTER day',None),('wide_notched_peak','day with a notched mountain peak behind the cliff (mountain-throwing)','day_wide'),('dusk_wide','dusk (sky + light only)','day_wide'),('night_wide','night, moon, firelight in the mouth','day_wide'),('boulder_sealing_mouth','boulder rolled across the mouth (boulder only)','day_wide')]),
 'cave_interior':("Inside a huge rough stone cave: wooden cheese racks on the left, a woven lamb pen behind and another at the right, a basket with a striped cloth, a stone fire pit in the centre, the huge round grey boulder sealing the entrance at the back.",'night_firelight',[('night_firelight','MASTER night, firelight',None),('day_shaft_of_light','day: cold fire, shaft of light','night_firelight'),('boulder_aside_daylight','boulder rolled aside, daylight through the mouth','night_firelight'),('sealed_boulder_from_inside','sealed boulder close-up (crop/zoom of the master)','night_firelight')]),
 'beach_and_ship':("A wide beach below tall sandstone cliffs at morning, calm sea, soft pink-gold sky, an empty beach in the master; the ship (props/ship.png) is placed on it in the beached variant.",'morning',[('morning','MASTER morning, empty beach',None),('ship_beached','ship beached (same ship, sail furled)','morning'),('ship_at_sea_wide','ship at sea (same ship, sail up, oars out)','props/ship'),('ship_night_stars','ship at night under stars','ship_at_sea_wide'),('ship_dusk_violet','ship at dusk, violet sea','ship_at_sea_wide'),('harbour_dawn','ship leaving a harbour at dawn, line of cliffs','ship_at_sea_wide'),('shore_dusk_red','empty shore at dusk, blood-red sea and burning sky (silhouette)','morning')]),
 'forge_cave':("A smoky Bronze Age forge cave: rough stone cave, a huge stone anvil on a tree stump in the centre, a glowing orange forge hearth with bellows at right, hammers and tongs hung on the wall, a rack of glowing metal bars, sparks and thick smoke, red-orange forge glow. Place only; add the three Cyclopes from characters/neighbour_cyclops.",'master',[('master','MASTER forge cave',None)]),
'smithy':("A small ancient smith's workshop at night: stone and timber walls, forge hearth glowing, an anvil, hanging tools, a wooden water trough on a stand at front with an axe beside it, window with moonlight. Place only (axe-in-water simile; hot axe/tongs/trough prop in props/).",'master',[('master','MASTER smithy at night',None)]),
'tiryns_wall':("A Bronze Age Mycenaean fortress on a hill at noon: a cyclopean wall of giant rough sandstone blocks, a paved ramp up to a gate with a carved lion relief above the lintel, dry golden grass, olive trees, bright blue sky.",'master',[('master','MASTER noon',None),('lion_gate_golden','Lion Gate close, golden hour (derived; zoomed view, edge check n/a)','master'),('wall_sunset','wall at sunset','master')]),
'three_hilltops_night':("A moonlit night landscape: three rounded hills in a row, each with its own dark cave mouth and a faint warm glow inside, a full moon in a starry blue sky, ruined columns bottom left, sea glint behind. Place only; add the three giants from characters/neighbour_cyclops.",'master',[('master','MASTER moonlit',None),('thundercloud','thundercloud over the middle hill','master')]),
'vineyard_golden':("A Greek hillside vineyard at golden hour: terraced rows of vines with dark purple grapes on wooden stakes, a small stone shrine with a clay jar, olive trees, low gold light, distant sea. Maron (characters/maron) is added small among the vines.",'master',[('master','MASTER golden hour',None)]),
'library_lamplit':("A towering Victorian university library at night: floor-to-ceiling dark wood shelves of bound leather volumes, a rolling ladder, a brass reading lamp on a table, warm lamplight, blue-black shadows, arched window. Hackman's library; no figures.",'master',[('master','MASTER lamplit',None)]),
'library_ancient_empty':("An ancient stone library chamber: dressed sandstone walls, recessed wooden shelves, one wide EMPTY shelf in the centre with no scrolls, dust, cool light from a high window.",'master',[('master','MASTER empty shelf',None)]),
'study_1914':("A 1914 scholar's study (Abel): large wooden desk by a window with inkwell, quill, open papers, stacked books and a green-shaded lamp, bookcase, rug, warm evening light, dark panelled walls. Nobody seated: add Abel from characters/abel.",'master',[('master','MASTER study',None)]),
'sea_storm':("A night sea with a storm: a huge dark wave rising in the foreground, a towering black thunderhead lit by lightning, deep blue and black water with white foam, a few stars. No ship in the master; ship_in_storm adds the tiny ship.",'master',[('master','MASTER dark wave + thunderhead',None),('ship_in_storm','tiny ship speck in front of the storm','master')]),
'ship_deck':("The deck of the ancient Greek ship seen from the stern: wooden planks, gold meander stern rail, big steering oar, mast with furled blue-and-white striped sail, rowing benches, blue sea beyond. Empty deck; add Odysseus at the helm.",'master',[('master','MASTER bright morning',None),('dusk','dusk, dark sea, first star','master')]),
'hillside_pasture':("A grassy hillside pasture with a flock of white sheep, a worn dirt path with huge footprints winding up to a cave mouth in the cliff above, sea in the distance.",'dusk',[('dusk','MASTER dusk',None),('dawn','dawn (sky + light only)','dusk')]),
}
def places():
    for k,(desc,master,items) in PL.items():
        d=f'places/{k}/'; w,h=1200,800; cols=2 if len(items)>1 else 1; rows=(len(items)+cols-1)//cols
        S=Image.new('RGB',(cols*w+(cols+1)*20,110+rows*(h+64)),BG); dr=ImageDraw.Draw(S)
        dr.text((20,20),k.replace('_',' ').upper()+'  -  place sheet',fill=(31,58,95),font=font(60))
        for i,(n,l,_) in enumerate(items):
            x=20+(i%cols)*(w+20); y=110+(i//cols)*(h+64)
            dr.text((x,y),l.upper(),fill=(60,40,20),font=font(28)); S.paste(fit(d+n+'.png',w,h),(x,y+44))
        S.save(d+'sheet.jpg',quality=88)
        json.dump([dict(file=n+'.png',role=n,canonical=True,master=(n==master),derived_from=src) for n,l,src in items]+[dict(file='sheet.jpg',role='sheet',canonical=False)],open(d+'manifest.json','w'),indent=1)
        open(d+'PLACE.md','w').write(f"# {k}\n\nPrompt-ready description (always include in text):\n\n> {desc}\n\nMASTER: `{master}.png`. Every other image is DERIVED from the master (image edit, never regenerated from text), so rocks, plants, objects and layout are identical; only the named change differs. No characters appear in these images; add them from the character library.\n\nFiles:\n"+"\n".join(f"- {n}.png: {l}" for n,l,_ in items)+"\n- sheet.jpg: labelled composite\n")
# ---------------- props
PR=[('boulder',"The cave boulder: a huge round grey boulder of cave-door size. Derived from a crop of places/cave_exterior/day_wide.png (it IS the exterior boulder).",None),
('ship',"MASTER ship, side view, sail up: dark teal hull with a gold Greek meander band along the top, a row of seven round oar holes below it, carved curled prow with a painted eye, single mast, square sail with vertical deep-blue and white stripes.",None),
('ship_furled',"Same ship, sail furled: the stripes stay visible wrapped on the yard. Derived from ship.png.",'ship'),
('stake_raw',"Stake master: a raw olive trunk, flat-cut ends.",None),
('stake_sharp',"Stake state 2: the same trunk sharpened to a point. Derived from stake_raw.png.",'stake_raw'),
('stake_fire',"Stake state 3: the same trunk, sharpened, red-orange fire-hardened tip. Derived from stake_raw.png.",'stake_raw'),
('stake',"The three stake states stacked in one image (composited in code from stake_raw / stake_sharp / stake_fire).",'composite'),
('wine',"A dark goatskin wine bag with a tied neck beside a shallow clay bowl of dark red wine.",None),
('torch',"A wooden torch: rough shaft, pitch-soaked cloth head, bright orange flame (the Abel sailor's torch).",None),
('olive_club',"A rough gnarled olive-wood club with bark and a worn grip.",None),
('cheese_set',"Three big round pale-yellow cheese wheels stacked, a round wicker basket with a striped woollen cloth, and a tall two-handled stone water jar (also the woven basket and stone jar of the script). Matches the cave interior.",None),
('lyre',"A Greek lyre: tortoise-shell body, two curved wooden arms with a crossbar, seven strings.",None),
('scroll_quill',"A partly unrolled blank papyrus scroll with a white quill and a clay inkwell.",None),
('book_pile',"A tall wobbling pile of old leather-bound books and manuscripts in deep blue, burgundy, green and ochre. No titles.",None),
('brass_lamp',"A polished brass oil lamp with curved spout and a curling sheet of blank paper on a small rug-covered market table.",None),
('elephant_skull',"Elephant skull, FRONT view: pale bone, exactly ONE big round hole in the centre of the forehead, NO eye sockets, two curved tusks.",None),
('elephant_skull_in_clay',"The same skull front view half embedded in a rough orange-brown clay wall (derived from elephant_skull).",'elephant_skull'),
('dwarf_elephant',"A small dwarf elephant, pony-sized, standing in side view, grey wrinkled skin, short tusks.",None),
('mule_pair',"Two brown mules in harness straining forward in side view, ropes to a huge rope-bound sandstone block at left.",None),
('ox_cart',"A small ancient wooden ox-cart with two solid wheels and plank bed, a pair of pale oxen in front, side view (wagons/ox-carts for scale).",None),
('axe_tongs_trough',"A glowing hot bronze axe head in iron tongs over a wooden water trough with steam. Objects only, no hands (smith simile).",None),
('map_antique',"Antique sandstone-and-gold parchment map: Mediterranean-style coastline and islands in pale teal, gold border, compass rose, small painted longship, caravel and onion-domed church. No text.",None),
('map_rolled_blank',"The same parchment rolled up and tied with a cord, one corner unrolled showing blank parchment (derived from map_antique; the bard's rolled-up blank map).",'map_antique'),
('gulls',"Five white seagulls with grey wings and yellow beaks in flight, varied poses.",None),
('anvil_bolt',"A dark iron anvil on a stump, forging hammer, and tongs holding a glowing white-gold zigzag thunderbolt.",None),
('straw_bowls',"A heap of straw and hay, four straws in a fan (no hand), a row of three empty shallow clay bowls and one round wooden bowl.",None),
('ram',"MASTER ram: a big woolly ram with huge curled gold-brown horns and thick cream fleece hanging to its knees. The character sheet characters/ram is derived from it.",None)]
def props():
    json.dump([dict(file=k+'.png',role=k,canonical=True,derived_from=s) for k,_,s in PR],open('props/manifest.json','w'),indent=1)
    open('props/PROPS.md','w').write("# Props\n\nOne master per object on plain cream (the ship and its beached/sea variants live with the places); derived states are edits of the master.\n\n"+"\n".join(f"- `{k}.png`: {v}" for k,v,_ in PR)+"\n\nProp/place consistency: the boulder prop is cut from the cave exterior master; the ship in places/beach_and_ship is the props/ship.png ship; the interior boulder close-up is a crop of the interior master.\n")
def props_sheet():
    fs=[k for k,_,_ in PR if os.path.exists(f'props/{k}.png')]
    c=6; w=420; S=Image.new('RGB',(c*w+20,110+((len(fs)+c-1)//c)*(w+40)),BG); dr=ImageDraw.Draw(S)
    dr.text((20,20),'PROPS  -  contact sheet',fill=(31,58,95),font=font(60))
    for i,k in enumerate(fs):
        x=20+(i%c)*w; y=110+(i//c)*(w+40); dr.text((x,y),k,fill=(60,40,20),font=font(24)); S.paste(fit(f'props/{k}.png',w-10,w-10),(x,y+34))
    S.save('props/sheet.jpg',quality=88)
def refs():
    os.makedirs('refs',exist_ok=True)
    for x in glob.glob('refs/*'): os.remove(x)
    n=0
    for m in glob.glob('*/*/manifest.json')+['props/manifest.json']:
        folder=os.path.dirname(m); name='props' if m.startswith('props') else os.path.basename(folder)
        if folder.startswith('_'): continue
        for e in json.load(open(m)):
            if (e['canonical'] or e.get('variant')) and e['file'].endswith('.png'): shutil.copy(f"{folder}/{e['file']}",f"refs/{name}__{e['role']}.png"); n+=1
    print('refs',n)
if __name__=='__main__':
    chars(); places(); props(); props_sheet(); refs()
