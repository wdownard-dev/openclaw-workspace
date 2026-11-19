"""Self-check for SCRIPT-V3.md.
Usage: python3 -I selfcheck.py <SCRIPT-V3.md>
1. every beat has a trace line, and every trace names a source id or an explicit ours/gag/structure/tease/callback/disclosure tag
2. scan spoken text and chips against the RESEARCH-V1 'NOT to make' list and other retired wordings
3. assert each of the 18 FIX and 5 UNVERIFIED items from FACTCHECK-V2 is applied (by beat in V3)
4. visual grammar scan
"""
import re, sys

path = sys.argv[1]
BEAT = re.compile(r'^\*\*(\d+)\s*·\s*(NARR|ODY|POLY|CREW|CYC2)\*\*\s+(.*\S)\s*$')
CHIP = re.compile(r'^\*\*(\d+)\s*·\s*TEXT-CHIP\*\*\s+(.*\S)\s*$')
beats = {}
chips = {}
order = []
cur = None
for line in open(path, encoding='utf8'):
    line = line.rstrip('\n')
    if line.startswith('# END MATTER'):
        break
    m = BEAT.match(line)
    c = CHIP.match(line)
    if m:
        cur = int(m.group(1)); order.append(cur)
        beats[cur] = dict(tag=m.group(2), text=m.group(3), visual='', trace='')
    elif c:
        cur = int(c.group(1)); order.append(cur)
        chips[cur] = dict(text=c.group(2), visual='', trace='')
        beats.setdefault(cur, None)
        beats[cur] = None
    elif line.startswith('- visual:') and cur is not None:
        (beats[cur] or chips[cur])['visual'] = line
    elif line.startswith('- trace:') and cur is not None:
        if beats.get(cur):
            beats[cur]['trace'] = line
real = {k: v for k, v in beats.items() if v}
ok = True

print('== 1. beats and trace tags')
print('spoken beats:', len(real), '; chip beats:', len(chips), '; numbering contiguous:', order == list(range(1, len(order) + 1)))
ID = re.compile(r'\b([A-F]\d{1,2}|N\d)\b')
SOFT = re.compile(r'\b(ours|gag|structure|tease|callback|disclosure|dramatised)\b')
no_trace = [k for k, v in real.items() if not v['trace']]
no_source = []
source_only_soft = []
for k, v in real.items():
    t = v['trace']
    has_id = bool(ID.search(t)); has_soft = bool(SOFT.search(t))
    if not has_id and not has_soft:
        no_source.append(k)
    if not has_id and has_soft:
        source_only_soft.append(k)
print('beats with no trace line:', no_trace)
print('beats with a trace but neither a source id nor an ours/gag/structure tag:', no_source)
print('beats with a soft tag and no research id (no factual claim in the line):', source_only_soft)
# a beat with V/E/U marks must have an id
bad = [k for k, v in real.items() if re.search(r'\b[VEU]\b', v['trace']) and not ID.search(v['trace'])]
print('beats with a V/E/U label but no research id:', bad)
if no_trace or no_source or bad: ok = False

print()
print('== 2. retired and forbidden wordings (spoken text, chips and visual notes)')
FORBID = [
    (r'\b(knew|realised|realized|identified) (the|that) (skull|bones|elephant)', 'Greeks identified the skulls'),
    (r'\bsolved\b|\bhave proved\b|\bscientists have\b', 'solved / proved'),
    (r'\bHomer says\b', 'Homer says ...'),
    (r'Cyclops means|means .one eye', 'Cyclops means one eye'),
    (r'\bTilos\b|\bStrabo\b|\bNaples\b|\bPhlegraean\b', 'Tilos / Strabo / Naples'),
    (r'ten years after Troy', 'ten years after Troy'),
    (r'\bunfalsifiable\b|\bbaseless\b', 'unfalsifiable / baseless (unverified quotes)'),
    (r"Poseidon's sons", "Poseidon's sons"),
    (r'\blivestock\b', 'livestock (FIX 92)'),
    (r'\bhammer(s|ed)? out\b', 'hammer out (FIX 78)'),
    (r'unmixed|unblended', 'unmixed (beat 34 clause cut)'),
    (r'Aci Trezza|500,000|half a million', 'Aci Trezza / age (UNVERIFIED 85, cut)'),
    (r'\bArabia\b|\bKorea\b|\bIreland\b|twenty-five', 'Arabia / Korea / Ireland / 25 nations (UNVERIFIED 100)'),
    (r'suspects of their own', 'unresearched promise (UNVERIFIED 109)'),
    (r'\bWitton\b|\bHing\b', 'Witton and Hing named (UNVERIFIED 72)'),
    (r'sailor from 1914', 'sailor from 1914 (FIX 104)'),
    (r'made up\b(?! a few)', '"made up" for the sailor (retired; the disclosure "made a few up" is allowed)'),
    (r'\bMayor notes\b', 'Mayor notes (FIX 63)'),
    (r'and still do', 'and still do (FIX 61)'),
    (r'one great eye', 'Abel eye wording (FIX 64)'),
    (r'\bby trickery\. Not by force', 'V2 beat 42 wording'),
    (r'skull.{0,20}(centimet|inches|foot|feet|cm\b)', 'skull size claim'),
    (r"Polyphemus'?s? cave|Ulysses'?s? cave", 'named Polyphemus cave'),
    (r'\bcyclopia\b', 'cyclopia as explanation'),
    (r'Homer places|Homer locates', 'Homer places Polyphemus in Sicily'),
]
hits = 0
for k in order:
    v = beats.get(k)
    texts = []
    if v:
        texts = [('spoken', v['text']), ('visual', v['visual'])]
    elif k in chips:
        texts = [('chip', chips[k]['text']), ('visual', chips[k]['visual'])]
    for kind, txt in texts:
        for pat, label in FORBID:
            if re.search(pat, txt, re.I):
                hits += 1
                print('  HIT beat %d (%s): %s :: %s' % (k, kind, label, txt[:110]))
