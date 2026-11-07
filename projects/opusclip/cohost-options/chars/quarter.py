"""QUARTER - retro arcade-cabinet character, true pixel art (40x40 grid, nearest-neighbour upscale)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *
from PIL import Image, ImageDraw

SLUG, NAME, TAGLINE = "quarter", "QUARTER", "Insert coin. Receive opinions."
VOICE, SPEED = "am_fenrir", 1.05
LINE = "Player one, ready! I'm Quarter. Insert a coin and I'll rate your run. Warning: harsh scores ahead."
ACCENT = (255, 214, 64)
BG = ((18, 8, 40), (44, 12, 70))

K = hexc("#150a2e")        # outline
P1 = hexc("#7b3fe4"); P2 = hexc("#5a2bb8"); P3 = hexc("#3b1d82"); PL = hexc("#a77bff")
SCR0 = hexc("#06141a"); SCR1 = hexc("#0b2a30")
GRN = hexc("#5dff9e"); GRN2 = hexc("#2fbf6c"); YEL = hexc("#ffd23f"); YEL2 = hexc("#e29b12"); RED = hexc("#ff3d57"); PNK = hexc("#ff7ad9"); CYN = hexc("#4de3ff")
WHT = hexc("#fff4d6"); GRY = hexc("#9aa0b8"); GRY2 = hexc("#5d6382")
G = 40


def draw(mouth="closed", blink=False):
    im = Image.new("RGBA", (G, G), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def R(x0, y0, x1, y1, c):  # inclusive rect
        d.rectangle([x0, y0, x1, y1], fill=c)

    def P(x, y, c):
        d.point((x, y), fill=c)

    # feet
    R(10, 37, 16, 38, K); R(11, 36, 15, 37, P3)
    R(23, 37, 29, 38, K); R(24, 36, 28, 37, P3)
    # arms (stubby, waving up on wide)
    R(1, 24, 4, 31, K); R(2, 25, 3, 30, P2); R(2, 25, 2, 30, P1)
    R(1, 29, 4, 33, K); R(2, 30, 3, 32, WHT)       # glove
    if mouth == "wide":   # right arm raised, waving
        R(35, 14, 38, 29, K); R(36, 15, 37, 28, P2); R(36, 15, 36, 28, P1)
        R(34, 9, 38, 15, K); R(35, 10, 37, 14, WHT)
    else:
        R(35, 24, 38, 31, K); R(36, 25, 37, 30, P2); R(36, 25, 36, 30, P1)
        R(35, 29, 38, 33, K); R(36, 30, 37, 32, WHT)
    # cabinet body
    R(5, 2, 34, 36, K)
    R(6, 3, 33, 35, P2)
    R(6, 3, 8, 35, P1)           # lit left edge
    R(31, 3, 33, 35, P3)         # shaded right edge
    for y in range(4, 35, 4):    # side stripe dither
        P(7, y, PL)
    # marquee
    R(7, 3, 32, 8, K); R(8, 4, 31, 7, YEL)
    R(8, 7, 31, 7, YEL2)
    # marquee bulbs
    for x in range(9, 31, 3):
        P(x, 4, WHT)
    # tiny 'QTR' letters (3x5 font)
    glyph = {"Q": ["111", "101", "101", "111", "001"], "T": ["111", "010", "010", "010", "010"], "R": ["110", "101", "110", "101", "101"]}
    # (marquee is only 4px tall: draw stars instead)
    for x in (12, 17, 22, 27):
        P(x, 5, RED); P(x, 6, RED)
    # screen bezel
    R(8, 10, 31, 26, K); R(9, 11, 30, 25, GRY2); R(10, 12, 29, 24, K)
    R(11, 13, 28, 23, SCR0)
    for y in range(13, 24):
        if y % 2 == 0:
            R(11, y, 28, y, SCR1)    # scanlines
    # glare
    R(12, 14, 14, 14, hexc("#1d4a4e")); R(12, 15, 12, 15, hexc("#1d4a4e"))
    # eyes
    for ex in (15, 24):
        if blink:
            R(ex - 1, 17, ex + 2, 17, GRN)
        else:
            tall = {"closed": 3, "small": 3, "open": 4, "wide": 5}[mouth]
            R(ex - 1, 16 - (tall - 3) // 2 * 1, ex + 2, 16 - (tall - 3) // 2 + tall, GRN)
            R(ex, 16 - (tall - 3) // 2 + tall - 1, ex + 1, 16 - (tall - 3) // 2 + tall, GRN2)
            P(ex - 1, 16 - (tall - 3) // 2, WHT)
    # brows (raise when loud)
    by = {"closed": 14, "small": 14, "open": 13, "wide": 12}[mouth]
    if not blink:
        R(13, by, 16, by, YEL); R(23, by, 26, by, YEL)
        if mouth == "closed":
            P(16, by + 1, YEL); P(23, by + 1, YEL)   # slight frown-brow
    # cheeks
    P(12, 20, PNK); P(13, 20, PNK); P(26, 20, PNK); P(27, 20, PNK)
    # mouth
    if mouth == "closed":
        R(18, 21, 21, 21, GRN); P(17, 20, GRN); P(22, 20, GRN)
    elif mouth == "small":
        R(18, 20, 21, 21, GRN); R(19, 21, 20, 21, SCR0)
    elif mouth == "open":
        R(17, 19, 22, 22, GRN); R(18, 20, 21, 22, SCR0); R(19, 22, 20, 22, RED)
    else:
        R(16, 19, 23, 23, GRN); R(17, 20, 22, 23, SCR0); R(18, 22, 21, 23, RED); R(17, 20, 22, 20, WHT)
    # control panel
    R(6, 27, 33, 31, K); R(7, 28, 32, 30, P3); R(7, 28, 32, 28, PL)
    # joystick
    R(11, 27, 14, 30, K); R(12, 27, 13, 29, RED); P(12, 27, WHT); R(12, 29, 13, 29, hexc("#b01f36"))
    # buttons
    for bx, c in ((19, YEL), (22, CYN), (25, PNK), (28, GRN)):
        R(bx, 28, bx + 1, 29, K); R(bx, 28, bx + 1, 28, c)
        P(bx, 29, c)
    # lower cabinet / coin door
    R(9, 32, 30, 35, K)
    R(10, 33, 29, 34, P3)
    R(13, 32, 14, 35, K); R(14, 32, 15, 35, YEL); P(15, 33, YEL2); R(14, 33, 14, 34, YEL2)
    R(24, 32, 25, 35, K); R(25, 32, 26, 35, YEL); R(25, 33, 25, 34, YEL2)
    R(18, 33, 21, 34, K); R(19, 33, 20, 34, GRN2)
    # sparkles of 'coin' next to mouth when wide
    out = im.resize((600, 600), Image.NEAREST)
    return out
