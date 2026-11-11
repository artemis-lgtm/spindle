"""
RS-CAP-12L "label light": the lit version of the 12 in dome cap, plus the hub-side contact module.
CadQuery 2.8, mm. Same conventions as sconce_cad.py.

REV B (2026-11-11, Fable 5.2 pessimist review, cad/REVIEW-fable52.md; every change is listed in cad/FIXES-fable52.md).
Rev A / A.1 are SUPERSEDED: they could not be assembled as drawn (the D-key stood taller than the LED PCB) and the centre
spring pin had 0.09 mm of margin for all tolerances.

Cap-local frame: z = 0 is the cap's contact face (foot face, the plane the felt recess opens into), +Z toward the
room, the stud goes -Z. Hub-module frame: z = 0 is the BACKPLATE BACK FACE (= insert back end), +Z toward the room.

Power path (coaxial through the 1/4-20 stud, see label-light/DESIGN.md):
  +12 V : pigtail -> D1 -> CCR (20 mA) on the hub PCB -> spring -> gold plunger in the PEEK guard tube -> gold pin head at
          the stud tip -> pin in a PEEK sleeve inside the hollow stud -> PTFE wire up the bore -> LED PCB
  return: LED PCB (rings on BOTH faces: column top below, dome boss above) -> brass core -> stud thread -> E-Z Lok insert
          -> return spring pin (Mill-Max 0919) on the insert's back end -> hub PCB -> pigtail
"""
import math
import cadquery as cq
import sconce_cad as S

IN = 25.4
REV = "B"

# ---------------------------------------------------------------- stack / thread
# Rev B: the lit cap has NO felt and NO felt recess (see FLANGE_T). Its flat nickel flange sits on the PET label washer, so
# its contact face is 0.3 lower than the plain cap's (whose felt stands ~0.3 proud when tightened). The stud is 0.3 shorter
# to match, so both caps put their TIP at the same depth: the assert is on tip position, not on length (review M7).
LC_STUD_L = 11.65                # from the contact face (flange underside)
LC_STUD_D = S.STUD_14_20_D       # 6.35
LC_STUD_MINOR_D = 4.80           # 1/4-20 UNC-2A external minor (approx, rolled/cut)
LC_INSERT_MINOR_D = S.INSERT_MINOR_MIN       # 4.98 MIN (ASME B1.1); E-Z Lok 400-4 internal thread
LC_INSERT_MINOR_MAX = S.INSERT_MINOR_MAX     # 5.26
LC_RELIEF_D, LC_RELIEF_L = S.CAP_STUD_RELIEF_D, S.CAP_STUD_RELIEF_L   # thread relief groove, now BELOW the smooth shoulder
# Stepped axial bore (review M8): the PEEK sleeve seats on a shoulder, so the contact force can never walk it up the bore.
LC_BORE_D = 3.15                 # press fit for the 3.175 PEEK sleeve, from the tip
SLEEVE_OD, SLEEVE_ID, SLEEVE_L = 3.175, 1.60, 10.0       # turned PEEK (was cut tubing): OD 1/8 in, bore 1.60, 10.0 long
LC_BORE_STEP = SLEEVE_L          # D 3.15 runs exactly one sleeve length deep, then steps down to the wire bore
LC_WIRE_BORE_D = 2.2             # above the shoulder: PTFE lead only
PIN_D, PIN_L = 1.588, 9.0        # 1/16 in brass C360 shank, Au over Ni; PIN_L includes the head
PIN_HEAD_D, PIN_HEAD_H = 2.4, 0.5   # head at the CONTACT end, seated in a counterbore in the sleeve's tip end: the spring
                                 # pushes the pin INTO the cap, and the head cannot pass the sleeve bore (positive stop).
                                 # (The review asked for the head on the sleeve TOP; that stops the pin falling out, not
                                 # walking in, and a D 2.4 head cannot sit in a D 2.2 bore. Moved to the tip end.)
PIN_RECESS = 0.05                # pin face below the stud tip, +0.05 / -0
PIN_RECESS_TOL = 0.05
SLEEVE_CBORE_D = 2.50
SLEEVE_CBORE_H = PIN_HEAD_H + PIN_RECESS                 # 0.55


def lit_tip_above_seat(rec_t=None):
    """Lit cap stud tip relative to the record seat plane: record + PET washer, then the flange face. No felt term."""
    return (S.REC12_T if rec_t is None else rec_t) + S.PET_WASHER[2] - LC_STUD_L


assert abs(lit_tip_above_seat() - S.cap_tip_above_seat("12")) <= 0.05, \
    "lit and plain cap stud TIPS must land at the same depth (a plain cap in a lit sconce must behave like a lit one)"

# ---------------------------------------------------------------- core (brass, nickel)
CORE_R = 18.3                    # flange outer radius (window seat)
FLANGE_T = 1.3                   # z 0 .. 1.3. Rev B (review M4): rev A hung the whole flange on a 0.3 web over a D 13.2 x 1.0
                                 # felt recess. The recess and the felt are DELETED: the underside is one flat face on the PET
                                 # washer, the clamp load goes straight down the column, and nothing bends. (Thickening the
                                 # flange instead, as first tried, lifted the light slot 0.5 and tripled the dark collar.)
