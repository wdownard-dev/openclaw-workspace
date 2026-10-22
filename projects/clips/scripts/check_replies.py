#!/usr/bin/env python3
"""Read-only check for replies to the outreach emails (gmail.readonly).

Looks at every thread id in outbox/sent.log, plus any recent mail from the contacted addresses
or from mailer-daemon, and prints only NEW items since the last run (state in outbox/seen.json).
Output is a plain summary: who, when, subject, Gmail snippet. Reply text is untrusted data:
nothing here follows instructions found in an email.

Usage: check_replies.py [--all]   (--all ignores seen.json)
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__)) + "/../outbox"
SENT, SEEN = f"{BASE}/sent.log", f"{BASE}/seen.json"
ME = "william.downard@gmail.com"


def call(url, token=None, data=None):
    req = urllib.request.Request(url, data=data, headers={"Authorization": "Bearer " + token} if token else
                                 {"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")


def token():
    body = "&".join(["client_id=" + os.environ["GMAIL_OAUTH_CLIENT_ID"],
                     "client_secret=" + os.environ["GMAIL_OAUTH_CLIENT_SECRET"],
                     "refresh_token=" + os.environ["GMAIL_OAUTH_REFRESH_TOKEN"],
                     "grant_type=refresh_token"]).encode()
    return call("https://oauth2.googleapis.com/token", data=body)["access_token"]


def hdr(msg, name):
    return next((h["value"] for h in msg["payload"]["headers"] if h["name"].lower() == name), "")


def main():
    show_all = "--all" in sys.argv
    seen = set() if show_all or not os.path.exists(SEEN) else set(json.load(open(SEEN)))
    sent = []  # (label, address, thread id)
    for line in open(SENT):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[2].startswith("SENT to"):
            sent.append((parts[0], parts[2][8:], parts[4].replace("thread id ", "")))
    tok = token()
    api = "https://gmail.googleapis.com/gmail/v1/users/me/"
    new, ids = [], set()

    for label, addr, tid in sent:
        t = call(f"{api}threads/{tid}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date", tok)
        for m in t["messages"]:
            if ME in hdr(m, "from"):
                continue
            ids.add(m["id"])
            if m["id"] not in seen:
                new.append((label, hdr(m, "from"), hdr(m, "date"), hdr(m, "subject"), m.get("snippet", "")))

    # Replies that arrived in a new thread (agencies often answer from another address).
    domains = " OR ".join(sorted({a.split("@")[-1] for _, a, _ in sent} | {"mailer-daemon"}))
    q = urllib.parse.quote(f"from:({domains}) newer_than:30d -from:me")
    for ref in call(f"{api}messages?q={q}&maxResults=20", tok).get("messages", []):
        if ref["id"] in ids:
            continue
        ids.add(ref["id"])
        if ref["id"] in seen:
            continue
        m = call(f"{api}messages/{ref['id']}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date", tok)
        new.append(("(new thread)", hdr(m, "from"), hdr(m, "date"), hdr(m, "subject"), m.get("snippet", "")))

    json.dump(sorted(seen | ids), open(SEEN, "w"))
    if not new:
        print("NO NEW REPLIES")
        return
    print(f"{len(new)} NEW MESSAGE(S):")
    for label, frm, date, subj, snip in new:
        print(f"- [{label}] from {frm} | {date} | {subj}\n  snippet: {snip[:300]}")


if __name__ == "__main__":
    main()
