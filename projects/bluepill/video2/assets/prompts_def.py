#!/usr/bin/env python3
"""Prompt definitions for video 2 assets (ASSET-PLAN.md). Wraps SCENE text in the frozen video1 template pieces
(identity paragraphs, inline flat clause, KEEP footer, STYLE_ORIG / STYLE_NP from video1/build_manifest.py), unchanged except
the sprite-specific framing sentences (white background, full body, one figure)."""
import os, json, sys
ROOT = '/home/williamdownard/.openclaw/workspace/projects/bluepill'
sys.path.insert(0, f'{ROOT}/video1')
import build_manifest as bm   # ODY, CY, FLAT, INLINE_FLAT, KEEP_T0, STYLE_ORIG, STYLE_NP, PROP_KEEP, STYLE_REF, prompt_t0
A = f'{ROOT}/video2/assets'
P = f'{A}/prompts'; os.makedirs(P, exist_ok=True)

CREW = ("a young ancient Greek man with messy brown hair, stubble and a worried face, wearing a plain sleeveless slate-blue tunic "
        "with a brown leather strap across the chest, a twisted rope belt, bare arms and lace-up sandals; no helmet, no armour, no wreath, no sash, no weapon. "
        "He is drawn alone on plain white with no ship, no sea, no scenery and no other people.")
CYC2 = ("a Cyclops of Polyphemus' people (NOT Polyphemus himself): a giant with exactly ONE large eye in the centre of his forehead under a heavy brow and no other eyes, "
        "weathered grey-olive leathery skin (never orange, never tan, never pink), short cropped grey hair, a short trimmed grey beard, a brown leather smith's apron "
        "worn over a short ragged hide kilt, a plain twisted rope belt with NOTHING hanging from it (no bells, no pouch, no knife, no metal objects), bare feet, "
        "a slimmer and more symmetric build than a brute, with ordinary matching arms.")
EMPED = ("Empedocles, a Greek philosopher of the fifth century BC: an older man with a long grey beard and a bald crown with grey hair at the sides, "
         "a plain undyed cream himation wrapped over one shoulder leaving the other bare, bare feet; NO laurel wreath, NO blue sash, NO red tunic, no staff.")
THUC = ("a lean middle-aged ancient Greek man with close-cropped dark hair and a short dark beard, wearing a plain grey himation over a pale tunic and "
        "sandals; no wreath, no sash, no red clothing. He is drawn alone on plain white as one figure, not a reference sheet.")
IDENT = {'odysseus': bm.ODY, 'polyphemus': bm.CY, 'crew': CREW, 'cyc2': CYC2, 'empedocles': EMPED, 'thucydides': THUC}
MASTER = {'odysseus': f'{ROOT}/tests/stress_test/refs/odysseus_A_flat.png',
          'polyphemus': f'{ROOT}/tests/stress_test/refs/cy_v4_flat.png',
          'crew': f'{A}/masters/crew_master_white.png',
          'cyc2': f'{A}/masters/cyc2_master_white.png',
          'thucydides': f'{A}/masters/thucydides_master_white.png'}

SPRITE_KEEP = ("Keep the same ink line weight, flat colour with one cel-shadow tone and restrained earthy palette as the references; a natural asymmetric pose "
               "(no stiff A-pose, no symmetrical flexing); exactly the right number of arms, legs, hands and eyes; the face is clearly readable; no text anywhere; "
               "a single figure filling most of the frame height with a small margin all round; plain pure white background, no ground line, no cast shadow on the ground, "
               "no scenery and no props except those named in the pose. ONE single drawing of the figure only: NOT a character sheet, no turnaround, "
               "no multiple views, no expression chart, no colour swatches, no labels, no captions.")

def sprite_prompt(char, pose_text, prev=False, extra_eye=''):
    ident = IDENT[char]
    t = f"Image 1 shows the character: {ident}"
    if prev: t += " Image 2 is the same character in another pose that was accepted: use it only for the ink style, proportions and palette."
    t += " Keep the character's face, hair and costume exactly as in the references. Do not copy the pose of the reference images."
    if char in ('polyphemus', 'cyc2'): t += " He has exactly ONE eye and nothing hangs from his belt."
    scene = (f"The same character alone, full body with both feet visible, body turned a little toward the viewer's right (three-quarter view), "
             f"on a plain pure white background with nothing else in the frame, {bm.INLINE_FLAT}. Pose: {pose_text}.")
    return f"{t}\n\nSCENE: {scene}\n\n{SPRITE_KEEP}\n\n{bm.STYLE_ORIG}"