FLANGE_SOLID_MIN = 0.8           # check: least metal under the cavity floor, anywhere inboard of the louver
COL_R = 5.0                      # centre column, carries the LED PCB
COL_TOP = FLANGE_T + 3.5         # 4.8: LED PCB seat. Drawing: 4.80 +/-0.02 (datum for the lip gap)
SPG_D, SPG_MINOR_D, SPG_L = 8.0, 7.46, 4.0  # M8x0.5 LH spigot on the column: dome boss screws on (Loctite 270)
SPG_KEY_X = 3.6                  # D-flat on the spigot (x >= 3.6 removed) over the PCB zone only: anti-rotation key for the PCB
SPG_KEY_H = 0.55                 # rev B (review M2): was 0.9, TALLER than the 0.8 PCB, so the boss bottomed on the unthreaded
                                 # key and never clamped the board. 0.55 is under the thinnest board (0.72).
SPG_RELIEF_D, SPG_RELIEF_L = 7.3, 0.5        # thread run-out groove above the key
BORE_TOP = FLANGE_T + 0.5        # 1.8: the axial bore is blind, it stops just past the wire cross-hole
XHOLE_D = 1.0                    # 45 deg wire cross-hole from the column into the bore
XHOLE_START = (COL_R, COL_TOP - 0.2)   # (r, z) of the hole axis at the column surface; it breaks out through the column
                                       # TOP face edge (r 4.5..5), under the LED PCB (review S8)
XHOLE_ANG = 60.0                 # azimuth (between LEDs at 30 and 90 deg)

# ---------------------------------------------------------------- louver (black micro-SLA / micro-moulded)
LOUV_RI, LOUV_RO = 12.5, 17.5
LOUV_Z0, LOUV_Z1 = FLANGE_T, COL_TOP          # 1.3 .. 4.8 (at the bore)
LOUV_N = 5                       # fins (5 channels: floor..fin1 .. fin4..fin5)
LOUV_PITCH = 0.65
LOUV_FIN_T = 0.25
LOUV_TILTS = (8.0, 8.0, 8.0, 7.0, 6.0, 4.0)   # deg down toward the outside: [0] = core floor cone, [1..5] = fins
LOUV_TILT = LOUV_TILTS[1]
LOUV_WHITE_FRAC = 0.3            # inner 30 % of every fin is white (recycles light), outer 70 % matte black
LOUV_RIB_W = 0.4
LOUV_RIB_ANG = tuple(30 + 60 * k for k in range(6))
LOUV_FLOOR_OUT = FLANGE_T - (17.5 - 12.5) * math.tan(math.radians(LOUV_TILTS[0]))   # 0.60
LOUV_TOP = COL_TOP - 0.05        # 4.75, unchanged: the louver is the optic, it stays exactly where the ray trace put it
LIP_GAP = 0.25                   # rev B (review M3): was 0.05 against a +/-0.4 stack. The dome BOSS is the hard stop; the lip
                                 # must never land on the louver or the window. The LIP moves up 0.20, not the louver down.

# ---------------------------------------------------------------- window (clear PC, satin outside)
WIN_RI, WIN_RO = 17.55, 18.05
WIN_Z0, WIN_Z1 = LOUV_FLOOR_OUT, LOUV_TOP
WIN_SATIN_DEG = 3.0              # sigma of the surface-normal scatter on the outer face (light bead blast / MT-11010)

# ---------------------------------------------------------------- dome (brass, chrome) - same outside as RS-CAP-12
DOME_R = S.CAP12_D / 2           # 19.05
DOME_Z0 = LOUV_TOP + LIP_GAP     # lip (bottom face) height: 5.00 (rev A 4.80)
DOME_BAND_H = S.CAP12_RIM_H      # 1.6
DOME_H = S.CAP12_DOME_H          # 8.4
DOME_SPH_R = (DOME_R ** 2 + DOME_H ** 2) / (2 * DOME_H)   # 25.80
DOME_SHELL_T = 1.2
DOME_WALL_R = LOUV_RI            # 12.5 inner wall of the lower ring
BOSS_D = 12.0                    # dome centre boss: clamps the LED PCB ring r 4.1..6 onto the column top
BOSS_CBORE_D, BOSS_CBORE_H, BOSS_CBORE_CHAMFER = 8.3, 0.4, 0.2   # rev B (review M2): relief in the boss mouth, so the
                                 # threaded bore (minor D 7.46) can never land on the unthreaded D 8.0 key
DOME_TOP = DOME_Z0 + DOME_BAND_H + DOME_H                 # 15.0 (rev A 14.8)

# ---------------------------------------------------------------- LED PCB (cap)
LPCB_D, LPCB_T = 24.6, 0.8
LPCB_T_TOL = 0.08                # 0.8 mm FR4 +/-10 %
LPCB_Z0 = COL_TOP                # 4.8 .. 5.6, LEDs on the UNDERSIDE facing the white flange
LPCB_ID = 8.2
LPCB_PAD_R = 6.4                 # + pad (underside) where the PTFE lead lands
LED_N, LED_R = 6, 8.5
LED_SIZE = (3.5, 2.8, 0.8)       # LUXEON 2835: tangential x radial x height
R_BALLAST = 100.0
I_CCR = 0.020
BOSS_TO_LIP = (LPCB_Z0 + LPCB_T) - DOME_Z0    # 0.60: boss face above the lip face, +/-0.02 (drawing datum)
# tolerance stack for the lip gap (review M3): each is the +/- on a drawn, toleranced dimension
LIP_GAP_STACK = ((f"column top {COL_TOP:.2f} +/-0.02", 0.02), (f"boss face to lip face {BOSS_TO_LIP:.2f} +/-0.02", 0.02),
                 (f"LED PCB {LPCB_T:.2f} +/-{LPCB_T_TOL}", LPCB_T_TOL), ("louver / window top +0 / -0.05", 0.0))

