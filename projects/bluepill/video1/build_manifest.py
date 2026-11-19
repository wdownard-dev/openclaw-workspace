#!/usr/bin/env python3
"""Build video1/manifest.json from SHOTLIST-V1.md (shot ids per asset) plus the prompt table below.
Run: python3 build_manifest.py   (does not overwrite status fields of an existing manifest)"""
import re, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ODY = ("Odysseus: a bearded dark-haired man in his forties with a gold laurel wreath, a rust-red tunic with gold hem, "
       "a blue sash across one shoulder fastened with a gold brooch, a brown belt and lace-up sandals.")
CY = ("Polyphemus the Cyclops: a giant with exactly ONE large eye in the centre of his forehead under a massively heavy scarred brow and no other eyes, "
      "weathered olive-brown leathery skin with a grey-green cast (never orange, never tan, never pink) covered in pale scars, matted brown hair, a braided shaggy beard, "
      "a patched sheepskin wrap over one shoulder and a short ragged hide kilt, a plain twisted rope belt tied at the front with NOTHING hanging from it "
      "(no bells, no pouch, no gourd, no knife, no metal objects at all), lace-up leather sandals, a hunched asymmetric build with a huge right arm and a thinner left arm. "
      "The reference does not show his club: when a club appears it is an uprooted olive-wood club with grey-green bark, knot stubs and a few silver-green leaves.")
STYLE_REF = ("a STYLE reference only (ink line weight, flat colour, rock and water rendering): copy its drawing language, but do NOT copy its layout, lighting or colours, "
             "and do NOT draw any person, creature or ship from it")
FLAT = ("Render as flat inked cartoon: clean dark-brown ink outlines of medium weight, flat colour fills plus one tone of cel shadow, light ink hatching on rock and wood, "
        "no painterly texture, no soft airbrushed gradients, no mud, no moss, no photographic or 3D look.")
KEEP_CH = ("Keep the same ink line weight, flat colour with one cel-shadow tone and restrained earthy palette as the references; natural asymmetric working poses "
           "(no stiff A-pose, no symmetrical flexing); exactly the right number of arms, legs and eyes on every figure, and the Cyclops has exactly one eye; "
           "no bells on any belt; lighting exactly as stated (no sunset glow, no golden haze unless a fire is named); no text anywhere; widescreen 16:9 composition.")
KEEP_BG = ("No people and no figures anywhere unless the scene says otherwise. Natural, slightly irregular drawn forms (not neat or symmetrical); "
           "lighting exactly as stated (no sunset glow, no golden haze); no text, no letters, no symbols, no watermark; widescreen 16:9 composition.")
STYLE_ORIG = ("STYLE: mature inked cartoon explainer art in exactly the style of the reference images: confident dark brown ink outline of medium weight with slight hand-drawn wobble, flat colour fills plus one tone of cel shadow, "
              "human proportions about 4 heads tall for ordinary men, defined jawline and small line nose, small dot eyes with strong eyebrows; richly detailed costumes and props; "
              "backgrounds drawn in the same inked language (same line weight, flat colour, no painterly gradients, no photographic texture); earthy restrained palette of rock browns, olive, slate blue and cream with "
              "rust-red and gold accents only on costumes; no text, no letters, no watermark, no frame.")
STYLE_NP = ("STYLE: mature inked cartoon explainer art: confident dark brown ink outline of medium weight with slight hand-drawn wobble, flat colour fills plus one tone of cel shadow, "
            "light ink hatching, earthy restrained palette of browns, olive, slate blue and cream; no text, no letters, no watermark, no frame.")
STYLE = ("STYLE: mature inked cartoon explainer art in exactly the style of the reference images: confident dark brown ink outline of medium weight with slight hand-drawn wobble, "
         "flat colour fills plus one tone of cel shadow, richly detailed props; backgrounds drawn in the same inked language (same line weight, flat colour, no painterly gradients, "
         "no photographic texture); earthy restrained palette of rock browns, olive, slate blue and cream with rust-red and gold accents only on costumes; no text, no letters, no watermark, no frame.")

