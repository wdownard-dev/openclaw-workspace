# WARDROBE.md (Baba Yaga, video 3): text checkpoint before any image is generated

Status: DRAFT for William. Text only; no images, audio, spend or messages. Beat ids and `state:` lines come from `babayaga/SCRIPT-B-draft2.md` (gate 2 cleared 11/18: "length is fine, let's work on the picture library"). The cast was rebuilt from the script's `state:` lines, not from `CAST.md`; where they differ I say so. Card spec and rule 21 from `PROCESS.md` Stage 3 and rule 21. Format follows `norse/library/WARDROBE.md`.

**Locator caveat.** Source locators are the ones already in the script's `trace:` lines: **W** = Wheeler 1912 "Wassilissa the Beautiful"; **R** = Ralston 1873 "The Baba Yaga" pp.139-142 and "Vasilissa the Fair" pp.150-158; **A** = Afanasyev no.104 (Vasilisa) and no.103 (the aunt tale). I did not re-read the texts in this pass. Anything that comes from my memory of the tradition rather than from a `trace:` line is marked `(verify)`. No source fixes a costume colour: every colour below is OURS. Where a tell is traditional I say so.

**Style rule for every identity line.** Round cream face, two small black dot eyes, no nose, thick dark ink outline, flat warm shading, simple stick-figure body with chunky hands (`odysseus/CHARACTER.md`, `STYLE.txt`). Deliberate exceptions, listed: Baba Yaga's hooked nose (the only nose in the cast). Plain cream card background, no text on the figure.

**Colour rule (script header).** Palette: night blue-black, ember orange, bone cream. Ember orange is light only (skull lamp, candle, and the doll's eyes, which the script says light up "like two candles"). WHITE, RED and BLACK are reserved for the three riders. Fence skulls glow cold pale white, never orange. So no other figure, animal or prop is pure white, red or black. Bone cream, cream linen and dark umber/plum/teal are fine. Conflicts found and fixed are in section 1.3.

---

## 1. Card table

Counts: **21 character and creature cards** (4 FULL, 15 SIMPLE, 2 derived: `baba_yaga_mortar`, `doll_lit`) **plus 5 prop masters and 1 derived prop** (`candle_snuffed`) = **27 card ids**. Brief's expected set adjusted to what the script shows: no merchant father card (he never appears in any `state:` line), no "grown Vasilisa" card (header: one Vasilisa card in every beat), one cat card, one card for the two dogs, one maid.

Tier key: FULL = front + three-quarter turnaround + one face close-up (2 images). SIMPLE = one front image (the riders use one three-quarter gallop view instead). Derived = one edit of an existing card. Tier rule used: FULL when a character has 10 or more beats AND a face close-up shot, or when the face carries the identity (Baba Yaga); everything else SIMPLE.

Scale: Vasilisa 1.0 is the human reference and is the SMALLEST figure in every frame (script header, B-002). Beats are the beats where the figure is present per the `state:` lines (computed by script from the `state:` parentheses, plus the few shots that show a figure the state line does not list: noted).

### 1.1 Tale 1 people

#### `baba_yaga` | FULL | scale 1.15 (hunched; about 1.35 if she stood straight) | 53 beats
- Beats on foot: B-039–046, B-052–056, B-060–078, B-099–100, B-104–108, B-112, B-114, B-115–118 (pose: lying on the stove B-039–045, springing up B-073, at the loom B-099). In the mortar: see `baba_yaga_mortar`. B-047 (whistles, mortar flies to her) is this card plus the prop.
- Traditional iconography: old witch, long and bony; throws herself on the stove and "stretched out her bony legs" (W p.42 V); iron mortar, pestle, broom (W p.41; R p.153-154; A "в ступе... пестом... помелом"); smells Russian flesh (W p.41); grinds her teeth in fury (W p.50 V); hut on fowl's legs (R p.138 V). The BONE LEG ("Yaga Bony-leg", Afanasyev's epithet "костяная нога") and the HOOKED NOSE are standard Baba Yaga iconography; neither is in the text of this tale; Ralston's introduction p.138 discusses her (verify). The competing video (REF-SLAVIQUE 2:51) uses hunched, hook nose, bony leg, ash-stained rags: we keep the same traditional tells but draw them in our style.
- Which tells are bold enough: **keep** (1) tall hunched stoop, (2) a long hooked nose in profile and three-quarter (the single exception to "no nose": it carries every close shot, B-034 "long nose high", B-036), (3) wild grey hair streaming loose and uncovered, (4) ONE bone leg: a thick bone-cream shaft with knobbed joints and a bare bone foot sticking out from a ragged hem, the other leg in a dark rag boot (reads in the wide stove shot B-039 "one thin pale leg hanging off" and the mortar shot B-034 "one thin pale leg showing"), (5) dark umber shawl over ash-grey-brown rags, (6) an iron-grey pestle in her fist. **Face close-up only:** iron-grey pointed teeth (B-065, B-066, B-073, B-078, B-115–116 "teeth bared / grinding teeth"). Teeth at 540p in a wide shot are a few pixels; they live on the face card, not the identity line. **Dropped:** warts, rings, bone necklace, wrinkles detail.
- Why a stranger knows her: stooped silhouette, hooked nose, wild grey hair, and a bone-white leg that no other figure has.
- **Identity line:** `Baba Yaga: tall hunched old woman, long HOOKED nose in profile (the only nose in the cast), wild loose grey hair, dark umber shawl over ash-grey-brown rags, ONE bare leg a thick bone-white shaft with knobbed joints (the other in a dark rag boot), a long iron-grey pestle in her fist.`
- Silhouette: hunched back + hooked nose + streaming hair + one pale leg. Nobody else has hair out or a nose.
- Risk: umber is dark; at night keep her readable by the pale hair and bone leg (section 5).

#### `baba_yaga_mortar` | derived from `baba_yaga` + `mortar_pestle_broom` (1 image) | scale 1.15 plus the mortar (mortar 0.9 high; overall figure about 1.75) | 9 beats
- Beats: B-033–038 (bursts out of the forest, arrives, sniffs, bargains, rides through the open gate), B-048 (drives away, gate open), B-051 (drives in at dusk), B-119 (approaches the gate). Rule 21: card id `baba_yaga_mortar` for these beats, `baba_yaga` for all others.
- Why a derived card: standing in the mortar hides the legs and the bone leg, so the plate generator must not be asked to composite two cards. One image, edit of the Baba Yaga card inside the mortar prop, pestle driving, broom trailing behind.
- **Identity line:** `Baba Yaga in her mortar: the same hunched grey-haired woman, hooked nose, dark umber shawl, standing waist-deep in a big iron-grey mortar, driving it with the pestle, a twig broom sweeping behind. (Her bone leg is hidden; the knobbed bone foot may poke over the rim.)`

