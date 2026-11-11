"""Axisymmetric Monte Carlo raytracer for the RS-CAP-12L label light (3D rays, surfaces of revolution).

Scene = surfaces of revolution given as (r, z) profile segments, each one a cone frustum / annulus / cylinder:
  mirror  : specular reflector, reflectance R
  absorb  : black, kills the ray
  glass   : air / PMMA boundary (n = 1.49), Fresnel split + TIR, optional surface roughness (satin, sigma deg)
  diffuse : Lambertian reflector, reflectance R (white paint / PCB solder mask)
The label plane is z = 0 (paper). Every ray that lands on z = 0 is tallied by radius; that is the irradiance
profile E(r). Rays that leave the scene upward past the cap are tallied as glare.
Units mm. z up (away from the label), r radial from the spindle axis.
"""
import numpy as np

N_PMMA = 1.49
EPS = 1e-6


class Seg:
    def __init__(self, r1, z1, r2, z2, kind, R=1.0, sigma=0.0, name=""):
        self.r1, self.z1, self.r2, self.z2 = r1, z1, r2, z2
        self.kind, self.R, self.sigma, self.name = kind, R, np.radians(sigma), name
        dr, dz = r2 - r1, z2 - z1
        L = np.hypot(dr, dz)
        # outward normal for a CCW polygon in the (r, z) plane = (dz, -dr) / L. For glass polygons that is the air side.
        self.nr, self.nz = dz / L, -dr / L


def poly(pts, kind, **kw):
    """Closed polygon (list of (r, z)), CCW in the (r, z) plane, as segments."""
    out = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        if a[0] == b[0] and a[1] == b[1]:
            continue
        if a[0] <= 1e-9 and b[0] <= 1e-9:
            continue          # segment on the axis is not a surface
        out.append(Seg(a[0], a[1], b[0], b[1], kind, **kw))
    return out


def chain(pts, kind, **kw):
    return [Seg(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], kind, **kw) for i in range(len(pts) - 1)]


def hit_seg(o, d, s):
    """Distance along each ray to segment s (inf if none)."""
    n = o.shape[0]
    t_best = np.full(n, np.inf)
    if abs(s.z2 - s.z1) < 1e-12:
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (s.z1 - o[:, 2]) / d[:, 2]
        p = o + t[:, None] * d
        r = np.hypot(p[:, 0], p[:, 1])
        ok = (t > EPS) & (r >= min(s.r1, s.r2) - 1e-9) & (r <= max(s.r1, s.r2) + 1e-9)
        t_best[ok] = t[ok]
        return t_best
    b = (s.r2 - s.r1) / (s.z2 - s.z1)
    a = s.r1 - b * s.z1
    ox, oy, oz = o[:, 0], o[:, 1], o[:, 2]
    dx, dy, dz = d[:, 0], d[:, 1], d[:, 2]
    k = a + b * oz
    A = dx * dx + dy * dy - b * b * dz * dz
    B = 2 * (ox * dx + oy * dy - b * dz * k)
    C = ox * ox + oy * oy - k * k
    zlo, zhi = min(s.z1, s.z2), max(s.z1, s.z2)
    with np.errstate(divide="ignore", invalid="ignore"):
        disc = B * B - 4 * A * C
        sq = np.sqrt(np.where(disc >= 0, disc, np.nan))
        lin = np.abs(A) < 1e-12
        for sign in (-1, 1):
            t = np.where(lin, -C / B, (-B + sign * sq) / (2 * A))
            z = oz + t * dz
            ok = (t > EPS) & (z >= zlo - 1e-9) & (z <= zhi + 1e-9) & ((a + b * z) >= -1e-9) & np.isfinite(t)
            t_best = np.where(ok & (t < t_best), t, t_best)
    return t_best


def normal3(p, s):
    r = np.hypot(p[:, 0], p[:, 1])
    r = np.where(r < 1e-9, 1e-9, r)
    return np.stack([s.nr * p[:, 0] / r, s.nr * p[:, 1] / r, np.full(len(p), s.nz)], 1)


def perturb(nrm, sigma, rng):
    if sigma <= 0:
        return nrm
    t1 = np.cross(nrm, np.array([0.0, 0.0, 1.0]))
    bad = np.linalg.norm(t1, axis=1) < 1e-6
    t1[bad] = np.cross(nrm[bad], np.array([1.0, 0.0, 0.0]))
    t1 /= np.linalg.norm(t1, axis=1)[:, None]
    t2 = np.cross(nrm, t1)
    g1, g2 = rng.normal(0, sigma, len(nrm)), rng.normal(0, sigma, len(nrm))
    n2 = nrm + t1 * np.tan(g1)[:, None] + t2 * np.tan(g2)[:, None]
    return n2 / np.linalg.norm(n2, axis=1)[:, None]


def lambert(axis, n, rng):
    """n Lambertian directions about unit vectors axis (n,3)."""
    u, v = rng.random(n), rng.random(n)
    ct = np.sqrt(1 - u)          # cos theta, Lambertian
    st = np.sqrt(u)
    ph = 2 * np.pi * v
    t1 = np.cross(axis, np.array([0.0, 0.0, 1.0]))
    bad = np.linalg.norm(t1, axis=1) < 1e-6
    t1[bad] = np.cross(axis[bad], np.array([1.0, 0.0, 0.0]))
    t1 /= np.linalg.norm(t1, axis=1)[:, None]
    t2 = np.cross(axis, t1)
    return axis * ct[:, None] + t1 * (st * np.cos(ph))[:, None] + t2 * (st * np.sin(ph))[:, None]


