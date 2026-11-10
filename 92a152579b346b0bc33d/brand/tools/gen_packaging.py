"""Packaging artwork: 13x13x3 mailer dieline (outside + inside), insert tray,
insert card, warranty card, sticker. All text outlined. Units: points (72/in).

Run: python3 brand/tools/gen_packaging.py
Switch the brand by editing BRAND_KEY (sidea | deadwax | spindle).
"""
import os
import sys

import svgtext as T
import qrcode
import qrcode.image.svg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_brand import P, NAMES, RECOMMENDED, monogram  # noqa: E402

BRAND_KEY = RECOMMENDED
N = NAMES[BRAND_KEY]
BRAND = N["brand"]
WORD = N["word"]
PRODUCT = "Spindle" if BRAND_KEY != "spindle" else "Spindle"
INSTALL_URL = "https://spindlelighting.com/install"  # placeholder: domain checked free 2026-11-09, NOT registered

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "packaging")
os.makedirs(OUT, exist_ok=True)
IN = 72.0  # points per inch
BLEED = 0.125 * IN
SAFE = 0.25 * IN

CUT = f'fill="none" stroke="#E6007E" stroke-width="0.75"'          # magenta = cut (vendor convention)
CREASE = f'fill="none" stroke="#00A3E0" stroke-width="0.75" stroke-dasharray="6 4"'  # cyan dashed = crease
BLEEDL = f'fill="none" stroke="#E6007E" stroke-width="0.4" stroke-dasharray="2 3" opacity="0.6"'
SAFEL = f'fill="none" stroke="#3AAA35" stroke-width="0.4" stroke-dasharray="2 3" opacity="0.8"'


def svg(w, h, body, bg=None):
    bgrect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w/IN:.3f}in" height="{h/IN:.3f}in" viewBox="0 0 {w:.2f} {h:.2f}">\n{bgrect}\n{body}\n</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


def rect(x, y, w, h, style):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {style}/>'


def line(x1, y1, x2, y2, style):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {style}/>'


def mono(txt, size, x, y, fill, anchor="start", tracking=0.2):
    return T.text_path(txt, "mono-medium", size, x, y, tracking=tracking, anchor=anchor, fill=fill)


def sans(txt, size, x, y, fill, anchor="start", key="sans", tracking=0.0):
    return T.text_path(txt, key, size, x, y, tracking=tracking, anchor=anchor, fill=fill)


def serif(txt, size, x, y, fill, anchor="start"):
    return T.text_path(txt, "serif-italic", size, x, y, anchor=anchor, fill=fill)


# ------------------------------------------------------------------ dieline
# Roll-end tuck-top (RETT) mailer, interior 13 x 13 x 3 in. Flat layout, panels:
#   column centre (W = 13): tuck flap | lid (13) | back wall (3) | bottom (13) | front wall (3)
#   bottom panel wings: side wall (3) + roll-over inner wall (3) each side
#   lid wings: dust flaps (3 deep) each side; front wall wings: lock tabs.
# This is a working dieline for artwork placement. Packlane / Arka supply the exact
# production dieline PDF for their board and cutter; artwork is layered per panel so it
# re-flows onto theirs (see spec-sheet.md).
L = 13 * IN
W = 13 * IN
D = 3 * IN
TUCK = 1.5 * IN
MARGIN = 0.75 * IN
FLAT_W = W + 4 * D + 2 * MARGIN
FLAT_H = TUCK + L + D + L + D + 2 * MARGIN
X0 = MARGIN + 2 * D          # left edge of centre column
Y0 = MARGIN                  # top of tuck flap

PANELS = {
    "tuck": (X0, Y0, W, TUCK),
    "lid": (X0, Y0 + TUCK, W, L),
    "back": (X0, Y0 + TUCK + L, W, D),
    "bottom": (X0, Y0 + TUCK + L + D, W, L),
    "front": (X0, Y0 + TUCK + L + D + L, W, D),
    "side_l": (X0 - D, Y0 + TUCK + L + D, D, L),
    "side_r": (X0 + W, Y0 + TUCK + L + D, D, L),
    "roll_l": (X0 - 2 * D, Y0 + TUCK + L + D, D, L),
    "roll_r": (X0 + W + D, Y0 + TUCK + L + D, D, L),
    "dust_l": (X0 - D, Y0 + TUCK, D, L),
    "dust_r": (X0 + W, Y0 + TUCK, D, L),
}


