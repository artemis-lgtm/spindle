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
RABBET_W = 10.2              # 0.40" rim rabbet for an 8 mm COB strip. 7 in backplate ONLY since 12 in rev C (see HALO_ below)
RABBET_DEPTH = 1.5
LED_W = 8.0
LED_T = 1.6
NOTCH_W = 6.35               # 0.25" lead notch at 6 o'clock (7 in backplate only, with its rim rabbet)
BACK_CHAN_W = 6.0
BACK_CHAN_D = 4.0
BACK_CHAN_R0 = 60.0          # back-face lead channel starts under the hub (hub R 63.5) ...
BACK_CHAN_R1 = 97.0          # ... 12 in rev C: and stops 3 short of the cork ring (ID R 100), so the cork sits on unbroken MDF
# ---- HEAT-SAFE HALO, layout D (2026-11-11; cad/THERMAL.md, cad/FIXES-heat-layout.md). 12 in MDF sconce, plain cap AND lit cap.
# Why: the record (304.8) is wider than the backplate (266.7). With the strip on the rim, the record's outer 19 mm hung
# 3.45 mm in front of the LEDs with only air between. The strip now sits on the BACK face, LEDs toward the wall, on a
# 1 mm aluminium ring that spreads its heat, with a 1.6 mm (1/16 in) cork ring between the aluminium and the MDF. The LEDs have no
# line of sight to the record, and cork + 12.7 of MDF sit between them. This is also how the approved photos were lit.
# Stack from the backplate back face toward the wall: cork 1.6, aluminium 1.0, strip.
HALO_RING_OD = 260.0         # RS-HR-12 (aluminium) and RS-CK-12 (cork) share OD and ID: 3.35 inside the backplate rim
HALO_RING_ID = 200.0         # 36.5 outside the hub (R 63.5)
HEAT_RING_T = 1.0            # 5052-H32, 0.040 in, laser cut, flat
CORK_RING_T = 1.6            # 1/16 in cork sheet. Was 2.0 until the live quotes of 2026-11-11: 2 mm sheet is not a stocked size,
                             # 1/16 in is (sourcing/quotes-2026-11-11). Heat cost of the thinner cork: 0.1 K, see THERMAL.md.
HALO_STRIP_R = 115.0         # centreline of the 8 mm strip on the aluminium's wall-facing face: R 111 to 119
# Fastening: the cork is laid on the aluminium on the bench (stuck to it if the cork has an adhesive face), then 4 screws
# clamp the pair to the MDF. No adhesive is asked to hold on painted MDF, and the ring can come off for service. Same #4 x 3/8 screw as the P-clip.
HALO_SCREW_R = 105.5         # bolt circle, in the 11 mm band between the ring ID (R 100) and the strip (R 111)
HALO_SCREW_ANGLES = (45, 135, 225, 315)   # clear of the felt targets (90/210/330) and the 6 o'clock lead channel (270)
HALO_SCREW_L = 0.375 * IN    # 9.525: #4 x 3/8 pan head, Type AB (sheet metal / wood)
HALO_SCREW_MAJOR_D = 2.9     # #4 major diameter
HALO_SCREW_ROOT_D = 2.1      # #4 Type AB root diameter (the solid model carries the shank at the root, like every thread here)
HALO_SCREW_HEAD = (5.6, 2.1) # dia, height: #4 pan head, cross recess, ASME B18.6.3 max
HEAT_RING_HOLE_D = 3.3       # #4 clearance in the aluminium
CORK_RING_HOLE_D = 4.0       # punched, loose
HALO_PILOT_D = 2.2           # pilot in the MDF back face (confirm on the first article: no bulge on the front face)
HALO_PILOT_DEPTH = 8.0       # screw goes 6.9 into the MDF; 4.7 of MDF stays in front of the pilot
PAD_D = 12.7                 # 1/2" felt pad
PAD_T = 1.6                  # 1/16"
PAD_TARGET_DEPTH = 0.5
PAD_R_OUT = 120.0            # rev B (review M11b): was 5.00 in (127), where the D 13.3 target would have broken through the
                             # rim rabbet, so the old guard silently skipped all three outer pockets. 120 leaves 4.2 of MDF.