#### `vasilisa` | FULL | scale 1.0 (reference; smallest in every frame) | 84 beats (most-used card)
- Beats: B-002, B-006–012, B-014–027, B-029–057, B-060–073, B-075–082, B-085–087, B-093–094, B-111–112, B-116–117, B-124, B-126.
- ONE card for every beat (script header; CAST card 2 said "eight", which the hook no longer says). At the deathbed (B-014–017, age eight) the plate prompt scales her to 0.65 with the same costume; no second card (section 4 and open question 1). The script's own line (B-018): "One Vasilisa card is used in every beat; no grown variant."
- Traditional iconography: Vasilisa the Beautiful/Fair, in Russian folk costume: sarafan (pinafore dress) and a kerchief; the doll in her pocket (A "положила куколку в карман"; W p.39); in W/A/R she is of marrying age at the errand (A "стала невестой", W p.35). The long maiden's braid is the standard Slavic girl's look; the kerchief is the script's (B-002 "a pale kerchief").
- Why a stranger knows her: the smallest figure, a blue sarafan, a pale kerchief, one long braid, and the little doll in her pocket.
- **Identity line:** `Vasilisa: young woman and the smallest figure in every frame, round cream face, dot eyes, pale lavender kerchief, ONE long brown braid over the shoulder, cornflower-blue sarafan with a cream embroidered hem, bare brown boots, a tiny doll in her apron pocket.`
- Silhouette: small + kerchief + braid. The only cornflower blue in the cast.
- Doll is in the pocket (not in the hand) except B-014–016, B-020, B-044, which are doll-centred shots (the doll card appears).

#### `vasilisas_mother` | SIMPLE | scale 1.1 reclining in a bed | 4 beats
- Beats: B-014–017.
- Traditional iconography: the dying mother who blesses her daughter and leaves her the doll (A "родительское благословение"; R p.150; W p.31). No dress is traditional; the pale, raised-hand look is the script's (B-014, B-017).
- **Identity line:** `Vasilisa's mother: pale woman with long dark-brown hair loose on the pillow, cream linen nightdress, one thin hand raised in blessing, kind weak smile, lying propped in a bed.`
- Note: cream nightdress, not white (colour rule). The blanket is part of the `house_room_deathbed` place.

#### `doll` | SIMPLE | scale 0.13 (a palm-sized doll that fits Vasilisa's pocket; enlarged in close-ups) | 11 beats
- Beats (eyes unlit): B-014–016, B-020, B-044. Lit variant: see `doll_lit`.
- Traditional iconography: the little doll (A "куколка", W "tiny doll", W says "wooden doll" in places; SPINE note 9 chose "doll"), fed a crumb, speaks and works (W p.43; A; R p.153).
- **Colour conflict:** `CAST.md` gave it a red dress. Red is reserved for the Red Rider. Fix: **ochre-gold dress** with a rust-brown hem. See 1.3.
- **Identity line:** `The doll: tiny round-headed rag doll, plain cream face with two dot eyes, a small ochre-gold dress with a rust-brown hem, stubby cloth arms, no hair.`

#### `doll_lit` | derived from `doll` (1 image) | scale 0.13 | beats where the eyes glow
- Beats: B-021–023, B-045, B-050, B-057.
- The eyes glow ember orange "like two candles" (A; R p.153): the only warm light on the doll, tiny circles of ember. Lit while it speaks, walks (in the pocket at B-023) or works (B-050, B-057); unlit while it is simply fed or held (B-014–016, B-020, B-044). Rule 21 says exact card per beat, so lit and unlit are two cards, not a prompt choice.
- **Identity line:** `The doll (eyes lit): the same ochre-gold rag doll, but both dot eyes are glowing ember-orange circles; nothing else changes.`

#### `stepmother` | FULL | scale 1.15, the WIDEST figure | 11 beats
- Beats: B-005, B-018–019, B-083–090 (B-092 shows her as ash: no figure).
- Traditional iconography: the wicked stepmother who puts out every fire and plots the errand (W p.37; A; R p.152). No costume source; the dress colour is the script's ("dark red", B-005) and breaks the colour rule.
- **Colour conflict:** the shot line B-005 and `CAST.md` say dark red dress. Red is reserved for the riders. Fix: **deep aubergine (dark purple) dress**, plum-brown kerchief. Aubergine still reads as dark, wide and lit-from-below in firelight (B-005, B-087).
- **Identity line:** `Stepmother: broad stout woman in a deep AUBERGINE-purple long dress, hair fully covered by a plum-brown kerchief, thick folded arms, stern pinched mouth, wider than anyone else.`
- Silhouette: widest, long skirt, covered head.

#### `stepsister_a` | FULL (face close-up needed at B-009) | scale 1.1, SHORT and ROUND | 14 beats
- Beats: B-006–012, B-083–084, B-086–090 (B-088 "in the doorway").
- Traditional iconography: the two daughters sit at their work (W p.37: lace-making and knitting; W p.38 "steel pins", "silver needles"; A; R p.152). She is the one who snuffs the candle (B-008): the script says "one stepsister"; I give the job to A (the lace-maker with the pins) so each sister has one signature prop and one job.
- **Identity line:** `Stepsister A (lace-maker): short round broad girl, bare head with two round brown buns at the sides, MUSTARD-yellow blouse with cream dots over a brown skirt, thick fingers, holds a lace pillow stuck with steel pins.`
- Silhouette: short, round, two side buns.

#### `stepsister_b` | SIMPLE (upgrade to FULL only if the 540p test shows she and A look alike) | scale 1.3, TALL and THIN | 11 beats
- Beats: B-006–012, B-083–084, B-089–090.
- **Identity line:** `Stepsister B (knitter): tall thin girl, bare head with ONE tall brown topknot bun, dark TEAL long dress, holds two long knitting needles and a grey stocking.`
- Silhouette: tall, thin, topknot. The pair reads as two by height, width, hair, colour, and the prop in the hands (pins and pillow versus needles and stocking, B-011).
- Changed from `CAST.md` ("matching pair... distinct kerchief colour"): the sisters now share no feature; neither wears a kerchief (so neither can be mistaken for Vasilisa or the stepmother).

### 1.2 Riders and the unseen

#### `white_rider` | SIMPLE (one three-quarter gallop view) | scale: horse about 1.0 at the withers, rider seated, overall about 2.0 | 6 beats + flash
- Beats: B-024, B-046, B-114, B-115–116, B-123; B-062 is a pale flash on the wall (prompt text, no card present).
- Traditional iconography: three riders in white, red and black on horses of the same colour (A "сам белый, одет в белом, конь под ним белый"; R p.153; W p.39-40). Baba Yaga names them her bright Day, red Sun and dark Night (W p.50; R p.157). No source gives a headgear or cloak; the silhouette cues below are OURS so that colour does not carry it alone.
- **Identity line:** `White Rider: all-WHITE rider and all-white horse, bare-headed, a long white cloak streaming behind, a pale rim of light around the outline, long flowing white mane.`
- Silhouette cue: bare head, cloak streaming back. Reads against dawn and stays distinct from Red and Black in a row.

