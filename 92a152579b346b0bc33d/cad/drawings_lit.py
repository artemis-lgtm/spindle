"""2D drawings (PDF + PNG) for the RS-CAP-12L label-light parts, same style and helpers as drawings.py.
Rev B (2026-11-11): every critical fit carries its own tolerance on the sheet (review M3, M9); the core is dimensioned
with dimension lines instead of notes; sheet() refuses to export a sheet whose notes or title block leave the border."""
import math
import drawings as D
import sconce_cad as S
import sconce_lit as L

REV = L.REV
SUP = "rev A, A.1"


def _sheet(*a, **k):
    k.setdefault("rev", REV)
    k.setdefault("supersedes", SUP)
    return D.sheet(*a, **k)


def draw_dome(out_base):
    d = L.dome_lit()
    zb = L.LPCB_Z0 + L.LPCB_T
    fig = _sheet("LIT DOME CAP SHELL 1.5 in (label light)", "RS-CAP-12L-DOME",
                 "Brass C360 (CDA 360) bar, turned. Same outside profile as RS-CAP-12 (band + R 25.80 sphere segment).",
                 "OUTSIDE (dome, band, lip bottom face r 18.05..19.05): polish to mirror Ra <= 0.1 um, then Cu + bright Ni + decorative Cr per ASTM B456 SC2. "
                 "INSIDE (cavity, wall r 12.5, boss, thread): MASK, no chrome; bare or nickel. Rack on the inside only.",
                 [f"Outside is Class A (inspect at 300 mm daylight, zero pits/haze). The lip bottom face is seen lit from below: polish and chrome it like the dome.",
                  f"Sphere R {L.DOME_SPH_R:.2f}, height {L.DOME_H} above a {L.DOME_BAND_H} band; lip edge R {S.CAP_BASE_R}. Shell {L.DOME_SHELL_T} thick at the axis.",
                  f"Centre boss D {L.BOSS_D}: internal M8x0.5 LEFT-HAND, tap drill D {L.SPG_MINOR_D} (the STEP shows the tap-drill bore), full thread to {L.SPG_L + 0.6:.1f} from the boss face. "
                  f"Boss MOUTH: counterbore D {L.BOSS_CBORE_D} +0.1/-0 x {L.BOSS_CBORE_H} +0.1/-0 deep with a {L.BOSS_CBORE_CHAMFER} x 45 chamfer. It clears the unthreaded D {L.SPG_D} key on the core, so the boss can only ever land on the LED PCB.",
                  f"THE BOSS FACE IS THE HARD STOP of this cap. Boss face flat and square to the thread within 0.03 (it clamps the LED PCB and is a return contact). "
                  f"DATUM: boss face stands {L.BOSS_TO_LIP:.2f} +/-0.02 ABOVE the lip face; lip face parallel to the boss face within 0.03.",
                  f"Assembled, the lip face sits {L.LIP_GAP} above the louver and the window (stack of all tolerances {sum(v for _, v in L.LIP_GAP_STACK):.2f}): the lip must never touch them.",
                  "Mates: screws onto the RS-CAP-12L-CORE spigot (LH thread, Loctite 270 with activator 7649 on nickel, 1.5 N.m; keep adhesive off the boss face). LH so unscrewing the cap tightens this joint. Variants -CR / -BR / -BK."],
                 "SCALE: as shown")
    sec = D.section_polylines(d.val(), "XZ", 0.0)
    ax = D.view(fig, [0.05, 0.25, 0.55, 0.68], [(sec, "k", 1.0, "-")], title="SECTION THROUGH THE AXIS (y=0); z = cap frame, contact face of the core = 0", pad=10)
    D.dim_h(ax, -L.DOME_R, L.DOME_R, L.DOME_TOP + 4, f"D {D.mm_in(2 * L.DOME_R)}", off=0.6, ext_from=L.DOME_TOP)
    D.dim_h(ax, -L.DOME_WALL_R, L.DOME_WALL_R, L.DOME_Z0 - 3, f"bore D {2 * L.DOME_WALL_R:.1f} +0.1/-0", off=-0.6)
    D.dim_v(ax, L.DOME_Z0, L.DOME_TOP, L.DOME_R + 6, f"{L.DOME_TOP - L.DOME_Z0:.1f}", off=1.2, ext_from=L.DOME_R)
    D.dim_v(ax, L.DOME_Z0, L.DOME_Z0 + L.DOME_BAND_H, L.DOME_R + 2.5, f"{L.DOME_BAND_H}", off=0.8)
    D.dim_v(ax, L.DOME_Z0, zb, -L.DOME_R - 4, f"boss face above lip face {L.BOSS_TO_LIP:.2f} +/-0.02", off=-1.0, ext_from=-L.BOSS_D / 2)
    D.leader(ax, (L.DOME_R * 0.6, L.DOME_TOP - 2.2), (-L.DOME_R * 0.2, L.DOME_TOP + 9), f"sphere R {L.DOME_SPH_R:.2f} (outside), R {L.DOME_SPH_R - L.DOME_SHELL_T:.2f} inside")
    D.leader(ax, (L.DOME_R - 0.5, L.DOME_Z0), (L.DOME_R * 0.55, L.DOME_Z0 - 6), "lip face: mirror chrome\n(seen from below, folds light down)")
    D.leader(ax, (L.SPG_MINOR_D / 2, zb + 2.5), (-L.DOME_R * 1.25, zb + 6.5), f"M8x0.5-LH internal,\ntap drill D {L.SPG_MINOR_D}")
    D.leader(ax, (L.BOSS_CBORE_D / 2, zb + L.BOSS_CBORE_H / 2), (L.DOME_R * 0.2, L.DOME_Z0 - 9),
             f"counterbore D {L.BOSS_CBORE_D} +0.1/-0 x {L.BOSS_CBORE_H} +0.1/-0,\n{L.BOSS_CBORE_CHAMFER} x 45 chamfer; boss D {L.BOSS_D}")
    plan = D.plan_polylines(d, ("x", "y"))
    D.view(fig, [0.62, 0.45, 0.36, 0.48], [(plan, "k", 0.6, "-")], title="BOTTOM VIEW")
    D.save(fig, out_base)


