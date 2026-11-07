import sys, subprocess
from PIL import Image
mp4, out = sys.argv[1], sys.argv[2]; times = [float(x) for x in sys.argv[3:]]
FF = "/home/williamdownard/openclaw-sites/bin/ffmpeg"; ims = []
for t in times:
    p = f"/tmp/_f{t}.png"; subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", mp4, "-frames:v", "1", "-vf", "scale=400:-1", p]); ims.append(Image.open(p))
sh = Image.new("RGB", (400 * len(ims), ims[0].height))
for i, im in enumerate(ims): sh.paste(im, (i * 400, 0))
sh.save(out)
