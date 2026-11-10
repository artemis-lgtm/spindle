"""Generate the brand identity SVGs: monogram, wordmarks, lockups, palette, tokens.

Run:  python3 brand/tools/gen_brand.py
All text is outlined (fontTools) so the files carry no font dependency.
Units: SVG user units are points (72 per inch) unless stated.
"""
import json
import math
import os

import svgtext as T

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
LOGO = os.path.join(BRAND, "logo")
os.makedirs(LOGO, exist_ok=True)

# ---------------------------------------------------------------- palette
PALETTE = {
    "vinyl": {"hex": "#16130F", "name": "Vinyl", "role": "Ink. The record. Primary text and dark surfaces."},
    "soot": {"hex": "#2B2622", "name": "Soot", "role": "Dark surface two. Box interior, card backs."},
    "plaster": {"hex": "#E9DFCF", "name": "Plaster", "role": "Canvas. The warm wall in the reference photo."},
    "label": {"hex": "#F4ECDD", "name": "Label", "role": "Lightest surface. Cards, insert, web background."},
    "halo": {"hex": "#F0A43B", "name": "Halo", "role": "The one accent. 2700K glow. Used sparingly, never as a fill behind text."},
    "ember": {"hex": "#B9661C", "name": "Ember", "role": "Halo on light surfaces, hover states, print-safe accent."},
    "chrome": {"hex": "#C7CBD0", "name": "Chrome", "role": "Hardware highlight. Rules, metadata, monogram dome."},
    "chrome_deep": {"hex": "#5F6468", "name": "Chrome Deep", "role": "Hardware shadow. Secondary text on light surfaces."},
    "brass": {"hex": "#B7955B", "name": "Brass", "role": "Finish variant swatch only. Never a UI color."},
}
P = {k: v["hex"] for k, v in PALETTE.items()}

NAMES = {
    "sidea": {"brand": "Side A", "word": "SIDE A", "slug": "side-a"},
    "deadwax": {"brand": "Deadwax", "word": "DEADWAX", "slug": "deadwax"},
    "spindle": {"brand": "Spindle", "word": "SPINDLE", "slug": "spindle"},
}
RECOMMENDED = "spindle"


def svg(w, h, body, bg=None, vb=None):
    vb = vb or f"0 0 {w} {h}"
    bgrect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" viewBox="{vb}">\n'
            f"{bgrect}\n{body}\n</svg>\n")


def write(name, content):
    path = os.path.join(LOGO, name)
    with open(path, "w") as f:
        f.write(content)
    return path


# ---------------------------------------------------------------- monogram
def monogram(cx, cy, r, ink, dome, halo=None, rings=True, dome_hole=True):
    """The mark: a record seen head-on, grooves as thin rings, a mirror dome where
    the spindle hole is, and the halo as an offset ring behind the disc.
    Geometry echoes the product: 12" disc, 4" label, 1.4" dome. Ratios kept."""
    out = []
    if halo:
        # halo: a soft ring behind the disc, offset slightly down-right like a wall glow
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.18:.2f}" fill="none" stroke="{halo}" stroke-width="{r*0.16:.2f}" opacity="0.9"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.2f}" fill="{ink}"/>')
    if rings:
        # groove rings: three thin arcs, broken at the top-right like light catching the grooves
        for k, rr in enumerate((0.86, 0.72, 0.58)):
            rad = r * rr
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad:.2f}" fill="none" stroke="{dome}" stroke-width="{r*0.025:.2f}" opacity="{0.55 - k*0.12:.2f}" stroke-dasharray="{rad*2*math.pi*0.78:.2f} {rad*2*math.pi*0.22:.2f}" transform="rotate(-62 {cx} {cy})"/>')
    # label: slightly lighter disc, 1/3 of the record (4" of 12")
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r/3:.2f}" fill="{ink}" stroke="{dome}" stroke-width="{r*0.02:.2f}" opacity="1"/>')
    # dome: 1.4" of 12" = 0.117 r, drawn a touch larger for legibility at small sizes
    rd = r * 0.14
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{rd:.2f}" fill="{dome}"/>')
    if dome_hole:
        # specular: small bright crescent top-left of the dome
        out.append(f'<circle cx="{cx - rd*0.3:.2f}" cy="{cy - rd*0.3:.2f}" r="{rd*0.35:.2f}" fill="#FFFFFF" opacity="0.85"/>')
    return "\n".join(out)