# ---------------------------------------------------------------- hub contact module (frame: backplate back face z=0)
HUB_RELIEF_FLOOR = -S.CAP_RELIEF_DEPTH       # -9.1 (RS-HUB-01 rev B relief; rev A was 4.5 deep)
HPCB_D, HPCB_T = 13.0, 1.6
HPCB_Z0 = HUB_RELIEF_FLOOR                    # -9.1 .. -7.5
CAR_D = 13.0
CAR_Z0 = HPCB_Z0 + HPCB_T                     # -7.5: carrier sits on the PCB
CAR_Z1 = -0.6                                 # carrier body top. The insert is driven flush to 0.2 below the FRONT face and
                                              # the backplate is 12.70 +/-0.15, so its back end can stand 0.35 proud.
# Centre contact (review M6). No catalogue spring pin has more than 3.0 mm of stroke (Mill-Max calls its 3 mm 0919 the
# longest travel in its line), and the stack needs 4.2 with tolerances. So the centre contact is a gold plunger on a
# catalogue compression spring inside the carrier, and the carrier's spigot is the PEEK GUARD TUBE: its top is a hard
# stop BELOW the lowest place a correct stud can reach, so no stud of any length can ever crush the contact.
SPIG_D = 4.80                                 # pilots in the insert thread minor (4.98..5.26)
GUARD_TOP = 2.1                               # guard tube top above the backplate back face
SPIG_L = GUARD_TOP - CAR_Z1                   # 2.7
SPIG_CHAMFER = 0.6                            # lead-in (review S6: carrier floats +/-0.5 in the D 14 relief)
GUARD_BORE_D = 2.6                            # plunger flange + spring run in here
GUARD_LIP_T = 0.8                             # PEEK lip that retains the plunger when the cap is off
GUARD_NOSE_HOLE_D = 1.35
PLG_NOSE_D = 1.2                              # hard-gold contact nose, 0.3 R crown
PLG_FLANGE_D, PLG_FLANGE_H = 2.5, 0.6
PLG_PILOT_D, PLG_PILOT_H = 1.5, 0.8           # spring pilot under the flange
PLG_FREE_TIP = 7.0                            # nose tip with the cap off (flange up against the lip)
PLG_TRAVEL = PLG_FREE_TIP - GUARD_TOP         # 4.9: nose flush with the guard top = the stud is on the guard
PLG_NOSE_L = PLG_FREE_TIP - (GUARD_TOP - GUARD_LIP_T)    # 5.7
PLG_MIN_COMP = 0.5                            # least travel that still counts as contact
SPRING = dict(od=2.3, wire=0.20, free=11.2, n_total=13, rate=0.15,
              note="stainless 302 / 17-7 compression spring, closed ends, gold flash or passivated (calc; catalogue SKU not picked)")
SPRING_SOLID = SPRING["n_total"] * SPRING["wire"]        # 2.8
POGO_BORE_D = 1.9
# Return contact: Mill-Max 0919 (the verified 3 mm pin, now used where the travel is small and fixed)
POGO_RET = dict(pn="0919-0-15-20-89-14-11-0", free=9.63, h_min=6.63, h_max=8.87, plunger_d=1.07, barrel_d=1.6, barrel_l=6.2)
POGO_R_POS = (-3.8, 0.0)
INSERT_BACK_END = (-0.35, 0.15)               # insert back end relative to the backplate back face (- = proud toward the hub)
CCR_POCKET = (4.6, 2.6, 1.4, 3.6, -3.0)       # x, y, h, cx, cy (pocket in the carrier underside for the SOD-123 CCR)
WIRE_NOTCH_W = 3.0
D1_POCKET = (2.6, 2.0, 1.4, -3.0, -3.6)       # reverse-polarity diode 1N4148WS (SOD-323)
Z1_POCKET = (2.0, 1.6, 1.0, 3.0, 3.6)         # TVS 0402 (rev B: pocket added, the carrier used to sit on the part)
F1_POCKET = (2.4, 1.8, 1.0, -3.0, 3.6)        # 100 mA PTC 0603 on the tap from the 2 A rail (review S5)

# record-thickness envelope used in the clearance stack (mm, label area)
REC_T_MIN, REC_T_MAX = 1.2, 2.7   # Dynaflex ~1.2, deep-groove / heavy-label pressings ~2.7
# Tolerances that move the stud tip relative to the centre contact (review M6). (name, low side, high side) in mm;
# "low" pushes the tip toward the hub (more compression), "high" pulls it away.
TIP_TOLERANCES = (
    (f"stud length {LC_STUD_L:.2f} +/-0.05", 0.05, 0.05),
    ("backplate thickness 12.70 +/-0.15", 0.15, 0.15),
    ("MDF humidity swell (one-sided)", 0.0, 0.30),
    ("record seat: pad / backing-ring felt thickness", 0.30, 0.30),
    ("PET washer 0.25 +/-0.03", 0.03, 0.03),
    ("hub relief depth 9.1 +/-0.2 (FDM)", 0.20, 0.20),
    ("hub PCB 1.6 +/-0.16", 0.16, 0.16),
    ("carrier height +/-0.05", 0.05, 0.05),
    ("pin recess 0.05 +0.05/-0", 0.0, 0.05),
)
TOL_LOW = sum(t[1] for t in TIP_TOLERANCES)       # 0.94
TOL_HIGH = sum(t[2] for t in TIP_TOLERANCES)      # 1.29
TOL_RSS = math.sqrt(sum(max(t[1], t[2]) ** 2 for t in TIP_TOLERANCES))


