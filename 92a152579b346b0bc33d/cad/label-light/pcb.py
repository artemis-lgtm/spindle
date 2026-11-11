"""Board outlines (DXF, mm, R2010) + placement previews for the two label-light PCBs.

RS-PCB-12L-LED : cap LED ring, D 24.6 x D 8.2, 0.8 mm FR4, 6x LUXEON 2835 + 2x 100R on the BOTTOM side.
RS-PCB-12L-HUB : hub contact disc, D 13.0, 1.6 mm FR4, rev B: gold spring pad (centre) + Mill-Max 0919 return pin (SMT) + NSI45020 CCR
                 + 1N4148WS + 15 V TVS + 100 mA PTC, TOP side. No holes except the two wire pads.
Layers: OUTLINE (board edge), DRILL (plated unless noted), COMP_BOT / COMP_TOP (component bodies, reference only),
PAD (copper keep-in notes), NOTE (text). Run from cad/: .venv/bin/python label-light/pcb.py
"""
import math
import os
import sys
import ezdxf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sconce_lit as L    # noqa: E402

OUT = os.path.join(HERE, "pcb")


def _doc():
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    for name, col in (("OUTLINE", 7), ("DRILL", 1), ("COMP_BOT", 3), ("COMP_TOP", 5), ("PAD", 2), ("NOTE", 8)):
        doc.layers.add(name, color=col)
    return doc


def _rect(msp, cx, cy, w, h, ang, layer):
    a = math.radians(ang)
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        pts.append((cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)))
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})


def led_board(path):
    doc = _doc(); msp = doc.modelspace()
    msp.add_circle((0, 0), L.LPCB_D / 2, dxfattribs={"layer": "OUTLINE"})
    # D-shaped centre hole: arc of the ID circle + a chord (flat) at x = SPG_KEY_X + 0.1, keyed to the spigot flat (anti-rotation)
    xf = L.SPG_KEY_X + 0.1
    r = L.LPCB_ID / 2
    a = math.degrees(math.acos(xf / r))
    msp.add_arc((0, 0), r, a, 360 - a, dxfattribs={"layer": "OUTLINE"})
    yf = math.sqrt(r * r - xf * xf)
    msp.add_line((xf, -yf), (xf, yf), dxfattribs={"layer": "OUTLINE"})
    placements = []
    for k in range(L.LED_N):
        a = 90 + 360 / L.LED_N * k
        x, y = L.pol(L.LED_R, a)
        _rect(msp, x, y, L.LED_SIZE[0], L.LED_SIZE[1], a - 90, "COMP_BOT")
        placements.append((f"D{k + 1}", "LUXEON 2835 L128-2790SA35A0DF1", "bottom", round(x, 3), round(y, 3), round((a - 90) % 360, 1)))
    for i, a in enumerate((120, 300)):
        x, y = L.pol(11.0, a)
        _rect(msp, x, y, 1.6, 0.8, a, "COMP_BOT")
        placements.append((f"R{i + 1}", "100R 1% 0603", "bottom", round(x, 3), round(y, 3), a))
    # ESD clamp across LED+ / LED- (a static-charged record discharging into the pin would otherwise go through the LEDs)
    x, y = L.pol(11.0, 240)
    _rect(msp, x, y, 1.0, 0.6, 240, "COMP_BOT")
    placements.append(("Z1", "ESD/TVS 12 V UNIDIRECTIONAL 0402 (e.g. PESD12VS1UL class), cathode to LED+, anode to LED-", "bottom", round(x, 3), round(y, 3), 240))
    # pads: return ring on BOTH faces (r 4.1..6.0, exposed ENIG, stitched with 8 vias): bottom on the column top, top under
    # the dome boss (rev B: second return contact), + lead pad at r 6.4, az 60
    msp.add_circle((0, 0), 6.0, dxfattribs={"layer": "PAD"})
    for k in range(8):
        vx, vy = L.pol(5.2, 22.5 + 45 * k)
        if vx < L.SPG_KEY_X + 0.9:                       # keep vias off the D-flat side of the hole
            msp.add_circle((vx, vy), 0.15, dxfattribs={"layer": "DRILL"})
    x, y = L.pol(L.LPCB_PAD_R, L.XHOLE_ANG)
    msp.add_circle((x, y), 0.6, dxfattribs={"layer": "PAD"})
    msp.add_text("BOTH FACES: exposed ENIG ring r4.1-6.0 = LED- (no mask), stitched by D0.3 vias on r5.2. Bottom pad at r6.4/60deg = LED+ (hand-solder PTFE lead). Centre hole is a D: flat at x=+3.7 keys the spigot.",
                 dxfattribs={"layer": "NOTE", "height": 0.5}).set_placement((-12, -14))
    doc.saveas(path)
    return placements