#### `red_rider` | SIMPLE | same scale | 6 beats + flash
- Beats: B-025, B-048, B-114, B-115–116, B-123; B-063 is a red glow on the wall.
- **Identity line:** `Red Rider: all-RED rider and all-red horse, a tall pointed red cap with a tassel, short tunic, bare arms, a short braided red mane.`
- Silhouette cue: tall pointed cap.

#### `black_rider` | SIMPLE | same scale | 7 beats + flash
- Beats: B-029, B-030 (fades into the gate), B-051, B-114, B-115–116, B-123; B-064 is a black horse silhouette in the hut.
- **Identity line:** `Black Rider: all-BLACK rider and all-black horse, a deep black hood hiding the whole head, a heavy cloak hanging over the horse's rump; only the horse's one small pale eye shows.`
- Silhouette cue: hood, heavy cloak. The pale eye dot is the one thing that reads at night (script B-029 "only the horse's eye reading"). Black on a night blue-black plate is the biggest risk in the library (section 5).

#### `hands_three_pairs` | SIMPLE | each hand about 0.2 of Vasilisa's height (large for hands) | 4 beats
- Beats: B-055, B-057, B-069, B-114.
- Traditional iconography: three pairs of hands that appear, seize the wheat and carry it off (W p.46 V; A "три пары рук"; R p.156). Hands only, no arms (CAST item 12; ours).
- **Identity line:** `The Hands: SIX bone-cream disembodied hands, three pairs, floating palms-up in a row, no arms, no bodies, no sleeves, a pale soft glow at the wrist ends.`
- Risk: the model may miscount to five or seven; plan to composite from a cream row of single hands if it fails (PROCESS Stage 5).

### 1.3 Tale 2 (the aunt tale, A no.103, R p.139-142)

#### `girl_tale2` | SIMPLE | scale 0.8 | 10 beats
- Beats: B-096–103, B-109, B-113.
- Traditional iconography: the sensible girl sent for a needle and thread, who stops first at her real aunt (R p.139 "the girl was no fool"). No costume source.
- Pair check against Vasilisa: different colour, head, hair and size; never in the same beat. The script flags the tales as separate ("In another tale").
- **Identity line:** `Tale 2 girl: smaller than Vasilisa, bare head with TWO short brown pigtails tied with plain string, leaf-GREEN sarafan, bare feet, a plain cloth bag on one shoulder.`

#### `stepmother_tale2` | SIMPLE | scale 1.1, LEAN and upright | 1 beat
- Beat: B-096.
- **Identity line:** `Stepmother of tale 2: lean upright woman, grey hair in a tight bun, dusty slate-blue long dress, one finger pointing out of the door, thin hard mouth.`
- Distinct from `stepmother` (aubergine, wide, covered head): no overlap in beats, no shared feature.

#### `real_aunt` | SIMPLE | scale 0.95, plump | 2 beats
- Beats: B-097–098.
- **Identity line:** `Real aunt: short plump kind woman, warm tan dress with a brown apron, a bone-cream headcloth tied at the back, rosy round face with a gentle smile, one finger raised in advice.`

#### `servant_maid` | SIMPLE | scale 1.0 | 4 beats
- Beats: B-100–101, B-107–108.
- CAST said "two faceless women"; the script has ONE "Servant maid" (state lines). One card, one figure.
- **Identity line:** `Servant maid: thin woman in a plain mid-grey dress, dark-grey headscarf, bare forearms, a wooden bucket in one hand, tired blank expression.`

#### `cat` | SIMPLE | scale 0.3 (a cat on a bench, about hip height to Vasilisa when sitting) | 6 beats
- Beats: B-102, B-104–106, B-108, B-114.
- Traditional iconography: the cat who sits at the loom, says "I'm weaving, dear aunt" gruffly (R p.140-141 V) and was never given so much as a bone (R p.141).
- **Colour conflict:** `CAST.md` made the cat black. Black is reserved for the Black Rider. Fix: **slate blue-grey cat** with a cream chest patch and two big round pale-yellow eyes.
- **Identity line:** `The cat: slate blue-grey cat with a cream chest patch, two big round pale-yellow eyes, upright ears, sitting like a person.`

#### `dogs_pair` | SIMPLE (one card, two dogs) | scale 0.45 each | 4 beats
- Beats: B-103, B-107–108, B-113.
- Traditional iconography: the plural yard dogs that tear at strangers and are thrown rolls (R p.140 "the dogs would have rent her"; A "собаки... хлебца").
- **Identity line:** `The two yard dogs: one thin TAN dog with a curled tail, one thin grey-brown dog with floppy ears; both lean, ribs showing, no collars.`
- The two are different shades on purpose so a 2-dog count reads. No white or black dog.

#### `tale2_gate` | SIMPLE (character-prop) | scale 1.4 tall, 1.2 wide | 4 beats
- Beats: B-103, B-107–108, B-114.
- Traditional iconography: ворота "gate" that bangs and creaks until oiled (A; R says "doors", p.139-141). The script calls it "the Gate" and makes it answer Baba Yaga (B-107). A plain wooden yard gate with two iron hinges and a latch, face-free.
- **Identity line:** `Tale 2 gate: a plain brown wooden yard gate of vertical planks, two dark iron hinges with a drop of oil on each, a simple wooden latch, no bones, no skulls, no face.`
- Must never be confused with `skull_gate` (section 3).

#### `birch` | SIMPLE (character-prop) | scale 2.5 tall | 5 beats
- Beats: B-103, B-107–108, B-113, B-114.
- Traditional iconography: the birch whose branches would hit the girl in the eye until a ribbon is tied on (R p.139; A "берёзка... ленточкой").
- **Colour conflict:** real birch bark is white. White is reserved for the White Rider. Fix: **bone-cream trunk with grey bark marks**.
- **Identity line:** `The birch: slender tree with a bone-cream trunk marked with grey bark dashes, pale yellow-green leaves, a long TEAL ribbon tied to one branch, face-free.`

### 1.4 Pairwise confusion check (what I changed and what I verified)

Method: for every beat where two or more figures share a frame (the `state:` lines), compared main colour and silhouette.