def pol(r, a):
    return S.pol(r, a)


def _revolve(pts):
    wp = cq.Workplane("XZ").polyline(pts).close()
    return wp.revolve(360, (0, 0, 0), (0, 1, 0))


# ================================================================ CORE
def core_lit(asm=False):
    """asm=False: the STEP a shop quotes from (external threads at MAJOR diameter).
    asm=True : spigot thread zone at just under the M8x0.5 MINOR diameter, so the interference check sees the dome's
    tap-drill bore and the unthreaded key as they really are (rev A's check passed only because the dome bore was drawn
    at the major diameter)."""
    L = LC_STUD_L
    rs = LC_STUD_D / 2
    rd = S.CAP_STUD_DOG_D / 2
    sl, sr = S.CAP_SHOULDER_L, S.CAP_SHOULDER_D / 2
    rt = (SPG_MINOR_D / 2 - 0.01) if asm else SPG_D / 2
    zk = COL_TOP + SPG_KEY_H                     # top of the unthreaded key
    zr = zk + SPG_RELIEF_L                       # top of the run-out groove
    zt = COL_TOP + SPG_L
    pts = [(0, -L), (rd - 0.3, -L), (rd, -L + 0.3), (rd, -L + S.CAP_STUD_DOG_L), (rs, -L + S.CAP_STUD_DOG_L + (rs - rd)),
           (rs, -sl - LC_RELIEF_L), (LC_RELIEF_D / 2, -sl - LC_RELIEF_L), (LC_RELIEF_D / 2, -sl),
           (sr - 0.2, -sl), (sr, -sl + 0.2), (sr, 0.0),                               # smooth shoulder D 7.10
           (CORE_R - 0.3, 0.0), (CORE_R, 0.3), (CORE_R, LOUV_FLOOR_OUT),
           (LOUV_RO, LOUV_FLOOR_OUT), (LOUV_RI, FLANGE_T),            # 8 deg conical louver floor
           (COL_R, FLANGE_T), (COL_R, COL_TOP - 0.2), (COL_R - 0.2, COL_TOP),
           (SPG_D / 2, COL_TOP), (SPG_D / 2, zk),                     # unthreaded key zone, D 8.0
           (SPG_RELIEF_D / 2, zk), (SPG_RELIEF_D / 2, zr),            # run-out groove
           (rt, zr), (rt, zt - 0.3), (rt - 0.3, zt),
           (0, zt)]
    c = _revolve(pts)
    c = c.cut(S.cyl(LC_BORE_D, LC_BORE_STEP + 0.01, z0=-L - 0.01))                       # sleeve bore, to the shoulder
    c = c.cut(S.cyl(LC_WIRE_BORE_D, BORE_TOP - (-L + LC_BORE_STEP) + 0.01, z0=-L + LC_BORE_STEP - 0.01))   # wire bore
    # 45 deg wire cross-hole: from the column (r=5, z=COL_TOP-0.2) down and in to the wire bore
    r0, z0 = XHOLE_START
    length = (r0 + 1.0) * math.sqrt(2)
    hole = cq.Workplane("XY").circle(XHOLE_D / 2).extrude(length)
    hole = hole.rotate((0, 0, 0), (0, 1, 0), -135).translate((r0 + 0.5, 0, z0 + 0.5))
    hole = hole.rotate((0, 0, 0), (0, 0, 1), XHOLE_ANG)
    c = c.cut(hole)
    # D-flat on the spigot base (PCB zone only): anti-rotation key for the LED PCB
    c = c.cut(S.box(SPG_D, SPG_D + 2, SPG_KEY_H, SPG_KEY_X + SPG_D / 2, 0, COL_TOP))
    return c


# ================================================================ DOME
def dome_lit():
    z0 = DOME_Z0
    R = DOME_SPH_R
    zc = DOME_TOP - R
    Ri = R - DOME_SHELL_T
    br = S.CAP_BASE_R
    r = DOME_R
    rb = BOSS_D / 2
    zb = LPCB_Z0 + LPCB_T                          # boss bottom face clamps the PCB
    z_wall_top = zc + math.sqrt(Ri ** 2 - DOME_WALL_R ** 2)
    z_boss_top = zc + math.sqrt(Ri ** 2 - rb ** 2)
    a1 = math.asin(rb / Ri); a2 = math.asin(DOME_WALL_R / Ri)
    am_i = (a1 + a2) / 2
    rm = SPG_MINOR_D / 2                           # internal thread drawn at its tap-drill (minor) diameter
    rc = BOSS_CBORE_D / 2
    wp = (cq.Workplane("XZ").moveTo(rc + BOSS_CBORE_CHAMFER, zb)
          .lineTo(rb, zb).lineTo(rb, z_boss_top)
          .threePointArc((Ri * math.sin(am_i), zc + Ri * math.cos(am_i)), (DOME_WALL_R, z_wall_top))
          .lineTo(DOME_WALL_R, z0)
          .lineTo(r - br, z0)
          .threePointArc((r - br + br * math.sin(math.radians(45)), z0 + br - br * math.cos(math.radians(45))), (r, z0 + br))
          .lineTo(r, z0 + DOME_BAND_H))
    am = math.asin((z0 + DOME_BAND_H - zc) / R)
    amid = (am + math.pi / 2) / 2
    wp = (wp.threePointArc((R * math.cos(amid), zc + R * math.sin(amid)), (0, DOME_TOP))
          .lineTo(0, zb + SPG_L + 0.6).lineTo(rm, zb + SPG_L + 0.6)
          .lineTo(rm, zb + BOSS_CBORE_H).lineTo(rc, zb + BOSS_CBORE_H)          # counterbore floor
          .lineTo(rc, zb + BOSS_CBORE_CHAMFER).close())                          # 0.2 chamfer back to the start point
    return wp.revolve(360, (0, 0, 0), (0, 1, 0))


