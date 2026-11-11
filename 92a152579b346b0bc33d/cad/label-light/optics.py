"""Label-light optics: baseline (the renders Austin rejected) vs RS-CAP-12L (cavity + louver + satin window).

Run from cad/:  .venv/bin/python label-light/optics.py
Writes label-light/optics-results.json, label-light/optics-profile.png, label-light/RS-CAP-12L.ies
Geometry comes from sconce_lit.py (the same numbers that make the STEP files). Optics frame: label plane z = 0,
cap contact face at z = +0.25 (the PET label washer; rev B has no felt under the lit cap), so optics z = cap z + 0.25.
"""
import json
import math
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import raytrace as RT          # noqa: E402
import sconce_lit as L         # noqa: E402

ZOFF = L.S.PET_WASHER[2]         # 0.25: rev B has no felt under the lit cap, its flange sits on the PET label washer (rev A: 0.3 of felt)
LABEL_R = 50.5
CAP_R = L.DOME_R


def leds_src(n, rng, facing_down=True):
    k = rng.integers(0, L.LED_N, n)
    az = 2 * np.pi * k / L.LED_N + np.pi / 2
    ut = (rng.random(n) - 0.5) * 2.6        # LUXEON 2835 light-emitting surface ~2.6 x 1.8 (estimate)
    ur = (rng.random(n) - 0.5) * 1.8
    rad = np.stack([np.cos(az), np.sin(az), 0 * az], 1)
    tan = np.stack([-np.sin(az), np.cos(az), 0 * az], 1)
    o = rad * (L.LED_R + ur)[:, None] + tan * ut[:, None]
    o[:, 2] = L.LPCB_Z0 - L.LED_SIZE[2] + ZOFF
    ax = np.tile([0, 0, -1.0 if facing_down else 1.0], (n, 1))
    return o, RT.lambert(ax, n, rng)


def scene_lit(Rfloor=0.92, Rpcb=0.85, Rlip=0.65, satin=L.WIN_SATIN_DEG, white=L.LOUV_WHITE_FRAC):
    z = lambda c: c + ZOFF          # noqa: E731
    segs = []
    # cavity: flange top (white paint) from the louver inner edge to the column, column, PCB underside (white mask)
    segs += RT.chain([(L.LOUV_RI, z(L.FLANGE_T)), (L.COL_R, z(L.FLANGE_T)), (L.COL_R, z(L.COL_TOP))], "diffuse", R=Rfloor)
    segs += RT.chain([(L.COL_R, z(L.LPCB_Z0)), (L.LPCB_D / 2, z(L.LPCB_Z0)), (L.LPCB_D / 2, z(L.LPCB_Z0 + L.LPCB_T))], "diffuse", R=Rpcb)
    segs += RT.chain([(L.DOME_WALL_R, z(L.DOME_Z0)), (L.DOME_WALL_R, z(L.LPCB_Z0 + 1.0)), (0.01, z(L.LPCB_Z0 + 1.0))], "absorb")
    Lr = L.LOUV_RO - L.LOUV_RI
    rw = L.LOUV_RI + white * Lr
    t0 = math.tan(math.radians(L.LOUV_TILTS[0]))
    # channel floor = 8 deg conical flange top: white inner part, black outer part
    zf0 = z(L.FLANGE_T)
    if white > 0:
        segs += RT.chain([(L.LOUV_RI, zf0), (rw, zf0 - (rw - L.LOUV_RI) * t0)], "diffuse", R=Rfloor)
    segs += RT.chain([(rw, zf0 - (rw - L.LOUV_RI) * t0), (L.LOUV_RO, zf0 - Lr * t0)], "absorb")
    for zf, tt in zip(L.louver_fin_z(), L.LOUV_TILTS[1:]):
        t = math.tan(math.radians(tt))
        zi, zw, zo = z(zf), z(zf) - (rw - L.LOUV_RI) * t, z(zf) - Lr * t
        if white > 0:
            segs += RT.chain([(rw, zw + L.LOUV_FIN_T), (L.LOUV_RI, zi + L.LOUV_FIN_T), (L.LOUV_RI, zi), (rw, zw)], "diffuse", R=Rfloor)
        segs += RT.chain([(rw, zw), (L.LOUV_RO, zo), (L.LOUV_RO, zo + L.LOUV_FIN_T), (rw, zw + L.LOUV_FIN_T)], "absorb")
    # gap (L.LIP_GAP) between the louver top and the dome lip: black lip underside over the louver
    segs += RT.chain([(L.LOUV_RI, z(L.DOME_Z0)), (L.WIN_RO, z(L.DOME_Z0))], "absorb")
    # window ring (clear, satin outer face)
    g = RT.poly([(L.WIN_RI, z(L.WIN_Z0)), (L.WIN_RO, z(L.WIN_Z0)), (L.WIN_RO, z(L.WIN_Z1)), (L.WIN_RI, z(L.WIN_Z1))], "glass")
    for s in g:
        if abs(s.r1 - L.WIN_RO) < 1e-9 and abs(s.r2 - L.WIN_RO) < 1e-9:
            s.sigma = math.radians(satin)
    segs += g
    # flange rim + underside (black), lip mirror (chrome underside of the dome band), band
    segs += RT.chain([(L.WIN_RO, z(L.WIN_Z0)), (L.CORE_R, z(L.WIN_Z0)), (L.CORE_R, z(0)), (L.S.CAP_SHOULDER_D / 2, z(0))], "absorb")
    segs += RT.chain([(L.WIN_RO, z(L.DOME_Z0)), (L.DOME_R, z(L.DOME_Z0)), (L.DOME_R, z(L.DOME_Z0 + L.DOME_BAND_H))], "mirror", R=Rlip)
    return segs


