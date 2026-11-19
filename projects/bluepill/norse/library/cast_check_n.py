import re,json,collections
SC='../SCRIPT-N-LOCKED.md'
lines=open(SC).read().split('\n')
beat=None; rows=[]
for l in lines:
    m=re.match(r'\*\*(N-\d+)\*\*',l)
    if m: beat=m.group(1)
    if l.strip().startswith('- state:'): rows.append((beat,l.split('state:',1)[1].strip()))
CH=[ # regex, card id (None = prompt text by design)
(r'^Odin \(one eye\)','odin_one_eye'),(r'^Vili$|^Ve$','vili_ve'),(r"^Ymir's body",'ymir_dead'),(r'^Ymir','ymir'),(r'^Audhumla','audhumla'),
(r'dwarfs$','dwarf'),(r'^(Ask|Embla|Lif|Lifthrasir)$','ask_embla'),(r'^Loki \(bound\)','loki_bound'),(r'^Loki as a salmon','loki_salmon'),(r'^Loki as an old woman','loki_old_woman'),(r'^Loki','loki'),
(r'giantess','giantess'),(r'^Fenrir \(cub\)','fenrir_cub'),(r'^Fenrir \(young\)','fenrir_young'),(r'^Fenrir \(bound\)','fenrir_bound'),(r'^Fenrir','fenrir_grown'),
(r'^Hel','hel'),(r'^Tyr \(hand\)','tyr_hand'),(r'^Tyr \(stump\)','tyr_stump'),(r'^Thor','thor'),(r'^Hymir','hymir'),(r'^Baldr \(dead\)','baldr_dead'),(r'^Baldr','baldr'),
(r'^Frigg','frigg'),(r'^Hod','hod'),(r'^Sigyn','sigyn'),(r'^Surt','surt'),(r'^Heimdall','heimdall'),(r'^Vidar','vidar'),(r'^Garm','garm'),(r'^(Modi|Magni)$','modi_magni'),
(r'^Snorri','snorri'),(r'poet|scribe','skald_scribe'),(r'eagle|dragon|squirrel','eagle_nidhogg_ratatosk'),
(r'^Jormungandr|^the serpent$','jormungandr'),(r'^serpent$|serpent on the roof','PROMPT:cave serpent (pale yellow)'),
(r'hands raised|standing on the ground','PROMPT:crowd/pose text'),(r'three listeners','PROMPT:plain listeners'),(r'two wolves','PROMPT:sun-wolves (rust-brown)'),(r'hooded rider','PROMPT:Hermod, hooded rider on grey horse')]
PL=[ (r'^Asgard grounds','asgard_grounds'),(r'^Asgard hall','odins_hall / odins_hall_day'),(r'^Asgard wall','asgard_wall_night'),(r'^Asgard','asgard'),(r"^Baldr's bed",'bedroom'),
(r"^Fenrir \(bound\)'s rock",'fenrirs_rock'),(r"^Fenrir \(huge\)'s rock",'fenrirs_rock_night'),(r'^Fensalir','fensalir_door'),(r'^Ginnungagap|^the empty gap','cosmic_gap'),(r'^the gap, where ice','cosmic_gap_melt'),
(r"^Hel's gate",'hels_gate'),(r'^Hel$','hels_gate_day'),(r"^Hymir's farm",'hymirs_farm'),(r'^Jotunheim','jotunheim_home'),(r"^Mimir's well",'mimirs_well'),(r"^Odin's hall",'odins_hall'),
(r'^Reykholt','reykholt_study'),(r'^Vigrid','vigrid_plain'),(r'^Yggdrasil','yggdrasil / yggdrasil_trunk / yggdrasil_animals'),(r"^Ymir's body",'new_world'),(r'^a beach on Midgard|^the shore','midgard_shore (+evening/dusk)'),
(r'^a burning ship','open_sea_burning'),(r'^a cave','cave_day'),(r'^a dark cave','loki_prison'),(r'^a forest','new_world_forest'),(r'^a green hill','new_world_greenhill'),(r'^a hall in Iceland','iceland_room'),
(r'^a meadow','asgard_meadow'),(r'^a road through hills','hill_road_farm'),(r'^a scriptorium','scriptorium'),(r'^a small boat','open_sea_boat_morning / open_sea_boat_midday'),(r'^a waterfall','waterfall'),
(r'^an empty sea|^sea$|^the sea$','open_sea (+night)'),(r'^an oak','oak_mistletoe (prop)'),(r'^dwarf forge','dwarf_forge'),(r'^the hill','new_world_hill_day'),(r'^the ice field','ice_field'),
(r'^the new world|^the world','new_world (+dusk/snow/burning)'),(r'^the sky','night_sky (+skull/crack)')]
def split_names(txt):
    out=[];d=0;cur=''
    for c in txt:
        if c=='(':d+=1
        if c==')':d-=1
        if c==',' and d==0: out.append(cur.strip());cur=''
        else: cur+=c
    if cur.strip(): out.append(cur.strip())
    return out