REFNAMES = {'ody': 'odysseus_A_flat.png', 'cy': 'cy_v4_flat.png', 'land': 'sty_land.png', 'stone': 'sty_stone.png', 'cave': 'sty_cave.png'}

def intro(refs, extra=''):
    if not refs: return ''
    parts = []
    for i, r in enumerate(refs, 1):
        if r == 'ody': parts.append(f"Image {i} is the character design of {ODY}")
        elif r == 'cy': parts.append(f"Image {i} is the character design of {CY}")
        elif r in ('land', 'stone', 'cave'): parts.append(f"Image {i} is {STYLE_REF}.")
        else: parts.append(f"Image {i} is {r}")
    t = ' '.join(parts)
    if 'ody' in refs or 'cy' in refs:
        t += " Keep the characters' faces and costumes exactly as in the references. Do not copy the white background, layout or poses of the reference images."
    return t + extra

def prompt(refs, scene, keep=None, extra='', style=None):
    keep = keep or (KEEP_CH if ('ody' in refs or 'cy' in refs) else KEEP_BG)
    return f"{intro(refs, extra)}\n\nSCENE: {scene}\n\n{FLAT} {keep}\n\n{style or STYLE}".strip()

INLINE_FLAT = "flat inked cartoon rendering (clean ink outlines, flat colour, no painterly texture, no mud, no moss)"
KEEP_T0 = ("Keep the same ink line weight, flat colour with one cel-shadow tone and restrained earthy palette as the references; natural asymmetric working poses "
           "(no stiff A-pose, no symmetrical flexing); exactly the right number of arms, legs and eyes on every figure, and the Cyclops has exactly one eye; the figures are large enough in frame "
           "that faces are readable; no text anywhere; widescreen 16:9 composition.")
def prompt_t0(refs, scene):
    # exact stress-test template (STYLE_ORIG, original footer) plus the inline flat clause that fixed s05b
    sc = scene.replace('. ', ', ' + INLINE_FLAT + '. ', 1)
    return f"{intro(refs)}\n\nSCENE: {sc}\n\n{KEEP_T0}\n\n{STYLE_ORIG}"
T0_FIRST = {'NB17', 'NB22', 'NB24'}
A = {}  # id -> dict(kind, refs, scene, desc, checks, risk)
def add(i, kind, refs, scene, desc, checks, risk='M', keep=None, extra=''):
    A[i] = dict(id=i, kind=kind, refs=refs, scene=scene, desc=desc, checks=checks, risk=risk, keep=keep, extra=extra)

# ---------------- baked scenes ----------------
add('NB01','NB',['cy'],"COLD DIM CAVE with one warm fire edge. Extreme close-up, front-on, of the Cyclops' head and upper shoulders filling most of the frame. His single large eye sits in the centre of his forehead under the heavy scarred brow and glares straight at the camera; he has NO other eye. Matted hair, braided beard, scarred olive-brown skin. His face is lit cold slate-blue from the cave mouth behind the camera; a thin warm orange rim light runs along his left cheek and beard from a fire out of frame. Dark cave wall behind him.",
    "Hero close-up of the Cyclops, one eye, front-on, thumbnail source",["one eye, no second eye","olive-brown skin","cold light, one warm edge","no bells","flat ink style"],'M')
add('NB02','NB',['ody'],"WARM FIRELIT HALL, indoors, medium shot. Odysseus stands beside a great stone hearth in a columned palace hall at night, one hand raised mid-story, lips parted, eyes sweeping over his audience, the warm orange hearth light on the right side of his face. In the dark foreground along the bottom of the frame the backs of the heads and shoulders of several seated listeners are near-black silhouettes with no faces and almost no detail. Behind him painted columns, hanging bronze lamps, long tables with cups. His face is large enough to read.",
    "Odysseus telling his story in a firelit hall, listeners as foreground silhouettes",["wreath+sash+beard","listeners dark silhouettes only","face readable","warm firelit interior"],'H')
add('NB03','NB',['cy','land'],"PALE OVERCAST, grey-blue sky, wide landscape shot. A huge dark hunched silhouette of the Cyclops, a single flat dark olive-grey shape with ragged hair outline and no facial detail, stands alone on a high ridge above a grey-blue sea; he is so large that he rises above the pines and the other hills like a wooded peak. Down the slopes below him a scatter of tiny white sheep. Cool flat light, mist in the valleys, no sun.",
    "Far silhouette of the Cyclops on a ridge, sheep below",["silhouette reads as giant on ridge","no face detail","overcast grey-blue","flat ink"],'L')
