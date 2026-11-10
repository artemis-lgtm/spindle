"""
Record sconce: parametric CAD (CadQuery 2.8). All units mm. Z = wall normal, +Z toward the room.
+Y = 12 o'clock, -Y = 6 o'clock when the fixture hangs on the wall.

Part-local origins:
  wall plate  : rear (wall) face at z=0, +Z toward the hub
  hub         : rear (wall) face at z=0, front (glued to backplate) at z=HUB_T
  backplate   : back face at z=0, front (record side) at z=BP_T
  dome cap    : underside of the cap flange at z=0, stud goes -Z
Decisions and dimensions come from ../NOTES.md, ../engineering-report.md, ../mounting-report.md,
../design-report.md, ../render/sconce_v2.py. Standard part dims are cited in README.md.
"""
import math
import cadquery as cq

IN = 25.4

# ---------------------------------------------------------------- records (customer supplied)
REC12_D = 12.0 * IN          # 304.8
REC12_T = 0.08 * IN          # 2.03  (per task brief)
REC_HOLE_D = 0.286 * IN      # 7.26  spindle hole (engineering-report sec.1)
LABEL_D = 100.0
REC7_D = 7.0 * IN            # 177.8
REC7_T = 1.9
REC7_HOLE_D = 1.5 * IN       # 38.1  45 rpm large hole (engineering-report sec.1)

# ---------------------------------------------------------------- backplate
BP12_D = 10.5 * IN           # 266.7
BP7_D = 6.0 * IN             # 152.4 (engineering-report: "smaller 6-inch backplate variant")
BP_T = 0.5 * IN              # 12.7 MDF / Baltic birch
BP_AL_T = (3.0, 5.0)         # aluminum flat variants
INSERT_BORE_D = 25.0 / 64.0 * IN   # 9.92  E-Z Lok 400-4 drill 25/64" (engineering-report sec.1)
INSERT_L = 0.5 * IN          # 12.7
RABBET_W = 10.2              # 0.40" rim rabbet for an 8 mm COB strip
RABBET_DEPTH = 1.5
LED_W = 8.0
LED_T = 1.6
NOTCH_W = 6.35               # 0.25" lead notch at 6 o'clock
BACK_CHAN_W = 6.0
BACK_CHAN_D = 4.0
PAD_D = 12.7                 # 1/2" felt pad
PAD_T = 1.6                  # 1/16"
PAD_TARGET_DEPTH = 0.5
PAD_R_OUT = 5.0 * IN         # 127
PAD_R_IN = 2.75 * IN         # 69.85
PAD_ANGLES = (90, 210, 330)  # one at 12 o'clock
HUB_SCREW_R = 45.0           # #8 flat-head wood screws, front side, hidden by the record
HUB_SCREW_ANGLES = (90, 210, 330)
HUB_SCREW_CLR_D = 4.5        # #8 clearance
HUB_SCREW_CSK_D = 8.6
HUB_SCREW_PILOT_D = 3.2      # pilot in PETG for #8
HUB_SCREW_PILOT_DEPTH = 14.0
# aluminum flat variant (floating configuration): 1/4-20 flat head csk from the back + standoff on the front
AL_CLR_D = 6.6               # 1/4 in close clearance
AL_CSK_D = 13.0              # 82 deg countersink diameter for a 1/4-20 flat head (head dia 0.507 in max)
STANDOFF_OD = 3.0 / 8.0 * IN # 9.525
STANDOFF_L = 1.0 * IN        # 25.4
NEON_RING_INSET = 15.0       # neon-flex ring centreline inset from the plate edge

