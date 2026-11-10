"""DXF export (ezdxf, R2010, mm) of flat parts, taken from the CadQuery geometry itself so the DXF can never
drift from the STEP. Full circles export as CIRCLE entities, everything else as LWPOLYLINE."""
import math
import ezdxf
import cadquery as cq
import sconce_cad as S


def _edges_to_dxf(msp, edges, layer, n=96):
    for e in edges:
        gt = e.geomType()
        if gt == "CIRCLE" and e.IsClosed():
            c = e.arcCenter()
            msp.add_circle((c.x, c.y), e.radius(), dxfattribs={"layer": layer})
            continue
        pts = e.positions([i / (n - 1) for i in range(n)])
        msp.add_lwpolyline([(p.x, p.y) for p in pts], dxfattribs={"layer": layer})


def _new_doc():
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4  # mm
    for name, color in (("CUT", 7), ("BEND", 1), ("ETCH", 3), ("POCKET", 5), ("CSK", 6), ("NOTES", 2)):
        doc.layers.add(name, color=color)
    return doc


def _section_edges(solid, z):
    slab = cq.Workplane("XY").box(2000, 2000, 0.02).translate((0, 0, z)).val()
    sec = solid.val().intersect(slab)
    return cq.Workplane("XY").add(sec).faces(">Z").edges().vals()


def plate_flat_pattern(path):
    """Flat pattern of the formed wall plate: disc + unfolded tab, bend line on layer BEND."""
    g = S.wall_plate_flat_geometry()
    R = S.PLATE_D / 2
    t = 1.0
    flat = cq.Workplane("XY").circle(R).extrude(t)
    tab = S.box(S.TAB_W, g["tab_end_r"] - (R - 2.0), t, 0, (g["tab_end_r"] + R - 2.0) / 2, 0)
    tab = tab.edges("|Z").edges(">Y").fillet(1.5)
    tab = tab.rotate((0, 0, 0), (0, 0, 1), S.TAB_ANGLE - 90)
    flat = flat.union(tab)
    yc = (S.PLATE_HOLE_Y0 + S.PLATE_HOLE_Y1) / 2
    flat = flat.cut(cq.Workplane("XY").center(0, yc).slot2D(S.PLATE_HOLE_Y1 - S.PLATE_HOLE_Y0, S.PLATE_HOLE_D, 90)
                    .extrude(t + 2).translate((0, 0, -1)))
    for a in S.SLOT_ANGLES_GANG:
        flat = flat.cut(S.arc_slot(S.SLOT_R_GANG, a - S.SLOT_HALF_DEG, a + S.SLOT_HALF_DEG, S.SLOT_W, -1, t + 1))
    for a in S.SLOT_ANGLES_ROUND:
        flat = flat.cut(S.arc_slot(S.SLOT_R_ROUND, a - S.SLOT_HALF_DEG, a + S.SLOT_HALF_DEG, S.SLOT_W, -1, t + 1))
    for a in S.STUD_ANGLES:
        x, y = S.pol(S.STUD_R, a)
        flat = flat.cut(S.cyl(S.STUD_HOLE_D, t + 2, x, y, -1))
    hx, hy = S.pol(g["hole_r"], S.TAB_ANGLE)
    flat = flat.cut(S.cyl(S.TAB_HOLE_D, t + 2, hx, hy, -1))
    doc = _new_doc(); msp = doc.modelspace()
    _edges_to_dxf(msp, _section_edges(flat, 0.5), "CUT")
    # bend line across the tab at the bend-zone centre radius
    bx, by = S.pol(g["bend_line_r"], S.TAB_ANGLE)
    ux, uy = -math.sin(math.radians(S.TAB_ANGLE)), math.cos(math.radians(S.TAB_ANGLE))
    hw = S.TAB_W / 2 + 1
    msp.add_line((bx - ux * hw, by - uy * hw), (bx + ux * hw, by + uy * hw), dxfattribs={"layer": "BEND"})
    msp.add_text(f"BEND UP 90 deg, Ri {S.BEND_RI} mm, K {S.K_FACTOR}, BA {g['ba']:.2f}; tab stands toward the hub side",
                 dxfattribs={"layer": "NOTES", "height": 2.5}).set_placement((-R, -R - 8))
    msp.add_text(f"3x D{S.STUD_HOLE_D} = PEM FH-832-10 studs, press from the wall face. 14 ga (1.90) CRS. Units mm.",
                 dxfattribs={"layer": "NOTES", "height": 2.5}).set_placement((-R, -R - 13))
    doc.saveas(path)
    return flat