add('NB04','NB',['ody'],"COLD DIM CAVE, close-up. Odysseus, chest-up, three-quarter view, his right hand gripping the hilt of a bronze short sword at his hip, the blade half drawn, his eyes fixed on the dark beyond the frame, jaw clenched, thinking hard. Cold slate-blue light from a gap round a boulder at the back left, everything else in deep shadow. No fire, no orange light.",
    "Odysseus, hand on sword hilt, eyes on the dark",["wreath+sash+beard","hand on hilt","cold light","face reads"],'L')
add('NB05','NB',['cy'],"FIRE-LIT, DEEP SHADOW, wide shot inside the cave. In the right foreground the huge Cyclops seen from behind, hunched over a big cooking fire, his broad back and shaggy hair a dark mass against the flames, his club resting at his side. Far away in the deep shadow of the left corner a cluster of small cowering men shown only as dark silhouettes with no faces and no detail. Nothing graphic: no food, no bodies, no blood.",
    "Giant's back against the fire, cowering silhouettes far away",["Cyclops from behind only","crew silhouettes only, no detail","nothing graphic","no bells"],'H')
add('NB06','NB',['ody'],"DIM OVERCAST DAYLIGHT, low-angle wide shot inside the cave mouth. Odysseus, small, stands beside the Cyclops' enormous club lying on the cave floor: a green olive trunk as thick as a ship's mast, thicker than Odysseus is wide and far longer than he is tall, grey-green bark, knot stubs, silver-green leaves at the thick end. Odysseus rests one hand on it and looks up at it, awed and calculating. Dim flat grey daylight from the cave entrance on the left.",
    "Odysseus small beside the giant's olive club (scale)",["wreath+sash+beard","club huge, olive wood","scale clear","overcast daylight"],'M')
add('NB07','NB',['ody'],"FIRE-LIT, orange from the fire only. Odysseus crouches beside a small campfire in the dark cave, holding a long pole of olive wood nearly twice his own height; he is turning its sharpened end in the flames to char it, the tip glowing, a few sparks rising, his face lit orange from below, concentrated. It is a plain wooden pole: no blade, no hilt, no metal, NOT a sword. His long shadow on the cave wall behind him.",
    "Odysseus charring the stake tip in the fire",["wreath+sash+beard","stake is a pole not a sword","orange from fire only","flat ink"],'M')
add('NB08','NB',['ody','cy'],"FIRE-LIT, warm. Medium two-shot inside the cave. Odysseus stands at the right and holds out a big dark wineskin toward the giant with one hand, polite and calculating, the other hand open. The Cyclops sits hunched on the ground at the left beside a low fire, looking sideways down at him, suspicious, a milk pail and a ewe near his feet. Warm orange firelight only, deep brown-black shadows, a sheep pen of wooden stakes behind, cheese wheels on a rock shelf.",
    "Wine offer two-shot (replaces old slot 01)",["one eye, no bells","olive-brown skin","wreath+sash+beard","wineskin visible","flat ink"],'M')
add('NB09','NB',['cy'],"FIRE-LIT, warm, medium close-up. The Cyclops in side profile facing left, his head LEVEL (chin not raised, not tipped back), both huge hands raising a big wooden bowl of wine to his mouth, drinking, wine dripping into his beard. His one eye is visible once, in the middle of his forehead under the heavy brow; he has no other eye on either side of his face. A small fire below frame casts warm orange light up onto his face; dark cave behind, empty amphorae on the ground.",
    "Cyclops drinks wine, profile, head level",["exactly one eye","head level","bowl raised","no bells","flat ink"],'H')