PAD_R_IN = 2.75 * IN         # 69.85
PAD_ANGLES = (90, 210, 330)  # one at 12 o'clock
REC_SEAT_H = PAD_T - PAD_TARGET_DEPTH   # 1.1: record back face above the backplate FRONT face. The pads sit IN their 0.5
                             # targets, so the record is 1.1 off the face, not 1.6 (the rev C stack used 1.6).
# Centre backing ring (review M1). Directly behind the cap felt, so the clamp load runs felt - record - felt in a straight
# line and the record is never bent toward the insert. Die-cut 1/16 in adhesive felt, same blank as the cap felt.
CENTER_RING = (31.75, 9.5, 1.6)          # OD, ID, T free (12 in sconce)
CENTER_RING_SET = 0.5                    # how much the ring compresses under the cap clamp load (calc, bench-check on the
                                         # first article and edit THIS number; the pocket depth below follows it)
CENTER_RING_LOADED_T = CENTER_RING[2] - CENTER_RING_SET             # 1.1
CENTER_POCKET_DEPTH = round(max(0.0, CENTER_RING_LOADED_T - REC_SEAT_H), 3)   # 0.0: loaded ring top = free pad top
CENTER_WITNESS_CLR = 0.65                # scored witness circle = ring OD + 0.65 (D 32.4 for the 12 in ring)
CENTER_WITNESS_W, CENTER_WITNESS_DEPTH = 0.4, 0.15
assert abs((CENTER_RING_LOADED_T - CENTER_POCKET_DEPTH) - REC_SEAT_H) <= 0.05, "centre ring must be coplanar with the pads (record flatness)"
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
LOCK_ENTRY_SIGN = -1         # entry holes sit at (stud angle - 20) in the +Z (room-side) view => lock = CLOCKWISE from the room
# rev B (review M10): the panel jack is GONE. A straight barrel plug could never mate with a jack whose mouth sat 7.5 mm off
# the wall (the plug body and cable would have been inside the drywall). Power now enters on a 150 mm 18 AWG pigtail that
# ends in an inline female 5.5 x 2.1 jack, clamped by a P-clip in the rear pocket (real strain relief). Surface route: the
# pigtail turns down the 6 o'clock channel and mates behind the backplate. In-wall route: it goes back through the plate
# slot and mates inside the wall. Names keep the JACK_ prefix so the history reads straight.
POCKET_W = 27.0              # rear cable pocket (pigtail bend + P-clip)
POCKET_Y0, POCKET_Y1 = -13.5, 22.0   # rev B: was 28.5; the shorter pocket no longer cuts the J-web under the 75 deg stud
POCKET_DEPTH = 12.0          # rev B: was 16.5 (jack barrel); = cord channel depth. Frees depth for the label-light module.
JACK_Y = 15.0                # cable pass-through offset toward 12 o'clock, keeps the cap stud axis + insert clear
CABLE_HOLE_D = 6.5           # rev B: pigtail pass-through in the web (was the D 8.0 panel-jack hole)
JACK_WEB_T = 3.1
JACK_CAVITY = (14.0, 13.0)   # x, y; y from 8.5 to 21.5: splice cavity (pigtail to LED leads), opens to the front
JACK_CAVITY_Y_CENTER = 15.0
BP_JACK_POCKET = (16.0, 13.0, 6.5)   # x, y, depth: rear pocket in the backplate over the splice cavity (solder + heat-shrink)
PIGTAIL_L = 150.0            # free length beyond the P-clip, 18 AWG 2-conductor zip cord
PIGTAIL_CORD = (5.0, 2.6)    # cord section, wide x thick (18/2 zip cord class, estimate)
INLINE_JACK = (11.5, 28.0)   # dia, length: moulded inline female 5.5 x 2.1 (CCTV pigtail class, UNVERIFIED envelope)
INLINE_PLUG = (10.5, 22.0)   # dia, length of the adapter's straight plug body beyond the jack (UNVERIFIED envelope)
CLIP_POS = (-9.5, 4.0)       # P-clip screw pilot in the pocket ceiling (#4 x 3/8 pan head, nylon 1/4 in P-clip)
CLIP_PILOT_D, CLIP_PILOT_DEPTH = 2.4, 6.0
CAP_RELIEF_D = 14.0          # relief behind the insert / behind the aluminum csk screw head
CAP_RELIEF_DEPTH = 9.1       # rev B: was 4.5. Room for the long-travel centre contact of the lit sconce (sconce_lit.py);
                             # 4.3 of PETG stays between the relief floor and the rear pocket ceiling.
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
STUD_14_20_MAJOR_MAX = 6.322 # 1/4-20 UNC-2A major dia max (ASME B1.1), before plating
CAP_STUD_RELIEF_D = 5.4
CAP_STUD_RELIEF_L = 1.0
FELT_WASHER = (31.75, 9.5, 1.6)      # OD, ID, T: 1-1/4" x 3/8" x 1/16" adhesive felt, sits in the cap recess (rev B).
                                     # NOT a stock Durofelt size (their page lists only SAW1GY 1 x 3/8 x 1/8 and SAW12BK
                                     # 1/2 x 1/4 x 1/16, checked 2026-11-11): die-cut from 1/16 in adhesive felt sheet.
