"""Steady-state axisymmetric heat model of the 12 in MDF sconce: how warm does the RECORD get from the halo strip?
Finite-volume conduction in (r, z) with convective/radiative film coefficients to room air. Compares strip placements.
  .venv/bin/python thermal.py            -> prints a table, writes thermal-results.json
z = 0 is the backplate BACK face, +z toward the room. All temperatures are RISE over room air (K).
NOT modelled: the buoyant air plume (bounded separately in THERMAL.md). This is a calculation, not a measurement.
Config F is the FINAL layout D geometry and takes its dimensions from sconce_cad.py, so it cannot drift from the CAD.
Two cases are run: NORMAL (4 W strip, 30 C room) and WORST (the wrong 6 W strip, every film coefficient halved, 35 C room).
"""
import json, math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

DR, DZ = 0.5e-3, 0.1e-3      # DZ was 0.25: too coarse to tell 1.6 mm cork from 1.5 mm
R_MAX, Z0, Z1 = 160e-3, -3e-3, 15.83e-3
R_BP, R_REC = 133.35e-3, 152.4e-3
T_BP, Z_REC0, Z_REC1 = 12.7e-3, 13.80e-3, 15.83e-3
K = {1: 0.14, 2: 0.026, 3: 0.16, 4: 200.0, 5: 0.045}     # MDF, still air, PVC, aluminium, cork
P_IN = 4.0                    # W electrical, the capped 4 W strip
ETA_LIGHT = 0.35              # 2835 warm white, ~105 lm/W of ~300 lm/W
Q_HEAT, Q_LIGHT = P_IN * (1 - ETA_LIGHT), P_IN * ETA_LIGHT
H_ROOM, H_CAVITY, H_STRIP = 8.0, 6.0, 12.0   # W/m2K: open faces, the 1 in cavity behind the plate, a narrow warm strip
CASES = {"normal": dict(p_in=4.0, h_scale=1.0, room_C=30.0), "worst": dict(p_in=6.0, h_scale=0.5, room_C=35.0)}


def set_case(case):
    """Switch the module to a named case (strip power and film coefficients)."""
    global P_IN, Q_HEAT, Q_LIGHT, H_ROOM, H_CAVITY, H_STRIP
    c = CASES[case]
    P_IN = c["p_in"]
    Q_HEAT, Q_LIGHT = P_IN * (1 - ETA_LIGHT), P_IN * ETA_LIGHT
    H_ROOM, H_CAVITY, H_STRIP = 8.0 * c["h_scale"], 6.0 * c["h_scale"], 12.0 * c["h_scale"]

nr, nz = int(round(R_MAX / DR)), int(round((Z1 - Z0) / DZ))
rc = (np.arange(nr) + 0.5) * DR
zc = Z0 + (np.arange(nz) + 0.5) * DZ


def build(cfg):
    mat = np.zeros((nr, nz), dtype=int)
    R, Z = np.meshgrid(rc, zc, indexing="ij")
    mat[(R < R_BP) & (Z >= 0) & (Z < T_BP)] = 1
    mat[(R < R_BP) & (Z >= T_BP) & (Z < Z_REC0)] = 2
    mat[(R < R_REC) & (Z >= Z_REC0) & (Z < Z_REC1)] = 3
    src = np.zeros((nr, nz))
    if cfg["kind"] == "rim":
        m = (R >= R_BP - 1.5e-3) & (R < R_BP) & (Z >= 2.35e-3) & (Z < 10.35e-3)
    else:
        r0, r1 = cfg["ring"]
        if cfg.get("cork"):
            mat[(R >= r0) & (R < r1) & (Z >= -cfg["cork"]) & (Z < 0)] = 5
        za1 = -cfg.get("cork", 0.0); za0 = za1 - cfg.get("alu", 0.0)
        if cfg.get("alu"):
            mat[(R >= r0) & (R < r1) & (Z >= za0) & (Z < za1)] = 4
            m = (R >= cfg["strip"][0]) & (R < cfg["strip"][1]) & (Z >= za0) & (Z < za1)
        else:
            m = (R >= cfg["strip"][0]) & (R < cfg["strip"][1]) & (Z >= 0) & (Z < 0.5e-3)
    vol = 2 * math.pi * R * DR * DZ
    src[m] = Q_HEAT * vol[m] / vol[m].sum()
    # light / IR landing on the back of the record's overhang
    ov = (R >= R_BP) & (R < R_REC) & (Z >= Z_REC0) & (Z < Z_REC0 + DZ)
    src[ov] += cfg.get("q_overhang", 0.0) * vol[ov] / vol[ov].sum()
    return mat, src, m