add('NB10','NB',['cy','ody'],"NIGHT, dying embers, cold blue. Wide shot from a slightly high angle. The Cyclops lies sprawled asleep on his back across the cave floor, head at the left, mouth open, one huge hand limp, his single eye CLOSED under a heavy lid, no other eye. Far off at the lower right, tiny, Odysseus crouches in the shadow beside the glowing embers, watching him. A single cold blue moonbeam falls from a crack in the cave roof; the only orange is the embers on the floor.",
    "Cyclops asleep, single eye closed, Odysseus small",["one eye (closed)","Odysseus small, wreath visible","cold blue night","no bells"],'M')
add('NB11','NB',['ody'],"NIGHT, lit only by a glowing stake tip. Seen from behind Odysseus (his back and wreath in the foreground, face not shown), he drives a long charred olive-wood pole, its tip white-orange hot, forward into the black shadows of the cave toward an enormous dark mass lying on the floor, the sleeping giant, shown only as a featureless black shape at the edge of the glow, with no face, no eye and no blood visible. Sparks fly. The only light is the glowing tip, throwing orange rim light on Odysseus' shoulders, sash and wreath. No gore.",
    "Off-screen blinding: glowing stake tip, giant a black mass",["no gore, no eye visible","stake reads as a pole","orange from tip only","Odysseus from behind"],'M')
add('NB12','NB',['cy'],"NIGHT, cold moon rim light, medium-wide shot. The Cyclops stands at the mouth of his cave on a dark hillside, bellowing into the night, one huge hand clamped over the upper half of his face hiding his one eye completely, the other hand braced against the rock. IMPORTANT: no eye is visible anywhere on his face, because his single eye is hidden under the hand and he has no other eye; below the hand only the nose, beard and open bellowing mouth show. Cold moon rim light on his hair and shoulders, a faint orange glow from inside the cave behind him, black hills beyond.",
    "Cyclops at cave mouth, hand over the eye, shouting",["no eye visible / exactly one eye","hand over upper face","moon rim light","flat ink not painterly"],'H')
add('NB13','NB',['land','stone'],"DIM DAWN, cool grey-blue light. Wide shot of a cave mouth on a grassy hillside: a flock of big rams and sheep crowds out of the cave arch, the animals bound in threes with twisted willow rope, three abreast across the chest, jostling down the slope, one large fine ram in the middle of the flock. Pale grey-blue sky, thin mist. Animals only, no people.",
    "Rams bound in threes leaving the cave at dawn",["animals only","bound in threes visible","cool dim dawn","flat ink"],'L')
add('NB14','NB',['ody','cy'],"DIM DAWN, grey-blue overcast light, front-on view. The cave mouth is at the back. In the foreground a large ram with curled horns walks toward the camera. Odysseus is hanging UNDER the ram, upside down beneath its belly, both arms wrapped round its wool and his legs hooked over its back, his bearded face with laurel wreath and the blue sash visible between the ram's front legs, jaw set; the rest of his body is hidden by the wool; he is NOT standing and NOT hiding behind a rock. At the back right the huge Cyclops sits beside the cave mouth with one hand patting the ram's back as it passes, head turned sideways, his single eye closed, no blood. Cool pale light from outside, no sun visible, a few sheep following.",
    "Odysseus under the ram, Cyclops patting its back (replaces old slot 05b)",["Odysseus UNDER the ram","one eye, no bells","dawn grey-blue","flat ink"],'H')
add('NB15','NB',['cy'],"DIM DAWN, pale grey-blue light from the cave mouth. Close-up of the Cyclops' huge scarred olive-brown hands feeling slowly along the thick wool on the backs of rams as they pass beneath him; wool, a ram's curled horns, a sliver of the giant's forearm and hide wrap. His face is out of frame above the top edge: no face visible at all.",
    "Giant hands on wool, face out of frame",["no face visible","hands olive-brown with scars","wool on ram backs","flat ink"],'L')
add('NB16','NB',['cy'],"DIM DAWN, soft pale light. Medium shot. The Cyclops kneels at the cave mouth with his head bowed low toward a big ram that stands facing him, one huge hand stroking the ram's head, his mouth moving as if speaking softly to it; seen from slightly behind and above, so only his heavy brow, nose and beard show and his single eye is closed and in shadow beneath the brow; no second eye anywhere. A tender, quiet moment. Curled ram horns, cool grey-blue dawn.",
    "Cyclops bowed to the ram, speaking to it",["eye closed/hidden, only one","head bowed to ram","tender mood","flat ink"],'H')