def scene_baseline():
    """renders-labellight geometry: 16 side LEDs at r 21.8 under a thin flared chrome skirt."""
    segs = RT.chain([(18.8, 4.2), (24.0, 3.0), (24.4, 2.4)], "mirror", R=0.65)
    segs += RT.chain([(10, 0.3), (19.05, 0.3), (19.05, 1.6)], "absorb")
    return segs


def baseline_src(n, rng):
    k = rng.integers(0, 16, n)
    az = 2 * np.pi * k / 16
    rad = np.stack([np.cos(az), np.sin(az), 0 * az], 1)
    tan = np.stack([-np.sin(az), np.cos(az), 0 * az], 1)
    o = rad * 21.8 + tan * ((rng.random(n) - 0.5) * 1.0)[:, None]
    o[:, 2] = 1.4 + (rng.random(n) - 0.5) * 0.6
    return o, RT.lambert(rad, n, rng)


def run(scene, src, n, seed):
    rng = np.random.default_rng(seed)
    o, d = src(n, rng)
    return RT.trace(scene, o, d, np.zeros(n, bool), np.random.default_rng(seed + 1), max_bounce=150)


def summarize(res, nb=12):
    rc, E = RT.profile(res, CAP_R, LABEL_R, nb)
    m = rc >= CAP_R + 2.5
    eff = res["w"][(res["r"] > CAP_R) & (res["r"] < LABEL_R)].sum() / res["n"]
    return dict(r_mm=[round(x, 2) for x in rc], E_rel=[round(x, 3) for x in (E / E[m].mean())],
                max_over_min_r21_to_50=round(float(E[m].max() / E[m].min()), 2),
                fraction_of_led_flux_on_label=round(float(eff), 5),
                glare_fraction_upward=round(float(res["glare"] / res["n"]), 5),
                rays=int(res["n"]))


def azimuthal(res, r0, r1):
    m = (res["r"] > r0) & (res["r"] < r1)
    ang = np.degrees(np.arctan2(res["xy"][m, 1], res["xy"][m, 0])) % (360 / L.LED_N)
    h, _ = np.histogram(ang, 12, weights=res["w"][m])
    return round(float(h.max() / h.min()), 2)


