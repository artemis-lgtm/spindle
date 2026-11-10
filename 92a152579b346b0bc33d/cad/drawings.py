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

DATE = "2026-11-09"
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


def sheet(title, part_no, material, finish, notes, scale_txt, rev="A", size=(16.5, 11.7)):
    fig = plt.figure(figsize=size)
    fig.patch.set_facecolor("white")
    # border + title block
    ax0 = fig.add_axes([0, 0, 1, 1]); ax0.set_axis_off(); ax0.set_xlim(0, 1); ax0.set_ylim(0, 1)
    ax0.add_patch(plt.Rectangle((0.01, 0.01), 0.98, 0.98, fill=False, lw=1.2))
    ax0.add_patch(plt.Rectangle((0.56, 0.01), 0.43, 0.16, fill=False, lw=1.0))
    ax0.text(0.57, 0.16, f"RECORD SCONCE  |  {title}", fontsize=11.5, weight="bold", va="top", family="DejaVu Sans")
    y = 0.135
    lines = [f"PART NO: {part_no}      REV: {rev}      DATE: {DATE}"]
    lines += textwrap.wrap("MATERIAL: " + material, 95)
    lines += textwrap.wrap("FINISH: " + finish, 95)
    lines += ["UNITS: mm [in]   THIRD-ANGLE PROJECTION   " + scale_txt,
              "GENERAL TOLERANCES: x.x +/-0.3   x.xx +/-0.1   angles +/-0.5 deg   unless noted"]
    for ln in lines:
        ax0.text(0.57, y, ln, fontsize=7.4, va="top")
        y -= 0.0155
    ax0.text(0.02, 0.165, "NOTES:", fontsize=8.5, weight="bold", va="top")
    y = 0.148
    for i, n in enumerate(notes):
        for j, ln in enumerate(textwrap.wrap(n, 135)):
            ax0.text(0.02, y, (f"{i + 1}. " if j == 0 else "    ") + ln, fontsize=7.0, va="top")
            y -= 0.0145
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
    bp = S.backplate(d, pads_out=(d > 200))
    R = d / 2
    fig = sheet(f"BACKPLATE {d / 25.4:.1f} in, CNC MDF / BIRCH", part_no,
                "1/2 in (12.7) MDF or Baltic birch plywood, both faces flat",
                "Matte black, 2 coats (paint after machining); rim rabbet and notch unpainted OK",
                ["E-Z Lok 400-4 brass insert, 1/4-20, driven FLUSH with the FRONT face in the 25/64 in bore (CA glue in MDF).",
                 "Rim rabbet carries an 8 mm COB LED strip, LEDs facing outward; keep rabbet floor smooth (no fuzz).",
                 "Felt pad targets are 0.5 mm deep spots for 1/2 in self-adhesive felt pads (assembly aid only).",
                 "3x #8 flat-head countersinks on the FRONT face (hidden by the record) fasten the hub from the front.",
                 "Rear pocket 16 x 13 x 6.5 at y=+15 clears the DC jack body; rear channel 6 x 4 routes the LED leads to the hub.",
                 "Break all edges 0.5 max. Flatness 0.5 over the full face. No visible tear-out on the front face or rim."],
                "SCALE: as shown (not to print scale)")
    front = plan_polylines(bp, ("x", "y"))
    ax = view(fig, [0.03, 0.22, 0.50, 0.74], [(front, "k", 0.7, "-")], title="FRONT VIEW (record side)")
    dim_h(ax, -R, R, -R - 14, f"D {mm_in(d)}", off=1.0, ext_from=-R)
    leader(ax, (0, S.INSERT_BORE_D / 2), (R * 0.25, R * 0.55), f"THRU D {S.INSERT_BORE_D:.2f} [25/64]\nfor E-Z Lok 400-4 insert")
    x, y = S.pol(S.HUB_SCREW_R, 330)
    leader(ax, (x, y), (R * 0.55, -R * 0.35), f"3x #8 CSK 90 deg, D {S.HUB_SCREW_CLR_D} thru,\nCSK D {S.HUB_SCREW_CSK_D}, on R {S.HUB_SCREW_R} @ 90/210/330 deg")
    if d > 200:
        x, y = S.pol(S.PAD_R_OUT, 210)
        leader(ax, (x, y), (-R * 0.95, -R * 0.9), f"3x felt target D {S.PAD_D + 0.6:.1f} x 0.5 deep\non R {S.PAD_R_OUT:.1f} @ 90/210/330")
    x, y = S.pol(S.PAD_R_IN, 210)
    leader(ax, (x, y), (-R * 0.95, -R * 0.55), f"3x felt target D {S.PAD_D + 0.6:.1f} x 0.5 deep\non R {S.PAD_R_IN:.2f} @ 90/210/330")
    leader(ax, (0, -R + 1), (R * 0.2, -R * 0.78), f"lead notch {S.NOTCH_W} wide at 6 o'clock,\nrabbet floor to back face")
    # section through x=0 (YZ) to show the rabbet and the jack pocket
    sec = section_polylines(bp.val(), "YZ", 0.0)
    ax2 = view(fig, [0.55, 0.52, 0.43, 0.42], [(sec, "k", 0.9, "-")], title="SECTION A-A (x=0), rim detail enlarged below")
    dim_v(ax2, 0, S.BP_T, R + 16, mm_in(S.BP_T), off=2, ext_from=R)
    leader(ax2, (-R + 0.5, S.BP_T / 2), (-R * 0.7, S.BP_T + 18), f"rim rabbet {S.RABBET_W} wide x {S.RABBET_DEPTH} deep,\ncentred on the rim")
    leader(ax2, (S.JACK_Y, 2), (R * 0.3, S.BP_T + 18), f"rear pocket {S.BP_JACK_POCKET[0]} x {S.BP_JACK_POCKET[1]} x {S.BP_JACK_POCKET[2]} deep @ y=+{S.JACK_Y:.0f}")
    # rim detail
    sec_rim = [p for p in sec if p[:, 0].max() < -R + 40]
    ax3 = view(fig, [0.55, 0.20, 0.43, 0.30], [(sec_rim, "k", 1.1, "-")], title="DETAIL: rim rabbet + 6 o'clock lead notch (x=0 cut)", pad=3)
    z0 = (S.BP_T - S.RABBET_W) / 2
    dim_v(ax3, z0, z0 + S.RABBET_W, -R - 6, f"{S.RABBET_W}", off=-1.5)
    dim_h(ax3, -R, -R + S.RABBET_DEPTH, S.BP_T + 2.5, f"{S.RABBET_DEPTH}", off=0.5)
    dim_h(ax3, -R + S.RABBET_DEPTH, -60, -2.5, f"rear channel {S.BACK_CHAN_W} wide x {S.BACK_CHAN_D} deep to R60", off=-0.5)
    save(fig, out_base)


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
                 "16 x 13 through cut-out at y=+15 clears the DC jack body in the hub.",
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
    fig = sheet("HUB, twist-lock, PETG/ASA print (IM-ready)", "RS-HUB-01",
                "PETG or ASA, FDM: 0.2 mm layers, 5 perimeters, 40% gyroid, print REAR face down. Later: injection moulded ABS/PC-ABS",
                "As printed, matte black or dark grey filament. IM: SPI-C1 texture, add 0.5-1 deg draft on all pockets at tooling",
                ["Hidden part: sits between the backplate and the wall. Rear face (z=0) is the wall face.",
                 f"Rear recess D {2 * S.HUB_RECESS_R:.0f} x {S.HUB_RECESS_DEPTH} deep swallows the 4 in steel plate and screw heads.",
                 f"3x J-slots on R {S.STUD_R}: entry D {S.JENTRY_D} at {', '.join(str(a + 20) for a in S.STUD_ANGLES)} deg, shank slot {S.JSLOT_W} wide, {S.LOCK_ARC_DEG:.0f} deg arc to the locked position at {', '.join(str(a) for a in S.STUD_ANGLES)} deg; nut pocket {S.NUT_POCKET_W} wide above the {S.JWEB_T} web, ceiling z={S.NUT_POCKET_TOP}.",
                 f"Rear DC pocket: slot {S.POCKET_W} wide, y {S.POCKET_Y0:+.1f}..{S.POCKET_Y1:+.1f}, {S.POCKET_DEPTH} deep; D {S.JACK_PANEL_HOLE_D} jack hole at (0,+{S.JACK_Y:.0f}) through a {S.JACK_WEB_T} web; jack body cavity {S.JACK_CAVITY[0]} x {S.JACK_CAVITY[1]} opens to the FRONT.",
                 f"Rear cord channel {S.CORD_CHAN_W} x {S.CORD_CHAN_D} deep, 6 o'clock, pocket to rim (surface-cord option). Front lead channel {S.FRONT_CHAN_W} x {S.FRONT_CHAN_D} deep, 6 o'clock, rim to cavity.",
                 f"M3 heat-set insert (D {S.SET_INSERT_D} x {S.SET_INSERT_DEPTH} pilot) in the rim at {S.TAB_ANGLE:.0f} deg, z={S.SET_SCREW_Z}; M3x12 set screw lands in the plate tab. 3x D {S.HUB_SCREW_PILOT_D} x {S.HUB_SCREW_PILOT_DEPTH} pilots on R {S.HUB_SCREW_R} (front) for #8 x 1 in screws."],
                "SCALE: as shown")
    rear = plan_polylines(h, ("x", "y"), zmax=S.NUT_POCKET_TOP)
    ax = view(fig, [0.03, 0.22, 0.47, 0.74], [(rear, "k", 0.6, "-")], title="REAR VIEW (wall side, looking at z=0). +Y = 12 o'clock")
    dim_h(ax, -R, R, -R - 10, f"D {mm_in(S.HUB_D)}", off=1.0, ext_from=-R)
    x, y = S.pol(S.STUD_R, 315 + 20)
    leader(ax, (x, y), (R * 0.75, -R * 0.75), f"J-slot entry D {S.JENTRY_D}\n(3x on R {S.STUD_R})")
    x, y = S.pol(S.STUD_R, 315)
    leader(ax, (x, y), (R * 0.75, -R * 0.45), "locked position\n(twist 20 deg)")
    leader(ax, (0, S.JACK_Y), (R * 0.25, R * 0.8), f"DC jack hole D {S.JACK_PANEL_HOLE_D} @ y=+{S.JACK_Y:.0f}")
    leader(ax, (0, -R + 5), (R * 0.2, -R * 0.95), f"cord channel {S.CORD_CHAN_W} wide")
    tx, ty = S.pol(S.TAB_POCKET_R1 - 2, S.TAB_ANGLE)
    leader(ax, (tx, ty), (-R * 0.95, -R * 0.75), f"set-screw tab pocket @ {S.TAB_ANGLE:.0f} deg")
    secx = section_polylines(h.val(), "YZ", 0.0)
    ax2 = view(fig, [0.52, 0.56, 0.46, 0.38], [(secx, "k", 0.9, "-")], title="SECTION B-B (x=0): DC pocket, jack web, channels, front cavity")
    dim_v(ax2, 0, S.HUB_T, R + 12, mm_in(S.HUB_T), off=2, ext_from=R)
    dim_v(ax2, 0, S.POCKET_DEPTH, -R - 10, f"{S.POCKET_DEPTH}", off=-2)
    dim_v(ax2, 0, S.HUB_RECESS_DEPTH, R + 4, f"{S.HUB_RECESS_DEPTH}", off=1.5)
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
                "Zinc plate clear (ASTM B633 Fe/Zn 8) or black zinc; or powder coat black. Hidden part",
                ["Flat pattern in RS-WP-01_flat.dxf (1:1, mm). One 90 deg bend UP (toward the hub side), inside radius 1.9 (1t), K=0.44, tab at the 250 deg position.",
                 f"3x PEM self-clinching studs FH-832-10 (8-32 x 5/8) pressed from the WALL face (flush side to wall), in D {S.STUD_HOLE_D} holes on R {S.STUD_R} @ {', '.join(str(a) for a in S.STUD_ANGLES)} deg. Verify hole size on PEM bulletin FH before cutting.",
                 f"4x arc slots {S.SLOT_W} wide, +/-{S.SLOT_HALF_DEG:.0f} deg: pair on D 83.3 (single-gang / LV bracket) at 90/270 deg; pair on D 88.9 (round / octagon box) at 0/180 deg.",
                 f"Centre slot {S.PLATE_HOLE_D} wide x {S.PLATE_HOLE_Y1 - S.PLATE_HOLE_Y0:.0f} long passes the DC plug (jack is offset +15 toward 12 o'clock).",
                 f"Tab: {S.TAB_W} wide, stands {S.TAB_TOP_Z} above the wall face, D {S.TAB_HOLE_D} hole at z={S.TAB_HOLE_Z} for the M3 set screw.",
                 "Deburr all edges; no sharp edge toward the wall. Flat within 0.3 after forming."],
                "SCALE: as shown")
    plan = plan_polylines(p, ("x", "y"))
    ax = view(fig, [0.03, 0.22, 0.47, 0.74], [(plan, "k", 0.7, "-")], title="VIEW FROM THE HUB SIDE (studs toward viewer). +Y = 12 o'clock")
    dim_h(ax, -R, R, -R - 14, f"D {mm_in(S.PLATE_D)}", off=1.0, ext_from=-R)
    x, y = S.pol(S.STUD_R, 315)
    leader(ax, (x, y), (R * 0.75, -R * 0.75), f"3x D {S.STUD_HOLE_D} PEM FH-832 on R {S.STUD_R}")
    x, y = S.pol(S.SLOT_R_GANG, 90)
    leader(ax, (x, y), (R * 0.35, R * 1.12), f"2x arc slot {S.SLOT_W} w, R {S.SLOT_R_GANG:.2f} (D 83.3), +/-10 deg")
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
    if which == "12":
        cap, D, rim, dome, part_no = S.dome_cap_12(), S.CAP12_D, S.CAP12_RIM_H, S.CAP12_DOME_H, "RS-CAP-12"
        title = "DOME CAP 1.5 in, 12 in record"
        extra = "Underside flat; 1 in OD x 3/8 in ID x 1/8 in self-adhesive felt washer goes on the underside."
    else:
        cap, D, rim, dome, part_no = S.dome_cap_7(), S.CAP7_D, S.CAP7_RIM_H, S.CAP7_DOME_H, "RS-CAP-7"
        title = "DOME CAP 48 mm, 7 in record (45 adapter form)"
        extra = f"Underside boss D {S.CAP7_BOSS_D} x {S.CAP7_BOSS_H} centres the cap in the 38.1 mm 45-rpm hole (replaces the plastic adapter)."
    sphR = (D / 2) ** 2 / (2 * dome) + dome / 2
    fig = sheet(title, part_no,
                "Brass C360 (CDA 360) bar, turned in one piece with the 1/4-20 stud. Alt: tapped 1/4-20 x 0.40 deep + 1/4-20 x 1-1/8 stainless threaded stud, Loctite 243",
                "CHROME: polish to mirror (Ra <= 0.1 um) then copper + bright nickel + decorative chrome per ASTM B456 SC2 (or PVD chrome over bright nickel). BRASS: polish + clear lacquer or brushed + lacquer. BLACK: black chrome over bright nickel, or PVD black (TiC/DLC), or black nickel + lacquer",
                [f"Dome is a sphere segment, R {sphR:.2f}, height {dome} above a {rim} straight band; base edge R {S.CAP_BASE_R}. NO knurl, no tool marks on the dome.",
                 "Thread 1/4-20 UNC-2A, full form to within 1 mm of the shoulder; relief groove D 5.4 x 1.0 at the root; 0.5 x 45 deg chamfer at the tip.",
                 "Stud axis to dome axis: concentric within 0.05. Underside face flat and square to the stud within 0.05.",
                 "Plating: mask the thread (or chase after plating). Dome and visible band are Class A, inspect under daylight at 300 mm, zero pits/haze.",
                 extra,
                 "Finish variants share the same part number with suffix -CR (chrome), -BR (brass), -BK (black)."],
                "SCALE: as shown")
    sec = section_polylines(cap.val(), "XZ", 0.0)
    ax = view(fig, [0.05, 0.25, 0.55, 0.68], [(sec, "k", 1.0, "-")], title="SECTION THROUGH THE AXIS", pad=16)
    zt = rim + dome
    dim_h(ax, -D / 2, D / 2, zt + 5, f"D {mm_in(D)}", off=0.8, ext_from=zt)
    dim_v(ax, 0, zt, D / 2 + 7, mm_in(zt), off=1.5, ext_from=D / 2)
    dim_v(ax, 0, rim, D / 2 + 3, f"{rim}", off=1.0)
    dim_v(ax, -S.CAP_STUD_L, 0, D / 2 + 7, f"{mm_in(S.CAP_STUD_L)}  1/4-20 UNC-2A", off=1.5)
    dim_h(ax, -S.STUD_14_20_D / 2, S.STUD_14_20_D / 2, -S.CAP_STUD_L - 4, f"D {S.STUD_14_20_D:.2f} [0.250]", off=-0.8)
    if which == "7":
        dim_h(ax, -S.CAP7_BOSS_D / 2, S.CAP7_BOSS_D / 2, -S.CAP7_BOSS_H - 3.5, f"D {S.CAP7_BOSS_D} boss x {S.CAP7_BOSS_H} (fits 38.1 hole)", off=-0.8)
    leader(ax, (S.CAP_STUD_RELIEF_D / 2, -0.5), (D / 2 * 0.6, -6), f"relief D {S.CAP_STUD_RELIEF_D} x {S.CAP_STUD_RELIEF_L}")
    leader(ax, (D / 2 * 0.6, rim + dome * 0.7), (-D / 2 * 0.3, zt + 12), f"sphere R {sphR:.2f}")
    plan = plan_polylines(cap, ("x", "y"))
    view(fig, [0.62, 0.45, 0.36, 0.48], [(plan, "k", 0.7, "-")], title="TOP VIEW")
    save(fig, out_base)