def solve(cfg):
    mat, src, strip_mask = build(cfg)
    idx = -np.ones((nr, nz), dtype=int)
    solid = mat > 0
    idx[solid] = np.arange(solid.sum())
    n = solid.sum()
    rows, cols, vals = [], [], []
    diag = np.zeros(n)
    kk = np.zeros((nr, nz)); 
    for kmat, kv in K.items():
        kk[mat == kmat] = kv

    def h_for(i, j, direction):
        z = zc[j]
        if cfg["kind"] == "rim" and direction == "r+" and strip_mask[i, j]:
            return H_STRIP
        if z < T_BP and direction in ("z-",):
            return H_CAVITY
        if z < 0:
            return H_CAVITY
        return H_ROOM

    def link(i, j, i2, j2, area, d, direction):
        a = idx[i, j]
        inside = 0 <= i2 < nr and 0 <= j2 < nz and solid[i2, j2]
        if inside:
            g = area / (d / 2 / kk[i, j] + d / 2 / kk[i2, j2])
            rows.append(a); cols.append(idx[i2, j2]); vals.append(-g); diag[a] += g
        elif i2 >= 0:                      # exterior (i2 < 0 is the axis: no flux)
            g = area / (d / 2 / kk[i, j] + 1.0 / h_for(i, j, direction))
            diag[a] += g
    for i in range(nr):
        for j in range(nz):
            if not solid[i, j]:
                continue
            r = rc[i]
            link(i, j, i + 1, j, 2 * math.pi * (r + DR / 2) * DZ, DR, "r+")
            link(i, j, i - 1, j, 2 * math.pi * (r - DR / 2) * DZ, DR, "r-")
            link(i, j, i, j + 1, 2 * math.pi * r * DR, DZ, "z+")
            link(i, j, i, j - 1, 2 * math.pi * r * DR, DZ, "z-")
    A = sp.csr_matrix((vals + list(diag), (rows + list(range(n)), cols + list(range(n)))), shape=(n, n))
    T = np.zeros((nr, nz)); T[solid] = spl.spsolve(A, src[solid])
    rec = mat == 3
    Trec = np.where(rec, T, -1)
    i, j = np.unravel_index(Trec.argmax(), Trec.shape)
    edge = T[(rc >= R_BP)[:, None] & rec].max()
    centre = T[(rc < 19.05e-3)[:, None] & rec].max()          # the part of the record under the 38.1 mm cap
    return dict(record_max=float(Trec.max()), record_max_r_mm=float(rc[i] * 1e3), record_overhang_max=float(edge),
                record_under_cap_max=float(centre),
                source_max=float(T[strip_mask].max()), mdf_front_max=float(T[:, np.searchsorted(zc, T_BP) - 1].max()))


# view factor, strip (8 mm, on the rim) -> record overhang (19 mm, perpendicular, 3.45 mm forward): crossed strings
a_near, a_far, b = 3.45, 11.45, 19.05
F_RIM = ((math.hypot(b, a_near) + a_far) - (a_near + math.hypot(b, a_far))) / (2 * (a_far - a_near))

STRAY_W_AT_4W = 0.1           # back-face layouts: stray light assumed to reach the record's overhang off the wall, at 4 W


def final_cfg():
    """Final layout D geometry, read from the CAD parameters (mm -> m)."""
    import sconce_cad as S
    geo = dict(ring_r_mm=[S.HALO_RING_ID / 2, S.HALO_RING_OD / 2],
               strip_r_mm=[S.HALO_STRIP_R - S.LED_W / 2, S.HALO_STRIP_R + S.LED_W / 2],
               cork_mm=S.CORK_RING_T, alu_mm=S.HEAT_RING_T, backplate_r_mm=S.BP12_D / 2, backplate_t_mm=S.BP_T,
               record_r_mm=S.REC12_D / 2, record_seat_mm=S.REC_SEAT_H, record_t_mm=round(S.REC12_T, 3))
    assert abs(geo["backplate_r_mm"] * 1e-3 - R_BP) < 1e-9 and abs(geo["record_r_mm"] * 1e-3 - R_REC) < 1e-9
    assert abs(geo["backplate_t_mm"] * 1e-3 - T_BP) < 1e-9 and abs((S.BP_T + S.REC_SEAT_H) * 1e-3 - Z_REC0) < 1e-9
    cfg = dict(kind="back", ring=tuple(v * 1e-3 for v in geo["ring_r_mm"]), strip=tuple(v * 1e-3 for v in geo["strip_r_mm"]),
               alu=geo["alu_mm"] * 1e-3, cork=geo["cork_mm"] * 1e-3, q_overhang=STRAY_W_AT_4W)
    return cfg, geo


