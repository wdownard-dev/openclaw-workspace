#!/usr/bin/env python3
"""Cut one moment from a long VOD into a 9:16 draft + contact sheet. Posts/uploads/submits nothing, no credits.

  cut_moment.py VIDEO_ID_OR_URL --start S --end E [--out DIR] [--name N]

Downloads only that section (yt-dlp --download-sections, keyframe-accurate cuts, <=1080p), renders 1080x1920 (blurred
copy as background, 16:9 gameplay fitted in a band, source audio untouched, h264/aac, +faststart), max 60 s, and writes
a contact sheet (10 labelled frames) for screening. Prints the output paths.
"""
import argparse, glob, os, re, select, socket, subprocess, sys, threading

YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
HERE = os.path.dirname(os.path.abspath(__file__))


def start_proxy():
    """Tiny local CONNECT proxy. The static ffmpeg build segfaults on DNS lookups (getaddrinfo), so yt-dlp is pointed at
    this proxy and Python does the name resolution; ffmpeg only ever sees 127.0.0.1."""
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(64)

    def pipe(a, b):
        try:
            while True:
                r, _, _ = select.select([a, b], [], [], 120)
                if not r:
                    break
                for x in r:
                    d = x.recv(65536)
                    if not d:
                        return
                    (b if x is a else a).sendall(d)
        except OSError:
            pass
        finally:
            a.close()
            b.close()

    def handle(c):
        try:
            buf = b""
            while b"\r\n\r\n" not in buf:
                d = c.recv(4096)
                if not d:
                    return c.close()
                buf += d
            first = buf.split(b"\r\n")[0].decode()
            if not first.startswith("CONNECT "):
                c.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
                return c.close()
            host, port = first.split()[1].rsplit(":", 1)
            up = socket.create_connection((host, int(port)), timeout=30)
            c.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")
            pipe(c, up)
        except Exception:
            c.close()

    def loop():
        while True:
            c, _ = srv.accept()
            threading.Thread(target=handle, args=(c,), daemon=True).start()
    threading.Thread(target=loop, daemon=True).start()
    return srv.getsockname()[1]


def video_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def fmt(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def probe(path):
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    dur = int(d[1]) * 3600 + int(d[2]) * 60 + float(d[3]) if d else 0
    v = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", r)
    return dur, (int(v[1]), int(v[2])) if v else None, "Audio:" in r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--start", type=float, required=True)
    ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--name")
    a = ap.parse_args()
    if a.end <= a.start:
        sys.exit("end must be after start")
    if a.end - a.start > 60:
        sys.exit(f"max 60 s per cut (asked {a.end - a.start:.0f} s)")
    vid = video_id(a.video)
    name = a.name or f"{vid}_{int(a.start)}-{int(a.end)}"
    os.makedirs(a.out, exist_ok=True)
    raw_tpl = os.path.join(a.out, f"{name}.raw.%(ext)s")
    for old in glob.glob(os.path.join(a.out, f"{name}.raw.*")):
        os.remove(old)
    port = start_proxy()
    r = subprocess.run([YTDLP, "--no-warnings", "--proxy", f"http://127.0.0.1:{port}", "--ignore-no-formats-error", "--download-sections", f"*{a.start}-{a.end}",
                        "--force-keyframes-at-cuts", "--ffmpeg-location", FFMPEG, "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
                        "--merge-output-format", "mp4", "-o", raw_tpl, f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True, timeout=900)
    raws = glob.glob(os.path.join(a.out, f"{name}.raw.*"))
    if not raws:
        sys.exit("download failed: " + (r.stderr or r.stdout)[-400:])
    raw = raws[0]
    if not probe(raw)[1]:
        # Section download returned audio only (403 on the https DASH video track). Fall back to a video-only <=720p download of the
        # whole video (size-capped), cut the window locally, and mux the section audio back in.
        full_tpl = os.path.join(a.out, f"{name}.full.%(ext)s")
        for old in glob.glob(os.path.join(a.out, f"{name}.full.*")):
            os.remove(old)
        subprocess.run([YTDLP, "--no-warnings", "--proxy", f"http://127.0.0.1:{port}", "--ignore-no-formats-error", "--max-filesize", "900M",
                        "-f", "bv*[height<=720][ext=mp4]/bv*[height<=720]", "-o", full_tpl, f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True, timeout=1800)
        fulls = glob.glob(os.path.join(a.out, f"{name}.full.*"))
        if not fulls:
            sys.exit("no video track available (section 403, full download failed/too large)")
        cutv = os.path.join(a.out, f"{name}.rawv.mp4")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", str(a.start), "-i", fulls[0], "-i", raw, "-t", str(a.end - a.start), "-map", "0:v:0",
                        "-map", "1:a:0?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", cutv], check=True)
        os.remove(fulls[0])
        os.remove(raw)
        raw = cutv
    mp4 = os.path.join(a.out, f"{name}.mp4")
    # Same fit/blur layout as the-lowdown render_cut.py --blur: blurred cover background, source fitted full width.
    fc = ("[0:v]fps=30,split=2[x][y];[x]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];"
          "[y]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", raw, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
                    "-t", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], check=True)
    dur, res, has_audio = probe(mp4)
    # Contact sheet from the rendered clip: 10 evenly spaced frames, labelled with source timestamps.
    from PIL import Image, ImageDraw, ImageFont
    n = 10
    tmp = os.path.join(a.out, f"{name}.frames")
    os.makedirs(tmp, exist_ok=True)
    frames = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        fp = os.path.join(tmp, f"f{i:02d}.jpg")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1",
                        "-vf", "scale=270:480", fp], check=True)
        frames.append((t, fp))
    cols, rows = 5, 2
    sheet = Image.new("RGB", (cols * 270, rows * 480), "black")
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for i, (t, fp) in enumerate(frames):
        im = Image.open(fp)
        x, y = (i % cols) * 270, (i // cols) * 480
        sheet.paste(im, (x, y))
        d = ImageDraw.Draw(sheet)
        label = f"{fmt(a.start + t)} (+{t:.0f}s)"
        d.rectangle([x, y, x + 150, y + 28], fill="black")
        d.text((x + 4, y + 2), label, fill="yellow", font=font)
        os.remove(fp)
    os.rmdir(tmp)
    sheet_path = os.path.join(a.out, f"{name}.contact.jpg")
    sheet.save(sheet_path, quality=88)
    os.remove(raw)
    print(f"MP4 {mp4}\nSHEET {sheet_path}\n{dur:.1f}s {res[0]}x{res[1]} audio={has_audio}")


if __name__ == "__main__":
    main()
