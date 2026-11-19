"""Builds AUDITION.md from voice_log.csv, shortlist_shared.json, account_voices.json and the metrics_*.json files."""
import os, sys, json, csv, glob
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE); sys.path.insert(0,HERE)
from catalog import *
W=f"{OUT}/_work"
sh=json.load(open(f"{W}/shortlist_shared.json")); acct={v['voice_id']:v for v in json.load(open(f"{W}/account_voices.json"))['voices']}
M={}
for f in glob.glob(f"{W}/metrics_*.json"): M.update(json.load(open(f)))
def info(vid):
    if vid in sh:
        v=sh[vid]; l=f"{v['accent']}, {v['age']}, {v['descriptive'] or '-'}, {v['use_case']}"
        mods=[m['model_id'] for m in v.get('verified_languages',[])]
        lic=f"library, rate {v['rate']:g}, owner notice {v.get('notice_period')} d, live-moderation {'ON' if v['live_moderation_enabled'] else 'off'}"
        return (v['description'] or '').replace('\n',' ')[:105],l,lic
    v=acct[vid]; lb=v['labels']
    return (v.get('description') or '')[:105],f"{lb.get('accent')}, {lb.get('age')}, {lb.get('descriptive')}, {lb.get('use_case')}","premade, no owner notice"
def row(num,clip,fname,vname,vid,extra=""):
    m=M[os.path.basename(fname)]; d,l,lic=info(vid)
    return f"| {num} | `{fname}` | **{vname}**: {d} [{l}] ({lic}){extra} | {m['duration_s']} | {m['wpm_total']} | {m['pitch_spread_st']} | {m['lufs']} / {m['lra_lu']} |"
H="| # | file | voice: description [labels] (licence) | s | wpm | pitch st | LUFS / LRA |\n|---|---|---|---|---|---|---|"
L=[]
L.append(open(f"{HERE}/audition_head.md").read())
L.append("## Narrator clips (`narrators/`)\nFirst pass: 143 characters (beats 01 + 11), eleven_multilingual_v2, stability 0.5, style 0.2, boost on, speed 1.0. Spoken slate in the reel = the N number.\n")
L.append(H)
for c,n,v,s,note in NARRATORS:
    L.append(row(c,c,f"narrators/{c}_{n}.mp3",n,v))
L.append("\nLonger script (266 characters, beats 01, 02, 08, 11), same settings, top 4 by closeness to the reference plus N03 as the dry-British entry:\n")
L.append(H)
for c in ("N03","N05","N07","N08","N09"):
    n=[x for x in NARRATORS if x[0]==c][0]
    L.append(row(c+"L",c+"L",f"narrators/{c}L_{n[1]}.mp3",n[1],n[2]))
n=[x for x in NARRATORS if x[0]=="N09"][0]
L.append(row("N09 V1","N09","narrators/N09L_SpudsOxley_set-V1-0.75-0.05.mp3",n[1],n[2]," **settings V1 0.75 / 0.05**"))
L.append(row("N09 act","N09","narrators/N09L_SpudsOxley_set-act-0.4-0.3.mp3",n[1],n[2]," **settings 0.4 / 0.3**"))
L.append("\nModel side test (Eleven v4 with an audio tag, 195 characters incl. tag; the tag text should not be spoken, I cannot confirm that by ear):\n")
L.append(H)
for c in ("N01","N09"):
    n=[x for x in NARRATORS if x[0]==c][0]
    L.append(row(c+" v4",c,f"narrators/{c}_{n[1]}_model-eleven_v4-tag.mp3",n[1],n[2]," **eleven_v4, `[dry, deadpan, amused documentary narrator]`**"))
oa=M["O01_OpenAI-gpt-4o-mini-tts_onyx.mp3"]
L.append(f"\n| O01 | `narrators/O01_OpenAI-gpt-4o-mini-tts_onyx.mp3` | OpenAI gpt-4o-mini-tts, voice onyx, instruction 'dry, amused documentary narrator' (12 words only; not in the reel) | {oa['duration_s']} | {oa['wpm_total']} | {oa['pitch_spread_st']} | {oa['lufs']} / {oa['lra_lu']} |")
L.append("\n## Character clips (`characters/`)\nSame lines as the Nobody exchange and neighbours (beats 28-33, 37, 39, 44 and a few one-liners), 144-217 characters, stability 0.4, style 0.3, boost on, speed 1.0. In the reel the spoken slate gives the role and the candidate number within the role (Odysseus one = C01, Polyphemus two = C05, and so on).\n")
L.append(H)
for r,l in CHARS.items():
    for c,n,v,s,note in l:
        L.append(row(c,c,f"characters/{c}_{r}_{n}.mp3",f"{r} {n}",v))
L.append(open(f"{HERE}/audition_tail.md").read())
open(f"{OUT}/AUDITION.md","w").write("\n".join(L))
print("ok",len("\n".join(L)))