def write_ies(res, path, n_v=37, n_h=13):
    """Type C IES (LM-63-2002) for ONE emitter of a 48-emitter ring at r = WIN_RO, built from the traced rays that land
    on the label (their directions). Local frame: H = 0 deg points radially outward, V = 0 is straight down."""
    d = res["d"]; xy = res["xy"]; w = res["w"]
    keep = (res["r"] > CAP_R) & (res["r"] < 60)
    d, xy, w = d[keep], xy[keep], w[keep]
    # radial / tangential components at the ray's own azimuth (back-projected to the window)
    az = np.arctan2(xy[:, 1], xy[:, 0])
    dr = d[:, 0] * np.cos(az) + d[:, 1] * np.sin(az)
    dt = -d[:, 0] * np.sin(az) + d[:, 1] * np.cos(az)
    V = np.degrees(np.arccos(np.clip(-d[:, 2], -1, 1)))
    H = np.degrees(np.arctan2(dt, dr))
    vb = np.linspace(0, 90, n_v)
    hb = np.linspace(0, 180, n_h)                       # bilateral symmetry about H=0
    I = np.zeros((n_h, n_v))
    dv, dh = vb[1] - vb[0], hb[1] - hb[0]
    for i, hc in enumerate(hb):
        mh = np.abs(np.abs(H) - hc) <= dh / 2
        for j, vc in enumerate(vb):
            mv = np.abs(V - vc) <= dv / 2
            sa = max(math.sin(math.radians(max(vc, 0.5))), 1e-3) * math.radians(dv) * math.radians(dh) * 2
            I[i, j] = w[mh & mv].sum() / sa
    I = I / I.max() * 1000.0
    lines = ["IESNA:LM-63-2002", "[TEST] RS-CAP-12L Monte Carlo (cad/label-light/optics.py), relative candela",
             "[MANUFAC] record-sconces", "[LUMINAIRE] RS-CAP-12L label light, one of 48 ring emitters at the window",
             "TILT=NONE", f"1 -1 1 {n_v} {n_h} 1 2 0.001 0.001 0.001", "1.0 1.0 0.1",
             " ".join(f"{v:.2f}" for v in vb), " ".join(f"{h:.1f}" for h in hb)]
    for i in range(n_h):
        lines.append(" ".join(f"{x:.2f}" for x in I[i]))
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def plot(base, lit, sens, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
    for res, lab, c in ((base, "renders-labellight concept (side LEDs under a skirt)", "#c0392b"), (lit, "RS-CAP-12L (cavity + louver + satin window)", "#1f4e79")):
        rc, E = RT.profile(res, CAP_R, LABEL_R, 12)
        m = rc >= CAP_R + 2.5
        ax[0].plot(rc, E / E[m].mean(), "o-", color=c, label=lab, lw=1.6, ms=4)
    ax[0].set_yscale("log"); ax[0].set_xlabel("radius on the label (mm), cap edge 19.05 -> label edge 50.5")
    ax[0].set_ylabel("irradiance / mean (log)"); ax[0].grid(alpha=0.3, which="both"); ax[0].legend(fontsize=8)
    ax[0].set_title("Label irradiance profile (Monte Carlo)", fontsize=10, loc="left")
    rc, E = RT.profile(lit, CAP_R, LABEL_R, 12)
    m = rc >= CAP_R + 2.5
    ax[1].plot(rc, E / E[m].mean(), "o-", color="#1f4e79", lw=1.8, label="nominal")
    for k, (res, lab) in sens.items():
        rc2, E2 = RT.profile(res, CAP_R, LABEL_R, 12)
        ax[1].plot(rc2, E2 / E2[rc2 >= CAP_R + 2.5].mean(), "--", lw=1, label=lab)
    ax[1].set_ylim(0, 2.2); ax[1].set_xlabel("radius on the label (mm)"); ax[1].grid(alpha=0.3); ax[1].legend(fontsize=7)
    ax[1].set_title("RS-CAP-12L, linear scale, with tolerance cases", fontsize=10, loc="left")
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def main(n=1_200_000):
    out = {}
    base = run(scene_baseline(), baseline_src, 400_000, 11)
    out["baseline"] = summarize(base)
    lit = run(scene_lit(), leds_src, n, 21)
    out["RS-CAP-12L"] = summarize(lit)
    out["RS-CAP-12L"]["azimuthal_max_over_min_r19_26"] = azimuthal(lit, 19.05, 26)
    out["RS-CAP-12L"]["azimuthal_max_over_min_r35_50"] = azimuthal(lit, 35, 50.5)
    sens = {}
    for key, kw, lab in (("satin_6deg", dict(satin=6.0), "window satin 6 deg (rougher)"),
                         ("satin_1deg", dict(satin=1.0), "window satin 1 deg (clearer)"),
                         ("paint_R0.85", dict(Rfloor=0.85), "white paint R 0.85"),
                         ("no_white_tips", dict(white=0.0), "all-black fins")):
        r = run(scene_lit(**kw), leds_src, n // 3, 31)
        out["sens_" + key] = summarize(r)
        sens[key] = (r, lab)
    # photometry: LED flux at the CCR current (LUXEON 2835 2700K/90: 31 lm typ at 65 mA, flux ~ linear in I below 65 mA,
    # +10 % efficacy gain at low current = estimate)
    i_led = L.I_CCR / 2
    lm_led = 31.0 * (i_led / 0.065) * 1.10
    lm_total = lm_led * L.LED_N
    lm_label = lm_total * out["RS-CAP-12L"]["fraction_of_led_flux_on_label"]
    area_m2 = math.pi * (LABEL_R ** 2 - CAP_R ** 2) * 1e-6
    out["photometry"] = dict(I_per_LED_mA=i_led * 1e3, lm_per_LED_est=round(lm_led, 2), lm_LEDs_total_est=round(lm_total, 1),
                             lm_on_label_est=round(lm_label, 3), mean_lux_on_label_est=round(lm_label / area_m2, 0),
                             label_annulus_mm2=round(area_m2 * 1e6, 0))
    with open(os.path.join(HERE, "optics-results.json"), "w") as f:
        json.dump(out, f, indent=1)
    plot(base, lit, sens, os.path.join(HERE, "optics-profile.png"))
    write_ies(lit, os.path.join(HERE, "RS-CAP-12L.ies"))
    print(json.dumps({k: (v if k == "photometry" else {kk: vv for kk, vv in v.items() if kk not in ("r_mm",)}) for k, v in out.items()}, indent=1))


if __name__ == "__main__":
    main()
