import derive, gen, os, shutil, sys
from concurrent.futures import ThreadPoolExecutor
STY=open('../video2/tests/stickfig/prompts/STYLE.txt').read().strip()
os.makedirs('_work',exist_ok=True)
def ship():
    p='prompts/ship_master.txt'
    open(p,'w').write(STY+" A single ancient Greek wooden ship, side view, sail up, full ship shown on plain cream, no water, no scenery. ONE fixed design: dark teal-blue hull with a wide gold Greek meander (key) band along the top of the hull, a row of exactly seven round dark oar holes in a line below the meander band along the whole length of the hull, brown wooden planking below, a carved curled prow with a large painted eye on the prow, a tall single mast with a SQUARE sail fully raised and unfurled, the sail has bold vertical stripes alternating deep blue and white from top to bottom, wooden yard across the top, rope rigging, stern curved up. Thick dark ink outline, flat warm shading. No people, no characters. No text, no labels, no watermark.")
    gen.run('ship_master','props/ship.png',p,[],'1536x1024')
J={
 'ext_dusk':lambda: derive.derive('ext_dusk','places/cave_exterior/day_wide.png','_work/ext_dusk.png',"the sky to deep dusk with an orange sun on the horizon over the sea, orange and purple clouds, warm low orange light and long shadows over the whole scene",mode_thr=None) if False else derive.derive('ext_dusk','places/cave_exterior/day_wide.png','_work/ext_dusk.png',"the sky to deep dusk with an orange sun low on the horizon over the sea, orange and purple clouds, warm low orange light with long shadows across the whole scene",thr=(0.45,999)),
 'ext_sealed':lambda: derive.derive('ext_sealed','places/cave_exterior/day_wide.png','_work/ext_sealed.png',"the huge round grey boulder is rolled to the right so that it completely covers and seals the dark cave mouth. The empty spot where the boulder rested beside the mouth shows plain rock ground. The sky and lighting stay exactly the same bright midday",thr=(0.8,12)),
 'int_day':lambda: derive.derive('int_day','places/cave_interior/night_firelight.png','_work/int_day.png',"the fire is cold: no flames and no glow, only grey ash and a few dark charred logs in the stone ring. A single shaft of pale daylight falls from a small hole in the ceiling onto the floor, soft cool dim daylight ambience replaces the orange firelight. The boulder still seals the back",thr=(0.45,999)),
 'int_open':lambda: derive.derive('int_open','places/cave_interior/night_firelight.png','_work/int_open.png',"the huge round boulder at the back is rolled aside to the right, uncovering the cave mouth, and bright daylight pours in through the open mouth at the back, lighting the floor. The fire is cold: no flames, only grey ash and charred logs",thr=(0.45,999)),
 'hill_dawn':lambda: derive.derive('hill_dawn','places/hillside_pasture/dusk.png','_work/hill_dawn.png',"the sky and light to early dawn: pale pink and soft gold sky with a rising sun at the horizon, cool misty blue shadows, dew on the grass",thr=(0.45,999)),
 'beach_empty':lambda: derive.derive('beach_empty','places/beach_and_ship/morning.png','_work/beach_empty.png',"remove the ship completely, including its oars, mast, sail, ropes and the wooden blocks under it, leaving smooth empty beach sand where the ship was. Sky, light, cliffs, sea and rocks stay exactly the same",thr=(0.8,12)),
 'ship':ship,
}
if __name__=='__main__':
    names=sys.argv[1:] or list(J)
    with ThreadPoolExecutor(4) as ex:
        fs=[ex.submit(J[n]) for n in names]; [f.result() for f in fs]