def write_monograms():
    s = 240
    c = s / 2
    # on light
    write("monogram-on-light.svg", svg(s, s, monogram(c, c, 92, P["vinyl"], P["chrome_deep"], halo=P["halo"]), bg=None))
    # on dark
    write("monogram-on-dark.svg", svg(s, s, monogram(c, c, 92, P["vinyl"], P["chrome"], halo=P["halo"]), bg=P["soot"]))
    # one-colour (for embossing, debossing, foil, laser on the hub)
    write("monogram-mono-black.svg", svg(s, s, monogram(c, c, 100, "#000000", "#FFFFFF", halo=None, rings=False, dome_hole=False), bg=None))
    write("monogram-mono-white.svg", svg(s, s, monogram(c, c, 100, "#FFFFFF", "#000000", halo=None, rings=False, dome_hole=False), bg=None))
    # favicon / app icon: dome-forward, no rings
    write("icon-512.svg", svg(512, 512, f'<rect width="512" height="512" rx="112" fill="{P["vinyl"]}"/>' + monogram(256, 256, 190, P["vinyl"], P["chrome"], halo=P["halo"], rings=False), bg=None))


# ---------------------------------------------------------------- wordmarks
def wordmark_paths(word, size, x, y, fill, anchor="start"):
    # Inter Tight SemiBold, tracked +0.06em: a quiet grotesk wordmark in the
    # Schoolhouse / Rejuvenation lane. All caps so it sits as a plate on hardware.
    return T.text_path(word, "sans-semibold", size, x, y, tracking=0.06, anchor=anchor, fill=fill)


def write_wordmarks():
    for key, n in NAMES.items():
        size = 96
        w = T.measure(n["word"], "sans-semibold", size, 0.06)
        pad = 24
        W, H = w + pad * 2, size * 1.1 + pad * 2
        base = pad + size * 0.86
        write(f"wordmark-{n['slug']}-on-light.svg", svg(round(W), round(H), wordmark_paths(n["word"], size, pad, base, P["vinyl"])))
        write(f"wordmark-{n['slug']}-on-dark.svg", svg(round(W), round(H), wordmark_paths(n["word"], size, pad, base, P["label"]), bg=P["vinyl"]))
        # editorial variant: Instrument Serif italic, used in taglines and the "ritual" line, not as the logo
        ser = T.text_path(n["brand"], "serif-italic", 120, pad, pad + 100, tracking=0.0, fill=P["vinyl"])
        ws = T.measure(n["brand"], "serif-italic", 120)
        write(f"wordmark-{n['slug']}-serif-italic.svg", svg(round(ws + pad * 2), 150, ser))


def write_lockups():
    for key, n in NAMES.items():
        # horizontal: monogram left, wordmark right, baseline aligned to the dome centre
        size = 84
        r = 46
        gap = 26
        pad = 24
        ww = T.measure(n["word"], "sans-semibold", size, 0.06)
        W = pad + r * 2.4 + gap + ww + pad
        H = pad * 2 + r * 2.4
        cx = pad + r * 1.2
        cy = H / 2
        for variant, ink, dome, bg, fill in (
            ("on-light", P["vinyl"], P["chrome_deep"], None, P["vinyl"]),
            ("on-dark", P["vinyl"], P["chrome"], P["vinyl"], P["label"]),
            ("on-plaster", P["vinyl"], P["chrome_deep"], P["plaster"], P["vinyl"]),
        ):
            body = monogram(cx, cy, r, ink, dome, halo=P["halo"]) + "\n" + wordmark_paths(n["word"], size, pad + r * 2.4 + gap, cy + size * 0.36, fill)
            write(f"lockup-{n['slug']}-horizontal-{variant}.svg", svg(round(W), round(H), body, bg=bg))
        # stacked: monogram above, wordmark below, mono descriptor line under that
        size = 64
        r = 70
        ww = T.measure(n["word"], "sans-semibold", size, 0.06)
        W = max(ww, r * 2.6) + pad * 2
        H = pad + r * 2.4 + 22 + size + 14 + 14 + pad
        cx = W / 2
        cy = pad + r * 1.2
        desc = "RECORD SCONCES"
        for variant, ink, dome, bg, fill, sub in (
            ("on-light", P["vinyl"], P["chrome_deep"], None, P["vinyl"], P["chrome_deep"]),
            ("on-dark", P["vinyl"], P["chrome"], P["vinyl"], P["label"], P["chrome"]),
        ):
            body = monogram(cx, cy, r, ink, dome, halo=P["halo"])
            body += "\n" + wordmark_paths(n["word"], size, cx, pad + r * 2.4 + 22 + size * 0.86, fill, anchor="middle")
            body += "\n" + T.text_path(desc, "mono-medium", 12, cx, pad + r * 2.4 + 22 + size + 26, tracking=0.22, anchor="middle", fill=sub)
            write(f"lockup-{n['slug']}-stacked-{variant}.svg", svg(round(W), round(H), body, bg=bg))