FELT_LOADED_T = 1.1                  # 1/16 in felt under the clamp load (calc): free 1.6, about 1.1 loaded
# rev D (review M5): a clear PET label-saver washer sits between every cap and the label, so when the cap is turned the
# slip happens on PET and never on the paper. Matte face to the label (grips paper), gloss face to the cap.
PET_WASHER = (37.5, 7.5, 0.25)       # OD, ID, T under RS-CAP-12 and RS-CAP-12L
PET_WASHER7 = (47.5, 38.6, 0.25)     # under RS-CAP-7
# rev D (review S1): smooth unthreaded shoulder under the cap. The record hangs and centres on it (0.14..0.27 slop in a
# 7.24..7.32 hole) instead of riding on thread crests with 0.9 of slop.
CAP_SHOULDER_D = 7.10                # +0 / -0.05
CAP_SHOULDER_L = 2.0                 # below the contact face; must stay above the insert top with the thinnest record
REC_HOLE_MIN = 7.24
# rev B (2026-11-10): the felt hides in an underside recess so the chrome band seats ~0.3 mm off the label and the cap
# reads as one solid piece. Rev A's 1/8" felt under a flat underside left a 3.2 mm shadow gap.
CAP12_RECESS_D = 33.0
CAP12_RECESS_H = 1.0
FELT12_PROUD = FELT_WASHER[2] - CAP12_RECESS_H   # 0.6 free, ~0.3 compressed
CAP12_STUD_L = 11.95         # rev D (2026-11-11 Fable 5.2 review M5): rev C 11.70 + 0.25 for the PET washer. Same length as
                             # the lit RS-CAP-12L stud (asserted in sconce_lit.py). Tolerance +/-0.05 on the drawing.
CAP12_RECESS_TOL = 0.05      # recess depth 1.00 +/-0.05 (was under the +/-0.3 general tolerance)
CAP_DOG_TOL = (0.0, -0.10)   # dog point D 4.80 +0/-0.10: must clear the insert's 4.98 minimum minor diameter
INSERT_MINOR_MIN, INSERT_MINOR_MAX = 4.98, 5.26   # 1/4-20 UNC-2B internal minor dia (ASME B1.1)
CAP_STUD_DOG_D = 4.8         # rev C: unthreaded dog point at the tip (1/4-20 minor dia) ...
CAP_STUD_DOG_L = 1.5         # ... 1.5 long: pilots the stud into the insert so it cannot cross-thread, and the record's hole
                             # slides over a smooth pilot instead of thread crests (no vinyl shavings into the insert)
