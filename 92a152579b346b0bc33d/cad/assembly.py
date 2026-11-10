"""Assembly placement + interference / clearance checks. World frame = wall plate frame (wall at z=0)."""
import itertools
import math
import cadquery as cq
import sconce_cad as S


def z_levels(bp_t=S.BP_T):
    z_bp0 = S.HUB_T                       # backplate back face
    z_bp1 = z_bp0 + bp_t                  # backplate front face
    z_rec0 = z_bp1 + S.PAD_T              # record back face (on the felt pads)
    return z_bp0, z_bp1, z_rec0


def build(variant="12", backplate_material="mdf", explode=0.0):
    """Return ordered list of (name, cq.Workplane, color, kind). kind in {custom, purchased, customer}.
    backplate_material: "mdf" (CNC 1/2 in, record on felt pads) or "al5"/"al3" (flat aluminum, floating record)."""
    if variant == "12":
        bp_d, rec_d, rec_t, rec_hole = S.BP12_D, S.REC12_D, S.REC12_T, S.REC_HOLE_D
        cap = S.dome_cap_12()
        washer = S.felt_washer(*S.FELT_WASHER)
        pad_radii = (S.PAD_R_OUT, S.PAD_R_IN)
        cap_name, washer_name = "dome_cap_12", "felt_washer"
        felt_t = S.FELT_WASHER[2]
    else:
        bp_d, rec_d, rec_t, rec_hole = S.BP7_D, S.REC7_D, S.REC7_T, S.REC7_HOLE_D
        cap = S.dome_cap_7()
        washer = S.felt_washer(*S.FELT_RING7)
        pad_radii = (S.PAD_R_IN,)
        cap_name, washer_name = "dome_cap_7", "felt_ring_7"
        felt_t = S.FELT_RING7[2]
    alu = backplate_material.startswith("al")
    bp_t = float(backplate_material[2:]) if alu else S.BP_T
    z_bp0 = S.HUB_T
    z_bp1 = z_bp0 + bp_t
    z_rec0 = z_bp1 + (S.STANDOFF_L if alu else S.PAD_T)
    e = explode
    parts = []
    parts.append(("wall_plate", S.wall_plate(), "steel", "custom"))
    for a in S.STUD_ANGLES:
        x, y = S.pol(S.STUD_R, a)
        parts.append((f"pem_stud_{a}", S.pem_stud().translate((x, y, 0)), "chrome", "purchased"))
        parts.append((f"lock_nut_{a}", S.lock_nut().translate((x, y, S.PLATE_T + S.NUT_GAP)), "nut", "purchased"))
    for a in S.SLOT_ANGLES_GANG:
        x, y = S.pol(S.SLOT_R_GANG, a)
        parts.append((f"wall_screw_head_{a}", S.wall_screw_head().translate((x, y, 0)), "steel", "purchased"))
    parts.append(("hub", S.hub().translate((0, 0, e)), "petg", "custom"))
    parts.append(("dc_jack", S.dc_jack().translate((0, 0, e)), "black", "purchased"))
    parts.append(("dc_plug", S.dc_plug().translate((0, 0, e)), "black", "purchased"))
    parts.append(("set_screw_m3", S.set_screw().translate((0, 0, e)), "black", "purchased"))
    zb = z_bp0 + 2 * e
    if alu:
        bp = S.backplate_aluminum(bp_d, bp_t)
        parts.append((f"backplate_{variant}_al{int(bp_t)}", bp.translate((0, 0, zb)), "alu", "custom"))
        parts.append(("flat_head_1/4-20", S.flat_head_14_20(bp_t).translate((0, 0, zb)), "steel", "purchased"))
        parts.append(("standoff_3/8x1", S.standoff().translate((0, 0, zb + bp_t)), "alu", "purchased"))
        parts.append(("neon_flex_ring", S.neon_flex_ring(bp_d).translate((0, 0, zb)), "led", "purchased"))
    else:
        bp = S.backplate(bp_d, pads_out=(variant == "12"))
        parts.append((f"backplate_{variant}_mdf", bp.translate((0, 0, zb)), "mdf", "custom"))
        parts.append(("ez_lok_insert", S.ez_lok_insert().translate((0, 0, zb)), "brass", "purchased"))
        parts.append(("led_cob_strip", S.led_strip(bp_d).translate((0, 0, zb)), "led", "purchased"))
        parts.append(("felt_pads", S.felt_pads(pad_radii).translate((0, 0, z_bp1 + 2 * e)), "felt", "purchased"))
    parts.append((f"record_{variant}", S.record(rec_d, rec_t, rec_hole).translate((0, 0, z_rec0 + 3 * e)), "vinyl", "customer"))
    parts.append((washer_name, washer.translate((0, 0, z_rec0 + rec_t + 4 * e)), "felt", "purchased"))
    parts.append((cap_name, cap.translate((0, 0, z_rec0 + rec_t + felt_t + 5 * e)), "chrome", "custom"))
    return parts