add('NB17','NB',['cy'],"GREY DAWN, flat overcast light, wide-ish shot. The Cyclops seen from directly BEHIND, standing at the edge of a cliff top, his right arm raised high with the fist clenched and pointing out over a grey sea, his left arm hanging, hair and hide wrap ragged in the wind, the club on the ground at his feet. No face visible at all. Far out on the grey sea a tiny dark ship.",
    "Cyclops from behind on a cliff top, arm raised",["back view, no face","one arm raised","grey overcast","no bells"],'L')
add('NB18','NB',['land','stone'],"GREY DAWN, flat overcast light, wide shot over a grey sea. A dark wooden Greek ship with a plain hull (no painted symbol, no eye, no emblem) at the lower left, small in frame, a few tiny crewmen as dark specks along its rail, long oars out; just beside its stern a huge tall white splash plume erupts from the sea where a boulder has hit. A steep grey cliff on the far right. No sunset glow.",
    "Boulder splash beside the ship's stern, crew tiny",["ship plain hull no symbol","crew tiny specks","splash reads","overcast grey"],'H')
add('NB19','NB',['land','stone'],"DIM CAVE, firelit edge at the left. The floor and a reddish clay bank along a cave wall: several small old bones (ribs, a leg bone, vertebrae) sticking out of the clay, and set back in the middle distance an elephant skull half buried in the clay, small in frame, seen from the front: a broad domed forehead, two small eye sockets low at the sides and one large oval opening in the middle of the face. The skull is old, pale and partial, only its upper half emerges from the clay. Cave walls dark, a warm firelight edge at the left only. No people.",
    "Cave floor with clay bank, bones and a small half-buried elephant skull",["skull anatomy plausible (small side sockets, big central hole)","partial, small in frame","firelit edge","flat ink"],'H')
add('NB20','NB',['land','stone'],"COLD DAYLIGHT, a shallow sea cave on a beach. A man seen from behind sits crouched at the mouth of the cave with his back to us, wrapped in a rough undyed wool cloak over a plain tunic, dark curly hair, no laurel wreath, no blue sash, no gold, holding his hands out to a small fire of driftwood; beyond him the grey beach and pale sea; dim stone cave walls around him, a reddish clay bank on the right wall. Small fire glow on his hands only.",
    "Anonymous sailor, back view, sheltering in a beach cave with a small fire",["not Odysseus (no wreath/sash)","back view","cold daylight + small fire","flat ink"],'L')
add('NB21','NB',['land','stone'],"OVERCAST DAYLIGHT, wide shot of the stone porch of a Greek sanctuary with plain Doric columns. In the centre a gigantic fossil thigh bone, as long as a man is tall, lies displayed on a low stone plinth. Two tiny visitors in simple tunics, seen small from behind, stand before it, each only about one eighth of the frame height. Pale limestone, flat grey light, bare floor, a few olive trees beyond the columns.",
    "Sanctuary porch with a giant bone on a plinth, two tiny visitors",["bone huge on plinth","visitors tiny, no readable faces","overcast daylight","flat ink"],'M')
add('NB22','NB',['cy'],"FORGE GLOW, orange from the fire only, dark stone smithy, medium shot. The Cyclops works as a smith: a thick leather smith's apron over his chest and kilt, instead of the sheepskin wrap; he stands at a stone anvil, a heavy hammer raised in one hand over a glowing bar held on the anvil with long tongs in the other; his single eye gleams in the glow under the heavy brow, and he has no other eye. Sparks fly. Behind him a roaring stone hearth and a bellows. Everything outside the forge glow is near-black.",
    "Cyclops as smith at an anvil, one eye",["exactly one eye","leather apron","orange from forge only","same face as shepherd","no bells"],'M')
add('NB23','NB',['cy'],"FORGE GLOW, close-up on a stone anvil in a dark smithy. Long iron tongs hold a glowing jagged zigzag thunderbolt of bronze and gold with white-hot ends on the anvil; a heavy hammer rests beside it; sparks fly; two huge scarred olive-brown forearms enter from the sides of the frame holding the tongs and the hammer. No faces and no figures: only hands and forearms. Orange forge light, near-black background.",
    "Tongs, hammer and thunderbolt on the anvil, hands only",["no face visible","thunderbolt reads","forge glow","flat ink"],'L')