def draw_core(out_base):
    c = L.core_lit()
    Ls = L.LC_STUD_L
    zk = L.COL_TOP + L.SPG_KEY_H
    zr = zk + L.SPG_RELIEF_L
    fig = _sheet("LIT CAP CORE: hollow 1/4-20 stud + flange + column", "RS-CAP-12L-CORE",
                 "Brass C360 (CDA 360) bar, turned + one 45 deg cross-hole (live tooling or 2nd op).",
                 "Electroless nickel 5 um MAX, EVERYWHERE (conductive; thread class is before plating, it must accept a 1/4-20 2B GO gauge after). NO chrome. "
                 "Then PAINT ONLY, masking the thread, shoulder, bore, underside (contact) face, column top and spigot: white reflector paint (R >= 0.90) on the flange top r 5..14 and the column side; matte black on the cone r 14..17.5, window seat and rim OD.",
                 [f"Stud 1/4-20 UNC-2A, length {Ls:.2f} +/-0.05 from the contact (underside) face. TIP: dog point D {S.CAP_STUD_DOG_D:.2f} +0/-0.10 x {S.CAP_STUD_DOG_L}, 0.3 x 45 chamfer. Smooth shoulder D {S.CAP_SHOULDER_D:.2f} +0/-0.05 x {S.CAP_SHOULDER_L} under the flange (the record centres on it), relief D {L.LC_RELIEF_D} x {L.LC_RELIEF_L} below it.",
                  f"UNDERSIDE IS ONE FLAT FACE, D {2 * L.CORE_R:.1f}, flat within 0.05, square to the stud within 0.05: NO felt recess (rev A's D 13.2 x 1.0 recess is deleted). It sits on a PET washer.",
                  f"STEPPED BORE, concentric to the thread within 0.05: D {L.LC_BORE_D} +0.02/-0 x {L.LC_BORE_STEP:.2f} +/-0.05 deep from the tip (press fit for the 3.175 PEEK sleeve; the square shoulder is the sleeve's STOP), then D {L.LC_WIRE_BORE_D} to z {L.BORE_TOP}. Deburr the bore mouth; nothing may stand proud of the tip face. Do NOT stake.",
                  f"Column top at {L.COL_TOP:.2f} +/-0.02 above the contact face, flat within 0.03 (LED PCB seat + return contact; lip-gap datum).",
                  f"Spigot M8x0.5 LEFT-HAND, {L.SPG_L} long: first {L.SPG_KEY_H} +0/-0.05 is an UNTHREADED D {L.SPG_D} with a flat at {L.SPG_KEY_X} from the axis (keys the LED PCB; must stay BELOW the 0.72 min PCB), then a run-out groove D {L.SPG_RELIEF_D} x {L.SPG_RELIEF_L}, then thread.",
                  f"Wire cross-hole D {L.XHOLE_D} at 45 deg, az {L.XHOLE_ANG:.0f}: axis passes (r {L.XHOLE_START[0]}, z {L.XHOLE_START[1]:.1f}), so it breaks out through the EDGE of the column top face (r 4.5..5) and meets the D {L.LC_WIRE_BORE_D} bore near z 0.7. Deburr both ends flush: a burr here sits on the PCB seat.",
                  f"Louver floor: 8 deg cone from (r {L.LOUV_RI}, z {L.FLANGE_T}) to (r {L.LOUV_RO}, z {L.LOUV_FLOOR_OUT:.2f}), +/-0.3 deg. Loctite 270 on the spigot needs activator 7649 on nickel; keep it off the column top."],
                 "SCALE: as shown")
    sec = D.section_polylines(c.val(), "XZ", 0.0)
    ax = D.view(fig, [0.04, 0.24, 0.56, 0.70], [(sec, "k", 1.0, "-")], title="SECTION THROUGH THE AXIS (y=0); z = 0 at the contact (underside) face", pad=9)
    R = L.CORE_R
    D.dim_h(ax, -R, R, -3.2, f"D {D.mm_in(2 * R)}", off=-0.6)
    D.dim_h(ax, -L.COL_R, L.COL_R, L.COL_TOP + L.SPG_L + 2.6, f"column D {2 * L.COL_R:.1f}", off=0.4)
    D.dim_h(ax, -L.SPG_D / 2, L.SPG_D / 2, L.COL_TOP + L.SPG_L + 1.0, f"M8x0.5-LH x {L.SPG_L}", off=0.3)
    D.dim_v(ax, -Ls, 0, R + 3, f"{Ls:.2f} +/-0.05 [{Ls / 25.4:.3f}]  1/4-20 UNC-2A", off=1.0)
    D.dim_v(ax, 0, L.FLANGE_T, -R - 2.5, f"{L.FLANGE_T}", off=-0.8)
    D.dim_v(ax, 0, L.COL_TOP, -R - 6, f"{L.COL_TOP:.2f} +/-0.02", off=-0.8, ext_from=-L.COL_R)
    D.dim_v(ax, 0, L.LOUV_FLOOR_OUT, R + 1.2, f"{L.LOUV_FLOOR_OUT:.2f}", off=0.4)
    D.dim_v(ax, L.COL_TOP, zk, R * 0.62, f"key {L.SPG_KEY_H} +0/-0.05", off=0.5, ext_from=L.SPG_D / 2)
    D.dim_v(ax, zk, zr, R * 0.42, f"groove D {L.SPG_RELIEF_D} x {L.SPG_RELIEF_L}", off=0.5, ext_from=L.SPG_D / 2)
    D.dim_v(ax, -Ls, -Ls + L.LC_BORE_STEP, -R * 0.45, f"D {L.LC_BORE_D} +0.02/-0 x {L.LC_BORE_STEP:.2f} +/-0.05 (sleeve seat)", off=-0.5, ext_from=-L.LC_BORE_D / 2)
    D.dim_h(ax, -L.LC_BORE_D / 2, L.LC_BORE_D / 2, -Ls - 2.2, f"D {L.LC_BORE_D}", off=-0.4)
    D.leader(ax, (L.LC_WIRE_BORE_D / 2, 0.6), (R * 0.5, -6.0), f"wire bore D {L.LC_WIRE_BORE_D} to z {L.BORE_TOP}")
    D.leader(ax, (S.CAP_SHOULDER_D / 2, -S.CAP_SHOULDER_L / 2), (R * 0.5, -3.6), f"shoulder D {S.CAP_SHOULDER_D:.2f} +0/-0.05 x {S.CAP_SHOULDER_L}")
    D.leader(ax, (S.CAP_STUD_DOG_D / 2, -Ls + 0.8), (R * 0.5, -Ls + 1.5), f"dog point D {S.CAP_STUD_DOG_D:.2f} +0/-0.10 x {S.CAP_STUD_DOG_L}")
    D.leader(ax, ((L.LOUV_RI + L.LOUV_RO) / 2, (L.FLANGE_T + L.LOUV_FLOOR_OUT) / 2), (R * 0.75, L.COL_TOP + 2.5), "8 deg cone +/-0.3 deg")
    D.leader(ax, (-R * 0.6, 0), (-R * 1.2, -5.5), "underside: one flat face,\nflat 0.05, NO recess")
    plan = D.plan_polylines(c, ("x", "y"))
    D.view(fig, [0.62, 0.45, 0.36, 0.48], [(plan, "k", 0.5, "-")], title="TOP VIEW (spigot with D-flat, column, cone, window seat)")
    D.save(fig, out_base)