cards={}; missing=[]; chars=collections.Counter(); places=collections.Counter(); promptonly=collections.Counter()
thor_dis=[]; armed=[]
for b,s in rows:
    parts=[p.strip() for p in s.split(';')]
    loc=parts[0]; hit=None
    for rx,pid in PL:
        if re.search(rx,loc): hit=pid;break
    places[(loc,hit)]+=1
    if not hit: missing.append(('PLACE',b,loc))
    m=re.search(r'present:\s*(.*?);',s+';')
    names=split_names(m.group(1)) if m else []
    for n in names:
        h=None
        for rx,cid in CH:
            if re.search(rx,n): h=cid;break
        if h is None: missing.append(('CHAR',b,n)); continue
        if h.startswith('PROMPT:'): promptonly[(n,h[7:])]+=1; continue
        cards[n]=h; chars[(n,h)]+=1
    if 'Thor' in names and ('disguise' in s or re.match(r'^(a road through hills|Hymir|a small boat)',loc)): thor_dis.append(b)
    nb=int(b.split('-')[1]) if b else 0
    if 144<=nb<=146 and any(n.startswith('Odin') for n in names): armed.append(b)
json.dump(cards,open('cards.json','w'),indent=1,sort_keys=True)
o=['# CAST-CHECK (Norse)\n',f'State lines read: {len(rows)} from `norse/SCRIPT-N-LOCKED.md`. **MISSING: {len(missing)}**\n']
if missing: o+=['\n## MISSING\n']+[f'- {k} {b}: {n}\n' for k,b,n in missing]
o.append('\n## State name -> card id (cards.json)\n\n| state name | card id | uses |\n|---|---|---|\n')
for (n,c),k in sorted(chars.items()): o.append(f'| {n} | `{c}` | {k} |\n')
o.append('\n## Prompt-text figures (no card, by design)\n\n| state name | prompt text | uses |\n|---|---|---|\n')
for (n,c),k in sorted(promptonly.items()): o.append(f'| {n} | {c} | {k} |\n')
o.append('\n## Location -> place id\n\n| state location | place id(s) | uses |\n|---|---|---|\n')
for (l,p),k in sorted(places.items(),key=lambda x:x[0][0]): o.append(f'| {l} | `{p}` | {k} |\n')
o.append('\n## Beat-level overrides the state names do not carry (rule 21 gaps; script patch needed)\n')
o.append(f'- Thor in disguise: `state:` says "Thor" and only the shot line says "in disguise". Beats to override to `thor_disguise` (library says N-081 to N-100 in the wardrobe numbering; matching state lines in this script): {", ".join(sorted(set(thor_dis)))}\n')
o.append(f'- Odin armed: `state:` says "Odin (one eye)". Beats to override to `odin_armed`: {", ".join(armed)}\n')
o.append('- Fenrir (bound) with sword in jaws: `state:` says "Fenrir (bound)"; the sword beats (wardrobe N-078-079) need `fenrir_bound_sword`; the state line must name it.\n')
o.append('- "Thor" in other beats = `thor`; "Hymir", "Hymir (scale 3.0)" = `hymir`.\n')
open('CAST-CHECK.md','w').write(''.join(o))
print('rows',len(rows),'missing',len(missing)); print(missing[:10]); print(sorted(set(thor_dis)),armed)