# ================================================================ LOUVER
def _fin(z, tilt):
    dz = (LOUV_RO - LOUV_RI) * math.tan(math.radians(tilt))
    pts = [(LOUV_RI, z), (LOUV_RO, z - dz), (LOUV_RO, z - dz + LOUV_FIN_T), (LOUV_RI, z + LOUV_FIN_T)]
    return _revolve(pts)


def louver_fin_z():
    """Fin bottom heights at the inner edge (cap frame). The top fin's top face is LOUV_TOP."""
    return [LOUV_TOP - LOUV_FIN_T - (LOUV_N - k) * LOUV_PITCH for k in range(1, LOUV_N + 1)]


def _floor_cut():
    return _revolve([(LOUV_RI - 1, -1), (LOUV_RO + 1, -1), (LOUV_RO + 1, LOUV_FLOOR_OUT), (LOUV_RO, LOUV_FLOOR_OUT),
                     (LOUV_RI, FLANGE_T), (LOUV_RI - 1, FLANGE_T)])


def louver_lit():
    lv = None
    for z, t in zip(louver_fin_z(), LOUV_TILTS[1:]):
        f = _fin(z, t)
        lv = f if lv is None else lv.union(f)
    for a in LOUV_RIB_ANG:
        lv = lv.union(S.radial_box(LOUV_RIB_W, LOUV_RI, LOUV_RO, LOUV_FLOOR_OUT, LOUV_TOP, a))
    return lv.cut(_floor_cut())


def window_lit():
    return S.ring(WIN_RO, WIN_RI, WIN_Z1 - WIN_Z0, WIN_Z0)


# ================================================================ PIN + SLEEVE
def pin_lit():
    """Headed contact pin: D 2.4 x 0.5 head at the tip end (gold face), 1/16 in shank, solder cup on top."""
    z0 = -LC_STUD_L + PIN_RECESS
    p = S.cyl(PIN_HEAD_D, PIN_HEAD_H, z0=z0).union(S.cyl(PIN_D, PIN_L - PIN_HEAD_H + 0.01, z0=z0 + PIN_HEAD_H - 0.01))
    p = p.cut(S.cyl(0.8, 2.0, z0=z0 + PIN_L - 2.0))      # solder cup for the 30 AWG lead
    return p


def sleeve_lit():
    """PEEK sleeve, tip end flush with the stud tip, top end on the bore shoulder; counterbore for the pin head."""
    s = S.ring(SLEEVE_OD / 2 - 0.0125, SLEEVE_ID / 2, SLEEVE_L, -LC_STUD_L)
    return s.cut(S.cyl(SLEEVE_CBORE_D, SLEEVE_CBORE_H + 0.01, z0=-LC_STUD_L - 0.01))


# ================================================================ LED PCB (cap) + LEDs
def led_pcb():
    """Ring PCB with a D-shaped centre hole (flat at x = SPG_KEY_X + 0.1) keyed to the spigot flat."""
    hole = S.cyl(LPCB_ID, LPCB_T + 2, z0=LPCB_Z0 - 1)
    hole = hole.cut(S.box(LPCB_ID, LPCB_ID + 2, LPCB_T + 4, SPG_KEY_X + 0.1 + LPCB_ID / 2, 0, LPCB_Z0 - 2))
    return S.cyl(LPCB_D, LPCB_T, z0=LPCB_Z0).cut(hole)


def leds():
    out = None
    for k in range(LED_N):
        a = 90 + 360 / LED_N * k
        L_ = S.box(LED_SIZE[0], LED_SIZE[1], LED_SIZE[2], 0, LED_R, LPCB_Z0 - LED_SIZE[2]).rotate((0, 0, 0), (0, 0, 1), a - 90)
        out = L_ if out is None else out.union(L_)
    return out


def led_pcb_outline_pts(n=360):
    return [pol(LPCB_D / 2, 360 * k / n) for k in range(n)]


# ================================================================ HUB CONTACT MODULE
def hub_pcb():
    return S.cyl(HPCB_D, HPCB_T, z0=HPCB_Z0)        # no holes: the return pin is SMT, the centre spring sits on a gold pad