def draw_louver(out_base):
    lv = L.louver_lit()
    fz = L.louver_fin_z()
    fig = _sheet("LABEL-LIGHT LOUVER RING (angular filter)", "RS-CAP-12L-LOUVER",
                 "Prototype: precision SLA in black resin (BMF microArch / Formlabs Form 4 Black, 25 um). Production: micro-moulded PC, black.",
                 f"Fins matte black. Inner {L.LOUV_WHITE_FRAC * 100:.0f}% of every fin (r {L.LOUV_RI}..{L.LOUV_RI + L.LOUV_WHITE_FRAC * (L.LOUV_RO - L.LOUV_RI):.1f}) white: "
                 "dip the bore edge in white reflector ink 1.5 mm deep, or 2-shot mould.",
                 [f"{L.LOUV_N} conical fins {L.LOUV_FIN_T} thick, pitch {L.LOUV_PITCH}, sloping DOWN toward the outside at "
                  f"{', '.join(f'{t:.0f}' for t in L.LOUV_TILTS[1:])} deg (bottom to top); inner-edge fin bottoms at z {', '.join(f'{z:.2f}' for z in fz)} "
                  f"(cap frame). The floor is the core's 8 deg cone. Geometry unchanged from rev A.",
                  f"Channels clear and parallel: open height {L.LOUV_PITCH - L.LOUV_FIN_T:.2f} +/-0.05 (check on the first SLA articles; reject sagged fins), fin tilt +/-0.5 deg. This part sets where the light lands.",
                  f"{len(L.LOUV_RIB_ANG)} radial ribs {L.LOUV_RIB_W} wide at {', '.join(map(str, L.LOUV_RIB_ANG))} deg join the fins; rib bottoms follow the 8 deg floor.",
                  f"Top face at z {L.LOUV_TOP} +0/-0.05. The dome lip sits {L.LIP_GAP} ABOVE it (rev A 0.05): the louver is never clamped. Retained by 3 dots of UV adhesive on the floor.",
                  "No gloss: fin surfaces matte (Ra > 1.6 um); a glossy fin re-reflects light at the wrong angle."],
                 "SCALE: as shown (enlarged detail at right)")
    sec = D.section_polylines(lv.val(), "XZ", 0.0)
    ax = D.view(fig, [0.04, 0.55, 0.56, 0.38], [(sec, "k", 0.9, "-")], title="SECTION y=0 (ribs at 30/90/150.. deg are not cut)", pad=4)
    D.dim_h(ax, -L.LOUV_RO, L.LOUV_RO, L.LOUV_TOP + 1.5, f"D {2 * L.LOUV_RO:.1f}", off=0.3, ext_from=L.LOUV_TOP)
    D.dim_h(ax, -L.LOUV_RI, L.LOUV_RI, L.LOUV_FLOOR_OUT - 1.0, f"bore D {2 * L.LOUV_RI:.1f}", off=-0.3)
    det = [p for p in sec if p[:, 0].min() > 10]
    ax2 = D.view(fig, [0.04, 0.20, 0.56, 0.33], [(det, "k", 1.2, "-")], title="DETAIL: fins (x = radius)", pad=0.8)
    D.dim_v(ax2, fz[-1], fz[-1] + L.LOUV_FIN_T, L.LOUV_RI - 0.6, f"{L.LOUV_FIN_T}", off=-0.2)
    D.dim_v(ax2, fz[-2], fz[-1], L.LOUV_RI - 1.4, f"pitch {L.LOUV_PITCH}", off=-0.2)
    D.leader(ax2, (L.LOUV_RO, fz[0] - (L.LOUV_RO - L.LOUV_RI) * math.tan(math.radians(L.LOUV_TILTS[1]))), (L.LOUV_RO + 0.5, L.LOUV_FLOOR_OUT + 0.2), "fins slope 8/8/7/6/4 deg down (bottom to top)")
    plan = D.plan_polylines(lv, ("x", "y"), zmin=L.LOUV_TOP - 0.3)
    D.view(fig, [0.62, 0.45, 0.36, 0.48], [(plan, "k", 0.5, "-")], title="TOP VIEW (6 ribs)")
    D.save(fig, out_base)


