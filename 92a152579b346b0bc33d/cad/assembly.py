"""Assembly placement + interference / clearance checks. World frame = wall plate frame (wall at z=0)."""
import itertools
import math
import cadquery as cq
import sconce_cad as S


def z_levels(bp_t=S.BP_T):
    z_bp0 = S.HUB_T                       # backplate back face
    z_bp1 = z_bp0 + bp_t                  # backplate front face
    z_rec0 = z_bp1 + S.REC_SEAT_H         # record back face: on the pads seated in their 0.5 targets + the centre ring
    return z_bp0, z_bp1, z_rec0


def build(variant="12", backplate_material="mdf", explode=0.0):
    """Return ordered list of (name, cq.Workplane, color, kind). kind in {custom, purchased, customer}.
    backplate_material: "mdf" (CNC 1/2 in, record on felt pads) or "al5"/"al3" (flat aluminum, floating record)."""
    if variant == "12":
        bp_d, rec_d, rec_t, rec_hole = S.BP12_D, S.REC12_D, S.REC12_T, S.REC_HOLE_D
        cap = S.dome_cap_12()
        felt_t = S.FELT12_PROUD / 2                     # nominal = tightened: felt compressed to half its 0.6 proud
        washer = S.ring(S.FELT_WASHER[0] / 2, S.FELT_WASHER[1] / 2, S.CAP12_RECESS_H + felt_t)
        pad_radii = (S.PAD_R_OUT, S.PAD_R_IN)
        cap_name, washer_name = "dome_cap_12", "felt_washer"
        pet, ring_spec = S.PET_WASHER, S.CENTER_RING
    else:
        bp_d, rec_d, rec_t, rec_hole = S.BP7_D, S.REC7_D, S.REC7_T, S.REC7_HOLE_D
        cap = S.dome_cap_7()
        felt_t = S.FELT_LOADED_T
        washer = S.ring(S.FELT_RING7[0] / 2, S.FELT_RING7[1] / 2, felt_t)
        pad_radii = (S.PAD_R_IN,)
        cap_name, washer_name = "dome_cap_7", "felt_ring_7"
        pet, ring_spec = S.PET_WASHER7, S.CENTER_RING7
    alu = backplate_material.startswith("al")
    bp_t = float(backplate_material[2:]) if alu else S.BP_T
    z_bp0 = S.HUB_T
    z_bp1 = z_bp0 + bp_t
    z_rec0 = z_bp1 + (S.STANDOFF_L if alu else S.REC_SEAT_H)
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
    parts.append(("pigtail_cord", S.pigtail_cord().translate((0, 0, e)), "black", "purchased"))
    parts.append(("cord_p_clip", S.cord_clip().translate((0, 0, e)), "plastic", "purchased"))
    parts.append(("inline_jack", S.inline_jack().translate((0, 0, e)), "black", "purchased"))
    parts.append(("adapter_plug", S.inline_plug().translate((0, 0, e)), "black", "purchased"))
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
        if S.halo_layout(bp_d) == "back":
            # heat-safe halo, layout D: cork, aluminium, strip, stacked on the BACK face toward the wall. Shared by the
            # plain-cap and the lit-cap sconce (assembly_lit.py builds on this list).
            parts.append(("cork_ring", S.cork_ring_placed().translate((0, 0, zb - 0.28 * e)), "cork", "custom"))
            parts.append(("heat_ring_alu", S.heat_ring_placed().translate((0, 0, zb - 0.56 * e)), "alu", "custom"))
            parts.append(("led_cob_strip", S.led_strip_back().translate((0, 0, zb - 0.84 * e)), "led", "purchased"))
            for a in S.HALO_SCREW_ANGLES:
                parts.append((f"heat_ring_screw_{a}", S.halo_screw(a).translate((0, 0, zb - 1.1 * e)), "steel", "purchased"))
        else:
            parts.append(("led_cob_strip", S.led_strip_rim(bp_d).translate((0, 0, zb)), "led", "purchased"))
        parts.append(("felt_pads", S.felt_pads(pad_radii).translate((0, 0, z_bp1 + 2 * e)), "felt", "purchased"))
        parts.append(("centre_backing_ring", S.center_ring(ring_spec).translate((0, 0, z_bp1 + 2 * e)), "felt", "purchased"))
    parts.append((f"record_{variant}", S.record(rec_d, rec_t, rec_hole).translate((0, 0, z_rec0 + 3 * e)), "vinyl", "customer"))
    z_pet = z_rec0 + rec_t
    parts.append(("pet_label_washer", S.pet_washer(pet).translate((0, 0, z_pet + 3.5 * e)), "led", "purchased"))
    parts.append((washer_name, washer.translate((0, 0, z_pet + pet[2] + 4 * e)), "felt", "purchased"))
    parts.append((cap_name, cap.translate((0, 0, z_pet + pet[2] + felt_t + 5 * e)), "chrome", "custom"))
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
    for name, which, pet in (("12in", "12", S.PET_WASHER), ("7in", "7", S.PET_WASHER7)):
        engage = -(S.REC_SEAT_H + S.cap_tip_above_seat(which))          # stud below the backplate front face
        out[f"cap_{name}_thread_engagement_mm"] = round(min(engage, S.INSERT_L), 2)
        out[f"cap_{name}_threaded_engagement_past_dog_point_mm"] = round(min(engage, S.INSERT_L) - S.CAP_STUD_DOG_L, 2)
        out[f"cap_{name}_stud_end_above_backplate_back_face_mm"] = round(S.BP_T - engage, 2)
    out["cap_7in_tip_minus_cap_12in_tip_mm(asserted <= 0.05)"] = round(S.cap_tip_above_seat("7") - S.cap_tip_above_seat("12"), 3)
    # thinnest record, cap felt crushed flat, seat 0.3 low: the stud must still end inside the insert
    out["cap_12in_worst_case_stud_end_above_back_face_1.2mm_record_felt_flat_mm"] = round(
        S.BP_T + (S.REC_SEAT_H - 0.3) + 1.2 + S.PET_WASHER[2] - S.CAP12_STUD_L, 2)
    out["cap_12in_band_to_pet_washer_gap_compressed_mm"] = round(S.FELT12_PROUD / 2, 2)
    out["cap_12in_metal_above_recess_floor_at_axis_mm"] = round(S.CAP12_RIM_H + S.CAP12_DOME_H - S.CAP12_RECESS_H, 2)
    # record seat / flatness (review M1, M11b)
    out["record_back_face_above_backplate_front_face_mm"] = round(S.REC_SEAT_H, 2)
    out["centre_ring_loaded_top_minus_pad_top_mm(record dish at the clamp, must be 0)"] = round(
        (S.CENTER_RING_LOADED_T - S.CENTER_POCKET_DEPTH) - S.REC_SEAT_H, 3)
    out["centre_ring_od_minus_cap_felt_od_mm(clamp is felt-record-felt in line)"] = round(S.CENTER_RING[0] - S.FELT_WASHER[0], 2)
    out["outer_pad_target_edge_to_backplate_rim_mm(12 in rev C has no rim rabbet)"] = round(S.BP12_D / 2 - (S.PAD_R_OUT + (S.PAD_D + 0.6) / 2), 2)
    out["pet_washer_od_minus_cap12_band_od_mm(washer hidden under the cap)"] = round(S.PET_WASHER[0] - S.CAP12_D, 2)
    out["pet_washer_id_minus_shoulder_mm"] = round(S.PET_WASHER[1] - S.CAP_SHOULDER_D, 2)
    # smooth shoulder under the cap (review S1)
    out["record_hole_min_minus_cap_shoulder_mm"] = round(S.REC_HOLE_MIN - S.CAP_SHOULDER_D, 2)
    out["cap_shoulder_bottom_above_insert_top_worst_mm(1.2 record, felt flat, seat -0.3)"] = round(
        (S.REC_SEAT_H - 0.3) + 1.2 + (S.PET_WASHER[2] - 0.03) - S.CAP_SHOULDER_L, 2)
    # drawing tolerances that used to fall under the +/-0.3 block (review M9)
    out["dog_point_max_dia_mm"] = round(S.CAP_STUD_DOG_D + S.CAP_DOG_TOL[0], 2)
    out["insert_minor_min_minus_dog_point_max_mm"] = round(S.INSERT_MINOR_MIN - (S.CAP_STUD_DOG_D + S.CAP_DOG_TOL[0]), 2)
    out["cap_shoulder_wall_if_tapped_1/4-20_mm(why the separate-stud option is deleted)"] = round((S.CAP_SHOULDER_D - S.STUD_14_20_D) / 2, 3)
    out["hub_cap_relief_depth_mm"] = S.CAP_RELIEF_DEPTH
    out["hub_web_relief_floor_to_rear_pocket_ceiling_mm"] = round(S.HUB_T - S.CAP_RELIEF_DEPTH - S.POCKET_DEPTH, 2)
    # wall screw heads under the hub recess ceiling
    out["wall_screw_head(2.8)_to_recess_ceiling_mm"] = round(S.HUB_RECESS_DEPTH - (S.PLATE_T + 2.8), 2)
    out["hub_splice_cavity_depth_mm"] = round(S.HUB_T - (S.POCKET_DEPTH + S.JACK_WEB_T), 2)
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
    out["7in_only_rim_strip_proud_of_rim_mm"] = round(S.LED_T - S.RABBET_DEPTH, 2)
    out["7in_only_rabbet_width_minus_strip_mm"] = round(S.RABBET_W - S.LED_W, 2)
    out.update(halo_numbers())
    # set screw reach
    tab_inner_r = S.PLATE_D / 2 + S.BEND_RI
    tab_outer_r = tab_inner_r + S.PLATE_T
    tip_r = S.HUB_D / 2 - 12.0
    out["m3x12_tip_past_tab_inner_face_mm"] = round(tab_inner_r - tip_r, 2)
    out["m3_tip_to_plate_edge_radial_mm"] = round(tip_r - S.PLATE_D / 2, 2)
    out["tab_to_tab_pocket_outer_wall_mm"] = round(S.TAB_POCKET_R1 - tab_outer_r, 2)
    out["tab_top_to_tab_pocket_ceiling_mm"] = round(S.TAB_POCKET_DEPTH - S.TAB_TOP_Z, 2)
    # power pigtail (review M10): nothing has to enter the wall for the surface route
    R = S.HUB_D / 2
    out["pigtail_everything_stays_in_front_of_the_wall_plane_mm(min z of cord + jack + plug)"] = round(
        min(S.CORD_Z0, S.CORD_Z0 + S.PIGTAIL_CORD[1] / 2 - S.INLINE_JACK[0] / 2), 2)
    out["inline_jack_to_backplate_back_face_mm(wall gap minus jack)"] = round(
        S.HUB_T - (S.CORD_Z0 + S.PIGTAIL_CORD[1] / 2 + S.INLINE_JACK[0] / 2), 2)
    out["mated_plug_end_inside_backplate_radius_mm(hidden behind the backplate)"] = round(
        S.BP12_D / 2 - (R + S.PIGTAIL_EXIT + S.INLINE_JACK[1] + S.INLINE_PLUG[1]), 2)
    out["cord_channel_width_minus_cord_mm"] = round(S.CORD_CHAN_W - S.PIGTAIL_CORD[0], 2)
    out["cord_underside_above_wall_screw_head_mm"] = round(S.CORD_Z0 - (S.PLATE_T + 2.5), 2)
    out["cord_top_below_channel_ceiling_mm"] = round(S.CORD_CHAN_D - (S.CORD_Z0 + S.PIGTAIL_CORD[1]), 2)
    out["inline_jack_through_plate_slot_mm(in-wall route)"] = round(S.PLATE_HOLE_D - S.INLINE_JACK[0], 2)
    out["inline_jack_through_1in_centred_wall_hole_mm(in-wall route)"] = round(S.IN - S.INLINE_JACK[0], 2)
    out["1in_centred_wall_hole_inside_plate_slot_mm"] = round(min(S.PLATE_HOLE_D / 2, S.PLATE_HOLE_Y1, -S.PLATE_HOLE_Y0) - S.IN / 2, 2)
    out["pigtail_free_length_minus_surface_path_mm(slack tucks behind the backplate)"] = round(
        S.PIGTAIL_L - ((S.CLIP_POS[1] + 10.6) + (S.POCKET_DEPTH - S.CORD_Z0) + (R + S.PIGTAIL_EXIT - 10.6)), 1)
    out["clip_pilot_to_centre_relief_wall_mm"] = round(
        math.hypot(*S.CLIP_POS) - S.CAP_RELIEF_D / 2 - S.CLIP_PILOT_D / 2, 2)
    out["clip_pilot_end_below_hub_front_face_mm"] = round(S.HUB_T - (S.POCKET_DEPTH + S.CLIP_PILOT_DEPTH), 2)
    # bayonet direction (review M11d): +1 would be anticlockwise-to-lock
    out["bayonet_locks_clockwise_seen_from_the_room(1 = yes)"] = 1 if S.LOCK_ENTRY_SIGN < 0 else 0
    # rear pocket no longer cuts the J-web under the 75 deg stud
    sx, sy = S.pol(S.STUD_R, S.STUD_ANGLES[0])
    out["rear_pocket_to_75deg_nut_pocket_web_mm"] = round(
        math.hypot(sx, sy - (S.POCKET_Y1 - S.POCKET_W / 2)) - S.POCKET_W / 2 - S.NUT_POCKET_W / 2, 2)
    # splice cavity vs cap-stud axis
    out["splice_cavity_edge_to_cap_relief_edge_mm"] = round((S.JACK_CAVITY_Y_CENTER - S.JACK_CAVITY[1] / 2) - S.CAP_RELIEF_D / 2, 2)
    # aluminum floating configuration
    head_h = (S.AL_CSK_D - S.AL_CLR_D) / 2 / math.tan(math.radians(41))
    out["al_flat_head_height_mm"] = round(head_h, 2)
    out["al3_pan_head_to_hub_relief_floor_mm"] = round(S.CAP_RELIEF_DEPTH - S.PAN_HEAD_14_20[1], 2)
    out["al3_pan_head_to_hub_relief_wall_radial_mm"] = round((S.CAP_RELIEF_D - S.PAN_HEAD_14_20[0]) / 2, 2)
    al_engage = -S.cap_tip_above_seat("12")
    out["al_cap_stud_into_standoff_mm"] = round(al_engage, 2)
    out["al_standoff_free_thread_between_screw_and_cap_mm"] = round(S.STANDOFF_L - (S.AL_SCREW_L - head_h - 5.0) - al_engage, 2)
    out["al_neon_ring_top_to_wall_mm"] = round(S.HUB_T - 12.0, 2)
    # hub screw: #8 x 1" from the backplate front face
    out["hub_screw_1in_tip_depth_into_hub_mm"] = round(S.IN - S.BP_T, 2)
    out["hub_pilot_depth_minus_screw_penetration_mm"] = round(S.HUB_SCREW_PILOT_DEPTH - (S.IN - S.BP_T), 2)
    out["hub_pilot_bottom_above_nut_pocket_ceiling_mm(radial_offset_so_no_overlap)"] = round(S.HUB_SCREW_R - (S.STUD_R + S.NUT_POCKET_W / 2), 2)
    # wall gap
    out["wall_gap_mm"] = S.HUB_T
    return out


