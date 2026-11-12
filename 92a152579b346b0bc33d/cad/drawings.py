"""2D drawings (PDF + PNG) straight from the CadQuery geometry: section views through the solid plus
projected plan views, with dimension callouts driven by the same parameters as the 3D model."""
import math
import textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import cadquery as cq
import sconce_cad as S

DATE = "2026-11-11"
SHEET_LOG = []      # one entry per sheet: where the notes and the title block ended (build_all asserts they are inside the border)
LW = 0.9


def _edges_xy(edges, proj=("x", "y"), n=48):
    out = []
    idx = {"x": 0, "y": 1, "z": 2}
    for e in edges:
        try:
            pts = e.positions([i / (n - 1) for i in range(n)])
        except Exception:
            continue
        arr = np.array([(p.x, p.y, p.z) for p in pts])
        out.append(arr[:, [idx[proj[0]], idx[proj[1]]]])
    return out


def section_polylines(solid, plane="XZ", offset=0.0):
    """Intersect with a thin slab and return the section outline polylines in 2D (u, v)."""
    if plane == "XZ":
        slab = cq.Workplane("XY").box(2000, 0.02, 2000).translate((0, offset, 0))
        face_sel, proj = ">Y", ("x", "z")
    elif plane == "YZ":
        slab = cq.Workplane("XY").box(0.02, 2000, 2000).translate((offset, 0, 0))
        face_sel, proj = ">X", ("y", "z")
    else:
        slab = cq.Workplane("XY").box(2000, 2000, 0.02).translate((0, 0, offset))
        face_sel, proj = ">Z", ("x", "y")
    if hasattr(solid, "val"):
        solid = solid.val()
    try:
        sec = solid.intersect(slab.val())
        if sec.Volume() < 1e-6:
            return []
        faces = cq.Workplane("XY").add(sec).faces(face_sel)
        return _edges_xy(faces.edges().vals(), proj)
    except Exception:
        return []


def plan_polylines(solid, proj=("x", "y"), zmin=None, zmax=None):
    edges = solid.edges().vals()
    if zmin is not None or zmax is not None:
        keep = []
        for e in edges:
            bb = e.BoundingBox()
            if zmin is not None and bb.zmax < zmin - 1e-6:
                continue
            if zmax is not None and bb.zmin > zmax + 1e-6:
                continue
            keep.append(e)
        edges = keep
    return _edges_xy(edges, proj)


def draw_polys(ax, polys, color="k", lw=LW, ls="-"):
    for p in polys:
        ax.plot(p[:, 0], p[:, 1], color=color, lw=lw, ls=ls, solid_capstyle="round")


def dim_h(ax, x0, x1, y, text, off=0.0, fs=6.5, ext_from=None):
    """Horizontal dimension between x0 and x1 at height y."""
    ax.annotate("", xy=(x0, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", lw=0.6, color="#1f4e79", shrinkA=0, shrinkB=0))
    if ext_from is not None:
        for x in (x0, x1):
            ax.plot([x, x], [ext_from, y + (1.5 if y > ext_from else -1.5)], color="#1f4e79", lw=0.4)
    ax.text((x0 + x1) / 2, y + off, text, ha="center", va="bottom" if off >= 0 else "top", fontsize=fs, color="#1f4e79",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))


def dim_v(ax, y0, y1, x, text, off=0.0, fs=6.5, ext_from=None):
    ax.annotate("", xy=(x, y0), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", lw=0.6, color="#1f4e79", shrinkA=0, shrinkB=0))
    if ext_from is not None:
        for y in (y0, y1):
            ax.plot([ext_from, x + (1.5 if x > ext_from else -1.5)], [y, y], color="#1f4e79", lw=0.4)
    ax.text(x + off, (y0 + y1) / 2, text, ha="left" if off >= 0 else "right", va="center", fontsize=fs, color="#1f4e79",
            rotation=90, bbox=dict(facecolor="white", edgecolor="none", pad=0.6))


def leader(ax, xy, xytext, text, fs=6.5):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs, color="#1f4e79", ha="left", va="center",
                arrowprops=dict(arrowstyle="-|>", lw=0.6, color="#1f4e79", shrinkA=0, shrinkB=0),
                bbox=dict(facecolor="white", edgecolor="none", pad=0.6))



BORDER_Y0 = 0.01
TEXT_FLOOR = 0.016           # lowest y any note / title-block line may reach (border is at 0.01)
NOTES_TOP = 0.192            # views start at y >= 0.20


def _fit(make_lines, top, step_per_pt, fonts, part_no, what):
    """Largest font whose wrapped lines fit between `top` and TEXT_FLOOR. Raises if even the smallest does not fit, so a
    sheet with clipped notes can never be exported again (review M9: the tolerance line was below the border)."""
    for fs in fonts:
        lines = make_lines(fs)
        step = step_per_pt * fs
        if top - len(lines) * step >= TEXT_FLOOR:
            return fs, step, lines
    raise AssertionError(f"{part_no}: {what} does not fit inside the sheet border ({len(lines)} lines at {fs} pt); shorten it")


def sheet(title, part_no, material, finish, notes, scale_txt, rev="A", size=(16.5, 11.7), supersedes=None):
    fig = plt.figure(figsize=size)
    fig.patch.set_facecolor("white")
    ax0 = fig.add_axes([0, 0, 1, 1]); ax0.set_axis_off(); ax0.set_xlim(0, 1); ax0.set_ylim(0, 1)
    ax0.add_patch(plt.Rectangle((BORDER_Y0, BORDER_Y0), 0.98, 0.98, fill=False, lw=1.2))

    # ---- title block: height follows the text, so nothing can fall below the border
    def tb_lines(fs):
        w = int(95 * 7.4 / fs)
        head = f"PART NO: {part_no}      REV: {rev}      DATE: {DATE}"
        if supersedes:
            head += f"      SUPERSEDES: {supersedes} (do not build or quote)"
        out = textwrap.wrap(head, w)
        out += textwrap.wrap("MATERIAL: " + material, w)
        out += textwrap.wrap("FINISH: " + finish, w)
        out += ["UNITS: mm [in]   THIRD-ANGLE PROJECTION   " + scale_txt,
                "GENERAL TOLERANCES: x.x +/-0.3   x.xx +/-0.1   angles +/-0.5 deg   unless noted"]
        return out
    tb_top_max = NOTES_TOP + 0.003
    fs, step, lines = _fit(tb_lines, tb_top_max - 0.03, 0.0155 / 7.4, (7.4, 6.8, 6.2, 5.6, 5.0), part_no, "title block")
    tb_h = min(tb_top_max - BORDER_Y0, 0.03 + len(lines) * step + 0.008)
    tb_top = BORDER_Y0 + tb_h
    ax0.add_patch(plt.Rectangle((0.56, BORDER_Y0), 0.43, tb_h, fill=False, lw=1.0))
    ax0.text(0.57, tb_top - 0.004, f"RECORD SCONCE  |  {title}", fontsize=11.5 if len(title) < 52 else 9.5, weight="bold", va="top", family="DejaVu Sans")
    y = tb_top - 0.03
    for ln in lines:
        ax0.text(0.57, y, ln, fontsize=fs, va="top")
        y -= step
    tb_bottom = y + step * 0.25

    # ---- notes
    def note_lines(fs):
        w = int(135 * 7.0 / fs)
        out = []
        for i, n in enumerate(notes):
            for j, ln in enumerate(textwrap.wrap(n, w)):
                out.append((f"{i + 1}. " if j == 0 else "    ") + ln)
        return out
    nfs, nstep, nlines = _fit(note_lines, NOTES_TOP - 0.017, 0.0145 / 7.0, (7.0, 6.5, 6.0, 5.5, 5.0), part_no, "notes block")
    ax0.text(0.02, NOTES_TOP, "NOTES:", fontsize=8.5, weight="bold", va="top")
    y = NOTES_TOP - 0.017
    for ln in nlines:
        ax0.text(0.02, y, ln, fontsize=nfs, va="top")
        y -= nstep
    SHEET_LOG.append(dict(part=part_no, rev=rev, notes_pt=nfs, notes_lowest_y=round(y + nstep * 0.25, 4),
                          title_block_pt=fs, title_block_lowest_y=round(tb_bottom, 4), has_tolerance_line=True))
    return fig


def view(fig, rect, polys_list, title=None, equal=True, pad=8.0, hatch=None):
    ax = fig.add_axes(rect)
    ax.set_facecolor("white")
    allp = np.vstack([p for item in polys_list for p in item[0]])
    for item in polys_list:
        polys, color, lw, ls = item
        draw_polys(ax, polys, color=color, lw=lw, ls=ls)
    xmin, ymin = allp.min(0); xmax, ymax = allp.max(0)
    ax.set_xlim(xmin - pad, xmax + pad); ax.set_ylim(ymin - pad, ymax + pad)
    if equal:
        ax.set_aspect("equal", adjustable="datalim")
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=9, loc="left", pad=2)
    return ax