def sprite_prompt_v2(char, pose_text, prev=False):
    """Instruction-first variant for characters whose descriptive prompts turned into scenes or model sheets."""
    ident = IDENT[char]
    return (f"TASK: redraw the man in image 1 in a NEW POSE. Output ONE drawing of that same man alone, full body with both feet visible, "
            f"on a plain pure white background with absolutely nothing else: no scenery, no sky, no sea, no buildings, no other people, no text, no labels, "
            f"no multiple views, not a character sheet. Keep his face, hair, clothes and colours exactly as in image 1. "
            f"NEW POSE: {pose_text}. Body turned a little toward the viewer's right. {bm.INLINE_FLAT}.\n\n"
            f"The man is {ident}\n\n{bm.STYLE_ORIG}")

def newchar_prompt(ident, pose_text):
    scene = (f"A single character, full body with both feet visible, body turned a little toward the viewer's right (three-quarter view), on a plain pure white background "
             f"with nothing else in the frame, {bm.INLINE_FLAT}: {ident} Pose: {pose_text}.")
    return f"SCENE: {scene}\n\n{SPRITE_KEEP}\n\n{bm.STYLE_ORIG.replace('in exactly the style of the reference images: ', '')}"

def prop_prompt(obj):
    scene = f"{obj}, on pure white. Flat ink, one cel-shadow tone. Simplified proportions."
    return f"SCENE: {scene}\n\n{bm.FLAT} {bm.PROP_KEEP.replace('Widescreen 16:9 frame', 'Square frame')}\n\n{bm.STYLE_NP}"

MAP_KEEP = ("No people, no figures, no animals, no ships. No text, no letters, no numbers, no symbols, no compass rose, no scroll or parchment look, no frame or border. "
            "Flat inked cartoon rendering: a thin dark-brown ink coastline with slight hand-drawn wobble, flat colour fills, no painterly texture, no relief shading, no gradients. "
            "Widescreen 16:9, the whole frame is map.")
def map_prompt(scene):
    return f"SCENE: {scene}\n\n{MAP_KEEP}\n\n{bm.STYLE_NP}"

# ---------------- pose lists (ASSET-PLAN section 2) ----------------
POSES = {
 'odysseus': [
  ('walk', "mid-stride, walking briskly toward the viewer's right, a bulging dark goatskin wineskin slung over one shoulder on a strap, determined face"),
  ('talk', "both hands open and held out at waist height, palms up, explaining, mouth open mid-sentence, eyebrows raised"),
  ('shrug', "a big shrug: shoulders up, both palms out at the sides, eyebrows raised high, mouth a flat line"),
  ('think', "one hand at the chin, eyes looking up and to the side, weight shifted back onto the rear foot, thinking"),
  ('flat', "standing straight, arms hanging at the sides, a perfectly blank unimpressed face: half-lidded eyes, flat eyebrows, a small closed mouth"),
  ('smug', "arms folded loosely, chin slightly raised, a half smile, eyes glancing sideways, smug"),
  ('armscrossed', "arms folded tight across the chest, feet planted apart, mouth set, waiting impatiently"),
  ('sworddraw', "leaning forward, right hand on the hilt of a short bronze sword at his left hip, the blade half drawn from a plain leather scabbard, jaw clenched"),
  ('swordlower', "a short bronze sword held loosely in the right hand, lowered point-down at his side, shoulders dropped, deflated, looking down"),
  ('offerbowl', "holding out a wide shallow wooden bowl with both hands at chest height, face deadpan"),
  ('tiptoe', "up on his toes, chin high, one fist on the hip, the other hand cupped beside the mouth, shouting at someone far away"),
  ('lookup', "standing with the head tipped far back, looking straight up at something very tall, hands hanging, mouth slightly open"),
 ],
 'polyphemus': [
  ('wave', "one huge hand raised beside the head in a small awkward wave, a shy half smile, the other arm hanging"),
  ('leandown', "bent forward from the waist toward the viewer, hands on his knees, the one eye wide and curious, mouth open"),
  ('scorn', "straightened up tall, one hand flicking dismissively, lip curled in scorn, the brow pulled down over the one eye"),
  ('beam', "swaying, flushed cheeks, a sloppy wide grin, a wide wooden bowl held in one hand, the other arm loose, tipsy and happy"),
  ('tender', "kneeling on one knee, head bowed, one hand held out flat and low as if gently patting a small animal that is not drawn, a soft closed-mouth expression, the one eye half closed"),
  ('armswide', "both arms flung wide, palms up, pleading, the brow raised over the one eye, mouth open"),
  ('wounded', "one hand laid flat on his chest, mouth a small round o, brow up, looking hurt"),
 ],
 'crew': [
  ('point', "pointing to the viewer's right with the whole arm extended, mouth open"),
  ('plead', "hands clasped together at the chest, eyebrows up, pleading, one sweat drop beside the head"),
  ('torch', "holding a burning wooden torch up in one hand with flat orange flames, the other hand raised in a hesitant little wave, peering ahead"),
  ('alarmed', "leaning back hard, both hands up, eyes wide, mouth open in alarm, one foot already turned to run"),
  ('lookup', "head tipped back looking straight up, one hand shading the eyes, mouth open in wonder"),
 ],
 'cyc2': [
  ('shrug', "shoulders up, palms out, the one eye rolled upward, bored shrug"),
  ('back', "seen from behind, walking away from the viewer, one hand raised in a dismissive wave over the shoulder"),
  ('smith_hammer', "a smith's hammer raised over the shoulder in one fist, apron on, the one eye intent on work"),
  ('smith_tongs', "holding long iron tongs out in front with both hands, leaning back a little from heat"),
  ('smith_flat', "a smith's hammer hanging straight down from one hand, shoulders dropped, dead-flat expression, mouth a straight line"),
 ],
 'thucydides': [
  ('palmsup', "both palms turned up at waist height, head tilted, an honest 'I cannot tell' face with raised eyebrows"),
 ],
}
MASTER_POSE = {
 'crew': "standing at ease, weight on one leg, oar-callused hands hanging at the sides, looking at the viewer",
 'cyc2': "standing, arms loose at the sides, a bored expression, the one eye half-lidded",
 'thucydides': "standing, holding a rolled papyrus scroll at his side in one hand, calm face",
 'empedocles': "standing with one hand raised, index finger up, as if lecturing",
}

