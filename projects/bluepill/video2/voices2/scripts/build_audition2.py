"""Writes AUDITION2.md from plan.rows(), _work/metrics_*.json, _work/words.json, voice_log.csv and cfg.py (prompts, tags, settings).
Run: python -I build_audition2.py   (needs numpy venv only because plan imports select2; no API calls)"""
import os, sys, json, csv, math, itertools
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cfg import *
import plan, select2
W=f"{OUT}/_work"; MC=json.load(open(f"{W}/metrics_chars.json")); MD=json.load(open(f"{W}/metrics_daniel.json")); WD=json.load(open(f"{W}/words.json"))
EXTRA=json.load(open(f"{W}/extra_notes.json")) if os.path.exists(f"{W}/extra_notes.json") else {}
rows=plan.rows(); art=select2.art
LOGROWS=list(csv.DictReader(open(f"{OUT}/voice_log.csv")))
REEL_C={r["num"] for _,its in plan.reel_chars() for r in its}; REEL_X={r["num"] for _,its in plan.reel_extra() for r in its}
def reelof(r):
    if r["role"]=="NARR": return "D"
    return "C" if r["num"] in REEL_C else ("X" if r["num"] in REEL_X else "")
def hz2st(h): return 12*math.log2(h/100)
def hint(r,m):
    h=[]; f=m["f0w_median_hz"]; s=m["pitch_spread_st"]; l=m["lra_lu"]
    if r["role"]=="NARR": return ""
    if f<100: h.append("very deep")
    elif f>=200: h.append("high")
    if s is not None and s<2.5: h.append("flat pitch")
    if s is not None and s>=5: h.append("very wide pitch")
    if l>=8: h.append("big loudness swings")
    if m["true_peak_db"]<-12: h.append("quiet file")
    wd=WD.get(r["base"]); 
    if wd:
        for x in wd["words"]:
            st=x["status"]
            if st=="FLAT": h.append(f"'{x['word'].strip('.?')}' FLAT ({x['f0_p10_p90_st']} st)")
            elif st.startswith("UNRELIABLE"): h.append(f"'{x['word'].strip('.?')}' unmeasurable")
        heard=wd["heard"].lower()
        for bad,tag in (("olafemus","name misheard 'Olafemus'"),("paul of venus","name misheard 'Paul of Venus'"),("polyfamous","name misheard 'Polyfamous'")):
            if bad in heard: h.append(tag)
    return "; ".join(h)
def fmt(r):
    m=MD[r["base"]] if r["role"]=="NARR" else MC[r["base"]]
    return m
def voice_cell(r):
    if r["role"]=="NARR": return "Daniel (premade, onwK4e9ZLuTAKqWW03F9)"
    if r["engine"]=="design": return f"**Voice Design {r['role']} {r['design']}** (prompt {r['role']}-{r['design']}, §Voice Design); preview {r['preview']} of 3"
    if r["engine"]=="post": return "design POLY A preview 2, local pitch shift down 4 semitones, duration unchanged (method not recorded in the scripts; no API call)"
    if r["engine"]=="eleven_lib": return f"**{r['voice']}** (library voice 'BP {r['voice'].split('Warm')[0].split('Trusting')[0].split('Unhurried')[0]} (audition)'), line {r['line']}"
    if r["engine"]=="openai": return f"**{r['voice']}**, line {r['line']}"
def setting_cell(r):
    if r["role"]=="NARR":
        c=[x for x in NARR if x[0]==r["id"]][0]; st=c[4]
        tag=" tag "+(TAG_A if "tagA" in r["base"] else TAG_B if "tagB" in r["base"] else "") if "_v4_" in r["base"] else ""
        return f"{c[2]}; stability {st['stability']}, style {st['style']}, speed {st['speed']}, similarity {st['similarity_boost']}, boost on;{tag}"
    if r["engine"]=="design": return "eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag)"
    if r["engine"]=="post": return "n/a (local post-processing)"
    if r["engine"]=="eleven_lib": return f"eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag {TAGS[r['line']]}"
    if r["engine"]=="openai":
        return "gpt-4o-mini-tts; instructions: "+[i for v,i in OA[r['role']] if v==r['voice']][0]
