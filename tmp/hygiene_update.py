import json, subprocess, sys

PARA = ("TELEGRAM HYGIENE (William, 2026-11-08): Send at most ONE message per run, and only for a finished result, a failure, or a decision William must make. "
        "Never send progress, status or 'in progress / retrying / working on it / digest follows' messages, and do not use the message tool mid-run for progress. "
        "If nothing is new or actionable, reply NO_REPLY. Non-urgent routine numbers belong in the 8:15 AM digest, not a separate message. "
        "When a decision is needed, name the specific clip or item and offer 2-3 clear options so he can answer in one word.")

IDS = sys.argv[1:]

def get(i):
    r = subprocess.run(["openclaw", "automations", "get", i], capture_output=True, text=True)
    return json.loads(r.stdout)

for i in IDS:
    d = get(i)
    name = d["name"]
    p = d["payload"]
    msg = p.get("message")
    if d.get("enabled") is not True:
        print(i, name, "SKIP not enabled"); continue
    if p.get("kind") != "agentTurn" or msg is None:
        print(i, name, "SKIP payload kind", p.get("kind")); continue
    if msg.startswith("TELEGRAM HYGIENE"):
        print(i, name, "SKIP already has paragraph"); continue
    if "truncated" in msg[-40:].lower() or "…" in msg[-3:]:
        print(i, name, "STOP possible truncation"); continue
    new = PARA + "\n\n" + msg
    r = subprocess.run(["openclaw", "automations", "edit", i, "--message", new], capture_output=True, text=True)
    if r.returncode != 0:
        print(i, name, "EDIT FAILED", r.stderr[:300], r.stdout[:300]); continue
    d2 = get(i)
    m2 = d2["payload"]["message"]
    ok = m2.startswith(PARA + "\n\n") and m2[len(PARA) + 2:] == msg and len(m2) == len(msg) + len(PARA) + 2
    # confirm nothing else changed
    d["payload"] = {k: v for k, v in d["payload"].items() if k != "message"}
    d2["payload"] = {k: v for k, v in d2["payload"].items() if k != "message"}
    skip = {"updatedAtMs", "configRevision", "state"}
    diff = [k for k in d if k not in skip and d[k] != d2.get(k)]
    print(i, name, "OK" if ok else "VERIFY FAILED", "old", len(msg), "new", len(m2), "otherDiff", diff)