| Pair (shared beats) | Problem | Fix |
|---|---|---|
| Stepmother dark red dress (B-005, B-083–090) | Red is reserved for the Red Rider; the stepmother and the doll are the only non-riders in red in `CAST.md` and the shot line B-005 | Stepmother in **aubergine** (deep purple). Patch the shot line B-005 "dark red dress" to "deep aubergine dress" |
| Doll red dress (B-015 shot "tiny red dress") | Red reserved | Doll in **ochre-gold** with a rust-brown hem. Patch B-015 "tiny red dress" to "tiny ochre dress" |
| Cat black (CAST 16) | Black reserved for the Black Rider | Cat slate blue-grey, cream chest, pale-yellow eyes |
| Birch white (CAST 18) | White reserved | Trunk bone-cream with grey bark marks |
| B-126 "a shirt of fine white linen" | White reserved | Shirt in **cream** linen. Patch the B-126 shot line |
| B-089 "eyes... brightening to a deeper red" | Red reserved (it is a light state, not a costume) | Read as a deeper ember (burnt orange), not red. Prompt says "deeper ember orange, never red" |
| Stepmother vs Stepsister A vs Stepsister B in a dark wide shot (B-083–090, silhouettes at B-090) | Three women in a dark house | Silhouette ladder: stepmother WIDE with long skirt and covered head; A SHORT and ROUND with two side buns; B TALL and THIN with a topknot. Colours aubergine / mustard / teal |
| Stepsister A vs Stepsister B (B-006–012) | "must read as two, not clones" | Height 1.1 vs 1.3, round vs thin, two buns vs topknot, mustard vs teal, pins vs needles |
| Stepmother or sisters vs Baba Yaga | Dark-clothed women in a dark wide shot | They NEVER share a beat (stepmother and sisters: B-005 to B-090; Baba Yaga: B-033 on, tale 1 only after B-032). Baba Yaga is the only one with uncovered grey hair, a nose and a bone leg |
| Vasilisa vs Stepsisters (B-006, B-010–012) | Three girls round one candle | Vasilisa is smallest, cornflower blue with a pale lavender kerchief and a braid; A mustard, B teal; neither sister wears a kerchief |
| Vasilisa vs tale 2 girl | Two young girls in sarafans | Different palette (blue and lavender vs leaf-green), head (kerchief and braid vs bare with pigtails), size (1.0 vs 0.8); never in one beat |
| The three riders at night (B-115–116, B-123, B-114) | White, red, black on horses in a row at night | One card each; colour plus silhouette cue: White bare head and streaming cloak; Red tall pointed cap; Black deep hood and heavy cloak. Black rider has the pale horse eye |
| Baba Yaga vs Black Rider (B-115–116) | Both dark | Baba Yaga is umber with grey hair, bone leg, nose, on foot; the rider is on a horse in a hood. Different shape; kept |
| Skull lamp vs fence skulls (B-077 onward) | Both are skulls | Fence skulls cold pale white; skull lamp ember orange. B-077 is the beat where the skull changes colour |
| Doll's lit eyes vs skull lamp (both ember) | Same orange | Doll eyes are tiny circles on a 0.13-scale figure; they never share a frame |
| Real aunt vs Baba Yaga (tale 2 gives "aunt") | Both old women | Real aunt plump, tan with a cream headcloth; Baba Yaga tall, grey hair out, nose, bone leg; they never share a beat |
| Cat vs dogs vs maid (B-108, 7 present) | A crowd of small figures | Cat blue-grey, dogs tan and grey-brown, maid mid-grey but human-sized. B-107, B-108 and B-114 are COMPOSITE beats (section 4) |
| Tale 2 stepmother vs `stepmother` | Two stepmothers | Different tale, no shared beat; lean slate-blue with a bun vs wide aubergine with a kerchief |

Pairs checked with no clash: Vasilisa + doll + mother (B-014–017: blue, ochre, cream); Baba Yaga + Vasilisa in the hut (umber and bone vs blue and lavender); Baba Yaga + the three riders (B-115–116); girl2 + aunt (B-097–098); girl2 + Baba Yaga + cat (B-102, B-104).

---

## 2. Places table

Merged the script's 40-odd `state:` locations to **7 masters**. Every other view is a crop (free, cut in code) or an edit (one image). Crops: 5. Edits: 25. Edge-correlation check (0.6-0.75 pass) per PROCESS Stage 3 step 3 on every edit row.