def mm_in(v):
    return f"{v:.2f} [{v / 25.4:.3f}]"


def save(fig, base):
    fig.savefig(base + ".pdf", facecolor="white")
    fig.savefig(base + ".png", dpi=130, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- drawings per part

def draw_backplate(out_base, d=S.BP12_D, part_no="RS-BP-12-MDF"):
    big = d > 200
    bp = S.backplate(d, pads_out=big)
    R = d / 2
    ring_spec = S.CENTER_RING if big else S.CENTER_RING7
    n_pads = 6 if big else 3
    back = S.halo_layout(d) == "back"          # 12 in rev C: heat-safe halo, no rim rabbet. 7 in rev B: rim strip, unchanged
    if back:
        halo_notes = [
            "REV C (2026-11-11): NO rim rabbet and NO rim notch. The rim is a plain square edge, full thickness. The LED strip is no longer on this part: it rides on the aluminium ring RS-HR-12 over the cork ring RS-CK-12, which screw to the BACK face (heat-safe layout, see RS-ASM-12-MDF).",
            "3x #8 flat-head countersinks on the FRONT face (hidden by the record) fasten the hub from the front.",
            f"BACK face: 4x pilot D {S.HALO_PILOT_D} x {S.HALO_PILOT_DEPTH:.1f} +0.5/-0 deep on R {S.HALO_SCREW_R} at {'/'.join(str(a) for a in S.HALO_SCREW_ANGLES)} deg for the #4 x 3/8 heat-ring screws. BLIND: {S.BP_T - S.HALO_PILOT_DEPTH:.1f} of MDF must stay in front of each pilot, no mark on the front face.",
            f"BACK face: pocket {S.BP_JACK_POCKET[0]:.0f} x {S.BP_JACK_POCKET[1]:.0f} x {S.BP_JACK_POCKET[2]} at y=+{S.JACK_Y:.0f} over the hub's splice cavity; lead channel {S.BACK_CHAN_W:.0f} wide x {S.BACK_CHAN_D:.0f} deep at 6 o'clock from R {S.BACK_CHAN_R0:.0f} to R {S.BACK_CHAN_R1:.0f} ONLY (it stops {S.HALO_RING_ID / 2 - S.BACK_CHAN_R1:.0f} short of the cork ring, ID R {S.HALO_RING_ID / 2:.0f}).",
            "Break all edges 0.5 max. Flatness 0.3 over the full front face (the record lies on it) and over the back face band R 100 to R 130 (the cork ring lies on it). No tear-out on the front face or rim."]
        finish = "Matte black, 2 coats, ALL surfaces including the rim edge (sealed MDF)"
        rev, sup = "C", "rev A, B (rim rabbet + rim notch; do not cut)"
    else:
        halo_notes = [
            "Rim rabbet carries an 8 mm LED strip (6 W max, 4 W class preferred), LEDs facing outward; rabbet floor smooth and painted. NOTE: this 7 in part is NOT on the heat-safe back-face layout of the 12 in rev C plate (no room for the ring outside the hub); see cad/FIXES-heat-layout.md.",
            "3x #8 flat-head countersinks on the FRONT face (hidden by the record) fasten the hub from the front.",
            f"Rear pocket {S.BP_JACK_POCKET[0]:.0f} x {S.BP_JACK_POCKET[1]:.0f} x {S.BP_JACK_POCKET[2]} at y=+{S.JACK_Y:.0f} sits over the hub's splice cavity; rear channel 6 x 4 routes the LED leads to the hub.",
            "Break all edges 0.5 max. Flatness 0.3 over the full front face (the record lies on it). No tear-out on the front face or rim."]
        finish = "Matte black, 2 coats, ALL surfaces including the rim rabbet and the notch (sealed MDF: LED tape lets go of raw MDF)"
        rev, sup = "B", "rev A"
    fig = sheet(f"BACKPLATE {d / 25.4:.1f} in, CNC MDF", part_no,
                f"1/2 in MDF, thickness {S.BP_T:.2f} +/-0.15 MEASURED (reject sheet outside it; nominal 1/2 in Baltic birch is 12.0 and is NOT acceptable), both faces flat",
                finish,
                [f"E-Z Lok 400-4 brass insert, 1/4-20, in the 25/64 in bore (CA glue in the bore only): driven flush to 0.2 BELOW the FRONT face, never proud (the centre backing ring lies over it). Wipe the insert's BACK end clean: it is an electrical contact on the lit sconce.",
                 f"CENTRE BACKING RING: {ring_spec[0]:.2f} OD x {ring_spec[1]:.1f} ID x {ring_spec[2]} adhesive felt (same blank as the cap felt) bonded on the FRONT face concentric with the bore, inside the scored witness circle D {ring_spec[0] + S.CENTER_WITNESS_CLR:.1f} ({S.CENTER_WITNESS_W} wide x {S.CENTER_WITNESS_DEPTH} deep). It backs the record directly behind the cap so the clamp cannot dish it.",
                 f"{n_pads}x felt pad targets D {S.PAD_D + 0.6:.1f} x {S.PAD_TARGET_DEPTH} deep for 1/2 in x 1/16 in felt pads. Pads sit IN the targets: record seat plane = {S.REC_SEAT_H:.1f} above the front face, coplanar with the loaded centre ring.",
                 ] + halo_notes,
                "SCALE: as shown (not to print scale)", rev=rev, supersedes=sup)
    front = plan_polylines(bp, ("x", "y"))
    ax = view(fig, [0.03, 0.22, 0.50, 0.74], [(front, "k", 0.7, "-")], title="FRONT VIEW (record side)")
    dim_h(ax, -R, R, -R - 14, f"D {mm_in(d)}", off=1.0, ext_from=-R)
    leader(ax, (0, S.INSERT_BORE_D / 2), (R * 0.25, R * 0.55), f"THRU D {S.INSERT_BORE_D:.2f} [25/64] +0.1/-0\nfor E-Z Lok 400-4 insert")
    leader(ax, ((ring_spec[0] + S.CENTER_WITNESS_CLR) / 2, 0), (R * 0.45, R * 0.22),
           f"witness circle D {ring_spec[0] + S.CENTER_WITNESS_CLR:.1f}, scored {S.CENTER_WITNESS_DEPTH} deep:\ncentre backing ring {ring_spec[0]:.2f} x {ring_spec[1]:.1f} x {ring_spec[2]} goes inside it")
    x, y = S.pol(S.HUB_SCREW_R, 330)
    leader(ax, (x, y), (R * 0.55, -R * 0.35), f"3x #8 CSK 90 deg, D {S.HUB_SCREW_CLR_D} thru,\nCSK D {S.HUB_SCREW_CSK_D}, on R {S.HUB_SCREW_R} @ 90/210/330 deg")
    if big:
        x, y = S.pol(S.PAD_R_OUT, 210)
        leader(ax, (x, y), (-R * 0.95, -R * 0.9), f"3x felt target D {S.PAD_D + 0.6:.1f} x {S.PAD_TARGET_DEPTH} +/-0.1 deep\non R {S.PAD_R_OUT:.1f} @ 90/210/330")
    x, y = S.pol(S.PAD_R_IN, 210)
    leader(ax, (x, y), (-R * 0.95, -R * 0.55), f"3x felt target D {S.PAD_D + 0.6:.1f} x {S.PAD_TARGET_DEPTH} +/-0.1 deep\non R {S.PAD_R_IN:.2f} @ 90/210/330")
    if back:
        x, y = S.pol(S.HALO_SCREW_R, 315)
        leader(ax, (x, y), (R * 0.42, -R * 0.93), f"4x pilot D {S.HALO_PILOT_D} x {S.HALO_PILOT_DEPTH:.1f} deep, BACK face (blind),\non R {S.HALO_SCREW_R} @ {'/'.join(str(a) for a in S.HALO_SCREW_ANGLES)} deg")
        leader(ax, (S.BACK_CHAN_W / 2, -(S.BACK_CHAN_R0 + S.BACK_CHAN_R1) / 2), (-R * 0.5, -R * 0.2),
               f"BACK face lead channel {S.BACK_CHAN_W:.0f} wide x {S.BACK_CHAN_D:.0f} deep,\nR {S.BACK_CHAN_R0:.0f} to R {S.BACK_CHAN_R1:.0f} at 6 o'clock")
        sec = section_polylines(bp.val(), "YZ", 0.0)
        ax2 = view(fig, [0.55, 0.52, 0.43, 0.42], [(sec, "k", 0.9, "-")], title="SECTION A-A (x=0): plain rim, no rabbet (rev C)")
        dim_v(ax2, 0, S.BP_T, -R * 0.3, f"{S.BP_T:.2f} +/-0.15 [{S.BP_T / 25.4:.3f}]", off=-2)
        leader(ax2, (-R, S.BP_T / 2), (-R * 0.95, S.BP_T + 18), "rim: plain square edge,\nno rabbet, no notch")
        leader(ax2, (S.JACK_Y, 2), (R * 0.3, S.BP_T + 18), f"rear pocket {S.BP_JACK_POCKET[0]} x {S.BP_JACK_POCKET[1]} x {S.BP_JACK_POCKET[2]} deep @ y=+{S.JACK_Y:.0f}")
        dim_h(ax2, -S.BACK_CHAN_R1, -S.BACK_CHAN_R0, -9, f"lead channel R {S.BACK_CHAN_R0:.0f} to R {S.BACK_CHAN_R1:.0f}, {S.BACK_CHAN_D:.0f} deep", off=-0.8, ext_from=0)
        # section through one pilot (rotate the 45 deg pilot onto +X, cut XZ), outer 50 mm only
        bpr = bp.rotate((0, 0, 0), (0, 0, 1), -S.HALO_SCREW_ANGLES[0])
        secp = [q[q[:, 0] > R - 45] for q in section_polylines(bpr.val(), "XZ", 0.0)]
        secp = [q for q in secp if len(q) > 1]
        ax3 = view(fig, [0.55, 0.20, 0.43, 0.30], [(secp, "k", 1.1, "-")],
                   title=f"DETAIL B-B: radial cut through a heat-ring pilot ({S.HALO_SCREW_ANGLES[0]} deg), back face down", pad=4)
        dim_v(ax3, 0, S.HALO_PILOT_DEPTH, S.HALO_SCREW_R - 5, f"{S.HALO_PILOT_DEPTH:.1f} +0.5/-0", off=-1.0)
        dim_v(ax3, S.HALO_PILOT_DEPTH, S.BP_T, S.HALO_SCREW_R + 5, f"{S.BP_T - S.HALO_PILOT_DEPTH:.1f} min left", off=1.0)
        dim_h(ax3, S.HALO_SCREW_R, R, -2.5, f"{R - S.HALO_SCREW_R:.2f} to the rim (pilot on R {S.HALO_SCREW_R})", off=-0.5)
        leader(ax3, (S.HALO_SCREW_R, 1.5), (S.HALO_SCREW_R + 7, 5.0), f"pilot D {S.HALO_PILOT_D}, blind")
        ax3.text(R - 12, S.BP_T + 0.6, "FRONT face (record side)", fontsize=6.5, color="#1f4e79", ha="right", va="bottom")
        ax3.text(R - 12, -0.6, "BACK face", fontsize=6.5, color="#1f4e79", ha="right", va="top")
        save(fig, out_base)
        return
    leader(ax, (0, -R + 1), (R * 0.2, -R * 0.78), f"lead notch {S.NOTCH_W} wide at 6 o'clock,\nrabbet floor to back face")
    # section through x=0 (YZ) to show the rabbet and the rear pocket
    sec = section_polylines(bp.val(), "YZ", 0.0)
    ax2 = view(fig, [0.55, 0.52, 0.43, 0.42], [(sec, "k", 0.9, "-")], title="SECTION A-A (x=0), rim detail enlarged below")
    dim_v(ax2, 0, S.BP_T, R + 16, f"{S.BP_T:.2f} +/-0.15 [{S.BP_T / 25.4:.3f}]", off=2, ext_from=R)
    leader(ax2, (-R + 0.5, S.BP_T / 2), (-R * 0.7, S.BP_T + 18), f"rim rabbet {S.RABBET_W} wide x {S.RABBET_DEPTH} +/-0.2 deep,\ncentred on the rim")
    leader(ax2, (S.JACK_Y, 2), (R * 0.3, S.BP_T + 18), f"rear pocket {S.BP_JACK_POCKET[0]} x {S.BP_JACK_POCKET[1]} x {S.BP_JACK_POCKET[2]} deep @ y=+{S.JACK_Y:.0f}")
    # rim detail
    sec_rim = [p for p in sec if p[:, 0].max() < -R + 40]
    ax3 = view(fig, [0.55, 0.20, 0.43, 0.30], [(sec_rim, "k", 1.1, "-")], title="DETAIL: rim rabbet + 6 o'clock lead notch (x=0 cut)", pad=3)
    z0 = (S.BP_T - S.RABBET_W) / 2
    dim_v(ax3, z0, z0 + S.RABBET_W, -R - 6, f"{S.RABBET_W}", off=-1.5)
    dim_h(ax3, -R, -R + S.RABBET_DEPTH, S.BP_T + 2.5, f"{S.RABBET_DEPTH}", off=0.5)
    dim_h(ax3, -R + S.RABBET_DEPTH, -60, -2.5, f"rear channel {S.BACK_CHAN_W} wide x {S.BACK_CHAN_D} deep to R60", off=-0.5)
    save(fig, out_base)


def draw_halo_ring(out_base, which="alu"):
    """RS-HR-12 (aluminium heat ring) and RS-CK-12 (cork ring): same outline, different hole size and thickness."""
    Ro, Ri = S.HALO_RING_OD / 2, S.HALO_RING_ID / 2
    angs = "/".join(str(a) for a in S.HALO_SCREW_ANGLES)
    if which == "alu":
        shape, part_no, t, hole = S.heat_ring(), "RS-HR-12", S.HEAT_RING_T, S.HEAT_RING_HOLE_D
        title = "HEAT RING 12 in, flat aluminium (spreads the LED strip's heat)"
        material = f"5052-H32 aluminium sheet, {t:.1f} mm [0.040 in]. 6061-T6 or 3003-H14 of the same thickness acceptable (tell us)"
        finish = "Bare mill finish, both faces clean and oil-free (the LED strip's tape and the cork's adhesive bond to it). No anodise, no paint, no powder coat"
        notes = [f"Flat ring, laser cut: OD {S.HALO_RING_OD:.1f}, ID {S.HALO_RING_ID:.1f}, 4x D {hole} thru on R {S.HALO_SCREW_R} at {angs} deg. Nothing else. DXF RS-HR-12.dxf is 1:1, mm.",
                 "Deburr BOTH faces and BOTH edges, break edges 0.2: the LED leads cross the inner edge and a hand will hold it. No heat tint, no dross. Flat within 0.5 over the full ring.",
                 f"Where it goes: on the BACK of the 12 in MDF backplate RS-BP-12-MDF rev C, concentric, with the cork ring RS-CK-12 between it and the wood. The 8 mm LED strip sticks to the WALL-facing face, centred on R {S.HALO_STRIP_R:.0f} (R {S.HALO_STRIP_R - S.LED_W / 2:.0f} to R {S.HALO_STRIP_R + S.LED_W / 2:.0f}), LEDs toward the wall.",
                 f"Fastening: 4x #4 x 3/8 in pan-head screws (Type AB) through this ring and the cork into D {S.HALO_PILOT_D} pilots in the backplate. Snug only: stop when the head touches, do not crush the cork.",
                 "Assembly order: (1) lay the cork on this ring, holes lined up (adhesive face to the ring if the cork has one); (2) wipe the other face with isopropyl alcohol and lay the strip on it, joint and leads at 6 o'clock; (3) sleeve the solder joints and the leads with heat-shrink where they cross the inner edge (the ring is bare metal, the strip is 12 V); (4) screw the ring to the backplate.",
                 "Same ring on the plain-cap and the lit-cap 12 in sconce. Not used on the 7 in sconce or on the aluminium-backplate variants."]
    else:
        shape, part_no, t, hole = S.cork_ring(), "RS-CK-12", S.CORK_RING_T, S.CORK_RING_HOLE_D
        title = "CORK RING 12 in (insulates the wood from the warm aluminium ring)"
        material = f"Cork sheet, fine grain, {t:.1f} mm [1/16 in] +/-0.2. Plain composition cork. Pressure-sensitive adhesive on ONE face preferred; cork with no adhesive is acceptable (the 4 ring screws hold it). 1.5 mm sheet acceptable"
        finish = "None. Natural cork. Adhesive liner, if any, left on"
        notes = [f"Flat ring, die cut, knife cut or laser cut: OD {S.HALO_RING_OD:.1f}, ID {S.HALO_RING_ID:.1f}, 4x D {hole} thru on R {S.HALO_SCREW_R} at {angs} deg (punch the 4 holes; they line up with the aluminium ring's). DXF RS-CK-12.dxf is 1:1, mm.",
                 "Tolerance on OD, ID and hole position +/-0.5 (soft part). No cracks, no missing chunks wider than 2 mm at any edge. May be supplied in up to 4 butt-jointed segments if a 260 mm ring does not nest on your sheet (tell us).",
                 f"Where it goes: between the aluminium heat ring RS-HR-12 and the BACK face of the MDF backplate RS-BP-12-MDF rev C. If it has an adhesive face, that face goes on the ALUMINIUM. The plain face lies on the painted MDF and is held by the 4 ring screws.",
                 f"Why it is there: {t:.1f} mm of cork is a much poorer heat path than wood, so less of the strip's heat reaches the backplate and the record (cad/THERMAL.md).",
                 "Same ring on the plain-cap and the lit-cap 12 in sconce. Not used on the 7 in sconce or on the aluminium-backplate variants."]
    fig = sheet(title, part_no, material, finish, notes, "SCALE: as shown (not to print scale)", rev="A")
    plan = plan_polylines(shape, ("x", "y"), zmin=t - 1e-3)
    ax = view(fig, [0.03, 0.22, 0.52, 0.74], [(plan, "k", 0.8, "-")], title="PLAN (either face; the part is symmetric)", pad=30)
    dim_h(ax, -Ro, Ro, -Ro - 16, f"OD {mm_in(S.HALO_RING_OD)}", off=1.0, ext_from=-Ro)
    dim_h(ax, -Ri, Ri, 0, f"ID {mm_in(S.HALO_RING_ID)}", off=1.0)
    x, y = S.pol(S.HALO_SCREW_R, S.HALO_SCREW_ANGLES[0])
    leader(ax, (x, y), (Ro * 0.2, Ro * 0.35), f"4x D {hole} thru\non R {S.HALO_SCREW_R} [bolt circle D {2 * S.HALO_SCREW_R:.0f}]\n@ {angs} deg")
    dim_h(ax, Ri, Ro, Ro * 0.2, f"{Ro - Ri:.1f} wide", off=1.0)
    ax.plot([0, x], [0, y], color="#1f4e79", lw=0.4, ls="-.")
    ax.plot([-Ro - 8, Ro + 8], [0, 0], color="#1f4e79", lw=0.3, ls="-.")
    ax.plot([0, 0], [-Ro - 8, Ro + 8], color="#1f4e79", lw=0.3, ls="-.")
    # radial section through a hole, thickness to scale
    sr = shape.rotate((0, 0, 0), (0, 0, 1), -S.HALO_SCREW_ANGLES[0])
    sec = [q for q in section_polylines(sr.val(), "XZ", 0.0) if q[:, 0].min() > 0]
    ax2 = view(fig, [0.58, 0.60, 0.40, 0.30], [(sec, "k", 1.1, "-")], title=f"SECTION A-A: radial cut through a hole ({S.HALO_SCREW_ANGLES[0]} deg), to scale", pad=6)
    dim_h(ax2, Ri, Ro, -3.0, f"R {Ri:.1f} to R {Ro:.1f}", off=-0.5)
    dim_v(ax2, 0, t, Ro + 3, f"{t:.1f}", off=1.0)
    leader(ax2, (S.HALO_SCREW_R, t / 2), (S.HALO_SCREW_R + 3, t + 5), f"D {hole} on R {S.HALO_SCREW_R}")
    # where it sits in the stack (numbers only, printed from the parameters)
    ax3 = fig.add_axes([0.58, 0.20, 0.40, 0.36]); ax3.set_axis_off()
    ax3.text(0, 0.97, "WHERE IT SITS (12 in sconce, plain cap and lit cap)", fontsize=9, weight="bold", va="top")
    txt = (f"Stack on the backplate BACK face, toward the wall:\n"
           f"  cork ring RS-CK-12        {S.CORK_RING_T:.1f}\n"
           f"  aluminium ring RS-HR-12   {S.HEAT_RING_T:.1f}\n"
           f"  LED strip                 {S.LED_T:.1f}\n"
           f"  total at the strip        {S.HALO_STACK_H:.1f}   (at a screw head {S.HALO_STACK_H_AT_SCREW:.1f})\n"
           f"Gap behind the backplate     {S.HUB_T:.1f}\n"
           f"Strip face to the wall       {S.HUB_T - S.HALO_STACK_H:.1f}\n"
           f"Ring OD inside the backplate rim (R {S.BP12_D / 2:.2f})   {S.BP12_D / 2 - Ro:.2f}\n"
           f"Ring ID outside the hub (R {S.HUB_D / 2:.1f})              {Ri - S.HUB_D / 2:.1f}\n"
           f"Strip R {S.HALO_STRIP_R - S.LED_W / 2:.0f} to R {S.HALO_STRIP_R + S.LED_W / 2:.0f}; screw heads D {S.HALO_SCREW_HEAD[0]} on R {S.HALO_SCREW_R}\n"
           + (f"Mass (5052, 2.68 g/cm3)      {shape.val().Volume() * 2.68e-3:.0f} g" if which == "alu" else ""))
    ax3.text(0, 0.86, txt, fontsize=8, va="top", family="monospace")
    save(fig, out_base)


def halo_detail(fig, rect, parts):
    """Enlarged top-edge section of the heat-safe halo, the same picture on the plain and the lit assembly sheets.
    Section x=0 (u = radius, v = distance from the wall). Every dimension is measured on the section of the placed solids."""
    by = {n: p.val() for n, p, c, k in parts}
    col = {"backplate": "k", "cork_ring": "#8a5a2b", "heat_ring_alu": "#3b6ea5", "led_cob_strip": "#c46a00", "record": "#9b1c1c",
           "felt_pads": "#555555", "hub": "k"}
    layers, ext = [], {}
    for n in by:
        key = next((k for k in col if n.startswith(k)), None)
        if key is None or n.startswith("hub_"):
            continue
        sec = [q[q[:, 0] > 55] for q in section_polylines(by[n], "YZ", 0.0)]
        sec = [q for q in sec if len(q) > 1]
        if sec:
            layers.append((sec, col[key], 1.0, "--" if key == "record" else "-"))
            allq = np.vstack(sec)
            ext[key] = (allq[:, 0].min(), allq[:, 0].max(), allq[:, 1].min(), allq[:, 1].max())      # r0, r1, z0, z1 in the cut
    ax = view(fig, rect, layers, title="HALO DETAIL, top edge, section x=0 (same on plain and lit)", pad=3, equal=False)
    ax.set_xlim(40, 178); ax.set_ylim(-14, 52)
    ax.plot([40, 178], [0, 0], color="k", lw=1.6)
    ax.text(42, -0.8, "WALL", fontsize=6.5, va="top", color="k")
    s0, s1, sz0, sz1 = ext["led_cob_strip"]
    a0, a1, az0, az1 = ext["heat_ring_alu"]
    c0, c1, cz0, cz1 = ext["cork_ring"]
    b0, b1, bz0, bz1 = ext["backplate"]
    r0, r1, rz0, rz1 = ext["record"]
    dim_v(ax, 0, sz0, (s0 + s1) / 2, f"{sz0:.1f} strip to wall", off=0.8, fs=6)
    dim_v(ax, 0, bz0, 76, f"{bz0:.1f} gap", off=0.8, fs=6)
    dim_v(ax, bz0, bz1, 92, f"{bz1 - bz0:.2f} MDF", off=0.8, fs=6)
    dim_v(ax, 0, rz1, 163, f"{rz1:.2f} record front", off=0.8, fs=6)
    leader(ax, (s1 - 1, (sz0 + sz1) / 2), (136, 8.0), f"LED strip {sz1 - sz0:.1f} thick,\nLEDs face the wall", fs=6)
    leader(ax, (a1 - 0.5, (az0 + az1) / 2), (136, 14.5), f"aluminium ring RS-HR-12, {az1 - az0:.1f}", fs=6)
    leader(ax, (c1 - 0.5, (cz0 + cz1) / 2), (136, 19.5), f"cork ring RS-CK-12, {cz1 - cz0:.1f}", fs=6)
    ax.text(100, (bz0 + bz1) / 2, "MDF backplate", fontsize=6, ha="left", va="center")
    ax.text(r1 + 1, (rz0 + rz1) / 2, "record", fontsize=6, color="#9b1c1c", ha="left", va="center")
    if "felt_pads" in ext:
        ax.text(ext["felt_pads"][1] + 1.5, bz1 + 3.2, "felt pads", fontsize=6, color="#555555", ha="center", va="bottom")
    if "hub" in ext:
        ax.text(57, bz0 / 2, "hub edge", fontsize=6, ha="left", va="center", rotation=90)
    rows = ((a0, f"R {a0:.0f} ring inner edge"), (s0, f"R {s0:.0f} strip inner edge"), (s1, f"R {s1:.0f} strip outer edge"),
            (a1, f"R {a1:.0f} ring outer edge"), (b1, f"R {b1:.2f} backplate rim"), (r1, f"R {r1:.1f} record edge"))
    for k, (r, lab) in enumerate(rows):
        y = -3.0 - 1.75 * k
        ax.annotate("", xy=(r, y), xytext=(40, y), arrowprops=dict(arrowstyle="->", lw=0.5, color="#1f4e79", shrinkA=0, shrinkB=0))
        ax.plot([r, r], [y, 0], color="#1f4e79", lw=0.3)
        ax.text(r + 1, y, lab, fontsize=5.8, color="#1f4e79", va="center", ha="left",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.4))
    ax.text(41, -1.9, "radius from the centre", fontsize=5.5, color="#1f4e79", va="center")
    ax.text(42, 51, f"Record overhangs the backplate {r1 - b1:.2f}. The strip is {b1 - s1:.2f} inside the rim, on the\n"
                    f"far side of the wood: no line of sight to the record. 4x #4 x 3/8 screws on\nR {S.HALO_SCREW_R} at 45/135/225/315 deg are not in this cut.",
            fontsize=5.8, va="top", color="k")
    return ax


