"""Fact-check guard. check(slug) -> (passed, report_markdown, details).
Every line of script.json (reactions + outro) must either carry fact ids that verify against the stored official page text,
or contain no factual content. "Factual content" is detected mechanically: any digit/number, month name, or capitalised term
(not sentence-initial) that is not (a) inside a linked fact quote, (b) said in the transcript, or (c) in the always-allowed list.
Reactions must also point at a real transcript moment (quote found within +-2 s of t)."""
import json, os, re
import facts as F

HERE = os.path.dirname(os.path.abspath(__file__))
MONTHS = "january february march april may june july august september october november december".split()
SENT_END = re.compile(r"[.!?:]\s*$")


def words_in(s):
    return re.findall(r"[A-Za-z0-9$][A-Za-z0-9$'\-.,]*", s)


def terms(text):
    """numbers and capitalised terms (not first word of a sentence) -> list"""
    out, prev_end = [], True
    toks = re.findall(r"[A-Za-z0-9$][A-Za-z0-9$'\-.,%]*[.!?:]?|[.!?:]", text)
    for tk in toks:
        bare = tk.rstrip(".!?:,")
        if re.search(r"\d", bare):
            out.append(bare.replace(",", "").strip("."))
        elif bare and bare[0].isupper() and not prev_end:
            out.append(bare.strip("'"))
        elif bare.lower() in MONTHS:
            out.append(bare)
        prev_end = tk[-1] in ".!?:"
    return out


def date_forms(date):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date or ""):
        return ""
    y, m, d = date.split("-")
    mn = MONTHS[int(m) - 1]
    return f"{mn} {int(d)} {mn[:3]} {int(d)} {mn} {int(d):02d} {y}"


def contains(hay_norm, term):
    t = F.norm(term).replace(",", "")
    return t in hay_norm.replace(",", "")


def transcript_text(slug):
    d = json.load(open(os.path.join(HERE, "work", slug, "transcript.json")))
    return d


def level_cfg(level=None):
    lv = level or F.CFG.get("interrupt_level", "low")
    return lv, F.CFG["levels"][lv]


def est_dur(text):
    return 0.38 * len(text.split()) + 0.3