| # | Master (`place_id`) | Master look | Derived variants (type) | Beats served | `state:` locations absorbed |
|---|---|---|---|---|---|
| 1 | `house_ext` | The stepmother's timber house at a forest edge, night; a door with one step, a low hedge and gate in the yard, a black wall of forest behind and to the right; one faint ember glow low in one window (the candle) | `house_door_step` (crop), `house_forest_edge` (crop, see risk 9); `house_ext_day` (edit, door open, bright forest); `house_ext_dusk` (edit, the hedge and gate in front); `house_ext_morning` (edit, bare yard, grey light); `house_ext_tale2_dusk` (edit, thatched roof, door ajar, dusk) | B-001, B-002, B-012, B-019, B-020–022, B-080–081, B-085, B-094, B-109 | Stepmother's house exterior (night, door shut and locked; at the door; at the gate, dusk; yard, morning); forest edge by the house (night, day); tale 2 house exterior |
| 2 | `house_room` | A low timber room at night: plank floor, a table with an iron candle-holder at centre, a spinning wheel on one side, a big stove in one corner, a window, a door in the back wall, benches. Candle LIT (the only warm light) | `house_room_dark` (edit, candle out, cold blue, a faint window glow; ember light from the skull is added by the plate prompt); `house_room_kitchen_day` (edit, daylight, pots, a basket by the door); `house_room_deathbed` (edit, a bed against the wall, a small window, dim); `house_room_tale2_day` (edit, day, door open, a spindle on the table); `house_room_aunt_day` (edit, day, door shut, a laid table); `house_room_weaving_day` (edit, day, a loom with a fine thread, a shirt on a stand, a crown on a table); `study_desk` (edit, day, a plain desk, two open old books, a quill, a window) | base: B-004–007; dark: B-008–011, B-083–084, B-086–087, B-127; kitchen: B-018; deathbed: B-014–017; tale2: B-096; aunt: B-097–098; weaving: B-126; study: B-121–122 | Stepmother's house interior room; the kitchen; Vasilisa's mother's deathbed room; tale 2 house interior; real aunt's house; an old woman's house in town and the king's palace room; a study |
| 3 | `best_room` | The best room: a finer plank room, one table at centre with a tall iron candlestick, the skull set on top with ember eyes (the only warm light), a shuttered window; night | `best_room_flare` (edit, the eyes flaming like two furnaces, ember glare flooding every wall, deeper ember not red); `best_room_ash_morning` (edit, grey morning light, three small mounds of grey ash on the floor, the skull dim) | master B-088–089, B-128; flare B-090–091; ash B-092–093 | the best room (interior; with and without ash mounds, as the script header requires) |
| 4 | `forest_road` | A narrow track through tall dark forest, night, a faint pale gap of sky above | `forest_road_dawn` (edit, sky paling, pale rim light); `forest_road_sunrise` (edit, low gold sun between trunks); `forest_road_evening` (edit, long shadows, dusk); `forest_road_montage` (edit, three light zones along the road: pale dawn, red sun, dark; ends at a skull gate far away) | master B-003, B-023, B-079, B-120; dawn B-024; sunrise B-025; evening B-026, B-114 (composite); montage B-124 | the forest road (night, dawn, day, evening); forest road to the clearing; day-to-night montage |
| 5 | `hut_clearing` | The hut on two huge scaly bird legs inside a ring of bone-and-skull fence, in a clearing, dusk, the skull gate in the fence at the left third facing camera, the hut at the right, black forest behind. **Gate SHUT, fence skulls DARK** | `hut_clearing_night_dark` (edit, night, skulls dark; B-031 has one skull blinking on); `hut_clearing_night_lit` (edit, night, ALL fence skulls cold pale white, the clearing as bright as noon, gate shut); `hut_clearing_night_gate_open` (edit, as night_lit but the gate swung wide); `hut_clearing_dawn` (edit, dawn, skull glow fading, gate shut); `hut_clearing_dawn_gate_open` (edit, sunrise, gate open); `hut_clearing_morning` (edit, day, swept yard, gate shut, skulls dark) | master (dusk, shut, dark) B-027, B-029–030, B-110, B-119, B-123; night_dark B-031, B-051; night_lit B-032–037, B-125; gate_open B-038, B-075–078; dawn B-046–047; dawn_gate_open B-048; morning B-049, B-111 | the clearing outside the hut (dusk, night); inside the fence outside the hut (dawn, sunrise, morning, dusk to night); inside the fence in front of the hut (night, gate opens); inside the fence by the open gate |
| 6 | `hut_interior` | Inside the hut, night: one huge stove, DARK with its door shut, filling a corner; a long table and benches; a shelf; a small window; a low ceiling; lit only by a cold pale glow from the fence skulls through the window (see lighting note) | `hut_corner` (crop, a corner by the stove, B-044–045); `hut_interior_storehouse` (edit, sacks of grain and a heap of wheat, light through an open door; B-050, B-057); `hut_interior_loom_day` (edit, day through the window, a loom with half-woven cloth; tale 2) | master B-039–045, B-052–056, B-060–074, B-112, B-115–118; storehouse B-050, B-057; loom B-099, B-102, B-104–106 | hut interior (night, corner); the storehouse; Baba Yaga's hut interior (day); hut interior and the dark behind it |
| 7 | `aunt_yard` (tale 2) | A plain log hut with a door and small window, a bath-house hut and a wood pile at the left, a plain wooden fence with a gap for a gate, a birch at the corner, a dirt path; day. No bones, no skulls | `aunt_yard_bath` (crop, bath-house and woodpile; B-101); `aunt_yard_approach` (crop, the path with the gate and birch in the foreground; B-103, B-113) | B-100–101, B-103, B-107–108, B-113 | Baba Yaga's yard; near the bath house; Baba Yaga's yard approach |

**Master count: 7.** **Edits: 25** (house_ext 4, house_room 7, best_room 2, forest_road 4, hut_clearing 6, hut_interior 2, aunt_yard 0). **Crops: 5** (`house_door_step`, `house_forest_edge`, `hut_corner`, `aunt_yard_bath`, `aunt_yard_approach`).

Why these 7 and not more:
- The stepmother's house outside and inside are separate masters (an exterior cannot be an edit of an interior), but ALL interior rooms in the story (kitchen, the mother's deathbed room, tale 2's house, the real aunt's house, the loom room, the study) derive from the one `house_room` by edit. Tale 2's house exterior (B-109) derives from `house_ext` by a thatch-and-dusk edit.
- `best_room` is its own master because the script header names its ash states as derived from "one master", and it is the story's hero image (B-088–093, B-128).
- `hut_clearing` is ONE master. Rather than two masters for the outside and the inside of the fence, the master is a wide side-on view with the gate at the left third and the hut at the right, so shots inside the fence (B-046–049, B-075–078) are crops and edits of the same geometry. A pure reverse angle would be a second master; I decided it is not needed.
- `aunt_yard` is the only place for a handful of beats (6). It cannot be derived from `hut_clearing` because tale 2 shows a plain fence, a plain gate and no skulls (the edit would replace every defining element and fall under 0.6 edge correlation). Unavoidable, 6 beats.
- Single-beat views kept as edits: `hut_clearing_dawn_gate_open` (B-048, a header-named gate state), `house_room_weaving_day` (B-126, the story ending), `forest_road_montage` (B-124). Cut candidates if the budget tightens: `forest_road_montage` and `house_room_weaving_day` (notes list B-124/B-125 as time cuts).