def draw_window(out_base):
    w = L.window_lit()
    fig = _sheet("LABEL-LIGHT WINDOW RING", "RS-CAP-12L-WINDOW",
                 "Clear polycarbonate (Makrolon 2407 or equal) or PMMA, turned from tube or moulded",
                 f"Inner face polished/clear. OUTER face light satin: scatter sigma ~{L.WIN_SATIN_DEG:.0f} deg (glass-bead blast 150-200 grit at low pressure, "
                 "or mould texture MT-11010). Approve on a sample: satin 1-6 deg changes the light profile, see DESIGN.md sec. 5.",
                 [f"Ring D {2 * L.WIN_RO:.2f} x D {2 * L.WIN_RI:.2f} x {L.WIN_Z1 - L.WIN_Z0:.2f} +0/-0.05 high. Geometry unchanged from rev A.",
                  f"Sits on the core flange under the dome lip overhang (1.0 mm). The lip is {L.LIP_GAP} ABOVE its top face (rev A 0.05): it is never clamped. 3 dots of UV adhesive.",
                  "No yellowing grade: UV-stabilised PC or PMMA."],
                 "SCALE: as shown")
    sec = D.section_polylines(w.val(), "XZ", 0.0)
    ax = D.view(fig, [0.05, 0.30, 0.55, 0.60], [(sec, "k", 1.0, "-")], title="SECTION y=0", pad=4)
    D.dim_h(ax, -L.WIN_RO, L.WIN_RO, L.WIN_Z1 + 1.5, f"D {2 * L.WIN_RO:.2f}", off=0.3, ext_from=L.WIN_Z1)
    D.dim_h(ax, -L.WIN_RI, L.WIN_RI, L.WIN_Z0 - 1.5, f"D {2 * L.WIN_RI:.2f}", off=-0.3)
    D.dim_v(ax, L.WIN_Z0, L.WIN_Z1, L.WIN_RO + 2, f"{L.WIN_Z1 - L.WIN_Z0:.2f} +0/-0.05", off=0.5)
    D.save(fig, out_base)


