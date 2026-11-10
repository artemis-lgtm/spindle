"""Fictional record labels, insert card, box print and sleeve colours (PIL).
All names are invented. No real labels, bands or logos."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tex")
os.makedirs(OUT, exist_ok=True)
S = 2048
C = S // 2
SUP = "/System/Library/Fonts/Supplemental/"
F = dict(
    futura=(SUP + "Futura.ttc", 0), futura_b=(SUP + "Futura.ttc", 2), futura_m=(SUP + "Futura.ttc", 1),
    didot=(SUP + "Didot.ttc", 0), gill=(SUP + "GillSans.ttc", 0), gill_b=(SUP + "GillSans.ttc", 1),
    bodoni=(SUP + "Bodoni 72.ttc", 0), avenir=("/System/Library/Fonts/Avenir Next.ttc", 0),
    avenir_b=("/System/Library/Fonts/Avenir Next.ttc", 2), din=(SUP + "DIN Condensed Bold.ttf", 0),
    brush=(SUP + "Brush Script.ttf", 0), copper=(SUP + "Copperplate.ttc", 0),
)
def font(k, size):
    p, i = F[k]
    try:
        return ImageFont.truetype(p, size, index=i)
    except Exception:
        return ImageFont.truetype(p, size)

def ctext(d, y, txt, f, fill, x=C):
    w = d.textlength(txt, font=f)
    d.text((x - w / 2, y), txt, font=f, fill=fill, anchor="ls")

def paper(img, amount=10, seed=1):
    random.seed(seed)
    px = img.load()
    noise = Image.effect_noise((S, S), 18).convert("L")
    tint = Image.new("RGB", (S, S), (0, 0, 0))
    out = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), amount / 255.0)
    return out

def ring(d, r, w, fill):
    d.ellipse((C - r, C - r, C + r, C + r), outline=fill, width=w)

def tracks(d, y0, items, f, fill, step=58):
    for i, t in enumerate(items):
        ctext(d, y0 + i * step, t, f, fill)

def label_halo():
    """Cream / brown ink: the look of the hero Austin liked."""
    bg, ink = (214, 196, 160), (74, 44, 28)
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)
    ring(d, 960, 10, ink); ring(d, 930, 3, ink); ring(d, 470, 4, ink)
    ctext(d, 420, "HALO PRESSINGS", font("futura_m", 132), ink)
    ctext(d, 520, "HIGH FIDELITY  .  STEREO", font("futura", 54), ink)
    ctext(d, 1420, "SIDE A", font("futura_b", 86), ink)
    tracks(d, 1520, ["1. SLOW BURN   4:12", "2. AMBER HOUR   3:48", "3. LOW LIGHT   5:01"], font("futura", 50), ink)
    ctext(d, 1760, "33 1/3 RPM", font("futura", 58), ink)
    d.text((300, C), "HP-0117", font=font("futura", 48), fill=ink, anchor="lm")
    d.text((S - 300, C), "1974", font=font("futura", 48), fill=ink, anchor="rm")
    return paper(im, 12, 1)

def label_meridian():
    """Teal over cream split: the 'new record' in the swap sequence."""
    im = Image.new("RGB", (S, S), (226, 216, 190))
    d = ImageDraw.Draw(im)
    teal, cream, dark = (22, 92, 98), (232, 222, 196), (16, 40, 44)
    d.pieslice((C - 1030, C - 1030, C + 1030, C + 1030), 180, 360, fill=teal)
    d.rectangle((0, C - 14, S, C + 14), fill=dark)
    ctext(d, 560, "MERIDIAN", font("didot", 190), cream)
    ctext(d, 660, "RECORDING  COMPANY", font("gill", 58), cream)
    ctext(d, 1300, "SIDE TWO", font("gill_b", 80), dark)
    tracks(d, 1400, ["CORAL STREET  3:30", "NORTHBOUND  4:05", "THE LONG WAY HOME  6:12"], font("gill", 52), dark)
    ctext(d, 1700, "MR 2207  .  33", font("gill", 56), dark)
    return paper(im, 12, 2)

def label_afterhours():
    """Black with gold: the bar record."""
    im = Image.new("RGB", (S, S), (18, 16, 15))
    d = ImageDraw.Draw(im)
    gold = (196, 156, 84)
    ring(d, 950, 6, gold); ring(d, 900, 2, gold)
    ctext(d, 520, "After Hours", font("brush", 230), gold)
    ctext(d, 610, "SOUND  ARCHIVE", font("copper", 60), gold)
    ctext(d, 1380, "STEREO", font("copper", 64), gold)
    tracks(d, 1480, ["Last Call (4:44)", "Smoke Rings (3:21)", "Neon & Rain (5:30)"], font("bodoni", 62), gold, 66)
    ctext(d, 1760, "AH-33-061", font("copper", 48), gold)
    return paper(im, 8, 3)

def label_sunroom():
    """Mustard: the living room record."""
    im = Image.new("RGB", (S, S), (214, 160, 52))
    d = ImageDraw.Draw(im)
    ink = (40, 28, 18)
    for k in range(5):
        ring(d, 980 - k * 34, 14, (196, 128, 38) if k % 2 else (226, 178, 70))
    ctext(d, 520, "sunroom", font("avenir_b", 200), ink)
    ctext(d, 610, "records  .  stereo", font("avenir", 60), ink)
    ctext(d, 1390, "A", font("avenir_b", 120), ink)
    tracks(d, 1490, ["Golden Tape  3:58", "Porch Light  4:20", "Paper Moon Hours  5:12"], font("avenir", 54), ink)
    ctext(d, 1760, "SR-505", font("avenir", 54), ink)
    return paper(im, 12, 4)

def label_ember45():
    """Red over black split: a 7" single (house label, invented)."""
    im = Image.new("RGB", (S, S), (16, 14, 14))
    d = ImageDraw.Draw(im)
    red, cream = (196, 52, 30), (236, 222, 200)
    d.pieslice((C - 1030, C - 1030, C + 1030, C + 1030), 180, 360, fill=red)
    ctext(d, 520, "EMBER", font("din", 300), cream)
    ctext(d, 610, "45 R.P.M.", font("din", 80), (24, 20, 18))
    ctext(d, 1520, "NIGHT DRIVE", font("din", 110), cream)
    ctext(d, 1640, "(Instrumental)  2:58", font("futura", 60), cream)
    ctext(d, 1760, "E-4521", font("futura", 54), red)
    return paper(im, 10, 5)

