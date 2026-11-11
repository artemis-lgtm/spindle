"""RS-CAP-12L label-light assembly: the 12 in MDF sconce from assembly.py with the plain cap + felt swapped for the lit
cap, and the hub contact module dropped into the RS-HUB-01 centre relief. World frame = assembly.py's.
Rev B: record on the centre backing ring, PET label washer under the cap, plunger + guard-tube centre contact."""
import sconce_cad as S
import sconce_lit as L
import assembly as A


def build_lit(rec_t=S.REC12_T):
    """The lit cap has no felt: its flat flange sits on the PET label washer, which sits on the label."""
    parts = [p for p in A.build("12", "mdf") if p[0] not in ("felt_washer", "dome_cap_12", "record_12", "pet_label_washer")]
    z_bp0 = S.HUB_T                                   # backplate back face (module frame z=0)
    z_rec0 = z_bp0 + S.BP_T + S.REC_SEAT_H
    z_pet = z_rec0 + rec_t
    zc = z_pet + S.PET_WASHER[2]                      # cap contact face (flange underside)
    parts.append(("record_12", S.record(S.REC12_D, rec_t, S.REC_HOLE_D).translate((0, 0, z_rec0)), "vinyl", "customer"))
    parts.append(("pet_label_washer", S.pet_washer().translate((0, 0, z_pet)), "led", "purchased"))
    cap = [("lit_core", L.core_lit(asm=True), "chrome", "custom"), ("lit_dome", L.dome_lit(), "chrome", "custom"),
           ("lit_louver", L.louver_lit(), "black", "custom"), ("lit_window", L.window_lit(), "led", "custom"),
           ("lit_pin", L.pin_lit(), "brass", "custom"), ("peek_sleeve", L.sleeve_lit(), "felt", "custom"),
           ("led_pcb", L.led_pcb(), "petg", "custom"), ("leds_2835", L.leds(), "led", "purchased")]
    for n, p, c, k in cap:
        parts.append((n, p.translate((0, 0, zc)), c, k))
    face = (zc - z_bp0) - L.LC_STUD_L + L.PIN_RECESS          # gold pin face, module frame
    tip = min(face, L.PLG_FREE_TIP)                           # plunger nose rides on the pin face
    hub = [("hub_pcb", L.hub_pcb(), "petg", "custom"), ("hub_carrier_guard", L.carrier(), "black", "custom"),
           ("ccr_sod123", L.ccr_body(), "black", "purchased"),
           ("contact_plunger", L.plunger(tip), "brass", "custom"),
           ("contact_spring", L.spring(tip), "steel", "purchased"),
           ("pogo_return_0919", L.pogo(L.POGO_RET, L.CAR_Z0, 0.0, *L.POGO_R_POS), "brass", "purchased")]
    for n, p, c, k in hub:
        parts.append((n, p.translate((0, 0, z_bp0)), c, k))
    return parts
