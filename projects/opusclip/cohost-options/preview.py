"""Preview strip: python preview.py slug [out.png] -> 4 mouths + blink on dark bg."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "chars"))
from PIL import Image
from lib import MOUTHS
m = importlib.import_module(sys.argv[1])
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "_prev", sys.argv[1] + ".png")
tiles = [m.draw(mo, False) for mo in MOUTHS] + [m.draw("small", True)]
bg = Image.new("RGBA", (600 * 5 // 2, 600), m.BG[0] + (255,))
sheet = Image.new("RGBA", (300 * 5, 300), m.BG[0] + (255,))
for i, t in enumerate(tiles):
    sheet.alpha_composite(t.resize((300, 300), Image.LANCZOS), (i * 300, 0))
sheet.convert("RGB").save(out)
# also a full-res 'wide' frame
bgf = Image.new("RGBA", (600, 600), m.BG[0] + (255,)); bgf.alpha_composite(tiles[2]); bgf.convert("RGB").save(out.replace(".png", "_full.png"))
print(out)