def engine_cell(r):
    if r["role"]=="NARR": return "ElevenLabs "+[x for x in NARR if x[0]==r["id"]][0][2]
    return {"design":"ElevenLabs Voice Design (eleven_ttv_v3)","post":"local pitch shift","eleven_lib":"ElevenLabs eleven_v4 (library voice)","openai":"OpenAI gpt-4o-mini-tts"}[r["engine"]]
out=[]; P=out.append
P("# AUDITION2.md: voice round 2 for video 1 (The Myth Ledger), 2026-11-13\n")
P(EXTRA.get("intro","")+"\n")
# clip table
P("## 1. All clips, numbered\n")
P("Number = the number spoken on the slate in the reels (reel column: D = `reel2_daniel.mp3`, C = `reel2_characters.mp3`, X = `reel2_extra.mp3`, blank = only the raw file exists). F0 mean is the wide-range tracker (40-400 Hz) in Hz; spread = std of voiced F0 in semitones with the reference teardown's own definition (autocorrelation 70-300 Hz, corr > 0.5). wpm is words / speech span (first to last sound); the bracket is an articulation pace with every gap of 0.3 s or more removed. It runs high because it also removes normal sentence stops, so use it only to compare clips of the same line, and read the plain wpm as the pace you would actually get. Voice Design previews also carry a few seconds of silence between lines, which lowers their plain wpm. Pauses/min counts gaps of 0.3 s or more (reference definition).\n")
for sec,flt in (("Daniel narrator variants (`narrator_daniel/`, 266-310 characters, SCRIPT-V3 beats 01, 02, 08, 11)",lambda r:r["role"]=="NARR"),)+tuple((f"{plan.ROLE_NAME[ro]} (`characters/{ro}/`)",(lambda ro:lambda r:r["role"]==ro)(ro)) for ro in ("ODY","POLY","CYC2","CREW")):
    P(f"### {sec}\n")
    if sec.startswith("Daniel"):
        P("| # | reel | file | engine / model | voice | settings / tags | s | wpm | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |"); P("|---|---|---|---|---|---|---|---|---|---|---|---|")
    else:
        P("| # | reel | file | engine / model | voice or prompt id | settings / tags | s | wpm (art.) | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |"); P("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in [x for x in rows if flt(x)]:
        m=fmt(r); w=f"{m['wpm']}" if r["role"]=="NARR" else f"{m['wpm']} ({art(m)})"
        P(f"| {r['num']} | {reelof(r)} | `{r['file']}` | {engine_cell(r)} | {voice_cell(r)} | {setting_cell(r)} | {m['duration_s']} | {w} | {m['f0w_mean_hz']} ({m['pitch_spread_st']}) | {m['lufs']} / {m['lra_lu']} | {m['pauses_per_min']} | {hint(r,m)} |")
    P("")

# ---------------- sections 2-9 ----------------
RF={r["file"]:r for r in rows}
def N(f): return RF[f]["num"]
def M(f): return MC[os.path.basename(f)]
def mst(f): return M(f)["f0w_mean_st"]
def hzof(f): return M(f)["f0w_mean_hz"]
pre=[]; Q=pre.append
Q("# AUDITION2.md: voice round 2 for video 1 (The Myth Ledger), 2026-11-13\n")
Q("**I cannot hear any of these clips.** Every pick below comes from voice metadata, the prompts and the measurements. William's ears decide. Nothing was uploaded, posted or sent; only audition lines were generated (no full script).\n")
Q("**Listen in this order:**")
Q("1. `reel2_daniel.mp3` (2:17): slate, then clip, six Daniel variants numbered 1-6.")
Q("2. `reel2_characters.mp3` (4:54): per role (Odysseus, Polyphemus, the Cyclopes, the crew): the best preview of each of the three designed prompts, then the best-scoring library or OpenAI voice.")
Q("3. `reel2_extra.mp3` (3:22): the next candidates (extra library and OpenAI voices, the pitched-down Polyphemus, the ram and prayer lines).")
Q("Every reel clip is edge-trimmed, long gaps shortened to 0.7 s and level-matched to -19 LUFS so loudness does not bias you; slates are spoken by one fixed voice, River. Files in `narrator_daniel/` and `characters/` are raw. The slate number is the # in the table below.\n")
Q("**Reference traits** (REVIEW-ref-vs-draft section 4): 178 wpm overall, pitch spread 4.7 semitones, loudness range 3.6 LU, 1.9 pauses of 0.3 s or more per minute, performed voices for characters. Round-1 Daniel (N02, 143-character clip): 158 wpm, 3.43 st, 1.4 LU. Caveat: 12-27 second clips, one take each. Pitch spread and LRA wobble by a semitone or a couple of LU between takes of the same voice; read the numbers as hints.\n")
Q("**What the finisher did** (the first worker was cut off by the usage limit before writing this file): measured every clip again from the metric files it left (`_work/metrics_*.json`, `_work/words.json`; 6 + 73 clips, all present, none zero-length or corrupt), checked both reels, rebuilt `reel2_characters.mp3` and added `reel2_extra.mp3` (see section 6), backfilled one missing log row, and wrote this file. No audio was generated.\n")
body=[]; P=body.append
# Voice Design section
P("## 2. Voice Design: what it offered and what it cost\n")
P("- **Offered:** `POST /v1/text-to-voice/design`, model `eleven_ttv_v3`, `guidance_scale` 4, `loudness` 0.5, a text description (native language, gender, age, quality, persona, emotion, timbre and pacing) plus the audition line. Each call returned **3 previews** (3 different voices from one prompt). 12 calls (4 roles x 3 prompts) = **36 previews**, 8-12 s per call, all HTTP 200 on this Creator plan, so the feature is available without a plan change.")
P("- **Cost:** per the log, 1,911 characters (the audition text once per call: 201 x 3 Odysseus, 153 x 3 Polyphemus, 160 x 3 Cyclopes, 123 x 3 crew); the two other previews of a call were logged at 0. That is a reading of the account counter behaviour in round 1, not a verified invoice line: the subscription counter lags (see section 7), so I could not confirm the per-call charge.")
P("- **Slots:** previews are temporary (their ids are not in My Voices). Nothing was saved, so no designed voice occupies a slot. To use a designed voice for a full script it must be saved (create voice from preview) and takes **one slot each** (8 free of 30, see section 8); saving does not cost characters by itself. Previews cannot be re-rendered with other lines until saved.")
P("- **Limits seen:** the voice is fixed by the preview, so the first line decides; previews carry 1-4 s of silence between lines (lowers plain wpm); three previews have loudness range above 10 LU (Polyphemus B p1 11.9, Polyphemus C p1 17.5, crew A p3 10.8; outliers, flagged in the table).\n")
P("### Design prompts (full text, as sent)\n")
P("Audition line (same for all three prompts of a role): ODY = the 4-line Odysseus text; POLY = 'More. Now tell me your name... Nobody last.'; CYC2 = the 3-line Cyclopes text incl. 'Sheep.'; CREW = the 6-line crew text incl. 'Hello?' and 'Nope.'\n")
for role in ("ODY","POLY","CYC2","CREW"):
    for n,pr in DESIGN[role]:
        nums=[N(f"characters/{role}/design/{role}_design{n}_p{i}.mp3") for i in (1,2,3)]
        P(f"- **{role}-{n}** (clips {nums[0]}, {nums[1]}, {nums[2]}): {pr}")
P("")
# distinctness
P("## 3. Character distinctness (F0 mean, semitones re 100 Hz)\n")
D=MD["D2a_v4_tagA_speed1.0.mp3"]["f0w_mean_st"]
sets={
 "Set 1 (widest separation, all gaps at least 2 st)":["characters/ODY/design/ODY_designC_p2.mp3","characters/POLY/post/POLY_designA_p2_pitchdown4st.mp3","characters/CYC2/design/CYC2_designC_p2.mp3","characters/CREW/eleven_lib/C12_TimmyAnxiousNerd_CREW_v4.mp3"],
 "Set 2 (best total score from the selection script, gap 2.03 st; Odysseus is a library voice named Daniel, a different voice from the narrator)":["characters/ODY/eleven_lib/C01_DanielWarmBaritone_ODY_v4.mp3","characters/POLY/design/POLY_designA_p2.mp3","characters/CYC2/design/CYC2_designC_p2.mp3","characters/CREW/eleven_lib/C12_TimmyAnxiousNerd_CREW_v4.mp3"],
 "Set 3 (best-scoring clip per role, no gap rule; shows the problem)":["characters/ODY/design/ODY_designC_p2.mp3","characters/POLY/design/POLY_designA_p2.mp3","characters/CYC2/design/CYC2_designB_p2.mp3","characters/CREW/eleven_lib/C12_TimmyAnxiousNerd_CREW_v4.mp3"],
}
for name,fl in sets.items():
    labels=["Daniel (D2a, #2)"]+[f"{RF[f]['role']} #{N(f)}" for f in fl]; vals=[D]+[mst(f) for f in fl]; hz=[MD["D2a_v4_tagA_speed1.0.mp3"]["f0w_mean_hz"]]+[hzof(f) for f in fl]
    P(f"**{name}**\n")
    P("| |"+"|".join(f" {l} " for l in labels)+"|"); P("|---|"+"|".join("---" for _ in labels)+"|")
    for i,l in enumerate(labels):
        P(f"| **{l}** ({hz[i]} Hz, {vals[i]:+.1f} st) |"+"|".join(" - " if i==j else f" {abs(vals[i]-vals[j]):.1f} " for j in range(len(labels)))+"|")
    mn=min(abs(a-b) for a,b in itertools.combinations(vals,2)); P(f"\nSmallest gap: **{mn:.2f} st**"+(" (meets the 2 st rule)" if mn>=2 else " (fails the 2 st rule)")+".\n")
P("Notes: F0 mean is a proxy for the voice's register; two voices 2 st apart can still sound alike if the accent and delivery match, and two voices closer than 2 st can still be told apart by accent. The set-1 Cyclopes is a designed *female* voice (prompt CYC2-C); that is a casting decision for William. Crew is much higher than everyone else (210-230 Hz library voices), which is intended for a young, frightened crewman. Designed Odysseus, Polyphemus and Cyclopes-B all sit within 1.5 st of each other (98-106 Hz) when taken as the top-scoring preview, so the design prompts did not separate those three by register; accent, pace and delivery would have to.\n")
# per-role picks
P("## 4. Suggested picks per role (by measurement; I cannot hear them)\n")
P("Scores come from `scripts/select2.py`: lower = closer to explicit targets that are my reading of the brief, not facts about taste. Targets: **Odysseus** warm dry mid-baritone, 90-125 Hz, spread about 4.5 st, 185 wpm, LRA about 3.6. **Polyphemus** enormous, very deep and slow, 60-95 Hz, 150 wpm, not flat. **Cyclopes** bored and flat, 105-150 Hz, spread about 3 st. **Crew** young and breathless, 150-240 Hz, spread about 4.5 st, 'Nope.' and 'Hello?' not flat. Designed voices use the best of their three previews.\n")
def pk(f,why): 
    m=M(f); return f"**#{N(f)}** `{os.path.basename(f)}`: {hzof(f)} Hz mean, {m['pitch_spread_st']} st spread, {m['wpm']} wpm, {m['lufs']} LUFS / {m['lra_lu']} LU. {why}"
P("**Odysseus**")
P("1. "+pk("characters/ODY/design/ODY_designC_p2.mp3","Best score (1.28). Scottish-lowland negotiator prompt; deep (98-101 Hz), a little slow (132 wpm); preview 1 and 3 of the same prompt are slower still (138, 114 wpm)."))
P("2. "+pk("characters/ODY/eleven_lib/C01_DanielWarmBaritone_ODY_v4.mp3","Library voice 'Daniel (warm baritone)', a different voice from the narrator but the same name: say so when you listen, so the two are not confused. Closest to the reference pace and spread, but its mean F0 is only 2.0 st from the narrator."))
P("3. "+pk("characters/ODY/openai/ash_ODY.mp3","OpenAI ash with acting instructions; flatter (2.9 st) and slowish (150 wpm), peaks at -5.6 dB. Also on the list: designed A p3 (#9) and B p2 (#11).")+"\n")
P("**Polyphemus**")
P("1. "+pk("characters/POLY/design/POLY_designA_p2.mp3","Best score (0.75): deep (98 Hz), slow (97 wpm), not flat (2.7 st). The slowest-sounding of the picks; 'Nobody.' ok (2.5 st)."))
P("2. "+pk("characters/POLY/post/POLY_designA_p2_pitchdown4st.mp3","The same take pitched down 4 st locally: 80 Hz, 'enormous' on paper, spread 3.96 st. Pitch shifting can add a processed sound; I cannot hear whether it does."))
P("3. "+pk("characters/POLY/openai/ash_POLY_NOBODY.mp3","OpenAI ash, 97-100 Hz, 130 wpm, flat-ish (2.6 st). Rams and prayer lines #45, #46.")+"\nLibrary voices are poor fits by measurement (113-157 Hz and loudness range 6-10 LU on the Nobody line); OpenAI onyx is the deepest (89-93 Hz) but the flattest (1.3-1.8 st).\n")
P("**Cyclopes chorus**")
P("1. "+pk("characters/CYC2/design/CYC2_designB_p2.mp3","Best score (2.18): Midlands 'tired pub regular', slow (94 wpm), 98 Hz median, 3.4 st; loudness range 5.1 LU is wider than flat; 'Sheep.' ok."))
P("2. "+pk("characters/CYC2/eleven_lib/C07_DrewDeadpan_CYC2_v4.mp3","Library Drew with [bored, flat, deadpan]: steadiest levels (LRA 1.6), 146 wpm. 'Sheep.' could not be measured; the speech check heard the name as 'Olafemus', so the name spelling may need a respell."))
P("3. "+pk("characters/CYC2/design/CYC2_designC_p2.mp3","Female, irritated neighbour: flattest designed take (2.2 st), 158 Hz; this is the one that clears the 2 st rule against Daniel and Odysseus (section 3).")+"\n")
P("**Crew / sailor**")
P("1. "+pk("characters/CREW/eleven_lib/C12_TimmyAnxiousNerd_CREW_v4.mp3","Best score (1.22): 227 Hz, 142 wpm, 'Nope.' not flat (3.3 st); 'Hello?' could not be measured (too few voiced frames)."))
P("2. "+pk("characters/CREW/eleven_lib/C11_LukasExcitedYouth_CREW_v4.mp3","Widest pitch (5.2 st) and 'Nope.' lively (12 st range); but 'Hello?' is FLAT (0.8 st)."))
P("3. "+pk("characters/CREW/design/CREW_designB_p1.mp3","Only designed take with a wide pitch (3.8 st) and a lively 'Hello?' (16 st) and 'Nope.' (3.4 st); slow (99 wpm) and big loudness swings (7.6 LU). Designed A and C crew voices sit at 114-125 Hz median, which is low for a young sailor.")+"\n")
# flat one-word lines
P("**One-word and short lines (flatness check).** F0 range (10th-90th percentile, semitones) inside the word, found with a local speech aligner; FLAT = under 2.0 st with at least 6 voiced frames. A 0.2-0.3 s word gives only 6-20 voiced frames, so this is a rough flag. 'Ah.' is not in the round-2 text set.\n")
fl=[];un=[]
for b,v in WD.items():
    for x in v["words"]:
        if x["status"]=="FLAT": fl.append(f"{b[:-4]} {x['word']} {x['f0_p10_p90_st']} st")
        elif x["status"]!="ok": un.append(f"{b[:-4]} {x['word']}")
P("- FLAT: "+"; ".join(fl)+".")
P(f"- Not measurable (word too short, or aligner heard a different word): {len(un)} cases, mostly 'Hello?' and 'Sheep.'; listen to these first. Clips: "+"; ".join(un[:40])+".")
P("- 'Nobody.' (Polyphemus): no clip is flat. Narrowest: OpenAI onyx 2.1 st, library Philip 2.2 st. 'Sheep.' (Cyclopes): the only measured flat one is OpenAI fable (1.3 st); the library and OpenAI echo/sage clips could not be measured.\n")
# Daniel
P("## 5. Daniel: best variant against the reference\n")
P("| trait | reference | D1 (#1) | D2a (#2) | D2b (#3) | D3 (#4) | D4 control (#5) | D5 (#6) |"); P("|---|---|---|---|---|---|---|---|")
ks=["D1_multilingual_v2_speed1.1_style0.25.mp3","D2a_v4_tagA_speed1.0.mp3","D2b_v4_tagB_speed1.0.mp3","D3_v4_tagA_speed1.1.mp3","D4_control_r1_multilingual_v2.mp3","D5_v4_tagA_speed1.2.mp3"]
for lab,key,ref in (("pace, wpm","wpm","178 (target 170-178)"),("pitch spread, st","pitch_spread_st","4.7"),("loudness range, LU","lra_lu","3.6"),("pauses per minute (0.3 s or more)","pauses_per_min","1.9"),("F0 mean, Hz","f0w_mean_hz","-")):
    P(f"| {lab} | {ref} | "+" | ".join(str(MD[k][key]) for k in ks)+" |")
P("")
P("- **Best by closeness: D2a (#2): eleven_v4, tag `[dry, deadpan, amused documentary narrator]`, stability 0.5, style 0.2, similarity 0.75, speaker boost on, speed 1.0.** 166 wpm (12 under the reference), 4.6 st (reference 4.7), LRA 4.1 LU (0.5 over). Score 1.4 against 2.1-5.4 for the others.")
P("- **Tag A against tag B:** D2b (tag `[wry, unhurried, quietly amused]`) is deeper (121 Hz) and wider (5.1 st, 4.9 LU) but slower (158 wpm).")
P("- **Speed does not buy pace in v4:** 1.0, 1.1 and 1.2 give 166, 163 and 162 wpm. The extra 'speed' setting is not the lever; if William wants 174 wpm, a 5% time-stretch in post on D2a (166 x 1.05 = 174, pitch kept) is the cleaner route (not done here).")
P("- **v4 against multilingual_v2 (what round 1 used):** the v4 clips more than double the loudness range (4.1-4.9 against 1.6-1.9 LU) and widen the pitch spread by about 1 st, matching the reference far better than the control (D4: 149 wpm, 3.8 st, 1.6 LU) or D1 (157 wpm, 3.3 st, 1.9 LU).")
P("- **Pauses:** every variant sits at 19-30 pauses per minute against the reference's 1.9. Same rule as the reference script (gaps 18 dB under the median, 0.3 s or more); the v4 takes have the fewest (19-22) against 28-30 for multilingual_v2. This is largely something editing can tighten (gap trimming), not a voice property.")
P("- **Tags:** a speech check of all six clips shows the tag text is not spoken aloud (all start 'Twelve men follow Odysseus into a cave...'); D2a heard 'a one-eyed kind' for 'the one-eyed kind', a small drift worth checking by ear.")
P("- Loudness is -22 to -23 LUFS raw (peaks -2.5 to -6 dB), no clipping.\n")
# reels
P("## 6. Reels: checks\n")
P("| reel | duration | integrated | LRA | true peak | contents (slate numbers, in order) |"); P("|---|---|---|---|---|---|")
P("| `reel2_daniel.mp3` | 2:16.8 | -19.5 LUFS | 3.9 LU | -1.3 dBFS | intro 'Daniel, narrator variants', then 1, 2, 3, 4, 5 (control), 6 (bonus) |")
P("| `reel2_characters.mp3` | 4:53.7 | -19.6 LUFS | 4.6 LU | -1.3 dBFS | intro; Odysseus 9, 11, 14, 17; Polyphemus 23, 26, 29, 44; Cyclopes 51, 54, 57, 59; crew 67, 68, 72, 76 |")
P("| `reel2_extra.mp3` | 3:22.0 | -19.5 LUFS | 4.2 LU | -1.3 dBFS | Odysseus 19, 18; Polyphemus 31, 41, 38, 39 (ram), 40 (prayer), 45 (ram), 46 (prayer); Cyclopes 62, 60; crew 74, 75 |")
P("- **Slate mapping:** slate number = the # of the clip (numbering from `scripts/plan.py`, the same one the table uses), verified by transcribing the slates in the rebuilt reels and by building each reel from a manifest (`_work/reel_manifest.json`). The Daniel reel was already correct (slates one to six at the expected offsets, six clips in the right order, 'control' on 5, 'bonus' on 6) and was left as it was.")
P("- **Characters reel rebuilt:** the first worker's `reel2_characters.mp3` (6:41) had been built before `plan.py` and `slates2.py` were last edited, so it did not match the current plan (extras mixed in, none of the main/extra split). It is kept as `_work/reel2_characters_OLD_prePlanEdit.mp3`. The new main reel and the extras reel use only existing slate audio (no new TTS).")
P("- **No clipping, level-matched:** every clip is brought to -19 LUFS (alimiter at 0.89, true peak -1.3 dBFS in all three reels, nothing above 0 dBFS); reel-level -19.5 to -19.6 LUFS. Slates are spoken at the same level as the clips.")
P("- **Not in a reel:** the two unselected previews of each of the 12 design prompts (24 of the 36 design previews) and the other library/OpenAI voices for the ram and prayer lines. They exist as raw files and in the table.\n")
# spend
P("## 7. Spend\n")
import collections
cnt=collections.defaultdict(int)
for r in LOGROWS:
    if r["clip"].startswith("slate-"): k="slates (River, multilingual_v2)"
    elif r["engine"]=="elevenlabs-voice-design": k="Voice Design (12 calls)"
    elif r["engine"]=="openai": k="OpenAI"
    elif r["model_id"]=="eleven_v4": k="eleven_v4 (4 Daniel + 18 library clips)"
    else: k="multilingual_v2 Daniel (D1, D4)"
    cnt[k]+=int(r["characters"])
P("| item | characters |"); P("|---|---|")
for k in ("multilingual_v2 Daniel (D1, D4)","eleven_v4 (4 Daniel + 18 library clips)","Voice Design (12 calls)","slates (River, multilingual_v2)","OpenAI"): P(f"| {k} | {cnt[k]:,} |")
el=sum(v for k,v in cnt.items() if k!="OpenAI")
oam=sum(MC[os.path.basename(r['file'])]['duration_s'] for r in rows if r['engine']=='openai')/60
P(f"| **ElevenLabs total** | **{el:,}** (plan credits, about ${el*0.182/1000:.2f} of plan value at $0.182 per 1,000; no extra charge) |")
P(f"| OpenAI gpt-4o-mini-tts | {cnt['OpenAI']:,} characters, {oam:.1f} minutes of audio, about ${oam*0.015:.2f} (at about $0.015/min) |")
P("")
P("- Log: `voice_log.csv` has 119 rows from the first worker; one row (OA-coral-CREW, 123 characters) was missing though the file exists and was backfilled with a marked note; no new call. The log also contains one slate (n77) not used by any reel.")
P("- **Quota (ElevenLabs subscription endpoint, Creator, limit 131,000):** before round 2: not recorded by the first worker; the round-1 report predicted about 16,660 used once all its calls were counted (counter then showed 12,931). **Read now (10:0x ET): 17,404 used, 113,596 left.** The counter lags the calls (round-1 note in TOOLS.md), so this reading does not yet include all of round 2. Expected true figure once it catches up: about 16,660 + 7,526 = **about 24,200 used, about 106,800 left** (an estimate; Voice Design may bill differently from 1 character per text character). Re-read the endpoint later to confirm.")
P("- No tier change, no overage, nothing deleted.\n")
# slots
P("## 8. My Voices slot usage\n")
import json as _j
V=_j.load(open("/tmp/voices.json"))["voices"]
aud=sorted(v["name"] for v in V if v["name"].startswith("BP ") and "(audition)" in v["name"])
P(f"- Voices named 'BP ... (audition)': **{len(aud)}** (the 22 added in round 1). With the 21 premade voices the account lists 43 voices. Slots: **22 of 30 used, 8 free** (the API field `voice_slots_used` reads 0, so I am counting the library voices myself, as the round-1 note did).")
P("- **Designed voices created this round: 0** (previews only; see section 2). Nothing was deleted or added.")
P("- Audition voices: "+", ".join(n.replace("BP ","").replace(" (audition)","") for n in aud)+".\n")
# guide
P("## 9. What to tell me (so round 3 is targeted)\n")
P("Answer any of these in a word per voice or per role, using the slate number:")
P("- **Narrator (Daniel, clips 1-6):** closest to what you want? Too slow, too flat, too dry or too lively? Does the tag version (2, 3, 4, 6) sound better than the plain version (1, 5)? Fast enough, or should I speed it up in post (about 5%)?")
P("- **Too deep / too high:** say 'deeper' or 'lighter' by number (Polyphemus is the usual one: 3 of the designed bass takes are 95-100 Hz, #31 is the pitched-down one at 80 Hz).")
P("- **Too young / too old:** most useful for Odysseus (designs A 40-45, B 35-40, C 50-55) and the crew (18-25).")
P("- **Too cartoonish / too theatrical:** especially Polyphemus and the Cyclopes; say if you want 'plain' instead.")
P("- **Wrong accent:** Odysseus tried Greek-Cypriot (A), neutral American (B) and Scottish (C); Polyphemus Southern US (A), West Country (B), Newfoundland (C); Cyclopes Yorkshire (A), Black Country (B), Northern Irish female (C); crew Irish (A), West Country (B), Appalachian American (C). Say which accent family to keep or drop.")
P("- **Too much energy / too flat:** the crew's 'Nope.' and 'Hello?', the Cyclopes' 'Sheep.' and Polyphemus' 'Nobody.' (the flagged lines in section 4).")
P("- **Name:** 'Polyphemus' (written 'Pollifeemus' for the TTS) was misheard by the speech check in the Cyclopes line for Drew, sage and fable; tell me if any sound wrong.")
P("- **Casting:** is a female Cyclopes chorus (#57) acceptable? Should Odysseus avoid the library 'Daniel' name?")
P("- **Keep / drop:** name up to 3 numbers per role to keep; I will use those as the base and save them as designed voices (1 slot each, 8 free).")
P("- **Round-3 candidate moves:** re-prompt the winner of each role with the adjectives you give me, make a second Voice Design batch from the best prompt, try speed 1.0 plus a 5% post stretch on Daniel, and test the full cast on a 20-second scene.")
open(f"{OUT}/AUDITION2.md","w").write("\n".join(pre)+"\n"+"\n".join(out[2:])+"\n\n"+"\n".join(body)+"\n")
print("written",os.path.getsize(f"{OUT}/AUDITION2.md"))