def draw_backplate_al(out_base, d=S.BP12_D, t=5.0, part_no="RS-BP-12-AL5"):
    bp = S.backplate_aluminum(d, t)
    R = d / 2
    fastener = ("1/4-20 flat head (82 deg) countersunk FLUSH on the back face" if t >= 4.5
                else "1/4-20 pan head on the back face (sits in the hub relief); plain D 6.6 hole")
    fig = sheet(f"BACKPLATE {d / 25.4:.1f} in, FLAT ALUMINUM {t:.0f} mm (floating record)", part_no,
                f"5052-H32 aluminum sheet, {t:.1f} mm [{t / 25.4:.3f} in]",
                "Powder coat matte black (RAL 9005 texture or equal), all over, mask threads not required (no threads)",
                [f"Centre: {fastener}. Screw goes into a 3/8 in OD x 1 in 1/4-20 F-F aluminum standoff on the FRONT face (the record rests on it).",
                 "3x #8 flat-head countersinks on the FRONT face (hidden by the record) fasten the hub from the front.",
                 "16 x 13 through cut-out at y=+15 sits over the hub's splice cavity (pigtail to LED leads).",
                 "LED for this variant: 6 x 12 mm top-emitting 12 V COB neon flex laid as a ring on the BACK face, centreline R " + f"{R - S.NEON_RING_INSET:.0f}" + ", emitting toward the wall.",
                 "Laser or waterjet; deburr both faces; no heat-tint on the visible edge. Flatness 0.5 over the face after coating.",
                 "Countersinks may be done by the cutting vendor (SendCutSend / OSH Cut countersink service) or in-house."],
                "SCALE: as shown")
    front = plan_polylines(bp, ("x", "y"))
    ax = view(fig, [0.03, 0.22, 0.50, 0.74], [(front, "k", 0.7, "-")], title="FRONT VIEW (record side)")
    dim_h(ax, -R, R, -R - 14, f"D {mm_in(d)}", off=1.0, ext_from=-R)
    leader(ax, (0, S.AL_CLR_D / 2), (R * 0.25, R * 0.55), f"THRU D {S.AL_CLR_D}" + (f", CSK 82 deg D {S.AL_CSK_D} on BACK face" if t >= 4.5 else " (plain)"))
    x, y = S.pol(S.HUB_SCREW_R, 330)
    leader(ax, (x, y), (R * 0.55, -R * 0.35), f"3x #8 CSK 90 deg D {S.HUB_SCREW_CLR_D} thru, CSK D {min(S.HUB_SCREW_CSK_D, 2 * t - 0.4):.1f} FRONT,\non R {S.HUB_SCREW_R} @ 90/210/330 deg")
    leader(ax, (8, S.JACK_Y), (R * 0.3, R * 0.85), f"cut-out {S.BP_JACK_POCKET[0]} x {S.BP_JACK_POCKET[1]} @ (0, +{S.JACK_Y:.0f})")
    sec = section_polylines(bp.val(), "YZ", 0.0)
    ax2 = view(fig, [0.55, 0.45, 0.43, 0.45], [(sec, "k", 0.9, "-")], title="SECTION A-A (x=0)")
    dim_v(ax2, 0, t, R + 16, mm_in(t), off=2, ext_from=R)
    save(fig, out_base)



