#!/usr/bin/env python3
"""OpusClip credit guard for the GTA 6 push. Reads gaming-caps.json, keeps gaming-ledger.json.
Never submits anything; it only answers "may we?" and records spend.

  gaming_budget.py status
  gaming_budget.py can-spend SOURCE_MINUTES [--video ID]   JSON verdict (exit 0 = allowed, 3 = not allowed)
  gaming_budget.py record VIDEO_ID CREDITS [--note TEXT]   add to the ledger
"""
import json, os, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CAPS = os.path.join(HERE, "gaming-caps.json")
LEDGER = os.path.join(HERE, "gaming-ledger.json")
ET = ZoneInfo("America/New_York")


def caps():
    return json.load(open(CAPS))


def ledger():
    return json.load(open(LEDGER)) if os.path.exists(LEDGER) else {"entries": []}


def totals(now=None):
    now = now or datetime.now(ET)
    c = caps()
    start = datetime.fromisoformat(c["launch_week_start"]).replace(tzinfo=ET)
    end = datetime.fromisoformat(c["launch_week_end"]).replace(tzinfo=ET) + timedelta(days=1)
    week = day = 0.0
    for e in ledger()["entries"]:
        t = datetime.fromisoformat(e["ts"])
        if start <= t < end:
            week += e["credits"]
        if t.date() == now.date():
            day += e["credits"]
    return week, day


def can_spend(minutes, now=None):
    c = caps()
    cost = int(round(minutes * c["credits_per_source_minute"]))
    week, day = totals(now)
    why = []
    if minutes > c["auto_submit_max_source_min"]:
        why.append(f"source {minutes:.0f} min > {c['auto_submit_max_source_min']} min auto limit: flag for ffmpeg cut or ask William")
    if week + cost > c["launch_week_cap"]:
        why.append(f"launch-week cap: {week:.0f}+{cost} > {c['launch_week_cap']}")
    if day + cost > c["daily_cap"]:
        why.append(f"daily cap: {day:.0f}+{cost} > {c['daily_cap']}")
    return {"allowed": not why, "cost": cost, "week_spent": week, "day_spent": day, "reasons": why}


def record(video, credits, note=""):
    lg = ledger()
    lg["entries"].append({"ts": datetime.now(ET).isoformat(timespec="seconds"), "video": video, "credits": credits, "note": note})
    json.dump(lg, open(LEDGER, "w"), indent=1)


def main(argv):
    if not argv or argv[0] == "status":
        w, d = totals()
        c = caps()
        print(json.dumps({"week_spent": w, "week_cap": c["launch_week_cap"], "day_spent": d, "daily_cap": c["daily_cap"]}))
    elif argv[0] == "can-spend":
        v = can_spend(float(argv[1]))
        print(json.dumps(v))
        return 0 if v["allowed"] else 3
    elif argv[0] == "record":
        note = argv[argv.index("--note") + 1] if "--note" in argv else ""
        record(argv[1], float(argv[2]), note)
        print("recorded")
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
