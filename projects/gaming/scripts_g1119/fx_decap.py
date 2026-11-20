#!/usr/bin/env python3
"""fx_decap.py IN OUT [t0 t1]: erase the burned-in centre caption (band y 590-700) by inpainting text-shaped mask. Video only (audio dropped)."""
import sys, subprocess, numpy as np, cv2
FF = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
src, dst = sys.argv[1], sys.argv[2]
t0 = sys.argv[3] if len(sys.argv) > 3 else "0"; t1 = sys.argv[4] if len(sys.argv) > 4 else "61"
W, H = 720, 1280; Y0, Y1 = 585, 705
rd = subprocess.Popen([FF, "-loglevel", "error", "-ss", t0, "-t", str(float(t1) - float(t0)), "-i", src, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
k3 = np.ones((3, 3), np.uint8)
n = 0
while True:
    buf = rd.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    band = fr[Y0:Y1]
    mn = band.min(axis=2); mx = band.max(axis=2)
    white = (mn >= 232).astype(np.uint8)
    dark = (mx <= 40).astype(np.uint8)
    near_dark = cv2.dilate(dark, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    big = cv2.morphologyEx(white, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    big = cv2.dilate(big, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    core = white & near_dark & (1 - big)
    # text pixels cluster: drop sparse noise
    if core.sum() > 120:
        mask = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
        mask[:, :40] = 0; mask[:, W - 40:] = 0
        band2 = cv2.inpaint(band, mask * 255, 4, cv2.INPAINT_TELEA)
        fr[Y0:Y1] = band2
    wr.stdin.write(fr.tobytes()); n += 1
wr.stdin.close(); wr.wait(); print("frames", n)