FELT_RING7 = (47.0, 39.0, 1.6)       # OD, ID, T  (custom die-cut, see README open questions)
CENTER_RING7 = FELT_RING7            # 7 in sconce: the backing ring mirrors the 7 in cap's felt ring (the 38.1 hole is
                                     # wider than the 12 in ring, so that ring would support nothing)
CAP7_STUD_L = 12.6           # rev C (review M7): was 5/8 in (15.875), which drove a lit sconce's centre contact 4+ mm too deep.
                             # Chosen so the TIP lands where the RS-CAP-12 tip lands (see cap_tip_above_seat, asserted).


def cap_tip_above_seat(which="12", rec_t=None, felt=None):
    """Height of the stud tip relative to the record seat plane (record back face), mm, negative = behind it.
    Nominal loaded state: 12 in cap felt compressed to half its 0.6 proud, 7 in felt ring at FELT_LOADED_T."""
    if which == "12":
        return (REC12_T if rec_t is None else rec_t) + PET_WASHER[2] + (FELT12_PROUD / 2 if felt is None else felt) - CAP12_STUD_L
    return (REC7_T if rec_t is None else rec_t) + PET_WASHER7[2] + (FELT_LOADED_T if felt is None else felt) - CAP7_STUD_L


assert abs(cap_tip_above_seat("12") - cap_tip_above_seat("7")) <= 0.05, \
    "RS-CAP-7 and RS-CAP-12 stud tips must land at the same depth (a 7 in cap must never over-drive a lit sconce)"


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
def halo_layout(d):
    """Which halo a backplate diameter gets. "back" = layout D (strip on the back face on the aluminium + cork rings).
    "rim" = the old rim-rabbet strip. Only the 12 in plate is on layout D: on the 7 in plate the back face outside the hub
    is 9.35 mm wide (hub R 63.5 to R 72.85 at the same 3.35 rim margin), which leaves an 8.35 ring for an 8 mm strip
    and no room for a screw, so that variant is deliberately unchanged (cad/FIXES-heat-layout.md)."""
    return "back" if d > 200 else "rim"