def hub_board(path):
    doc = _doc(); msp = doc.modelspace()
    msp.add_circle((0, 0), L.HPCB_D / 2, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((0, 0), L.GUARD_BORE_D / 2, dxfattribs={"layer": "PAD"})       # flat ENIG pad D 2.6: the contact spring sits on it
    msp.add_circle(L.POGO_R_POS, 0.915, dxfattribs={"layer": "PAD"})              # 0919 SMT pad D 1.83 (return pin)
    px, py, ph, cx, cy = L.CCR_POCKET
    _rect(msp, cx, cy, 2.7, 1.6, 0, "COMP_TOP")
    qx, qy, qh, dx, dy = L.D1_POCKET
    _rect(msp, dx, dy, 1.7, 1.25, 0, "COMP_TOP")
    _rect(msp, L.Z1_POCKET[3], L.Z1_POCKET[4], 1.0, 0.6, 0, "COMP_TOP")      # Z1 TVS, contact node to return
    _rect(msp, L.F1_POCKET[3], L.F1_POCKET[4], 1.6, 0.8, 0, "COMP_TOP")      # F1 PTC on the +12 V tap
    msp.add_text("U1 CCR: >= 25 mm2 copper on both pads, stitched to the bottom layer (0.24 W continuous if the pin is shorted).",
                 dxfattribs={"layer": "NOTE", "height": 0.35}).set_placement((-6.2, -6.9))
    for (wx, label) in ((-1.2, "+12V IN"), (1.2, "JACK -")):
        msp.add_circle((wx, 5.2), 0.45, dxfattribs={"layer": "DRILL"})
        msp.add_text(label, dxfattribs={"layer": "NOTE", "height": 0.35}).set_placement((wx - 0.9, 5.8))
    doc.saveas(path)
    return [("P1", "spring pad D 2.6 ENIG, no part (contact spring + plunger live in the carrier)", "top", 0.0, 0.0, 0),
            ("P2", "Mill-Max 0919-0-15-20-89-14-11-0 (SMT) return pin", "top", L.POGO_R_POS[0], L.POGO_R_POS[1], 0),
            ("U1", "onsemi NSI45020AT1G SOD-123", "top", cx, cy, 0),
            ("D1", "1N4148WS SOD-323 (reverse-polarity block)", "top", L.D1_POCKET[3], L.D1_POCKET[4], 0),
            ("Z1", "TVS 15 V standoff unidirectional 0402 (SMF15A class in 0402/SOD-523), contact node to return", "top", L.Z1_POCKET[3], L.Z1_POCKET[4], 0),
            ("F1", "PTC resettable fuse 100 mA hold 0603, in the +12 V tap ahead of D1", "top", L.F1_POCKET[3], L.F1_POCKET[4], 0)]


def preview(dxf_path, png_path):
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    doc = ezdxf.readfile(dxf_path)
    fig = plt.figure(figsize=(6, 6)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=Configuration(background_policy=BackgroundPolicy.WHITE)).draw_layout(doc.modelspace(), finalize=True)
    fig.savefig(png_path, dpi=140, facecolor="white"); plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, fn in (("RS-PCB-12L-LED", led_board), ("RS-PCB-12L-HUB", hub_board)):
        p = os.path.join(OUT, name + ".dxf")
        for r in fn(p):
            rows.append((name,) + r)
        preview(p, os.path.join(OUT, name + ".png"))
    with open(os.path.join(OUT, "placement.csv"), "w") as f:
        f.write("board,designator,part,side,x_mm,y_mm,rot_deg\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    print("pcb outlines written:", OUT)


if __name__ == "__main__":
    main()