PROPS = {
 'cheese': "A round wheel of pale yellow cheese with a wedge cut out, resting on a small round wooden board",
 'wineskin': "A bulging dark goatskin wine bag with a wooden stopper and a leather carrying strap",
 'gift_basket': "A woven wicker gift basket with a folded cloth lining and a small ribbon bow on the handle, empty",
 'lightning': "A jagged gold thunderbolt with two forks, pointing downward",
 'club': "An uprooted olive-wood club with grey-green bark, knot stubs and a few silver-green leaves still on the thick end, lying horizontal",
 'stake': "A long sharpened olive-wood pole lying at a slight diagonal, the sharpened point charred black; a plain wooden pole with no metal, no blade, no hilt, NOT a sword",
 'flames': "A small campfire of three crossed logs with flat orange-and-gold flame shapes rising from them",
 'dung': "A soft stylised heap of dried sheep droppings mixed with straw, brown, with three small flies drawn as dots with tiny wings above it",
 'bowl': "A wide shallow wooden drinking bowl seen from slightly above, dark red wine inside",
 'ram': "A large ram with heavy curled horns and thick cream wool, in side view facing left, standing, full body",
 'ram_with_feet': "A large ram with heavy curled horns and thick cream wool in side view facing left, standing, and beneath its belly between its legs a pair of human shins and sandalled feet hanging down as if a man were clinging underneath; only the shins and sandals of the man are visible",
 'sheeptrio': "Three woolly sheep walking abreast in side view facing left, bound together across their chests with one twisted willow rope",
 'giftbox': "A small wooden chest with its lid open, a gold cup standing inside",
 'magnifier': "A large hand magnifying glass with a round brass rim and a dark wooden handle, held at a diagonal",
 'book_fossil_hunters': "A thick hardback book standing upright, a plain dark green cloth cover with absolutely NO text, no letters and no title on it",
 'fossil_bone': "A single large fossil long bone, grey-brown, with cracks and both knobbed ends, lying at a diagonal",
 'drawer_closed': "A small wooden card-index drawer with a brass label holder and a brass pull on the front, closed, seen from the front and slightly above",
 'drawer_open_empty': "A small wooden card-index drawer with a brass label holder and a brass pull, pulled open and completely empty inside, seen from the front and slightly above",
 'hammer': "A smith's hammer with a heavy iron head and a wooden haft, lying at a diagonal",
 'anvil': "A smith's iron anvil standing on a tree-stump base",
 'wall_block': "A single huge rough limestone block, unworked and irregular, pale grey-cream with ink hatching, resting on nothing",
 'folktale_scroll': "A loosely rolled papyrus scroll with one end unrolled, blank with no text",
 'bag': "A leather sack tied at the neck with a cord, bulging",
 'wand': "A slim dark wooden wand with a small knob at one end, at a diagonal",
 'whirlpool': "A stylised whirlpool of concentric slate-blue rings spiralling into a dark centre, seen from above, as a round emblem",
 'etna_icon': "A small volcano cone, brown with a snow-free dark top, sending up a grey smoke plume, as a simple map icon",
}