def draw_assembly(out_base, variant="12", material="mdf"):
    import assembly as A
    parts = A.build(variant, material)
    fig = sheet(f"ASSEMBLY SECTION, {variant} in record, backplate {material.upper()}", f"RS-ASM-{variant}-{material.upper()}",
                "see parts list in README.md", "n/a",
                ["Section through x=0 (12 o'clock up). Wall at z=0. Customer record shown for fit only.",
                 "Hub rear face and plate rear face both sit on the wall; the plate hides in the hub recess.",
                 "Record rests on felt pads (MDF) or on the 1 in standoff (aluminum floating configuration).",
                 "Dome cap stud is 5/8 in: fully engaged, never proud of the backplate back face (see checks.md).",
                 "DC plug enters along the wall normal through the plate slot and the 1-1/4 in wall hole (in-wall option).",
                 "All clearances verified by boolean interference check in assembly.py (0 hits)."],
                "SCALE: as shown")
    colors = {"custom": "k", "purchased": "#555555", "customer": "#9b1c1c"}
    layers = []
    for n, p, c, kind in parts:
        sec = section_polylines(p.val(), "YZ", 0.0)
        if sec:
            layers.append((sec, colors[kind], 0.9 if kind == "custom" else 0.7, "-" if kind != "customer" else "--"))
    ax = view(fig, [0.03, 0.22, 0.94, 0.72], layers, title="SECTION x=0  (black = custom parts, grey = purchased, red dashed = customer record)", pad=10)
    z_bp0 = S.HUB_T
    dim_v(ax, 0, S.HUB_T, -S.REC12_D / 2 - 6 if variant == "12" else -S.REC7_D / 2 - 6, f"wall gap {S.HUB_T:.1f}", off=-1.5)
    save(fig, out_base)
