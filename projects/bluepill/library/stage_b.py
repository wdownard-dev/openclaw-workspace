import derive, gen, os, sys
from concurrent.futures import ThreadPoolExecutor
STY=open('../video2/tests/stickfig/prompts/STYLE.txt').read().strip()
PF="Use the attached image as the exact object. Keep its exact shape, colours, outline, planking, meander band, oar holes, eye on the prow and sail stripes."
def ship_furled(): return derive.derive('ship_furled','props/ship.png','_work/ship_furled.png',"ONLY the sail: it is furled, rolled up tightly along the yard into a neat horizontal bundle, and the blue and white vertical stripes are still clearly visible wrapped around the rolled bundle. The hull, meander band, oar holes, eye, mast and rigging are identical",thr=(0.8,999),preface=PF)
def ship_beached(): return derive.derive('ship_beached','places/beach_and_ship/morning.png','_work/ship_beached.png',"add the ship from the second attached image (ship master) onto the beach, hauled up on the sand, in side view with its sail furled but the blue and white vertical stripes still visible rolled on the yard, seven oar holes, meander band and prow eye exactly as in the ship master image, oars stacked beside it. The beach, cliffs, sea and sky of the first image stay exactly as they are",thr=(0.5,999),extra_refs=['props/ship.png'],preface="Use the first attached image as the exact scene.")
def ship_sea(): return derive.derive('ship_sea','props/ship.png','_work/ship_sea.png',"place this exact same ship (identical hull, meander band, seven oar holes, prow eye and blue-and-white vertical striped sail raised) sailing on open deep blue Aegean sea in a bright day, wide view with distant cliffs far behind, oars out through the oar holes, no crew; the sea and sky fill the full frame instead of the cream background",check='none',preface=PF)
def stake_raw():
    open('prompts/stake_raw.txt','w').write(STY+" A single raw olive tree trunk, a thick straight length of olive wood with bark, both ends cut flat, lying horizontally on plain cream, no hands. Thick dark ink outline, flat warm shading. Plain flat cream background, no scenery, no text, no labels. No people, no characters.")
    gen.run('stake_raw','props/stake_raw.png','prompts/stake_raw.txt',[],'1536x1024')
def boulder(): return derive.derive('boulder_prop','_work/boulder_crop.png','_work/boulder_prop.png',"remove everything except the boulder: erase the rock cliff and cave behind it and any ground, put the boulder alone on a plain flat cream background with a soft shadow under it. The boulder itself keeps its exact shape, cracks, colours and shading",check='none',preface="Use the attached image as the exact boulder.")
if __name__=='__main__':
    with ThreadPoolExecutor(4) as ex:
        fs=[ex.submit(f) for f in (ship_furled,ship_beached,ship_sea,stake_raw,boulder)]; [f.result() for f in fs]