def draw_hub(out_base):
    h = S.hub()
    R = S.HUB_D / 2
    ent = [a + S.LOCK_ENTRY_SIGN * S.LOCK_ARC_DEG for a in S.STUD_ANGLES]
    fig = sheet("HUB, twist-lock, PETG/ASA print (IM-ready)", "RS-HUB-01",
                "PETG or ASA, FDM: 0.2 mm layers, 5 perimeters, 40% gyroid, print REAR face down. Later: injection moulded ABS/PC-ABS",
                "As printed, matte black or dark grey filament. IM: SPI-C1 texture, add 0.5-1 deg draft on all pockets at tooling",
                ["Hidden part: sits between the backplate and the wall. Rear face (z=0) is the wall face.",
                 f"Rear recess D {2 * S.HUB_RECESS_R:.0f} x {S.HUB_RECESS_DEPTH} deep swallows the 4 in steel plate and screw heads.",
                 f"3x J-slots on R {S.STUD_R}: entry D {S.JENTRY_D} at {', '.join(f'{a:.0f}' for a in ent)} deg, shank slot {S.JSLOT_W} wide, {S.LOCK_ARC_DEG:.0f} deg arc to the locked position at {', '.join(str(a) for a in S.STUD_ANGLES)} deg (angles in the FRONT / room-side view): the hub LOCKS CLOCKWISE seen from the room. Nut pocket {S.NUT_POCKET_W} wide above the {S.JWEB_T} web, ceiling z={S.NUT_POCKET_TOP}.",
                 f"NO DC JACK (rev B). Rear cable pocket: slot {S.POCKET_W} wide, y {S.POCKET_Y0:+.1f}..{S.POCKET_Y1:+.1f}, {S.POCKET_DEPTH} deep. D {S.CABLE_HOLE_D} pigtail hole at (0,+{S.JACK_Y:.0f}) through a {S.JACK_WEB_T} web into the splice cavity {S.JACK_CAVITY[0]} x {S.JACK_CAVITY[1]} (opens to the FRONT). D {S.CLIP_PILOT_D} x {S.CLIP_PILOT_DEPTH} pilot at ({S.CLIP_POS[0]}, {S.CLIP_POS[1]}) in the pocket ceiling for the P-clip screw (#4 x 3/8): the strain relief for the {S.PIGTAIL_L:.0f} mm 18 AWG pigtail.",
                 f"Rear cord channel {S.CORD_CHAN_W} x {S.CORD_CHAN_D} deep, 6 o'clock, pocket to rim: the pigtail leaves here for a surface cord, or turns back through the plate slot for in-wall. Front lead channel {S.FRONT_CHAN_W} x {S.FRONT_CHAN_D} deep, 6 o'clock, rim to cavity.",
                 f"Front centre relief D {S.CAP_RELIEF_D} x {S.CAP_RELIEF_DEPTH} +/-0.2 deep (rev A 4.5), floor flat: seat of the label-light contact module. Mark '12 V DC ONLY' beside the cord channel (label or deboss 0.4).",
                 f"M3 heat-set insert (D {S.SET_INSERT_D} x {S.SET_INSERT_DEPTH} pilot) in the rim at {S.TAB_ANGLE:.0f} deg, z={S.SET_SCREW_Z}; M3x12 set screw lands in the plate tab. 3x D {S.HUB_SCREW_PILOT_D} x {S.HUB_SCREW_PILOT_DEPTH} pilots on R {S.HUB_SCREW_R} (front) for #8 x 1 in screws."],
                "SCALE: as shown", rev="C", supersedes="rev A, rev B (rev B could not be twisted onto the plate: tab pocket too short)")
    rear = plan_polylines(h, ("x", "y"), zmax=S.NUT_POCKET_TOP)
    ax = view(fig, [0.03, 0.22, 0.47, 0.74], [(rear, "k", 0.6, "-")], title="PLAN (features up to z=19, +X to the right = room-side orientation). +Y = 12 o'clock")
    dim_h(ax, -R, R, -R - 10, f"D {mm_in(S.HUB_D)}", off=1.0, ext_from=-R)
    x, y = S.pol(S.STUD_R, 315 + S.LOCK_ENTRY_SIGN * S.LOCK_ARC_DEG)
    leader(ax, (x, y), (R * 0.75, -R * 0.75), f"J-slot entry D {S.JENTRY_D}\n(3x on R {S.STUD_R})")
    x, y = S.pol(S.STUD_R, 315)
    leader(ax, (x, y), (R * 0.75, -R * 0.45), "locked position\n(twist 20 deg CLOCKWISE\nseen from the room)")
    leader(ax, (0, S.JACK_Y), (R * 0.25, R * 0.8), f"pigtail hole D {S.CABLE_HOLE_D} @ y=+{S.JACK_Y:.0f}")
    leader(ax, S.CLIP_POS, (-R * 0.95, R * 0.55), f"P-clip pilot D {S.CLIP_PILOT_D} x {S.CLIP_PILOT_DEPTH}\n@ ({S.CLIP_POS[0]}, {S.CLIP_POS[1]})")
    leader(ax, (0, -R + 5), (R * 0.2, -R * 0.95), f"cord channel {S.CORD_CHAN_W} wide")
    tx, ty = S.pol(S.TAB_POCKET_R1 - 2, S.TAB_ANGLE)
    leader(ax, (tx, ty), (-R * 0.95, -R * 0.75), f"set-screw tab pocket: arc {S.tab_sweep_angles()[0]:.0f} to {S.tab_sweep_angles()[1]:.0f} deg\n(REV C: covers the whole 20 deg twist;\nset screw at {S.TAB_ANGLE:.0f} deg)")
    secx = section_polylines(h.val(), "YZ", 0.0)
    ax2 = view(fig, [0.52, 0.56, 0.46, 0.38], [(secx, "k", 0.9, "-")], title="SECTION B-B (x=0): cable pocket, web, channels, splice cavity, centre relief")
    dim_v(ax2, 0, S.HUB_T, R + 4, mm_in(S.HUB_T), off=1.5)
    dim_v(ax2, 0, S.POCKET_DEPTH, S.POCKET_Y1 - 4, f"pocket {S.POCKET_DEPTH}", off=1.5)
    dim_v(ax2, 0, S.HUB_RECESS_DEPTH, -45, f"{S.HUB_RECESS_DEPTH}", off=1.5)
    dim_v(ax2, S.HUB_T - S.CAP_RELIEF_DEPTH, S.HUB_T, -2, f"relief {S.CAP_RELIEF_DEPTH} +/-0.2", off=-1.5)
    sa = S.STUD_ANGLES[0]
    # section through a stud (rotate the hub so the stud sits on +X, then cut XZ)
    hr = h.rotate((0, 0, 0), (0, 0, 1), -sa)
    secs = section_polylines(hr.val(), "XZ", 0.0)
    ax3 = view(fig, [0.52, 0.20, 0.46, 0.33], [(secs, "k", 0.9, "-")], title=f"SECTION C-C through a stud ({sa} deg, locked position): recess, J-web, nut pocket")
    dim_v(ax3, S.HUB_RECESS_DEPTH, S.HUB_RECESS_DEPTH + S.JWEB_T, S.STUD_R + 12, f"web {S.JWEB_T}", off=1.5)
    dim_v(ax3, S.HUB_RECESS_DEPTH + S.JWEB_T, S.NUT_POCKET_TOP, S.STUD_R + 20, f"pocket to z={S.NUT_POCKET_TOP}", off=1.5)
    save(fig, out_base)


