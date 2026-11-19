"""v3 jobs: workers fix, sheep, ram expressions, Maron, new place masters and prop masters. Run: python3 stage_v3.py <group>"""
import json, os, sys, gen
STY = open('../video2/tests/stickfig/prompts/STYLE.txt').read().strip()
PT = " Thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels. No people, no characters, no human figure anywhere."
PL = " Wide view. No people, no characters, no human figure, no animals unless stated. No text, no labels, no watermark."
CH_TAIL = " Thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels."
def job(cid, out, body, size, refs=(), tail=''):
    os.makedirs('prompts', exist_ok=True)
    open(f'prompts/{cid}.txt', 'w').write(STY + ' ' + body + tail)
    return dict(id=cid, out=out, prompt_file=f'prompts/{cid}.txt', size=size, refs=list(refs))
SK = "SKIN RULE: every bare skin area (face, head, neck, chest, arms, hands, legs, feet) is the SAME flat pale cream skin colour as the face, one uniform skin tone across the whole body, exactly like the cream skin of the attached crewman reference; never tan, never orange, never darker than the face."
G = {}
G['fix'] = [
 job('workers_turn_v3', 'characters/workers/turnaround.png', "Character model sheet. Redraw the two labourers of the first attached image with the same poses, rope harnesses, ochre loincloths, wrapped hands, logs under the block and the same layout (top row: A and B hauling a block on logs in side view; bottom row: front view of each), but " + SK + " Worker A: strong stocky build, shaved cream head. Worker B: lean, short black beard, cloth head wrap. Round cream face with two small black dot eyes and no nose. Same ink outline style and same flat shading as the crewman reference (thin dark ink line limbs are NOT used here, bodies are muscular).", '1536x1024', ['characters/workers/turnaround_old.png', 'characters/crewman/turnaround.png'], CH_TAIL),
]
G['sheep'] = [
 job('sheep_turn', 'characters/sheep/turnaround.png', "Character model sheet of the SHEEP of the Cyclops flock, same style as the sheep seen in the attached cave interior (thick rounded cream-white woolly fleece in soft clumps outlined in dark ink, small dark grey-brown face and ears, dark small hooves, short thin dark legs, no horns on the ewes). Top row: an adult sheep in front view, side view and back view, same size, hooves on one baseline. Bottom row left: a small lamb (smaller, same fleece, a little long-legged, in side view and front view). Calm placid deadpan face, two small dot eyes. Nothing else.", '1536x1024', ['places/cave_interior/night_firelight.png'], CH_TAIL + " No people."),
 job('sheep_group', 'characters/sheep/group.png', "Character model sheet, two panels on one cream image. Top panel: a small flock group of exactly SIX sheep (five adults and one lamb) standing close together, slightly overlapping, in a loose cluster seen from the side, varied poses (one grazing, one looking at us). Bottom panel: THREE sheep tied in a row side by side, seen from the side, standing shoulder to shoulder, a rope looped round their bodies linking the three together at the middle, all facing the same way, a thick rope visible between them. Same fleece style as the attached sheep reference.", '1536x1024', ['characters/sheep/turnaround.png'], CH_TAIL + " No people."),
 job('sheep_face', 'characters/sheep/face.png', "Head and shoulders close-up portrait of the same adult sheep, facing front, deadpan flat expression, two small black dot eyes, small dark grey-brown face, dark ears, thick cream fleece around the neck.", '1024x1024', ['characters/sheep/turnaround.png'], CH_TAIL + " No people."),
]
G['ram'] = [
 job('ram_expr', 'characters/ram/expressions.png', "Expression sheet: exactly four heads of the same ram in a single row, evenly spaced, same size, head and neck only, expressions left to right: 1 neutral calm, 2 deadpan (flat unimpressed stare, two small dot eyes), 3 straining (eyes squeezed, teeth gritted, effort lines, head lowered), 4 trotting (head up, proud, ears back, mouth slightly open, cheerful). Same huge curled gold-brown horns and cream fleece as the attached ram.", '1536x1024', ['characters/ram/turnaround.png'], CH_TAIL + " No people."),
]
G['maron'] = [
 job('maron_turn', 'characters/maron/turnaround.png', "Character model sheet turnaround, three views of the same character: front view, three-quarter view and back view side by side, same height, full body, all feet on one shared baseline. The character: Maron, a priest of Apollo, a small human man: round cream face, two small black dot eyes and no nose, white-grey short beard, a long flowing cream-white robe with a purple band at the hem, a wreath of ivy leaves on his head, a wooden walking staff (head height), a small gold sun brooch pinning the robe at one shoulder, leather sandals.", '1536x1024', [], CH_TAIL),
 job('maron_face', 'characters/maron/face.png', "Head and shoulders close-up portrait, neutral expression, facing front. The character: Maron, a priest of Apollo, round cream face, two small black dot eyes and no nose, white-grey short beard, ivy-leaf wreath, cream-white robe with a purple band.", '1024x1024', ['characters/maron/turnaround.png'], CH_TAIL),
]
G['odyhelm'] = [
 job('ody_helmet', 'characters/odysseus/turnaround_helmet.png', "Use the attached turnaround as the exact character. Redraw the same three views of Odysseus with the same blue tunic, gold belt, meander hem, red cloak, sandals and sword, but replace the laurel wreath with a bronze Greek helmet with a tall crest of red horsehair (the script variant worn in the cave and at the stern). Same face, same beard, same layout and ink style.", '1536x1024', ['characters/odysseus/turnaround.png'], CH_TAIL),
]
P = lambda cid, f, body, size='1536x1024', refs=(): job(cid, f, body, size, refs, PL)
G['places'] = [
 P('forge_cave', 'places/forge_cave/master.png', "A smoky Bronze Age forge cave, deep rough stone cave interior, a huge stone anvil on a tree stump in the centre, a glowing orange forge hearth with bellows on the right, heavy hammers and tongs hanging on the wall, a rack of glowing metal bars, sparks drifting in the air, thick dark smoke, lit by red-orange forge glow with deep blue-black shadows. Empty of figures: no giants, no people."),
 P('smithy', 'places/smithy/master.png', "A small ancient smith's workshop at night, rough stone and timber walls, a glowing forge hearth, an anvil, hanging tools, and in the front a wooden water trough on a stand, an axe lying beside it. Lit by orange forge glow and cold blue moonlight through a window. Empty of figures."),
 P('tiryns_wall', 'places/tiryns_wall/master.png', "A Bronze Age Mycenaean fortress on a hill at noon, a massive cyclopean wall of giant rough sandstone blocks of different sizes fitted together, a stone-paved ramp climbing to a gateway, dry golden grass and a few olives on the hillside, bright clear blue sky, strong sun. Empty of figures."),
 P('three_hilltops_night', 'places/three_hilltops_night/master.png', "A moonlit landscape at night: three separate rounded hills in a row, each with its own dark cave mouth in its face and a faint warm glow inside, a big bright full moon in a deep blue star-filled sky, silver moonlight on pale rocky slopes, valleys between the hills, sea glint far behind. Empty of figures."),
 P('vineyard_golden', 'places/vineyard_golden/master.png', "A Greek hillside vineyard at golden hour, terraced rows of grape vines heavy with dark purple grapes on wooden stakes, a small stone shrine with a clay jar beside it, olive trees, warm low gold light, long shadows, distant sea and a soft peach sky. Empty of figures."),
 P('library_lamplit', 'places/library_lamplit/master.png', "A towering Victorian-era university library interior at night, floor-to-ceiling dark wooden shelves packed with bound leather volumes, a rolling wooden ladder, a brass reading lamp glowing on a table, warm lamplight with deep blue-black shadows, dust motes. Empty of figures."),
 P('library_ancient_empty', 'places/library_ancient_empty/master.png', "An ancient stone library chamber, rough dressed sandstone walls with recessed wooden shelves, one wide empty shelf in the centre with no scrolls on it, dusty, a few cobwebs, soft cool light from a high window, an otherwise bare room. Empty of figures."),
 P('study_1914', 'places/study_1914/master.png', "A 1914 scholar's study: a large wooden desk by a window with an inkwell, quill pen, open papers, stacked books and a green-shaded lamp, a bookcase behind, a rug, warm evening light, dark panelled walls. Empty of figures, nobody seated."),
 P('sea_storm', 'places/sea_storm/master.png', "A night sea with a storm brewing: a huge dark wave rising in the foreground, towering black thunderhead cloud over the horizon lit from inside by a flash of lightning, a deep blue and black sea with white foam, a few stars at the top. No ship, no figures."),
 P('ship_deck', 'places/ship_deck/master.png', "The deck of an ancient Greek ship in bright morning light seen from the stern: wooden planks, a gold meander-patterned stern rail, a large steering oar at the stern, the mast with a furled blue-and-white striped sail ahead, rowing benches, calm blue sea beyond the rail. Empty of figures."),
]
G['props'] = [
 job('torch', 'props/torch.png', "A single wooden torch: a rough wooden shaft wrapped with pitch-soaked cloth at the top, burning with a bright orange flame and a little smoke, shown upright on cream.", '1024x1024', [], PT),
 job('olive_club', 'props/olive_club.png', "A rough olive-wood club: a thick gnarled length of olive branch with bark, thicker at one end, a hand-worn grip, shown lying diagonally on cream.", '1024x1024', [], PT),
 job('cheese_set', 'props/cheese_set.png', "A set of cave-dairy objects arranged together: a stack of three big round pale yellow cheese wheels, a round woven wicker basket with a striped woollen cloth in it, and a tall stone water jar with two handles, all on cream.", '1536x1024', [], PT),
 job('lyre', 'props/lyre.png', "A Greek lyre: a curved tortoise-shell body, two curved wooden arms with a crossbar, seven taut strings, in a warm brown, shown upright on cream.", '1024x1024', [], PT),
 job('scroll_quill', 'props/scroll_quill.png', "A rolled papyrus scroll partly unrolled with blank lines of nothing, beside a long white quill pen and a small clay inkwell, on cream. No writing.", '1024x1024', [], PT),
 job('book_pile', 'props/book_pile.png', "A tall wobbling pile of old leather-bound books and manuscripts, different sizes and colours (deep blue, burgundy, green, ochre), stacked about a metre high, some with ribbons, on cream. No titles, no text.", '1024x1024', [], PT),
 job('brass_lamp', 'props/brass_lamp.png', "A polished brass oil lamp shaped like a genie lamp with a curved spout and handle, next to a curling sheet of old paper with a rolled edge, both on a small rug-covered market table top shown from the front, on cream. No text on the paper.", '1024x1024', [], PT),
 job('elephant_skull', 'props/elephant_skull.png', "An elephant skull in FRONT view: a large pale bone-coloured skull with exactly ONE single big round hole in the centre of the forehead (the nasal opening), NO eye sockets visible anywhere, two curved tusks at the bottom, cracked bone texture, on cream.", '1024x1024', [], PT),
 job('dwarf_elephant', 'props/dwarf_elephant.png', "A small dwarf elephant standing in side view, about the size of a pony, grey skin with wrinkles, short tusks, small round ears, calm, on cream.", '1024x1024', [], PT),
 job('mule_pair', 'props/mule_pair.png', "A pair of brown mules in harness standing side by side in side view, leaning into leather and rope harness straining forward, ropes leading to the left toward a huge rough sandstone block (a big square cut stone block, rope-bound, on the left edge of the image). Mules look strained and stubborn.", '1536x1024', [], PT),
 job('ox_cart', 'props/ox_cart.png', "A small ancient wooden ox-cart: two big solid wooden wheels, a plank bed with low rails, a yoke pole, a pair of pale oxen in front in side view, all in a warm brown and cream. Shown in side view on cream, small and simple.", '1536x1024', [], PT),
 job('axe_tongs_trough', 'props/axe_tongs_trough.png', "Smithing objects together: a bronze axe head glowing orange-hot held in iron tongs, over a rough wooden water trough with water, a small cloud of steam rising, on cream.", '1536x1024', [], PT),
 job('map_antique', 'props/map_antique.png', "An antique parchment map in sandstone and gold tones, a Mediterranean-style coastline with islands and sea in pale teal, gold border, compass rose, and small painted pictures on the water and land: a longship, a caravel with three sails, an onion-domed church. No text, no letters, no labels, no writing anywhere on the map.", '1536x1024', [], PT),
 job('gulls', 'props/gulls.png', "A flock of five white seagulls with grey wings and yellow beaks in flight, in varied poses, wings spread, side views, on cream.", '1024x1024', [], PT),
 job('anvil_bolt', 'props/anvil_bolt.png', "A heavy dark iron anvil on a stump, a big forging hammer leaning on it, iron tongs holding a glowing white-gold zigzag thunderbolt shaped bolt of metal with sparks, on cream.", '1536x1024', [], PT),
 job('straw_bowls', 'props/straw_bowls.png', "Small cave objects together: a messy heap of straw and hay, four straws of different lengths held in a fan (just the straws, no hand), a row of three empty shallow clay bowls, and one plain round wooden bowl, on cream.", '1536x1024', [], PT),
]
if __name__ == '__main__':
    jobs = G[sys.argv[1]]
    json.dump(jobs, open(f'jobs_v3_{sys.argv[1]}.json', 'w'), indent=1)
    from concurrent.futures import ThreadPoolExecutor
    import time
    with ThreadPoolExecutor(4) as ex:
        fs = []
        for j in jobs:
            fs.append(ex.submit(gen.run, j['id'], j['out'], j['prompt_file'], j.get('refs', []), j.get('size', '1024x1024'))); time.sleep(1.5)
        [f.result() for f in fs]