Scale and lighting notes:
- Ground scale: Vasilisa 1.0 is about 1/6 of the frame height in a medium shot. Hut: total height about 3.0 (legs about 1.6, cabin about 1.4), cabin width about 2.6, door about 1.0 high. Fence about 1.4 high with skulls on top at about 1.5; gate 1.9 high by 2.2 wide. Clearing about 12 wide. Interior: ceiling 1.7 (Baba Yaga stoops), stove 1.5 high and long enough for her to lie on, "smaller than the figure inside it" per CAST.
- Lighting: night blue-black everywhere. Fence skulls glow cold pale white and light the clearing "as bright as noon" (B-032), never orange. **Ember orange is only: the candle, the skull lamp (and the doll's eyes).** The hut interior therefore has a DARK stove and a cold skull-glow through the window; no orange fire. Dawn pale blue to gold (B-024–025, B-046–048); dusk violet.
- Doors and gates: the stepmother's house door states (shut and locked, open) are prompt-level states in `state.json`, not extra masters; the hut gate states (shut, open) ARE variants (header-named). Interior doorways at B-084–085 are prompt-level.
- `house_forest_edge` (B-002): a crop of the right-hand part of `house_ext` with the house small at the left of the crop; if the crop is too tight, one edit (+1 image).

---

## 3. Props table

The script shows props in the following ways; only the five hero props below need masters. Everything else rides on a character card, a place master or prompt text.

| # | Prop | Beats | Card? | Reason and scale |
|---|---|---|---|---|
| 1 | Skull lamp (skull with burning eyes on a stick) | B-003, B-077–082, B-086–094, B-120, B-128 | **`skull_lamp`** (master) | The hero prop and the hook. Ember-orange eye sockets are the ONLY warm light. Skull about 0.14 of Vasilisa's height (a human skull), on a plain wooden stick about 1.2 tall planted, about 0.8 when held out (B-079). States: eyes ember (default); flaring at B-090–091 and dim at B-092 are place variants (`best_room_flare`, `best_room_ash_morning`), buried at B-094 is prompt text. Fence skulls are NOT this card: cold pale white, part of `hut_clearing` |
| 2 | The skull gate (posts of human legs, bolts of arms, lock of a toothed mouth) | B-028 (close-up), B-030, B-038, B-051, B-075–076, B-119, B-123 | **`skull_gate`** (master) | The gate is also a place feature (open and shut states are `hut_clearing` variants), but B-028 is a close-up of the legs, arms and mouth that the place master cannot supply. One image: shut gate, two leg-bone posts with foot bones at the base, two arm-bones as cross bolts with open hands, a wide grinning toothed mouth as the lock plate. Bone-cream with dark gaps (A, R p.153). 1.9 high by 2.2 wide. No gore: plain bone shafts. Used as a reference when editing every `hut_clearing` gate variant |
| 3 | Candle (tallow, iron holder) | B-004–011, B-127 | **`candle`** (master) + `candle_snuffed` (derived) | Close-ups B-004, B-008 (flame going out), B-127 (snuffed, a thread of smoke). The room's one warm light before the skull. Candle about 0.06 of Vasilisa's height in a holder 0.1 high; flame small and steady. `candle_snuffed`: the same candle, no flame, a thin smoke curl. Lit through B-007, snuffed from B-008 |
| 4 | Mortar, pestle, broom | B-033–038 (inside `baba_yaga_mortar`), B-043, B-047, B-048, B-051–052, B-105, B-111, B-119 | **`mortar_pestle_broom`** (master) | One card: a big iron-grey mortar (0.9 high, 0.9 wide), an iron-grey pestle (1.3 long), a twig broom (1.3 long, birch twigs tied to a stick). Needed alone at B-047 (all three fly to her), at B-043 (broom against the wall), at B-105 (she raises the broom), at B-111 (Vasilisa sweeps) and as the input for `baba_yaga_mortar` |
| 5 | The four gifts (ribbon, oil jar, bread, bacon) | B-098, B-102, B-103, B-113 | **`gifts_set`** (master, one image of four items) | One card keeps them consistent across four beats: a long TEAL ribbon (0.4 long), a small brown clay oil jar (0.15 high), a round brown loaf (0.15), a strip of pink bacon (0.2). Ribbon colour is not red or white. The same teal ribbon is tied on the birch |
| 6 | Comb and towel | B-102, B-109 | no card, prompt text | Two hand-sized items shown at most in one hand; a small bone comb and a cream cloth towel. No beat hinges on their look |
| 7 | Spinning wheel | B-006 | no card: part of `house_room` | One shot; a plain wooden wheel on the left of the master |
| 8 | Lace pillow with steel pins; knitting needles and grey stocking | B-006, B-008, B-011 | no card: on `stepsister_a` and `stepsister_b` | Signature props of each sister. Pins glint cold blue-silver (not orange). Pillow about 0.3 of a person's torso; needles about 0.5 of Vasilisa's height |
| 9 | Food: dishes, a leg of meat, jugs, three scraps on a plate | B-040–042 | no card, prompt text | Table scene in `hut_interior`; the three scraps (soup ladle, crust, tiny pork piece) are one close plate of three small items, each about 0.04 |
| 10 | Wheat, black seeds, poppy seed and earth, sacks, oil jar | B-043, B-050, B-055, B-057, B-069 | no card: part of `hut_interior_storehouse` and prompt | A heap of wheat flecked with three black seeds; poppy seed mixed with dark earth; a sack of wheat carried by the hands. Prompt text for a heap about 0.3 tall |
| 11 | Basket | B-018–019 | no card, prompt text | Wicker basket on Vasilisa's arm, about 0.25 |
| 12 | Flint and steel, a shovel with an ember | B-084 | no card, prompt text | Two hand-sized items; the ember on the shovel dies at the threshold: the ember colour is the rule's ember orange |
| 13 | Handkerchief, wash-tub, sieve, damp firewood | B-100–101 | no card, prompt text | A folded cream handkerchief (0.1); a wooden tub (0.4) on the maid; a round sieve (0.25); a pile of damp sticks |
| 14 | Loom | B-099, B-102, B-104–106, B-126 | no card: part of `hut_interior_loom_day` and `house_room_weaving_day` | Wooden frame about 1.3 high; the cat sits at it at 0.3 |
| 15 | Spindle | B-096 | no card, prompt text | One shot; on the table in `house_room_tale2_day` |
| 16 | Books, quill, desk | B-121–122 | no card: part of `study_desk` | Two open old books, a quill; the page showing a woman in a mortar and the other a coiled serpent are painted into the plate |
| 17 | Shirt, crown, thread through a needle's eye | B-126 | no card, prompt text | Shirt in CREAM linen (colour rule), a plain gold crown on a table; thread a glowing line |
| 18 | Hut on fowl's legs | B-027, B-125 etc. | no card: part of `hut_clearing` | The place master carries the hut; scale in section 2 |
| 19 | Fence skulls and bones | B-027, B-031–038, B-046–051, B-075–078, B-125 | no card: part of `hut_clearing` | About 20 skulls on bone posts; cold pale white sockets; skulls about 0.14 each |
| 20 | Stove, bed, blanket, benches | B-005, B-014–017, B-039, B-083 | no card: part of place masters | The stove at B-005 is the house stove (fire pinched out); the hut stove is dark |
| 21 | Tale 2 gate and the birch | B-103, B-107–108, B-113, B-114 | cards `tale2_gate` and `birch` (section 1.3) | They speak and complain; they are small cards, not props |

**Prop masters: 5** (`skull_lamp`, `skull_gate`, `candle`, `mortar_pestle_broom`, `gifts_set`) plus 1 derived (`candle_snuffed`). Animals and scale: cat 0.3, dogs 0.45 each, horses about 1.0 at the withers (riders section 1.2), doll 0.13.

---

## 4. Variant ledger (rule 21, mechanical)

Each row gives the `state:` name, the exact card id or place id to pull, and the beat where it changes. The plate builder reads the card id from `state.json`; it never infers a variant from the shot line. Rows marked "prompt" are not separate images.

### 4.1 Figures and cards

| Figure | `state:` name | card_id | First beat | Last beat | Changes at |
|---|---|---|---|---|---|
| Vasilisa | Vasilisa | `vasilisa` | B-002 | B-126 | never changes. At B-014–017 the prompt scales her to 0.65 (the deathbed child); back to 1.0 at B-018. Same card throughout (script header) |
| Baba Yaga | Baba Yaga (on foot) | `baba_yaga` | B-039 | B-046 | to `baba_yaga_mortar` at B-048 (she climbs in after the mortar flies out at B-047) |
| Baba Yaga | Baba Yaga arriving in the mortar | `baba_yaga_mortar` | B-033 | B-038 | to `baba_yaga` at B-039 (she throws herself on the stove) |
| Baba Yaga | Baba Yaga in the mortar | `baba_yaga_mortar` | B-048 | B-048 | to `baba_yaga` at B-052 (inside the hut) |
| Baba Yaga | Baba Yaga rides in | `baba_yaga_mortar` | B-051 | B-051 | to `baba_yaga` at B-052 |
| Baba Yaga | Baba Yaga (tale 1 remainder and tale 2) | `baba_yaga` | B-052 | B-118 | none (B-099–108 tale 2 is the same card); to `baba_yaga_mortar` at B-119 |
| Baba Yaga | Baba Yaga arrives at the gate | `baba_yaga_mortar` | B-119 | B-119 | end |
| Doll | the doll (eyes unlit) | `doll` | B-014 | B-016 | to `doll_lit` at B-021 |
| Doll | the doll (unlit) | `doll` | B-020 | B-020 | to `doll_lit` at B-021 |
| Doll | the doll (eyes lit) | `doll_lit` | B-021 | B-023 | to `doll` at B-044 (fed, not speaking) |
| Doll | the doll (unlit) | `doll` | B-044 | B-044 | to `doll_lit` at B-045 (speaks) |
| Doll | the doll (eyes lit) | `doll_lit` | B-045 | B-057 | none (B-050, B-057 work shots stay lit) |
| Stepmother | Stepmother | `stepmother` | B-005 | B-090 | none; B-092 is ash, no figure |
| Stepsisters | Stepsister A, Stepsister B | `stepsister_a`, `stepsister_b` | B-006 | B-090 | none |
| Vasilisa's mother | Vasilisa's mother | `vasilisas_mother` | B-014 | B-017 | none |
| Riders | White, Red, Black Rider | `white_rider`, `red_rider`, `black_rider` | B-024 / B-025 / B-029 | B-123 | none; B-062–064 flashes are prompt text |
| Hands | the Hands (three pairs) | `hands_three_pairs` | B-055 | B-114 | none |
| Tale 2 | Girl, Stepmother of tale 2, Real aunt, Servant maid, Cat, two dogs, The Gate, Birch | `girl_tale2`, `stepmother_tale2`, `real_aunt`, `servant_maid`, `cat`, `dogs_pair`, `tale2_gate`, `birch` | B-096 | B-114 | none |
| Candle | candle lit | `candle` | B-004 | B-007 | to `candle_snuffed` at B-008 (flame going out) |
| Candle | candle snuffed | `candle_snuffed` | B-008 | B-011 | candle lit only again in callbacks: B-127 is `candle_snuffed` (smoke thread) |
| Skull | skull lamp (ember) | `skull_lamp` | B-003 | B-094 | B-003 upright on a pole; B-077 first appearance of the ember glow (it was a fence skull, cold white, until she takes it); B-092 dim (place variant); B-094 buried (prompt); B-120 and B-128 upright again |

### 4.2 Places

| Place | State | variant id | Beats | Changes at |
|---|---|---|---|---|
| `hut_clearing` | gate shut, fence skulls dark, dusk | `hut_clearing` (master) | B-027, B-029–030, B-110, B-119, B-123 | to night dark at B-031 |
| `hut_clearing` | gate shut, night, skulls dark (one blinks at B-031) | `hut_clearing_night_dark` | B-031, B-051 | to night lit at B-032 |
| `hut_clearing` | gate shut, night, ALL skulls lit cold white | `hut_clearing_night_lit` | B-032–037, B-125 | to gate open at B-038 |
| `hut_clearing` | gate open, night, lit | `hut_clearing_night_gate_open` | B-038, B-075–078 | to inside the hut at B-039 |
| `hut_clearing` | gate shut, dawn, glow fading | `hut_clearing_dawn` | B-046–047 | to gate open at B-048 |
| `hut_clearing` | gate open, sunrise | `hut_clearing_dawn_gate_open` | B-048 | to shut at B-049 |
| `hut_clearing` | gate shut, morning, skulls dark | `hut_clearing_morning` | B-049, B-111 | end |
| `best_room` | skull on candlestick, ash ABSENT | `best_room` (master) | B-088–089, B-128 | to flare at B-090 |
| `best_room` | skull flaring, glare on every wall | `best_room_flare` | B-090–091 | to ash at B-092 |
| `best_room` | ash PRESENT, skull dim, morning | `best_room_ash_morning` | B-092–093 | end; B-128 returns to the master (no ash) |
| `house_room` | candle lit | `house_room` (master) | B-004–007 | to dark at B-008 |
| `house_room` | candle out, dark | `house_room_dark` | B-008–011, B-083–084, B-086–087, B-127 | none |
| `house_room` | deathbed | `house_room_deathbed` | B-014–017 | to kitchen at B-018 |
| `house_room` | kitchen day | `house_room_kitchen_day` | B-018 | end |
| `house_room` | tale 2 house; aunt's house; weaving; study | `house_room_tale2_day`, `house_room_aunt_day`, `house_room_weaving_day`, `study_desk` | B-096; B-097–098; B-126; B-121–122 | per beat |
| `house_ext` | night, door shut and locked | `house_ext` (master) | B-001, B-002, B-012, B-020–022 | to day at B-019 (a day beat in between) |
| `house_ext` | day, door open | `house_ext_day` | B-019 | to night at B-020 |
| `house_ext` | dusk, at the gate | `house_ext_dusk` | B-080–081 | to B-085 night doorway |
| `house_ext` | night, door open | prompt-level on `house_door_step` | B-085 | end |
| `house_ext` | morning, yard | `house_ext_morning` | B-094 | end |
| `house_ext` | tale 2 dusk | `house_ext_tale2_dusk` | B-109 | end |
| `forest_road` | night | `forest_road` (master) | B-003, B-023, B-079, B-120 | to dawn at B-024 |
| `forest_road` | dawn, sunrise, evening, montage | `forest_road_dawn`, `forest_road_sunrise`, `forest_road_evening`, `forest_road_montage` | B-024; B-025; B-026, B-114; B-124 | per beat |
| `hut_interior` | night | `hut_interior` (master) | B-039–045, B-052–056, B-060–074, B-112, B-115–118 | to storehouse at B-050 |
| `hut_interior` | storehouse, loom day | `hut_interior_storehouse`, `hut_interior_loom_day` | B-050, B-057; B-099, B-102, B-104–106 | per beat |
| `aunt_yard` | day | `aunt_yard` + crops | B-100–101, B-103, B-107–108, B-113 | none |

**Composite beats (crowds over five or exact-count groups, PROCESS Stage 5).** B-107 (Baba Yaga, two dogs, the gate, the birch, the maid), B-108 (those plus the cat: 7) and B-114 (three riders, the Hands, the cat, the birch, the gate, Baba Yaga: 8 groups) are composites. Plan them as cards pasted onto the place master, not as one generation. B-114 uses `forest_road_evening` (the shot line says "a ridge"; patch to "a bend in the road": no ridge master exists).

**Shot-line patches to land before narration** (text only, no story change): B-005 "dark red dress" to "deep aubergine dress"; B-015 "tiny red dress" to "tiny ochre dress"; B-126 "white linen" to "cream linen"; B-089 "deeper red" to "deeper ember orange"; B-114 "ridge" to "bend in the road". All logged in section 1.4.

---

## 5. Risks (what could still read wrong at 540p, and what to look at first)

1. **Baba Yaga's bone leg and nose.** The bone leg must read as a pale knobbed bone against umber rags and a night plate; at 540p it may look like a pale stocking. The nose is the one exception to the no-nose rule and could read as a long beak. Look at the Baba Yaga face close-up and the stove shot (B-039) first. Fallback: a thicker bone with bigger knobs; a plain hooked nose in profile only.
2. **The skull lamp.** The two skulls (cold pale fence skulls and the ember skull lamp) must read as two different lights. B-077 is where a fence skull becomes the ember lamp; the colour change must be visible in one frame. Also the doll's eyes share the orange.
3. **The three riders at night.** Black on a night blue-black plate is nearly invisible: only the pale horse eye reads. White at dawn on a pale sky is the opposite problem. The silhouette cues (bare head and cloak, pointed cap, deep hood) must carry them. B-115–116 and B-123 (three in a row) are the hardest plates. Fallback: a thin cold rim light on the Black Rider's outline.
4. **The sisters as two.** The pair must read as two women, not clones, in B-006, B-010–011 and the silhouettes at B-090 (round-with-buns vs tall-with-topknot). Look at the two cards side by side. If B reads like A, upgrade B to FULL.
5. **Baba Yaga is dark at night.** Umber shawl on a night plate: she reads only by the pale hair and bone leg. At B-115–116 she stands beside the Black Rider.
6. **The Hands.** The model may miscount six hands. Composite from a cream row of single hands if it fails.
7. **The skull gate.** Legs, arms and a toothed mouth must read at 540p without gore; B-028 is the plate. If the mouth reads as a smile, enlarge the teeth.
8. **Gate and skull state edits** (`hut_clearing_night_lit`, `_gate_open`, `_dawn_gate_open`) change lighting a lot; edge correlation may fall under 0.6. If so, regenerate from the master prompt rather than patching.
9. **`house_forest_edge` crop** (B-002) may cut the house; one edit is the fallback. The tale 2 house exterior (`house_ext_tale2_dusk`) derived from the same master may read as Vasilisa's house; the thatch and the green-sarafan girl are the separators.
10. **The one Vasilisa card at the deathbed** (B-014–017). A 0.65 scale with the same braid and kerchief may read as the same age as the errand. Option in open question 1: a derived `vasilisa_child` card ($0.04).
11. **Hut interior lighting.** No orange stove fire keeps ember orange exclusive to the lamp and candle; a dark interior may read murky. Open question 2.
12. **Locators** are the script's (see caveat); costume tells are ours.

What William should look at first: (1) the Baba Yaga card (face and stove pose), (2) the skull lamp, (3) the three rider cards side by side in a dark crop, (4) the two stepsisters side by side, (5) the `hut_clearing_night_lit` and `_gate_open` pair.

---

## 6. Cost estimate for the image step (gpt-image-2.6 at about $0.04 an image, 20% re-roll allowance)

| Item | Count | Images |
|---|---|---|
| FULL cards (turnaround + face): `baba_yaga`, `vasilisa`, `stepmother`, `stepsister_a` | 4 | 8 |
| SIMPLE cards: `vasilisas_mother`, `doll`, `stepsister_b`, `white_rider`, `red_rider`, `black_rider`, `hands_three_pairs`, `girl_tale2`, `stepmother_tale2`, `real_aunt`, `servant_maid`, `cat`, `dogs_pair`, `tale2_gate`, `birch` | 15 | 15 |
| Derived character cards: `baba_yaga_mortar`, `doll_lit` | 2 | 2 |
| Prop masters: `skull_lamp`, `skull_gate`, `candle`, `mortar_pestle_broom`, `gifts_set` | 5 | 5 |
| Derived prop: `candle_snuffed` | 1 | 1 |
| Place masters | 7 | 7 |
| Place variants made by edit (crops are free) | 25 | 25 |
| **Subtotal** | | **63** |
| Re-roll allowance 20% | | +13 |
| **Total with allowance** | | **about 76 images** |

- Spend: 63 images x $0.04 = **$2.52**; with the 20% re-roll about **$3.04**. This is under the roughly $4 target for the round (PROCESS Stage 3).
- Headroom of about $1: room for the optional `vasilisa_child` ($0.04), a FULL upgrade of `stepsister_b` ($0.04) or `girl_tale2` ($0.04), and a Black Rider re-roll or two.
- If a cut is wanted: `forest_road_montage` and `house_room_weaving_day` (2 images; both single-beat), `hut_clearing_dawn_gate_open` (1).
- Free work in code: 5 crops, the composed labelled cards, edge-correlation checks, `cast_check.py`, the B-107/B-108/B-114 composites.
- Not included: 540p look-checks and any wardrobe option sheets (skipped on the condition that the cards are right the first time).

---

## Open questions for William

1. **Vasilisa at the deathbed (B-014–017):** one card (0.65 scale, same costume), as the script header says, or a derived `vasilisa_child` card ($0.04, a small girl, same kerchief, no braid)? I recommend ONE card unless the 540p test shows she reads as the same age.
2. **Hut interior lighting:** dark stove and a cold skull-glow through the window (keeps ember orange only for the lamp, candle and doll), or a warm orange stove glow? I recommend dark and cold.
3. **Colour changes forced by the colour rule:** stepmother dark red to aubergine; doll red to ochre-gold; cat black to slate blue-grey; birch white to bone-cream; B-126 white shirt to cream. Accept?
4. **Baba Yaga's tells:** keep the hooked nose (the one nose in the cast) and one bone leg; iron teeth only on the face close-up. Accept, or drop either?
5. **Rider silhouette cues** (White bare head and cloak, Red pointed cap, Black deep hood): these are ours, not traditional. Accept?
6. **Sisters:** A (short, round, buns, mustard, pins) is the one who snuffs the candle; B (tall, thin, topknot, teal, needles). The script just says "one stepsister". Accept A as the snuffer?
7. **Hut `state:` change:** B-048 shows the gate OPEN at sunrise as she drives out (the script says "gate opens then shuts behind her"). OK to render it as the open state?

## WILLIAM'S DECISIONS