def draw_wall_plate(out_base):
    p = S.wall_plate()
    R = S.PLATE_D / 2
    g = S.wall_plate_flat_geometry()
    fig = sheet("WALL MOUNTING PLATE, 14 ga steel, formed", "RS-WP-01",
                "Mild steel CRS, 14 ga (0.0747 in / 1.90 mm). Alt: 304 SS 14 ga",
                "Powder coat black, studs masked (SendCutSend cannot zinc plate 0.074 in steel, checked 2026-11-11). Alt: G90 galvanized sheet, no finish. Hidden part",
                ["Flat pattern in RS-WP-01_flat.dxf (1:1, mm). One 90 deg bend UP (toward the hub side), inside radius 1.9 (1t), K=0.44, tab at the 250 deg position.",
                 f"3x PEM self-clinching studs FH-832-10 (8-32 x 5/8) pressed from the WALL face (flush side to wall), in D {S.STUD_HOLE_D} holes on R {S.STUD_R} @ {', '.join(str(a) for a in S.STUD_ANGLES)} deg. Verify hole size on PEM bulletin FH before cutting.",
                 f"4x arc slots {S.SLOT_W} wide: pair on D 83.3 (single-gang / LV bracket) at 90/270 deg, +/-{S.SLOT_HALF_DEG_GANG:.0f} deg (REV B: was +/-10, too close to the 75 deg stud hole); pair on D 88.9 (round / octagon box) at 0/180 deg, +/-{S.SLOT_HALF_DEG:.0f} deg. Stud holes D {S.STUD_HOLE_D} (PEM FH-832: 4.14 to 4.22), each at least {S.PEM_MIN_CL_TO_EDGE:.2f} from any edge.",
                 f"Centre slot {S.PLATE_HOLE_D} wide x {S.PLATE_HOLE_Y1 - S.PLATE_HOLE_Y0:.0f} long passes the hub pigtail and its inline jack (in-wall route); the wall hole is 1 in, on the plate centre.",
                 f"Tab: {S.TAB_W} wide, stands {S.TAB_TOP_Z} above the wall face, D {S.TAB_HOLE_D} hole at z={S.TAB_HOLE_Z} for the M3 set screw.",
                 "Deburr all edges; no sharp edge toward the wall. Flat within 0.3 after forming."],
                "SCALE: as shown", rev="B", supersedes="rev A (gang slots +/-10 deg, stud holes D 4.22)")
    plan = plan_polylines(p, ("x", "y"))
    ax = view(fig, [0.03, 0.22, 0.47, 0.74], [(plan, "k", 0.7, "-")], title="VIEW FROM THE HUB SIDE (studs toward viewer). +Y = 12 o'clock")
    dim_h(ax, -R, R, -R - 14, f"D {mm_in(S.PLATE_D)}", off=1.0, ext_from=-R)
    x, y = S.pol(S.STUD_R, 315)
    leader(ax, (x, y), (R * 0.75, -R * 0.75), f"3x D {S.STUD_HOLE_D} PEM FH-832 on R {S.STUD_R}")
    x, y = S.pol(S.SLOT_R_GANG, 90)
    leader(ax, (x, y), (R * 0.35, R * 1.12), f"2x arc slot {S.SLOT_W} w, R {S.SLOT_R_GANG:.2f} (D 83.3), +/-{S.SLOT_HALF_DEG_GANG:.0f} deg")
    x, y = S.pol(S.SLOT_R_ROUND, 0)
    leader(ax, (x, y), (R * 0.75, R * 0.35), f"2x arc slot {S.SLOT_W} w, R {S.SLOT_R_ROUND:.2f} (D 88.9), +/-10 deg")
    leader(ax, (S.PLATE_HOLE_D / 2, 5), (R * 0.55, R * 0.7), f"slot {S.PLATE_HOLE_D} x {S.PLATE_HOLE_Y1 - S.PLATE_HOLE_Y0:.0f} (y {S.PLATE_HOLE_Y0:+.0f}..{S.PLATE_HOLE_Y1:+.0f})")
    tx, ty = S.pol(R + 2, S.TAB_ANGLE)
    leader(ax, (tx, ty), (-R * 1.1, -R * 0.85), f"bent tab @ {S.TAB_ANGLE:.0f} deg")
    # side section through the tab
    pr = p.rotate((0, 0, 0), (0, 0, 1), -S.TAB_ANGLE)
    sec = section_polylines(pr.val(), "XZ", 0.0)
    sec = [s for s in sec if s[:, 0].min() > 30]
    ax2 = view(fig, [0.53, 0.55, 0.45, 0.38], [(sec, "k", 1.0, "-")], title="SECTION D-D through the tab (radial cut at 250 deg)", pad=3)
    dim_v(ax2, 0, S.TAB_TOP_Z, R + S.BEND_RI + S.PLATE_T + 5, f"{S.TAB_TOP_Z}", off=1.0)
    dim_v(ax2, 0, S.PLATE_T, R - 8, f"{S.PLATE_T:.2f}", off=-1.0)
    leader(ax2, (R + S.BEND_RI + S.PLATE_T, S.TAB_HOLE_Z), (R + 10, S.TAB_HOLE_Z + 4), f"D {S.TAB_HOLE_D} @ z={S.TAB_HOLE_Z}")
    leader(ax2, (R + S.BEND_RI * 0.3, S.PLATE_T + 0.3), (R - 6, S.PLATE_T + 6), f"Ri {S.BEND_RI} (1t)")
    # flat pattern note panel
    ax3 = fig.add_axes([0.53, 0.20, 0.45, 0.32]); ax3.set_axis_off()
    ax3.text(0, 0.95, "FLAT PATTERN (see RS-WP-01_flat.dxf)", fontsize=9, weight="bold", va="top")
    txt = (f"Bend allowance (90 deg, Ri {S.BEND_RI}, t {S.PLATE_T:.2f}, K {S.K_FACTOR}) = {g['ba']:.2f} mm\n"
           f"Tab flat length from the plate edge (R {R:.1f}) = {g['tab_end_r'] - R:.2f} mm  (ends at R {g['tab_end_r']:.2f})\n"
           f"Bend line (centre of bend zone) at R {g['bend_line_r']:.2f}\n"
           f"Tab hole centre in the flat at R {g['hole_r']:.2f} on the {S.TAB_ANGLE:.0f} deg radial\n"
           f"Flat envelope: {2 * R:.1f} x {R + g['tab_end_r']:.1f} mm")
    ax3.text(0, 0.82, txt, fontsize=8, va="top", family="monospace")
    save(fig, out_base)



