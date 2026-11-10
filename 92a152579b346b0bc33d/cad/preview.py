"""Clean PNG previews of CadQuery solids (matplotlib painter's-algorithm shading, no GPU needed)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

PALETTE = {
    "mdf": (0.30, 0.30, 0.32), "petg": (0.50, 0.55, 0.62), "steel": (0.62, 0.64, 0.66),
    "chrome": (0.80, 0.82, 0.85), "brass": (0.78, 0.62, 0.30), "black": (0.15, 0.15, 0.17),
    "vinyl": (0.12, 0.12, 0.14), "felt": (0.55, 0.50, 0.42), "led": (1.0, 0.78, 0.45),
    "alu": (0.70, 0.72, 0.74), "nut": (0.75, 0.75, 0.70), "plastic": (0.12, 0.12, 0.13),
}


def tess(shape, tol=0.12, ang=0.2):
    verts, tris = shape.tessellate(tol, ang)
    V = np.array([(v.x, v.y, v.z) for v in verts])
    F = np.array(tris, dtype=int)
    return V, F


def render(items, out, view=(30, -60), size=(1400, 1100), title=None, dpi=150, zoom=1.5, explode=None):
    """items: list of (cq_shape_or_workplane, color_key_or_rgb, alpha)."""
    fig = plt.figure(figsize=(size[0] / dpi, size[1] / dpi), dpi=dpi)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_proj_type("persp", focal_length=1.2)
    allV = []
    el0, az0 = np.radians(view[0]), np.radians(view[1])
    cam = np.array([np.cos(el0) * np.cos(az0), np.cos(el0) * np.sin(az0), np.sin(el0)])
    light = cam + np.array([0.3, -0.3, 0.5]); light /= np.linalg.norm(light)
    polys, cols = [], []
    for it in items:
        shape, color, alpha = (it + (1.0,))[:3]
        if hasattr(shape, "val"):
            shape = shape.val()
        base = np.array(PALETTE.get(color, color) if isinstance(color, str) else color)
        V, F = tess(shape)
        allV.append(V)
        P = V[F]
        n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
        nn = np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        n = n / nn
        lam = np.clip(n @ light, 0, 1)
        shade = 0.45 + 0.55 * lam
        spec = (np.clip(n @ light, 0, 1) ** 24) * 0.25
        c = np.clip(base[None, :] * shade[:, None] + spec[:, None], 0, 1)
        for tri, cc in zip(P, c):
            polys.append(tri)
            cols.append((*cc, alpha))
    polys = np.array(polys)
    cols = np.array(cols)
    # cull back faces, then painter's sort by depth along the view direction
    el, az = np.radians(view[0]), np.radians(view[1])
    d = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    fn = np.cross(polys[:, 1] - polys[:, 0], polys[:, 2] - polys[:, 0])
    keep = (fn @ d) > 0
    polys, cols = polys[keep], cols[keep]
    depth = polys.mean(axis=1) @ d
    order = np.argsort(depth)
    coll = Poly3DCollection(polys[order], facecolors=cols[order], edgecolors="none", linewidths=0)
    ax.add_collection3d(coll)
    allV = np.vstack(allV)
    c = (allV.max(0) + allV.min(0)) / 2
    r = (allV.max(0) - allV.min(0)).max() / 2 / zoom
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=view[0], azim=view[1])
    ax.set_axis_off()
    fig.patch.set_facecolor("white")
    if title:
        fig.text(0.02, 0.97, title, fontsize=10, family="monospace", va="top")
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(out, dpi=dpi, facecolor="white")
    plt.close(fig)
    return out