def carrier():
    """PEEK carrier + guard tube. Body D 13 on the hub PCB, spigot D 4.80 up into the insert thread; the spigot is bored
    D 2.6 for the plunger and spring, and closed by a 0.8 lip with a D 1.35 hole for the plunger nose."""
    c = S.cyl(CAR_D, CAR_Z1 - CAR_Z0, z0=CAR_Z0)
    sp = (cq.Workplane("XY").circle(SPIG_D / 2).extrude(SPIG_L - SPIG_CHAMFER)
          .faces(">Z").workplane().circle(SPIG_D / 2).workplane(offset=SPIG_CHAMFER).circle(SPIG_D / 2 - SPIG_CHAMFER).loft()
          .translate((0, 0, CAR_Z1)))
    c = c.union(sp).union(S.cyl(SPIG_D, 0.06, z0=CAR_Z1 - 0.01))
    z_lip = GUARD_TOP - GUARD_LIP_T
    c = c.cut(S.cyl(GUARD_BORE_D, z_lip - CAR_Z0 + 1, z0=CAR_Z0 - 1))                    # plunger + spring bore
    c = c.cut(S.cyl(GUARD_NOSE_HOLE_D, GUARD_LIP_T + 2, z0=z_lip - 1))                   # nose hole through the lip
    c = c.cut(S.cyl(POGO_BORE_D, 20, POGO_R_POS[0], POGO_R_POS[1], CAR_Z0 - 1))          # return pin guide
    for px, py, ph, cx, cy in (CCR_POCKET, D1_POCKET, Z1_POCKET, F1_POCKET):
        c = c.cut(S.box(px, py, ph + 0.5, cx, cy, CAR_Z0 - 0.5))
    # wire notch toward the splice cavity (+Y), full height of the body
    c = c.cut(S.box(WIRE_NOTCH_W, 3.0, CAR_Z1 - CAR_Z0 + 1, 0, CAR_D / 2, CAR_Z0 - 0.5))
    return c


def plunger(tip_z=PLG_FREE_TIP):
    """Gold contact plunger at a given nose-tip height (module frame). Free = PLG_FREE_TIP, flange against the lip."""
    z_fl_top = tip_z - PLG_NOSE_L
    nose = S.cyl(PLG_NOSE_D, PLG_NOSE_L + 0.01, z0=z_fl_top - 0.01)
    flange = S.cyl(PLG_FLANGE_D, PLG_FLANGE_H, z0=z_fl_top - PLG_FLANGE_H)
    pilot = S.cyl(PLG_PILOT_D, PLG_PILOT_H + 0.01, z0=z_fl_top - PLG_FLANGE_H - PLG_PILOT_H)
    return nose.union(flange).union(pilot)


def spring_len(tip_z=PLG_FREE_TIP):
    """Working length of the spring: hub PCB top to the underside of the plunger flange."""
    return (tip_z - PLG_NOSE_L - PLG_FLANGE_H) - CAR_Z0


def spring(tip_z=PLG_FREE_TIP):
    return S.ring(SPRING["od"] / 2, SPRING["od"] / 2 - SPRING["wire"], spring_len(tip_z), CAR_Z0)


def pogo(spec, base_z, tip_z, x=0.0, y=0.0):
    """Purchased spring pin, modelled at a given compressed tip height (barrel + plunger envelope)."""
    bar = S.cyl(spec["barrel_d"], spec["barrel_l"], x, y, base_z)
    plg = S.cyl(spec["plunger_d"], tip_z - (base_z + spec["barrel_l"]) + 0.0, x, y, base_z + spec["barrel_l"])
    return bar.union(plg)


def ccr_body():
    px, py, ph, cx, cy = CCR_POCKET
    return S.box(2.7, 1.6, 1.1, cx, cy, HPCB_Z0 + HPCB_T)


# ================================================================ stack-up numbers (single source for checks + DESIGN.md)
def tip_back(rec_t, seat=None):
    """Lit cap stud tip height above the backplate BACK face (= module frame z). The record sits on the pads and the
    centre backing ring at S.REC_SEAT_H; then the PET washer; then the cap's flat flange face."""
    seat = S.REC_SEAT_H if seat is None else seat
    return S.BP_T + seat + lit_tip_above_seat(rec_t)


STACK_CASES = dict(nominal=S.REC12_T, thick_record=REC_T_MAX, thin_record=REC_T_MIN)


def stack(rec_t):
    tip = tip_back(rec_t)
    face = tip + PIN_RECESS
    engage = S.BP_T - tip
    return dict(stud_tip=tip, pin_face=face, engage=min(engage, S.INSERT_L),
                engage_threaded=min(engage, S.INSERT_L) - S.CAP_STUD_DOG_L,
                comp=PLG_FREE_TIP - face, tip_to_guard=tip - GUARD_TOP)