add('NB24','NB',['cy'],"BLUE DUSK, cool deep blue light, no orange, no sunset. The Cyclops sits on a cliff edge above a calm sea in three-quarter view toward the camera, one hand on his chest, mouth open as if singing, a rough reed pipe lying on his knee, his single eye soft and wistful under one long continuous heavy eyebrow; exactly one eye, no other. Behind him a calm dark-blue sea, a pale teal band of sky at the horizon, first stars. His face is large enough to read.",
    "Seated Cyclops singing on a cliff above the sea, blue dusk",["exactly one eye","long single brow","blue dusk no orange","face reads"],'M')
add('NB25','NB',['land','stone'],"OVERCAST DAYLIGHT. Two mules in rope harness strain at a huge rough unworked limestone boulder far bigger than both of them together, ropes round the stone, hooves dug into the dirt, necks stretched forward, the boulder not moving. Behind them part of an ancient wall of huge rough boulders, grey sky. Animals only, no people.",
    "Two mules straining at a huge stone",["two mules","boulder huge","animals only","overcast","flat ink"],'L')

# ---------------- empty-stage backgrounds ----------------
add('NBG01','NBG',['land','stone'],"OVERCAST DAYLIGHT, cool grey-green, wide empty landscape. A high sea cliff covered in laurel bushes with a cave opening partway up, and in front of the cave a rough stone-and-timber yard wall with a gate; sheep and goats graze on the slopes; a worn dirt path winds up from the lower left to the yard gate; a grey sea behind. Keep the lower third a wide, clear, flat band of packed earth path with nothing standing on it. No people.",
    "Cave on a sea cliff with laurels, yard wall, sheep and goats; overcast",["no people","cave+yard wall+sheep","clear ground band","overcast cool","flat ink"],'L')
add('NBG02','NBG',['cave','stone'],"DIM CAVE INTERIOR with daylight from the entrance. Wide empty stage seen straight on: racks of pale cheese wheels on a wooden frame at the right, a pen of wooden stakes with lambs behind a rough fence at the back, big clay pots on a stone ledge, a rough arched entrance at the left letting in cool grey daylight, dark layered rock walls. Keep the lower third a wide, clear, flat band of packed earth floor with nothing on it. No people.",
    "Cave interior: cheese racks, lamb pens, daylight from entrance",["no people","cheese racks+lamb pens","clear floor band","dim cave, cool daylight at entrance"],'L')
add('NBG03','NBG',['land','stone'],"NIGHT, empty stage. A bare rocky hillside under a low, large pale moon with a few thin clouds; in the middle distance a cave mouth glowing faintly orange in the hillside; dark rolling hills; a clear flat band of dark earth across the lower third with nothing standing on it. The large moon sits just above the ridge line at centre-left so figures standing on the ridge would be silhouetted against it. Cool blue-black night, only the cave mouth is warm. No people.",
    "Night hillside, low moon, glowing cave mouth, clear ground band",["no people","large low moon","glowing cave mouth","clear ground band","flat ink"],'L')
add('NBG04','NBG',['land','stone'],"CLEAR COOL DAWN over a calm sea, empty stage. A low straight horizon, the sea nearly flat with a few small ripple lines, pale cool sky going from soft blue-grey to a thin pale cream band at the horizon, no visible sun, a very faint far coastline at the far left. Nothing on the water. No sunset glow, no orange, no golden light. No ships, no people.",
    "Calm clear dawn sea, low horizon, empty",["empty sea","cool pale dawn, no orange","low horizon"],'L')
add('NBG05','NBG',['land','stone'],"NIGHT. Mount Etna smoking, empty stage. A broad dark volcano rising behind a dark foothill coast, a red-orange glow at the summit crater and a thick plume of smoke drifting across a star-pricked deep blue sky, a few dark cave mouths at the foot of the slope, a faint red reflection in the sea at the left. A wide clear flat band of dark earth across the lower third. Cool night sky, the glow is only at the crater. No people.",
    "Etna smoking at night, caves at its foot, volcanic glow",["no people","volcano with glowing crater and smoke","caves at foot","clear ground band"],'L')