def draw_pin(out_base):
    p = L.pin_lit()
    s = L.sleeve_lit()
    z0 = -L.LC_STUD_L
    fig = _sheet("CENTRE CONTACT PIN (headed) + PEEK SLEEVE (coax through the stud)", "RS-CAP-12L-PIN",
                 f"PIN: brass C360, turned: head D {L.PIN_HEAD_D} x {L.PIN_HEAD_H}, shank D {L.PIN_D} (1/16 in), {L.PIN_L} overall. "
                 f"SLEEVE: natural PEEK, turned: OD {L.SLEEVE_OD} +0.01/-0, bore D {L.SLEEVE_ID} +0.03/-0, length {L.SLEEVE_L:.2f} +0/-0.05, counterbore D {L.SLEEVE_CBORE_D} x {L.SLEEVE_CBORE_H:.2f} +0.05/-0 in the tip end.",
                 "PIN: 1.3 um (50 uin) hard gold over 2.5 um nickel, all over (contact face + solder cup). SLEEVE: no finish.",
                 [f"POSITIVE STOPS (rev B): the contact spring pushes the pin INTO the cap, for ever. The sleeve seats on the square shoulder of the stud bore (D {L.LC_BORE_D} to D {L.LC_WIRE_BORE_D}); the pin HEAD seats on the counterbore floor in the sleeve. Neither can move inward. No Loctite 609, no staking (rev A; anaerobics do not bond PEEK).",
                  f"Pin head face flat (or R 3 crown), square within 0.05, edge broken 0.05. Assembled, the gold face sits {L.PIN_RECESS:.2f} +{L.PIN_RECESS_TOL}/-0 BELOW the stud tip face.",
                  "Solder cup D 0.8 x 2.0 deep in the top end for the 30 AWG PTFE lead (pre-tin).",
                  f"Assembly: solder the lead to the pin; feed the lead up through the sleeve, seat the head in the counterbore; feed the lead up the stud bore from the tip; press the sleeve home on the shoulder (0.025 interference in D {L.LC_BORE_D}). Sleeve end flush with the stud tip +0/-0.05.",
                  "Test: push 5 N on the pin face, no movement. Pull 2 N on the lead, pin stays seated. Pin to stud > 100 Mohm at 50 V DC. No solder or flux on the stud tip face."],
                 "SCALE: as shown (enlarged)")
    sp = D.section_polylines(p.val(), "XZ", 0.0)
    ss = D.section_polylines(s.val(), "XZ", 0.0)
    ax = D.view(fig, [0.05, 0.25, 0.55, 0.68], [(ss, "#555555", 0.9, "-"), (sp, "k", 1.1, "-")], title="SECTION (pin black, sleeve grey), z = cap frame; stud tip at the bottom", pad=2.4)
    D.dim_v(ax, z0 + L.PIN_RECESS, z0 + L.PIN_RECESS + L.PIN_L, 3.2, f"pin {L.PIN_L}", off=0.3)
    D.dim_v(ax, z0, z0 + L.SLEEVE_L, -3.2, f"sleeve {L.SLEEVE_L:.2f} +0/-0.05", off=-0.3)
    D.dim_h(ax, -L.PIN_HEAD_D / 2, L.PIN_HEAD_D / 2, z0 - 1.0, f"head D {L.PIN_HEAD_D} x {L.PIN_HEAD_H}", off=-0.2)
    D.dim_h(ax, -L.SLEEVE_OD / 2, L.SLEEVE_OD / 2, z0 + L.SLEEVE_L + 1.0, f"D {L.SLEEVE_OD} PEEK", off=0.2)
    D.leader(ax, (L.PIN_D / 2, z0 + 5.0), (2.4, z0 + 6.5), f"shank D {L.PIN_D}")
    D.leader(ax, (L.SLEEVE_CBORE_D / 2, z0 + L.SLEEVE_CBORE_H), (2.4, z0 + 2.2), f"c'bore D {L.SLEEVE_CBORE_D} x {L.SLEEVE_CBORE_H:.2f} +0.05/-0")
    D.save(fig, out_base)


