#!/usr/bin/env python3
"""Optional live-chat replay signal. Prints CHAT_UNAVAILABLE and exits 0 when the VOD has no chat replay.

  signals_chat.py VIDEO_ID_OR_URL [--out DIR]

Tries yt-dlp --skip-download --write-subs --sub-langs live_chat. If a live_chat.json exists, computes messages per 30 s
(z-scored) and an emote-spam score (share of messages that are short/repeated/caps), writes OUT/<id>.chat.json:
{"hop":30,"windows":[[start, msgs, spam, cz], ...]}. Edited uploads normally have no chat replay.
"""
import argparse, glob, json, os, re, subprocess, sys
import numpy as np

YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
HERE = os.path.dirname(os.path.abspath(__file__))


def video_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    a = ap.parse_args()
    vid = video_id(a.video)
    os.makedirs(a.out, exist_ok=True)
    try:
        subprocess.run([YTDLP, "--no-warnings", "--ignore-no-formats-error", "--skip-download", "--write-subs",
                        "--sub-langs", "live_chat", "-o", os.path.join(a.out, "%(id)s"),
                        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        pass
    files = glob.glob(os.path.join(a.out, f"{vid}.live_chat.json"))
    if not files:
        print(f"CHAT_UNAVAILABLE {vid}")
        sys.exit(0)
    times, spam = [], []
    for line in open(files[0], errors="ignore"):
        try:
            d = json.loads(line)
            act = d["replayChatItemAction"]
            ms = int(act["videoOffsetTimeMsec"])
            r = act["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]
            txt = "".join(x.get("text", x.get("emoji", {}).get("shortcuts", [":e:"])[0]) for x in r["message"]["runs"])
        except Exception:
            continue
        toks = txt.split()
        times.append(ms / 1000)
        spam.append(1.0 if (len(toks) <= 2 or len(set(toks)) <= max(1, len(toks) // 3) or txt.isupper()) else 0.0)
    if not times:
        print(f"CHAT_UNAVAILABLE {vid}")
        sys.exit(0)
    t = np.array(times)
    sp = np.array(spam)
    nb = int(t.max() // 30) + 1
    cnt = np.bincount((t // 30).astype(int), minlength=nb).astype(float)
    spm = np.bincount((t // 30).astype(int), weights=sp, minlength=nb) / np.maximum(cnt, 1)
    med = np.median(cnt)
    mad = np.median(np.abs(cnt - med)) * 1.4826 or (cnt.std() + 1e-9)
    z = (cnt - med) / mad
    rows = [[i * 30, int(cnt[i]), round(float(spm[i]), 2), round(float(z[i]), 2)] for i in range(nb)]
    outp = os.path.join(a.out, f"{vid}.chat.json")
    json.dump({"video": vid, "hop": 30, "windows": rows}, open(outp, "w"), separators=(",", ":"))
    print(f"CHAT {vid}: {len(times)} messages, wrote {outp}")


if __name__ == "__main__":
    main()
