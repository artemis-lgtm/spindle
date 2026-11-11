"""Regression gates for the Fable 5.2 pessimist review (cad/REVIEW-fable52.md) and for the heat-safe halo, layout D
(cad/FIXES-heat-layout.md, gates tagged HEAT).

build_all.py collects every derived number into `checks`, then calls run_gates(). Each gate names the review item it
protects, the number, and the rule. If any gate fails the build exits non-zero, so a later edit cannot quietly put a
fixed dimension back. Three kinds of evidence:
  clearances      : numbers derived from the parameters (assembly.clearance_numbers, sconce_lit.clearance_numbers_lit)
  geometry_probes : point-in-solid probes on the solids that become the STEP files (catches "the parameter says 6
                    pockets but the solid has 3", which is exactly how review item M11b happened)
  documents       : stale sentences that must not reappear in the BOM, the site copy or the reports
"""
import os
import re
import cadquery as cq
import sconce_cad as S
import sconce_lit as L


def _inside(shape, x, y, z):
    return bool(shape.val().isInside(cq.Vector(x, y, z), 1e-6))


def geometry_probes():
    out = {}
    # ---- backplates: felt targets and the centre-ring witness circle really are in the solid
    for name, d, radii, ring_spec in (("12in", S.BP12_D, (S.PAD_R_OUT, S.PAD_R_IN), S.CENTER_RING),
                                      ("7in", S.BP7_D, (S.PAD_R_IN,), S.CENTER_RING7)):
        bp = S.backplate(d, pads_out=(d > 200))
        n = 0
        for rr in radii:
            for a in S.PAD_ANGLES:
                x, y = S.pol(rr, a)
                n += 0 if _inside(bp, x, y, S.BP_T - S.PAD_TARGET_DEPTH / 2) else 1
        out[f"backplate_{name}_felt_target_pockets_found_in_the_solid"] = n
        rw = (ring_spec[0] + S.CENTER_WITNESS_CLR) / 2
        if S.CENTER_POCKET_DEPTH > 0:
            seat = not _inside(bp, rw - 1.0, 0, S.BP_T - S.CENTER_POCKET_DEPTH / 2)
        else:
            seat = (not _inside(bp, rw, 0, S.BP_T - S.CENTER_WITNESS_DEPTH / 2)) and _inside(bp, rw - 2.0, 0, S.BP_T - 0.05)
        out[f"backplate_{name}_centre_ring_seat_found_in_the_solid(1 = yes)"] = int(seat)
    # ---- hub
    h = S.hub()
    out["hub_centre_relief_measured_depth_ok(1 = yes)"] = int(
        (not _inside(h, 0, 0, S.HUB_T - S.CAP_RELIEF_DEPTH + 0.2)) and _inside(h, 0, 0, S.HUB_T - S.CAP_RELIEF_DEPTH - 0.2))
    out["hub_has_no_panel_jack_hole(1 = yes: solid at r 3.7 from the cable hole axis)"] = int(
        _inside(h, 3.7, S.JACK_Y, S.POCKET_DEPTH + 1.0) and not _inside(h, 0, S.JACK_Y, S.POCKET_DEPTH + 1.0))
    out["hub_p_clip_pilot_found(1 = yes)"] = int(not _inside(h, S.CLIP_POS[0], S.CLIP_POS[1], S.POCKET_DEPTH + 2.0))
    a0 = S.STUD_ANGLES[0]
    xm, ym = S.pol(S.STUD_R, a0 - S.LOCK_ARC_DEG)
    xp, yp = S.pol(S.STUD_R, a0 + S.LOCK_ARC_DEG)
    zc = S.HUB_RECESS_DEPTH + S.JWEB_T / 2                 # inside the J-web: open only at an entry hole
    out["hub_j_slot_entry_is_clockwise_side_in_the_solid(1 = yes)"] = int((not _inside(h, xm, ym, zc)) and _inside(h, xp, yp, zc))
    # ---- plain caps
    c12, c7 = S.dome_cap_12(), S.dome_cap_7()
    out["cap12_stud_tip_z_measured_mm"] = round(c12.val().BoundingBox().zmin, 3)
    out["cap7_stud_tip_z_measured_mm"] = round(c7.val().BoundingBox().zmin, 3)
    rs = S.CAP_SHOULDER_D / 2 - 0.1
    out["cap12_smooth_shoulder_found(1 = yes)"] = int(
        _inside(c12, rs, 0, -S.CAP_SHOULDER_L / 2) and not _inside(c12, rs, 0, -S.CAP_SHOULDER_L - S.CAP_STUD_RELIEF_L / 2))
    out["cap12_mass_g_brass_8.5"] = round(c12.val().Volume() * 8.5e-3, 1)
    out["cap7_mass_g_brass_8.5"] = round(c7.val().Volume() * 8.5e-3, 1)
    # ---- lit core / dome / sleeve / pin
    core, dome = L.core_lit(), L.dome_lit()
    tip = -L.LC_STUD_L
    r_between = (L.LC_BORE_D / 2 + L.LC_WIRE_BORE_D / 2) / 2          # inside the sleeve bore, outside the wire bore
    out["core_bore_shoulder_found(1 = yes: open below the step, solid above it)"] = int(
        (not _inside(core, r_between, 0, tip + L.LC_BORE_STEP - 0.5)) and _inside(core, r_between, 0, tip + L.LC_BORE_STEP + 0.5))
    out["core_underside_has_no_felt_recess(1 = yes)"] = int(_inside(core, 5.5, 0, 0.3) and _inside(core, 4.0, 0, 0.3))
    zk = L.COL_TOP + L.SPG_KEY_H
    rk = -(L.SPG_D / 2 - 0.1)          # on the round side of the key (the flat is at +x)
    out["core_key_top_measured_below_min_pcb_top(1 = yes)"] = int(
        _inside(core, rk, 0, zk - 0.05) and not _inside(core, rk, 0, zk + 0.05) and zk < L.COL_TOP + L.LPCB_T - L.LPCB_T_TOL)
    zb = L.LPCB_Z0 + L.LPCB_T
    rc = (L.SPG_D / 2 + L.BOSS_CBORE_D / 2) / 2                        # just outside the D 8.0 key
    out["dome_boss_counterbore_found(1 = yes)"] = int(
        (not _inside(dome, rc, 0, zb + L.BOSS_CBORE_H / 2)) and _inside(dome, rc, 0, zb + L.BOSS_CBORE_H + 0.3))
    out["dome_lip_face_z_measured_mm"] = round(dome.val().BoundingBox().zmin, 3)
    out["louver_top_z_measured_mm"] = round(L.louver_lit().val().BoundingBox().zmax, 3)
    out["window_top_z_measured_mm"] = round(L.window_lit().val().BoundingBox().zmax, 3)
    out["lip_gap_measured_on_the_solids_mm"] = round(
        dome.val().BoundingBox().zmin - max(L.louver_lit().val().BoundingBox().zmax, L.window_lit().val().BoundingBox().zmax), 3)
    pin, slv = L.pin_lit(), L.sleeve_lit()
    out["pin_head_dia_measured_mm"] = round(pin.val().BoundingBox().xlen, 3)
    out["sleeve_top_z_minus_bore_shoulder_z_measured_mm"] = round(slv.val().BoundingBox().zmax - (tip + L.LC_BORE_STEP), 3)
    car = L.carrier()
    out["guard_tube_top_z_measured_mm"] = round(car.val().BoundingBox().zmax, 3)
    out["plunger_free_tip_z_measured_mm"] = round(L.plunger().val().BoundingBox().zmax, 3)
    out.update(halo_probes())
    return out


