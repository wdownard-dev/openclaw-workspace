#!/usr/bin/env python3
"""set_status.py <channel_id> approved|info_only|ignored|new. approved also adds the channel to candidates.json (approved=true,
verdict watch_screen) so watch.py scans it. info_only/ignored remove it from approval."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATE, CANDS = os.path.join(HERE, "discovery_state.json"), os.path.join(HERE, "candidates.json")
if len(sys.argv) != 3 or sys.argv[2] not in ("approved", "info_only", "ignored", "new"):
    sys.exit(__doc__)
cid, status = sys.argv[1:]
st = json.load(open(STATE))
ch = st["channels"].setdefault(cid, {"name": cid, "subs": None, "status": "new", "videos": {}})
ch["status"] = status
json.dump(st, open(STATE, "w"), indent=1)
c = json.load(open(CANDS))
ent = next((x for x in c["candidates"] if x.get("channel_id") == cid), None)
if status == "approved" and not ent:
    c["candidates"].append({"name": ch["name"], "channel_id": cid, "channel_url": f"https://www.youtube.com/channel/{cid}", "verdict": "watch_screen",
                            "gta_rp": False, "approved": True, "evidence": "approved via gta6_discovery set_status.py"})
elif ent and ent.get("approved") != (status == "approved") and "discovery" in str(ent.get("evidence", "")):
    ent["approved"] = status == "approved"
elif status == "approved" and ent:
    ent["approved"] = True
json.dump(c, open(CANDS, "w"), indent=1)
print(f"{ch['name']} ({cid}) -> {status}")
