#!/usr/bin/env python3
"""Pull live English-language streamers per Twitch category for outreach candidates.

Usage: twitch_candidates.py OUTFILE [--per-cat 4] [--min 300] [--max 8000]
Skips streamers already listed in projects/clips/permissions.md. Credentials: TWITCH_CLIENT_ID /
TWITCH_CLIENT_SECRET (egress-proxy sentinels). Output is a markdown table; viewer counts are a
single snapshot.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

CATS = {  # name: game_id (from helix/games/top, 2026-10-21)
    "Just Chatting": "509658", "Fortnite": "33214", "Minecraft": "27471", "VALORANT": "516575",
    "Counter-Strike": "32399", "ARC Raiders": "464339927", "Call of Duty: MW4": "1478650472",
    "League of Legends": "21779", "Apex Legends": "511224", "Elden Ring": "512953",
}
HERE = os.path.dirname(os.path.abspath(__file__))


def get(url, tok=None, data=None):
    h = {"Authorization": "Bearer " + tok, "Client-Id": os.environ["TWITCH_CLIENT_ID"]} if tok else {}
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=60) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--per-cat", type=int, default=4)
    ap.add_argument("--min", type=int, default=300)
    ap.add_argument("--max", type=int, default=8000)
    a = ap.parse_args()

    body = "&".join(["client_id=" + os.environ["TWITCH_CLIENT_ID"],
                     "client_secret=" + os.environ["TWITCH_CLIENT_SECRET"],
                     "grant_type=client_credentials"]).encode()
    tok = get("https://id.twitch.tv/oauth2/token", data=body)["access_token"]
    known = set(m.lower() for m in re.findall(r"^\| (\S+) \|", open(f"{HERE}/../permissions.md").read(), re.M))
    rows, seen = [], set()
    for cat, gid in CATS.items():
        d = get(f"https://api.twitch.tv/helix/streams?game_id={gid}&first=100&language=en", tok)["data"]
        n = 0
        for s in sorted(d, key=lambda s: -s["viewer_count"]):
            u = s["user_login"]
            if u.lower() in known or u in seen or s.get("is_mature") or not (a.min <= s["viewer_count"] <= a.max):
                continue
            seen.add(u)
            rows.append((cat, s["user_name"], u, s["viewer_count"], s["title"][:50].replace("|", "/")))
            n += 1
            if n >= a.per_cat:
                break
    with open(a.out, "w") as f:
        f.write("# Scope A candidates (Twitch API snapshot; mature-flagged streams excluded)\n\n")
        f.write("| Category | Streamer | Login | Viewers | Stream title |\n|---|---|---|---|---|\n")
        for r in rows:
            f.write("| " + " | ".join(str(x) for x in r) + " |\n")
    print(f"wrote {len(rows)} candidates to {a.out}")


if __name__ == "__main__":
    main()