BP7_REV_B_VOLUME = 220801.9      # mm3, RS-BP-7-MDF rev B as built on 2026-11-11 BEFORE the heat-layout change
PROJECTION = dict(record_front=41.23, plain_cap_tip=51.78, lit_cap_tip=56.48)   # mm from the wall, before the change


def halo_probes():
    """Heat-safe halo, layout D: measured on the solids and on the placed assemblies, not on the parameters."""
    import assembly as A
    import assembly_lit as AL
    out = {}
    t, R = S.BP_T, S.BP12_D / 2
    bp = S.backplate()
    out["backplate_12in_rim_rabbet_is_gone(1 = yes: solid 0.5 inside the rim at mid thickness)"] = int(_inside(bp, R - 0.5, 0, t / 2))
    out["backplate_12in_rim_notch_is_gone(1 = yes: solid at 6 o'clock, 0.5 inside the rim, 1.0 above the back face)"] = int(
        _inside(bp, 0, -(R - 0.5), 1.0))
    n = 0
    front_ok = 1
    for a in S.HALO_SCREW_ANGLES:
        x, y = S.pol(S.HALO_SCREW_R, a)
        n += int((not _inside(bp, x, y, S.HALO_PILOT_DEPTH / 2)) and _inside(bp, x, y, S.HALO_PILOT_DEPTH + 0.5))
        front_ok &= int(_inside(bp, x, y, t - 0.05))
    out["backplate_12in_heat_ring_pilots_found_in_the_solid"] = n
    out["backplate_12in_front_face_is_solid_over_every_pilot(1 = yes)"] = front_ok
    out["backplate_12in_back_channel_runs_R60_to_R97_only(1 = yes)"] = int(
        (not _inside(bp, 0, -90.0, 1.0)) and _inside(bp, 0, -(S.BACK_CHAN_R1 + 1.5), 1.0) and _inside(bp, 0, -(R - 5.0), 1.0))
    bp7 = S.backplate(S.BP7_D, pads_out=False)
    out["backplate_7in_still_has_its_rim_rabbet(1 = yes: variant deliberately unchanged)"] = int(
        not _inside(bp7, S.BP7_D / 2 - 0.5, 0, t / 2))
    out["backplate_7in_volume_minus_rev_B_volume_mm3(0 = geometry unchanged)"] = round(bp7.val().Volume() - BP7_REV_B_VOLUME, 1)
    for name, shape, th, hole in (("heat_ring", S.heat_ring(), S.HEAT_RING_T, S.HEAT_RING_HOLE_D),
                                  ("cork_ring", S.cork_ring(), S.CORK_RING_T, S.CORK_RING_HOLE_D)):
        bb = shape.val().BoundingBox()
        out[f"{name}_od_measured_mm"] = round(bb.xlen, 3)
        out[f"{name}_thickness_measured_mm"] = round(bb.zlen, 3)
        out[f"{name}_id_measured_ok(1 = yes: open at R 99.9, solid at R 100.1)"] = int(
            (not _inside(shape, S.HALO_RING_ID / 2 - 0.1, 0, th / 2)) and _inside(shape, S.HALO_RING_ID / 2 + 0.1, 0, th / 2))
        k = 0
        for a in S.HALO_SCREW_ANGLES:
            x, y = S.pol(S.HALO_SCREW_R, a)
            xe, ye = S.pol(S.HALO_SCREW_R + hole / 2 + 0.2, a)
            k += int((not _inside(shape, x, y, th / 2)) and _inside(shape, xe, ye, th / 2))
        out[f"{name}_screw_holes_found_in_the_solid"] = k
    out["heat_ring_mass_g_5052_at_2.68"] = round(S.heat_ring().val().Volume() * 2.68e-3, 1)
    # placed assemblies: plain and lit must carry the SAME halo stack, and nothing may move forward
    plain = {nm: q.val() for nm, q, c, k in A.build("12", "mdf")}
    lit = {nm: q.val() for nm, q, c, k in AL.build_lit()}
    halo = [nm for nm in plain if nm.startswith(("cork_ring", "heat_ring", "led_cob_strip"))]
    same = len(halo) == 7
    for nm in halo:
        if nm not in lit:
            same = False
            continue
        a, b = plain[nm].BoundingBox(), lit[nm].BoundingBox()
        same &= all(abs(u - v) < 1e-6 for u, v in ((a.xmin, b.xmin), (a.xmax, b.xmax), (a.ymin, b.ymin), (a.ymax, b.ymax),
                                                     (a.zmin, b.zmin), (a.zmax, b.zmax))) and abs(plain[nm].Volume() - lit[nm].Volume()) < 1e-6
    out["plain_and_lit_assemblies_carry_the_identical_halo_stack(1 = yes, 7 solids)"] = int(same)
    for tag, asm in (("plain", plain), ("lit", lit)):
        out[f"{tag}_strip_face_to_wall_measured_mm"] = round(asm["led_cob_strip"].BoundingBox().zmin, 3)
        out[f"{tag}_halo_lowest_point_to_wall_measured_mm"] = round(min(asm[nm].BoundingBox().zmin for nm in halo), 3)
        out[f"{tag}_halo_stack_top_minus_backplate_back_face_measured_mm"] = round(
            asm["cork_ring"].BoundingBox().zmax - asm["backplate_12_mdf"].BoundingBox().zmin, 3)
        out[f"{tag}_aluminium_ring_to_hub_measured_mm"] = round(asm["heat_ring_alu"].distance(asm["hub"]), 3)
        out[f"{tag}_halo_stack_to_inline_jack_measured_mm"] = round(
            min(asm[nm].distance(asm["inline_jack"]) for nm in halo), 3)
        out[f"{tag}_halo_stack_to_adapter_plug_and_cable_measured_mm"] = round(
            min(asm[nm].distance(asm["adapter_plug"]) for nm in halo), 3)
        out[f"{tag}_halo_stack_to_bayonet_studs_measured_mm"] = round(
            min(asm[nm].distance(asm[s_]) for nm in halo for s_ in asm if s_.startswith("pem_stud")), 3)
        out[f"{tag}_record_front_face_from_wall_measured_mm"] = round(asm["record_12"].BoundingBox().zmax, 2)
    out["plain_cap_tip_from_wall_measured_mm"] = round(plain["dome_cap_12"].BoundingBox().zmax, 2)
    out["lit_cap_tip_from_wall_measured_mm"] = round(lit["lit_dome"].BoundingBox().zmax, 2)
    out["plain_furthest_point_of_anything_from_wall_measured_mm"] = round(max(v.BoundingBox().zmax for v in plain.values()), 2)
    out["lit_furthest_point_of_anything_from_wall_measured_mm"] = round(max(v.BoundingBox().zmax for v in lit.values()), 2)
    # negative control: a ring WITHOUT screw holes must show up as an interference (proves the 0-hit result is live)
    blank = S.ring(S.HALO_RING_OD / 2, S.HALO_RING_ID / 2, S.HEAT_RING_T).translate((0, 0, S.HALO_Z_ALU))
    v = blank.val().intersect(S.halo_screw(S.HALO_SCREW_ANGLES[0]).val()).Volume()
    out["negative_control_ring_without_holes_is_caught_as_interference(1 = yes)"] = int(v > 0.5)
    return out