def draw_cap(out_base, which="12"):
    sl = S.CAP_SHOULDER_L
    if which == "12":
        cap, D, rim, dome, part_no = S.dome_cap_12(), S.CAP12_D, S.CAP12_RIM_H, S.CAP12_DOME_H, "RS-CAP-12"
        title = "DOME CAP 1.5 in, 12 in record"
        rev, sup, stud_l = "D", "rev A, B, C", S.CAP12_STUD_L
        fits = (f"Smooth shoulder D {S.CAP_SHOULDER_D:.2f} +0/-0.05 from the recess floor to {sl} below the band face, Ra 0.8, 0.2 lead-in: the record "
                f"hangs and centres on it (spindle hole 7.24 min). Underside recess D {S.CAP12_RECESS_D} x {S.CAP12_RECESS_H:.2f} +/-{S.CAP12_RECESS_TOL} deep, flat floor.")
        extra = (f"We fit after plating: felt washer {S.FELT_WASHER[0]} OD x {S.FELT_WASHER[1]} ID x {S.FELT_WASHER[2]} in the recess (0.6 proud free, 0.3 at 50 N) and a loose clear PET "
                 f"label washer {S.PET_WASHER[0]} x {S.PET_WASHER[1]} x {S.PET_WASHER[2]} under the cap. REV D (2026-11-11): stud {stud_l} (rev C 11.70), shoulder added, tolerances added, "
                 "separate-stud option deleted (a tapped D 7.10 shoulder would have a 0.37 wall).")
    else:
        cap, D, rim, dome, part_no = S.dome_cap_7(), S.CAP7_D, S.CAP7_RIM_H, S.CAP7_DOME_H, "RS-CAP-7"
        title = "DOME CAP 48 mm, 7 in record (45 adapter form)"
        rev, sup, stud_l = "C", "rev A, B", S.CAP7_STUD_L
        fits = f"Underside boss D {S.CAP7_BOSS_D} +0/-0.1 x {S.CAP7_BOSS_H} centres the cap in the 38.1 mm 45-rpm hole (replaces the plastic adapter)."
        extra = (f"We fit: felt ring {S.FELT_RING7[0]} x {S.FELT_RING7[1]} x {S.FELT_RING7[2]} and a clear PET ring {S.PET_WASHER7[0]} x {S.PET_WASHER7[1]} x {S.PET_WASHER7[2]}. "
                 f"REV C (2026-11-11): stud {stud_l} (rev B 15.88) so its tip lands exactly where the RS-CAP-12 tip lands; a rev B cap over-drives the lit sconce's centre contact.")
    sphR = (D / 2) ** 2 / (2 * dome) + dome / 2
    fig = sheet(title, part_no,
                "Brass C360 (CDA 360) bar, turned in ONE piece with the 1/4-20 stud. No separate or bonded stud.",
                "CHROME: polish to mirror (Ra <= 0.1 um) then copper + bright nickel + decorative chrome per ASTM B456 SC2 (or PVD chrome over bright nickel). BRASS: polish + clear lacquer or brushed + lacquer. BLACK: black chrome over bright nickel, or PVD black (TiC/DLC), or black nickel + lacquer",
                [f"Dome is a sphere segment, R {sphR:.2f}, height {dome} above a {rim} straight band; base edge R {S.CAP_BASE_R}. NO knurl, no tool marks on the dome.",
                 f"Thread 1/4-20 UNC-2A (class BEFORE plating), full form from the run-in to the relief groove D {S.CAP_STUD_RELIEF_D} x {S.CAP_STUD_RELIEF_L} (R 0.2 at the groove root). TIP: unthreaded dog point "
                 f"D {S.CAP_STUD_DOG_D:.2f} +{S.CAP_DOG_TOL[0]:.0f}/{S.CAP_DOG_TOL[1]:.2f} x {S.CAP_STUD_DOG_L} long (must enter the insert's 4.98 MIN minor dia), 0.3 x 45 chamfer, 45 deg run-in to the thread.",
                 f"Stud length {stud_l:.2f} +/-0.05 from the band (underside) face to the tip. Stud axis to dome axis concentric within 0.05. Underside face flat and square to the stud within 0.05.",
                 fits,
                 "Plating: rack on the STUD only. MASK the thread" + (" and the shoulder" if which == "12" else "") + " (do NOT chase after plating: chrome flakes). Any nickel on the thread 5 um max; the thread must accept a 1/4-20 2B GO gauge AFTER plating. Dome and band are Class A: inspect under daylight at 300 mm, zero pits/haze.",
                 extra,
                 "Finish variants share the same part number with suffix -CR (chrome), -BR (brass), -BK (black)."],
                "SCALE: as shown", rev=rev, supersedes=sup)
    sec = section_polylines(cap.val(), "XZ", 0.0)
    ax = view(fig, [0.05, 0.25, 0.55, 0.68], [(sec, "k", 1.0, "-")], title="SECTION THROUGH THE AXIS", pad=16)
    zt = rim + dome
    dim_h(ax, -D / 2, D / 2, zt + 5, f"D {mm_in(D)}", off=0.8, ext_from=zt)
    dim_v(ax, 0, zt, D / 2 + 7, mm_in(zt), off=1.5, ext_from=D / 2)
    dim_v(ax, 0, rim, D / 2 + 3, f"{rim}", off=1.0)
    dim_v(ax, -stud_l, 0, D / 2 + 7, f"{stud_l:.2f} +/-0.05 [{stud_l / 25.4:.3f}]  1/4-20 UNC-2A", off=1.5)
    dim_h(ax, -S.STUD_14_20_D / 2, S.STUD_14_20_D / 2, -stud_l - 4, f"D {S.STUD_14_20_D:.2f} [0.250]", off=-0.8)
    leader(ax, (S.CAP_STUD_DOG_D / 2, -stud_l + S.CAP_STUD_DOG_L / 2), (D / 2 * 0.75, -stud_l + 3.5),
           f"dog point D {S.CAP_STUD_DOG_D:.2f} +{S.CAP_DOG_TOL[0]:.0f}/{S.CAP_DOG_TOL[1]:.2f} x {S.CAP_STUD_DOG_L}")
    if which == "7":
        dim_h(ax, -S.CAP7_BOSS_D / 2, S.CAP7_BOSS_D / 2, -S.CAP7_BOSS_H - 3.5, f"D {S.CAP7_BOSS_D} +0/-0.1 boss x {S.CAP7_BOSS_H} (fits 38.1 hole)", off=-0.8)
        leader(ax, (S.CAP_STUD_RELIEF_D / 2, -S.CAP7_BOSS_H - 0.5), (D / 2 * 0.6, -7), f"relief D {S.CAP_STUD_RELIEF_D} x {S.CAP_STUD_RELIEF_L}, R 0.2 root")
    else:
        leader(ax, (S.CAP_SHOULDER_D / 2, -sl / 2), (D / 2 * 0.55, -4.2), f"smooth shoulder D {S.CAP_SHOULDER_D:.2f} +0/-0.05\nto {sl} below the band face, Ra 0.8")
        leader(ax, (S.CAP_STUD_RELIEF_D / 2, -sl - 0.5), (D / 2 * 0.55, -7.2), f"relief D {S.CAP_STUD_RELIEF_D} x {S.CAP_STUD_RELIEF_L}, R 0.2 root")
        leader(ax, (-S.CAP12_RECESS_D / 2 + 3, S.CAP12_RECESS_H), (-D / 2 * 1.25, -4.5),
               f"recess D {S.CAP12_RECESS_D} x {S.CAP12_RECESS_H:.2f} +/-{S.CAP12_RECESS_TOL} deep")
    leader(ax, (D / 2 * 0.6, rim + dome * 0.7), (-D / 2 * 0.3, zt + 12), f"sphere R {sphR:.2f}")
    plan = plan_polylines(cap, ("x", "y"))
    view(fig, [0.62, 0.45, 0.36, 0.48], [(plan, "k", 0.7, "-")], title="TOP VIEW")
    save(fig, out_base)