def check(slug, script=None, facts=None, level=None):
    base = os.path.join(HERE, "work", slug)
    cfg = F.CFG
    level, LV = level_cfg(level)
    script = script or json.load(open(os.path.join(base, "script.json")))
    facts_all = facts if facts is not None else json.load(open(os.path.join(base, "facts.json")))
    valid, fact_problems = F.verify(slug, facts_all)
    tr = transcript_text(slug)
    allw_raw = [w for sg in tr["segments"] for w in sg["words"]]
    allowed = {F.norm(x) for x in cfg["always_allowed_terms"]} | {F.norm(x) for x in script.get("allow_terms", [])}
    rows, errors = [], []
    for p in fact_problems:
        errors.append("FACT " + p)
    clip = script["clip"]
    cs, ce = clip["start"], clip["start"] + clip["len"]

    def line_check(kind, lid, text, fact_ids, t=None, quote=None, maxw=None):
        row = {"id": lid, "kind": kind, "text": text, "facts": fact_ids, "issues": []}
        n = len(text.split())
        if n > (maxw or cfg["max_line_words"]):
            row["issues"].append(f"{n} words (max {maxw or cfg['max_line_words']})")
        for fid in fact_ids:
            if fid not in valid:
                row["issues"].append(f"fact '{fid}' missing or failed verification")
        hay = " ".join(F.norm(valid[f]["quote"]) + " " + date_forms(valid[f]["date"]) for f in fact_ids if f in valid)
        win = ""
        if kind in ("interjection", "card"):
            if t is None or not (cs <= t <= ce):
                row["issues"].append(f"t={t} outside the shown clip window {cs}-{ce}")
            allw = []
            for sg in tr["segments"]:
                for w in sg["words"]:
                    if w["w"].startswith(",") and allw and re.search(r"\d$", allw[-1][0]):
                        allw[-1] = (allw[-1][0] + re.sub(r"[^a-z0-9$]", "", w["w"].lower()), dict(allw[-1][1], end=w["end"]))
                        continue
                    allw.append((re.sub(r"[^a-z0-9$]", "", w["w"].lower()), w))
            qt = [re.sub(r"[^a-z0-9$]", "", x.lower()) for x in (quote or "").split()]
            qt = [x for x in qt if x]
            hit = None
            for i in range(len(allw) - len(qt) + 1):
                if qt and [a for a, _ in allw[i:i + len(qt)]] == qt:
                    hit = i
                    if t is not None and abs(allw[i][1]["start"] - t) <= 2.0:
                        break
            if hit is None:
                row["issues"].append("'quote' is not in the transcript")
            else:
                a0, a1 = allw[hit][1]["start"], allw[hit + len(qt) - 1][1]["end"]
                if t is not None and abs(a0 - t) > 2.0:
                    row["issues"].append(f"transcript quote starts at {a0}s, not within 2 s of t={t}")
                win = F.norm(" ".join(w["w"] for _, w in allw if a0 - 1.0 <= w["start"] <= a1 + 1.0))
        if kind == "interjection" and t is not None:
            clash = [w for w in allw_raw if w["end"] > t - 0.05 and w["start"] < t + 0.3]
            if clash:
                row["issues"].append(f"starts at t={t} but the clip is speaking ('{clash[0]['w']}' {clash[0]['start']}-{clash[0]['end']}): start inside a pause (see: render_cohost.py gaps {slug})")
            for a, b in clip.get("protect", []):
                if t < b and t + est_dur(text) > a:
                    row["issues"].append(f"spoken span {t}-{t + est_dur(text):.1f} overlaps protected key line {a}-{b}")
            if est_dur(text) > LV["max_interjection_s"]:
                row["issues"].append(f"estimated {est_dur(text):.1f}s exceeds {LV['max_interjection_s']}s ({level})")
        if kind == "card":
            dl = LV["card_dur"]
            if not (dl[0] <= row_dur.get(lid, dl[0]) <= dl[1]):
                row["issues"].append(f"card dur must be {dl[0]}-{dl[1]} s")
        for tm in terms(text):
            nt = F.norm(tm)
            if nt in allowed:
                continue
            if hay and contains(hay, tm):
                continue
            if kind in ("interjection", "card") and win and contains(win, tm):
                continue
            row["issues"].append(f"unsourced term '{tm}' (not in linked fact quotes{' or transcript window' if kind in ('interjection', 'card') else ''})")
        if kind == "outro_takeaway" and not fact_ids:
            row["issues"].append("takeaway line has no fact id")
        row["status"] = "PASS" if not row["issues"] else "FAIL"
        rows.append(row)
        for i in row["issues"]:
            errors.append(f"{lid}: {i}")

    row_dur = {c["id"]: c.get("dur", 0) for c in script.get("cards", [])}
    ij, cards = script.get("interjections", []), script.get("cards", [])
    if len(ij) > LV["max_interjections"]:
        errors.append(f"{len(ij)} spoken interjections; interrupt_level '{level}' allows {LV['max_interjections']}")
    if len(cards) > LV["max_cards"]:
        errors.append(f"{len(cards)} cards; interrupt_level '{level}' allows {LV['max_cards']}")
    for r in ij:
        line_check("interjection", r["id"], r["text"], r.get("facts", []), r.get("t"), r.get("quote"))
    for r in cards:
        line_check("card", r["id"], r["text"], r.get("facts", []), r.get("t"), r.get("quote"), cfg["max_card_words"])
    parts = [o["part"] for o in script["outro"]]
    order = [p for i, p in enumerate(parts) if i == 0 or p != parts[i - 1]]
    if order != ["takeaway", "opinion", "question"]:
        errors.append(f"outro parts must be takeaway, opinion, question in order (got {order})")
    for i, o in enumerate(script["outro"]):
        line_check("outro_" + o["part"], o.get("id", f"o{i+1}"), o["text"], o.get("facts", []))
    if not any(o["part"] == "takeaway" and o.get("facts") for o in script["outro"]):
        errors.append("outro needs at least one fact-linked takeaway line")
    if not any(o.get("card") for o in script["outro"]):
        errors.append("outro needs an on-screen source card on a fact line (card field)")
    for o in script["outro"]:
        if o.get("card") and not set(o.get("facts", [])) & set(valid):
            errors.append(f"{o.get('id')}: card shown without a verified fact")

    passed = not errors
    md = [f"# Fact-check report: {slug}", "", f"**Result: {'PASS' if passed else 'FAIL'}**  (structure: {script.get('structure')}, interrupt_level: {level})", "",
          "Guard: every factual claim must link to a fact whose quote was found verbatim on its official page; digits, month names and proper nouns in script lines must appear in a linked quote (or in the clip transcript near the moment). Spoken interjections must start in a transcript pause.", "",
          "## Facts (all from official pages, quote checked verbatim against the fetched page)", "",
          "| id | date | quote | source | verified |", "|---|---|---|---|---|"]
    for f in facts_all:
        md.append(f"| {f.get('id')} | {f.get('date')} | \"{f.get('quote','')}\" | {f.get('url')} | {'yes' if f.get('id') in valid else 'NO'} |")
    md += ["", "## Claims by script line", "", "| line | kind | text | fact ids | status |", "|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['id']} | {r['kind']} | {r['text']} | {', '.join(r['facts']) or '-'} | {r['status']}{(': ' + '; '.join(r['issues'])) if r['issues'] else ''} |")
    md += ["", "## Lines tied to the transcript", ""]
    for r in ij + cards:
        md.append(f"- t={r.get('t')} s, clip says: \"{r.get('quote')}\" -> NULL ({'spoken' if r in ij else 'card'}): \"{r['text']}\"")
    if script.get("allow_terms"):
        md += ["", f"## Terms allowed without a source (topic names, declared in script.json): {', '.join(script['allow_terms'])}"]
    if script.get("derived_notes"):
        md += ["", "## Derived statements (opinion or arithmetic, not quoted facts; read against the quotes)", ""] + [f"- {n}" for n in script["derived_notes"]]
    if errors:
        md += ["", "## Problems", ""] + [f"- {e}" for e in errors]
    md += ["", "## Limits of this check", "",
           "It proves quotes exist on official pages and that numbers/names in the script come from those quotes. It does not prove the quote supports the sentence's meaning; a human (or the agent) must read each fact-linked line against its quote before publishing."]
    return passed, "\n".join(md) + "\n", valid
