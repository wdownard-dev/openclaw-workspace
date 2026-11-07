"""Draw 'BOLT', an original flat-style robot mascot with a gaming headset.
Outputs transparent PNGs: mascot_{closed,half,open}[_blink].png in ./frames/
Usage: python mascot.py [outdir]
"""
import sys, os
from PIL import Image, ImageDraw

S = 4            # supersample factor
W = H = 600      # final size
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)

NAVY = (28, 32, 66, 255)
BODY = (255, 196, 40, 255)      # yellow
BODY_D = (235, 160, 20, 255)
FACE = (36, 44, 92, 255)
CYAN = (60, 230, 255, 255)
PINK = (255, 80, 150, 255)
WHITE = (255, 255, 255, 255)
MOUTH = (14, 16, 38, 255)
TONGUE = (255, 90, 120, 255)


def rr(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle([c * S for c in box], r * S, fill=fill, outline=outline, width=width * S)


def ell(d, box, fill, outline=None, width=0):
    d.ellipse([c * S for c in box], fill=fill, outline=outline, width=width * S)


def draw(mouth="closed", blink=False):
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # shadow-less flat style. Antenna
    rr(d, (292, 20, 308, 90), 6, NAVY)
    ell(d, (270, 0, 330, 60), PINK, NAVY, 6)
    ell(d, (284, 12, 298, 26), WHITE)
    # ear cups (behind head)
    rr(d, (28, 230, 88, 360), 24, PINK, NAVY, 7)
    rr(d, (512, 230, 572, 360), 24, PINK, NAVY, 7)
    # headband
    d.arc([p * S for p in (58, 60, 542, 420)], 190, 350, fill=NAVY, width=26 * S)
    d.arc([p * S for p in (58, 60, 542, 420)], 192, 348, fill=PINK, width=14 * S)
    # head
    rr(d, (80, 120, 520, 430), 90, BODY, NAVY, 9)
    rr(d, (96, 380, 504, 420), 22, BODY_D)  # lower shade
    rr(d, (80, 120, 520, 430), 90, None, NAVY, 9)
    # face screen
    rr(d, (125, 170, 475, 385), 60, FACE, NAVY, 7)
    # cheeks
    ell(d, (140, 300, 190, 335), (255, 90, 150, 140))
    ell(d, (410, 300, 460, 335), (255, 90, 150, 140))
    # eyes
    for cx in (225, 375):
        if blink:
            d.arc([(cx - 38) * S, 225 * S, (cx + 38) * S, 275 * S], 200, 340, fill=CYAN, width=11 * S)
        else:
            ell(d, (cx - 38, 205, cx + 38, 285), CYAN)
            ell(d, (cx - 20, 222, cx + 20, 266), NAVY)
            ell(d, (cx - 14, 228, cx - 2, 242), WHITE)
    # mouth
    if mouth == "closed":
        d.arc([265 * S, 300 * S, 335 * S, 345 * S], 20, 160, fill=CYAN, width=9 * S)
    elif mouth == "half":
        rr(d, (258, 306, 342, 346), 20, MOUTH, CYAN, 6)
        rr(d, (278, 330, 322, 344), 8, TONGUE)
    else:
        rr(d, (250, 300, 350, 372), 34, MOUTH, CYAN, 7)
        ell(d, (268, 336, 332, 392), TONGUE)
        rr(d, (262, 304, 338, 322), 6, WHITE)  # teeth
        rr(d, (250, 300, 350, 372), 34, None, CYAN, 7)
    # mic boom from left ear cup
    d.line([(58 * S, 345 * S), (70 * S, 410 * S), (170 * S, 440 * S), (235 * S, 428 * S)], fill=NAVY, width=11 * S, joint="curve")
    ell(d, (222, 414, 262, 446), NAVY)
    ell(d, (230, 420, 254, 440), CYAN)
    # neck + shoulders
    rr(d, (255, 428, 345, 470), 8, NAVY)
    rr(d, (150, 462, 450, 595), 60, BODY, NAVY, 9)
    rr(d, (150, 540, 450, 595), 40, BODY_D)
    rr(d, (150, 462, 450, 595), 60, None, NAVY, 9)
    # chest badge
    ell(d, (270, 490, 330, 550), FACE, NAVY, 6)
    ell(d, (286, 506, 314, 534), CYAN)
    return im.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    for m in ("closed", "half", "open"):
        for b in (False, True):
            draw(m, b).save(os.path.join(OUT, f"mascot_{m}{'_blink' if b else ''}.png"))
    print("wrote", OUT)
