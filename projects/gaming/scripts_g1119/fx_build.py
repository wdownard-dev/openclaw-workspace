#!/usr/bin/env python3
"""fx_build.py SPEC.json : Fluxx 0212 guide Short (own-footage, 9:16 source, burned-in captions removed by fx_decap.py).
Layout: source (720x1280, already footage over blur) scaled 1.5x to 1080x1920; title + yellow step labels top; word-by-word captions
in the lower blur zone. Reuses gbuild helpers (Liam TTS with timestamps, PNG overlays, durations)."""
import json, os, sys, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbuild as G
from PIL import Image, ImageDraw, ImageFont

B, FF, OUT = G.B, G.FF, G.OUT
SRC = B + "/work/fluxx_1119/src_nocap.mp4"
USD = G.USD


def main():
    spec = json.load(open(sys.argv[1])); slug = spec["slug"]; P = spec["parts"]; N = len(P)
    W = f"{B}/work/g1119/build_{slug}"; os.makedirs(W, exist_ok=True)
    text = " ".join(p["text"] for p in P); low = text.lower()
    bad = [h for h in G.HEDGES if h in low]
    if bad: sys.exit("LINT hedge words " + str(bad))
    print("words", len(spec["script_display"].split()))
    chars = 0; mp3s = []; als = []
    for p in P:
        m, al, c = G.tts(slug, p); mp3s.append(m); als.append(al); chars += c
    ds = [G.dur(m) for m in mp3s]
    GAP = 0.2; starts = []; t = 0.15
    for d in ds: starts.append(t); t += d + GAP
    total = t + 0.4
    print("part durs", [round(x, 1) for x in ds], "total", round(total, 1), "tts chars new", chars, "usd", round(chars * USD, 3))
    if os.environ.get("DRY"): return
    edges = [0] + [starts[i] - 0.05 for i in range(1, N)] + [total]
    segs = []  # (src_start, src_len, out_dur)
    for i, p in enumerate(P):
        a, b = edges[i], edges[i + 1]; tot = sum(e - s for s, e in p["clips"])
        for s, e in p["clips"]:
            d = (b - a) * (e - s) / tot
            print(f"  {p['key']}: src {s}-{e} -> {d:.2f}s speed {(e - s) / d:.2f}x")
            segs.append((s, e - s, d))
    ov = []
    G.line_png(f"{W}/title.png", spec["title"], 64, 8, "white", H=150); ov.append((f"{W}/title.png", None, None, 70))
    for i, p in enumerate(P):
        if p.get("label"):
            G.line_png(f"{W}/lab{i}.png", p["label"], 66, 8, "#FFE14D", box=True, H=150)
            ov.append((f"{W}/lab{i}.png", starts[i], starts[i + 1] - 0.05 if i < N - 1 else total, 215))
    import re
    ci = 0
    for i, p in enumerate(P):
        ws = G.words_from_alignment(p["text"], als[i])
        for seq, disp in spec.get("cap_merge", []):
            norm = lambda w: re.sub(r"[^\w]", "", w).lower()
            k = 0
            while k + len(seq) <= len(ws):
                if [norm(w[0]) for w in ws[k:k + len(seq)]] == seq:
                    ws[k:k + len(seq)] = [(disp, ws[k][1], ws[k + len(seq) - 1][2])]
                k += 1
        for j, (w, s0, e0) in enumerate(ws):
            a = starts[i] + s0
            b = starts[i] + (ws[j + 1][1] if j + 1 < len(ws) else e0 + 0.12)
            pth = f"{W}/cap{ci}.png"; G.cap_png(w, pth); ci += 1
            ov.append((pth, a, b, 1590))
    print("caption words", ci)
    cin = []
    for m in mp3s: cin += ["-i", m]
    for s, sl, d in segs: cin += ["-ss", f"{s:.3f}", "-t", f"{sl:.3f}", "-i", SRC]
    for o in ov: cin += ["-i", o[0]]
    nv = len(segs); fc = []
    for i in range(N): fc.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
    for j, (s, sl, d) in enumerate(segs):
        fc.append(f"[{N+j}:v]setpts=(PTS-STARTPTS)*{d/sl:.5f},fps=30,scale=1080:1920:flags=lanczos,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[t{j}]")
    fc.append("".join(f"[t{j}]" for j in range(nv)) + f"concat=n={nv}:v=1:a=0[bg]")
    lab = "bg"; base = N + nv
    for j, (pth, a, b, y) in enumerate(ov):
        en = f":enable='between(t,{a:.2f},{b:.2f})'" if a is not None else ""
        nxt = "v" if j == len(ov) - 1 else f"o{j}"
        fc.append(f"[{lab}][{base+j}:v]overlay=0:{y}{en}[{nxt}]"); lab = nxt
    fc.append("".join(f"[a{i}]" for i in range(N)) + f"amix=inputs={N}:normalize=0,apad[aout]")
    open(f"{W}/fc.txt", "w").write(";\n".join(fc))
    mp4 = f"{OUT}/guide_1119_{slug}.mp4"; t1 = time.time()
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + cin + ["-filter_complex_script", f"{W}/fc.txt", "-map", "[v]", "-map", "[aout]", "-t", f"{total:.2f}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], capture_output=True, text=True)
    if r.returncode: sys.exit("RENDER FAIL " + r.stderr[-800:])
    d_ = G.dur(mp4); print("RENDERED", mp4, round(d_, 1), "s in", round(time.time() - t1), "s")

    def sheet(times, outp, cols):
        rows = (len(times) + cols - 1) // cols; sh = Image.new("RGB", (cols * 270, rows * 480))
        for i, t in enumerate(times):
            fp = f"{W}/_c.jpg"
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=270:480", fp], check=True)
            sh.paste(Image.open(fp), ((i % cols) * 270, (i // cols) * 480)); ImageDraw.Draw(sh).text(((i % cols) * 270 + 4, (i // cols) * 480 + 2), f"{t:.1f}s", fill="yellow", font=ImageFont.truetype(G.FONT2, 22))
        sh.save(outp, quality=86)
    n = int(d_ // 3.2); sheet([0.4 + k * (d_ - 0.8) / (n - 1) for k in range(n)][:30], f"{OUT}/guide_1119_{slug}.contact.jpg", 6)
    sheet([0.3 + k for k in range(8)], f"{OUT}/guide_1119_{slug}.first7.jpg", 8)
    disp = spec["script_display"]
    open(f"{OUT}/guide_1119_{slug}.script.txt", "w").write(
        "RANKED TIPS\n" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(spec["tips"])) + f"\n\nFINAL SCRIPT ({len(disp.split())} words, Liam, {d_:.1f} s)\n" + disp +
        f"\n\nOverlays: title \"{spec['title']}\"; " + ", ".join('"%s"' % p["label"] for p in P if p.get("label")) + "; word-by-word white captions (lower blur zone); source burned-in captions removed\n\nSHOT LIST (source seconds)\n" +
        "\n".join(f"{p['key']}: {p['clips']}  # {p.get('proof','')}" for p in P) + "\n\nVERIFICATION\n" + spec["verify"] + "\n")
    desc = (spec["yt_title"] + "\n\n" + spec["hook"] + "\n\n" + "\n".join(spec["desc_steps"]) + f"\n\nWorks as of {spec['source_date']}; update if the game changes.\n\n" + spec["hashtags"] + "\n")
    open(f"{OUT}/guide_1119_{slug}.desc.txt", "w").write(desc)
    open(f"{OUT}/guide_1119_{slug}.title.txt", "w").write(spec["yt_title"] + "\n")
    json.dump({"slug": slug, "title": spec["yt_title"], "tags": spec["tags"], "tts_chars_new": chars, "tts_usd_est": round(chars * USD, 3), "duration": round(d_, 1)}, open(f"{OUT}/guide_1119_{slug}.COSTS.json", "w"))
    print("DONE", slug)


if __name__ == "__main__":
    main()
