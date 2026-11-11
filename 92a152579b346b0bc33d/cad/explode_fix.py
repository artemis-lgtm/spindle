"""Heat-safe layout drawing: exploded view of the 12 in MDF sconce plus a side cut, centre to edge.
Since 2026-11-11 the heat-safe layout (cad/THERMAL.md, layout D) IS the canonical CAD, so nothing is injected here any
more: the strip, the aluminium ring RS-HR-12, the cork ring RS-CK-12 and their screws come from assembly.build(), and
every bar in the side cut is placed from sconce_cad.py parameters. The two temperatures come from thermal-results.json.
  .venv/bin/python explode_fix.py export ; Blender -b -P explode_fix.py -- fix ; .venv/bin/python explode_fix.py annotate
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import explode_lit as E
E.TMP = os.path.join(HERE, ".render-tmp", "explode-fix"); E.MAN = os.path.join(E.TMP, "manifest.json")
E.SCENES["fix"] = dict(res=(3200, 1750), ortho=1.14, zmid=0.415, az=27, el=14, only=None, wall=True,
    offsets=[("wall_screw_head", 55), ("wall_plate", 0), ("pem_stud", 0), ("lock_nut", 0), ("hub", 120), ("pigtail", 120),
             ("cord_p", 120), ("inline_jack", 120), ("adapter_plug", 120), ("set_screw", 120), ("heat_ring_screw", 158),
             ("led_cob_strip", 185), ("heat_ring_alu", 222), ("cork_ring", 259), ("backplate", 310), ("ez_lok", 310),
             ("felt_pads", 365), ("centre_backing", 365), ("record", 560), ("pet_label", 660), ("felt_washer", 710),
             ("dome_cap", 780)],
    calls=[("1", ("wall_plate",), "top", -40, -150), ("2", ("hub",), "top", -20, -170), ("3", ("inline_jack",), "bottom", 130, 150),
           ("4", ("led_cob_strip",), "top", -70, -190), ("5", ("heat_ring_alu",), "top", 0, -230), ("6", ("cork_ring",), "top", 70, -190),
           ("7", ("backplate",), "bottom", -150, 110), ("8", ("felt_pads",), "top", 150, -110), ("9", ("record",), "top", 30, -170),
           ("10", ("pet_label",), "top", -50, -230), ("11", ("felt_washer",), "top", 10, -330), ("12", ("dome_cap",), "top", 60, -230)])
LEGEND = [("1", "Steel wall plate", "Screws to the wall or a junction box. Three studs stick out of it."),
          ("2", "Hub", "Twists onto the studs and locks with one small screw. Sets the 1 inch gap behind the plate."),
          ("3", "Power lead", "Short 12 V pigtail with a plug-in connector."),
          ("4", "LED strip (on the back)", "Faces the wall. It has no line of sight to the record."),
          ("5", "Aluminium ring", "1 mm thick, 30 mm wide. Spreads the strip's heat. Four small screws hold it on."),
          ("6", "Cork ring", "1/16 in (1.6 mm) of insulation between the warm aluminium and the wood."),
          ("7", "Backplate", "Black 1/2 in MDF. With the cork, this is the wall between the light and your record."),
          ("8", "Felt pads + centre ring", "The record rests on these, so it never touches wood."),
          ("9", "Your record", "Any 12 in LP. Nothing glued, drilled or modified."),
          ("10", "Clear label washer", "Protects the paper label."),
          ("11", "Felt washer", "Cushion between the chrome and the label."),
          ("12", "Chrome dome cap", "Screw built in. Goes through the record's hole into the brass insert.")]
HALO = ("led_cob_strip", "heat_ring_alu", "cork_ring", "heat_ring_screw")


def export():
    import assembly as A
    from cadquery import exporters
    os.makedirs(E.TMP, exist_ok=True)
    man = []
    for n, p, c, k in A.build("12", "mdf"):                 # canonical parts only
        f = os.path.join(E.TMP, n.replace("/", "-") + ".stl")
        exporters.export(p, f, exportType="STL", tolerance=0.02, angularTolerance=0.06)
        bb = p.val().BoundingBox()
        c = {"pet_label_washer": "pet", "hub": "hub"}.get(n, c)
        man.append(dict(name=n, file=f, color=c, bb=[bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]))
    json.dump(man, open(E.MAN, "w"), indent=1)
    for m in man:
        if m["name"].startswith(HALO):
            print(m["name"], [round(v, 2) for v in m["bb"]])


def side_cut_numbers():
    """Every bar of the side cut as (z0, z1, r0, r1) in mm from the wall / from the centre, from the CAD parameters."""
    import sconce_cad as S
    zb0 = S.HUB_T
    zb1 = zb0 + S.BP_T
    zr0 = zb1 + S.REC_SEAT_H
    zr1 = zr0 + S.REC12_T
    zp1 = zr1 + S.PET_WASHER[2]
    zc = zp1 + S.FELT12_PROUD / 2                      # cap band underside (felt compressed to half its 0.6 proud)
    ztip = zc + S.CAP12_RIM_H + S.CAP12_DOME_H
    hd, hh = S.HALO_SCREW_HEAD
    n = dict(
        hub=(0, S.HUB_T, 0, S.HUB_D / 2),
        plate=(0, S.PLATE_T, S.PLATE_HOLE_Y1, S.PLATE_D / 2),
        post=(S.PLATE_T, S.PLATE_T + S.STUD_L, S.STUD_R - S.STUD_D / 2, S.STUD_R + S.STUD_D / 2),
        backplate=(zb0, zb1, 0, S.BP12_D / 2),
        insert=(zb0, zb1, 0, S.INSERT_BORE_D / 2),
        cork=(zb0 + S.HALO_Z_CORK, zb0, S.HALO_RING_ID / 2, S.HALO_RING_OD / 2),
        alu=(zb0 + S.HALO_Z_ALU, zb0 + S.HALO_Z_CORK, S.HALO_RING_ID / 2, S.HALO_RING_OD / 2),
        strip=(zb0 + S.HALO_Z_STRIP, zb0 + S.HALO_Z_ALU, S.HALO_STRIP_R - S.LED_W / 2, S.HALO_STRIP_R + S.LED_W / 2),
        screw_head=(zb0 + S.HALO_Z_ALU - hh, zb0 + S.HALO_Z_ALU, S.HALO_SCREW_R - hd / 2, S.HALO_SCREW_R + hd / 2),
        screw_shank=(zb0 + S.HALO_Z_ALU, zb0 + S.HALO_Z_ALU + S.HALO_SCREW_L, S.HALO_SCREW_R - S.HALO_SCREW_MAJOR_D / 2,
                     S.HALO_SCREW_R + S.HALO_SCREW_MAJOR_D / 2),
        pad=(zb1 - S.PAD_TARGET_DEPTH, zr0, S.PAD_R_OUT - S.PAD_D / 2, S.PAD_R_OUT + S.PAD_D / 2),
        pad_in=(zb1 - S.PAD_TARGET_DEPTH, zr0, S.PAD_R_IN - S.PAD_D / 2, S.PAD_R_IN + S.PAD_D / 2),
        centre_ring=(zb1, zr0, S.CENTER_RING[1] / 2, S.CENTER_RING[0] / 2),
        record=(zr0, zr1, S.REC_HOLE_D / 2, S.REC12_D / 2),
        pet=(zr1, zp1, S.PET_WASHER[1] / 2, S.PET_WASHER[0] / 2),
        felt=(zp1, zc + S.CAP12_RECESS_H, S.FELT_WASHER[1] / 2, S.FELT_WASHER[0] / 2),
        stud=(zc - S.CAP12_STUD_L, zc, 0, S.STUD_14_20_D / 2),
        cap=(zc, ztip, 0, S.CAP12_D / 2),
    )
    return {k: tuple(round(float(v), 3) for v in t) for k, t in n.items()}


def annotate():
    from PIL import Image, ImageDraw, ImageFont
    N = side_cut_numbers()
    th = json.load(open(os.path.join(HERE, "thermal-results.json")))
    fin = th["final_name"]
    f_of = lambda c: c * 9 / 5 + 32
    t_norm, t_worst = f_of(th["normal"][fin]["record_C"]), f_of(th["worst"][fin]["record_C"])
    room_n, room_w = f_of(th["assumptions"]["cases"]["normal"]["room_C"]), f_of(th["assumptions"]["cases"]["worst"]["room_C"])
    BG, INK, MUTE, ACC, PAN = (244, 241, 235, 255), (26, 26, 28, 255), (105, 102, 96, 255), (196, 84, 40, 255), (232, 228, 220, 255)
    W = 3200
    img = Image.open(os.path.join(E.OUT, "lit_fix_raw.png")).convert("RGBA")
    A_ = json.load(open(os.path.join(E.OUT, "lit_fix_raw.png.anchors.json")))
    y_img, y_sec, sh = 150, 1760, 1300
    y_leg = y_sec + sh + 120
    H = y_leg + 6 * 150 + 50
    cv = Image.new("RGBA", (W, H), BG); cv.alpha_composite(img, (0, y_img)); d = ImageDraw.Draw(cv)
    F = "/System/Library/Fonts/Helvetica.ttc"
    f_t = ImageFont.truetype(F, 84, index=1); f_s = ImageFont.truetype(F, 40); f_n = ImageFont.truetype(F, 44, index=1)
    f_h = ImageFont.truetype(F, 46, index=1); f_b = ImageFont.truetype(F, 38); f_x = ImageFont.truetype(F, 34)
    d.text((90, 70), "Spindle: heat-safe layout", font=f_t, fill=INK)
    d.text((92, 172), "This is the design now, for the plain cap and the lit cap. The LED strip is on the back of the backplate, on an aluminium ring and a cork ring.", font=f_s, fill=MUTE)

    def bubble(x, y, n, r=40):
        d.ellipse((x - r, y - r, x + r, y + r), fill=ACC, outline=(255, 255, 255, 255), width=4)
        tw = d.textlength(n, font=f_n); d.text((x - tw / 2, y - 25), n, font=f_n, fill=(255, 255, 255, 255))
    for n, (x, y, dx, dy) in A_.items():
        y += y_img
        d.line((x, y, x + dx, y + dy), fill=ACC, width=5); d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=ACC); bubble(x + dx, y + dy, n)
    # ---- side cut, centre to edge. Every bar comes from side_cut_numbers() ----
    d.rounded_rectangle((70, y_sec, W - 70, y_sec + sh), radius=26, fill=PAN, outline=(200, 195, 186, 255), width=3)
    d.text((110, y_sec + 30), "Side cut, from the centre out to the top edge (depth stretched so the thin parts show)", font=f_h, fill=INK)
    sx, sy = 30.0, 4.3                      # px per mm: distance from wall, radius
    x0, r_hi = 770, 160.0
    ybase = y_sec + sh - 300                # y of the centre line (r = 0)
    X = lambda mm: x0 + mm * sx
    Y = lambda r: ybase - r * sy
    tip = N["cap"][1]

    def bar(key, fill, outline=None):
        z0, z1, r0, r1 = N[key]
        d.rectangle((X(z0), Y(r1), X(z1), Y(r0)), fill=fill, outline=outline)
    d.rectangle((X(-7), Y(r_hi), X(0), Y(0)), fill=(205, 196, 180, 255))
    d.text((X(-7) + 36, Y(156)), "WALL", font=f_h, fill=MUTE)
    bar("hub", (96, 100, 108, 255))
    bar("plate", (176, 180, 186, 255), (110, 114, 120, 255))
    bar("post", (200, 204, 210, 255))
    bar("backplate", (40, 40, 44, 255))
    bar("insert", (206, 160, 70, 255))
    bar("cork", (150, 104, 62, 255))
    bar("alu", (196, 200, 206, 255), (120, 124, 130, 255))
    bar("strip", (255, 176, 60, 255))
    bar("screw_shank", (168, 172, 178, 255))
    bar("screw_head", (168, 172, 178, 255), (110, 114, 120, 255))
    bar("pad", (176, 160, 130, 255)); bar("pad_in", (176, 160, 130, 255)); bar("centre_ring", (176, 160, 130, 255))
    bar("record", (12, 12, 14, 255))
    bar("pet", (150, 190, 220, 255))
    bar("felt", (176, 160, 130, 255))
    bar("stud", (214, 218, 224, 255), (120, 124, 130, 255))
    cz0, cz1, _, cr = N["cap"]
    d.pieslice((X(cz0) - (X(cz1) - X(cz0)), Y(cr), X(cz1), Y(-cr)), -90, 0, fill=(214, 218, 224, 255), outline=(120, 124, 130, 255))  # dome
    sz0, sz1, sr0, sr1 = N["strip"]
    rmid = (sr0 + sr1) / 2
    for rr in (rmid - 2, rmid, rmid + 2):                                    # light toward the wall
        d.line((X(sz0 - 0.4), Y(rr), X(2.5), Y(rr + (rr - rmid) * 9)), fill=(255, 176, 60, 255), width=4)
    d.polygon([(X(2.8), Y(rmid) - 12), (X(2.8), Y(rmid) + 12), (X(0.5), Y(rmid))], fill=(255, 176, 60, 255))
    for xx in range(int(X(-7)), int(X(58)), 36):                             # centre line
        d.line((xx, Y(0), xx + 20, Y(0)), fill=MUTE, width=3)
    d.text((X(58) + 10, Y(0) - 20), "centre of the record", font=f_x, fill=MUTE)

    def note(key, text, tx, ty, fz=0.5, fr=0.5):
        z0, z1, r0, r1 = N[key]
        zmm, r = z0 + (z1 - z0) * fz, r0 + (r1 - r0) * fr
        d.line((X(zmm), Y(r), tx, ty + 20), fill=INK, width=3); d.ellipse((X(zmm) - 7, Y(r) - 7, X(zmm) + 7, Y(r) + 7), fill=INK)
        d.text((tx + (12 if tx > X(zmm) else -12 - d.textlength(text, font=f_x)), ty), text, font=f_x, fill=INK)
    lx, rx = X(-7) - 40, X(tip) + 190
    note("alu", f"aluminium ring, {N['alu'][1] - N['alu'][0]:.0f} mm", lx, Y(146), fr=0.85)
    note("strip", "LED strip, shining at the wall", lx, Y(130))
    note("cork", f"cork ring, {N['cork'][1] - N['cork'][0]:.1f} mm", lx, Y(114), fr=0.3)
    note("screw_head", "one of 4 small screws", lx, Y(98), fz=0.3)
    note("hub", "hub (sets the 1 inch gap)", lx, Y(62), fr=0.85)
    note("plate", "steel wall plate (inside the hub)", lx, Y(42))
    note("post", "post the hub twists onto", lx, Y(22))
    note("record", "record, its edge overhangs the plate", rx, Y(150), fr=0.96)
    note("pad", "felt pad", rx, Y(132))
    note("backplate", "1/2 in MDF backplate", rx, Y(114), fz=0.6, fr=0.62)
    note("cap", "chrome cap", rx, Y(64), fr=0.3)
    note("pet", "clear washer and felt washer", rx, Y(46), fr=0.8)
    note("stud", "cap's screw, into the brass insert", rx, Y(28), fz=0.35)
    d.text((rx + 12, Y(98)), f"Record in an {room_n:.0f}°F room: {t_norm:.0f}°F.", font=f_x, fill=ACC)
    d.text((rx + 12, Y(98) + 44), f"Worst case stacked, {room_w:.0f}°F room: {t_worst:.0f}°F.", font=f_x, fill=ACC)
    d.text((rx + 12, Y(98) + 88), "Calculated, not yet measured.", font=f_x, fill=ACC)
    # distances from the wall
    yd = ybase + 60
    rows = ((N["strip"][0], "face of the LED strip"), (N["hub"][1], "back of the backplate (wall plate + hub)"),
            (N["record"][1], "front of the record"), (tip, "tip of the chrome cap (furthest point)"))
    for k, (mm, lab) in enumerate(rows):
        y = yd + k * 46
        d.line((X(0), y, X(mm), y), fill=INK, width=4)
        d.line((X(0), y - 12, X(0), y + 12), fill=INK, width=4); d.line((X(mm), y - 12, X(mm), y + 12), fill=INK, width=4)
        d.text((X(tip) + 30, y - 20), f"{mm / 25.4:.2f} in  {lab}", font=f_x, fill=INK)
        d.line((X(mm), Y(0), X(mm), y), fill=(150, 146, 140, 255), width=2)
    d.text((X(0), yd + len(rows) * 46 + 4),
           f"Sizes used: rings {N['alu'][2] / 25.4:.2f} to {N['alu'][3] / 25.4:.2f} in from the centre, strip {sr0 / 25.4:.2f} to {sr1 / 25.4:.2f} in, "
           f"backplate edge {N['backplate'][3] / 25.4:.2f} in, record edge {N['record'][3] / 25.4:.2f} in.", font=f_x, fill=MUTE)
    # legend
    d.line((90, y_leg - 55, W - 90, y_leg - 55), fill=(200, 195, 186, 255), width=3)
    colw = (W - 180) // 2

    def wrap(text, font, maxw):
        lines, cur = [], ""
        for w_ in text.split():
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w_
        return lines + [cur]
    for i, (n, title, line) in enumerate(LEGEND):
        col, row = divmod(i, 6)
        x, y = 90 + col * colw, y_leg + row * 150
        bubble(x + 40, y + 44, n)
        d.text((x + 105, y), title, font=f_h, fill=ACC if n in ("4", "5", "6") else INK)
        for j, ln in enumerate(wrap(line, f_b, colw - 150)[:2]):
            d.text((x + 105, y + 54 + j * 42), ln, font=f_b, fill=MUTE)
    out = os.path.join(E.OUT, "spindle-heat-safe-layout.png")
    cv.convert("RGB").save(out); print("saved", out, cv.size)
    json.dump(dict(side_cut_mm=N, record_F_normal=round(t_norm, 1), record_F_worst=round(t_worst, 1)),
              open(os.path.join(E.TMP, "side-cut-numbers.json"), "w"), indent=1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export()
    elif len(sys.argv) > 1 and sys.argv[1] == "annotate":
        annotate()
    elif len(sys.argv) > 1 and sys.argv[1] == "numbers":
        print(json.dumps(side_cut_numbers(), indent=1))
    elif "--" in sys.argv:
        E.render(sys.argv[sys.argv.index("--") + 1])