# ---------------------------------------------------------------- palette sheet + tokens
def write_palette():
    sw = 150
    gap = 14
    items = list(PALETTE.items())
    W = gap + (sw + gap) * len(items)
    H = 260
    body = []
    for i, (k, v) in enumerate(items):
        x = gap + i * (sw + gap)
        body.append(f'<rect x="{x}" y="{gap}" width="{sw}" height="150" rx="6" fill="{v["hex"]}" stroke="{P["chrome"]}" stroke-width="0.5"/>')
        body.append(T.text_path(v["name"], "sans-semibold", 14, x, gap + 150 + 24, fill=P["vinyl"]))
        body.append(T.text_path(v["hex"], "mono", 11, x, gap + 150 + 42, fill=P["chrome_deep"]))
        for j, ln in enumerate(T.wrap(v["role"], "sans-regular", 9, sw)):
            body.append(T.text_path(ln, "sans-regular", 9, x, gap + 150 + 60 + j * 12, fill=P["chrome_deep"]))
    write("palette.svg", svg(W, H, "\n".join(body), bg="#FFFFFF"))
    tokens = {
        "brand": NAMES[RECOMMENDED]["brand"],
        "alternates": [NAMES[k]["brand"] for k in NAMES if k != RECOMMENDED],
        "color": {k: v["hex"] for k, v in PALETTE.items()},
        "font": {
            "display": {"family": "Inter Tight", "weights": [500, 600, 700], "source": "https://fonts.google.com/specimen/Inter+Tight", "license": "OFL", "use": "Wordmark (600, +0.06em caps), headlines (600, -0.02em), UI and body (400/500)"},
            "editorial": {"family": "Instrument Serif", "weights": [400, "400 italic"], "source": "https://fonts.google.com/specimen/Instrument+Serif", "license": "OFL", "use": "Taglines, the ritual line, pull quotes. Italic, large, never below 20px"},
            "mono": {"family": "JetBrains Mono", "weights": [400, 500], "source": "https://fonts.google.com/specimen/JetBrains+Mono", "license": "OFL", "use": "Specs, serials, finish codes, labels: the deadwax etching voice. Caps, +0.18 to +0.22em"},
            "licensed_alternatives": {"display": "Söhne (Klim) or Neue Haas Grotesk", "editorial": "GT Alpina (Grilli) or Canela (Commercial Type)", "mono": "Söhne Mono (Klim) or Berkeley Mono"},
        },
        "type_scale_px": {"display": 64, "h1": 44, "h2": 32, "h3": 24, "body": 17, "small": 14, "meta": 12},
        "letter_spacing_em": {"display": -0.02, "h1": -0.015, "body": 0, "caps_meta": 0.2, "wordmark": 0.06},
        "radius_px": {"card": 6, "button": 999, "image": 8},
        "space_px": [4, 8, 12, 16, 24, 32, 48, 64, 96, 128],
        "rules": [
            "One accent only (Halo). It appears as light, not as a fill: glows, hairline rules, a single word.",
            "Warm neutrals only. No pure white and no pure black in print; Label and Vinyl are the extremes.",
            "Chrome colours are for hardware and metadata, never for headlines.",
            "Brass is a finish swatch in the configurator and nowhere else.",
        ],
    }
    with open(os.path.join(BRAND, "tokens.json"), "w") as f:
        json.dump(tokens, f, indent=2)
    css = [":root {"]
    for k, v in PALETTE.items():
        css.append(f"  --c-{k.replace('_', '-')}: {v['hex']};")
    css += [
        "  --f-display: 'Inter Tight', 'Helvetica Neue', Arial, sans-serif;",
        "  --f-editorial: 'Instrument Serif', Georgia, serif;",
        "  --f-mono: 'JetBrains Mono', ui-monospace, Menlo, monospace;",
        "}",
    ]
    with open(os.path.join(BRAND, "tokens.css"), "w") as f:
        f.write("\n".join(css) + "\n")


if __name__ == "__main__":
    write_monograms()
    write_wordmarks()
    write_lockups()
    write_palette()
    print("brand assets written to", LOGO)
    print(sorted(os.listdir(LOGO)))