def dieline_lines():
    out = []
    px, py, pw, ph = PANELS["tuck"]
    # outer cut outline (simplified polygon, per panel edges)
    cuts = []
    # tuck flap with angled corners
    cuts.append(line(px + 0.35 * IN, py, px + pw - 0.35 * IN, py, CUT))
    cuts.append(line(px, py + TUCK, px + 0.35 * IN, py, CUT))
    cuts.append(line(px + pw - 0.35 * IN, py, px + pw, py + TUCK, CUT))
    # dust flaps outer edges
    for key in ("dust_l", "dust_r"):
        x, y, w, h = PANELS[key]
        inset = 0.1 * IN
        if key == "dust_l":
            cuts += [line(x, y + inset, x, y + h - inset, CUT), line(x, y + inset, x + w, y, CUT), line(x, y + h - inset, x + w, y + h, CUT)]
        else:
            cuts += [line(x + w, y + inset, x + w, y + h - inset, CUT), line(x + w, y + inset, x, y, CUT), line(x + w, y + h - inset, x, y + h, CUT)]
    # back wall ends (between dust flaps and side walls)
    x, y, w, h = PANELS["back"]
    cuts += [line(x, y, x, y + h, CUT), line(x + w, y, x + w, y + h, CUT)]
    # roll-over walls outer edges with tuck tabs
    for key in ("roll_l", "roll_r"):
        x, y, w, h = PANELS[key]
        if key == "roll_l":
            cuts += [line(x, y, x, y + h, CUT), line(x, y, x + w, y, CUT), line(x, y + h, x + w, y + h, CUT)]
        else:
            cuts += [line(x + w, y, x + w, y + h, CUT), line(x, y, x + w, y, CUT), line(x, y + h, x + w, y + h, CUT)]
    # front wall with lock tabs
    x, y, w, h = PANELS["front"]
    tab = 0.6 * IN
    cuts += [line(x - tab, y + 0.15 * IN, x - tab, y + h, CUT), line(x - tab, y + 0.15 * IN, x, y, CUT), line(x - tab, y + h, x + w + tab, y + h, CUT),
             line(x + w + tab, y + 0.15 * IN, x + w + tab, y + h, CUT), line(x + w + tab, y + 0.15 * IN, x + w, y, CUT)]
    # thumb notch on lid front edge (lid meets tuck)
    out += cuts
    # creases
    cr = []
    cr.append(line(X0, Y0 + TUCK, X0 + W, Y0 + TUCK, CREASE))
    cr.append(line(X0, Y0 + TUCK + L, X0 + W, Y0 + TUCK + L, CREASE))
    cr.append(line(X0, Y0 + TUCK + L + D, X0 + W, Y0 + TUCK + L + D, CREASE))
    cr.append(line(X0, Y0 + TUCK + L + D + L, X0 + W, Y0 + TUCK + L + D + L, CREASE))
    for key in ("side_l", "side_r", "dust_l", "dust_r"):
        x, y, w, h = PANELS[key]
        cx = x + w if key.endswith("_l") else x
        cr.append(line(cx, y, cx, y + h, CREASE))
    for key in ("roll_l", "roll_r"):
        x, y, w, h = PANELS[key]
        cx = x + w if key.endswith("_l") else x
        cr.append(line(cx, y, cx, y + h, CREASE))
    out += cr
    return "\n".join(out)


def panel_guides(labels=True):
    out = []
    for key, (x, y, w, h) in PANELS.items():
        out.append(rect(x + SAFE, y + SAFE, w - 2 * SAFE, h - 2 * SAFE, SAFEL))
        if labels:
            out.append(mono(key.upper().replace("_", " "), 6, x + w / 2, y + h / 2, "#999999", anchor="middle", tracking=0.15))
    out.append(rect(X0 - 2 * D - BLEED, Y0 - BLEED, W + 4 * D + 2 * BLEED, FLAT_H - 2 * MARGIN + 2 * BLEED, BLEEDL))
    return "\n".join(out)


def legend(x, y):
    items = [("CUT", CUT), ("CREASE", CREASE), ("BLEED 0.125 in", BLEEDL), ("SAFE 0.25 in", SAFEL)]
    out = []
    for i, (lab, st) in enumerate(items):
        yy = y + i * 14
        out.append(line(x, yy, x + 30, yy, st))
        out.append(mono(lab, 6.5, x + 38, yy + 2.3, "#555555", tracking=0.1))
    return "\n".join(out)


def title_block(title, sub, x, y):
    return "\n".join([
        sans(title, 11, x, y, "#333333", key="sans-semibold"),
        mono(sub, 6.5, x, y + 12, "#666666", tracking=0.08),
    ])