def clearance_numbers_lit():
    out = {}
    for k, t in STACK_CASES.items():
        s = stack(t)
        out[f"lit_{k}_thread_engagement_mm"] = round(s["engage"], 2)
        out[f"lit_{k}_threaded_engagement_past_dog_point_mm"] = round(s["engage_threaded"], 2)
        out[f"lit_{k}_centre_contact_compression_mm({PLG_MIN_COMP}..{PLG_TRAVEL:.1f})"] = round(s["comp"], 2)
        out[f"lit_{k}_stud_tip_above_guard_tube_mm"] = round(s["tip_to_guard"], 2)
    # ---- worst case: every tolerance stacked on the thin and the thick record (review M6)
    thin, thick = stack(STACK_CASES["thin_record"]), stack(STACK_CASES["thick_record"])
    out["tolerance_stack_low_side_sum_mm"] = round(TOL_LOW, 2)
    out["tolerance_stack_high_side_sum_mm"] = round(TOL_HIGH, 2)
    out["tolerance_stack_rss_mm"] = round(TOL_RSS, 2)
    out["worst_case_thin_record_stud_tip_above_guard_tube_mm(must be >= 0.2)"] = round(thin["tip_to_guard"] - TOL_LOW, 2)
    out["lit_tip_minus_plain_cap12_tip_nominal_mm(asserted <= 0.05)"] = round(lit_tip_above_seat() - S.cap_tip_above_seat("12"), 3)
    out["worst_case_thin_record_centre_contact_compression_mm(must be <= travel)"] = round(thin["comp"] + TOL_LOW, 2)
    out["worst_case_thick_record_centre_contact_compression_mm(must be >= 0.5)"] = round(thick["comp"] - TOL_HIGH, 2)
    out["centre_contact_travel_mm(nose free tip to guard top)"] = round(PLG_TRAVEL, 2)
    out["worst_case_thick_record_threaded_engagement_mm(must be >= 5.0)"] = round(thick["engage_threaded"] - 0.30 - 0.03 - 0.05, 2)
    # ---- guard tube: no stud of any length can bottom the contact
    out["plunger_flange_underside_above_spring_solid_height_with_stud_on_guard_mm"] = round(spring_len(GUARD_TOP) - SPRING_SOLID, 2)
    out["plunger_pilot_end_above_hub_pcb_with_stud_on_guard_mm"] = round(spring_len(GUARD_TOP) - PLG_PILOT_H, 2)
    out["spring_force_cap_off_N"] = round((SPRING["free"] - spring_len()) * SPRING["rate"], 2)
    out["spring_force_min_contact_N(thick record, worst case)"] = round(
        (SPRING["free"] - spring_len(PLG_FREE_TIP - (thick["comp"] - TOL_HIGH))) * SPRING["rate"], 2)
    out["spring_force_max_N(stud on the guard)"] = round((SPRING["free"] - spring_len(GUARD_TOP)) * SPRING["rate"], 2)
    out["guard_tube_wall_mm"] = round((SPIG_D - GUARD_BORE_D) / 2, 2)
    # ---- a PLAIN RS-CAP-12 / RS-CAP-7 screwed into a lit sconce (review M7)
    plain_thin = S.BP_T + S.REC_SEAT_H + S.cap_tip_above_seat("12", REC_T_MIN, 0.0)
    out["plain_cap12_in_lit_sconce_thin_record_tip_above_guard_tube_worst_mm"] = round(plain_thin - TOL_LOW - GUARD_TOP, 2)
    cap7_thin = S.BP_T + S.REC_SEAT_H + S.cap_tip_above_seat("7", REC_T_MIN, 0.6)
    out["cap7_in_lit_sconce_thin_45_tip_above_guard_tube_worst_mm"] = round(cap7_thin - TOL_LOW - GUARD_TOP, 2)
    out["any_longer_screw_stops_on_the_guard_tube_at_mm_above_back_face"] = GUARD_TOP
    # ---- return pin (Mill-Max 0919) on the insert's back end
    hs = [-CAR_Z0 + INSERT_BACK_END[0] - 0.36, -CAR_Z0 + INSERT_BACK_END[1] + 0.36]   # + relief depth and PCB tolerance
    out["return_pin_working_height_nominal_mm(6.63..8.87)"] = round(-CAR_Z0, 2)
    out["return_pin_working_height_worst_min_mm(must be >= 6.63)"] = round(hs[0], 2)
    out["return_pin_working_height_worst_max_mm(must be <= 8.87)"] = round(hs[1], 2)
    out["carrier_top_below_backplate_back_face_mm(insert may stand 0.35 proud)"] = round(0 - CAR_Z1, 2)
    out["spigot_key_flat_to_pcb_flat_clearance_mm"] = 0.1
    # ---- coax geometry
    misalign = 0.15 + (LC_INSERT_MINOR_MAX - SPIG_D) / 2 + (GUARD_NOSE_HOLE_D - PLG_NOSE_D) / 2 + 0.10   # thread, spigot, nose, concentricity
    out["plunger_contact_edge_radius_worst_mm"] = round(misalign + PLG_NOSE_D / 2, 2)
    out["pin_head_gold_face_radius_mm"] = round(PIN_HEAD_D / 2, 2)
    out["brass_annulus_inner_radius_mm"] = round(LC_BORE_D / 2, 3)
    out["plunger_to_brass_margin_worst_mm(short-circuit guard)"] = round(LC_BORE_D / 2 - (misalign + PLG_NOSE_D / 2), 2)
    out["pin_head_to_brass_bore_radial_peek_mm"] = round((LC_BORE_D - PIN_HEAD_D) / 2, 3)
    out["hollow_stud_wall_at_thread_root_mm"] = round((LC_STUD_MINOR_D - LC_BORE_D) / 2, 2)
    out["hollow_stud_tensile_area_mm2"] = round(math.pi / 4 * (LC_STUD_MINOR_D ** 2 - LC_BORE_D ** 2), 1)
    out["spigot_radial_clearance_in_insert_minor_min_mm"] = round((LC_INSERT_MINOR_D - SPIG_D) / 2, 2)
    out["spigot_radial_clearance_in_insert_minor_max_mm"] = round((LC_INSERT_MINOR_MAX - SPIG_D) / 2, 2)
    out["spigot_lead_in_capture_range_mm(carrier floats +/-0.5)"] = round(SPIG_CHAMFER + (LC_INSERT_MINOR_D - SPIG_D) / 2, 2)
    out["record_hole_min_minus_shoulder_mm"] = round(S.REC_HOLE_MIN - S.CAP_SHOULDER_D, 2)
    # ---- pin / sleeve positive stops (review M8)
    out["sleeve_od_minus_wire_bore_mm(sleeve seats on the bore shoulder)"] = round(SLEEVE_OD - LC_WIRE_BORE_D, 3)
    out["pin_head_minus_sleeve_bore_mm(head cannot pass up the sleeve)"] = round(PIN_HEAD_D - SLEEVE_ID, 3)
    out["sleeve_top_to_bore_shoulder_gap_mm"] = round((-LC_STUD_L + LC_BORE_STEP) - (-LC_STUD_L + SLEEVE_L), 3)
    out["pin_head_top_to_sleeve_counterbore_floor_gap_mm"] = round(SLEEVE_CBORE_H - (PIN_RECESS + PIN_HEAD_H), 3)
    out["sleeve_wall_at_pin_head_counterbore_mm"] = round((SLEEVE_OD - SLEEVE_CBORE_D) / 2, 3)
    # ---- cap internals
    out["led_pcb_edge_to_dome_inner_wall_mm"] = round(DOME_WALL_R - LPCB_D / 2, 2)
    out["led_body_outer_to_louver_inner_mm"] = round(LOUV_RI - (LED_R + LED_SIZE[1] / 2), 2)
    out["led_body_inner_to_column_mm"] = round((LED_R - LED_SIZE[1] / 2) - COL_R, 2)
    out["led_underside_to_flange_top_mm"] = round((LPCB_Z0 - LED_SIZE[2]) - FLANGE_T, 2)
    out["flange_solid_thickness_under_the_cavity_mm(no felt recess; must be >= 0.8)"] = round(FLANGE_T, 2)
    r_sh = S.CAP_SHOULDER_D / 2
    out["cross_hole_lower_edge_above_contact_face_at_the_shoulder_mm"] = round(
        (XHOLE_START[1] - (XHOLE_START[0] - r_sh)) - XHOLE_D / 2 * math.sqrt(2), 2)
    out["window_to_lip_edge_overhang_mm"] = round(DOME_R - WIN_RO, 2)
    out["louver_to_window_radial_gap_mm"] = round(WIN_RI - LOUV_RO, 2)
    out["dome_boss_to_led_body_mm"] = round((LED_R - LED_SIZE[1] / 2) - BOSS_D / 2, 2)
    out["pcb_clamp_ring_width_mm(boss r6 - pcb ID r4.1)"] = round(BOSS_D / 2 - LPCB_ID / 2, 2)
    # review M2: key under the thinnest board, counterbore over the key, real thread engagement
    out["pcb_min_top_minus_key_top_mm(must be > 0: boss clamps the PCB, not the key)"] = round(
        (LPCB_T - LPCB_T_TOL) - SPG_KEY_H, 2)
    out["boss_counterbore_dia_minus_key_dia_mm(must be > 0)"] = round(BOSS_CBORE_D - SPG_D, 2)
    out["boss_thread_minor_dia_minus_key_dia_mm(negative = why the counterbore exists)"] = round(SPG_MINOR_D - SPG_D, 2)
    out["spigot_thread_engagement_in_dome_boss_mm"] = round(
        (COL_TOP + SPG_L) - max(LPCB_Z0 + LPCB_T + BOSS_CBORE_H, COL_TOP + SPG_KEY_H + SPG_RELIEF_L), 2)
    # review M3: lip gap against its own tolerance stack
    stack_sum = sum(v for _, v in LIP_GAP_STACK)
    out["boss_face_above_lip_face_mm"] = round(BOSS_TO_LIP, 2)
    out["louver_top_to_dome_lip_gap_mm"] = round(DOME_Z0 - LOUV_TOP, 2)
    out["window_top_to_dome_lip_gap_mm"] = round(DOME_Z0 - WIN_Z1, 2)
    out["lip_gap_tolerance_stack_worst_mm"] = round(stack_sum, 2)
    out["lip_gap_minus_tolerance_stack_mm(must be > 0: the boss is always the stop)"] = round(LIP_GAP - stack_sum, 2)
    out["flange_thickness_at_window_seat_mm"] = round(LOUV_FLOOR_OUT, 2)
    out["louver_bottom_channel_open_at_outer_edge_mm"] = round(louver_fin_z()[0] - (LOUV_RO - LOUV_RI) * math.tan(math.radians(LOUV_TILTS[1])) - LOUV_FLOOR_OUT, 2)
    out["lit_cap_height_above_contact_face_mm"] = round(DOME_TOP, 2)
    out["lit_cap_height_minus_plain_cap_mm"] = round(DOME_TOP - (S.CAP12_RIM_H + S.CAP12_DOME_H), 2)
    out["light_slot_height_visible_mm(flange rim + window, under the lip)"] = round(DOME_Z0, 2)
    out["window_height_mm"] = round(WIN_Z1 - WIN_Z0, 2)
    out["pet_washer_od_minus_flange_od_mm(flange rides on PET, never on the label)"] = round(S.PET_WASHER[0] - 2 * CORE_R, 2)
    return out