def label_nightshift45():
    """Cream with a checker strip: the other 7"."""
    im = Image.new("RGB", (S, S), (232, 222, 202))
    d = ImageDraw.Draw(im)
    ink, red = (30, 26, 24), (160, 40, 40)
    ctext(d, 560, "Lantern", font("brush", 330), red)
    y0, h, sq = 640, 70, 70
    for i, x in enumerate(range(0, S, sq)):
        d.rectangle((x, y0, x + sq, y0 + h // 2), fill=ink if i % 2 else (232, 222, 202))
        d.rectangle((x, y0 + h // 2, x + sq, y0 + h), fill=(232, 222, 202) if i % 2 else ink)
    ctext(d, 1420, "45 R.P.M.", font("futura", 60), ink)
    ctext(d, 1540, "MIDNIGHT TRAIN", font("futura_b", 90), ink)
    ctext(d, 1640, "2:41", font("futura", 60), ink)
    return paper(im, 10, 6)

def label_plain(bg, ink, seed):
    """Promo blank: one line of small print."""
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)
    ring(d, 940, 4, ink)
    ctext(d, 520, "PROMOTIONAL COPY", font("futura", 70), ink)
    ctext(d, 1560, "NOT FOR SALE", font("futura", 60), ink)
    ctext(d, 1660, "33 1/3", font("futura", 60), ink)
    return paper(im, 10, seed)

def insert_card():
    W, H = 1500, 2100
    im = Image.new("RGB", (W, H), (236, 230, 218))
    d = ImageDraw.Draw(im)
    ink = (34, 30, 28)
    d.text((110, 170), "Hang it. Plug it. Play it.", font=font("futura_m", 92), fill=ink)
    d.line((110, 310, W - 110, 310), fill=ink, width=4)
    steps = [("1", "Screw the steel plate to the wall.", "Level it in the slots."),
             ("2", "Twist the light on. Click.", "Set screw at 6 o'clock."),
             ("3", "Set your record on the felt.", "Finger-tight dome. Done."),
             ("4", "Change the record any time.", "The light stays on the wall.")]
    for i, (n, a, b) in enumerate(steps):
        y = 420 + i * 390
        d.ellipse((110, y, 290, y + 180), outline=ink, width=5)
        d.text((200, y + 92), n, font=font("futura_m", 110), fill=ink, anchor="mm")
        d.text((350, y + 70), a, font=font("futura_m", 64), fill=ink)
        d.text((350, y + 150), b, font=font("futura", 54), fill=(90, 84, 78))
    d.text((110, H - 150), "12 V Class 2  .  2700K  .  adapter stays at the outlet", font=font("futura", 46), fill=(90, 84, 78))
    return paper(im.resize((W, H)), 6, 9) if False else im

def box_print():
    """Kraft lid: a single printed halo mark, no brand."""
    W = 2048
    im = Image.new("RGB", (W, W), (178, 138, 96))
    noise = Image.effect_noise((W, W), 30).convert("L").filter(ImageFilter.GaussianBlur(1.2))
    im = Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.08)
    d = ImageDraw.Draw(im)
    ink = (40, 30, 24)
    c = W // 2
    for r, w in ((300, 10), (250, 3)):
        d.ellipse((c - r, c - r - 80, c + r, c + r - 80), outline=ink, width=w)
    d.ellipse((c - 150, c - 230, c + 150, c + 70), fill=ink)
    d.ellipse((c - 40, c - 120, c + 40, c - 40), fill=(178, 138, 96))
    ctext(d, c + 420, "SCONCE KIT  No. 001", font("futura_m", 90), ink, x=c)
    ctext(d, c + 520, "THIS SIDE UP  .  HANDLE LIKE VINYL", font("futura", 50), ink, x=c)
    return im

if __name__ == "__main__":
    jobs = dict(label_halo=label_halo, label_meridian=label_meridian, label_afterhours=label_afterhours,
                label_sunroom=label_sunroom, label_ember45=label_ember45, label_lantern45=label_nightshift45,
                insert_card=insert_card, box_print=box_print)
    for k, fn in jobs.items():
        fn().save(os.path.join(OUT, k + ".png"))
    label_plain((200, 60, 50), (240, 230, 220), 11).save(os.path.join(OUT, "label_promo_red.png"))
    label_plain((228, 226, 220), (30, 30, 30), 12).save(os.path.join(OUT, "label_promo_white.png"))
    label_plain((40, 70, 120), (230, 230, 235), 13).save(os.path.join(OUT, "label_promo_blue.png"))
    print("ok", sorted(os.listdir(OUT)))