def mailer_outside():
    body = []
    # Kraft base is the board itself; we simulate it in preview with a kraft fill on the panels.
    for key, (x, y, w, h) in PANELS.items():
        body.append(rect(x, y, w, h, 'fill="#C9A36A" opacity="0.55"'))
    # LID: monogram large, centred, single-colour black + halo ring in Ember (print-safe on kraft)
    x, y, w, h = PANELS["lid"]
    cx, cy = x + w / 2, y + h / 2
    body.append(monogram(cx, cy - 0.3 * IN, 3.1 * IN, P["vinyl"], "#F4ECDD", halo=P["ember"], rings=True, dome_hole=False))
    body.append(T.text_path(WORD, "sans-semibold", 0.62 * IN, cx, y + h - 1.25 * IN, tracking=0.08, anchor="middle", fill=P["vinyl"]))
    body.append(mono("RECORD SCONCES  ·  MADE TO ORDER", 8.5, cx, y + h - 0.85 * IN, P["vinyl"], anchor="middle", tracking=0.22))
    # FRONT wall: wordmark small, left; finish code box right (applied as a sticker, see sticker.svg)
    x, y, w, h = PANELS["front"]
    body.append(T.text_path(WORD, "sans-semibold", 0.42 * IN, x + SAFE + 0.25 * IN, y + h / 2 + 0.15 * IN, tracking=0.08, fill=P["vinyl"]))
    body.append(mono("SPINDLE 12  ·  12 IN RECORD SCONCE", 8, x + w - SAFE - 0.25 * IN, y + h / 2 + 0.1 * IN, P["vinyl"], anchor="end", tracking=0.2))
    body.append(rect(x + w - SAFE - 2.6 * IN, y + h / 2 + 0.3 * IN, 2.35 * IN, 0.55 * IN, 'fill="none" stroke="#16130F" stroke-width="0.6" stroke-dasharray="3 3"'))
    body.append(mono("FINISH STICKER", 5.5, x + w - SAFE - 1.425 * IN, y + h / 2 + 0.63 * IN, "#16130F", anchor="middle", tracking=0.2))
    # BACK wall: the ritual line in serif italic
    x, y, w, h = PANELS["back"]
    body.append(serif("Change the record. Change the room.", 0.36 * IN, x + w / 2, y + h / 2 + 0.12 * IN, P["vinyl"], anchor="middle"))
    # SIDE walls: vertical mono spec lines
    for key, rot in (("side_l", -90), ("side_r", 90)):
        x, y, w, h = PANELS[key]
        cx, cy = x + w / 2, y + h / 2
        txt = "12 V CLASS 2  ·  2700 K  ·  NOTHING GLUED TO YOUR RECORD" if key == "side_l" else f"{WORD}  ·  DESIGNED IN FLORIDA  ·  ASSEMBLED IN USA"
        body.append(f'<g transform="rotate({rot} {cx:.2f} {cy:.2f})">' + mono(txt, 9, cx, cy + 3, P["vinyl"], anchor="middle", tracking=0.2) + "</g>")
    # BOTTOM: recycle + handling marks only
    x, y, w, h = PANELS["bottom"]
    body.append(mono("THIS SIDE DOWN  ·  FRAGILE  ·  RECYCLE THE BOX, KEEP THE RECORD", 8, x + w / 2, y + h - SAFE - 0.2 * IN, P["vinyl"], anchor="middle", tracking=0.18))
    body.append(monogram(x + w / 2, y + h / 2, 0.5 * IN, P["vinyl"], "#F4ECDD", halo=None, rings=False, dome_hole=False))
    body.append(dieline_lines())
    body.append(panel_guides(labels=False))
    body.append(title_block(f"{BRAND}  ·  Mailer 13 x 13 x 3 in  ·  OUTSIDE print", "Roll-end tuck-top mailer  ·  kraft B-flute  ·  inks: K + Ember (C32 M62 Y100 K20 approx.)  ·  all text outlined  ·  scale 1:1 at 72 pt/in", MARGIN, FLAT_H - 0.35 * IN))
    body.append(legend(FLAT_W - 2.4 * IN, FLAT_H - 1.0 * IN))
    write("mailer-13x13x3-outside.svg", svg(FLAT_W, FLAT_H, "\n".join(body), bg="#FFFFFF"))


