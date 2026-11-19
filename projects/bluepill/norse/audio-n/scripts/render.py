"""Render passages with the with-timestamps endpoint. Usage: render.py <P01 P02 ...|all> [--force]
Daniel onwK4e9ZLuTAKqWW03F9, eleven_multilingual_v2, stability 0.5 / style 0.2 / speed 1.0 / similarity 0.75 / boost on, previous_text/next_text from the neighbouring passages.
Any non-200 / non-JSON response stops everything (no retry loop). Cached: skips a passage that already has passages/Pxx.json unless --force (force = a logged retake)."""
import os, sys, json, csv, time, base64, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
OUT = os.path.dirname(HERE); PD = os.path.join(OUT, "passages")
VOICE = "onwK4e9ZLuTAKqWW03F9"; MODEL = "eleven_multilingual_v2"; FMT = "mp3_44100_192"
SET = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True, "speed": 1.0}
LOG = os.path.join(OUT, "voice_log.csv")
COLS = ["time", "passage", "beats", "script_words", "characters", "model_id", "voice_id", "settings", "output_format", "audio_s", "speech_s", "wpm", "api_seconds", "note"]

def run(pid, force=False, note=""):
    plan = json.load(open(os.path.join(OUT, "plan.json")))["passages"]
    p = next(x for x in plan if x["id"] == pid)
    jp = os.path.join(PD, pid + ".json")
    if os.path.exists(jp) and not force: print("cached", pid); return
    body = {"text": p["text"], "model_id": MODEL, "voice_settings": SET}
    if p["prev"]: body["previous_text"] = p["prev"]
    if p["next"]: body["next_text"] = p["next"]
    bp = os.path.join(OUT, "_work", "_body.json"); open(bp, "w").write(json.dumps(body))
    t0 = time.time()
    r = subprocess.run(["curl", "-s", "-m", "240", "-w", "\n%{http_code}", "-X", "POST",
                        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format={FMT}",
                        "-H", "xi-api-key: " + os.environ["ELEVENLABS_API_KEY"], "-H", "Content-Type: application/json", "-d", "@" + bp],
                       capture_output=True, text=True)
    body_txt, _, code = r.stdout.rpartition("\n")
    if code != "200": raise SystemExit(f"STOP: API error {code} on {pid}: {body_txt[:400]} {r.stderr[:200]}")
    d = json.loads(body_txt)
    if "audio_base64" not in d: raise SystemExit(f"STOP: no audio on {pid}: {str(d)[:400]}")
    if os.path.exists(jp):   # keep the previous take
        k = 1
        while os.path.exists(os.path.join(PD, f"{pid}_take{k}.json")): k += 1
        os.rename(jp, os.path.join(PD, f"{pid}_take{k}.json")); os.rename(os.path.join(PD, pid + ".mp3"), os.path.join(PD, f"{pid}_take{k}.mp3"))
    open(os.path.join(PD, pid + ".mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
    json.dump({"alignment": d["alignment"], "normalized_alignment": d.get("normalized_alignment"), "text": p["text"]}, open(jp, "w"))
    al = d["alignment"]; chars = al["characters"]; ts = al["character_start_times_seconds"]; te = al["character_end_times_seconds"]
    assert "".join(chars) == p["text"], f"alignment text differs from sent text on {pid}"
    idx = [i for i, c in enumerate(chars) if not c.isspace()]; speech = te[idx[-1]] - ts[idx[0]]; dur = te[-1]
    sw = sum(len(s["script"].split()) for s in p["segs"])
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(COLS)
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), pid, f'{p["beats"][0]}-{p["beats"][-1]}', sw, len(p["text"]), MODEL, VOICE, json.dumps(SET), FMT,
                    round(dur, 2), round(speech, 2), round(sw / speech * 60), round(time.time() - t0, 1), note])
    print(pid, "chars", len(p["text"]), "audio_s", round(dur, 2), "speech_s", round(speech, 2), "wpm(script words)", round(sw / speech * 60), "api_s", round(time.time() - t0, 1))

if __name__ == "__main__":
    a = sys.argv[1:]; force = "--force" in a; a = [x for x in a if not x.startswith("--")]
    plan = json.load(open(os.path.join(OUT, "plan.json")))["passages"]
    ids = [p["id"] for p in plan] if a == ["all"] else a
    for pid in ids: run(pid, force, "retake" if force else "")
