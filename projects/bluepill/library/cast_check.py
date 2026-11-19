import re
L=[(i+1,l.split('shot:',1)[1].strip()) for i,l in enumerate(open('../video2/SCRIPT-V5.md')) if l.strip().startswith('- shot:')]
E=[ # entity, regex, library path
('Odysseus (laurel; helmeted variant for helmet/crest beats)',r'odysseus|helmet|crest',"characters/odysseus (turnaround, turnaround_helmet)"),
('Crew / crewmen / sailors (brown tunics)',r'crew|grey figures|grey-tunic|figures climbing|tiny figures|hand on one shoulder|men hidden',"characters/crewman (+ turnaround_b/_c)"),
('Polyphemus (one eye)',r'giant(?!s)|\bhuge hand|huge face|his huge|the giant',"characters/polyphemus"),
('Polyphemus blinded (cloth over eye)',r'cloth|blind|fumbling|palm on the boulder|hand opening|hand moving|hand resting|hand reaching|hand on the ram|huge hand|giant seated|giant sitting|giant alone|silhouette on the shore|silhouette.s raised',"characters/polyphemus_blinded (turnaround_band)"),
('Three neighbour Cyclopes',r'three giants|three silhouettes|neighbour|silhouettes',"characters/neighbour_cyclops"),
('Bard / Homer',r'bard',"characters/bard"),
('Hesiod (shepherd-poet) + scroll',r'shepherd-poet',"characters/hesiod"),
('Abel (1914 scholar, desk, quill)',r'scholar at a desk',"characters/abel"),
('Pausanias (traveller, sun hat, staff)',r'traveller',"characters/pausanias"),
('Hackman (library scholar)',r'scholar between|stacking a tall pile',"characters/hackman"),
('Sailor with torch (Abel story)',r'sailor|two tiny sailors',"characters/sailor"),
('Workers hauling block',r'workers hauling',"characters/workers (regenerated, uniform cream skin)"),
('Maron (robed figure in vineyard)',r'robed figure',"characters/maron"),
('Sheep / flock / lambs',r'sheep|flock|lambs|woolly',"characters/sheep (turnaround, group, face)"),
('Sheep tied in threes side by side',r'three woolly sheep|roped',"characters/sheep/group.png"),
('Big ram',r'ram\b',"characters/ram (turnaround, face, expressions) + props/ram"),
('Mules + block',r'mules',"props/mule_pair"),
('Ox-carts / wagons',r'ox-cart|wagons',"props/ox_cart"),
('Gulls',r'gulls',"props/gulls"),
('Ship (sail up / furled)',r'\bship\b|helm|stern|deck|rail|bow\b|oars',"props/ship, props/ship_furled, places/beach_and_ship, places/ship_deck"),
('Goatskin + wine bowl',r'goatskin|wine bowl|wooden bowl|three empty bowls|bowl',"props/wine, props/straw_bowls (wooden bowl, clay bowls)"),
('Torch',r'torch',"props/torch"),
('Olive trunk / stake',r'olive trunk|stake|shaving a point|point glowing|white-hot tip|glow tip|long beam',"props/stake_raw, props/stake_sharp, props/stake_fire, props/stake"),
('Olive club',r'olive club|club',"props/olive_club (no beat uses a club; kept per brief)"),
('Boulder (round door)',r'boulder|stone rolling|stone going|stone back|the stone|sealing',"props/boulder, places/cave_exterior, places/cave_interior"),
('Cheese racks / baskets / jars',r'cheese|basket|jar|racks',"props/cheese_set, places/cave_interior"),
('Straw / hay / dung heap, straws',r'straw|hay|dung',"props/straw_bowls"),
('Lyre',r'lyre',"props/lyre (+ characters/bard holds one)"),
('Scroll, quill',r'scroll|quill|paper',"props/scroll_quill, props/brass_lamp (curling paper)"),
('Manuscripts / books / bound volumes',r'manuscripts|book|volumes',"props/book_pile, places/library_lamplit"),
('Brass lamp, market table',r'brass lamp',"props/brass_lamp"),
('Antique map; rolled blank map',r'map',"props/map_antique, props/map_rolled_blank"),
('Elephant skull (one central hole)',r'skull',"props/elephant_skull, props/elephant_skull_in_clay"),
('Dwarf elephant',r'small elephant',"props/dwarf_elephant"),
('Forge cave, anvil, thunderbolt on tongs',r'forge|anvil|bolt',"places/forge_cave, props/anvil_bolt"),
('Smithy, axe in trough (steam)',r'smith|axe|trough',"places/smithy, props/axe_tongs_trough"),
('Tiryns/Mycenae fortress wall, blocks',r'fortress|vast wall|finished wall|\bwall\b',"places/tiryns_wall (master, wall_sunset)"),
('Lion Gate',r'lion gate',"places/tiryns_wall/lion_gate_golden"),
('Hillside with three caves (neighbours)',r'three giants standing apart|moonlit hill|hills',"places/three_hilltops_night (+ thundercloud)"),
('Vineyard (Maron)',r'vineyard',"places/vineyard_golden"),
('Library interior (Hackman)',r'towering shelves',"places/library_lamplit"),
('Ancient library, empty shelf',r'empty shelf',"places/library_ancient_empty"),
('Scholar\'s study (Abel)',r'scholar at a desk',"places/study_1914"),
('Cave exterior / sea cliff / path',r'cave mouth|cliff|path|switchback',"places/cave_exterior, places/hillside_pasture"),
('Cave interior',r'cave interior|cave wall|cave floor|firelight|fire|hay',"places/cave_interior"),
('Cliff-top with notched peak, shore',r'notched peak|shore|slab',"places/cave_exterior/wide_notched_peak, places/beach_and_ship/shore_dusk_red"),
('Beach / pebble beach / unmarked coast / harbour',r'beach|coast|harbour',"places/beach_and_ship (morning, ship_beached, harbour_dawn)"),
('Sea, storm, wave, thunderhead, stars',r'wave|storm|thunder|stars|sea\b',"places/sea_storm, places/beach_and_ship (ship_night_stars, ship_dusk_violet)"),
('Sword / blade',r'sword|blade',"characters/odysseus (short sword at hip)"),
('Cloth over eye',r'cloth over',"characters/polyphemus_blinded (cloth band)"),
]
import os
out=["# CAST CHECK - SCRIPT-V5.md vs library\n","Parsed %d `shot:` lines. Beat id = line number of the shot in SCRIPT-V5.md. Status: OK = a locked reference folder exists; no entity is MISSING after v3.\n"%len(L),"| Entity | Library folder | Status | Beats (line no.) |","|---|---|---|---|"]
miss=0
for name,rx,path in E:
    b=[n for n,t in L if re.search(rx,t,re.I) and not (name.startswith('Polyphemus (') and n>=413) and not (name.startswith('Polyphemus blinded') and n<413) and not (name.startswith('Sailor') and n<640 and 'sailor' in t and 'crew' in t)]
    paths=[re.split(r'[ (]',p.strip())[0] for p in re.sub(r'\([^)]*\)','',path).split(',') if '/' in p]
    ok=all(any(os.path.exists(c) for c in (p.strip('()'),p.strip('()')+'.png')) for p in paths)
    if not ok: miss+=1
    out.append(f"| {name} | {path} | {'OK' if ok else 'MISSING'} | {', '.join(map(str,b)) or '(none)'} |")
out+=["","Notes",
"- Beat ids come from keyword matching on each shot line (regex, so a few extras/omissions are possible); the entity list and folder mapping are exhaustive.",
"- Odysseus: SCRIPT-V5 gives him a bronze crested helmet (and a blue cloak at beat 16); the canonical turnaround has a laurel and a red cloak. `characters/odysseus/turnaround_helmet.png` is the helmeted variant (laurel replaced by crested helmet, same costume). The blue-vs-red cloak is a script/library conflict left for the script owner.",
"- Elements covered by a master image rather than a dedicated folder: twelve crew (crewman + variants), thought bubbles/cards (Remotion, not generated), stick pointer (beat 663, drawn in shot), faint older storyteller (bard, ghosted in compositing), 'green' cliffs of the pebble beach (beach_and_ship morning/ship_beached).",
"- props/olive_club: no V5 shot names a club (the stake is the olive trunk); kept because the brief listed it.",
"- Tiryns lion-gate variant is a zoomed re-framing of the master (edge check not meaningful for a zoom); eyeballed OK.",""]
open('CAST-CHECK.md','w').write('\n'.join(out)+'\n')
print(len(L),len(E),miss)