def mailer_inside():
    body = []
    # inside print: the lid interior is the reveal. Full Soot flood with a Halo gradient disc,
    # so opening the box shows the glow before the product. Everything else stays kraft.
    body.append('<defs><radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#F0A43B" stop-opacity="1"/><stop offset="0.55" stop-color="#F0A43B" stop-opacity="0.85"/><stop offset="0.8" stop-color="#B9661C" stop-opacity="0.35"/><stop offset="1" stop-color="#2B2622" stop-opacity="0"/></radialGradient></defs>')
    for key, (x, y, w, h) in PANELS.items():
        body.append(rect(x, y, w, h, 'fill="#C9A36A" opacity="0.55"'))
    x, y, w, h = PANELS["lid"]
    body.append(rect(x - BLEED, y, w + 2 * BLEED, h, f'fill="{P["soot"]}"'))
    cx, cy = x + w / 2, y + h / 2
    body.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{5.6*IN:.2f}" fill="url(#halo)"/>')
    body.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{3.4*IN:.2f}" fill="{P["soot"]}"/>')
    body.append(serif("Side A, always.", 0.5 * IN, cx, cy - 0.1 * IN, P["label"], anchor="middle") if BRAND_KEY == "sidea" else serif("Put something on.", 0.5 * IN, cx, cy - 0.1 * IN, P["label"], anchor="middle"))
    body.append(mono("UNSCREW THE DOME  ·  SLIDE YOUR RECORD ON  ·  SCREW IT BACK  ·  LIGHTS ON", 8, cx, cy + 0.45 * IN, P["chrome"], anchor="middle", tracking=0.18))
    body.append(mono(f"{WORD}  ·  NO. ______  ·  FINISH ______", 7.5, cx, y + h - SAFE - 0.25 * IN, P["chrome"], anchor="middle", tracking=0.2))
    # bottom interior: tray sits here; print only a hairline frame and the tray key
    x, y, w, h = PANELS["bottom"]
    body.append(rect(x + SAFE, y + SAFE, w - 2 * SAFE, h - 2 * SAFE, 'fill="none" stroke="#16130F" stroke-width="0.6"'))
    body.append(mono("TRAY SEATS HERE  ·  DOME POCKET AT CENTRE  ·  CORD UNDER THE TRAY", 7.5, x + w / 2, y + h - SAFE - 0.2 * IN, P["vinyl"], anchor="middle", tracking=0.18))
    body.append(dieline_lines())
    body.append(panel_guides(labels=False))
    body.append(title_block(f"{BRAND}  ·  Mailer 13 x 13 x 3 in  ·  INSIDE print", "Lid interior: Soot flood + Halo radial (CMYK)  ·  bottom interior: K hairline only  ·  side walls unprinted  ·  mirrored layout: vendor flips automatically", MARGIN, FLAT_H - 0.35 * IN))
    body.append(legend(FLAT_W - 2.4 * IN, FLAT_H - 1.0 * IN))
    write("mailer-13x13x3-inside.svg", svg(FLAT_W, FLAT_H, "\n".join(body), bg="#FFFFFF"))


# ------------------------------------------------------------------ insert tray
def tray():
    """Two-layer die-cut tray, 12.75 x 12.75 in footprint, 2.75 in total depth.
    Top layer (1.25 in, black EPE foam or moulded pulp): dome pocket dead centre where the
    spindle hole would be, cord coil pocket, hardware pocket, card slot.
    Lower layer (1.5 in): 10.75 in round pocket for the hub + backplate, record sleeve
    flat beneath (sleeve 12.4 in square sits under the lower layer on the box floor)."""
    S = 12.75 * IN
    pad = 0.6 * IN
    Wt = S * 2 + pad * 3
    Ht = S + pad * 2 + 4.6 * IN
    body = []
    # plan: top layer
    x0, y0 = pad, pad
    body.append(rect(x0, y0, S, S, f'fill="#2B2622"'))
    cx, cy = x0 + S / 2, y0 + S / 2
    body.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{5.375*IN:.2f}" fill="none" stroke="#5F6468" stroke-width="0.6" stroke-dasharray="4 3"/>')
    body.append(mono("HUB + BACKPLATE OUTLINE (LAYER 2)", 6, cx, cy - 4.9 * IN, "#8A8F94", anchor="middle", tracking=0.15))
    body.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{1.0*IN:.2f}" fill="#16130F" stroke="#C7CBD0" stroke-width="0.8"/>')
    body.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{0.72*IN:.2f}" fill="#C7CBD0"/>')
    body.append(f'<circle cx="{cx - 0.22*IN:.2f}" cy="{cy - 0.22*IN:.2f}" r="{0.2*IN:.2f}" fill="#FFFFFF" opacity="0.8"/>')
    body.append(mono("DOME CAP  Ø2.0 IN POCKET", 6.5, cx, cy + 1.35 * IN, "#C7CBD0", anchor="middle", tracking=0.15))
    # cord coil pocket (ring segment, lower left)
    body.append(f'<path d="M {cx-4.6*IN:.2f} {cy+1.2*IN:.2f} A {4.75*IN:.2f} {4.75*IN:.2f} 0 0 0 {cx-1.4*IN:.2f} {cy+4.55*IN:.2f} L {cx-1.4*IN:.2f} {cy+3.6*IN:.2f} A {3.8*IN:.2f} {3.8*IN:.2f} 0 0 1 {cx-3.65*IN:.2f} {cy+1.0*IN:.2f} Z" fill="#16130F" stroke="#C7CBD0" stroke-width="0.8"/>')
    body.append(mono("CORD + ADAPTER", 6.5, cx - 3.3 * IN, cy + 3.3 * IN, "#C7CBD0", anchor="middle", tracking=0.15))
    # hardware pocket (upper right): plate, screws, anchors, felt washer
    body.append(rect(cx + 1.6 * IN, cy - 4.4 * IN, 2.9 * IN, 1.5 * IN, 'fill="#16130F" stroke="#C7CBD0" stroke-width="0.8" rx="6"'))
    body.append(mono("WALL PLATE + HARDWARE", 6.5, cx + 3.05 * IN, cy - 3.6 * IN, "#C7CBD0", anchor="middle", tracking=0.15))
    # card slot (upper left)
    body.append(rect(cx - 4.6 * IN, cy - 4.4 * IN, 2.9 * IN, 0.35 * IN, 'fill="#16130F" stroke="#C7CBD0" stroke-width="0.8" rx="3"'))
    body.append(mono("CARD SLOT 5 x 7", 6.5, cx - 3.15 * IN, cy - 3.75 * IN, "#C7CBD0", anchor="middle", tracking=0.15))
    body.append(mono("LAYER 1  ·  TOP  ·  1.25 IN  ·  BLACK EPE FOAM 1.7 PCF or MOULDED PULP (BLACK)", 7, x0, y0 + S + 0.3 * IN, "#333333", tracking=0.12))
    # plan: lower layer
    x1 = pad * 2 + S
    body.append(rect(x1, y0, S, S, f'fill="#2B2622"'))
    cx1 = x1 + S / 2
    body.append(f'<circle cx="{cx1:.2f}" cy="{cy:.2f}" r="{5.375*IN:.2f}" fill="#16130F" stroke="#C7CBD0" stroke-width="0.8"/>')
    body.append(f'<circle cx="{cx1:.2f}" cy="{cy:.2f}" r="{2.1*IN:.2f}" fill="none" stroke="#5F6468" stroke-width="0.6" stroke-dasharray="4 3"/>')
    body.append(mono("HUB RELIEF Ø4.2", 6, cx1, cy + 0.1 * IN, "#8A8F94", anchor="middle", tracking=0.15))
    body.append(mono("BACKPLATE + LED RING  Ø10.75 IN POCKET", 6.5, cx1, cy + 4.8 * IN, "#C7CBD0", anchor="middle", tracking=0.15))
    body.append(mono("LAYER 2  ·  1.5 IN  ·  SAME MATERIAL  ·  RECORD IN POLY-LINED SLEEVE LIES FLAT UNDER THIS LAYER", 7, x1, y0 + S + 0.3 * IN, "#333333", tracking=0.12))
    # section view
    sy = y0 + S + 0.9 * IN
    sx = pad
    sw = S
    body.append(mono("SECTION A-A (THROUGH CENTRE)  ·  BOX INTERIOR DEPTH 3.0 IN", 7, sx, sy, "#333333", tracking=0.12))
    top = sy + 0.3 * IN
    body.append(rect(sx, top, sw, 3.0 * IN, 'fill="none" stroke="#999999" stroke-width="0.6"'))
    # sleeve
    body.append(rect(sx + 0.15 * IN, top + 2.75 * IN, sw - 0.3 * IN, 0.2 * IN, 'fill="#5F6468"'))
    body.append(mono("RECORD IN SLEEVE  0.2 IN", 6, sx + sw - 0.3 * IN, top + 2.9 * IN, "#FFFFFF", anchor="end", tracking=0.1))
    # layer 2
    body.append(rect(sx + 0.125 * IN, top + 1.25 * IN, sw - 0.25 * IN, 1.5 * IN, 'fill="#2B2622"'))
    body.append(rect(sx + sw / 2 - 5.375 * IN, top + 1.25 * IN, 10.75 * IN, 1.1 * IN, 'fill="#16130F"'))
    body.append(rect(sx + sw / 2 - 2.1 * IN, top + 2.35 * IN, 4.2 * IN, 0.4 * IN, 'fill="#16130F"'))
    # backplate in pocket
    body.append(rect(sx + sw / 2 - 5.25 * IN, top + 1.95 * IN, 10.5 * IN, 0.35 * IN, 'fill="#8A8F94"'))
    body.append(rect(sx + sw / 2 - 2.0 * IN, top + 2.3 * IN, 4.0 * IN, 0.4 * IN, 'fill="#8A8F94"'))
    body.append(mono("BACKPLATE + HUB", 6, sx + sw / 2 + 2.3 * IN, top + 2.15 * IN, "#FFFFFF", tracking=0.1))
    # layer 1
    body.append(rect(sx + 0.125 * IN, top, sw - 0.25 * IN, 1.25 * IN, 'fill="#2B2622"'))
    body.append(rect(sx + sw / 2 - 1.0 * IN, top, 2.0 * IN, 1.0 * IN, 'fill="#16130F"'))
    body.append(f'<path d="M {sx + sw/2 - 0.72*IN:.2f} {top + 0.95*IN:.2f} A {0.72*IN:.2f} {0.72*IN:.2f} 0 0 1 {sx + sw/2 + 0.72*IN:.2f} {top + 0.95*IN:.2f} Z" fill="#C7CBD0"/>')
    body.append(mono("DOME, FACE UP, FIRST THING SEEN", 6, sx + sw / 2 + 1.2 * IN, top + 0.6 * IN, "#FFFFFF", tracking=0.1))
    body.append(mono("1.25", 6, sx + sw + 4, top + 0.65 * IN, "#333333", tracking=0.05))
    body.append(mono("1.50", 6, sx + sw + 4, top + 2.05 * IN, "#333333", tracking=0.05))
    body.append(mono("0.25", 6, sx + sw + 4, top + 2.9 * IN, "#333333", tracking=0.05))
    body.append(title_block(f"{BRAND}  ·  Insert tray  ·  12.75 x 12.75 in, two layers, 2.75 in", "Fits 13 x 13 x 3 mailer with 0.125 in clearance per side  ·  dome centred on the spindle axis  ·  die-cut EPE foam (sample from a foam converter) or moulded pulp at volume", pad, Ht - 0.3 * IN))
    write("insert-tray.svg", svg(Wt, Ht, "\n".join(body), bg="#FFFFFF"))


# ------------------------------------------------------------------ cards
def qr_svg_paths(data, x, y, size):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=0)
    qr.add_data(data)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    cell = size / n
    out = []
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v:
                out.append(f'<rect x="{x + c*cell:.2f}" y="{y + r*cell:.2f}" width="{cell+0.05:.2f}" height="{cell+0.05:.2f}" fill="{P["vinyl"]}"/>')
    return "\n".join(out)