def flat_from_solid(solid, path, z_mid, csk_points=None, pocket_edges=None, notes=()):
    doc = _new_doc(); msp = doc.modelspace()
    _edges_to_dxf(msp, _section_edges(solid, z_mid), "CUT")
    if csk_points:
        for (x, y, d) in csk_points:
            msp.add_circle((x, y), d / 2, dxfattribs={"layer": "CSK"})
    if pocket_edges:
        for layer, edges in pocket_edges:
            _edges_to_dxf(msp, edges, layer)
    y = -solid.val().BoundingBox().ylen / 2 - 8
    for n in notes:
        msp.add_text(n, dxfattribs={"layer": "NOTES", "height": 2.5}).set_placement((-solid.val().BoundingBox().xlen / 2, y))
        y -= 5
    doc.saveas(path)


def backplate_al_dxf(path, d=S.BP12_D, t=5.0):
    bp = S.backplate_aluminum(d, t)
    csk = [(*S.pol(S.HUB_SCREW_R, a), min(S.HUB_SCREW_CSK_D, 2 * t - 0.4)) for a in S.HUB_SCREW_ANGLES]
    if t >= 4.5:
        csk.append((0.0, 0.0, S.AL_CSK_D))
    flat_from_solid(bp, path, t / 2, csk_points=csk,
                    notes=[f"5052-H32 aluminum {t:.1f} mm. Layer CUT = through profile. Layer CSK = countersink diameters:",
                           "3x #8 flat head 90 deg CSK on the FRONT face (+Z);" + (" centre 1/4-20 82 deg CSK on the BACK face." if t >= 4.5 else " centre hole plain (pan head)."),
                           "Powder coat matte black after cutting. Units mm."])


def backplate_mdf_dxf(path, d=S.BP12_D):
    """2D for the CNC router: through profile (CUT), rear features (POCKET), front felt targets (ETCH)."""
    bp = S.backplate(d, pads_out=(d > 200))
    cut_edges = _section_edges(bp, S.BP_T / 2 + 0.3)            # inside the rabbet band: outer rim is the rabbet floor
    # outer true profile at the front face level (outside the rabbet)
    front_edges = _section_edges(bp, S.BP_T - 0.2)
    rear_edges = _section_edges(bp, 1.0)
    doc = _new_doc(); msp = doc.modelspace()
    _edges_to_dxf(msp, front_edges, "CUT")
    _edges_to_dxf(msp, cut_edges, "ETCH")
    _edges_to_dxf(msp, rear_edges, "POCKET")
    R = d / 2
    for i, n in enumerate([
        f"1/2 in MDF or Baltic birch, D {d:.1f}. Layer CUT = front-face profile + through holes + 0.5 deep felt targets + #8 CSK (front).",
        f"Layer ETCH = rim rabbet floor (D {d - 2 * S.RABBET_DEPTH:.1f}) : rabbet {S.RABBET_W} wide x {S.RABBET_DEPTH} deep centred on the rim, plus the 6 o'clock lead notch.",
        f"Layer POCKET = REAR face features at depth: jack pocket {S.BP_JACK_POCKET[0]}x{S.BP_JACK_POCKET[1]} x {S.BP_JACK_POCKET[2]} deep @ (0,+{S.JACK_Y:.0f}); lead channel {S.BACK_CHAN_W} wide x {S.BACK_CHAN_D} deep, 6 o'clock to R60.",
        "Centre bore 25/64 in (9.92) through for E-Z Lok 400-4. 3D reference: the STEP file of the same name. Units mm."]):
        msp.add_text(n, dxfattribs={"layer": "NOTES", "height": 3}).set_placement((-R, -R - 10 - 6 * i))
    doc.saveas(path)