print('forbidden-wording hits in spoken/chip/visual:', hits)
# "Sicily" never given as Homer's setting
for k, v in real.items():
    if re.search(r'Sicil', v['text']) and v['tag'] == 'NARR':
        print('  note: beat %d mentions Sicily in the spoken line (check it is not Homer\'s setting): %s' % (k, v['text'][:90]))

print()
print('== 3. FACTCHECK-V2 FIX and UNVERIFIED items: where applied')
T = lambda k: real[k]['text']
V = lambda k: real[k]['visual']
checks = [
    ('FIX 05  Abel imagined sailors, hedged', '62', 'imagined sailors' in T(62) and 'might be where the Cyclops came from' in T(62)),
    ('FIX 10  chip says some lines invented', '04', 'SOME LINES INVENTED' in V(4)),
    ('FIX 11  disclosure wording', '04', "Where he doesn't, we have made a few up" in T(4)),
    ('FIX 24  sword impulse is Odysseus (not crew)', '18-20', real[18]['tag'] == 'ODY' and 'kill him right now' in T(18) and not any(real[k]['tag'] == 'CREW' and 'Kill him' in real[k]['text'] for k in real)),
    ('FIX 29  no number in Odysseus line', '23', T(23) == 'Who helps me carry the stake? Draw lots.'),
    ('FIX 48  mountain, whisker from the rudder', '47-48', 'mountain' in T(47) and 'whisker from the rudder' in T(48) and 'hill' not in T(47)),
    ('FIX 55  years before Ithaca (not rest of poem)', '55', 'years before Odysseus sees Ithaca again' in T(55) and 'rest of the poem' not in T(55)),
    ('FIX 61  caves on Sicily and Malta, no "still do"', '61', 'have turned up in caves on Sicily and Malta' in T(61) and 'still do' not in T(61)),
    ('FIX 63  Alexander line is Discover, not Mayor', '70', 'Discover magazine' in T(70) and 'Mayor' not in T(70) and 'SOURCE: DISCOVER MAGAZINE' in V(70) and 'most Greeks' in T(70)),
    ('FIX 64  no Abel "one great eye" callback', '62-67', not any('Abel pictured' in real[k]['text'] or 'one great eye' in real[k]['text'] for k in real) and 'our version' in T(63)),
    ('FIX 70  Empedocles "reported", not "found"', '74', 'reported such bones' in T(74) and 'found such bones' not in T(74)),
    ('FIX 78  "make the thunderbolt"', '84', 'make the thunderbolt' in T(84)),
    ('FIX 81  Sicilian address; smiths later via Callimachus', '90-91', 'Sicilian address' in T(90) and 'Callimachus' in T(91) and 'packed up' not in T(90)),
    ('FIX 86  love song, not "gives a love life"', '95', 'sing a love song' in T(95) and 'love life' not in T(95)),
    ('FIX 92  wagons and mules', '103', 'wagons and mules' in T(103)),
    ('FIX 93  Cyclopes built it; Mycenae "said to be"', '102', 'said to be theirs' in T(102)),
    ('FIX 94  no "assumed only Cyclopes could move"', '104', 'assumed' not in T(104) and 'credited the Cyclopes' in T(104)),
    ('FIX 104 real skulls, imaginary sailor', '114', 'real skulls, and an imaginary sailor' in T(114)),
    ('UNV 72  Witton and Hing not named, no baseless', '77', 'Witton' not in T(77) and 'baseless' not in T(77) and 'Witton' not in V(77)),
    ('UNV 73  serious doubts, no "unfalsifiable"', '79', 'serious doubts' in T(79) and 'unfalsifiable' not in T(79)),
    ('UNV 85  Aci Trezza cut', 'cut', not any('Aci Trezza' in real[k]['text'] or 'Aci Trezza' in real[k]['visual'] for k in real)),
    ('UNV 100 Hackman-verified places only', '109', all(x in T(109) for x in ('Iceland', 'Portugal', 'Russia', 'Arabian Nights')) and not re.search(r'Arabia\b|Korea|Ireland|twenty-five', T(109))),
    ('UNV 109 unresearched promise cut', '120', 'suspects of their own' not in T(120)),
]
nfix = 0
for label, where, passed in checks:
    print('  [%s] %-52s -> V3 beat %s' % ('OK' if passed else 'FAIL', label, where))
    if not passed: ok = False
    nfix += 1 if passed else 0
print('applied:', nfix, 'of', len(checks), '(18 FIX + 5 UNVERIFIED = 23; UNV 85 is satisfied by the cut)')

print()
print('== 4. visual grammar')
BANNED = r'\b(pan|panning|kick|tilt|tilts|wipe|wiped|push|fade|fades|dissolve|zoom|crossfade|ken burns|shake|whip|slow motion)\b'
vh = [(k, v['visual'][:100]) for k, v in list(real.items()) if re.search(BANNED, v['visual'], re.I)] + [(k, c['visual'][:100]) for k, c in chips.items() if re.search(BANNED, c['visual'], re.I)]
print('banned camera/transition words in visual notes:', vh)
long_quote = [k for k, v in real.items() if re.search(r'full sentence|card with the sentence', v['visual']) and 'no full' not in v['visual']]
print('quote-card notes holding a full sentence:', long_quote)
longest = max((len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", s)), k) for k, v in real.items() for s in re.split(r'(?<=[.?!])\s+', v['text']))
print('longest spoken sentence (words, beat):', longest)
print('ALL CHECKS PASS' if ok and hits == 0 and not vh else 'REVIEW NEEDED (see above)')