# ---------------------------------------------------------------- hub (PETG print, IM-compatible)
HUB_D = 5.0 * IN             # 127
HUB_T = 1.0 * IN             # 25.4 = wall gap
HUB_FILLET = 1.2
HUB_RECESS_R = 53.5          # swallows the 4" plate (R50.8) + 2.7 clearance
HUB_RECESS_DEPTH = 5.5       # plate 1.9 + #8 pan head 2.8 + 0.8
JWEB_T = 3.0                 # J-slot web thickness (z 5.5..8.5)
NUT_POCKET_TOP = 19.0        # z of the nut/stud pocket ceiling (stud end 17.8)
JSLOT_W = 4.8                # for the 8-32 stud shank (4.17)
JENTRY_D = 10.8              # entry hole for the 8-32 nylon lock nut (8.73 A/F, 10.1 A/C)
NUT_POCKET_W = 11.5
LOCK_ARC_DEG = 20.0          # twist to lock
POCKET_W = 27.0              # rear DC pocket (plug body 10 dia + cable bend)
POCKET_Y0, POCKET_Y1 = -13.5, 28.5
POCKET_DEPTH = 16.5
JACK_Y = 15.0                # jack axis offset toward 12 o'clock, keeps the cap stud axis + insert clear
JACK_PANEL_HOLE_D = 8.0      # 5.5x2.1 panel jack, 8 mm threaded barrel
JACK_WEB_T = 3.1
JACK_CAVITY = (14.0, 13.0)   # x, y; y from 8.5 to 21.5 (jack body 12 x 9 x 10 long)
JACK_CAVITY_Y_CENTER = 15.0
JACK_BODY_L = 10.0
BP_JACK_POCKET = (16.0, 13.0, 6.5)   # x, y, depth: rear pocket in the backplate for the jack body
CAP_RELIEF_D = 14.0          # relief behind the insert / behind the aluminum csk screw head
CAP_RELIEF_DEPTH = 4.5
FRONT_CHAN_W = 6.0
FRONT_CHAN_D = 4.0
CORD_CHAN_W = 9.5            # surface-cord channel, rear face, 6 o'clock
CORD_CHAN_D = 12.0
TAB_ANGLE = 250.0            # set-screw tab, about 6:40 (clears the 6 o'clock cord channel)
TAB_POCKET_R0, TAB_POCKET_R1 = 49.0, 55.6
TAB_POCKET_W = 10.0
TAB_POCKET_DEPTH = 13.5
SET_SCREW_Z = 9.5
SET_SCREW_HOLE_D = 3.2       # M3 clearance through the rim
SET_INSERT_D = 4.0           # M3 heat-set insert pilot
SET_INSERT_DEPTH = 5.7

# ---------------------------------------------------------------- steel wall plate (14 ga)
PLATE_D = 4.0 * IN           # 101.6
PLATE_T = 0.0747 * IN        # 1.90 (14 ga steel)
PLATE_HOLE_D = 30.0          # cable / plug pass-through slot width (plug body 10 dia at y=+15)
PLATE_HOLE_Y0, PLATE_HOLE_Y1 = -15.0, 22.0   # slot end-centres... overall y extent -15..+22 -> see wall_plate()
SLOT_W = 4.8                 # #8 / 6-32 screws
SLOT_HALF_DEG = 10.0         # +/- rotation for levelling
SLOT_R_GANG = 83.3 / 2       # single-gang / LV bracket 83.3 mm (mounting-report)
SLOT_R_ROUND = 88.9 / 2      # round / octagon box 88.9 mm (mounting-report)
SLOT_ANGLES_GANG = (90, 270)
SLOT_ANGLES_ROUND = (0, 180)
STUD_R = 33.0
STUD_ANGLES = (75, 195, 315)
STUD_HOLE_D = 4.22           # PEM FH-832 clinch hole (verify on PEM bulletin FH)
STUD_D = 0.164 * IN          # 4.17  8-32 major dia
STUD_L = 0.625 * IN          # 15.9  FH-832-10
NUT_AF = 11.0 / 32.0 * IN    # 8.73  8-32 nylon-insert lock nut across flats
NUT_H = 5.8
NUT_GAP = HUB_RECESS_DEPTH + JWEB_T + 0.6 - PLATE_T   # plate top to nut underside = 7.2
BEND_RI = 1.9                # inside bend radius = 1t
K_FACTOR = 0.44
TAB_W = 8.0
TAB_TOP_Z = 12.0
TAB_HOLE_D = 3.4
TAB_HOLE_Z = SET_SCREW_Z