F_NAME = "F  FINAL layout D as built in the CAD: ring r 100 to 130, strip r 111 to 119, cork 1.6"
CONFIGS = [
    ("A  old: strip on the rim, facing out", dict(kind="rim")),
    ("B  strip on the back face, bare MDF", dict(kind="back", ring=(0.103, 0.133), strip=(0.114, 0.122), q_overhang=0.1)),
    ("C  back face on 1 mm aluminium ring, 30 mm wide", dict(kind="back", ring=(0.103, 0.133), strip=(0.114, 0.122), alu=1e-3, q_overhang=0.1)),
    ("D  study version: C plus 2 mm cork (ring r 103 to 133)", dict(kind="back", ring=(0.103, 0.133), strip=(0.114, 0.122), alu=1e-3, cork=2e-3, q_overhang=0.1)),
    ("E  D with the ring pulled 10 mm in from the rim", dict(kind="back", ring=(0.093, 0.123), strip=(0.104, 0.112), alu=1e-3, cork=2e-3, q_overhang=0.1)),
]


def run_case(case, configs):
    set_case(case)
    room = CASES[case]["room_C"]
    res = {}
    print(f"\nCASE {case}: {P_IN:.0f} W strip, film coefficients x{CASES[case]['h_scale']}, {room:.0f} C room")
    print(f"{'config':72s} {'strip K':>8s} {'record max K':>13s} {'at r mm':>8s} {'overhang K':>11s} {'under cap K':>12s} {'record C':>9s}")
    for name, cfg in configs:
        cfg = dict(cfg)
        if cfg["kind"] == "rim":
            cfg["q_overhang"] = F_RIM * Q_LIGHT
            r0 = solve(cfg)                      # first pass for strip temperature, then add its thermal IR
            ir = 0.9 * 5.67e-8 * 4 * 308 ** 3 * r0["source_max"] * (2 * math.pi * R_BP * 8e-3) * F_RIM
            cfg["q_overhang"] = F_RIM * Q_LIGHT + ir
        else:
            cfg["q_overhang"] = cfg.get("q_overhang", 0.0) * P_IN / 4.0     # stray light scales with strip power
        r = solve(cfg)
        r["q_overhang_W"] = cfg.get("q_overhang", 0)
        r["record_C"] = room + r["record_max"]
        r["strip_C"] = room + r["source_max"]
        res[name] = r
        print(f"{name:72s} {r['source_max']:8.1f} {r['record_max']:13.1f} {r['record_max_r_mm']:8.1f} {r['record_overhang_max']:11.1f} "
              f"{r['record_under_cap_max']:12.2f} {r['record_C']:9.1f}")
    return res


if __name__ == "__main__":
    import os
    fcfg, geo = final_cfg()
    configs = CONFIGS + [(F_NAME, fcfg)]
    out = {"assumptions": dict(eta_light=ETA_LIGHT, h_room=8.0, h_cavity=6.0, h_strip=12.0, k_W_mK=dict(mdf=K[1], air=K[2], pvc=K[3], aluminium=K[4], cork=K[5]),
                               stray_light_to_overhang_W_at_4W=STRAY_W_AT_4W,
                               view_factor_rim_to_overhang=round(F_RIM, 3), vinyl_softens_C="55-60", cases=CASES),
           "final_geometry": geo, "final_name": F_NAME}
    print(f"view factor rim strip -> record overhang: {F_RIM:.2f}")
    for case in ("normal", "worst"):
        out[case] = run_case(case, configs)
    # why 1/16 in cork is acceptable: the final geometry with other cork thicknesses
    out["cork_comparison"] = {}
    for mm in (2.0, 1.6, 1.5, 0.0):
        c = dict(fcfg)
        if mm:
            c["cork"] = mm * 1e-3
        else:
            c.pop("cork")
        row = {}
        for case in ("normal", "worst"):
            set_case(case)
            cc = dict(c); cc["q_overhang"] = c["q_overhang"] * P_IN / 4.0
            r = solve(cc)
            row[case] = dict(record_C=CASES[case]["room_C"] + r["record_max"], strip_C=CASES[case]["room_C"] + r["source_max"])
        out["cork_comparison"][f"{mm:.1f}"] = row
        print(f"cork {mm:.1f} mm: record {row['normal']['record_C']:.2f} C normal, {row['worst']['record_C']:.2f} C worst; strip {row['normal']['strip_C']:.1f} / {row['worst']['strip_C']:.1f} C")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thermal-results.json"), "w"), indent=1)