def backplate(d=BP12_D, t=BP_T, pads_out=True, pads_in=True, hub_screws=True, center_ring=None, halo=None):
    """12 in = rev C (2026-11-11): rim rabbet and 6 o'clock rim notch DELETED, back channel shortened to R 60..97,
    4 pilots added on the back face for the heat-ring screws. 7 in = rev B geometry, unchanged (halo="rim")."""
    R = d / 2
    if center_ring is None:
        center_ring = CENTER_RING if d > 200 else CENTER_RING7
    if halo is None:
        halo = halo_layout(d)
    bp = cq.Workplane("XY").circle(R).extrude(t)
    rabbet = RABBET_DEPTH if halo == "rim" else 0.0
    z0 = (t - RABBET_W) / 2
    if halo == "rim":
        # rim rabbet for the COB strip, centred on the rim
        bp = bp.cut(ring(R + 1, R - RABBET_DEPTH, RABBET_W, z0))
    # insert bore 25/64" through
    bp = bp.cut(cyl(INSERT_BORE_D, t + 2, z0=-1))
    if halo == "rim":
        # lead notch at 6 o'clock from the rabbet floor to the back face
        bp = bp.cut(box_y(NOTCH_W, -(R + 1), -(R - RABBET_DEPTH - 3), -1, z0 + 0.5))
        # back-face lead channel from the notch to under the hub
        bp = bp.cut(box_y(BACK_CHAN_W, -(R - RABBET_DEPTH - 2), -BACK_CHAN_R0, -1, BACK_CHAN_D))
    else:
        # back-face lead channel: from just inside the cork ring to under the hub, where the hub's front channel takes over
        bp = bp.cut(box_y(BACK_CHAN_W, -BACK_CHAN_R1, -BACK_CHAN_R0, -1, BACK_CHAN_D))
        # pilots for the 4 heat-ring screws, back face
        for a in HALO_SCREW_ANGLES:
            x, y = pol(HALO_SCREW_R, a)
            bp = bp.cut(cyl(HALO_PILOT_D, HALO_PILOT_DEPTH + 1, x, y, -1))
    # felt pad targets (0.5 mm spot) on the front face
    if pads_out and PAD_R_OUT + (PAD_D + 0.6) / 2 > R - rabbet - 3.0:
        raise ValueError("outer felt targets break through the rim: move PAD_R_OUT in (never skip them silently)")
    for ang in PAD_ANGLES:
        if pads_out:
            x, y = pol(PAD_R_OUT, ang)
            bp = bp.cut(cyl(PAD_D + 0.6, PAD_TARGET_DEPTH + 1, x, y, t - PAD_TARGET_DEPTH))
        if pads_in:
            x, y = pol(PAD_R_IN, ang)
            bp = bp.cut(cyl(PAD_D + 0.6, PAD_TARGET_DEPTH + 1, x, y, t - PAD_TARGET_DEPTH))
    # centre backing ring seat (review M1): pocket if the ring needs one to finish coplanar with the pads, plus a scored
    # witness circle just outside the ring so the assembler can see it is concentric
    r_w = (center_ring[0] + CENTER_WITNESS_CLR) / 2
    if CENTER_POCKET_DEPTH > 0:
        bp = bp.cut(cyl(2 * r_w, CENTER_POCKET_DEPTH + 1, 0, 0, t - CENTER_POCKET_DEPTH))
    else:
        bp = bp.cut(ring(r_w + CENTER_WITNESS_W / 2, r_w - CENTER_WITNESS_W / 2, CENTER_WITNESS_DEPTH + 1, t - CENTER_WITNESS_DEPTH))
    # rear pocket over the hub's splice cavity (under the hub, hidden by the record)
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
AL_SCREW_L = 0.625 * IN        # 1/4-20 x 5/8 machine screw from the back of the aluminum plate into the standoff


def flat_head_14_20(t_plate):
    """1/4-20 x 5/8 machine screw from the back. t>=4.5: 82 deg flat head flush in the countersink.
    t<4.5: pan head proud of the back face (sits inside the hub's centre relief)."""
    if t_plate >= 4.5:
        head_h = (AL_CSK_D - AL_CLR_D) / 2 / math.tan(math.radians(41))
        head = (cq.Workplane("XY").circle(AL_CSK_D / 2).workplane(offset=head_h).circle(AL_CLR_D / 2).loft())
        shank = cyl(STUD_14_20_D, AL_SCREW_L - head_h, 0, 0, head_h)
        return head.union(shank)
    hd, hh = PAN_HEAD_14_20
    head = cyl(hd, hh, 0, 0, -hh)
    shank = cyl(STUD_14_20_D, AL_SCREW_L - hh, 0, 0, 0)
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
    # pigtail pass-through in the web, splice cavity opening to the front; P-clip screw pilot in the pocket ceiling
    h = h.cut(cyl(CABLE_HOLE_D, HUB_T, 0, JACK_Y, POCKET_DEPTH - 0.5))
    h = h.cut(cyl(CLIP_PILOT_D, CLIP_PILOT_DEPTH + 0.5, CLIP_POS[0], CLIP_POS[1], POCKET_DEPTH - 0.5))
    h = h.cut(box(JACK_CAVITY[0], JACK_CAVITY[1], HUB_T, 0, JACK_CAVITY_Y_CENTER, POCKET_DEPTH + JACK_WEB_T))
    # relief behind the insert (front face)
    h = h.cut(cyl(CAP_RELIEF_D, CAP_RELIEF_DEPTH + 1, 0, 0, HUB_T - CAP_RELIEF_DEPTH))
    # front lead channel, 6 o'clock, cavity -> rim
    h = h.cut(box_y(FRONT_CHAN_W, -(R + 1), JACK_CAVITY_Y_CENTER, HUB_T - FRONT_CHAN_D, HUB_T + 1))
    # rear surface-cord channel, 6 o'clock, pocket -> rim
    h = h.cut(box_y(CORD_CHAN_W, -(R + 1), -10.0, -1, CORD_CHAN_D))
    # J-slots: modelled in the LOCKED position (studs at STUD_ANGLES, entries at LOCK_DIR * LOCK_ARC_DEG from them).
    # rev B (review M11d): entries are now at stud angle MINUS 20, so the hub is hung 20 deg anticlockwise (seen from the
    # room) and locks CLOCKWISE, as the install sheet says, and tightening the cap drives the bayonet home, not open.
    zweb0 = HUB_RECESS_DEPTH
    zweb1 = HUB_RECESS_DEPTH + JWEB_T
    for a in STUD_ANGLES:
        ae = a + LOCK_ENTRY_SIGN * LOCK_ARC_DEG
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