# ---------------------------------------------------------------- dome caps (brass, plated)
CAP12_D = 1.5 * IN           # 38.1 (design-report sec. "Cap size and proportion")
CAP12_RIM_H = 1.6
CAP12_DOME_H = 8.4           # total 10.0 = 0.39"
CAP7_D = 48.0                # 1.89" chromed-45-adapter proportion (design-report)
CAP7_RIM_H = 2.0
CAP7_DOME_H = 6.5
CAP7_BOSS_D = 37.6           # centres in the 38.1 hole, replaces the plastic adapter
CAP7_BOSS_H = 1.6
CAP_BASE_R = 0.8
STUD_14_20_D = 0.25 * IN     # 6.35
CAP_STUD_L = 0.625 * IN      # 15.9 (5/8"): never protrudes behind the insert
CAP_STUD_RELIEF_D = 5.4
CAP_STUD_RELIEF_L = 1.0
FELT_WASHER = (25.4, 9.5, 3.2)       # OD, ID, T (Durofelt 1" x 3/8" x 1/8")
FELT_RING7 = (47.0, 39.0, 1.6)       # OD, ID, T  (custom die-cut, see README open questions)


def pol(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


def arc_slot_wire(r, a0, a1, w):
    """2D arc slot (Workplane XY) centred on radius r from angle a0 to a1 (deg), width w."""
    ro, ri = r + w / 2, r - w / 2
    am = (a0 + a1) / 2
    wp = (cq.Workplane("XY").moveTo(*pol(ro, a0))
          .threePointArc(pol(ro, am), pol(ro, a1))
          .threePointArc(pol(r, a1 + math.degrees(w / 2 / r)), pol(ri, a1))
          .threePointArc(pol(ri, am), pol(ri, a0))
          .threePointArc(pol(r, a0 - math.degrees(w / 2 / r)), pol(ro, a0))
          .close())
    return wp


def arc_slot(r, a0, a1, w, z0, z1):
    lo, hi = min(a0, a1), max(a0, a1)
    return arc_slot_wire(r, lo, hi, w).extrude(z1 - z0).translate((0, 0, z0))


def ring(ro, ri, h, z0=0.0):
    return cq.Workplane("XY").circle(ro).circle(ri).extrude(h).translate((0, 0, z0))


def cyl(d, h, x=0.0, y=0.0, z0=0.0):
    return cq.Workplane("XY").center(x, y).circle(d / 2).extrude(h).translate((0, 0, z0))


def box(sx, sy, sz, cx=0.0, cy=0.0, z0=0.0):
    return cq.Workplane("XY").box(sx, sy, sz, centered=(True, True, False)).translate((cx, cy, z0))


def box_y(sx, y0, y1, z0, z1):
    """Box centred on x=0 spanning y0..y1 and z0..z1."""
    lo, hi = min(y0, y1), max(y0, y1)
    return box(sx, hi - lo, z1 - z0, 0, (lo + hi) / 2, z0)


def radial_box(width_t, r0, r1, z0, z1, angle):
    """Box spanning radius r0..r1 along direction `angle`, tangential width width_t, z0..z1."""
    b = box(width_t, r1 - r0, z1 - z0, 0, (r0 + r1) / 2, z0)
    return b.rotate((0, 0, 0), (0, 0, 1), angle - 90)


# ================================================================ BACKPLATE (MDF / birch, CNC)
def backplate(d=BP12_D, t=BP_T, pads_out=True, pads_in=True, hub_screws=True):
    R = d / 2
    bp = cq.Workplane("XY").circle(R).extrude(t)
    # rim rabbet for the COB strip, centred on the rim
    z0 = (t - RABBET_W) / 2
    bp = bp.cut(ring(R + 1, R - RABBET_DEPTH, RABBET_W, z0))
    # insert bore 25/64" through
    bp = bp.cut(cyl(INSERT_BORE_D, t + 2, z0=-1))
    # lead notch at 6 o'clock from the rabbet floor to the back face
    bp = bp.cut(box_y(NOTCH_W, -(R + 1), -(R - RABBET_DEPTH - 3), -1, z0 + 0.5))
    # back-face lead channel from the notch to under the hub
    bp = bp.cut(box_y(BACK_CHAN_W, -(R - RABBET_DEPTH - 2), -60.0, -1, BACK_CHAN_D))
    # felt pad targets (0.5 mm spot) on the front face
    for ang in PAD_ANGLES:
        if pads_out and PAD_R_OUT + PAD_D / 2 < R - RABBET_DEPTH - 1:
            x, y = pol(PAD_R_OUT, ang)
            bp = bp.cut(cyl(PAD_D + 0.6, PAD_TARGET_DEPTH + 1, x, y, t - PAD_TARGET_DEPTH))
        if pads_in:
            x, y = pol(PAD_R_IN, ang)
            bp = bp.cut(cyl(PAD_D + 0.6, PAD_TARGET_DEPTH + 1, x, y, t - PAD_TARGET_DEPTH))
    # rear pocket for the DC jack body (under the hub, hidden by the record)
    px, py, pd = BP_JACK_POCKET
    bp = bp.cut(box(px, py, pd + 1, 0, JACK_Y, -1))
    # hub screws: #8 flat head from the front (hidden by the record), countersunk
    if hub_screws:
        pts = [pol(HUB_SCREW_R, a) for a in HUB_SCREW_ANGLES]
        bp = (bp.faces(">Z").workplane(origin=(0, 0, t)).pushPoints(pts)
              .cskHole(HUB_SCREW_CLR_D, HUB_SCREW_CSK_D, 90))
    return bp


def backplate_aluminum(d=BP12_D, t=5.0):
    """Flat waterjet/laser variant = the engineering report's FLOATING configuration.
    1/4-20 flat-head machine screw countersunk from the back into a 3/8" OD x 1" F-F aluminum standoff
    on the front; the record sits on the standoff, 1" forward of the plate. LED = 6x12 mm COB neon-flex
    ring on the back face (top-emitting, bends in-plane), see README."""
    R = d / 2
    bp = cq.Workplane("XY").circle(R).extrude(t)
    # 1/4-20 from the back: 5 mm plate takes an 82 deg countersunk flat head (flush);
    # 3 mm plate is too thin for the 3.7 mm head, so it gets a plain hole + pan head sitting in the hub relief
    if t >= 4.5:
        bp = bp.faces("<Z").workplane(origin=(0, 0, 0)).cskHole(AL_CLR_D, AL_CSK_D, 82)
    else:
        bp = bp.cut(cyl(AL_CLR_D, t + 2, z0=-1))
    # through cut-out for the DC jack body (record hides it)
    bp = bp.cut(box(BP_JACK_POCKET[0], BP_JACK_POCKET[1], t + 2, 0, JACK_Y, -1))
    pts = [pol(HUB_SCREW_R, a) for a in HUB_SCREW_ANGLES]
    bp = (bp.faces(">Z").workplane(origin=(0, 0, t)).pushPoints(pts)
          .cskHole(HUB_SCREW_CLR_D, min(HUB_SCREW_CSK_D, 2 * t - 0.4), 90))
    return bp


def standoff():
    """3/8 OD x 1 in, 1/4-20 F-F 6061 standoff (aluminumspacers.com AS38-1420-64), on the plate front."""
    return ring(STANDOFF_OD / 2, STUD_14_20_D / 2, STANDOFF_L)


PAN_HEAD_14_20 = (12.5, 3.4)   # dia, height (ASME B18.6.3 1/4-20 pan head, max)


def flat_head_14_20(t_plate):
    """1/4-20 x 5/8 machine screw from the back. t>=4.5: 82 deg flat head flush in the countersink.
    t<4.5: pan head proud of the back face (sits inside the hub's centre relief)."""
    if t_plate >= 4.5:
        head_h = (AL_CSK_D - AL_CLR_D) / 2 / math.tan(math.radians(41))
        head = (cq.Workplane("XY").circle(AL_CSK_D / 2).workplane(offset=head_h).circle(AL_CLR_D / 2).loft())
        shank = cyl(STUD_14_20_D, 15.9 - head_h, 0, 0, head_h)
        return head.union(shank)
    hd, hh = PAN_HEAD_14_20
    head = cyl(hd, hh, 0, 0, -hh)
    shank = cyl(STUD_14_20_D, 15.9 - hh, 0, 0, 0)
    return head.union(shank)


def neon_flex_ring(bp_d):
    """6 x 12 mm top-emitting COB neon flex laid on the back face, emitting toward the wall."""
    r = bp_d / 2 - NEON_RING_INSET
    return ring(r + 3.0, r - 3.0, 12.0, -12.0)


# ================================================================ HUB (PETG print)
def hub():
    R = HUB_D / 2
    h = cq.Workplane("XY").circle(R).extrude(HUB_T)
    h = h.edges("%CIRCLE").edges(">Z or <Z").fillet(HUB_FILLET)
    # rear recess for the steel plate + screw heads
    h = h.cut(cyl(2 * HUB_RECESS_R, HUB_RECESS_DEPTH + 1, z0=-1))
    # rear DC pocket (oval), 16.5 deep
    yc = (POCKET_Y0 + POCKET_Y1) / 2
    pocket = (cq.Workplane("XY").center(0, yc)
              .slot2D(POCKET_Y1 - POCKET_Y0, POCKET_W, 90).extrude(POCKET_DEPTH + 1).translate((0, 0, -1)))
    h = h.cut(pocket)
    # jack panel hole through the web, cavity for the jack body opening to the front
    h = h.cut(cyl(JACK_PANEL_HOLE_D, HUB_T, 0, JACK_Y, POCKET_DEPTH - 0.5))
    h = h.cut(box(JACK_CAVITY[0], JACK_CAVITY[1], HUB_T, 0, JACK_CAVITY_Y_CENTER, POCKET_DEPTH + JACK_WEB_T))
    # relief behind the insert (front face)
    h = h.cut(cyl(CAP_RELIEF_D, CAP_RELIEF_DEPTH + 1, 0, 0, HUB_T - CAP_RELIEF_DEPTH))
    # front lead channel, 6 o'clock, cavity -> rim
    h = h.cut(box_y(FRONT_CHAN_W, -(R + 1), JACK_CAVITY_Y_CENTER, HUB_T - FRONT_CHAN_D, HUB_T + 1))
    # rear surface-cord channel, 6 o'clock, pocket -> rim
    h = h.cut(box_y(CORD_CHAN_W, -(R + 1), -10.0, -1, CORD_CHAN_D))
    # J-slots: modelled in the LOCKED position (studs at STUD_ANGLES, entries +LOCK_ARC_DEG)
    zweb0 = HUB_RECESS_DEPTH
    zweb1 = HUB_RECESS_DEPTH + JWEB_T
    for a in STUD_ANGLES:
        ae = a + LOCK_ARC_DEG
        x, y = pol(STUD_R, ae)
        h = h.cut(cyl(JENTRY_D, NUT_POCKET_TOP - zweb0 + 0.5, x, y, zweb0 - 0.5))      # entry
        h = h.cut(arc_slot(STUD_R, a, ae, JSLOT_W, zweb0 - 0.5, zweb1 + 0.5))           # shank slot
        h = h.cut(arc_slot(STUD_R, a, ae, NUT_POCKET_W, zweb1, NUT_POCKET_TOP))         # nut pocket
    # set-screw tab pocket and the M3 hole through the rim
    h = h.cut(radial_box(TAB_POCKET_W, TAB_POCKET_R0, TAB_POCKET_R1, -1, TAB_POCKET_DEPTH, TAB_ANGLE))
    hole = (cq.Workplane("XY").circle(SET_SCREW_HOLE_D / 2).extrude(R + 2 - TAB_POCKET_R1 + 1)
            .translate((0, 0, TAB_POCKET_R1 - 1)))
    ins = (cq.Workplane("XY").circle(SET_INSERT_D / 2).extrude(SET_INSERT_DEPTH + 2)
           .translate((0, 0, R - SET_INSERT_DEPTH)))
    for c in (hole, ins):
        c = c.rotate((0, 0, 0), (0, 1, 0), 90)           # +Z axis -> +X radial
        c = c.translate((0, 0, SET_SCREW_Z))
        c = c.rotate((0, 0, 0), (0, 0, 1), TAB_ANGLE)
        h = h.cut(c)
    # front pilot holes for the #8 hub screws
    for a in HUB_SCREW_ANGLES:
        x, y = pol(HUB_SCREW_R, a)
        h = h.cut(cyl(HUB_SCREW_PILOT_D, HUB_SCREW_PILOT_DEPTH + 1, x, y, HUB_T - HUB_SCREW_PILOT_DEPTH))
    return h


# ================================================================ STEEL WALL PLATE (formed)
def bend_allowance(angle_deg=90.0, ri=BEND_RI, t=PLATE_T, k=K_FACTOR):
    return math.radians(angle_deg) * (ri + k * t)


def wall_plate():
    R = PLATE_D / 2
    t = PLATE_T
    p = cq.Workplane("XY").circle(R).extrude(t)
    yc = (PLATE_HOLE_Y0 + PLATE_HOLE_Y1) / 2
    p = p.cut(cq.Workplane("XY").center(0, yc).slot2D(PLATE_HOLE_Y1 - PLATE_HOLE_Y0, PLATE_HOLE_D, 90)
              .extrude(t + 2).translate((0, 0, -1)))
    for a in SLOT_ANGLES_GANG:
        p = p.cut(arc_slot(SLOT_R_GANG, a - SLOT_HALF_DEG, a + SLOT_HALF_DEG, SLOT_W, -1, t + 1))
    for a in SLOT_ANGLES_ROUND:
        p = p.cut(arc_slot(SLOT_R_ROUND, a - SLOT_HALF_DEG, a + SLOT_HALF_DEG, SLOT_W, -1, t + 1))
    for a in STUD_ANGLES:
        x, y = pol(STUD_R, a)
        p = p.cut(cyl(STUD_HOLE_D, t + 2, x, y, -1))
    # bent tab at TAB_ANGLE: profile in the (radial, z) plane, built along +Y then rotated
    ro = BEND_RI + t
    cz = t + BEND_RI                       # bend centre (r=R, z=cz)
    prof = (cq.Workplane("YZ")
            .moveTo(R - 2.0, 0)
            .lineTo(R, 0)
            .threePointArc((R + ro * math.sin(math.radians(45)), cz - ro * math.cos(math.radians(45))), (R + ro, cz))
            .lineTo(R + ro, TAB_TOP_Z)
            .lineTo(R + BEND_RI, TAB_TOP_Z)
            .lineTo(R + BEND_RI, cz)
            .threePointArc((R + BEND_RI * math.sin(math.radians(45)), cz - BEND_RI * math.cos(math.radians(45))), (R, t))
            .lineTo(R - 2.0, t)
            .close()
            .extrude(TAB_W / 2, both=True))
    tab_hole = (cq.Workplane("XZ").center(0, TAB_HOLE_Z).circle(TAB_HOLE_D / 2)
                .extrude(20, both=True).translate((0, R + BEND_RI + t / 2, 0)))
    prof = prof.cut(tab_hole)
    prof = prof.rotate((0, 0, 0), (0, 0, 1), TAB_ANGLE - 90)
    p = p.union(prof)
    return p


def wall_plate_flat_geometry():
    """Flat-pattern numbers for the DXF (bend line, tab length, hole position)."""
    R = PLATE_D / 2
    ba = bend_allowance()
    leg = TAB_TOP_Z - (PLATE_T + BEND_RI)
    hole_from_bend_tangent = TAB_HOLE_Z - (PLATE_T + BEND_RI)
    return dict(
        R=R, ba=ba, leg=leg,
        tab_end_r=R + ba + leg,
        bend_line_r=R + ba / 2,
        hole_r=R + ba + hole_from_bend_tangent,
    )


# ================================================================ DOME CAPS (brass bar, lathe)
def _dome_profile(wp, r_base, rim_h, dome_h):
    """Continue a profile from (r_base, 0) : base radius, rim band, spherical dome to the apex."""
    br = CAP_BASE_R
    # base edge radius
    wp = wp.lineTo(r_base - br, 0).threePointArc(
        (r_base - br + br * math.sin(math.radians(45)), br - br * math.cos(math.radians(45))), (r_base, br))
    wp = wp.lineTo(r_base, rim_h)
    sphR = (r_base ** 2 + dome_h ** 2) / (2 * dome_h)
    zc = rim_h + dome_h - sphR
    am = math.asin((rim_h - zc) / sphR)
    amid = (am + math.pi / 2) / 2
    wp = wp.threePointArc((sphR * math.cos(amid), zc + sphR * math.sin(amid)), (0, rim_h + dome_h))
    return wp


def dome_cap_12():
    r = CAP12_D / 2
    rs = STUD_14_20_D / 2
    L = CAP_STUD_L
    wp = (cq.Workplane("XZ")
          .moveTo(0, -L)
          .lineTo(rs - 0.5, -L)
          .lineTo(rs, -L + 0.5)
          .lineTo(rs, -CAP_STUD_RELIEF_L)
          .lineTo(CAP_STUD_RELIEF_D / 2, -CAP_STUD_RELIEF_L)
          .lineTo(CAP_STUD_RELIEF_D / 2, 0))
    wp = _dome_profile(wp, r, CAP12_RIM_H, CAP12_DOME_H)
    return wp.close().revolve(360, (0, 0, 0), (0, 1, 0))


def dome_cap_7():
    r = CAP7_D / 2
    rb = CAP7_BOSS_D / 2
    rs = STUD_14_20_D / 2
    L = CAP_STUD_L
    wp = (cq.Workplane("XZ")
          .moveTo(0, -L)
          .lineTo(rs - 0.5, -L)
          .lineTo(rs, -L + 0.5)
          .lineTo(rs, -CAP7_BOSS_H - CAP_STUD_RELIEF_L)
          .lineTo(CAP_STUD_RELIEF_D / 2, -CAP7_BOSS_H - CAP_STUD_RELIEF_L)
          .lineTo(CAP_STUD_RELIEF_D / 2, -CAP7_BOSS_H)
          .lineTo(rb - 0.4, -CAP7_BOSS_H)
          .lineTo(rb, -CAP7_BOSS_H + 0.4)
          .lineTo(rb, 0))
    wp = _dome_profile(wp, r, CAP7_RIM_H, CAP7_DOME_H)
    return wp.close().revolve(360, (0, 0, 0), (0, 1, 0))


# ================================================================ purchased / reference parts
def record(d=REC12_D, t=REC12_T, hole=REC_HOLE_D):
    return cq.Workplane("XY").circle(d / 2).circle(hole / 2).extrude(t)


def felt_washer(od, idd, t):
    return ring(od / 2, idd / 2, t)


def felt_pads(radii, t=PAD_T):
    pads = None
    for rr in radii:
        for a in PAD_ANGLES:
            x, y = pol(rr, a)
            c = cyl(PAD_D, t, x, y, 0)
            pads = c if pads is None else pads.union(c)
    return pads


def led_strip(bp_d):
    R = bp_d / 2
    z0 = (BP_T - RABBET_W) / 2 + (RABBET_W - LED_W) / 2
    return ring(R - RABBET_DEPTH + LED_T, R - RABBET_DEPTH, LED_W, z0)


def ez_lok_insert():
    return ring(INSERT_BORE_D / 2 - 0.02, STUD_14_20_D / 2, INSERT_L)


def pem_stud():
    return cyl(STUD_D, STUD_L, z0=PLATE_T)


def lock_nut():
    return (cq.Workplane("XY").polygon(6, NUT_AF / math.cos(math.radians(30))).extrude(NUT_H)
            .faces(">Z").workplane().hole(STUD_D + 0.3))


def wall_screw_head():
    """#8 pan head sitting on the plate top face."""
    return cyl(8.4, 2.5, z0=PLATE_T)


JACK_BARREL_L = 9.0


def dc_jack():
    """Panel-mount 5.5x2.1 DC jack: 8 mm threaded barrel + 12 x 9 x 10 body (DC-022B class envelope)."""
    barrel = cyl(JACK_PANEL_HOLE_D, JACK_BARREL_L, 0, JACK_Y, POCKET_DEPTH - JACK_BARREL_L)
    body = box(12.0, 9.0, JACK_BODY_L, 0, JACK_Y, POCKET_DEPTH + JACK_WEB_T)
    return barrel.union(body)


def dc_plug():
    """Straight 5.5x2.1 plug, mated: 10 mm sleeve over the barrel, body + cable toward the wall."""
    tip = POCKET_DEPTH - JACK_BARREL_L
    sleeve = ring(5.0, 4.2, JACK_BARREL_L - 1.0, tip).translate((0, JACK_Y, 0))
    body = cyl(10.0, 16.0, 0, JACK_Y, tip - 16.0)
    cable = cyl(4.6, 30.0, 0, JACK_Y, tip - 16.0 - 30.0)
    return sleeve.union(body).union(cable)


def set_screw():
    """M3 x 12 flat point, through the hub rim into the plate tab."""
    L = 12.0
    R = HUB_D / 2
    s = cq.Workplane("XY").circle(1.5).extrude(L).translate((0, 0, R - L))
    s = s.rotate((0, 0, 0), (0, 1, 0), 90).translate((0, 0, SET_SCREW_Z)).rotate((0, 0, 0), (0, 0, 1), TAB_ANGLE)
    return s