def interference_report(parts, tol_vol=0.5):
    """Pairwise boolean intersections. Returns list of (a, b, volume_mm3) above tol_vol."""
    hits = []
    shapes = [(n, p.val()) for n, p, _, _ in parts]
    for (na, sa), (nb, sb) in itertools.combinations(shapes, 2):
        ba, bb = sa.BoundingBox(), sb.BoundingBox()
        if (ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin
                or ba.zmax < bb.zmin or bb.zmax < ba.zmin):
            continue
        try:
            v = sa.intersect(sb).Volume()
        except Exception as ex:  # noqa
            v = float("nan")
        if not (v == v) or v > tol_vol:
            hits.append((na, nb, v))
    return hits


def clearance_numbers():
    """Hand-derived clearances from the parameters (all mm). Positive = clearance."""
    z_bp0, z_bp1, z_rec0 = z_levels()
    out = {}
    # cap stud engagement and protrusion
    for name, rec_t, felt_t in (("12in", S.REC12_T, S.FELT_WASHER[2]), ("7in", S.REC7_T, S.FELT_RING7[2])):
        stack = rec_t + felt_t + S.PAD_T
        engage = S.CAP_STUD_L - stack
        out[f"cap_{name}_thread_engagement_mm"] = round(min(engage, S.INSERT_L), 2)
        out[f"cap_{name}_stud_end_above_backplate_back_face_mm"] = round(S.BP_T - engage, 2)
    # thin record with no felt (worst case protrusion)
    out["cap_12in_worst_case_protrusion_no_felt_1.5mm_record_mm"] = round(S.CAP_STUD_L - (1.5 + 0 + S.PAD_T) - S.BP_T, 2)
    out["hub_cap_relief_depth_mm"] = S.CAP_RELIEF_DEPTH
    # wall screw heads under the hub recess ceiling
    out["wall_screw_head(2.8)_to_recess_ceiling_mm"] = round(S.HUB_RECESS_DEPTH - (S.PLATE_T + 2.8), 2)
    out["jack_body_end_to_backplate_pocket_floor_mm"] = round((S.HUB_T + S.BP_JACK_POCKET[2]) - (S.POCKET_DEPTH + S.JACK_WEB_T + S.JACK_BODY_L), 2)
    out["backplate_mdf_left_under_jack_pocket_mm"] = round(S.BP_T - S.BP_JACK_POCKET[2], 2)
    out["backplate_web_jack_pocket_to_insert_bore_mm"] = round((S.JACK_Y - S.BP_JACK_POCKET[1] / 2) - S.INSERT_BORE_D / 2, 2)
    # plate edge to recess wall
    out["plate_edge_to_hub_recess_wall_mm"] = round(S.HUB_RECESS_R - S.PLATE_D / 2, 2)
    # bayonet stack
    nut_bottom = S.PLATE_T + S.NUT_GAP
    out["jweb_top_to_nut_underside_mm"] = round(nut_bottom - (S.HUB_RECESS_DEPTH + S.JWEB_T), 2)
    out["nut_top_to_pocket_ceiling_mm"] = round(S.NUT_POCKET_TOP - (nut_bottom + S.NUT_H), 2)
    out["stud_end_to_pocket_ceiling_mm"] = round(S.NUT_POCKET_TOP - (S.PLATE_T + S.STUD_L), 2)
    out["stud_thread_past_nut_mm"] = round(S.PLATE_T + S.STUD_L - (nut_bottom + S.NUT_H), 2)
    out["jslot_width_minus_stud_mm"] = round(S.JSLOT_W - S.STUD_D, 2)
    out["entry_hole_minus_nut_across_corners_mm"] = round(S.JENTRY_D - S.NUT_AF / math.cos(math.radians(30)), 2)
    # record edge vs LED strip (radial) and record vs backplate rim
    out["record12_overhang_past_backplate_mm"] = round((S.REC12_D - S.BP12_D) / 2, 2)
    out["record7_overhang_past_backplate_mm"] = round((S.REC7_D - S.BP7_D) / 2, 2)
    out["led_strip_proud_of_rim_mm"] = round(S.LED_T - S.RABBET_DEPTH, 2)
    out["rabbet_width_minus_strip_mm"] = round(S.RABBET_W - S.LED_W, 2)
    # set screw reach
    tab_inner_r = S.PLATE_D / 2 + S.BEND_RI
    tab_outer_r = tab_inner_r + S.PLATE_T
    tip_r = S.HUB_D / 2 - 12.0
    out["m3x12_tip_past_tab_inner_face_mm"] = round(tab_inner_r - tip_r, 2)
    out["m3_tip_to_plate_edge_radial_mm"] = round(tip_r - S.PLATE_D / 2, 2)
    out["tab_to_tab_pocket_outer_wall_mm"] = round(S.TAB_POCKET_R1 - tab_outer_r, 2)
    out["tab_top_to_tab_pocket_ceiling_mm"] = round(S.TAB_POCKET_DEPTH - S.TAB_TOP_Z, 2)
    # plug through the plate hole and wall hole
    out["plug_body_edge_to_plate_slot_end_mm"] = round(S.PLATE_HOLE_Y1 - (S.JACK_Y + 5.0), 2)
    out["plug_body_edge_to_plate_slot_side_mm"] = round(S.PLATE_HOLE_D / 2 - 5.0, 2)
    out["plug_body_edge_to_1-1/4in_wall_hole_at_y+6_mm"] = round(1.25 * S.IN / 2 - (S.JACK_Y + 5.0 - 6.0), 2)
    out["pocket_wall_to_plug_body_mm"] = round(min(S.POCKET_W / 2 - 5.0, S.POCKET_Y1 - (S.JACK_Y + 5.0)), 2)
    # jack body vs cap-stud axis
    out["jack_body_edge_to_cap_relief_edge_mm"] = round((S.JACK_Y - 4.5) - S.CAP_RELIEF_D / 2, 2)
    # aluminum floating configuration
    head_h = (S.AL_CSK_D - S.AL_CLR_D) / 2 / math.tan(math.radians(41))
    out["al_flat_head_height_mm"] = round(head_h, 2)
    out["al3_pan_head_to_hub_relief_floor_mm"] = round(S.CAP_RELIEF_DEPTH - S.PAN_HEAD_14_20[1], 2)
    out["al3_pan_head_to_hub_relief_wall_radial_mm"] = round((S.CAP_RELIEF_D - S.PAN_HEAD_14_20[0]) / 2, 2)
    out["al_cap_stud_into_standoff_mm"] = round(S.CAP_STUD_L - S.REC12_T - S.FELT_WASHER[2], 2)
    out["al_standoff_free_thread_between_screw_and_cap_mm"] = round(S.STANDOFF_L - (15.9 - head_h - 5.0) - (S.CAP_STUD_L - S.REC12_T - S.FELT_WASHER[2]), 2)
    out["al_neon_ring_top_to_wall_mm"] = round(S.HUB_T - 12.0, 2)
    # hub screw: #8 x 1" from the backplate front face
    out["hub_screw_1in_tip_depth_into_hub_mm"] = round(S.IN - S.BP_T, 2)
    out["hub_pilot_depth_minus_screw_penetration_mm"] = round(S.HUB_SCREW_PILOT_DEPTH - (S.IN - S.BP_T), 2)
    out["hub_pilot_bottom_above_nut_pocket_ceiling_mm(radial_offset_so_no_overlap)"] = round(S.HUB_SCREW_R - (S.STUD_R + S.NUT_POCKET_W / 2), 2)
    # wall gap
    out["wall_gap_mm"] = S.HUB_T
    return out


def to_cq_assembly(parts, name="record_sconce"):
    colors = {"steel": (0.6, 0.62, 0.65), "chrome": (0.85, 0.87, 0.9), "nut": (0.7, 0.7, 0.65), "petg": (0.25, 0.27, 0.3),
              "black": (0.08, 0.08, 0.09), "mdf": (0.15, 0.15, 0.16), "alu": (0.7, 0.72, 0.74), "brass": (0.78, 0.62, 0.3),
              "led": (1.0, 0.8, 0.5), "felt": (0.55, 0.5, 0.42), "vinyl": (0.05, 0.05, 0.06)}
    asm = cq.Assembly(name=name)
    for n, p, c, _ in parts:
        asm.add(p, name=n, color=cq.Color(*colors[c]))
    return asm