add('NBG06','NBG',['land','stone'],"NIGHT. A small volcanic island in a black sea with a cone-shaped crater, a vent glowing red-orange at the top and a thick smoke plume rising and drifting, a second dark island silhouette beyond, a few stars. Cool blue-black sky; only the vent is warm. Empty stage, no people, no boats.",
    "Aeolian island crater with glowing vent and smoke plume",["no people","glowing vent","smoke plume","flat ink"],'L')
add('NBG07','NBG',['land','stone'],"SOFT DAWN LIGHT, low raking sun from the left with cool blue shadows, empty stage. A massive ancient wall built of huge unworked rough boulders of grey limestone, irregular and different sizes, small wedge stones filling the gaps between them, grass tufts at the base, a dirt path in front, hills in the pale morning distance. The stones are rough and uneven, NOT neat blocks. Keep the lower third a wide clear flat band of packed earth with nothing on it. No people.",
    "Cyclopean wall of unworked boulders, raking dawn sun",["boulders irregular, unworked","raking dawn light","clear ground band","no people"],'M')
add('NBG08','NBG',['land','stone'],"COOL CLEAR MORNING, empty stage. The Lion Gate of Mycenae seen straight on: a massive flat-topped doorway of squared blocks with a huge single stone lintel set into a wall of enormous rough boulders; above the lintel a triangular relief slab showing two lionesses standing on their hind legs facing each other with their front paws resting on a short altar, a tall slender column between them tapering downward; both lions have lost their heads (broken, flat necks). A dirt path leads to the gate. Pale clear sky. No people.",
    "Mycenae Lion Gate with two-lion relief, cool morning",["relief: two lions facing a central column, heads missing","lintel + cyclopean wall","cool morning","no people"],'M')
add('NBG09','NBG',['land','stone'],"BRIGHT OVERCAST, cool light, empty stage. Several dark jagged basalt sea stacks of columnar rock rising from a calm grey-green sea a short way off a rocky coast, one tall and others lower, white foam at their bases, seabirds, a low pale shoreline with a few distant small houses at the far left. No boats, no people.",
    "Basalt sea stacks off a coast (Aci Trezza)",["columnar basalt stacks","calm sea","bright overcast","no people"],'L')

# ---------------- props / sprites ----------------
PROP_KEEP = "A single isolated object on a plain pure white background, no ground line, no shadow, no scene, nothing else in the frame, no text. Cutout-ready: clean closed outline with white all round. Widescreen 16:9 frame with the object centred."
add('NP01','NP',[],"A small dwarf elephant (Palaeoloxodon falconeri) in side view facing left, full body, on pure white: short sturdy legs, a rounded domed head with a tuft of hair on top, a short trunk, small ears and a pair of short straight tusks pointing forward, tough grey-brown skin with a few wrinkle lines, a short thin tail; stocky and small like a pony rather than a full-size elephant. Flat ink, one cel-shadow tone. Simplified proportions.",
    "Flat-ink dwarf elephant sprite, side view, on white",["one elephant, side view, white bg","dwarf proportions (short legs, domed head)","clean outline for cutout"],'M',keep=PROP_KEEP)
add('NP02','NP',[],"A shipwright's pit auger (a long iron drill bit with a spiral flute and a wooden T-shaped handle) boring into a thick, rough-hewn wooden ship plank lying at an angle, curls of wood shavings spiralling out of the hole; a thick oak plank with visible grain. Objects only, no hands, no people. Flat ink, one cel-shadow tone.",
    "Flat-ink shipwright auger boring a plank, prop on white",["auger + plank + shavings","no hands","white bg"],'L',keep=PROP_KEEP)
add('NP03','NP',[],"A bronze axe head glowing dull red-orange held in long iron tongs, just dipping into a round wooden trough of water; white steam rising in curling clouds from the water. Objects only, no hands, no people. Flat ink, one cel-shadow tone.",
    "Flat-ink axe head quenched in a water trough with steam, prop on white",["axe head + trough + steam","no hands","white bg"],'L',keep=PROP_KEEP)