def stud_tip(wp, L, rs=STUD_14_20_D / 2):
    """Stud tip profile from the axis at z=-L up to the thread major diameter: 0.3 chamfer, dog point
    D CAP_STUD_DOG_D x CAP_STUD_DOG_L (unthreaded pilot), 45 deg run-in to the thread (rev C, 2026-11-10)."""
    rd = CAP_STUD_DOG_D / 2
    return (wp.moveTo(0, -L)
              .lineTo(rd - 0.3, -L)
              .lineTo(rd, -L + 0.3)
              .lineTo(rd, -L + CAP_STUD_DOG_L)
              .lineTo(rs, -L + CAP_STUD_DOG_L + (rs - rd)))


def dome_cap_12():
    r = CAP12_D / 2
    rs = STUD_14_20_D / 2
    L = CAP12_STUD_L
    h = CAP12_RECESS_H
    sl, sr = CAP_SHOULDER_L, CAP_SHOULDER_D / 2
    wp = stud_tip(cq.Workplane("XZ"), L)
    wp = (wp.lineTo(rs, -sl - CAP_STUD_RELIEF_L)                   # thread ends at the relief groove under the shoulder
          .lineTo(CAP_STUD_RELIEF_D / 2, -sl - CAP_STUD_RELIEF_L)
          .lineTo(CAP_STUD_RELIEF_D / 2, -sl)
          .lineTo(sr - 0.2, -sl).lineTo(sr, -sl + 0.2)              # smooth shoulder D 7.10 (rev D), 0.2 lead-in
          .lineTo(sr, h)
          .lineTo(CAP12_RECESS_D / 2, h)
          .lineTo(CAP12_RECESS_D / 2, 0))
    wp = _dome_profile(wp, r, CAP12_RIM_H, CAP12_DOME_H)
    return wp.close().revolve(360, (0, 0, 0), (0, 1, 0))