def sheet_numbers(sheet_log):
    return {
        "sheets_drawn": len(sheet_log),
        "lowest_note_line_y(border at 0.010)": min(s["notes_lowest_y"] for s in sheet_log),
        "lowest_title_block_line_y(border at 0.010)": min(s["title_block_lowest_y"] for s in sheet_log),
        "sheets_with_the_general_tolerance_line": sum(1 for s in sheet_log if s["has_tolerance_line"]),
        "smallest_note_font_pt": min(s["notes_pt"] for s in sheet_log),
        "revisions": ", ".join(f"{s['part']} {s['rev']}" for s in sheet_log),
    }


# (file relative to the project root, regex that must NOT match, what it was)
STALE = [
    ("site/product.html", r"4 to 10\s*W", "wattage 4 to 10 W (hard cap is 6 W)"),
    ("site/faq.html", r"4 to 10\s*(W|watts)", "wattage 4 to 10 W (hard cap is 6 W)"),
    ("site/index.html", r"4 to 10\s*(W|watts)", "wattage 4 to 10 W (hard cap is 6 W)"),
    ("site/faq.html", r"1/4-20 post", "phantom post (the stud is part of the cap)"),
    ("site/product.html", r"1/4-20 post", "phantom post (the stud is part of the cap)"),
    ("site/index.html", r"1/4-20 post", "phantom post (the stud is part of the cap)"),
    ("site/faq.html", r"Every electrical component is UL or ETL listed", "UL over-claim"),
    ("site/product.html", r"Hub with DC jack", "panel jack in the hub (now a pigtail)"),
    ("build/BOM.md", r"M3 x 6 cup", "M3 x 6 set screw (cannot reach the tab)"),
    ("build/BOM.md", r"8-32 shoulder screws", "shoulder-screw bayonet (CAD uses PEM FH-832-10 + lock nuts)"),
    ("build/BOM.md", r'1" OD x 3/8" ID x 1/8"', "1/8 in cap felt (stands 2.2 proud)"),
    ("build/BOM.md", r'1" centre hole', "1 in round centre hole in the plate (it is a 30 x 37 slot)"),
    ("build/BOM.md", r"jack pocket at 6 o'clock", "jack at 6 o'clock"),
    ("build/BOM.md", r'1/4-20 x 1" hex bolt', "bonded cap on a 1 in bolt"),
    ("mounting-report.md", r"simply turns down", "surface cord into a wall-normal jack"),
    ("mounting-report.md", r"twist (counter|anti)", "bayonet direction"),
    ("cad/README.md", r"3/8 in ID x 1/8 in", "1/8 in cap felt"),
    ("cad/README.md", r"= 63 g", "cap mass 63 g"),
    ("cad/label-light/PCB-SPEC.md", r"12 V bidirectional", "bidirectional 12 V TVS"),
    ("cad/label-light/DESIGN.md", r"Loctite 609", "anaerobic on PEEK"),
    ("cad/rfq/dome-cap-brass/SPEC.txt", r"cut to 1[78]\.\d", "separate-stud option"),
    # heat-safe halo, layout D (2026-11-11): the 12 in strip is on the BACK face. These sentences described the rim strip.
    ("build/BOM.md", r"Mounted on the backplate RIM", "12 in strip on the rim"),
    ("build/BOM.md", r'10\.5" dia x 1/2" MDF, 25/64" centre hole, rim rabbet', "12 in backplate with a rim rabbet"),
    ("cad/README.md", r"LED ring placement, decided for now: RIM", "rim placement as the decision"),
    ("cad/label-light/DESIGN.md", r"halo strip on the rim", "halo strip on the rim"),
    ("site/product.html", r"sits on the (backplate )?rim|ring on its rim|COB ring on the backplate rim|33-inch", "LED ring on the rim in the site copy"),
    ("site/faq.html", r"sits on the (backplate )?rim|ring on its rim|COB ring on the backplate rim|33-inch", "LED ring on the rim in the site copy"),
    ("site/index.html", r"sits on the (backplate )?rim|ring on its rim|COB ring on the backplate rim|33-inch", "LED ring on the rim in the site copy"),
    ("site/install.html", r"sits on the (backplate )?rim|ring on its rim|COB ring on the backplate rim|33-inch", "LED ring on the rim in the site copy"),
    ("cad/explode_fix.py", r"new_strip|new_alu|new_cork", "hand-injected fake ring parts in the heat-safe drawing"),
    # cork is 1/16 in (1.6 mm) since the live quotes of 2026-11-11; 2 mm sheet is not stocked
    ("build/BOM.md", r"2\.0 mm cork sheet", "2.0 mm cork in the BOM"),
    ("build/BOM.md", r"NOT YET PRICED", "heat rings left unpriced in the BOM"),
    ("cad/explode_fix.py", r"2 mm of insulation|cork ring, 2 mm", "2 mm cork in the heat-safe drawing legend"),
    ("cad/explode_view.py", r"2 mm of cork", "2 mm cork in the exploded drawing legend"),
    ("cad/rfq/cork-ring/SPEC.txt", r"5/64", "5/64 in (2 mm) cork in the cork RFQ"),
]
# (file, regex that MUST match, what it proves)
REQUIRED = [
    ("cad/rfq/dome-cap-brass/SPEC.txt", r"REVISION STATUS", "revision block on the plain cap RFQ"),
    ("cad/rfq/dome-cap-lit/SPEC.txt", r"REVISION STATUS", "revision block on the lit cap RFQ"),
    ("cad/rfq/backplate-mdf-cnc/SPEC.txt", r"SIX on the 12 in part", "six felt targets in the backplate RFQ"),
    ("cad/rfq/README.md", r"SUPERSEDED", "RFQ index lists superseded revisions"),
    ("site/product.html", r"up to 6 W", "6 W cap on the product page"),
    ("site/faq.html", r"sits on the back of the backplate, facing the wall", "site FAQ puts the LED ring on the back of the backplate"),
    ("NOTES.md", r"(?i)render discrepancy", "render / CAD LED placement discrepancy is on record"),
    ("build/BOM.md", r"RS-HR-12", "aluminium heat ring is in the BOM"),
    ("build/BOM.md", r"RS-CK-12", "cork ring is in the BOM"),
    ("build/BOM.md", r"\$47\.46", "12 in parts total at 100 includes the two heat rings and their screws"),
    ("build/BOM.md", r"\$7\.38", "heat ring price is the quote of the canonical file with its holes"),
    ("build/BOM.csv", r"TOTAL parts,91\.98,68\.0,47\.46,38\.48", "BOM.csv 12 in total matches BOM.md"),
    ("cad/rfq/cork-ring/SPEC.txt", r"1\.6 mm \(1/16 in\)", "cork RFQ says 1/16 in"),
    ("cad/rfq/heat-ring-aluminum/SPEC.txt", r"REVISION STATUS", "revision block on the heat ring RFQ"),
    ("cad/rfq/cork-ring/SPEC.txt", r"REVISION STATUS", "revision block on the cork ring RFQ"),
    ("cad/rfq/backplate-mdf-cnc/SPEC.txt", r"NO rim rabbet", "12 in backplate RFQ says the rabbet is gone"),
    ("cad/THERMAL.md", r"F  FINAL", "thermal table carries the final geometry"),
    ("mounting-report.md", r"twist clockwise", "install sheet says clockwise (matches the J-slots)"),
]