def draw_carrier(out_base):
    c = L.carrier()
    pl = L.plunger()
    sp = L.spring()
    fig = _sheet("HUB CONTACT CARRIER + GUARD TUBE, plunger and spring", "RS-HUB-12L-CARRIER",
                 f"CARRIER: PEEK (preferred) or PA66-GF30, machined; prototype SLA Formlabs High Temp / Tough 2000. Insulator. "
                 f"PLUNGER: brass C360 or BeCu, turned, nose D {L.PLG_NOSE_D} with R 0.3 crown. SPRING: catalogue compression spring, see note 4.",
                 "CARRIER as machined, no metal inserts. PLUNGER: 1.3 um hard gold over 2.5 um nickel all over.",
                 [f"Sits in the RS-HUB-01 rev B centre relief (D {S.CAP_RELIEF_D} x {S.CAP_RELIEF_DEPTH}) on top of RS-PCB-12L-HUB; frame z=0 = backplate back face. Body D {L.CAR_D} x {L.CAR_Z1 - L.CAR_Z0:.2f} +/-0.05.",
                  f"GUARD TUBE = the spigot: D {L.SPIG_D:.2f} +0/-0.03, top at z {L.GUARD_TOP} ({L.SPIG_L:.2f} +/-0.05 above the body), {L.SPIG_CHAMFER} x 45 lead-in. It pilots in the back of the E-Z Lok thread (minor D {L.LC_INSERT_MINOR_D}..{L.LC_INSERT_MINOR_MAX}) "
                  f"and its top is a HARD STOP {L.stack(L.REC_T_MIN)['tip_to_guard'] - L.TOL_LOW:.2f} below the lowest position a correct lit-cap stud can reach with every tolerance stacked: no screw of any length can crush the contact.",
                  f"Plunger bore D {L.GUARD_BORE_D} +0.05/-0 from the underside to {L.GUARD_LIP_T} below the guard top; D {L.GUARD_NOSE_HOLE_D} +0.03/-0 through the {L.GUARD_LIP_T} lip. The lip retains the plunger (flange D {L.PLG_FLANGE_D} x {L.PLG_FLANGE_H}) with the cap off; nose tip then stands at z {L.PLG_FREE_TIP} ({L.PLG_TRAVEL:.1f} of travel down to the guard top).",
                  f"SPRING (calc, catalogue SKU to be picked): OD {L.SPRING['od']}, wire {L.SPRING['wire']}, free length {L.SPRING['free']}, {L.SPRING['n_total']} coils closed ends, about {L.SPRING['rate']} N/mm, stainless. "
                  f"Solid height must be <= {L.spring_len(L.GUARD_TOP):.1f}. It sits on a flat gold pad on the PCB and on the plunger pilot (D {L.PLG_PILOT_D} x {L.PLG_PILOT_H}); it carries the 20 mA.",
                  f"Return pin guide bore D {L.POGO_BORE_D} thru at ({L.POGO_R_POS[0]}, {L.POGO_R_POS[1]}) for Mill-Max {L.POGO_RET['pn']} (SMT on the PCB; working height {-L.CAR_Z0} against the insert's back end). Confirm bore = barrel OD + 0.10 against the Mill-Max drawing.",
                  f"Underside pockets: CCR {L.CCR_POCKET[0]} x {L.CCR_POCKET[1]} x {L.CCR_POCKET[2]}, D1 {L.D1_POCKET[0]} x {L.D1_POCKET[1]}, Z1 {L.Z1_POCKET[0]} x {L.Z1_POCKET[1]}, F1 {L.F1_POCKET[0]} x {L.F1_POCKET[1]}; wire notch {L.WIRE_NOTCH_W} wide toward +Y. "
                  "Drop spring + plunger into the bore, bond the carrier to the PCB with 2 dots of epoxy (none in the bore). Test: plunger returns freely from full depth 10 times."],
                 "SCALE: as shown")
    sec = D.section_polylines(c.val(), "XZ", 0.0)
    secp = D.section_polylines(pl.val(), "XZ", 0.0)
    secs = D.section_polylines(sp.val(), "XZ", 0.0)
    ax = D.view(fig, [0.05, 0.25, 0.55, 0.68], [(sec, "k", 1.0, "-"), (secp, "#9b6a00", 0.9, "-"), (secs, "#555555", 0.6, "-")],
                title="SECTION y=0 (backplate back face at z=0); plunger shown free (cap off), spring grey", pad=7)
    D.dim_h(ax, -L.CAR_D / 2, L.CAR_D / 2, L.CAR_Z0 - 1.5, f"D {L.CAR_D}", off=-0.3)
    D.leader(ax, (-L.SPIG_D / 2, 0.6), (-L.CAR_D / 2 - 6.0, 6.2), f"guard tube D {L.SPIG_D:.2f} +0/-0.03")
    D.dim_v(ax, L.CAR_Z0, L.CAR_Z1, L.CAR_D / 2 + 1.5, f"{L.CAR_Z1 - L.CAR_Z0:.2f} +/-0.05", off=0.4)
    D.dim_v(ax, L.CAR_Z1, L.GUARD_TOP, L.CAR_D / 2 + 1.5, f"{L.SPIG_L:.2f} +/-0.05", off=0.4)
    D.dim_v(ax, L.GUARD_TOP, L.PLG_FREE_TIP, L.CAR_D / 2 - 2.0, f"travel {L.PLG_TRAVEL:.1f}", off=0.4, ext_from=L.PLG_NOSE_D / 2)
    D.leader(ax, (-L.GUARD_BORE_D / 2, -3.0), (-L.CAR_D / 2 - 6.0, 0.8), f"bore D {L.GUARD_BORE_D} +0.05/-0")
    D.leader(ax, (-L.GUARD_NOSE_HOLE_D / 2, L.GUARD_TOP - 0.4), (-L.CAR_D / 2 - 6.0, 3.6), f"lip {L.GUARD_LIP_T}, hole D {L.GUARD_NOSE_HOLE_D} +0.03/-0")
    D.leader(ax, (L.PLG_NOSE_D / 2, 5.0), (L.CAR_D / 2 + 1.0, 8.0), f"plunger nose D {L.PLG_NOSE_D}, gold")
    plan = D.plan_polylines(c, ("x", "y"))
    D.view(fig, [0.62, 0.45, 0.36, 0.48], [(plan, "k", 0.6, "-")], title="TOP VIEW (+Y = 12 o'clock, toward the splice cavity)")
    D.save(fig, out_base)


