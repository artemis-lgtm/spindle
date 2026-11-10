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


def main():
    t0 = time.time()
    log = []

    # ------------------------------------------------------------ custom parts
    custom = {
        "RS-BP-12-MDF": (S.backplate(), "mdf", (35, -60), ["step", "stl"]),
        "RS-BP-7-MDF": (S.backplate(S.BP7_D, pads_out=False), "mdf", (35, -60), ["step", "stl"]),
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
    # DXF previews (what the laser vendor will see)
    try:
        from ezdxf.addons.drawing import RenderContext, Frontend
        from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
        from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy
        import ezdxf
        import matplotlib.pyplot as plt
        for f in ("RS-WP-01_flat", "RS-BP-12-AL5", "RS-BP-12-MDF"):
            doc = ezdxf.readfile(os.path.join(PARTS, f + ".dxf"))
            fig = plt.figure(figsize=(8, 8)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
            cfg = Configuration(background_policy=BackgroundPolicy.WHITE)
            Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(doc.modelspace(), finalize=True)
            fig.savefig(os.path.join(PREV, f + "_dxf.png"), dpi=120, facecolor="white"); plt.close(fig)
    except Exception as ex:  # noqa
        print("dxf preview skipped:", ex)

    # ------------------------------------------------------------ assemblies + checks
    checks = {"interference": {}, "clearances": A.clearance_numbers()}
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
    with open(os.path.join(HERE, "checks.json"), "w") as f:
        json.dump(checks, f, indent=1)
    write_checks_md(checks)

    # ------------------------------------------------------------ drawings
    D.draw_hub(os.path.join(DRW, "RS-HUB-01"))
    D.draw_wall_plate(os.path.join(DRW, "RS-WP-01"))
    D.draw_cap(os.path.join(DRW, "RS-CAP-12"), "12")
    D.draw_cap(os.path.join(DRW, "RS-CAP-7"), "7")
    D.draw_backplate(os.path.join(DRW, "RS-BP-12-MDF"))
    D.draw_backplate(os.path.join(DRW, "RS-BP-7-MDF"), S.BP7_D, "RS-BP-7-MDF")
    D.draw_backplate_al(os.path.join(DRW, "RS-BP-12-AL5"))
    D.draw_backplate_al(os.path.join(DRW, "RS-BP-12-AL3"), t=3.0, part_no="RS-BP-12-AL3")
    D.draw_backplate_al(os.path.join(DRW, "RS-BP-7-AL5"), d=S.BP7_D, part_no="RS-BP-7-AL5")
    D.draw_assembly(os.path.join(DRW, "RS-ASM-12-MDF"))
    D.draw_assembly(os.path.join(DRW, "RS-ASM-7-MDF"), "7")
    D.draw_assembly(os.path.join(DRW, "RS-ASM-12-AL5"), "12", "al5")

    # ------------------------------------------------------------ RFQ packets
    build_rfq()
    with open(os.path.join(HERE, "build-log.json"), "w") as f:
        json.dump(dict(parts=log, seconds=round(time.time() - t0, 1)), f, indent=1)
    print(f"done in {time.time() - t0:.0f}s")


def write_checks_md(checks):
    lines = ["# Interference and clearance checks", "",
             "Generated by `build_all.py` from the same parameters that produce the STEP files. Interference = pairwise boolean",
             "intersection of every solid in the placed assembly (CadQuery/OCCT), anything over 0.5 mm3 is a hit.", ""]
    lines.append("## Interference (0 hits = nothing overlaps)")
    for k, v in checks["interference"].items():
        lines.append(f"- {k}: {v['parts']} solids, hits: {v['hits'] if v['hits'] else 'none'}")
    lines += ["", "## Clearances derived from the parameters (mm, positive = clearance / engagement)"]
    for k, v in checks["clearances"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Reading the numbers",
              "- Cap stud: 5/8 in (15.9) gives 9.0 mm (7 threads) of 1/4-20 engagement in the 12.7 insert with a 12 in record, 10.8 mm with a 7 in,",
              "  and the stud end stays 3.7 / 1.9 mm short of the backplate back face. Worst case (1.5 mm record, no felt) it is 0.1 mm proud,",
              "  which the hub's 14 x 4.5 centre relief absorbs.",
              "- Wall screw heads (#8 pan, 2.8 high) clear the hub recess ceiling by 0.8 mm. Use pan or truss heads, not round heads.",
              "- Bayonet: 8-32 lock nut underside 0.6 above the J-web, 4.1 below the pocket ceiling; stud end 1.2 below the ceiling, 2.9 past the nut.",
              "  The nut height is set at assembly with a 7.2 mm gauge block between plate and nut (NUT_GAP).",
              "- DC plug (10 dia) clears the plate slot by 2.0 at the end and the 1-1/4 in wall hole (centred 6 mm above plate centre) by 1.9.",
              "- M3 x 12 set screw tip passes 1.2 mm through the plate tab and stops 0.7 mm short of the plate edge radially.",
              "- Record overhangs the backplate 19.05 mm (12 in) / 12.7 mm (7 in): the LED strip is hidden from a viewer in front."]
    with open(os.path.join(HERE, "checks.md"), "w") as f:
        f.write("\n".join(lines) + "\n")


RFQ_SPECS = {
    "backplate-mdf-cnc": dict(
        files=["RS-BP-12-MDF.step", "RS-BP-12-MDF.dxf", "RS-BP-12-MDF.stl", "RS-BP-7-MDF.step", "RS-BP-7-MDF.dxf"],
        drawings=["RS-BP-12-MDF.pdf", "RS-BP-7-MDF.pdf"],
        spec="""RFQ: CNC-routed backplates, 2 sizes (sample run)
Parts: RS-BP-12-MDF (D 266.7 / 10.50 in) and RS-BP-7-MDF (D 152.4 / 6.00 in), both 12.7 mm (1/2 in) thick.
Material: 1/2 in MDF (preferred for flatness and paint) OR 1/2 in Baltic birch plywood; quote both.
Quantity: 5 + 5 samples; please also quote 100 + 50.
Features (see STEP + PDF): outer profile; rim rabbet 10.2 wide x 1.5 deep centred on the rim (3D rim feature, needs a
 rabbet/slot pass or a lathe); centre bore 25/64 in through; 3x #8 90 deg countersinks on the FRONT face on R 45 at
 90/210/330 deg; 6 felt-pad spot pockets 13.3 dia x 0.5 deep (12 in part) / 3 on the 7 in part; one 6.35 wide notch at
 6 o'clock from the rabbet floor to the back face; REAR face: pocket 16 x 13 x 6.5 deep at (0, +15) and a channel
 6 wide x 4 deep from the notch to R 60 at 6 o'clock.
Tolerances: diameter +/-0.3; thickness as supplied; rabbet depth +/-0.2; bore +0.1/-0; countersinks +/-0.3 on position.
Finish: supply sanded, ready for paint (we paint matte black) OR quote painted matte black 2 coats as an option.
Deliverable: parts, bagged, no labels on the front face.
Ship to: Florida, USA. Please state lead time and tooling/setup charge separately.
Files: STEP is the master; DXF layers CUT / ETCH (rabbet floor) / POCKET (rear features) are a 2D aid.
"""),
    "backplate-aluminum-flat": dict(
        files=["RS-BP-12-AL5.step", "RS-BP-12-AL5.dxf", "RS-BP-12-AL3.step", "RS-BP-12-AL3.dxf", "RS-BP-7-AL5.step", "RS-BP-7-AL5.dxf"],
        drawings=["RS-BP-12-AL5.pdf", "RS-BP-12-AL3.pdf", "RS-BP-7-AL5.pdf"],
        spec="""RFQ: laser / waterjet flat aluminum backplates + countersinks + powder coat
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
        spec="""RFQ: FDM printed hub (PETG or ASA), sample run, with injection moulding in mind later
Part: RS-HUB-01, D 127 x 25.4 mm, one piece, ~250 cm3 solid volume (print at 40% infill, 5 perimeters, 0.2 mm layers).
Material: PETG black (ASA black acceptable; no PLA). Orientation: REAR face (the flat face with the shallow 107 mm recess)
 DOWN on the bed; the front face carries the shallow pockets and prints up. Supports only inside the J-slot nut pockets
 if your slicer insists; prefer bridging.
Quantity: 5 samples; also quote 50 and 100.
Critical features: 3 J-slots (10.8 entry, 4.8 slot) on R 33: must be clean, no elephant foot in the recess (chamfer or
 z-hop compensation); 8.0 jack hole; 4.0 pilot in the rim for an M3 heat-set insert (we install); 3x 3.2 pilots on the front.
Tolerance: +/-0.2 on holes, +/-0.3 elsewhere; recess floor flat (we glue a steel plate into it).
Finish: as printed, matte black.
Also wanted (separate line): a DFM review for injection moulding this part in ABS or PC-ABS, with draft and gate
 suggestions, and a rough tooling + per-part quote at 1,000 and 5,000 pieces.
Ship to: Florida, USA. STEP is the master; STL is 0.05 mm chord tolerance.
"""),
    "wall-plate-steel": dict(
        files=["RS-WP-01.step", "RS-WP-01_flat.dxf"],
        drawings=["RS-WP-01.pdf"],
        spec="""RFQ: laser-cut + formed 14 ga steel mounting plate with 3 PEM studs (SendCutSend / OSH Cut style order)
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
        spec="""RFQ: turned brass dome caps, polished and plated, 2 sizes x 3 finishes (sample run)
Parts: RS-CAP-12 (D 38.1 / 1.50 in, 10.0 tall, integral 1/4-20 UNC-2A x 15.9 stud)
       RS-CAP-7  (D 48.0 / 1.89 in, 8.5 tall, D 37.6 x 1.6 locating boss underneath, same stud)
Material: brass C360 (CDA 360) bar. Option: machine the stud separately (tap 1/4-20 x 10 deep in the cap and fit a 1/4-20
 x 1-1/8 in stainless stud with Loctite 243) if that is cheaper; tell us which you quoted.
Quantity: samples 4 + 4 per finish (chrome, brass, black) = 24; also quote 100 and 500 per size in chrome.
Geometry: dome is a sphere segment (RS-CAP-12: R 25.8; RS-CAP-7: R 47.6) on a short straight band; base edge R 0.8.
 No knurl. No witness lines. Underside face flat and square to the stud within 0.05; stud concentric within 0.05.
Surface: polish the dome and band to mirror (Ra 0.1 um or better) before plating; the dome is the only part the customer
 sees, so it is a Class A surface: inspect under daylight at 300 mm, zero pits, haze or polishing lines.
Finishes:  -CR bright chrome: copper strike + bright nickel + decorative chrome, ASTM B456 SC2 (or PVD chrome over bright nickel).
           -BR brass: polished brass, clear lacquer (or brushed + lacquer; quote both).
           -BK black: black chrome over bright nickel, or PVD black (TiC / DLC), or black nickel + lacquer; say which.
 Mask the thread or chase it after plating; thread must accept a 1/4-20 2B insert by hand.
Packing: individually sleeved, no part-to-part contact.
Ship to: Florida, USA. State lead time and plating minimum lot charges separately.
"""),
}


def build_rfq():
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


if __name__ == "__main__":
    main()