def document_numbers(root):
    out = {}
    for rel, pat, what in STALE:
        p = os.path.join(root, rel)
        txt = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        out[f"STALE {rel}: {what}"] = len(re.findall(pat, txt))
    for rel, pat, what in REQUIRED:
        p = os.path.join(root, rel)
        txt = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        out[f"REQUIRED {rel}: {what}"] = 1 if re.search(pat, txt) else 0
    sup = os.path.join(root, "cad", "rfq")
    out["superseded zips still sitting in cad/rfq/"] = sum(
        1 for f in os.listdir(sup) if f.endswith(".zip") and re.search(r"revB\.zip|revC\.zip|RS-CAP-12L\.zip", f)
        and not f.startswith("dome-cap-lit-RS-CAP-12L-rev"))
    return out


def run_gates(checks):
    c = checks["clearances"]
    ll = checks["label_light"]["clearances"]
    g = checks["geometry_probes"]
    dr = checks["drawings"]
    doc = checks["documents"]
    res = []

    def gate(item, src, key, op, lim):
        v = src[key]
        ok = {">=": lambda: v >= lim, "<=": lambda: v <= lim, "==": lambda: v == lim,
              "abs<=": lambda: abs(v) <= lim}[op]()
        res.append((item, key, v, f"{op} {lim}", bool(ok)))

    # interference: every assembly, plain and lit
    for k, v in list(checks["interference"].items()) + list(checks["label_light"]["interference"].items()):
        res.append(("all", f"interference hits, {k}", len(v["hits"]), "== 0", len(v["hits"]) == 0))
    # M1 centre backing ring / record flatness
    gate("M1", c, "centre_ring_loaded_top_minus_pad_top_mm(record dish at the clamp, must be 0)", "abs<=", 0.05)
    gate("M1", c, "centre_ring_od_minus_cap_felt_od_mm(clamp is felt-record-felt in line)", "abs<=", 0.5)
    gate("M1", c, "record_back_face_above_backplate_front_face_mm", "==", 1.1)
    gate("M1", g, "backplate_12in_centre_ring_seat_found_in_the_solid(1 = yes)", "==", 1)
    gate("M1", g, "backplate_7in_centre_ring_seat_found_in_the_solid(1 = yes)", "==", 1)
    # M2 key / counterbore
    gate("M2", ll, "pcb_min_top_minus_key_top_mm(must be > 0: boss clamps the PCB, not the key)", ">=", 0.1)
    gate("M2", ll, "boss_counterbore_dia_minus_key_dia_mm(must be > 0)", ">=", 0.2)
    gate("M2", ll, "spigot_thread_engagement_in_dome_boss_mm", ">=", 2.5)
    gate("M2", ll, "negative_control_revA1_key_0.9_would_fail_the_pcb_gate(1 = yes)", "==", 1)
    gate("M2", g, "core_key_top_measured_below_min_pcb_top(1 = yes)", "==", 1)
    gate("M2", g, "dome_boss_counterbore_found(1 = yes)", "==", 1)
    # M3 lip gap
    gate("M3", ll, "louver_top_to_dome_lip_gap_mm", ">=", 0.25)
    gate("M3", ll, "window_top_to_dome_lip_gap_mm", ">=", 0.25)
    gate("M3", ll, "lip_gap_minus_tolerance_stack_mm(must be > 0: the boss is always the stop)", ">=", 0.1)
    gate("M3", g, "lip_gap_measured_on_the_solids_mm", ">=", 0.25)
    # M4 flange
    gate("M4", ll, "flange_solid_thickness_under_the_cavity_mm(no felt recess; must be >= 0.8)", ">=", 0.8)
    gate("M4", g, "core_underside_has_no_felt_recess(1 = yes)", "==", 1)
    # M5 PET washer / studs
    gate("M5", ll, "pet_washer_od_minus_flange_od_mm(flange rides on PET, never on the label)", ">=", 0.5)
    gate("M5", c, "pet_washer_od_minus_cap12_band_od_mm(washer hidden under the cap)", "<=", 0.0)
    gate("M5", c, "pet_washer_od_minus_cap12_band_od_mm(washer hidden under the cap)", ">=", -1.0)
    gate("M5", c, "pet_washer_id_minus_shoulder_mm", ">=", 0.2)
    gate("M5", g, "cap12_stud_tip_z_measured_mm", "==", -11.95)
    gate("M5", ll, "lit_tip_minus_plain_cap12_tip_nominal_mm(asserted <= 0.05)", "abs<=", 0.05)
    # M6 centre contact travel and guard
    gate("M6", ll, "centre_contact_travel_mm(nose free tip to guard top)", ">=", 4.5)
    gate("M6", ll, "worst_case_thin_record_stud_tip_above_guard_tube_mm(must be >= 0.2)", ">=", 0.2)
    gate("M6", ll, "worst_case_thick_record_centre_contact_compression_mm(must be >= 0.5)", ">=", 0.5)
    gate("M6", ll, "plunger_flange_underside_above_spring_solid_height_with_stud_on_guard_mm", ">=", 0.3)
    gate("M6", ll, "return_pin_working_height_worst_min_mm(must be >= 6.63)", ">=", 6.63)
    gate("M6", ll, "return_pin_working_height_worst_max_mm(must be <= 8.87)", "<=", 8.87)
    gate("M6", ll, "worst_case_thick_record_threaded_engagement_mm(must be >= 5.0)", ">=", 5.0)
    gate("M6", g, "guard_tube_top_z_measured_mm", "==", L.GUARD_TOP)
    gate("M6", g, "hub_centre_relief_measured_depth_ok(1 = yes)", "==", 1)
    # M7 wrong caps
    gate("M7", c, "cap_7in_tip_minus_cap_12in_tip_mm(asserted <= 0.05)", "abs<=", 0.05)
    gate("M7", ll, "plain_cap12_in_lit_sconce_thin_record_tip_above_guard_tube_worst_mm", ">=", 0.2)
    gate("M7", ll, "cap7_in_lit_sconce_thin_45_tip_above_guard_tube_worst_mm", ">=", 0.2)
    gate("M7", g, "cap7_stud_tip_z_measured_mm", "==", -S.CAP7_STUD_L)
    # M8 pin / sleeve stops
    gate("M8", ll, "sleeve_od_minus_wire_bore_mm(sleeve seats on the bore shoulder)", ">=", 0.5)
    gate("M8", ll, "pin_head_minus_sleeve_bore_mm(head cannot pass up the sleeve)", ">=", 0.5)
    gate("M8", ll, "sleeve_top_to_bore_shoulder_gap_mm", "abs<=", 0.001)
    gate("M8", ll, "pin_head_top_to_sleeve_counterbore_floor_gap_mm", "abs<=", 0.001)
    gate("M8", ll, "pin_head_to_brass_bore_radial_peek_mm", ">=", 0.3)
    gate("M8", ll, "plunger_to_brass_margin_worst_mm(short-circuit guard)", ">=", 0.3)
    gate("M8", g, "core_bore_shoulder_found(1 = yes: open below the step, solid above it)", "==", 1)
    gate("M8", g, "sleeve_top_z_minus_bore_shoulder_z_measured_mm", "abs<=", 0.001)
    # M9 drawing tolerances
    gate("M9", c, "insert_minor_min_minus_dog_point_max_mm", ">=", 0.1)
    gate("M9", dr, "lowest_note_line_y(border at 0.010)", ">=", 0.012)
    gate("M9", dr, "lowest_title_block_line_y(border at 0.010)", ">=", 0.012)
    res.append(("M9", "every sheet carries the GENERAL TOLERANCES line", dr["sheets_with_the_general_tolerance_line"],
                f"== {dr['sheets_drawn']}", dr["sheets_with_the_general_tolerance_line"] == dr["sheets_drawn"]))
    # M10 pigtail
    gate("M10", c, "pigtail_everything_stays_in_front_of_the_wall_plane_mm(min z of cord + jack + plug)", ">=", 0.5)
    gate("M10", c, "inline_jack_to_backplate_back_face_mm(wall gap minus jack)", ">=", 2.0)
    gate("M10", c, "mated_plug_end_inside_backplate_radius_mm(hidden behind the backplate)", ">=", 0.0)
    gate("M10", c, "cord_underside_above_wall_screw_head_mm", ">=", 1.0)
    gate("M10", c, "inline_jack_through_1in_centred_wall_hole_mm(in-wall route)", ">=", 5.0)
    gate("M10", c, "1in_centred_wall_hole_inside_plate_slot_mm", ">=", 1.0)
    gate("M10", g, "hub_has_no_panel_jack_hole(1 = yes: solid at r 3.7 from the cable hole axis)", "==", 1)
    gate("M10", g, "hub_p_clip_pilot_found(1 = yes)", "==", 1)
    # M11 contradictions
    gate("M11b", g, "backplate_12in_felt_target_pockets_found_in_the_solid", "==", 6)
    gate("M11b", g, "backplate_7in_felt_target_pockets_found_in_the_solid", "==", 3)
    gate("M11b", c, "outer_pad_target_edge_to_backplate_rim_mm(12 in rev C has no rim rabbet)", ">=", 3.0)
    gate("M11d", c, "bayonet_locks_clockwise_seen_from_the_room(1 = yes)", "==", 1)
    gate("M11d", g, "hub_j_slot_entry_is_clockwise_side_in_the_solid(1 = yes)", "==", 1)
    gate("hub", c, "rear_pocket_to_75deg_nut_pocket_web_mm", ">=", 2.0)
    gate("hub", c, "hub_web_relief_floor_to_rear_pocket_ceiling_mm", ">=", 3.0)
    for k, v in doc.items():
        if k.startswith("STALE") or k.startswith("superseded"):
            res.append(("M11", k, v, "== 0", v == 0))
        else:
            res.append(("M11", k, v, "== 1", v == 1))
    # S1 shoulder, S6 lead-in
    gate("S1", c, "record_hole_min_minus_cap_shoulder_mm", ">=", 0.1)
    gate("S1", c, "cap_shoulder_bottom_above_insert_top_worst_mm(1.2 record, felt flat, seat -0.3)", ">=", 0.1)
    gate("S1", g, "cap12_smooth_shoulder_found(1 = yes)", "==", 1)
    gate("S6", ll, "spigot_lead_in_capture_range_mm(carrier floats +/-0.5)", ">=", 0.5)
    gate("stack", c, "cap_12in_threaded_engagement_past_dog_point_mm", ">=", 5.0)
    gate("stack", c, "cap_12in_worst_case_stud_end_above_back_face_1.2mm_record_felt_flat_mm", ">=", 0.5)
    # ---------------------------------------------------------------- HEAT: heat-safe halo, layout D (2026-11-11)
    # ring position: inside the rim, clear of the hub, hub screws and studs
    gate("HEAT", c, "halo_ring_od_inside_backplate_rim_mm", "==", 3.35)
    gate("HEAT", c, "halo_ring_id_outside_hub_mm", ">=", 10.0)
    gate("HEAT", c, "halo_ring_id_outside_hub_screw_countersinks_mm", ">=", 10.0)
    gate("HEAT", c, "halo_ring_id_outside_bayonet_studs_mm", ">=", 10.0)
    for tag in ("plain", "lit"):
        gate("HEAT", g, f"{tag}_aluminium_ring_to_hub_measured_mm", ">=", 10.0)
        gate("HEAT", g, f"{tag}_halo_stack_to_bayonet_studs_measured_mm", ">=", 10.0)
        gate("HEAT", g, f"{tag}_halo_stack_to_inline_jack_measured_mm", ">=", 5.0)
        gate("HEAT", g, f"{tag}_halo_stack_to_adapter_plug_and_cable_measured_mm", ">=", 5.0)
        # the stack sits ON the back face, is 4.7 deep at most, and the strip is 21.2 from the wall
        gate("HEAT", g, f"{tag}_halo_stack_top_minus_backplate_back_face_measured_mm", "abs<=", 0.001)
        gate("HEAT", g, f"{tag}_strip_face_to_wall_measured_mm", "==", 21.2)
        gate("HEAT", g, f"{tag}_halo_lowest_point_to_wall_measured_mm", ">=", 15.0)
    # strip position on the ring: R 111 to 119, with room for the screw heads and no line of sight to the record
    gate("HEAT", c, "halo_strip_inner_edge_radius_mm", "==", 111.0)
    gate("HEAT", c, "halo_strip_outer_edge_radius_mm", "==", 119.0)
    gate("HEAT", c, "halo_strip_outer_edge_inside_ring_od_mm", ">=", 5.0)
    gate("HEAT", c, "halo_strip_outer_edge_inside_backplate_rim_mm(no line of sight from the LEDs to the record)", ">=", 10.0)
    gate("HEAT", c, "halo_strip_inner_edge_to_screw_head_mm", ">=", 2.0)
    gate("HEAT", c, "halo_screw_hole_edge_to_ring_id_mm", ">=", 3.0)
    gate("HEAT", c, "solid_material_between_strip_and_record_mm(aluminium + cork + MDF)", ">=", 15.0)
    # stack height against the 25.4 cavity
    gate("HEAT", c, "halo_stack_height_at_the_strip_mm(cork + aluminium + strip)", "==", 4.2)
    gate("HEAT", c, "halo_stack_height_at_a_screw_head_mm", "<=", 6.0)
    gate("HEAT", c, "halo_cavity_depth_mm(wall to backplate back face)", "==", 25.4)
    gate("HEAT", c, "halo_strip_face_to_wall_mm", ">=", 20.0)
    gate("HEAT", c, "halo_stack_to_inline_jack_gap_along_z_mm", ">=", 5.0)
    # screws: never through the front face, never into a felt target, the lead channel, the hub, a hub screw or the insert
    gate("HEAT", c, "halo_screw_engagement_in_mdf_mm", ">=", 6.0)
    gate("HEAT", c, "halo_screw_tip_behind_backplate_front_face_mm", ">=", 5.0)
    gate("HEAT", c, "halo_pilot_bottom_behind_backplate_front_face_mm", ">=", 4.0)
    gate("HEAT", c, "halo_pilot_depth_minus_screw_engagement_mm", ">=", 1.0)
    gate("HEAT", c, "halo_pilot_bottom_behind_felt_target_floor_mm(even if a pilot sat under a target)", ">=", 3.0)
    gate("HEAT", c, "halo_screw_to_nearest_felt_target_edge_in_plan_mm", ">=", 10.0)
    gate("HEAT", c, "halo_screw_to_back_lead_channel_in_plan_mm", ">=", 10.0)
    gate("HEAT", c, "halo_screw_to_hub_edge_in_plan_mm", ">=", 10.0)
    gate("HEAT", c, "halo_screw_to_nearest_hub_screw_in_plan_mm", ">=", 10.0)
    gate("HEAT", c, "halo_screw_to_insert_bore_in_plan_mm", ">=", 10.0)
    gate("HEAT", c, "back_lead_channel_end_inside_cork_ring_id_mm", ">=", 2.0)
    gate("HEAT", c, "back_lead_channel_start_under_the_hub_mm", ">=", 2.0)
    # the solids that become the STEP / DXF files
    gate("HEAT", g, "backplate_12in_rim_rabbet_is_gone(1 = yes: solid 0.5 inside the rim at mid thickness)", "==", 1)
    gate("HEAT", g, "backplate_12in_rim_notch_is_gone(1 = yes: solid at 6 o'clock, 0.5 inside the rim, 1.0 above the back face)", "==", 1)
    gate("HEAT", g, "backplate_12in_heat_ring_pilots_found_in_the_solid", "==", 4)
    gate("HEAT", g, "backplate_12in_front_face_is_solid_over_every_pilot(1 = yes)", "==", 1)
    gate("HEAT", g, "backplate_12in_back_channel_runs_R60_to_R97_only(1 = yes)", "==", 1)
    for nm, th in (("heat_ring", 1.0), ("cork_ring", 1.6)):
        gate("HEAT", g, f"{nm}_od_measured_mm", "==", 260.0)
        gate("HEAT", g, f"{nm}_thickness_measured_mm", "==", th)
        gate("HEAT", g, f"{nm}_id_measured_ok(1 = yes: open at R 99.9, solid at R 100.1)", "==", 1)
        gate("HEAT", g, f"{nm}_screw_holes_found_in_the_solid", "==", 4)
    gate("HEAT", g, "negative_control_ring_without_holes_is_caught_as_interference(1 = yes)", "==", 1)
    # ONE layout for the plain-cap and the lit-cap sconce (Austin 2026-11-11)
    gate("HEAT", g, "plain_and_lit_assemblies_carry_the_identical_halo_stack(1 = yes, 7 solids)", "==", 1)
    # nothing moved forward: projection from the wall is what it was before the change
    gate("HEAT", g, "plain_record_front_face_from_wall_measured_mm", "==", PROJECTION["record_front"])
    gate("HEAT", g, "lit_record_front_face_from_wall_measured_mm", "==", PROJECTION["record_front"])
    gate("HEAT", g, "plain_cap_tip_from_wall_measured_mm", "==", PROJECTION["plain_cap_tip"])
    gate("HEAT", g, "lit_cap_tip_from_wall_measured_mm", "==", PROJECTION["lit_cap_tip"])
    gate("HEAT", g, "plain_furthest_point_of_anything_from_wall_measured_mm", "==", PROJECTION["plain_cap_tip"])
    gate("HEAT", g, "lit_furthest_point_of_anything_from_wall_measured_mm", "==", PROJECTION["lit_cap_tip"])
    # 7 in sconce is deliberately NOT on layout D and must not change by accident
    gate("HEAT-7", g, "backplate_7in_still_has_its_rim_rabbet(1 = yes: variant deliberately unchanged)", "==", 1)
    gate("HEAT-7", g, "backplate_7in_volume_minus_rev_B_volume_mm3(0 = geometry unchanged)", "abs<=", 0.1)
    # thermal model was re-run on the final geometry (thermal-results.json is written by thermal.py)
    th = checks.get("thermal", {})
    res.append(("HEAT", "thermal: THERMAL.md_quotes_these_four_final_temperatures(1 = yes)",
                th.get("THERMAL.md_quotes_these_four_final_temperatures(1 = yes)"), "== 1",
                th.get("THERMAL.md_quotes_these_four_final_temperatures(1 = yes)") == 1))
    for key, lim in (("final_geometry_matches_cad(1 = yes)", None), ("final_normal_record_C_in_30C_room", 40.0),
                     ("final_worst_case_record_C_in_35C_room", 50.0)):
        v = th.get(key)
        if lim is None:
            res.append(("HEAT", "thermal: " + key, v, "== 1", v == 1))
        else:
            res.append(("HEAT", "thermal: " + key + " (vinyl softens 55 to 60 C; gate keeps 5 K below 55)", v, f"<= {lim}", v is not None and v <= lim))
    return res