def insert_card():
    Wc, Hc = 5 * IN, 7 * IN
    # FRONT: Label stock, monogram, brand, the ritual line
    body = [rect(-BLEED, -BLEED, Wc + 2 * BLEED, Hc + 2 * BLEED, f'fill="{P["label"]}"')]
    body.append(monogram(Wc / 2, 2.2 * IN, 1.25 * IN, P["vinyl"], P["chrome_deep"], halo=P["halo"]))
    body.append(T.text_path(WORD, "sans-semibold", 0.42 * IN, Wc / 2, 4.15 * IN, tracking=0.08, anchor="middle", fill=P["vinyl"]))
    body.append(serif("Change the record.", 0.4 * IN, Wc / 2, 5.0 * IN, P["ember"], anchor="middle"))
    body.append(serif("Change the room.", 0.4 * IN, Wc / 2, 5.45 * IN, P["ember"], anchor="middle"))
    body.append(mono("THANK YOU FOR BEING ONE OF THE FIRST", 7.5, Wc / 2, Hc - 0.55 * IN, P["chrome_deep"], anchor="middle", tracking=0.2))
    body.append(rect(0, 0, Wc, Hc, BLEEDL.replace("0.6", "0.9")))
    write("insert-card-front.svg", svg(Wc, Hc, "\n".join(body)))
    # BACK: install steps + QR + the swap ritual + safety
    body = [rect(-BLEED, -BLEED, Wc + 2 * BLEED, Hc + 2 * BLEED, f'fill="{P["label"]}"')]
    m = 0.45 * IN
    body.append(mono("INSTALL IN FOUR STEPS", 8, m, m + 8, P["chrome_deep"], tracking=0.22))
    steps = [
        ("1", "Plate.", "Screw the steel plate to the wall. It fits a standard box or two anchors; the arc slots let you level it."),
        ("2", "Hub.", "Set the hub on the plate, twist to lock, snug the set screw at six o'clock."),
        ("3", "Power.", "In-wall: run the low-voltage cable down to the outlet plate. Surface: clip the cord into the channel."),
        ("4", "Record.", "Unscrew the dome. Slide your record onto the post, label out. Screw the dome back until the felt just grips."),
    ]
    yy = m + 0.45 * IN
    for num, head, text in steps:
        body.append(T.text_path(num, "serif-italic", 0.36 * IN, m, yy + 0.22 * IN, fill=P["ember"]))
        body.append(sans(head, 12, m + 0.35 * IN, yy + 0.05 * IN, P["vinyl"], key="sans-semibold"))
        lines = T.wrap(text, "sans-regular", 9, Wc - 2 * m - 0.35 * IN - 1.35 * IN)
        for i, ln in enumerate(lines):
            body.append(sans(ln, 9, m + 0.35 * IN, yy + 0.25 * IN + i * 12, P["chrome_deep"], key="sans-regular"))
        yy += 0.25 * IN + len(lines) * 12 + 0.14 * IN
    # QR right column
    qx, qy, qs = Wc - m - 1.2 * IN, m + 0.45 * IN, 1.2 * IN
    body.append(qr_svg_paths(INSTALL_URL, qx, qy, qs))
    body.append(mono("VIDEO + IN-WALL GUIDE", 6, qx + qs / 2, qy + qs + 0.2 * IN, P["chrome_deep"], anchor="middle", tracking=0.15))
    body.append(mono(INSTALL_URL.replace("https://", ""), 6, qx + qs / 2, qy + qs + 0.33 * IN, P["chrome_deep"], anchor="middle", tracking=0.05))
    # ritual
    body.append(line(m, yy, Wc - m, yy, f'stroke="{P["chrome"]}" stroke-width="0.6"'))
    yy += 0.3 * IN
    body.append(mono("THE RITUAL", 8, m, yy, P["chrome_deep"], tracking=0.22))
    rit = "New season, new record. The dome comes off by hand in two turns and nothing touches your vinyl but felt. Put on what you are playing this month. Flip it to the B side when you are bored of the label. The halo does the rest."
    rit_lines = T.wrap(rit, "sans-regular", 9, Wc - 2 * m)
    for i, ln in enumerate(rit_lines):
        body.append(sans(ln, 9, m, yy + 0.2 * IN + i * 12, P["vinyl"], key="sans-regular"))
    yy += 0.2 * IN + len(rit_lines) * 12 + 0.12 * IN
    body.append(line(m, yy, Wc - m, yy, f'stroke="{P["chrome"]}" stroke-width="0.6"'))
    yy += 0.28 * IN
    body.append(mono("SAFETY", 8, m, yy, P["chrome_deep"], tracking=0.22))
    saf = "12 V DC Class 2 only, from the supplied listed adapter. Indoor, dry locations. The light ring runs warm to the touch, never hot; keep the 1/4 in gap behind the record clear. Do not open the hub. Nothing in this fixture carries line voltage."
    saf_lines = T.wrap(saf, "sans-regular", 7.5, Wc - 2 * m)
    for i, ln in enumerate(saf_lines):
        body.append(sans(ln, 7.5, m, yy + 0.18 * IN + i * 10, P["chrome_deep"], key="sans-regular"))
    yy += 0.18 * IN + len(saf_lines) * 10
    assert yy < Hc - 0.45 * IN, f"insert card back overflows: {yy/IN:.2f} in"
    body.append(mono(f"{WORD}  ·  MADE TO ORDER  ·  SERIAL ON THE HUB", 6.5, Wc / 2, Hc - 0.28 * IN, P["chrome_deep"], anchor="middle", tracking=0.2))
    body.append(rect(0, 0, Wc, Hc, BLEEDL.replace("0.6", "0.9")))
    write("insert-card-back.svg", svg(Wc, Hc, "\n".join(body)))


