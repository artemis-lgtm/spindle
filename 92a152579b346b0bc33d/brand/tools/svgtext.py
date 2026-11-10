"""Text to outlined SVG paths with fontTools (no Inkscape on this box).

All brand and packaging SVGs are fully outlined so a packaging vendor's prepress
sees shapes, not font dependencies. Fonts: Inter Tight, Instrument Serif,
JetBrains Mono (Google Fonts, OFL). TTFs are cached in brand/tools/fonts/.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
FONTS = {
    "sans": "InterTight-500.ttf",
    "sans-semibold": "InterTight-600.ttf",
    "sans-bold": "InterTight-700.ttf",
    "sans-regular": "InterTight-400.ttf",
    "serif": "InstrumentSerif-Regular.ttf",
    "serif-italic": "InstrumentSerif-Italic.ttf",
    "mono": "JetBrainsMono-400.ttf",
    "mono-medium": "JetBrainsMono-500.ttf",
}
_cache = {}


def font(key):
    if key not in _cache:
        f = TTFont(os.path.join(FONT_DIR, FONTS[key]))
        kern = {}
        try:
            gpos = f["GPOS"].table
            for lookup in gpos.LookupList.Lookup:
                for st in lookup.SubTable:
                    if lookup.LookupType == 9:
                        st = st.ExtSubTable
                    if getattr(st, "LookupType", lookup.LookupType) != 2:
                        continue
                    if st.Format == 1:
                        cov = st.Coverage.glyphs
                        for i, ps in enumerate(st.PairSet):
                            for pvr in ps.PairValueRecord:
                                v = pvr.Value1
                                if v and getattr(v, "XAdvance", 0):
                                    kern[(cov[i], pvr.SecondGlyph)] = v.XAdvance
                    elif st.Format == 2:
                        cov = st.Coverage.glyphs
                        c1 = st.ClassDef1.classDefs
                        c2 = st.ClassDef2.classDefs
                        cls2_members = {}
                        for g, c in c2.items():
                            cls2_members.setdefault(c, []).append(g)
                        for g1 in cov:
                            k1 = c1.get(g1, 0)
                            rec1 = st.Class1Record[k1]
                            for k2, rec2 in enumerate(rec1.Class2Record):
                                v = rec2.Value1
                                if v and getattr(v, "XAdvance", 0):
                                    for g2 in cls2_members.get(k2, []):
                                        kern.setdefault((g1, g2), v.XAdvance)
        except Exception:
            pass
        _cache[key] = (f, kern)
    return _cache[key]


def measure(text, key, size, tracking=0.0):
    """Advance width in user units for text set at `size` (same units)."""
    f, kern = font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    s = size / upm
    w = 0.0
    prev = None
    for ch in text:
        g = cmap.get(ord(ch), ".notdef")
        if prev is not None and (prev, g) in kern:
            w += kern[(prev, g)] * s
        w += hmtx[g][0] * s + tracking * size
        prev = g
    return w - tracking * size if text else 0.0


def text_path(text, key, size, x=0.0, y=0.0, tracking=0.0, anchor="start", fill="#000", extra=""):
    """Return an SVG <path> string for `text` with baseline at (x, y).

    size and coordinates share the SVG user unit. tracking is in em.
    anchor: start | middle | end.
    """
    f, kern = font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    glyphset = f.getGlyphSet()
    upm = f["head"].unitsPerEm
    s = size / upm
    total = measure(text, key, size, tracking)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    d = []
    prev = None
    for ch in text:
        g = cmap.get(ord(ch), ".notdef")
        if prev is not None and (prev, g) in kern:
            x += kern[(prev, g)] * s
        pen = SVGPathPen(glyphset)
        glyphset[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
        cmd = pen.getCommands()
        if cmd:
            d.append(cmd)
        x += hmtx[g][0] * s + tracking * size
        prev = g
    return f'<path d="{" ".join(d)}" fill="{fill}" {extra}/>'


def text_block(lines, key, size, x, y, leading=1.3, tracking=0.0, anchor="start", fill="#000"):
    out = []
    for i, ln in enumerate(lines):
        if ln:
            out.append(text_path(ln, key, size, x, y + i * size * leading, tracking, anchor, fill))
    return "\n".join(out)


def wrap(text, key, size, max_width, tracking=0.0):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if measure(t, key, size, tracking) <= max_width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines
