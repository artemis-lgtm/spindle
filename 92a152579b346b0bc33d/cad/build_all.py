"""One-shot build: STEP/STL/DXF for every part, assembly STEPs, interference + clearance report,
PNG previews, 2D drawings, and the per-vendor RFQ packets. Run from cad/ with the project venv:
    .venv/bin/python build_all.py
"""
import json
import os
import shutil
import time
import cadquery as cq
from cadquery import exporters
import sconce_cad as S
import assembly as A
import preview as P
import drawings as D
import dxf_out as X
import gates as G

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "parts")
ASM = os.path.join(HERE, "assemblies")
PREV = os.path.join(HERE, "previews")
DRW = os.path.join(HERE, "drawings")
RFQ = os.path.join(HERE, "rfq")
for d in (PARTS, ASM, PREV, DRW, RFQ):
    os.makedirs(d, exist_ok=True)


def step(shape, path):
    exporters.export(shape, path, exportType="STEP")


def stl(shape, path, tol=0.05, ang=0.1):
    exporters.export(shape, path, exportType="STL", tolerance=tol, angularTolerance=ang)


PLAIN_REV, CAP7_REV, LIT_REV, HUB_REV = "D", "C", "B", "B"
# 2026-11-11 heat-safe halo (layout D): the 12 in MDF backplate goes to rev C (rim rabbet + rim notch deleted, back channel
# shortened, 4 blind pilots for the heat-ring screws). The 7 in backplate stays rev B: it is NOT on layout D (no room).
BP12_REV, BP7_REV, RING_REV = "C", "B", "A"
BP_REV = BP12_REV
SUPERSEDED_ZIPS = ("dome-cap-RS-CAP-12-revB.zip", "dome-cap-RS-CAP-12-revC.zip", "dome-cap-lit-RS-CAP-12L.zip")


def main():
    t0 = time.time()
    log = []

    # ------------------------------------------------------------ custom parts
    custom = {
        "RS-BP-12-MDF": (S.backplate(), "mdf", (35, -60), ["step", "stl"]),
        "RS-BP-7-MDF": (S.backplate(S.BP7_D, pads_out=False), "mdf", (35, -60), ["step", "stl"]),
        "RS-HR-12": (S.heat_ring(), "alu", (35, -60), ["step"]),
        "RS-CK-12": (S.cork_ring(), "cork", (35, -60), ["step"]),
        "RS-BP-12-AL5": (S.backplate_aluminum(S.BP12_D, 5.0), "alu", (35, -60), ["step"]),
        "RS-BP-12-AL3": (S.backplate_aluminum(S.BP12_D, 3.0), "alu", (35, -60), ["step"]),
        "RS-BP-7-AL5": (S.backplate_aluminum(S.BP7_D, 5.0), "alu", (35, -60), ["step"]),
        "RS-HUB-01": (S.hub(), "petg", (35, -60), ["step", "stl"]),
        "RS-WP-01": (S.wall_plate(), "steel", (35, -60), ["step"]),
        "RS-CAP-12": (S.dome_cap_12(), "chrome", (20, -60), ["step", "stl"]),
        "RS-CAP-7": (S.dome_cap_7(), "chrome", (20, -60), ["step", "stl"]),
    }
    for name, (shape, color, view, fmts) in custom.items():
        v = shape.val()
        assert v.isValid() and len(shape.solids().vals()) == 1, name
        if "step" in fmts:
            step(shape, os.path.join(PARTS, name + ".step"))
        if "stl" in fmts:
            stl(shape, os.path.join(PARTS, name + ".stl"))
        P.render([(shape, color)], os.path.join(PREV, name + ".png"), view=view, title=name)
        if name in ("RS-HUB-01", "RS-WP-01", "RS-BP-12-MDF", "RS-BP-7-MDF"):
            P.render([(shape, color)], os.path.join(PREV, name + "_rear.png"), view=(-35, -60), title=name + " (rear / wall side)")
        if name.startswith("RS-CAP"):
            P.render([(shape, color)], os.path.join(PREV, name + "_under.png"), view=(-25, -60), title=name + " (underside)")
        bb = v.BoundingBox()
        log.append(dict(part=name, volume_mm3=round(v.Volume(), 1), bbox_mm=[round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)]))
        print(f"  {name}: vol {v.Volume():.0f} mm3, bbox {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}")

    # ------------------------------------------------------------ DXF flat parts
    X.plate_flat_pattern(os.path.join(PARTS, "RS-WP-01_flat.dxf"))
    X.backplate_al_dxf(os.path.join(PARTS, "RS-BP-12-AL5.dxf"), S.BP12_D, 5.0)
    X.backplate_al_dxf(os.path.join(PARTS, "RS-BP-12-AL3.dxf"), S.BP12_D, 3.0)
    X.backplate_al_dxf(os.path.join(PARTS, "RS-BP-7-AL5.dxf"), S.BP7_D, 5.0)
    X.backplate_mdf_dxf(os.path.join(PARTS, "RS-BP-12-MDF.dxf"), S.BP12_D)
    X.backplate_mdf_dxf(os.path.join(PARTS, "RS-BP-7-MDF.dxf"), S.BP7_D)
    X.halo_ring_dxf(os.path.join(PARTS, "RS-HR-12.dxf"), "alu")
    X.halo_ring_dxf(os.path.join(PARTS, "RS-CK-12.dxf"), "cork")
    # DXF previews (what the laser vendor will see)
    try:
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
        import ezdxf
        import matplotlib.pyplot as plt
        for f in ("RS-WP-01_flat", "RS-BP-12-AL5", "RS-BP-12-MDF", "RS-HR-12", "RS-CK-12"):
            doc = ezdxf.readfile(os.path.join(PARTS, f + ".dxf"))
            fig = plt.figure(figsize=(8, 8)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
            cfg = Configuration(background_policy=BackgroundPolicy.WHITE)
            Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(doc.modelspace(), finalize=True)
            fig.savefig(os.path.join(PREV, f + "_dxf.png"), dpi=120, facecolor="white"); plt.close(fig)
    except Exception as ex:  # noqa
        print("dxf preview skipped:", ex)

    # ------------------------------------------------------------ assemblies + checks
    checks = {"interference": {}, "clearances": A.clearance_numbers(), "geometry_probes": G.geometry_probes()}
    for variant, mat in (("12", "mdf"), ("7", "mdf"), ("12", "al5"), ("12", "al3")):
        parts = A.build(variant, mat)
        hits = A.interference_report(parts)
        key = f"{variant}in_{mat}"
        checks["interference"][key] = {"parts": len(parts), "hits": [(a, b, round(v, 2)) for a, b, v in hits]}
        print(f"  assembly {key}: {len(parts)} solids, interferences: {hits}")
        asm = A.to_cq_assembly(parts, name=f"record_sconce_{key}")
        asm.save(os.path.join(ASM, f"RS-ASM-{variant}-{mat.upper()}.step"))
        items = [(p, c) for n, p, c, k in parts]
        P.render(items, os.path.join(PREV, f"RS-ASM-{variant}-{mat.upper()}.png"), view=(22, -62), title=f"assembly {key}")
        P.render([(p, c) for n, p, c, k in parts if not n.startswith("record")],
                 os.path.join(PREV, f"RS-ASM-{variant}-{mat.upper()}_rear.png"), view=(-32, -62), title=f"assembly {key}, rear, record hidden")
        if variant == "12" and mat == "mdf":
            ex = A.build(variant, mat, explode=45.0)
            P.render([(p, c) for n, p, c, k in ex], os.path.join(PREV, "RS-ASM-12-MDF_exploded.png"), view=(38, -62), title="exploded, 12 in MDF")

    # ------------------------------------------------------------ drawings
    D.SHEET_LOG.clear()
    D.draw_hub(os.path.join(DRW, "RS-HUB-01"))
    D.draw_wall_plate(os.path.join(DRW, "RS-WP-01"))
    D.draw_cap(os.path.join(DRW, "RS-CAP-12"), "12")
    D.draw_cap(os.path.join(DRW, "RS-CAP-7"), "7")
    D.draw_backplate(os.path.join(DRW, "RS-BP-12-MDF"))
    D.draw_backplate(os.path.join(DRW, "RS-BP-7-MDF"), S.BP7_D, "RS-BP-7-MDF")
    D.draw_halo_ring(os.path.join(DRW, "RS-HR-12"), "alu")
    D.draw_halo_ring(os.path.join(DRW, "RS-CK-12"), "cork")
    D.draw_backplate_al(os.path.join(DRW, "RS-BP-12-AL5"))
    D.draw_backplate_al(os.path.join(DRW, "RS-BP-12-AL3"), t=3.0, part_no="RS-BP-12-AL3")
    D.draw_backplate_al(os.path.join(DRW, "RS-BP-7-AL5"), d=S.BP7_D, part_no="RS-BP-7-AL5")
    D.draw_assembly(os.path.join(DRW, "RS-ASM-12-MDF"))
    D.draw_assembly(os.path.join(DRW, "RS-ASM-7-MDF"), "7")
    D.draw_assembly(os.path.join(DRW, "RS-ASM-12-AL5"), "12", "al5")

    # ------------------------------------------------------------ RS-CAP-12L label light (parts, lit assembly, drawings)
    build_label_light(checks, log)
    checks["drawings"] = G.sheet_numbers(D.SHEET_LOG)
    checks["thermal"] = thermal_numbers()

    # ------------------------------------------------------------ RFQ packets (after every drawing exists)
    build_rfq()
    build_label_light_rfq()
    checks["documents"] = G.document_numbers(os.path.dirname(HERE))

    # ------------------------------------------------------------ regression gates: any FAIL stops the build
    results = G.run_gates(checks)
    checks["gates"] = [dict(item=r[0], check=r[1], value=r[2], rule=r[3], ok=r[4]) for r in results]
    with open(os.path.join(HERE, "checks.json"), "w") as f:
        json.dump(checks, f, indent=1)
    write_checks_md(checks, results)
    with open(os.path.join(HERE, "build-log.json"), "w") as f:
        json.dump(dict(parts=log, seconds=round(time.time() - t0, 1)), f, indent=1)
    failed = [r for r in results if not r[4]]
    print(f"gates: {len(results) - len(failed)} pass, {len(failed)} FAIL")
    for r in failed:
        print("  FAIL", r)
    if failed:
        raise SystemExit(f"{len(failed)} regression gate(s) failed, see checks.md")
    print(f"done in {time.time() - t0:.0f}s")


def thermal_numbers():
    """Re-run thermal.py (about 3 s) so the numbers always belong to the geometry being built, then pull out the final
    layout and check that THERMAL.md quotes exactly these numbers."""
    import subprocess
    import sys
    r = subprocess.run([sys.executable, os.path.join(HERE, "thermal.py")], cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("thermal.py failed:\n" + r.stderr)
    t = json.load(open(os.path.join(HERE, "thermal-results.json")))
    geo, name = t["final_geometry"], t["final_name"]
    want = dict(ring_r_mm=[S.HALO_RING_ID / 2, S.HALO_RING_OD / 2], strip_r_mm=[S.HALO_STRIP_R - S.LED_W / 2, S.HALO_STRIP_R + S.LED_W / 2],
                cork_mm=S.CORK_RING_T, alu_mm=S.HEAT_RING_T)
    n, w = t["normal"][name], t["worst"][name]
    old_n, old_w = [t[c][k] for c in ("normal", "worst") for k in t[c] if k.startswith("A ")]
    out = {
        "final_geometry_matches_cad(1 = yes)": int(all(geo[k] == v for k, v in want.items())),
        "final_geometry": f"ring r {geo['ring_r_mm'][0]:.0f} to {geo['ring_r_mm'][1]:.0f}, strip r {geo['strip_r_mm'][0]:.0f} to {geo['strip_r_mm'][1]:.0f}, cork {geo['cork_mm']}, aluminium {geo['alu_mm']}",
        "final_normal_record_rise_K": round(n["record_max"], 1),
        "final_normal_record_C_in_30C_room": round(n["record_C"], 1),
        "final_normal_hottest_spot_radius_mm": round(n["record_max_r_mm"], 1),
        "final_normal_strip_C_in_30C_room": round(n["strip_C"], 1),
        "final_normal_record_under_the_cap_rise_K": round(n["record_under_cap_max"], 2),
        "final_worst_case_record_rise_K": round(w["record_max"], 1),
        "final_worst_case_record_C_in_35C_room": round(w["record_C"], 1),
        "final_worst_case_strip_C_in_35C_room": round(w["strip_C"], 1),
        "old_rim_strip_normal_record_C_in_30C_room": round(old_n["record_C"], 1),
        "old_rim_strip_worst_case_record_C_in_35C_room": round(old_w["record_C"], 1),
    }
    md = open(os.path.join(HERE, "THERMAL.md"), encoding="utf-8").read()
    quoted = all(f"{out[k]:.1f} C" in md for k in ("final_normal_record_C_in_30C_room", "final_worst_case_record_C_in_35C_room",
                                                   "final_normal_strip_C_in_30C_room", "final_worst_case_strip_C_in_35C_room"))
    out["THERMAL.md_quotes_these_four_final_temperatures(1 = yes)"] = int(quoted)
    return out


def write_checks_md(checks, results):
    import sconce_lit as LL
    c, ll = checks["clearances"], checks["label_light"]["clearances"]
    lines = ["# Interference and clearance checks", "",
             "Generated by `build_all.py` from the same parameters that produce the STEP files. Interference = pairwise boolean",
             "intersection of every solid in the placed assembly (CadQuery/OCCT), anything over 0.5 mm3 is a hit.",
             f"Revisions built: RS-CAP-12 rev {PLAIN_REV}, RS-CAP-7 rev {CAP7_REV}, RS-CAP-12L (all lit parts) rev {LIT_REV}, RS-BP-12-MDF rev {BP12_REV}, "
             f"RS-BP-7-MDF rev {BP7_REV}, RS-HR-12 rev {RING_REV}, RS-CK-12 rev {RING_REV}, RS-HUB-01 rev {HUB_REV}.", ""]
    nfail = sum(1 for r in results if not r[4])
    lines += [f"## Regression gates: {len(results) - nfail} pass, {nfail} FAIL",
              "Each gate is a dimension or fact fixed by the Fable 5.2 review (cad/REVIEW-fable52.md) or, tagged HEAT, by the heat-safe halo layout",
              "(cad/FIXES-heat-layout.md). `build_all.py` exits non-zero if any fails.", "",
              "| Review item | Check | Value | Rule | Result |", "|---|---|---|---|---|"]
    for item, name, val, rule, ok in results:
        lines.append(f"| {item} | {name} | {val} | {rule} | {'pass' if ok else '**FAIL**'} |")
    lines += ["", "## Interference (0 hits = nothing overlaps)"]
    for k, v in checks["interference"].items():
        lines.append(f"- {k}: {v['parts']} solids, hits: {v['hits'] if v['hits'] else 'none'}")
    lines += ["", "## Clearances derived from the parameters (mm, positive = clearance / engagement)"]
    for k, v in c.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Geometry probes (measured on the built solids, not on the parameters)"]
    for k, v in checks["geometry_probes"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Reading the numbers (every figure below is printed from the parameters)",
              f"- Record seat: the record lies {c['record_back_face_above_backplate_front_face_mm']} mm off the backplate on 6 felt pads (seated in their {S.PAD_TARGET_DEPTH} targets) and on the centre backing ring,",
              f"  which is the same {S.CENTER_RING[0]} x {S.CENTER_RING[1]} felt blank as the cap felt and sits directly behind it. Loaded ring top minus pad top = "
              f"{c['centre_ring_loaded_top_minus_pad_top_mm(record dish at the clamp, must be 0)']} mm, so the clamp does not dish the record.",
              f"- Cap studs: RS-CAP-12 rev {PLAIN_REV} is {S.CAP12_STUD_L} long and gives {c['cap_12in_thread_engagement_mm']} mm of engagement in the {S.INSERT_L} insert "
              f"({c['cap_12in_threaded_engagement_past_dog_point_mm']} threaded past the dog point); RS-CAP-7 rev {CAP7_REV} is {S.CAP7_STUD_L} long, {c['cap_7in_thread_engagement_mm']} mm.",
              f"  Stud ends stay {c['cap_12in_stud_end_above_backplate_back_face_mm']} / {c['cap_7in_stud_end_above_backplate_back_face_mm']} mm inside the backplate; worst case (1.2 mm record, felt crushed flat, seat 0.3 low) "
              f"{c['cap_12in_worst_case_stud_end_above_back_face_1.2mm_record_felt_flat_mm']} mm inside. Never proud.",
              f"- A clear PET washer ({S.PET_WASHER[0]} x {S.PET_WASHER[1]} x {S.PET_WASHER[2]}) lies between every cap and the label. The record centres on a smooth D {S.CAP_SHOULDER_D} shoulder "
              f"({c['record_hole_min_minus_cap_shoulder_mm']} mm slop in the tightest hole), not on thread crests.",
              "- Wall screw heads (#8 pan, 2.8 high) clear the hub recess ceiling by 0.8 mm. Use pan or truss heads, not round heads, and flangeless anchors.",
              f"- Bayonet: locks CLOCKWISE seen from the room. 8-32 lock nut underside {c['jweb_top_to_nut_underside_mm']} above the J-web, {c['nut_top_to_pocket_ceiling_mm']} below the pocket ceiling.",
              f"  The nut height is set at assembly with a {S.NUT_GAP:.1f} mm gauge block between plate and nut (NUT_GAP).",
              f"- Power: {S.PIGTAIL_L:.0f} mm pigtail with an inline jack. On the surface route everything stays {c['pigtail_everything_stays_in_front_of_the_wall_plane_mm(min z of cord + jack + plug)']} mm or more in front of the wall "
              f"and the mated plug ends {c['mated_plug_end_inside_backplate_radius_mm(hidden behind the backplate)']} mm inside the backplate edge. In-wall: the jack passes a 1 in hole on the plate centre with {c['inline_jack_through_1in_centred_wall_hole_mm(in-wall route)']} to spare.",
              "- M3 x 12 set screw tip passes 1.2 mm through the plate tab and stops 0.7 mm short of the plate edge radially.",
              f"- Record overhangs the backplate {c['record12_overhang_past_backplate_mm']} mm (12 in) / {c['record7_overhang_past_backplate_mm']} mm (7 in).",
              f"- HEAT-SAFE HALO, 12 in sconce, plain cap and lit cap alike: the LED strip is on the BACK face of the backplate, LEDs toward the wall, on a {S.HEAT_RING_T} aluminium ring (RS-HR-12) over a {S.CORK_RING_T} cork ring (RS-CK-12). "
              f"Rings R {S.HALO_RING_ID / 2:.0f} to R {S.HALO_RING_OD / 2:.0f}, strip R {c['halo_strip_inner_edge_radius_mm']:.0f} to R {c['halo_strip_outer_edge_radius_mm']:.0f}. The strip is {c['halo_strip_outer_edge_inside_backplate_rim_mm(no line of sight from the LEDs to the record)']} mm inside the backplate rim on the far side of the wood, "
              f"so the LEDs cannot see the record; {c['solid_material_between_strip_and_record_mm(aluminium + cork + MDF)']} mm of aluminium, cork and MDF sit between them.",
              f"  Stack {c['halo_stack_height_at_the_strip_mm(cork + aluminium + strip)']} mm deep ({c['halo_stack_height_at_a_screw_head_mm']} at a screw head) in the {S.HUB_T} mm gap; strip face {c['halo_strip_face_to_wall_mm']} mm from the wall. 4x #4 x 3/8 screws on R {S.HALO_SCREW_R}: "
              f"{c['halo_screw_engagement_in_mdf_mm']} mm into the MDF, tip {c['halo_screw_tip_behind_backplate_front_face_mm']} mm behind the front face, {c['halo_screw_to_nearest_felt_target_edge_in_plan_mm']} mm from the nearest felt target.",
              f"- 7 in sconce: NOT on this layout. Outside the hub its back face is {c['7in_back_face_band_outside_the_hub_at_the_same_rim_margin_mm']} mm wide at the same rim margin; its strip is still in the rim rabbet. Open item.",
              "- Aluminium-backplate variants (AL3 / AL5, neon flex ring): not covered by this layout and not thermally modelled."]
    th = checks["thermal"]
    lines += ["", "## Thermal model of the final halo geometry (cad/thermal.py, re-run by this build; a calculation, not a measurement)"]
    for k, v in th.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Label light RS-CAP-12L rev " + LIT_REV + " (lit cap + hub contact module, see label-light/DESIGN.md)",
              "Interference, same method (lit cap and hub module swapped into the 12 in MDF assembly; thin/thick record cases too). The spigot thread is",
              "modelled at its minor diameter and the dome bore at its tap-drill diameter, so an unthreaded feature inside the thread WOULD show as a hit:"]
    for k, v in checks["label_light"]["interference"].items():
        lines.append(f"- {k}: {v['parts']} solids, hits: {v['hits'] if v['hits'] else 'none'}")
    lines += ["", f"Clearances (mm). Thin record = {LL.REC_T_MIN} mm, thick = {LL.REC_T_MAX} mm, nominal = {S.REC12_T:.2f}; record seat {S.REC_SEAT_H}; PET washer {S.PET_WASHER[2]}; no felt under the lit cap:"]
    for k, v in ll.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "Tolerance stack on the stud tip relative to the centre contact (low = tip deeper, high = tip shallower):", "",
              "| Contributor | low side | high side |", "|---|---|---|"]
    for name, lo, hi in LL.TIP_TOLERANCES:
        lines.append(f"| {name} | {lo:.2f} | {hi:.2f} |")
    lines.append(f"| **Worst-case sum** | **{LL.TOL_LOW:.2f}** | **{LL.TOL_HIGH:.2f}** |")
    lines.append(f"| RSS (reference) | {LL.TOL_RSS:.2f} | {LL.TOL_RSS:.2f} |")
    lines += ["", "Reading the numbers:",
              f"- Centre contact: gold plunger with {LL.PLG_TRAVEL:.1f} mm of travel (no catalogue spring pin exceeds 3.0). With EVERY tolerance stacked the wrong way it still has "
              f"{ll['worst_case_thick_record_centre_contact_compression_mm(must be >= 0.5)']} mm of compression on a {LL.REC_T_MAX} mm record and the stud tip is still "
              f"{ll['worst_case_thin_record_stud_tip_above_guard_tube_mm(must be >= 0.2)']} mm above the guard tube on a {LL.REC_T_MIN} mm record.",
              f"- Guard tube: its top is {LL.GUARD_TOP} mm above the backplate back face. A stud that is too long lands on PEEK there; the plunger still has "
              f"{ll['plunger_flange_underside_above_spring_solid_height_with_stud_on_guard_mm']} mm before its spring goes solid. Nothing a customer screws in can crush the contact.",
              f"- A plain RS-CAP-12 rev {PLAIN_REV} or an RS-CAP-7 rev {CAP7_REV} in a lit sconce puts its tip where the lit cap's goes (asserted). It shorts the contact through a 20 mA limit: no light, no damage, halo unaffected.",
              f"- Short-circuit guard: worst-case plunger edge at r {ll['plunger_contact_edge_radius_worst_mm']} against brass at r {ll['brass_annulus_inner_radius_mm']}: {ll['plunger_to_brass_margin_worst_mm(short-circuit guard)']} mm margin; it lands on the gold head (r {ll['pin_head_gold_face_radius_mm']}) or PEEK.",
              f"- Lip gap {ll['louver_top_to_dome_lip_gap_mm']} against a worst-case stack of {ll['lip_gap_tolerance_stack_worst_mm']}: the dome boss always stops on the LED PCB before the lip can reach the louver or window."]
    lines += ["", "## Drawing sheets (text inside the border, tolerance block present)"]
    for k, v in checks["drawings"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Document consistency (stale claims that must not come back)"]
    for k, v in checks["documents"].items():
        lines.append(f"- {k}: {v}")
    with open(os.path.join(HERE, "checks.md"), "w") as f:
        f.write("\n".join(lines) + "\n")


def _rev_block(current, superseded):
    return (f"REVISION STATUS (2026-11-11): CURRENT = {current}.\n"
            f"SUPERSEDED, DO NOT QUOTE OR BUILD: {superseded}.\n"
            "If you hold any earlier drawing, STEP or zip of these parts, discard it. See cad/rfq/README.md.\n\n")


RFQ_SPECS = {
    "backplate-mdf-cnc": dict(
        files=["RS-BP-12-MDF.step", "RS-BP-12-MDF.dxf", "RS-BP-12-MDF.stl", "RS-BP-7-MDF.step", "RS-BP-7-MDF.dxf"],
        drawings=["RS-BP-12-MDF.pdf", "RS-BP-7-MDF.pdf"],
        spec=_rev_block(f"RS-BP-12-MDF rev {BP12_REV}, RS-BP-7-MDF rev {BP7_REV}",
                        "RS-BP-12-MDF rev B (2026-11-11 morning: rim rabbet and rim notch, LED strip on the rim) and rev A; RS-BP-7-MDF rev A. "
                        "The rev B 12 in files are kept in SUPERSEDED-do-not-quote/SUPERSEDED-backplate-RS-BP-12-MDF-revB/") +
        f"""RFQ: CNC-routed backplates, 2 sizes (sample run)
Parts: RS-BP-12-MDF rev {BP12_REV} (D 266.7 / 10.50 in) and RS-BP-7-MDF rev {BP7_REV} (D 152.4 / 6.00 in).
Material: 1/2 in MDF ONLY, thickness {S.BP_T:.2f} +/-0.15 mm MEASURED on the sheet you cut (tell us the measured value).
 Do NOT substitute 1/2 in Baltic birch: it is 12.0 mm nominal and the centre contact stack does not allow it.
Quantity: 5 + 5 samples; please also quote 100 + 50.
Features common to both (see STEP + PDF): outer profile; centre bore 25/64 in through; 3x #8 90 deg countersinks on the FRONT face on
 R {S.HUB_SCREW_R:.0f} at 90/210/330 deg; FRONT face felt-pad spot pockets D {S.PAD_D + 0.6:.1f} x {S.PAD_TARGET_DEPTH} +/-0.1 deep: SIX on the 12 in part (3 on R {S.PAD_R_OUT:.1f} and
 3 on R {S.PAD_R_IN:.2f}, at 90/210/330 deg), THREE on the 7 in part (R {S.PAD_R_IN:.2f}); FRONT face scored witness circle
 {S.CENTER_WITNESS_W} wide x {S.CENTER_WITNESS_DEPTH} deep, D {S.CENTER_RING[0] + S.CENTER_WITNESS_CLR:.1f} (12 in) / D {S.CENTER_RING7[0] + S.CENTER_WITNESS_CLR:.1f} (7 in), concentric with the bore within 0.2;
 REAR face pocket {S.BP_JACK_POCKET[0]:.0f} x {S.BP_JACK_POCKET[1]:.0f} x {S.BP_JACK_POCKET[2]} deep at (0, +{S.JACK_Y:.0f}).
12 in part, rev {BP12_REV} ONLY: NO rim rabbet and NO rim notch (plain square rim, a 2D job from both faces, no rim pass).
 REAR face: channel {S.BACK_CHAN_W:.0f} wide x {S.BACK_CHAN_D:.0f} deep at 6 o'clock from R {S.BACK_CHAN_R0:.0f} to R {S.BACK_CHAN_R1:.0f} only; 4x BLIND pilot D {S.HALO_PILOT_D} x {S.HALO_PILOT_DEPTH:.1f} +0.5/-0 deep
 on R {S.HALO_SCREW_R} at {'/'.join(str(a) for a in S.HALO_SCREW_ANGLES)} deg (must NOT break through or mark the front face: {S.BP_T - S.HALO_PILOT_DEPTH:.1f} stays).
 Back face flat within 0.3 over the band R {S.HALO_RING_ID / 2:.0f} to R {S.HALO_RING_OD / 2:.0f} (a cork ring lies on it).
7 in part, rev {BP7_REV} ONLY: rim rabbet {S.RABBET_W} wide x {S.RABBET_DEPTH} deep centred on the rim (3D rim feature, needs a rabbet/slot pass
 or a lathe); one {S.NOTCH_W} wide notch at 6 o'clock from the rabbet floor to the back face; REAR face channel {S.BACK_CHAN_W:.0f} wide x {S.BACK_CHAN_D:.0f} deep
 from the notch to R {S.BACK_CHAN_R0:.0f} at 6 o'clock.
Tolerances: diameter +/-0.3; thickness {S.BP_T:.2f} +/-0.15; rabbet depth (7 in) +/-0.2; bore +0.1/-0; countersinks and pilots +/-0.3 on
 position; front face flat within 0.3 (a record lies on it).
Finish: supply sanded, ready for paint (we paint matte black, ALL surfaces) OR quote painted matte black 2 coats.
Deliverable: parts, bagged, no labels on the front face.
Ship to: Florida, USA. Please state lead time and tooling/setup charge separately.
Files: STEP is the master; DXF layers CUT / ETCH (7 in rabbet floor only) / POCKET (rear features) are a 2D aid.
"""),
    "heat-ring-aluminum": dict(
        files=["RS-HR-12.step", "RS-HR-12.dxf"],
        drawings=["RS-HR-12.pdf"],
        spec=_rev_block(f"RS-HR-12 rev {RING_REV} (new part, 2026-11-11)", "none") +
        f"""RFQ: flat laser-cut aluminium ring (SendCutSend / OSH Cut / Xometry sheet style order)
Part: RS-HR-12 rev {RING_REV}, "heat ring". One flat ring, nothing formed.
Size: OD {S.HALO_RING_OD:.1f} mm (10.236 in), ID {S.HALO_RING_ID:.1f} mm (7.874 in), 4x D {S.HEAT_RING_HOLE_D} mm holes on a D {2 * S.HALO_SCREW_R:.0f} mm bolt circle
 (R {S.HALO_SCREW_R}) at {'/'.join(str(a) for a in S.HALO_SCREW_ANGLES)} deg.
Material: 5052-H32 aluminium sheet, {S.HEAT_RING_T:.1f} mm (0.040 in). 6061-T6 or 3003-H14 at the same thickness is acceptable, tell us.
Quantity: 10 samples; please also quote 100 and 250.
Cutting: laser (or waterjet). Layer CUT in the DXF is the whole job.
Finish: bare mill finish. NO anodise, paint or powder coat (an LED strip's adhesive tape and a cork ring's adhesive bond to it).
 Deburr both faces and both edges; no dross, no heat tint. Flat within 0.5 mm.
Tolerance: +/-0.2 on OD, ID and hole position.
What it does: it sits behind a wooden disc and carries a 4 W LED strip; it spreads the strip's heat. Mass about {S.heat_ring().val().Volume() * 2.68e-3:.0f} g.
Packing: interleaved so the faces do not scratch each other.
Ship to: Florida, USA. State lead time. DXF is mm, R2010, 1:1; STEP is the 3D master.
"""),
    "cork-ring": dict(
        files=["RS-CK-12.step", "RS-CK-12.dxf"],
        drawings=["RS-CK-12.pdf"],
        spec=_rev_block(f"RS-CK-12 rev {RING_REV} (new part, 2026-11-11)", "none") +
        f"""RFQ: die-cut or knife-cut cork ring, 1/16 in (gasket cutter style order; we may also cut these in-house from roll)
Part: RS-CK-12 rev {RING_REV}, "cork ring". One flat ring.
Size: OD {S.HALO_RING_OD:.1f} mm (10.236 in), ID {S.HALO_RING_ID:.1f} mm (7.874 in), 4x D {S.CORK_RING_HOLE_D} mm holes on a D {2 * S.HALO_SCREW_R:.0f} mm bolt circle
 (R {S.HALO_SCREW_R}) at {'/'.join(str(a) for a in S.HALO_SCREW_ANGLES)} deg.
Material: fine-grain composition cork sheet, {S.CORK_RING_T:.1f} mm (1/16 in) +/-0.2. 1.5 mm sheet is acceptable. Pressure-sensitive adhesive on ONE face is
 preferred (liner left on); plain cork with no adhesive is acceptable, tell us which you are quoting.
Quantity: 10 samples; please also quote 100 and 250.
Cutting: die, flash/knife or laser. Layer CUT in the DXF is the whole job, INCLUDING the 4 holes. Tolerance +/-0.5 mm.
 If a 260 mm ring nests badly on your sheet, quote it as up to 4 butt-jointed segments as an option.
What it does: it sits between a wooden disc and a warm aluminium ring as a heat break. It carries no load beyond 4 small screws.
Packing: flat, not rolled.
Ship to: Florida, USA. State lead time. DXF is mm, R2010, 1:1; STEP is the 3D master.
"""),
    "backplate-aluminum-flat": dict(
        files=["RS-BP-12-AL5.step", "RS-BP-12-AL5.dxf", "RS-BP-12-AL3.step", "RS-BP-12-AL3.dxf", "RS-BP-7-AL5.step", "RS-BP-7-AL5.dxf"],
        drawings=["RS-BP-12-AL5.pdf", "RS-BP-12-AL3.pdf", "RS-BP-7-AL5.pdf"],
        spec=_rev_block("RS-BP-12-AL5 / -AL3 / RS-BP-7-AL5 rev A (geometry unchanged, sheets re-issued 2026-11-11)", "none") +
        """RFQ: laser / waterjet flat aluminum backplates + countersinks + powder coat
Parts: RS-BP-12-AL5 (D 266.7, 5.0 mm), RS-BP-12-AL3 (D 266.7, 3.0 mm), RS-BP-7-AL5 (D 152.4, 5.0 mm).
Material: 5052-H32 aluminum sheet (6061-T6 acceptable). Thickness 5.0 mm (0.197 in; 3/16 in = 4.76 acceptable, tell us) or 3.0 mm.
Quantity: 5 of each for samples; please also quote 100 of the 12 in / 5 mm.
Cutting: outer D, centre hole D 6.6, 3x D 4.5 holes on R 45 at 90/210/330, one 16 x 13 rectangular cut-out at (0, +15).
Countersinks (layer CSK in the DXF): 3x 90 deg for #8 flat head on the FRONT (+Z) face, D 8.6 (5 mm) / D 5.6 (3 mm);
 5 mm parts only: centre hole countersunk 82 deg D 13.0 on the BACK face for a 1/4-20 flat head.
Finish: powder coat matte black (RAL 9005 fine texture or your closest), both faces, hang from the 16 x 13 cut-out.
Deburr: both faces, no heat tint. Flat within 0.5 after coating.
Ship to: Florida, USA. State lead time. DXF is mm, R2010; STEP is the 3D master.
"""),
    "hub-3dprint": dict(
        files=["RS-HUB-01.step", "RS-HUB-01.stl"],
        drawings=["RS-HUB-01.pdf"],
        spec=_rev_block(f"RS-HUB-01 rev {HUB_REV}", "rev A (2026-11-09): panel-jack hub, J-slots the other hand, 4.5 centre relief") +
        f"""RFQ: FDM printed hub (PETG or ASA), sample run, with injection moulding in mind later
Part: RS-HUB-01 rev {HUB_REV}, D 127 x 25.4 mm, one piece, ~250 cm3 solid volume (print at 40% infill, 5 perimeters, 0.2 mm layers).
Material: PETG black (ASA black acceptable; no PLA). Orientation: REAR face (the flat face with the shallow 107 mm recess)
 DOWN on the bed; the front face carries the shallow pockets and prints up. Supports only inside the J-slot nut pockets
 if your slicer insists; prefer bridging.
Quantity: 5 samples; also quote 50 and 100.
Critical features: 3 J-slots ({S.JENTRY_D} entry, {S.JSLOT_W} slot) on R {S.STUD_R:.0f}: must be clean, no elephant foot in the recess (chamfer or
 z-hop compensation); D {S.CABLE_HOLE_D} cable hole (there is NO panel jack in rev {HUB_REV}); D {S.CLIP_PILOT_D} x {S.CLIP_PILOT_DEPTH} pilot in the rear pocket
 ceiling for a #4 screw; front centre relief D {S.CAP_RELIEF_D:.0f} x {S.CAP_RELIEF_DEPTH} +/-0.2 deep with a FLAT floor; {S.SET_INSERT_D} pilot in the rim for an M3
 heat-set insert (we install); 3x {S.HUB_SCREW_PILOT_D} pilots on the front.
Tolerance: +/-0.2 on holes and on the centre relief depth, +/-0.3 elsewhere; recess floor flat (we glue a steel plate into it).
Finish: as printed, matte black.
Also wanted (separate line): a DFM review for injection moulding this part in ABS or PC-ABS, with draft and gate
 suggestions, and a rough tooling + per-part quote at 1,000 and 5,000 pieces.
Ship to: Florida, USA. STEP is the master; STL is 0.05 mm chord tolerance.
"""),
    "wall-plate-steel": dict(
        files=["RS-WP-01.step", "RS-WP-01_flat.dxf"],
        drawings=["RS-WP-01.pdf"],
        spec=_rev_block("RS-WP-01 rev A (geometry unchanged, sheet re-issued 2026-11-11)", "none") +
        """RFQ: laser-cut + formed 14 ga steel mounting plate with 3 PEM studs (SendCutSend / OSH Cut style order)
Part: RS-WP-01. Round plate D 101.6 (4.00 in) with one 8 mm wide tab bent up 90 deg.
Material: mild steel CRS 14 ga (0.0747 in / 1.90 mm). Alt quote: 304 stainless 14 ga.
Quantity: 10 samples; also quote 100 and 250.
Cut: centre slot 30 x 37; 4 arc slots 4.8 wide (+/-10 deg) on D 83.3 (at 90/270 deg) and D 88.9 (at 0/180 deg);
 3 holes D 4.22 on R 33 at 75/195/315 deg for PEM studs; 1 hole D 3.4 in the tab.
Bend: one 90 deg bend UP (tab stands on the same side as the stud threads), inside radius 1.9 (1t), tab height 12.0
 from the wall face. Flat pattern supplied (K 0.44, BA 4.30) but use your own K if you prefer; the formed STEP is the master.
Hardware: 3x PEM self-clinching studs FH-832-10 (8-32 x 5/8 in), pressed from the plain (wall) face so the head is flush
 on the wall side and the threads stand on the tab side. Please confirm the D 4.22 clinch hole against PEM bulletin FH
 for 0.075 in sheet and adjust if needed.
Finish: zinc plate clear (or black zinc); powder coat black acceptable if the studs are masked.
Deburr: all edges; the plate sits against drywall.
Ship to: Florida, USA. State lead time. DXF is mm.
"""),
    "dome-cap-brass": dict(
        files=["RS-CAP-12.step", "RS-CAP-12.stl", "RS-CAP-7.step", "RS-CAP-7.stl"],
        drawings=["RS-CAP-12.pdf", "RS-CAP-7.pdf"],
        spec=_rev_block(f"RS-CAP-12 rev {PLAIN_REV}, RS-CAP-7 rev {CAP7_REV}",
                        "RS-CAP-12 rev A (15.9 stud), rev B (13.3 stud), rev C (11.70 stud, no shoulder); RS-CAP-7 rev A / B (15.88 stud); "
                        "the zips dome-cap-RS-CAP-12-revB.zip and -revC.zip") +
        f"""RFQ: turned brass dome caps, polished and plated, 2 sizes x 3 finishes (sample run)
Parts: RS-CAP-12 rev {PLAIN_REV} (D 38.1 / 1.50 in, 10.0 tall, underside recess D {S.CAP12_RECESS_D} x {S.CAP12_RECESS_H:.2f} +/-{S.CAP12_RECESS_TOL} deep, smooth shoulder
       D {S.CAP_SHOULDER_D:.2f} +0/-0.05 from the recess floor to {S.CAP_SHOULDER_L} below the underside face, relief groove D {S.CAP_STUD_RELIEF_D} x {S.CAP_STUD_RELIEF_L}, integral
       1/4-20 UNC-2A stud, {S.CAP12_STUD_L:.2f} +/-0.05 from the underside face to the tip; tip = unthreaded dog point
       D {S.CAP_STUD_DOG_D:.2f} +0/-0.10 x {S.CAP_STUD_DOG_L}, 0.3 x 45 chamfer)
       RS-CAP-7 rev {CAP7_REV} (D 48.0 / 1.89 in, 8.5 tall, D {S.CAP7_BOSS_D} x {S.CAP7_BOSS_H} locating boss underneath, stud 1/4-20 x {S.CAP7_STUD_L:.2f} +/-0.05
       from the flange underside, same dog point)
Material: brass C360 (CDA 360) bar, ONE piece with the stud. There is no separate-stud option any more: the D {S.CAP_SHOULDER_D:.2f}
 shoulder cannot be tapped 1/4-20 (0.37 wall).
Quantity: samples 4 + 4 per finish (chrome, brass, black) = 24; also quote 100 and 500 per size in chrome.
Geometry: dome is a sphere segment (RS-CAP-12: R 25.8; RS-CAP-7: R 47.6) on a short straight band; base edge R 0.8.
 Recess floor flat (we bond a felt washer in it). No knurl. No witness lines. Underside face flat and square to the stud
 within 0.05; stud concentric within 0.05. R 0.2 at the relief groove root.
Surface: polish the dome and band to mirror (Ra 0.1 um or better) before plating; the dome is the only part the customer
 sees, so it is a Class A surface: inspect under daylight at 300 mm, zero pits, haze or polishing lines.
Finishes:  -CR bright chrome: copper strike + bright nickel + decorative chrome, ASTM B456 SC2 (or PVD chrome over bright nickel).
           -BR brass: polished brass, clear lacquer (or brushed + lacquer; quote both).
           -BK black: black chrome over bright nickel, or PVD black (TiC / DLC), or black nickel + lacquer; say which.
 Rack on the stud only. MASK the thread and the shoulder; do NOT chase the thread after plating (chrome flakes). Thread class
 2A is before plating; any nickel on the thread 5 um max; it must accept a 1/4-20 2B GO gauge AFTER plating.
Packing: individually sleeved, no part-to-part contact.
Ship to: Florida, USA. State lead time and plating minimum lot charges separately.

"""),
}


def build_rfq():
    import zipfile
    for folder, d in RFQ_SPECS.items():
        out = os.path.join(RFQ, folder)
        os.makedirs(out, exist_ok=True)
        for f in d["files"]:
            shutil.copy(os.path.join(PARTS, f), os.path.join(out, f))
        for f in d["drawings"]:
            shutil.copy(os.path.join(DRW, f), os.path.join(out, f))
            png = f.replace(".pdf", ".png")
            if os.path.exists(os.path.join(DRW, png)):
                shutil.copy(os.path.join(DRW, png), os.path.join(out, png))
        with open(os.path.join(out, "SPEC.txt"), "w") as f:
            f.write(d["spec"] + "\nFiles in this folder: " + ", ".join(d["files"] + d["drawings"]) +
                    "\nContact: (fill in before sending; nothing has been sent)\n")
    # machine-shop zip for the plain caps, named by revision
    out = os.path.join(RFQ, "dome-cap-brass")
    zpath = os.path.join(RFQ, f"dome-cap-RS-CAP-12-rev{PLAIN_REV}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("RS-CAP-12.step", "RS-CAP-12.pdf", "RS-CAP-12.stl", "RS-CAP-7.step", "RS-CAP-7.pdf", "RS-CAP-7.stl", "SPEC.txt"):
            z.write(os.path.join(out, f), f)
    print("  plain cap RFQ zip:", zpath)
    # superseded zips move out of the way and are renamed so nobody attaches one by mistake
    sup = os.path.join(RFQ, "SUPERSEDED-do-not-quote")
    os.makedirs(sup, exist_ok=True)
    for z in SUPERSEDED_ZIPS:
        src = os.path.join(RFQ, z)
        if os.path.exists(src):
            shutil.move(src, os.path.join(sup, "SUPERSEDED-" + z))
    with open(os.path.join(sup, "README.txt"), "w") as f:
        f.write("Everything in this folder is SUPERSEDED and kept only as a record of what was drafted.\n"
                "Do not send, quote or build from it. Current packets are one folder up; see ../README.md.\n\n"
                "SUPERSEDED-dome-cap-RS-CAP-12-revB.zip   RS-CAP-12 rev B (13.3 stud)            superseded 2026-11-10\n"
                "SUPERSEDED-dome-cap-RS-CAP-12-revC.zip   RS-CAP-12 rev C (11.70 stud)           superseded 2026-11-11\n"
                "SUPERSEDED-dome-cap-lit-RS-CAP-12L.zip   RS-CAP-12L rev A.1 (could not be assembled as drawn) superseded 2026-11-11\n"
                "SUPERSEDED-backplate-RS-BP-12-MDF-revB/  RS-BP-12-MDF rev B (rim rabbet, LED strip on the rim) and the two\n"
                "                                         assembly sheets that showed the rim strip    superseded 2026-11-11 (heat-safe layout)\n")
    with open(os.path.join(RFQ, "README.md"), "w") as f:
        f.write(f"""# RFQ packets: what is current

Generated by `build_all.py` on every build. Nothing here has been sent to anyone.

| Packet | Parts and CURRENT revision | Superseded (do not quote) |
|---|---|---|
| `dome-cap-brass/` and `dome-cap-RS-CAP-12-rev{PLAIN_REV}.zip` | RS-CAP-12 **rev {PLAIN_REV}** (stud {S.CAP12_STUD_L}, D {S.CAP_SHOULDER_D} shoulder), RS-CAP-7 **rev {CAP7_REV}** (stud {S.CAP7_STUD_L}) | RS-CAP-12 rev A, B, C; RS-CAP-7 rev A, B |
| `dome-cap-lit/` and `dome-cap-lit-RS-CAP-12L-rev{LIT_REV}.zip` | RS-CAP-12L **rev {LIT_REV}**: dome, core, pin, sleeve, louver, window, hub carrier, plunger, both PCBs | rev A, rev A.1 |
| `backplate-mdf-cnc/` | RS-BP-12-MDF **rev {BP12_REV}** (no rim rabbet, 4 blind pilots on the back), RS-BP-7-MDF **rev {BP7_REV}** | RS-BP-12-MDF rev A, B; RS-BP-7-MDF rev A |
| `heat-ring-aluminum/` | RS-HR-12 **rev {RING_REV}**: 1.0 mm aluminium ring that carries the LED strip (new 2026-11-11) | none |
| `cork-ring/` | RS-CK-12 **rev {RING_REV}**: {S.CORK_RING_T} mm (1/16 in) cork ring between the aluminium ring and the wood (new 2026-11-11) | none |
| `hub-3dprint/` | RS-HUB-01 **rev {HUB_REV}** (pigtail, no panel jack) | rev A |
| `wall-plate-steel/` | RS-WP-01 rev A | none |
| `backplate-aluminum-flat/` | RS-BP-12-AL5 / -AL3 / RS-BP-7-AL5 rev A | none |

Rules:
- Every SPEC.txt starts with a REVISION STATUS block. Every drawing title block carries REV and a SUPERSEDES line.
- Old zips live in `SUPERSEDED-do-not-quote/` with a `SUPERSEDED-` prefix. They are a record, not a packet.
- The dome-cap drafts in `../../sourcing/rfq-drafts/` predate this CAD (they describe a 1 in stud) and are marked superseded.
- What changed and why: `../FIXES-fable52.md` (review) and `../FIXES-heat-layout.md` (LED strip moved to the back face on the two rings). The gates that keep it that way: `../checks.md`.
- The heat ring and the cork ring are for the 12 in MDF sconce, plain cap and lit cap alike. The 7 in sconce and the aluminium-backplate variants do not use them.
""")


def build_label_light(checks, log):
    """RS-CAP-12L: STEP for every part, lit assembly + interference, clearances, drawings, PCB outlines."""
    import sconce_lit as LL
    import assembly_lit as AL
    import drawings_lit as DL
    sys_path = os.path.join(HERE, "label-light")
    lit_parts = lit_part_shapes()
    for name, (shape, color, fmts) in lit_parts.items():
        v = shape.val()
        assert v.isValid() and len(shape.solids().vals()) == 1, name
        if "step" in fmts:
            step(shape, os.path.join(PARTS, name + ".step"))
        if "stl" in fmts:
            stl(shape, os.path.join(PARTS, name + ".stl"))
        P.render([(shape, color)], os.path.join(PREV, name + ".png"), view=(25, -60), title=name)
        bb = v.BoundingBox()
        log.append(dict(part=name, volume_mm3=round(v.Volume(), 1), bbox_mm=[round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)]))
        print(f"  {name}: vol {v.Volume():.0f} mm3, bbox {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}")
    ll = {"interference": {}, "clearances": LL.clearance_numbers_lit()}
    for key, kw in (("12in_mdf_lit_nominal", {}), ("12in_mdf_lit_thin_record", dict(rec_t=LL.REC_T_MIN)),
                    ("12in_mdf_lit_thick_record", dict(rec_t=LL.REC_T_MAX))):
        parts = AL.build_lit(**kw)
        hits = A.interference_report(parts)
        ll["interference"][key] = {"parts": len(parts), "hits": [(a, b, round(v, 2)) for a, b, v in hits]}
        print(f"  assembly {key}: {len(parts)} solids, interferences: {hits}")
        if key == "12in_mdf_lit_nominal":
            A.to_cq_assembly(parts, name="record_sconce_12in_lit").save(os.path.join(ASM, "RS-ASM-12L-MDF.step"))
            cen = [(p, c) for n, p, c, k in parts if n.startswith(("lit_", "led", "peek", "hub_", "pogo", "ccr", "contact_", "pet_"))]
            P.render(cen, os.path.join(PREV, "RS-ASM-12L_cap_and_contacts.png"), view=(20, -60), title="RS-CAP-12L + hub contact module")
            DL.draw_assembly_lit(os.path.join(DRW, "RS-ASM-12L"), parts)
    # negative control: the rev A.1 key height must be CAUGHT (proves the M2 gate is live)
    ll["clearances"]["negative_control_revA1_key_0.9_would_fail_the_pcb_gate(1 = yes)"] = 1 if (LL.LPCB_T - LL.LPCB_T_TOL) - 0.9 <= 0 else 0
    checks["label_light"] = ll
    DL.draw_dome(os.path.join(DRW, "RS-CAP-12L-DOME"))
    DL.draw_core(os.path.join(DRW, "RS-CAP-12L-CORE"))
    DL.draw_louver(os.path.join(DRW, "RS-CAP-12L-LOUVER"))
    DL.draw_window(os.path.join(DRW, "RS-CAP-12L-WINDOW"))
    DL.draw_pin(os.path.join(DRW, "RS-CAP-12L-PIN"))
    DL.draw_carrier(os.path.join(DRW, "RS-HUB-12L-CARRIER"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("ll_pcb", os.path.join(sys_path, "pcb.py"))
    pcb = importlib.util.module_from_spec(spec); spec.loader.exec_module(pcb)
    pcb.main()


def lit_part_shapes():
    import sconce_lit as LL
    return {
        "RS-CAP-12L-DOME": (LL.dome_lit(), "chrome", ["step", "stl"]),
        "RS-CAP-12L-CORE": (LL.core_lit(), "chrome", ["step"]),
        "RS-CAP-12L-LOUVER": (LL.louver_lit(), "black", ["step", "stl"]),
        "RS-CAP-12L-WINDOW": (LL.window_lit(), "led", ["step"]),
        "RS-CAP-12L-PIN": (LL.pin_lit(), "brass", ["step"]),
        "RS-CAP-12L-SLEEVE": (LL.sleeve_lit(), "felt", ["step"]),
        "RS-HUB-12L-CARRIER": (LL.carrier(), "black", ["step", "stl"]),
        "RS-HUB-12L-PLUNGER": (LL.plunger(), "brass", ["step"]),
        "RS-PCB-12L-LED": (LL.led_pcb(), "petg", ["step"]),
        "RS-PCB-12L-HUB": (LL.hub_pcb(), "petg", ["step"]),
    }


def lit_rfq_spec():
    """RFQ text for the lit cap, printed from the parameters (rev A's was a hand-kept file that drifted)."""
    import sconce_lit as LL
    return _rev_block(f"RS-CAP-12L rev {LIT_REV}, every part in this packet",
                      "rev A and rev A.1 (2026-11-10), and the zip dome-cap-lit-RS-CAP-12L.zip. Rev A.1 could not be assembled as drawn") + f"""RFQ: LIT dome cap RS-CAP-12L ("label light") - turned brass parts, plated, plus small plastic parts (sample run)
Nothing has been sent. This packet is for quoting only. Master geometry = the STEP files; drawings carry finish and tolerances.

A. TURNED BRASS (one shop, same as RS-CAP-12 if possible)
 1. RS-CAP-12L-DOME  chrome dome shell. D 38.10, {LL.DOME_TOP - LL.DOME_Z0:.1f} tall above its lip face. Outside identical to RS-CAP-12
    (R {LL.DOME_SPH_R:.2f} sphere segment {LL.DOME_H} high on a {LL.DOME_BAND_H} band, lip edge R 0.8). Hollow: bore D {2 * LL.DOME_WALL_R:.1f} in the lip, shell {LL.DOME_SHELL_T} at the
    axis, centre boss D {LL.BOSS_D} with an INTERNAL M8x0.5 LEFT-HAND thread {LL.SPG_L + 0.6:.1f} deep (the STEP shows the D {LL.SPG_MINOR_D} tap-drill bore) and a
    D {LL.BOSS_CBORE_D} x {LL.BOSS_CBORE_H} counterbore in the boss mouth. CRITICAL: boss face {LL.BOSS_TO_LIP:.2f} +/-0.02 above the lip face.
    Material brass C360. Finish OUTSIDE incl. the lip bottom face: polish to mirror Ra <= 0.1 um, then Cu + bright Ni +
    decorative Cr per ASTM B456 SC2 (or PVD chrome over bright Ni). INSIDE: mask, no chrome; rack on the inside. Class A outside,
    inspect at 300 mm daylight, zero pits/haze/polish lines. Variants -CR / -BR / -BK as RS-CAP-12.
 2. RS-CAP-12L-CORE  brass C360: hollow 1/4-20 UNC-2A stud {LL.LC_STUD_L:.2f} +/-0.05 long (tip = unthreaded dog point D {S.CAP_STUD_DOG_D:.2f} +0/-0.10
    x {S.CAP_STUD_DOG_L}), smooth shoulder D {S.CAP_SHOULDER_D:.2f} +0/-0.05 x {S.CAP_SHOULDER_L} under the flange, STEPPED bore D {LL.LC_BORE_D} +0.02/-0 x {LL.LC_BORE_STEP:.2f} +/-0.05
    deep from the tip then D {LL.LC_WIRE_BORE_D} (square shoulder between them; concentric to the thread within 0.05), D {2 * LL.CORE_R:.1f} flange with
    an 8 deg cone on top and a FLAT underside (no recess), D {2 * LL.COL_R:.0f} column with its top {LL.COL_TOP:.2f} +/-0.02 above the underside,
    M8x0.5 LEFT-HAND male spigot {LL.SPG_L} long of which the first {LL.SPG_KEY_H} is an unthreaded D (flat at {LL.SPG_KEY_X} from the axis), then
    a D {LL.SPG_RELIEF_D} x {LL.SPG_RELIEF_L} run-out groove; one D {LL.XHOLE_D} cross-hole at 45 deg into the bore (see drawing). Do NOT stake the bore.
    Finish: electroless nickel 5 um MAX everywhere (NO chrome). Thread must accept a 1/4-20 2B GO gauge after plating.
    Optional line: we paint the cavity zones ourselves; quote with and without.
 3. RS-CAP-12L-PIN   brass C360 headed pin: head D {LL.PIN_HEAD_D} x {LL.PIN_HEAD_H}, shank D {LL.PIN_D} (1/16 in), {LL.PIN_L} overall, solder cup D 0.8 x 2.0
    in the shank end, hard gold 1.3 um (50 uin) over 2.5 um Ni. Quote 500 / 1,000 (tiny part, plating lot charge separately).
 4. RS-HUB-12L-PLUNGER  brass C360 or BeCu: nose D {LL.PLG_NOSE_D} x {LL.PLG_NOSE_L} with R 0.3 crown, flange D {LL.PLG_FLANGE_D} x {LL.PLG_FLANGE_H}, pilot D {LL.PLG_PILOT_D} x {LL.PLG_PILOT_H}.
    Same gold as the pin. Quote 500 / 1,000.
 Tolerances: drawings, otherwise ISO 2768-m. Thread 1/4-20 must accept an E-Z Lok 400-4 brass insert by hand.
 Quantity: samples 6 (chrome) + 3 (brass) + 3 (black); also 100 and 500 in chrome.

B. PLASTIC
 5. RS-CAP-12L-LOUVER  louver ring D {2 * LL.LOUV_RO:.1f} x D {2 * LL.LOUV_RI:.1f} x {LL.LOUV_TOP - LL.LOUV_FLOOR_OUT:.2f}, 5 conical fins {LL.LOUV_FIN_T} thick at {LL.LOUV_PITCH} pitch (8/8/7/6/4 deg),
    6 radial ribs {LL.LOUV_RIB_W} wide. Prototype: precision SLA, black resin, 25 um layers or finer (BMF microArch S240 class, or
    Formlabs Form 4 Black if it holds 0.25 fins over 5 mm). Matte. Inner 1.5 mm of every fin white (we can dip it; quote
    as option). Also quote a micro-moulding DFM review in black PC at 1,000 / 5,000 with tooling.
 6. RS-CAP-12L-WINDOW  clear PC ring D {2 * LL.WIN_RO:.2f} x D {2 * LL.WIN_RI:.2f} x {LL.WIN_Z1 - LL.WIN_Z0:.2f}, outer face light satin (~3 deg scatter; MT-11010 or a light
    150-200 grit glass-bead blast), UV-stabilised grade. Quote turned-from-tube and moulded.
 7. RS-CAP-12L-SLEEVE  natural PEEK, turned: OD {LL.SLEEVE_OD} x bore D {LL.SLEEVE_ID} x {LL.SLEEVE_L:.2f} long, counterbore D {LL.SLEEVE_CBORE_D} x {LL.SLEEVE_CBORE_H:.2f} in one end.
 8. RS-HUB-12L-CARRIER  PEEK insulator + guard tube: body D {LL.CAR_D} x {LL.CAR_Z1 - LL.CAR_Z0:.2f} with a D {LL.SPIG_D:.2f} x {LL.SPIG_L:.2f} spigot; the spigot is bored
    D {LL.GUARD_BORE_D} from the underside to {LL.GUARD_LIP_T} below its top and D {LL.GUARD_NOSE_HOLE_D} through; one D {LL.POGO_BORE_D} guide bore, 4 underside pockets.
    PEEK machined (preferred) or PA66-GF30; prototype SLA (Formlabs High Temp) acceptable.
 Quantity: 12 samples each; 100 and 500.

C. PCBs (separate vendor, JLCPCB / PCBWay): see PCB-SPEC.md, RS-PCB-12L-LED.dxf, RS-PCB-12L-HUB.dxf, placement.csv.

Mates with: RS-HUB-01 rev {HUB_REV} (centre relief {S.CAP_RELIEF_DEPTH} deep; rev A hubs do NOT fit) and RS-BP-12-MDF rev {BP12_REV} (rev B fits the cap equally: thickness, bore and seat are unchanged) with the E-Z Lok 400-4 insert.
Ship to: Florida, USA. State lead time, setup and plating minimum lot charges separately.
Files: RS-CAP-12L-*.step, RS-HUB-12L-*.step, RS-PCB-12L-*.step, drawings RS-CAP-12L-*.pdf, RS-HUB-12L-CARRIER.pdf,
RS-ASM-12L.pdf (stack section), PCB-SPEC.md, *.dxf, placement.csv.
Contact: (fill in before sending; nothing has been sent)
"""


def build_label_light_rfq():
    """label-light deliverables folder + RFQ packet + revision-named zip."""
    import zipfile
    ldir = os.path.join(HERE, "label-light")
    for sub in ("step", "drawings"):
        os.makedirs(os.path.join(ldir, sub), exist_ok=True)
    out = os.path.join(RFQ, "dome-cap-lit")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(ldir, "rfq-SPEC.txt"), "w") as f:
        f.write(lit_rfq_spec())
    names = list(lit_part_shapes()) + ["RS-ASM-12L"]
    for n in names:
        for ext, src_dir, dst in ((".step", PARTS, "step"), (".pdf", DRW, "drawings"), (".png", DRW, "drawings")):
            src = os.path.join(src_dir if n != "RS-ASM-12L" or ext != ".step" else ASM, n + ext if n != "RS-ASM-12L" or ext != ".step" else "RS-ASM-12L-MDF.step")
            if os.path.exists(src):
                shutil.copy(src, os.path.join(ldir, dst, os.path.basename(src)))
                if dst == "drawings" or n.startswith(("RS-CAP-12L", "RS-HUB-12L", "RS-PCB-12L")):
                    shutil.copy(src, os.path.join(out, os.path.basename(src)))
    shutil.copy(os.path.join(ldir, "rfq-SPEC.txt"), os.path.join(out, "SPEC.txt"))
    for f in ("PCB-SPEC.md", "pcb/RS-PCB-12L-LED.dxf", "pcb/RS-PCB-12L-HUB.dxf", "pcb/placement.csv", "pcb/RS-PCB-12L-LED.png", "pcb/RS-PCB-12L-HUB.png"):
        src = os.path.join(ldir, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out, os.path.basename(src)))
    zpath = os.path.join(RFQ, f"dome-cap-lit-RS-CAP-12L-rev{LIT_REV}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(out)):
            z.write(os.path.join(out, f), os.path.join("dome-cap-lit", f))
    print("  label light RFQ:", zpath)


if __name__ == "__main__":
    main()