def warranty_card():
    Wc, Hc = 3.5 * IN, 5 * IN
    body = [rect(-BLEED, -BLEED, Wc + 2 * BLEED, Hc + 2 * BLEED, f'fill="{P["soot"]}"')]
    m = 0.35 * IN
    body.append(monogram(Wc / 2, 0.95 * IN, 0.5 * IN, P["vinyl"], P["chrome"], halo=P["halo"], rings=False))
    body.append(mono("TWO-YEAR WARRANTY", 9, Wc / 2, 1.85 * IN, P["label"], anchor="middle", tracking=0.24))
    txt = ("We cover the light ring, driver, hub and plate against defects in materials and workmanship for two years from delivery. "
           "If it fails, we repair or replace it and pay the shipping both ways. The warranty does not cover your record, "
           "damage from line-voltage adapters, outdoor use, or opening the hub. Register with the serial below, or do not: your order email is your proof.")
    for i, ln in enumerate(T.wrap(txt, "sans-regular", 8, Wc - 2 * m)):
        body.append(sans(ln, 8, m, 2.2 * IN + i * 11, P["chrome"], key="sans-regular"))
    yy = 3.75 * IN
    for lab in ("SERIAL", "FINISH", "DATE"):
        body.append(mono(lab, 6.5, m, yy, P["chrome"], tracking=0.2))
        body.append(line(m + 0.7 * IN, yy + 1, Wc - m, yy + 1, f'stroke="{P["chrome"]}" stroke-width="0.5"'))
        yy += 0.3 * IN
    body.append(mono("HELLO@" + INSTALL_URL.split("/")[2].upper(), 6.5, Wc / 2, Hc - 0.3 * IN, P["chrome"], anchor="middle", tracking=0.15))
    body.append(rect(0, 0, Wc, Hc, BLEEDL.replace("0.6", "0.9")))
    write("warranty-card.svg", svg(Wc, Hc, "\n".join(body)))