def draw_assembly(out_base, variant="12", material="mdf"):
    import assembly as A
    parts = A.build(variant, material)
    halo = any(n == "heat_ring_alu" for n, p, c, k in parts)
    by = {n: p.val().BoundingBox() for n, p, c, k in parts}
    cap_tip = max(b.zmax for n, b in by.items() if n.startswith("dome_cap"))
    rec_front = max(b.zmax for n, b in by.items() if n.startswith("record"))
    if halo:
        light = (f"HEAT-SAFE HALO (rev 2026-11-11, same on the plain-cap and lit-cap sconce): the 8 mm LED strip is on the BACK of the backplate, LEDs facing the wall, on the 1.0 aluminium ring RS-HR-12 "
                 f"over the {S.CORK_RING_T} cork ring RS-CK-12 (OD {S.HALO_RING_OD:.0f}, ID {S.HALO_RING_ID:.0f}), strip centred on R {S.HALO_STRIP_R:.0f}. Held by 4x #4 x 3/8 screws on R {S.HALO_SCREW_R} into blind pilots. "
                 f"Stack {S.HALO_STACK_H:.1f} deep in the {S.HUB_T:.1f} gap; strip face {S.HUB_T - S.HALO_STACK_H:.1f} from the wall. Strip leads run in the 6 o'clock back channel to the hub splice cavity. No strip on the rim.")
    elif material == "mdf":
        light = ("LED strip on this 7 in sconce is still in the RIM rabbet, facing outward. It is NOT on the heat-safe back-face layout of the 12 in sconce (the back face outside the hub is only "
                 f"{S.BP7_D / 2 - (S.BP12_D / 2 - S.HALO_RING_OD / 2) - S.HUB_D / 2:.2f} wide). Open item, see cad/FIXES-heat-layout.md.")
    else:
        light = "Aluminium-backplate variant: neon flex ring on the back face. NOT covered by the heat-safe layout D of the 12 in MDF sconce and not thermally modelled."
    fig = sheet(f"ASSEMBLY SECTION, {variant} in record, backplate {material.upper()}", f"RS-ASM-{variant}-{material.upper()}",
                "see parts list in README.md", "n/a",
                ["Section through x=0 (12 o'clock up). Wall at z=0. Customer record shown for fit only.",
                 "Hub rear face and plate rear face both sit on the wall; the plate hides in the hub recess.",
                 "MDF: record rests on the felt pads AND the centre backing ring (coplanar), clamped felt - record - felt in line. Aluminum: on the 1 in standoff.",
                 f"Cap studs (RS-CAP-12 rev D {S.CAP12_STUD_L}, RS-CAP-7 rev C {S.CAP7_STUD_L}): fully engaged, never proud of the backplate back face (see checks.md). Clear PET label washer under every cap.",
                 "Power: 150 mm pigtail with an inline female 5.5 x 2.1 jack, P-clipped in the hub. Shown on the surface route (6 o'clock channel, mated behind the backplate); for in-wall it turns back through the plate slot and a 1 in wall hole.",
                 light,
                 f"From the wall, measured on this assembly: backplate back {S.HUB_T:.2f}, record front {rec_front:.2f}, cap tip {cap_tip:.2f} (furthest point). All clearances verified by boolean interference check in assembly.py (0 hits)."],
                "SCALE: as shown", rev="B" if halo else "A", supersedes="rev A (LED strip on the rim)" if halo else None)
    colors = {"custom": "k", "purchased": "#555555", "customer": "#9b1c1c"}
    layers = []
    for n, p, c, kind in parts:
        sec = section_polylines(p.val(), "YZ", 0.0)
        if sec:
            layers.append((sec, colors[kind], 0.9 if kind == "custom" else 0.7, "-" if kind != "customer" else "--"))
    rect = [0.03, 0.22, 0.60, 0.72] if halo else [0.03, 0.22, 0.94, 0.72]
    ax = view(fig, rect, layers, title="SECTION x=0  (black = custom parts, grey = purchased, red dashed = customer record)", pad=10)
    xr = S.REC12_D / 2 if variant == "12" else S.REC7_D / 2
    ax.set_xlim(-xr - 22, xr + 40)
    ax.plot([-xr - 16, xr + 34], [0, 0], color="k", lw=1.4)
    ax.text(-xr - 16, -1.5, "WALL (z = 0)", fontsize=6.5, va="top")
    dim_v(ax, 0, S.HUB_T, -xr - 6, f"wall gap {S.HUB_T:.1f}", off=-1.5)
    dim_v(ax, 0, rec_front, xr + 8, f"record front {rec_front:.2f}", off=1.5, ext_from=xr)
    dim_v(ax, 0, cap_tip, xr + 22, f"cap tip {cap_tip:.2f}", off=1.5, ext_from=20)
    if halo:
        halo_detail(fig, [0.66, 0.22, 0.32, 0.72], parts)
    save(fig, out_base)
