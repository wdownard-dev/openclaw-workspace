import derive
from concurrent.futures import ThreadPoolExecutor
R=(0.45,999)
PF_SCENE="Use the attached image as the exact scene. Keep every rock, block, tree, building, shelf and object in exactly the same position and shape."
def d(*a,**k): return lambda: derive.derive(*a,**k)
J=[
 d('tiryns_lion_gate','places/tiryns_wall/master.png','places/tiryns_wall/lion_gate_golden.png',"zoom in on the gateway of the same fortress at golden hour: the gate with a huge stone lintel and above it a triangular relief slab carved with two standing lions facing each other with a column between them, the giant blocks of the same wall on both sides, warm low gold light, long shadows",thr=R,preface=PF_SCENE),
 d('tiryns_sunset','places/tiryns_wall/master.png','places/tiryns_wall/wall_sunset.png',"the time is sunset: orange and pink sky, long shadows, the wall glowing gold, finished and complete",thr=R,preface=PF_SCENE),
 d('hilltops_thunder','places/three_hilltops_night/master.png','places/three_hilltops_night/thundercloud.png',"add one big dark thundercloud with a faint flash of lightning inside it over the middle hill, moon partly covered by cloud",thr=R,preface=PF_SCENE),
 d('cliff_peak','places/cave_exterior/day_wide.png','places/cave_exterior/wide_notched_peak.png',"add behind the cliff a tall dramatic mountain peak with a clear V-shaped notch in its summit rising above the horizon, and a small flat rocky shore strip by the water; everything else identical",thr=R,preface=PF_SCENE),
 d('ship_night','places/beach_and_ship/ship_at_sea_wide.png','places/beach_and_ship/ship_night_stars.png',"it is deep night: a dark navy sky full of stars, a pale moon, the sea deep blue and calm with silver moon glints; the same ship stays in the same place with the same striped sail, now in moonlight",thr=R,preface="Use the attached image as the exact scene. Keep the ship and composition exactly."),
 d('ship_dusk','places/beach_and_ship/ship_at_sea_wide.png','places/beach_and_ship/ship_dusk_violet.png',"it is dusk: a calm violet sea, a violet and rose sky, the cliff small on the horizon; the same ship in the same place",thr=R,preface="Use the attached image as the exact scene. Keep the ship and composition exactly."),
 d('harbour_dawn','places/beach_and_ship/ship_at_sea_wide.png','places/beach_and_ship/harbour_dawn.png',"it is dawn: a pink-gold sky, the ship sailing out of a sheltered harbour between two headlands, a line of sandstone cliffs on the horizon behind it; same ship with sail up",thr=R,preface="Use the attached image as the exact scene. Keep the ship exactly."),
 d('shore_red','places/beach_and_ship/morning.png','places/beach_and_ship/shore_dusk_red.png',"it is dusk: a burning blood-red and orange sky, the sea glowing deep red, the beach and cliffs in dark silhouette; empty beach",thr=R,preface=PF_SCENE),
 d('deck_dusk','places/ship_deck/master.png','places/ship_deck/dusk.png',"it is dusk: dark sea beyond the rail, a deep violet-blue sky with a first star, soft lantern glow on the deck",thr=R,preface=PF_SCENE),
 d('ship_storm','places/sea_storm/master.png','places/sea_storm/ship_in_storm.png',"add the ship from the second attached image (exact same hull, meander band, prow eye, striped sail) tiny in the distance on the dark water in front of the thunderhead, a speck; the dark wave and cloud stay exactly as they are",thr=R,extra_refs=['props/ship.png'],preface="Use the first attached image as the exact scene."),
 d('map_rolled','props/map_antique.png','props/map_rolled_blank.png',"redraw the same parchment as a rolled-up scroll map, tied with a cord, with one corner unrolled showing completely blank pale parchment, no markings, no drawings, no text",check='none',preface="Use the attached image as the exact object."),
 d('skull_clay','props/elephant_skull.png','props/elephant_skull_in_clay.png',"the same skull front view half embedded in a rough wall of orange-brown clay, only the front of the skull showing, one central hole and no eye sockets, a thin dark torchlit tone",check='none',preface="Use the attached image as the exact object."),
]
with ThreadPoolExecutor(4) as ex:
    [f.result() for f in [ex.submit(j) for j in J]]