def sticker():
    # 2 in round: Vinyl field, Chrome ring, monogram. Also the finish stickers (2.25 x 0.5 in).
    S = 2 * IN
    body = [f'<circle cx="{S/2:.2f}" cy="{S/2:.2f}" r="{S/2 + BLEED:.2f}" fill="{P["vinyl"]}"/>']
    body.append(f'<circle cx="{S/2:.2f}" cy="{S/2:.2f}" r="{S/2 - 0.06*IN:.2f}" fill="none" stroke="{P["chrome"]}" stroke-width="1.2"/>')
    body.append(monogram(S / 2, S / 2 - 0.08 * IN, 0.5 * IN, P["vinyl"], P["chrome"], halo=P["halo"]))
    body.append(mono(WORD, 7.5, S / 2, S / 2 + 0.72 * IN, P["label"], anchor="middle", tracking=0.26))
    body.append(f'<circle cx="{S/2:.2f}" cy="{S/2:.2f}" r="{S/2:.2f}" {CUT}/>')
    write("sticker-2in-round.svg", svg(S, S, "\n".join(body)))
    # finish stickers strip
    Wf, Hf = 3.0 * IN, 0.55 * IN
    rows = [("CHROME", P["chrome"], P["vinyl"]), ("BRASS", P["brass"], P["vinyl"]), ("BLACK", "#111111", P["label"])]
    body = []
    for i, (name, sw, fg) in enumerate(rows):
        y = i * (Hf + 0.2 * IN)
        body.append(rect(0, y, Wf, Hf, f'fill="{P["label"]}" stroke="#E6007E" stroke-width="0.5" rx="4"'))
        body.append(f'<circle cx="{0.3*IN:.2f}" cy="{y + Hf/2:.2f}" r="{0.15*IN:.2f}" fill="{sw}" stroke="{P["vinyl"]}" stroke-width="0.4"/>')
        body.append(mono(f"FINISH  {name}", 7.5, 0.6 * IN, y + Hf / 2 + 2.5, P["vinyl"], tracking=0.2))
        body.append(mono("SPINDLE 12", 7.5, Wf - 0.15 * IN, y + Hf / 2 + 2.5, P["chrome_deep"], anchor="end", tracking=0.2))
    write("sticker-finish-labels.svg", svg(Wf, 3 * Hf + 0.4 * IN, "\n".join(body)))


if __name__ == "__main__":
    mailer_outside()
    mailer_inside()
    tray()
    insert_card()
    warranty_card()
    sticker()
    print("packaging written:", sorted(os.listdir(OUT)))