PLATES = {
 'NB_prayer': dict(refs=['cy', 'land'], scene="DUSK, blue-violet sky with one band of pale light low on the horizon, wide shot. On a dark rocky shore in the foreground the Cyclops stands with his back to the camera, both huge arms raised to the sky, palms open, head tipped back, shown as a single flat near-black silhouette with his ragged hair, beard and hide wrap read only in outline; no face, no eye visible. Beyond him a dark calm sea and, very small and far out on the water, a single ship with one square sail. No sun, no glow, no god figure in the sky. The upper third of the frame is clear sky."),
 'NB_forge': dict(refs=['cave', 'stone'], scene="DIM FORGE INTERIOR, warm orange from a single forge hearth at the left, medium-wide shot, empty stage. A great stone anvil on a stump stands at centre on a flat earthen floor, a bed of coals glowing in a stone hearth at the left with bellows, hammers and tongs hung on the rock wall at the right, a chain and a water trough, smoke drifting up into darkness. A clear flat band of floor across the lower third with nothing standing on it, so figures can be placed there; the upper right of the frame is dark and clear for labels. No people and no figures."),
 'NBG02_mouth': dict(refs=[f'{ROOT}/video1/images/NBG02.png', 'cave'], scene="Same cave interior as the reference image 1, seen from deeper inside looking toward the entrance: the bright cave mouth fills the right half of the frame as a tall ragged arch of overcast grey daylight, the cheese racks and lamb pens along the left wall in shadow, the floor a flat band across the bottom with nothing standing on it. The daylight in the arch is a flat pale grey-white so a large dark figure standing in it would read as a silhouette. No people, no animals in the arch."),
 'NBG06_day': dict(refs=[f'{ROOT}/video1/images/NBG06.png', 'land'], scene="Same island crater and coastline as the reference image 1, redrawn in full daylight: pale blue sky, the sea slate blue, the vent no longer glowing but sending up one tall grey-white smoke plume that leans slightly to the right and reaches the top of the frame; the rock warm grey-brown in flat overcast light; the lower right corner is a clear band of shore so a figure can be placed there. No people."),
 'board_base': dict(refs=[], scene="A detective's evidence board seen flat and front-on, filling a widescreen frame: a cork pinboard in a plain dark wood frame, four empty rectangular paper cards pinned in a two-by-two grid with brass pins, each card blank and cream, a few loose pins and a short length of red string in one corner, the top strip of cork above the cards left clear. Flat inked cartoon rendering, no text, no letters, no labels, no photographs on the cards."),
 'NB_ram': dict(refs=['ody'], scene="DIM OVERCAST DAYLIGHT inside a cave mouth, low wide shot at ground level. A huge ram with heavy curled horns and thick cream wool walks slowly toward the camera and a little to the right across the cave floor; clinging beneath its belly, face down and gripping the wool with both hands, hangs Odysseus, his body hidden under the fleece except his head, arms and his sandalled feet; his face is tense and determined. Other sheep walk beside and behind the ram as simple woolly shapes. Flat grey daylight from the cave mouth ahead. Nobody else is in the frame: no giant, no hands reaching, no club; the upper third of the frame is dark cave wall, clear."),
}
MAPS = {
 'map_med': "A flat inked map of the central and eastern Mediterranean from the heel of Italy and Sicily on the left to the coast of Asia Minor on the right, with Greece, Crete and the Aegean islands in the middle, land in flat olive-cream with a thin dark-brown ink coastline, sea in flat slate blue, no place names, a few small ink hatch marks for mountains; the sea areas left plain so route lines and labels can be drawn over them",
 'map_sicily': "A flat inked map of Sicily filling most of the frame with Malta below it and the toe of Italy at the upper right, the Aeolian islands as a few small dots north of Sicily, Mount Etna drawn as a small ink cone on the east coast, land flat olive-cream with a dark-brown coastline, sea flat slate blue",
 'map_world': "A flat inked world map in equirectangular projection, all continents in flat olive-cream with a dark-brown ink coastline, oceans flat slate blue, Europe and the Middle East near the centre-left of the frame",
 'map_argolid': "A flat inked map of the Argolid peninsula in the Peloponnese of Greece with the Gulf of Argos opening to the south, two small dark ink squares marking the sites of Mycenae inland to the north and Tiryns near the coast, land flat olive-cream, sea flat slate blue",
}

def write(name, text):
    p = f'{P}/{name}.txt'; open(p, 'w').write(text); return p

if __name__ == '__main__':
    print(sprite_prompt('odysseus', POSES['odysseus'][0][1], True))