def draw_assembly_lit(out_base, parts):
    fig = _sheet("LABEL-LIGHT STACK, section through the spindle axis", "RS-ASM-12L",
                 "see label-light/DESIGN.md parts list", "n/a",
                 ["Section x=0, world frame (wall at z=0). Black = custom, grey = purchased, red dashed = customer record.",
                  "Clamp: flat core flange - PET label washer - record - centre backing ring (felt) - backplate, in one straight line. The record also rests on 6 felt pads, coplanar with the ring.",
                  "+12 V: hub CCR -> spring -> gold plunger in the PEEK guard tube -> headed gold pin at the stud tip -> PTFE lead up the bore -> LED PCB.",
                  "Return: LED PCB (both faces) -> column + dome boss -> brass core -> 1/4-20 thread -> E-Z Lok insert -> return spring pin on the insert's back end -> hub PCB.",
                  "Light: 6 LEDs face DOWN into a white cavity; it leaks out only through the 5-channel louver and the satin window, under the chrome lip, and grazes the label.",
                  "Stack numbers, contact travel and the full tolerance stack: checks.md, section 'Label light'.",
                  f"HALO (right-hand view): identical to the plain-cap sconce RS-ASM-12-MDF. 8 mm strip on the BACK of the backplate facing the wall, on the {S.HEAT_RING_T} aluminium ring RS-HR-12 over the {S.CORK_RING_T} cork ring RS-CK-12, strip centred on R {S.HALO_STRIP_R:.0f}, 4x #4 x 3/8 screws on R {S.HALO_SCREW_R}. No strip on the rim.",
                  f"From the wall, measured on this assembly: backplate back {S.HUB_T:.2f}, record front {max(p.val().BoundingBox().zmax for n, p, c, k in parts if n.startswith('record')):.2f}, lit cap tip {max(p.val().BoundingBox().zmax for n, p, c, k in parts if n == 'lit_dome'):.2f} (furthest point)."],
                 "SCALE: as shown", rev="B.1", supersedes="rev A, A.1, B (B showed the LED strip on the rim)")
    colors = {"custom": "k", "purchased": "#555555", "customer": "#9b1c1c"}
    layers = []
    for n, p, c, kind in parts:
        sec = D.section_polylines(p.val(), "YZ", 0.0)
        sec = [s for s in sec if abs(s[:, 0]).max() < 60 or kind != "customer"]
        sec = [s[(abs(s[:, 0]) < 60)] for s in sec]
        sec = [s for s in sec if len(s) > 1]
        if sec:
            layers.append((sec, colors[kind], 0.9 if kind == "custom" else 0.6, "-" if kind != "customer" else "--"))
    ax = D.view(fig, [0.03, 0.22, 0.60, 0.72], layers, title="SECTION x=0, cap + backplate + hub centre (world z, mm)", pad=2)
    ax.set_xlim(-26, 26)
    ax.set_ylim(14, 58)
    D.halo_detail(fig, [0.66, 0.22, 0.32, 0.72], parts)
    D.save(fig, out_base)