def halo_numbers():
    """Heat-safe halo, layout D (12 in MDF sconce, plain and lit). Everything from the parameters, mm."""
    out = {}
    Rbp, Ro, Ri = S.BP12_D / 2, S.HALO_RING_OD / 2, S.HALO_RING_ID / 2
    s_in, s_out = S.HALO_STRIP_R - S.LED_W / 2, S.HALO_STRIP_R + S.LED_W / 2
    hd, hh = S.HALO_SCREW_HEAD
    out["halo_ring_od_inside_backplate_rim_mm"] = round(Rbp - Ro, 2)
    out["halo_ring_id_outside_hub_mm"] = round(Ri - S.HUB_D / 2, 2)
    out["halo_ring_id_outside_hub_screw_countersinks_mm"] = round(Ri - (S.HUB_SCREW_R + S.HUB_SCREW_CSK_D / 2), 2)
    out["halo_ring_id_outside_bayonet_studs_mm"] = round(Ri - (S.STUD_R + S.STUD_D / 2), 2)
    out["halo_strip_inner_edge_radius_mm"] = s_in
    out["halo_strip_outer_edge_radius_mm"] = s_out
    out["halo_strip_outer_edge_inside_ring_od_mm"] = round(Ro - s_out, 2)
    out["halo_strip_outer_edge_inside_backplate_rim_mm(no line of sight from the LEDs to the record)"] = round(Rbp - s_out, 2)
    out["halo_strip_inner_edge_to_screw_head_mm"] = round(s_in - (S.HALO_SCREW_R + hd / 2), 2)
    out["halo_screw_hole_edge_to_ring_id_mm"] = round(S.HALO_SCREW_R - S.HEAT_RING_HOLE_D / 2 - Ri, 2)
    out["halo_stack_height_at_the_strip_mm(cork + aluminium + strip)"] = round(S.HALO_STACK_H, 2)
    out["halo_stack_height_at_a_screw_head_mm"] = round(S.HALO_STACK_H_AT_SCREW, 2)
    out["halo_cavity_depth_mm(wall to backplate back face)"] = S.HUB_T
    out["halo_strip_face_to_wall_mm"] = round(S.HUB_T - S.HALO_STACK_H, 2)
    out["halo_screw_head_to_wall_mm"] = round(S.HUB_T - S.HALO_STACK_H_AT_SCREW, 2)
    jack_top = S.CORD_Z0 + S.PIGTAIL_CORD[1] / 2 + S.INLINE_JACK[0] / 2
    out["halo_stack_to_inline_jack_gap_along_z_mm"] = round(S.HUB_T - S.HALO_STACK_H_AT_SCREW - jack_top, 2)
    out["solid_material_between_strip_and_record_mm(aluminium + cork + MDF)"] = round(S.HEAT_RING_T + S.CORK_RING_T + S.BP_T, 2)
    pen = S.HALO_SCREW_L - S.HEAT_RING_T - S.CORK_RING_T
    out["halo_screw_engagement_in_mdf_mm"] = round(pen, 2)
    out["halo_screw_tip_behind_backplate_front_face_mm"] = round(S.BP_T - pen, 2)
    out["halo_pilot_bottom_behind_backplate_front_face_mm"] = round(S.BP_T - S.HALO_PILOT_DEPTH, 2)
    out["halo_pilot_depth_minus_screw_engagement_mm"] = round(S.HALO_PILOT_DEPTH - pen, 2)
    out["halo_pilot_bottom_behind_felt_target_floor_mm(even if a pilot sat under a target)"] = round(
        S.BP_T - S.PAD_TARGET_DEPTH - S.HALO_PILOT_DEPTH, 2)
    # plan-view distances from the screw axes (thread major diameter) to everything else cut into the backplate
    pads = [S.pol(r, a) for r in (S.PAD_R_OUT, S.PAD_R_IN) for a in S.PAD_ANGLES]
    scr = [S.pol(S.HALO_SCREW_R, a) for a in S.HALO_SCREW_ANGLES]
    out["halo_screw_to_nearest_felt_target_edge_in_plan_mm"] = round(min(
        math.hypot(sx - px, sy - py) for sx, sy in scr for px, py in pads) - (S.PAD_D + 0.6) / 2 - S.HALO_SCREW_MAJOR_D / 2, 2)

    def to_channel(x, y):       # channel: |x| <= W/2, y from -R1 to -R0
        dx = max(abs(x) - S.BACK_CHAN_W / 2, 0.0)
        dy = max(-S.BACK_CHAN_R1 - y, y + S.BACK_CHAN_R0, 0.0)
        return math.hypot(dx, dy)
    out["halo_screw_to_back_lead_channel_in_plan_mm"] = round(min(to_channel(x, y) for x, y in scr) - S.HALO_SCREW_MAJOR_D / 2, 2)
    out["halo_screw_to_hub_edge_in_plan_mm"] = round(S.HALO_SCREW_R - hd / 2 - S.HUB_D / 2, 2)
    hubs = [S.pol(S.HUB_SCREW_R, a) for a in S.HUB_SCREW_ANGLES]
    out["halo_screw_to_nearest_hub_screw_in_plan_mm"] = round(min(
        math.hypot(sx - px, sy - py) for sx, sy in scr for px, py in hubs) - S.HUB_SCREW_CSK_D / 2 - S.HALO_SCREW_MAJOR_D / 2, 2)
    out["halo_screw_to_insert_bore_in_plan_mm"] = round(S.HALO_SCREW_R - S.INSERT_BORE_D / 2 - S.HALO_SCREW_MAJOR_D / 2, 2)
    out["back_lead_channel_end_inside_cork_ring_id_mm"] = round(Ri - S.BACK_CHAN_R1, 2)
    out["back_lead_channel_start_under_the_hub_mm"] = round(S.HUB_D / 2 - S.BACK_CHAN_R0, 2)
    # 7 in sconce: why it is NOT on layout D
    band7 = S.BP7_D / 2 - (Rbp - Ro) - S.HUB_D / 2
    out["7in_back_face_band_outside_the_hub_at_the_same_rim_margin_mm"] = round(band7, 2)
    out["7in_ring_width_left_with_1mm_hub_clearance_mm(for an 8 mm strip and a 5.6 screw head)"] = round(band7 - 1.0, 2)
    return out


def to_cq_assembly(parts, name="record_sconce"):
    colors = {"steel": (0.6, 0.62, 0.65), "chrome": (0.85, 0.87, 0.9), "nut": (0.7, 0.7, 0.65), "petg": (0.25, 0.27, 0.3),
              "black": (0.08, 0.08, 0.09), "mdf": (0.15, 0.15, 0.16), "alu": (0.7, 0.72, 0.74), "brass": (0.78, 0.62, 0.3),
              "led": (1.0, 0.8, 0.5), "felt": (0.55, 0.5, 0.42), "vinyl": (0.05, 0.05, 0.06), "plastic": (0.12, 0.12, 0.13),
              "cork": (0.62, 0.45, 0.28)}
    asm = cq.Assembly(name=name)
    for n, p, c, _ in parts:
        asm.add(p, name=n, color=cq.Color(*colors[c]))
    return asm