add('NP04','NP',[],"An ancient Greek ship in side view facing right, on pure white: a long low dark-brown wooden hull with a plain unpainted hull (no eye symbol, no painted emblem, no pattern band, no decoration at all), a curved stern post at the left, a row of long oars sloping into the water line, a single mast with a furled cream square sail, a few rope stays. No crew. Flat ink, one cel-shadow tone. No water, no waves, no shadow: the ship alone on white.",
    "Flat-ink Greek ship, side view, plain hull, on white (cutout)",["plain hull, NO eye/symbol","oars + mast","no crew","white bg, clean matte edge"],'H',keep=PROP_KEEP)

def build():
    sl = open(os.path.join(ROOT, 'SHOTLIST-V1.md'), encoding='utf-8').read()
    shots = {}
    for line in sl.splitlines():
        m = re.match(r'\|\s*(\d+)\s*\|\s*([\d:]+)\s*\|\s*([\d.]+)\s*\|(.*)', line)
        if not m: continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 10: continue
        n = int(cells[0]); shots[n] = dict(shot=n, start=cells[1], sec=float(cells[2]), narration=cells[3], type=cells[4], chars=cells[5], light=cells[6], cam=cells[7], asset=cells[8], note=cells[9])
    assert len(shots) == 147, len(shots)
    used = {}
    for n, s in shots.items():
        for a in re.findall(r'\b(NBG\d+|NB\d+|NP\d+|RS\d+|RC\d+)\b', s['asset']):
            used.setdefault(a, []).append(n)
    mpath = os.path.join(HERE, 'manifest.json')
    old = {}
    if os.path.exists(mpath):
        old = {a['id']: a for a in json.load(open(mpath))['assets']}
    assets = []
    for i, a in A.items():
        refs = a['refs']
        refpaths = [REFNAMES[r] if r in REFNAMES else REFNAMES['ody'] for r in refs]
        if a['kind'] == 'NP':
            refpaths = []
        refs_for_prompt = refs
        if i in T0_FIRST: p = prompt_t0(refs_for_prompt, a['scene'])
        else: p = prompt(refs_for_prompt, a['scene'], keep=a['keep'], style=STYLE_NP if a['kind'] == 'NP' else None)
        ent = dict(id=i, kind=a['kind'], desc=a['desc'], risk=a['risk'], shots=used.get(i, []), refs=refpaths, size='1536x864', quality='medium',
                   prompt=p, checks=a['checks'], status='pending', attempts=[])
        if i in old:
            for k in ('status', 'attempts', 'note'):
                if k in old[i]: ent[k] = old[i][k]
        assets.append(ent)
    reuse = [dict(id='RS07', src='tests/stress_test/gen/s07.png', shots=used.get('RS07', []), status='reused'),
             dict(id='RS08', src='tests/stress_test/gen/s08.png', shots=used.get('RS08', []), status='reused'),
             dict(id='RS09', src='tests/stress_test/gen/s09.png', shots=used.get('RS09', []), status='reused'),
             dict(id='RS10', src='tests/stress_test/gen/s10.png', shots=used.get('RS10', []), status='reused'),
             dict(id='RC02', src='tests/stress_test/gen/cy_v4_s02.png', shots=used.get('RC02', []), status='reused'),
             dict(id='RC11', src='tests/stress_test/gen/cy_v4_s11.png', shots=used.get('RC11', []), status='reused')]
    shot_assets = {n: re.findall(r'\b(NBG\d+|NB\d+|NP\d+|RS\d+|RC\d+)\b', s['asset']) for n, s in shots.items()}
    json.dump(dict(video='V1 The Cyclops Was Real?', assets=assets, reused=reuse, shot_assets=shot_assets), open(mpath, 'w'), indent=1, ensure_ascii=False)
    json.dump(shots, open(os.path.join(HERE, 'shots.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(assets), 'assets to generate;', len(reuse), 'reused;', sum(1 for a in assets if not a['shots']), 'assets with no shots')
    for a in assets:
        if not a['shots']: print('  unused:', a['id'])
if __name__ == '__main__':
    build()