def trace(segs, o, d, inside, rng, max_bounce=40, r_label=(3.63, 50.5), r_bins=None):
    """Returns dict with tallies. inside: bool array, ray starts inside PMMA."""
    n = len(o)
    w = np.ones(n)
    alive = np.ones(n, bool)
    land_r, land_w, land_xy, land_d = [], [], [], []
    glare = 0.0
    lost_abs = 0.0
    spill = 0.0
    for _ in range(max_bounce):
        idx = np.nonzero(alive)[0]
        if len(idx) == 0:
            break
        oo, dd = o[idx], d[idx]
        tmin = np.full(len(idx), np.inf)
        which = np.full(len(idx), -1)
        for k, s in enumerate(segs):
            t = hit_seg(oo, dd, s)
            m = t < tmin
            tmin[m] = t[m]; which[m] = k
        # label plane z = 0
        with np.errstate(divide="ignore", invalid="ignore"):
            tl = np.where(dd[:, 2] < 0, -oo[:, 2] / dd[:, 2], np.inf)
        lab = (tl > EPS) & (tl < tmin)
        # label hits
        li = idx[lab]
        if len(li):
            p = oo[lab] + tl[lab][:, None] * dd[lab]
            r = np.hypot(p[:, 0], p[:, 1])
            land_r.append(r); land_w.append(w[li]); land_xy.append(p[:, :2]); land_d.append(dd[lab])
            alive[li] = False
        # escapes
        esc = (~lab) & (which < 0)
        ei = idx[esc]
        if len(ei):
            up = dd[esc][:, 2] > 0
            glare += w[ei][up].sum()
            spill += w[ei][~up].sum()
            alive[ei] = False
        hitm = (~lab) & (which >= 0)
        for k, s in enumerate(segs):
            m = hitm & (which == k)
            if not m.any():
                continue
            ii = idx[m]
            p = oo[m] + tmin[m][:, None] * dd[m]
            nrm = normal3(p, s)
            din = dd[m]
            if s.kind == "absorb":
                lost_abs += w[ii].sum(); alive[ii] = False; continue
            if s.kind == "mirror":
                nn = perturb(nrm, s.sigma, rng)
                dn = (din * nn).sum(1)
                dout = din - 2 * dn[:, None] * nn
                w[ii] *= s.R
                o[ii] = p + dout * 1e-5; d[ii] = dout; continue
            if s.kind == "diffuse":
                # Lambertian back into the hemisphere the ray came from
                side = np.where(((din * nrm).sum(1) < 0)[:, None], nrm, -nrm)
                dout = lambert(side, len(ii), rng)
                w[ii] *= s.R
                o[ii] = p + dout * 1e-5; d[ii] = dout; continue
            # glass boundary: nrm points to air
            nn = perturb(nrm, s.sigma, rng)
            cos_i = -(din * nn).sum(1)
            ins = inside[ii]
            n1 = np.where(ins, N_PMMA, 1.0); n2 = np.where(ins, 1.0, N_PMMA)
            # orient normal against the incoming ray
            nf = np.where((cos_i < 0)[:, None], -nn, nn)
            ci = np.abs(cos_i)
            eta = n1 / n2
            k2 = 1 - eta ** 2 * (1 - ci ** 2)
            tir = k2 < 0
            ct = np.sqrt(np.clip(k2, 0, None))
            rs = ((n1 * ci - n2 * ct) / (n1 * ci + n2 * ct)) ** 2
            rp = ((n1 * ct - n2 * ci) / (n1 * ct + n2 * ci)) ** 2
            Rf = np.where(tir, 1.0, 0.5 * (rs + rp))
            refl = rng.random(len(ii)) < Rf
            drefl = din + 2 * ci[:, None] * nf
            dtran = eta[:, None] * din + (eta * ci - ct)[:, None] * nf
            dout = np.where(refl[:, None], drefl, dtran)
            dout /= np.linalg.norm(dout, axis=1)[:, None]
            inside[ii] = np.where(refl, ins, ~ins)
            o[ii] = p + dout * 1e-5; d[ii] = dout
        # PMMA bulk absorption is negligible over a few cm; ignored
    lr = np.concatenate(land_r) if land_r else np.zeros(0)
    lw = np.concatenate(land_w) if land_w else np.zeros(0)
    lxy = np.concatenate(land_xy) if land_xy else np.zeros((0, 2))
    ld = np.concatenate(land_d) if land_d else np.zeros((0, 3))
    return dict(r=lr, w=lw, xy=lxy, d=ld, glare=glare, spill=spill, lost=lost_abs + w[alive].sum(), n=n)


def profile(res, r0, r1, nb=30):
    """Irradiance per unit area (relative) in nb radial bins between r0 and r1."""
    edges = np.linspace(r0, r1, nb + 1)
    h, _ = np.histogram(res["r"], edges, weights=res["w"])
    area = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    E = h / area / res["n"]
    return 0.5 * (edges[1:] + edges[:-1]), E