def dome_cap_7():
    r = CAP7_D / 2
    rb = CAP7_BOSS_D / 2
    rs = STUD_14_20_D / 2
    L = CAP7_STUD_L
    wp = stud_tip(cq.Workplane("XZ"), L)
    wp = (wp.lineTo(rs, -CAP7_BOSS_H - CAP_STUD_RELIEF_L)
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
    """Pads seated IN their 0.5 targets: local z = 0 is the backplate front face, pad top at REC_SEAT_H."""
    pads = None
    for rr in radii:
        for a in PAD_ANGLES:
            x, y = pol(rr, a)
            c = cyl(PAD_D, t, x, y, -PAD_TARGET_DEPTH)
            pads = c if pads is None else pads.union(c)
    return pads


def center_ring(spec=CENTER_RING):
    """Centre backing ring at its LOADED thickness; local z = 0 is the backplate front face."""
    return ring(spec[0] / 2, spec[1] / 2, CENTER_RING_LOADED_T, -CENTER_POCKET_DEPTH)


def pet_washer(spec=PET_WASHER):
    return ring(spec[0] / 2, spec[1] / 2, spec[2])


def led_strip_rim(bp_d):
    """Rim strip in the rim rabbet, LEDs facing outward. 7 in sconce only (see halo_layout)."""
    R = bp_d / 2
    z0 = (BP_T - RABBET_W) / 2 + (RABBET_W - LED_W) / 2
    return ring(R - RABBET_DEPTH + LED_T, R - RABBET_DEPTH, LED_W, z0)


# ---- heat-safe halo stack (layout D). Local z = 0 is the backplate BACK face; the stack grows toward the wall (-z).
HALO_Z_CORK = -CORK_RING_T                         # cork: -1.6 .. 0
HALO_Z_ALU = HALO_Z_CORK - HEAT_RING_T             # aluminium: -2.6 .. -1.6
HALO_Z_STRIP = HALO_Z_ALU - LED_T                  # strip: -4.2 .. -2.6, LEDs on the -z (wall) face
HALO_STACK_H = -HALO_Z_STRIP                       # 4.2 at the strip
HALO_STACK_H_AT_SCREW = -HALO_Z_ALU + HALO_SCREW_HEAD[1]   # 4.7 at a screw head


def _halo_holes(shape, hole_d, t, z0):
    for a in HALO_SCREW_ANGLES:
        x, y = pol(HALO_SCREW_R, a)
        shape = shape.cut(cyl(hole_d, t + 2, x, y, z0 - 1))
    return shape


def heat_ring():
    """RS-HR-12: 5052-H32 aluminium, 1.0 thick, OD 260, ID 200, 4x D 3.3 on R 105.5. Flat, laser cut. Part-local:
    z = 0 is the face that takes the cork, z = HEAT_RING_T is the wall-facing face that takes the LED strip."""
    return _halo_holes(ring(HALO_RING_OD / 2, HALO_RING_ID / 2, HEAT_RING_T), HEAT_RING_HOLE_D, HEAT_RING_T, 0.0)


def cork_ring():
    """RS-CK-12: 1.6 (1/16 in) cork, same OD / ID, 4x D 4.0 on R 105.5, adhesive on one face (onto the aluminium)."""
    return _halo_holes(ring(HALO_RING_OD / 2, HALO_RING_ID / 2, CORK_RING_T), CORK_RING_HOLE_D, CORK_RING_T, 0.0)


def heat_ring_placed():
    """Aluminium ring in the backplate frame (back face at z = 0)."""
    return heat_ring().translate((0, 0, HALO_Z_ALU))


def cork_ring_placed():
    return cork_ring().translate((0, 0, HALO_Z_CORK))


def led_strip_back():
    """8 mm strip on the aluminium ring's wall-facing face, centred on R 115, LEDs toward the wall. Backplate frame."""
    return ring(HALO_STRIP_R + LED_W / 2, HALO_STRIP_R - LED_W / 2, LED_T, HALO_Z_STRIP)


def halo_screw(angle):
    """#4 x 3/8 pan head through the aluminium and the cork into the MDF pilot. Backplate frame. Shank at the root dia."""
    x, y = pol(HALO_SCREW_R, angle)
    hd, hh = HALO_SCREW_HEAD
    return cyl(hd, hh, x, y, HALO_Z_ALU - hh).union(cyl(HALO_SCREW_ROOT_D, HALO_SCREW_L, x, y, HALO_Z_ALU))


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


# ---- power pigtail (rev B, review M10), modelled on the SURFACE-cord route: the worst case for space
CORD_Z0 = 6.0                 # cord rides over the wall plate (1.9) and the wall-screw heads (4.4) in the 12 deep channel
PIGTAIL_EXIT = 10.0           # cord length past the hub rim before the inline jack body starts


def pigtail_cord():
    """18/2 zip cord: through the web hole, along the pocket ceiling past the P-clip, down the 6 o'clock channel."""
    w, t = PIGTAIL_CORD
    R = HUB_D / 2
    stub = cyl(min(w, CABLE_HOLE_D - 1.0), JACK_WEB_T + 3.0, 0, JACK_Y, POCKET_DEPTH - 0.1)       # in the web hole
    a = box_y(w, -11.0, JACK_Y, POCKET_DEPTH - 0.2 - t, POCKET_DEPTH - 0.2)                         # ceiling run
    b = box_y(w, -12.6, -10.6, CORD_Z0, POCKET_DEPTH - 0.2)                                          # drop into the channel
    c = box_y(w, -(R + PIGTAIL_EXIT), -10.6, CORD_Z0, CORD_Z0 + t)                                   # channel run to the jack
    return stub.union(a).union(b).union(c)


def cord_clip():
    """Nylon P-clip on the pocket ceiling: strap under the cord + screw tab at CLIP_POS."""
    w, t = PIGTAIL_CORD
    z1 = POCKET_DEPTH
    zc = POCKET_DEPTH - 0.2 - t
    y0, y1 = CLIP_POS[1] - 2.5, CLIP_POS[1] + 2.5
    tab = box(5.0, y1 - y0, z1 - (zc - 0.7), CLIP_POS[0], CLIP_POS[1], zc - 0.7)
    strap = box(w / 2 + 0.7 - (CLIP_POS[0] + 2.5), y1 - y0, 0.6, (w / 2 + 0.7 + CLIP_POS[0] + 2.5) / 2, CLIP_POS[1], zc - 0.7)
    side = box(0.6, y1 - y0, z1 - (zc - 0.7), w / 2 + 0.4, CLIP_POS[1], zc - 0.7)
    return tab.union(strap).union(side)


def _cyl_y(d, y0, y1, z):
    """Cylinder along +Y from y0 to y1, axis at x = 0, height z."""
    c = cyl(d, y1 - y0).rotate((0, 0, 0), (1, 0, 0), -90)        # +Z axis -> +Y
    return c.translate((0, y0, z))


def inline_jack():
    """Inline female 5.5 x 2.1 on the end of the pigtail, lying in the wall gap below the hub, behind the backplate."""
    R = HUB_D / 2
    d, ln = INLINE_JACK
    y1 = -(R + PIGTAIL_EXIT)
    return _cyl_y(d, y1 - ln, y1, CORD_Z0 + PIGTAIL_CORD[1] / 2)


def inline_plug():
    """The adapter's straight plug mated into the inline jack, plus 20 mm of its cable."""
    R = HUB_D / 2
    y1 = -(R + PIGTAIL_EXIT) - INLINE_JACK[1]
    z = CORD_Z0 + PIGTAIL_CORD[1] / 2
    return _cyl_y(INLINE_PLUG[0], y1 - INLINE_PLUG[1], y1, z).union(_cyl_y(4.6, y1 - INLINE_PLUG[1] - 20.0, y1 - INLINE_PLUG[1], z))


def set_screw():
    """M3 x 12 flat point, through the hub rim into the plate tab."""
    L = 12.0
    R = HUB_D / 2
    s = cq.Workplane("XY").circle(1.5).extrude(L).translate((0, 0, R - L))
    s = s.rotate((0, 0, 0), (0, 1, 0), 90).translate((0, 0, SET_SCREW_Z)).rotate((0, 0, 0), (0, 0, 1), TAB_ANGLE)
    return s
