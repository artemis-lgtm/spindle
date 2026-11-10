"""Record sconce: final product image set. CYCLES only, OIDN denoised.

Builds on render/sconce_v2.py (geometry, materials) and render/sconce.py (the hero
look Austin liked). Originals are untouched.

Usage:
  Blender -b -P final.py -- SCENE ASPECT [--samples N] [--preview] [--out file]
                                         [--pass full|ambient|halo] [--exr]
SCENE : hero_chrome hero_brass hero_black single7 set living bar studio bedroom
        macro swap1 swap2 swap3 flatlay darkroom
ASPECT: wide (1920x1080) | square (1600x1600) | tall (1080x1920)

World frame: wall face is y=0, room is +y, z is up. Sconce parts are lathed on
local Z inside an empty; on the wall that empty is rotated so local Z = world +Y
and local -Y = world up.
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector, Euler, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SCENE = argv[0] if argv else "hero_chrome"
ASPECT = argv[1] if len(argv) > 1 else "wide"
def opt(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
PREVIEW = "--preview" in argv
SAMPLES = int(opt("--samples", "24" if PREVIEW else "512"))
PASS = opt("--pass", "full")
EXR = "--exr" in argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
TEX = os.path.join(ROOT, "tex")
RES = dict(wide=(1920, 1080), square=(1600, 1600), tall=(1080, 1920))[ASPECT]
OUT = opt("--out", os.path.join(ROOT, "preview" if PREVIEW else "png", f"{SCENE}_{ASPECT}.png"))
random.seed(7)

IN = 0.0254
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
COL = scene.collection

# =============================================================== helpers
def smooth(ob, angle=50):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))

def link(ob, parent=None):
    COL.objects.link(ob)
    if parent:
        ob.parent = parent
    return ob

def lathe(name, profile, steps=192, mat=None, parent=None, z=0.0, sm=50):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0.0, zz)) for r, zz in profile]
    es = [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1), angle=2 * math.pi, steps=steps, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new(name, me), parent)
    ob.location = (0, 0, z)
    if sm:
        smooth(ob, sm)
    if mat:
        ob.data.materials.append(mat)
    return ob

def box(name, size, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, parent=None, bevel=0.0, seg=3):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new(name, me), parent)
    ob.location = loc; ob.rotation_euler = rot; ob.scale = size
    if bevel > 0:
        m = ob.modifiers.new("bev", "BEVEL")
        m.width = bevel; m.segments = seg; m.harden_normals = True
        m.use_clamp_overlap = True
        # bevel works in local (unit) space: compensate by applying scale first
        me.transform(Matrix.Diagonal((*size, 1)))
        ob.scale = (1, 1, 1)
        for p in me.polygons:
            p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    return ob

def cyl(name, r, depth, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, parent=None, verts=48, bevel=0.0):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=r, depth=depth)
    bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new(name, me), parent)
    ob.location = loc; ob.rotation_euler = rot
    if bevel:
        m = ob.modifiers.new("bev", "BEVEL"); m.width = bevel; m.segments = 3; m.harden_normals = True
        m.limit_method = "ANGLE"
        for p in me.polygons:
            p.use_smooth = True
    if mat:
        ob.data.materials.append(mat)
    return ob

def tube(name, pts, r, mat, parent=None, res=6):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = res; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for b, p in zip(sp.bezier_points, pts):
        b.co = p; b.handle_left_type = b.handle_right_type = "AUTO"
    ob = link(bpy.data.objects.new(name, cu), parent)
    ob.data.materials.append(mat)
    return ob

def empty(name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    e = link(bpy.data.objects.new(name, None), parent)
    e.location = loc; e.rotation_euler = rot
    return e

# =============================================================== node builder
class NB:
    def __init__(self, mat):
        mat.use_nodes = True
        self.nt = mat.node_tree; self.nt.nodes.clear()
        self.out = self.n("ShaderNodeOutputMaterial")
    def n(self, kind, **props):
        nd = self.nt.nodes.new(kind)
        for k, v in props.items():
            setattr(nd, k, v)
        return nd
    def link(self, a, b):
        self.nt.links.new(a, b)
    def math(self, op, a, b=None, clamp=False):
        m = self.n("ShaderNodeMath", operation=op, use_clamp=clamp)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            else:
                self.link(v, m.inputs[i])
        return m.outputs[0]
    def bsdf(self, **vals):
        p = self.n("ShaderNodeBsdfPrincipled")
        for k, v in vals.items():
            if isinstance(v, (int, float)):
                p.inputs[k].default_value = v
            elif isinstance(v, tuple):
                p.inputs[k].default_value = (*v, 1) if len(v) == 3 else v
            else:
                self.link(v, p.inputs[k])
        return p

def obj_xyz(nb):
    tc = nb.n("ShaderNodeTexCoord")
    sep = nb.n("ShaderNodeSeparateXYZ")
    nb.link(tc.outputs["Object"], sep.inputs[0])
    return sep.outputs[0], sep.outputs[1], sep.outputs[2], tc

def band(nb, r, lo, hi):
    return nb.math("MULTIPLY", nb.math("GREATER_THAN", r, lo), nb.math("LESS_THAN", r, hi))

_imgs = {}
def img(name, colorspace="sRGB"):
    if name not in _imgs:
        im = bpy.data.images.load(os.path.join(TEX, name + ".png"))
        im.colorspace_settings.name = colorspace
        _imgs[name] = im
    return _imgs[name]

# =============================================================== materials
_mc = {}
def cached(key, fn):
    if key not in _mc:
        _mc[key] = fn()
    return _mc[key]

def mat_simple(name, color, rough, metallic=0.0, sheen=0.0, bump_scale=None, bump_str=0.2, spec=0.5,
               coat=0.0, trans=0.0, ior=1.45, sss=0.0):
    m = bpy.data.materials.new(name)
    nb = NB(m)
    p = nb.bsdf(**{"Base Color": color, "Roughness": rough, "Metallic": metallic, "Sheen Weight": sheen,
                   "Sheen Roughness": 0.6, "Specular IOR Level": spec, "Coat Weight": coat,
                   "Transmission Weight": trans, "IOR": ior, "Subsurface Weight": sss})
    if bump_scale:
        nz = nb.n("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = bump_scale; nz.inputs["Detail"].default_value = 8
        b = nb.n("ShaderNodeBump"); b.inputs["Strength"].default_value = bump_str
        nb.link(nz.outputs[0], b.inputs["Height"]); nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_plaster(name, color, var=0.06, scale=3.0):
    """Painted plaster: low-frequency tone variation + fine trowel bump."""
    m = bpy.data.materials.new(name)
    nb = NB(m)
    x, y, z, tc = obj_xyz(nb)
    big = nb.n("ShaderNodeTexNoise"); big.inputs["Scale"].default_value = scale; big.inputs["Detail"].default_value = 4
    nb.link(tc.outputs["Object"], big.inputs[0])
    c = nb.n("ShaderNodeMix", data_type="RGBA")
    c.inputs[6].default_value = (*[v * (1 - var) for v in color], 1)
    c.inputs[7].default_value = (*[min(1, v * (1 + var)) for v in color], 1)
    nb.link(big.outputs[0], c.inputs[0])
    fine = nb.n("ShaderNodeTexNoise"); fine.inputs["Scale"].default_value = 140; fine.inputs["Detail"].default_value = 10
    nb.link(tc.outputs["Object"], fine.inputs[0])
    b = nb.n("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.05
    nb.link(fine.outputs[0], b.inputs["Height"])
    p = nb.bsdf(**{"Roughness": 0.88, "Specular IOR Level": 0.25})
    nb.link(c.outputs[2], p.inputs["Base Color"]); nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_vinyl(label, label_r, groove_lo, groove_hi, gaps, spin=0.0):
    m = bpy.data.materials.new("Vinyl_" + label)
    nb = NB(m)
    x, y, z, tc = obj_xyz(nb)
    r = nb.math("SQRT", nb.math("ADD", nb.math("MULTIPLY", x, x), nb.math("MULTIPLY", y, y)))
    grooved = band(nb, r, groove_lo, groove_hi)
    gp = None
    for ri in gaps:
        g = nb.math("COMPARE", r, ri); g.node.inputs[2].default_value = 0.0009
        gp = g if gp is None else nb.math("MAXIMUM", gp, g)
    music = nb.math("MULTIPLY", grooved, nb.math("SUBTRACT", 1.0, gp)) if gp else grooved
    mod = nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0041))
    h = nb.math("MULTIPLY", music, nb.math("MULTIPLY", mod, 0.3))
    runout = band(nb, r, label_r + 0.0005, groove_lo)
    ro = nb.math("MULTIPLY", runout, nb.math("GREATER_THAN",
                 nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0021)), 0.93))
    h = nb.math("ADD", h, nb.math("MULTIPLY", ro, -1.0))
    bump = nb.n("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.18
    bump.inputs["Distance"].default_value = 0.00002
    nb.link(h, bump.inputs["Height"])
    noise = nb.n("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 900
    rough = nb.math("ADD", nb.math("MULTIPLY", music, 0.05), 0.035)
    rough = nb.math("ADD", rough, nb.math("MULTIPLY", noise.outputs[0], 0.015))
    tan = nb.n("ShaderNodeTangent", direction_type="RADIAL", axis="Z")
    vin = nb.bsdf(**{"Base Color": (0.006, 0.006, 0.007), "Roughness": rough, "Specular IOR Level": 0.55})
    nb.link(nb.math("ADD", nb.math("MULTIPLY", music, 0.6), 0.1), vin.inputs["Anisotropic"])
    nb.link(tan.outputs[0], vin.inputs["Tangent"]); nb.link(bump.outputs[0], vin.inputs["Normal"])
    # printed paper label
    mp = nb.n("ShaderNodeMapping")
    mp.inputs["Location"].default_value = (0.5, 0.5, 0)
    mp.inputs["Rotation"].default_value = (0, 0, spin)
    mp.inputs["Scale"].default_value = (-1 / (2 * label_r), -1 / (2 * label_r), 1)
    nb.link(tc.outputs["Object"], mp.inputs[0])
    # mapping applies scale then rotation: rotate in object space first via a 2nd mapping
    tex = nb.n("ShaderNodeTexImage"); tex.image = img(label); tex.extension = "EXTEND"
    nb.link(mp.outputs[0], tex.inputs[0])
    ln = nb.n("ShaderNodeTexNoise"); ln.inputs["Scale"].default_value = 4000; ln.inputs["Detail"].default_value = 6
    lb = nb.n("ShaderNodeBump"); lb.inputs["Strength"].default_value = 0.10
    nb.link(ln.outputs[0], lb.inputs["Height"])
    lab = nb.bsdf(**{"Roughness": 0.55, "Specular IOR Level": 0.35})
    nb.link(tex.outputs[0], lab.inputs["Base Color"]); nb.link(lb.outputs[0], lab.inputs["Normal"])
    mix = nb.n("ShaderNodeMixShader")
    nb.link(nb.math("LESS_THAN", r, label_r), mix.inputs[0])
    nb.link(vin.outputs[0], mix.inputs[1]); nb.link(lab.outputs[0], mix.inputs[2])
    nb.link(mix.outputs[0], nb.out.inputs[0])
    return m

def mat_chrome():
    m = bpy.data.materials.new("Chrome"); nb = NB(m)
    p = nb.bsdf(**{"Base Color": (0.93, 0.93, 0.94), "Metallic": 1.0, "Roughness": 0.03})
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def mat_gloss_black():
    m = bpy.data.materials.new("GlossBlack"); nb = NB(m)
    p = nb.bsdf(**{"Base Color": (0.10, 0.10, 0.11), "Metallic": 1.0, "Roughness": 0.04,
                   "Coat Weight": 1.0, "Coat Roughness": 0.02})
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def mat_brass(brushed=True):
    m = bpy.data.materials.new("Brass"); nb = NB(m)
    noise = nb.n("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 300
    base = 0.13 if brushed else 0.05
    rough = nb.math("ADD", nb.math("MULTIPLY", noise.outputs[0], 0.03), base)
    p = nb.bsdf(**{"Base Color": (0.90, 0.66, 0.34), "Metallic": 1.0, "Roughness": rough,
                   "Anisotropic": 0.6 if brushed else 0.2})
    tan = nb.n("ShaderNodeTangent", direction_type="RADIAL", axis="Z")
    nb.link(tan.outputs[0], p.inputs["Tangent"]); nb.link(p.outputs[0], nb.out.inputs[0]); return m

LED_STRENGTH = float(opt("--led", "70"))
SIDE_K = float(opt("--side", "0.25"))
REAR_K = float(opt("--rear", "0.45"))
def mat_led(bp_r, z0, z1, k=1.0, uniform=False):
    m = bpy.data.materials.new("LED"); nb = NB(m)
    if uniform:
        em = nb.n("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.42, 0.10, 1)
        em.inputs["Strength"].default_value = LED_STRENGTH * k if PASS != "ambient" else 0.0
        nb.link(em.outputs[0], nb.out.inputs[0]); return m
    x, y, z, tc = obj_xyz(nb)
    a = nb.math("ARCTAN2", y, x)
    n_led = round(2 * math.pi * bp_r * 60)
    dot = nb.math("GREATER_THAN", nb.math("SINE", nb.math("MULTIPLY", a, n_led)), 0.55)
    dot = nb.math("MULTIPLY", dot, band(nb, z, z0, z1))
    em = nb.n("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.42, 0.10, 1)
    s = LED_STRENGTH * k if PASS != "ambient" else 0.0
    nb.link(nb.math("ADD", nb.math("MULTIPLY", dot, s), s * 0.25), em.inputs["Strength"])
    pcb = nb.bsdf(**{"Base Color": (0.85, 0.83, 0.78), "Roughness": 0.4})
    add = nb.n("ShaderNodeAddShader")
    nb.link(pcb.outputs[0], add.inputs[0]); nb.link(em.outputs[0], add.inputs[1])
    nb.link(add.outputs[0], nb.out.inputs[0]); return m

def mat_wood(name, c1, c2, scale=8.0, rough=0.45, stretch=0.08, axis="X", coat=0.3):
    """Walnut/oak: stretched noise grain along an object axis."""
    m = bpy.data.materials.new(name); nb = NB(m)
    tc = nb.n("ShaderNodeTexCoord"); mp = nb.n("ShaderNodeMapping")
    s = {"X": (stretch, 1, 1), "Y": (1, stretch, 1), "Z": (1, 1, stretch)}[axis]
    mp.inputs["Scale"].default_value = s
    nb.link(tc.outputs["Object"], mp.inputs[0])
    w = nb.n("ShaderNodeTexWave"); w.inputs["Scale"].default_value = scale
    w.inputs["Distortion"].default_value = 8; w.inputs["Detail"].default_value = 4
    w.wave_type = "BANDS"
    w.bands_direction = {"X": "X", "Y": "Y", "Z": "Z"}["Y" if axis == "X" else "X"]
    nb.link(mp.outputs[0], w.inputs[0])
    nz = nb.n("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 30; nz.inputs["Detail"].default_value = 6
    nb.link(mp.outputs[0], nz.inputs[0])
    f = nb.math("ADD", nb.math("MULTIPLY", w.outputs[1], 0.6), nb.math("MULTIPLY", nz.outputs[0], 0.4))
    c = nb.n("ShaderNodeMix", data_type="RGBA")
    c.inputs[6].default_value = (*c1, 1); c.inputs[7].default_value = (*c2, 1)
    nb.link(f, c.inputs[0])
    b = nb.n("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.05
    nb.link(f, b.inputs["Height"])
    p = nb.bsdf(**{"Roughness": rough, "Coat Weight": coat, "Coat Roughness": 0.15, "Specular IOR Level": 0.4})
    nb.link(c.outputs[2], p.inputs["Base Color"]); nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def walnut():
    return cached("walnut", lambda: mat_wood("Walnut", (0.10, 0.055, 0.03), (0.22, 0.12, 0.065), coat=0.35))
def oak():
    return cached("oak", lambda: mat_wood("Oak", (0.42, 0.28, 0.16), (0.62, 0.45, 0.28), rough=0.5, coat=0.15))

def mat_planks(name, c1, c2):
    m = bpy.data.materials.new(name); nb = NB(m)
    tc = nb.n("ShaderNodeTexCoord")
    br = nb.n("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.002
    br.inputs["Brick Width"].default_value = 1.4; br.inputs["Row Height"].default_value = 0.14
    br.inputs["Color1"].default_value = (*c1, 1); br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (0.04, 0.03, 0.02, 1)
    br.offset = 0.37
    nb.link(tc.outputs["Object"], br.inputs[0])
    mp = nb.n("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.06, 1, 1)
    nb.link(tc.outputs["Object"], mp.inputs[0])
    w = nb.n("ShaderNodeTexNoise"); w.inputs["Scale"].default_value = 40; w.inputs["Detail"].default_value = 8
    nb.link(mp.outputs[0], w.inputs[0])
    c = nb.n("ShaderNodeMix", data_type="RGBA"); c.blend_type = "MULTIPLY"
    c.inputs[0].default_value = 0.5
    nb.link(br.outputs[0], c.inputs[6]); nb.link(w.outputs[1], c.inputs[7])
    b = nb.n("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.2
    nb.link(br.outputs[1], b.inputs["Height"])
    p = nb.bsdf(**{"Roughness": 0.38, "Coat Weight": 0.2, "Specular IOR Level": 0.45})
    nb.link(c.outputs[2], p.inputs["Base Color"]); nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def mat_fabric(name, color, scale=600, rough=0.9, sheen=0.4):
    m = bpy.data.materials.new(name); nb = NB(m)
    tc = nb.n("ShaderNodeTexCoord")
    wv = nb.n("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = scale
    wv2 = nb.n("ShaderNodeTexWave"); wv2.inputs["Scale"].default_value = scale; wv2.bands_direction = "Y"
    nb.link(tc.outputs["Object"], wv.inputs[0]); nb.link(tc.outputs["Object"], wv2.inputs[0])
    nz = nb.n("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 25
    nb.link(tc.outputs["Object"], nz.inputs[0])
    h = nb.math("ADD", nb.math("MULTIPLY", wv.outputs[0], wv2.outputs[0]), nb.math("MULTIPLY", nz.outputs[0], 0.5))
    b = nb.n("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.25
    nb.link(h, b.inputs["Height"])
    cm = nb.n("ShaderNodeMix", data_type="RGBA")
    cm.inputs[6].default_value = (*[v * 0.85 for v in color], 1); cm.inputs[7].default_value = (*color, 1)
    nb.link(nz.outputs[0], cm.inputs[0])
    p = nb.bsdf(**{"Roughness": rough, "Sheen Weight": sheen, "Sheen Roughness": 0.5, "Specular IOR Level": 0.2})
    nb.link(cm.outputs[2], p.inputs["Base Color"]); nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def mat_leaf(color=(0.05, 0.16, 0.035)):
    m = bpy.data.materials.new("Leaf"); nb = NB(m)
    nz = nb.n("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 30
    cm = nb.n("ShaderNodeMix", data_type="RGBA")
    cm.inputs[6].default_value = (*color, 1); cm.inputs[7].default_value = (color[0] * 1.6, color[1] * 1.3, color[2] * 0.9, 1)
    nb.link(nz.outputs[0], cm.inputs[0])
    p = nb.bsdf(**{"Roughness": 0.38, "Specular IOR Level": 0.5})
    nb.link(cm.outputs[2], p.inputs["Base Color"])
    tr = nb.n("ShaderNodeBsdfTranslucent")
    nb.link(cm.outputs[2], tr.inputs[0])
    mx = nb.n("ShaderNodeMixShader"); mx.inputs[0].default_value = 0.25
    nb.link(p.outputs[0], mx.inputs[1]); nb.link(tr.outputs[0], mx.inputs[2])
    nb.link(mx.outputs[0], nb.out.inputs[0]); return m

def mat_glass(tint=(0.95, 0.97, 0.96), rough=0.0):
    m = bpy.data.materials.new("Glass"); nb = NB(m)
    p = nb.bsdf(**{"Base Color": tint, "Transmission Weight": 1.0, "Roughness": rough, "IOR": 1.5})
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def mat_liquid(color):
    m = bpy.data.materials.new("Liquid"); nb = NB(m)
    p = nb.bsdf(**{"Base Color": color, "Transmission Weight": 1.0, "Roughness": 0.0, "IOR": 1.36})
    nb.link(p.outputs[0], nb.out.inputs[0]); return m

def mat_emit(name, color, strength):
    m = bpy.data.materials.new(name); nb = NB(m)
    em = nb.n("ShaderNodeEmission"); em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength if PASS != "halo" else 0.0
    nb.link(em.outputs[0], nb.out.inputs[0]); return m

def mat_image(name, image, rough=0.6, colorspace="sRGB"):
    m = bpy.data.materials.new(name); nb = NB(m)
    tc = nb.n("ShaderNodeTexCoord")
    t = nb.n("ShaderNodeTexImage"); t.image = img(image, colorspace)
    nb.link(tc.outputs["UV"], t.inputs[0])
    p = nb.bsdf(**{"Roughness": rough, "Specular IOR Level": 0.3})
    nb.link(t.outputs[0], p.inputs["Base Color"]); nb.link(p.outputs[0], nb.out.inputs[0]); return m

def M_(key):
    table = dict(
        chrome=mat_chrome, black_gloss=mat_gloss_black, brass=lambda: mat_brass(True),
        brass_pol=lambda: mat_brass(False),
        bp=lambda: mat_simple("BackplatePaint", (0.03, 0.03, 0.032), 0.75, spec=0.25, bump_scale=2500, bump_str=0.05),
        hub=lambda: mat_simple("HubPETG", (0.04, 0.04, 0.045), 0.55, spec=0.4),
        felt=lambda: mat_simple("Felt", (0.085, 0.012, 0.012), 1.0, sheen=0.15, spec=0.1, bump_scale=6000, bump_str=0.4),
        black=lambda: mat_simple("Black", (0.02, 0.02, 0.02), 0.5),
        black_plastic=lambda: mat_simple("BlackPlastic", (0.015, 0.015, 0.016), 0.35, spec=0.5),
        steel=lambda: mat_simple("ZincSteel", (0.55, 0.57, 0.6), 0.32, metallic=1.0, bump_scale=400, bump_str=0.05),
        alu=lambda: mat_simple("Alu", (0.8, 0.8, 0.82), 0.22, metallic=1.0),
        rubber=lambda: mat_simple("Rubber", (0.02, 0.02, 0.02), 0.7),
        white=lambda: mat_simple("WhitePlastic", (0.88, 0.88, 0.86), 0.35),
        ceramic=lambda: mat_simple("Ceramic", (0.80, 0.76, 0.70), 0.3, coat=0.3),
        paper=lambda: mat_simple("Paper", (0.82, 0.80, 0.75), 0.8, spec=0.2),
        leaf=mat_leaf, gold=lambda: mat_simple("GoldFrame", (0.78, 0.58, 0.30), 0.25, metallic=1.0),
        glass=mat_glass, soil=lambda: mat_simple("Soil", (0.05, 0.035, 0.025), 0.95, bump_scale=200, bump_str=0.6),
    )
    return cached(key, table[key])

def cap_mats(cap):
    return {"chrome": (M_("chrome"), M_("chrome")), "brass": (M_("brass"), M_("brass")),
            "black": (M_("black_gloss"), M_("chrome"))}[cap]

# =============================================================== the sconce
def dome_cap(parent, cap, z, dome_r=0.0191, dome_h=0.0105, rim_r=0.0201, rim_h=0.0016, post=0.020, name="DomeCap"):
    """Low segment-of-sphere dome (1.5 in) on a thin bezel, 1/4-20 post behind."""
    sph_R = (dome_r ** 2 + dome_h ** 2) / (2 * dome_h)
    sph_c = rim_h + dome_h - sph_R
    prof = [(0.0001, -post), (0.0030, -post), (0.0032, -post + 0.0006), (0.0032, 0.0),
            (rim_r - 0.0004, 0.0), (rim_r, 0.0004), (rim_r, rim_h - 0.0004), (rim_r - 0.0004, rim_h),
            (dome_r + 0.0002, rim_h), (dome_r, rim_h + 0.0002)]
    a0 = math.asin(max(-1, min(1, (rim_h + 0.0002 - sph_c) / sph_R)))
    for i in range(1, 41):
        a = a0 + (math.pi / 2 - a0) * i / 40
        prof.append((max(sph_R * math.cos(a), 0.00005), sph_c + sph_R * math.sin(a)))
    c = lathe(name, prof, steps=256, parent=parent, z=z, sm=40)
    dm, rm = cap_mats(cap)
    c.data.materials.append(dm); c.data.materials.append(rm)
    for poly in c.data.polygons:
        zc = sum(c.data.vertices[v].co.z for v in poly.vertices) / len(poly.vertices)
        poly.material_index = 1 if zc < rim_h + 0.0001 else 0
    return c

def adapter45_cap(parent, cap, z, name="Cap45"):
    """7 in cap: a chromed 45 adapter (plain ring) with a small jewel dome at its centre."""
    prof = [(0.0001, -0.018), (0.0030, -0.018), (0.0032, -0.0175), (0.0032, -0.0019),
            (0.0188, -0.0019), (0.0188, 0.0), (0.0244, 0.0), (0.0250, 0.0006), (0.0250, 0.0020),
            (0.0243, 0.0028), (0.0200, 0.0034), (0.0170, 0.0030), (0.0160, 0.0034), (0.0130, 0.0040),
            (0.0112, 0.0042)]
    for i in range(1, 21):   # small dome r=11mm h=5mm
        a = math.pi / 2 * i / 20
        prof.append((max(0.0112 * math.cos(a), 0.00005), 0.0042 + 0.0052 * math.sin(a)))
    c = lathe(name, prof, steps=256, parent=parent, z=z, sm=35)
    dm, rm = cap_mats(cap)
    c.data.materials.append(dm)
    return c

SPEC = {
    "12": dict(rec_r=6 * IN, hole_r=0.00362, label_r=0.0505, groove=(0.0605, 0.1462),
               gaps=(0.0742, 0.0893, 0.1031, 0.1158, 0.1305), bp_r=5.25 * IN, hub_r=2.5 * IN),
    "7": dict(rec_r=3.5 * IN, hole_r=0.01905, label_r=0.0435, groove=(0.0490, 0.0855),
              gaps=(0.0650,), bp_r=3.0 * IN, hub_r=1.5 * IN),
}
HUB_T, BP_T, SO_T, REC_T, WASH_T = 1.0 * IN, 0.0127, 0.004, 0.0019, 0.0022

def record(parent, size, label, z=0.0, spin=0.0, name="Record"):
    s = SPEC[size]
    R, L, H = s["rec_r"], s["label_r"], s["hole_r"]
    lo, hi = s["groove"]
    prof = [(H, 0.0), (R - 0.0005, 0.0), (R, 0.0004), (R, 0.0013), (R - 0.0006, 0.0018),
            (R - 0.0034, 0.0017), (hi + 0.0003, 0.0015), (lo, 0.0015), (lo - 0.005, 0.0016),
            (L + 0.001, 0.0018), (L, REC_T), (H + 0.0002, REC_T), (H, REC_T - 0.0002)]
    rec = lathe(name, prof, steps=384, parent=parent, z=z)
    rec.data.materials.append(mat_vinyl(label, L, lo, hi, s["gaps"], spin))
    return rec

def sconce(name, size="12", cap="chrome", label="label_halo", loc=(0, 0, 0), parent=None, wall=True,
           rec_off=(0, 0, 0), rec_tilt=0.0, cap_off=(0, 0, 0), wash_off=(0, 0, 0), spin=None,
           show_record=True, show_cap=True):
    """Builds hub + backplate + LED ring + pads + record + washer + cap. Offsets are in
    the sconce's local frame (x right-ish, -y up, z out of wall)."""
    s = SPEC[size]
    root = empty(name, loc, (-math.pi / 2, 0, 0) if wall else (0, 0, 0), parent)
    bev = 0.0012
    hub = lathe(name + "_hub", [(0.0001, 0.0), (s["hub_r"] - bev, 0), (s["hub_r"], bev), (s["hub_r"], HUB_T - bev),
                                (s["hub_r"] - bev, HUB_T), (0.0001, HUB_T)], parent=root, mat=M_("hub"))
    bpr = s["bp_r"]
    bp = lathe(name + "_bp", [(0.0050, 0.0), (bpr - bev, 0.0), (bpr, bev), (bpr, BP_T - bev), (bpr - bev, BP_T),
                              (0.0050, BP_T)], parent=root, z=HUB_T, mat=M_("bp"))
    lathe(name + "_led", [(bpr - 0.0002, 0.0030), (bpr + 0.0008, 0.0030), (bpr + 0.0008, 0.0100),
                          (bpr - 0.0002, 0.0100)], parent=root, z=HUB_T, mat=mat_led(bpr, 0.0032, 0.0098, SIDE_K))
    # rear-facing COB ring just inside the rim, aimed at the wall: this is what draws the tight halo
    lathe(name + "_cob", [(bpr - 0.014, -0.0012), (bpr - 0.004, -0.0012), (bpr - 0.004, 0.0), (bpr - 0.014, 0.0)],
          parent=root, z=HUB_T, mat=mat_led(bpr, -1, 1, REAR_K, uniform=True), sm=0)
    lathe(name + "_insert", [(0.0032, 0.0), (0.0050, 0.0), (0.0050, BP_T + 0.0004), (0.0032, BP_T + 0.0004)],
          steps=48, parent=root, z=HUB_T, mat=M_("brass_pol"))
    pads = [(bpr - 0.012, 3), (bpr * 0.55, 3)] if size == "12" else [(bpr - 0.010, 3)]
    for rr, n in pads:
        for i in range(n):
            a = math.radians(-90 + 120 * i + (60 if rr < bpr * 0.6 else 0))
            p = cyl(name + "_pad", 0.00635, SO_T, loc=(rr * math.cos(a), rr * math.sin(a), HUB_T + BP_T + SO_T / 2),
                    mat=M_("felt"), parent=root, verts=24)
    rz = HUB_T + BP_T + SO_T
    rec = None
    if show_record:
        sp = random.uniform(0, 2 * math.pi) if spin is None else spin
        rec = record(root, size, label, z=rz, spin=sp, name=name + "_rec")
        rec.location = (rec_off[0], rec_off[1], rz + rec_off[2])
        rec.rotation_euler = (rec_tilt, 0, 0)
    capz = rz + REC_T
    if size == "12":
        wa = lathe(name + "_wash", [(0.0036, 0.0), (0.0210, 0.0), (0.0212, WASH_T * 0.5), (0.0210, WASH_T),
                                    (0.0036, WASH_T)], steps=128, parent=root, mat=M_("felt"))
        wa.location = (wash_off[0], wash_off[1], capz + wash_off[2])
        if show_cap:
            c = dome_cap(root, cap, capz + WASH_T, name=name + "_cap")
            c.location = (cap_off[0], cap_off[1], capz + WASH_T + cap_off[2])
    else:
        if show_cap:
            c = adapter45_cap(root, cap, capz, name=name + "_cap")
            c.location = (cap_off[0], cap_off[1], capz + cap_off[2])
    return root

# =============================================================== props
def leaf_mesh(name, L=0.08, W=0.055, fold=0.25, bend=0.2):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    NS, NW = 14, 6
    grid = []
    for i in range(NS + 1):
        s = i / NS
        # heart-ish: wide near the base, pointed tip
        hw = W * 0.5 * (math.sin(math.pi * min(1, s * 1.15) ** 0.75) * (1 - 0.15 * s)) if s < 0.98 else 0.0
        if s < 0.12:
            hw = W * 0.5 * (0.55 + 3.5 * s)
        row = []
        for j in range(-NW, NW + 1):
            x = hw * j / NW
            zz = fold * abs(x) - bend * L * s * s
            row.append(bm.verts.new((x, s * L, zz)))
        grid.append(row)
    for i in range(NS):
        for j in range(2 * NW):
            bm.faces.new((grid[i][j], grid[i][j + 1], grid[i + 1][j + 1], grid[i + 1][j]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = link(bpy.data.objects.new(name, me))
    ob.data.materials.append(M_("leaf"))
    m = ob.modifiers.new("solid", "SOLIDIFY"); m.thickness = 0.0006
    return ob

def vine(pts, n=26, size=(0.05, 0.085), seed=1):
    """Trailing pothos: a stem curve with alternating leaves."""
    rnd = random.Random(seed)
    tube("VineStem", pts, 0.0018, M_("leaf"))
    # sample the polyline
    segs = [(Vector(pts[i]), Vector(pts[i + 1])) for i in range(len(pts) - 1)]
    total = sum((b - a).length for a, b in segs)
    for k in range(n):
        t = (k + 0.5) / n * total
        for a, b in segs:
            l = (b - a).length
            if t <= l:
                p = a + (b - a) * (t / l); d = (b - a).normalized(); break
            t -= l
        L = rnd.uniform(*size)
        lf = leaf_mesh("Leaf", L=L, W=L * 0.75, fold=0.3, bend=rnd.uniform(0.1, 0.35))
        side = 1 if k % 2 else -1
        lf.location = p + Vector((side * 0.006, rnd.uniform(0.0, 0.02), 0))
        lf.rotation_euler = (rnd.uniform(-0.6, 0.4) + math.radians(-60), rnd.uniform(-0.5, 0.5),
                             side * rnd.uniform(0.5, 1.3) + rnd.uniform(-0.3, 0.3))

def pot(loc, r=0.11, h=0.20, mat=None):
    prof = [(0.0001, 0), (r * 0.78, 0), (r, h * 0.9), (r * 1.04, h), (r * 0.95, h), (r * 0.9, h * 0.92),
            (0.0001, h * 0.92)]
    p = lathe("Pot", prof, steps=96, mat=mat or M_("ceramic"))
    p.location = loc
    cyl("Soil", r * 0.88, 0.004, loc=(loc[0], loc[1], loc[2] + h * 0.88), mat=M_("soil"))
    return p

def snake_plant(loc, n=9, H=0.75, seed=3):
    rnd = random.Random(seed)
    pot(loc, 0.13, 0.26)
    m = cached("snakeleaf", lambda: mat_leaf((0.035, 0.11, 0.04)))
    for k in range(n):
        h = H * rnd.uniform(0.6, 1.0); w = rnd.uniform(0.04, 0.06)
        me = bpy.data.meshes.new("blade"); bm = bmesh.new()
        rows = []
        for i in range(11):
            s = i / 10
            hw = w * 0.5 * (math.sin(math.pi * (0.25 + 0.75 * s)) if s < 0.95 else 0.02) * (1.2 - 0.4 * s)
            tw = s * rnd.uniform(-0.6, 0.6)
            row = [bm.verts.new((x * math.cos(tw), x * math.sin(tw) + 0.012 * abs(x) / max(w, 1e-4) * 0, s * h))
                   for x in (-hw, -hw * 0.5, 0, hw * 0.5, hw)]
            row[2].co.y += 0.004
            rows.append(row)
        for i in range(10):
            for j in range(4):
                bm.faces.new((rows[i][j], rows[i][j + 1], rows[i + 1][j + 1], rows[i + 1][j]))
        bm.to_mesh(me); bm.free()
        for p in me.polygons:
            p.use_smooth = True
        ob = link(bpy.data.objects.new("Blade", me)); ob.data.materials.append(m)
        ob.modifiers.new("s", "SOLIDIFY").thickness = 0.002
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0.01, 0.07)
        ob.location = (loc[0] + rr * math.cos(a), loc[1] + rr * math.sin(a), loc[2] + 0.22)
        ob.rotation_euler = (rnd.uniform(-0.18, 0.18), rnd.uniform(-0.18, 0.18), rnd.uniform(0, math.pi))

def picture_frame(x0, x1, z0, z1, y=0.0, art=(0.45, 0.30, 0.22), frame="gold"):
    t, d = 0.025, 0.03
    fm = M_("gold") if frame == "gold" else cached("frameblack", lambda: mat_simple("FrameBlack", (0.02, 0.02, 0.02), 0.4))
    cx = (x0 + x1) / 2; cz = (z0 + z1) / 2
    box("FrameT", (x1 - x0, d, t), (cx, y + d / 2, z1 - t / 2), mat=fm, bevel=0.003)
    box("FrameB", (x1 - x0, d, t), (cx, y + d / 2, z0 + t / 2), mat=fm, bevel=0.003)
    box("FrameL", (t, d, z1 - z0), (x0 + t / 2, y + d / 2, cz), mat=fm, bevel=0.003)
    box("FrameR", (t, d, z1 - z0), (x1 - t / 2, y + d / 2, cz), mat=fm, bevel=0.003)
    am = cached("art" + str(art), lambda: mat_plaster("Art", art, var=0.35, scale=6))
    box("Art", (x1 - x0 - 2 * t, 0.004, z1 - z0 - 2 * t), (cx, y + d * 0.4, cz), mat=am)

def sleeve_mat(rnd):
    pal = [(0.55, 0.12, 0.08), (0.08, 0.18, 0.30), (0.75, 0.62, 0.40), (0.10, 0.10, 0.10), (0.70, 0.68, 0.62),
           (0.20, 0.32, 0.22), (0.62, 0.38, 0.12), (0.35, 0.22, 0.30), (0.85, 0.82, 0.74), (0.15, 0.25, 0.40)]
    c = rnd.choice(pal)
    return cached("sleeve" + str(c), lambda: mat_simple("Sleeve", c, 0.6, spec=0.3, bump_scale=300, bump_str=0.05))

def record_row(x0, x1, y0, depth, z0, rnd, lean=0.0):
    """Sleeves standing on edge in a cube (spines face +y)."""
    x = x0
    while x < x1 - 0.004:
        t = rnd.uniform(0.0035, 0.007)
        tilt = lean + rnd.uniform(-0.03, 0.03)
        box("Sleeve", (t, depth, 0.315), (x + t / 2, y0 + depth / 2, z0 + 0.1575), rot=(0, tilt, 0),
            mat=sleeve_mat(rnd), bevel=0.0008, seg=1)
        x += t + rnd.uniform(0.0, 0.0012)

def credenza(x0, x1, y0, depth, top_z, floor_z, legs=0.14, mat=None):
    mat = mat or walnut()
    h = top_z - floor_z - legs
    cx = (x0 + x1) / 2
    box("CredBody", (x1 - x0, depth, h), (cx, y0 + depth / 2, floor_z + legs + h / 2), mat=mat, bevel=0.006)
    n = max(2, round((x1 - x0) / 0.45))
    w = (x1 - x0 - 0.02) / n
    for i in range(n):
        xc = x0 + 0.01 + w * (i + 0.5)
        box("CredDoor", (w - 0.006, 0.006, h - 0.03), (xc, y0 + depth + 0.002, floor_z + legs + h / 2), mat=mat, bevel=0.002)
        box("CredPull", (0.006, 0.012, 0.09), (xc + w / 2 - 0.04, y0 + depth + 0.009, floor_z + legs + h * 0.62),
            mat=M_("brass_pol"), bevel=0.002)
    for lx in (x0 + 0.05, x1 - 0.05):
        for ly in (y0 + 0.05, y0 + depth - 0.05):
            lathe("Leg", [(0.0001, 0), (0.012, 0), (0.019, legs), (0.0001, legs)], steps=24, mat=mat).location = (lx, ly, floor_z)

def turntable(cx, cy, top, label="label_sunroom"):
    plinth = walnut()
    box("TTPlinth", (0.45, 0.36, 0.07), (cx, cy, top + 0.035 + 0.012), mat=plinth, bevel=0.005)
    for fx in (-0.19, 0.19):
        for fy in (-0.15, 0.15):
            cyl("TTFoot", 0.018, 0.012, loc=(cx + fx, cy + fy, top + 0.006), mat=M_("alu"))
    pz = top + 0.082
    lathe("Platter", [(0.0001, 0), (0.150, 0), (0.151, 0.0015), (0.151, 0.016), (0.149, 0.0175), (0.0001, 0.0175)],
          steps=192, mat=M_("alu")).location = (cx - 0.04, cy, pz)
    rec = record(empty("TTRec", (cx - 0.04, cy, pz + 0.018)), "12", label, spin=1.0)
    cyl("Spindle", 0.0035, 0.02, loc=(cx - 0.04, cy, pz + 0.025), mat=M_("chrome"))
    bx, by = cx + 0.17, cy + 0.11
    cyl("ArmBase", 0.022, 0.03, loc=(bx, by, pz + 0.005), mat=M_("alu"), bevel=0.002)
    tube("Tonearm", [(bx, by, pz + 0.03), (bx - 0.05, by - 0.10, pz + 0.032), (bx - 0.12, by - 0.17, pz + 0.03)],
         0.0035, M_("alu"))
    box("Headshell", (0.03, 0.018, 0.006), (bx - 0.135, by - 0.18, pz + 0.027), rot=(0, 0, 0.8), mat=M_("black"), bevel=0.001)
    cyl("Counterweight", 0.014, 0.025, loc=(bx + 0.03, by + 0.05, pz + 0.032), rot=(math.pi / 2, 0, 0.5), mat=M_("alu"))
    cyl("Knob", 0.012, 0.012, loc=(cx - 0.19, cy + 0.17, pz - 0.02), rot=(math.pi / 2, 0, 0), mat=M_("alu"))

def speaker(cx, cy, z, w=0.20, d=0.24, h=0.32, mat=None, front=(0.02, 0.02, 0.02)):
    box("Spk", (w, d, h), (cx, cy, z + h / 2), mat=mat or walnut(), bevel=0.006)
    fm = cached("spkfront" + str(front), lambda: mat_fabric("SpkFront", front, scale=900))
    box("SpkFront", (w - 0.012, 0.004, h - 0.012), (cx, cy + d / 2 + 0.001, z + h / 2), mat=fm, bevel=0.002)
    for zz, rr in ((z + h * 0.36, 0.062), (z + h * 0.78, 0.020)):
        c = lathe("Driver", [(0.0001, -0.010), (rr * 0.5, -0.006), (rr, 0.0), (rr + 0.006, 0.002), (rr + 0.006, 0.0),
                             (0.0001, 0.0)], steps=64, mat=M_("black_plastic"))
        c.location = (cx, cy + d / 2 + 0.004, zz); c.rotation_euler = (-math.pi / 2, 0, 0)

def bottle(loc, kind, liquid, rnd):
    if kind == 0:   # whisky square-ish shoulder (round approximation)
        prof = [(0.0001, 0), (0.040, 0), (0.042, 0.004), (0.042, 0.20), (0.030, 0.235), (0.013, 0.25), (0.013, 0.30),
                (0.015, 0.302), (0.015, 0.31), (0.0001, 0.31)]
    elif kind == 1:  # gin tall
        prof = [(0.0001, 0), (0.036, 0), (0.038, 0.004), (0.038, 0.24), (0.020, 0.28), (0.012, 0.29), (0.012, 0.33),
                (0.0001, 0.33)]
    else:            # decanter round
        prof = [(0.0001, 0), (0.035, 0), (0.055, 0.06), (0.058, 0.10), (0.045, 0.16), (0.016, 0.19), (0.016, 0.22),
                (0.024, 0.23), (0.024, 0.26), (0.0001, 0.27)]
    b = lathe("Bottle", prof, steps=64, mat=cached("bglass", lambda: mat_glass((0.92, 0.96, 0.94))))
    b.location = loc
    s = 0.9
    inner = [(max(r * s - 0.002, 0.0001), z * 0.72 + 0.004) for r, z in prof if z < prof[-1][1] * 0.75]
    inner = [(0.0001, 0.004)] + inner[1:] + [(0.0001, inner[-1][1])]
    li = lathe("Liquid", inner, steps=64, mat=cached("liq" + str(liquid), lambda: mat_liquid(liquid)))
    li.location = loc
    if kind != 2:
        cap_c = rnd.choice([(0.02, 0.02, 0.02), (0.5, 0.35, 0.2), (0.6, 0.1, 0.08)])
        cyl("BCap", 0.014, 0.025, loc=(loc[0], loc[1], loc[2] + prof[-1][1] + 0.01),
            mat=cached("bc" + str(cap_c), lambda: mat_simple("BCap", cap_c, 0.4)))
        lab_c = rnd.choice([(0.85, 0.82, 0.72), (0.08, 0.08, 0.08), (0.6, 0.5, 0.35), (0.15, 0.2, 0.3)])
        cyl("BLabel", prof[3][0] + 0.0012, 0.07, loc=(loc[0], loc[1], loc[2] + 0.10),
            mat=cached("bl" + str(lab_c), lambda: mat_simple("BLabel", lab_c, 0.6, spec=0.3)))

def rocks_glass(loc, fill=0.5):
    prof = [(0.0001, 0), (0.040, 0), (0.042, 0.002), (0.043, 0.085), (0.040, 0.085), (0.039, 0.012), (0.0001, 0.012)]
    lathe("Rocks", prof, steps=64, mat=cached("rglass", mat_glass)).location = loc
    lathe("Whisky", [(0.0001, 0.0125), (0.0385, 0.0125), (0.0390, 0.012 + 0.07 * fill), (0.0001, 0.012 + 0.07 * fill)],
          steps=64, mat=cached("liqwh", lambda: mat_liquid((0.85, 0.45, 0.12)))).location = loc
    box("Ice", (0.035, 0.035, 0.032), (loc[0] + 0.004, loc[1], loc[2] + 0.012 + 0.07 * fill - 0.008),
        rot=(0.2, 0.15, 0.4), mat=cached("ice", lambda: mat_glass((0.97, 0.98, 1.0), 0.08)), bevel=0.006)

# =============================================================== world, lights, camera
world = bpy.data.worlds.new("World"); scene.world = world
world.use_nodes = True
wnt = world.node_tree
BG = wnt.nodes["Background"]
hdr_dir = [d for d in __import__("glob").glob("/Applications/Blender.app/Contents/Resources/*/datafiles/studiolights/world")][0]
ENV = wnt.nodes.new("ShaderNodeTexEnvironment")
ENV.image = bpy.data.images.load(os.path.join(hdr_dir, "interior.exr"))
_map = wnt.nodes.new("ShaderNodeMapping"); _tcw = wnt.nodes.new("ShaderNodeTexCoord")
wnt.links.new(_tcw.outputs["Generated"], _map.inputs[0])
_map.inputs["Rotation"].default_value = (0, 0, math.radians(200))
wnt.links.new(_map.outputs[0], ENV.inputs[0])
BGH = wnt.nodes.new("ShaderNodeBackground"); wnt.links.new(ENV.outputs[0], BGH.inputs[0])
_lp = wnt.nodes.new("ShaderNodeLightPath"); _mx = wnt.nodes.new("ShaderNodeMixShader")
wnt.links.new(_lp.outputs["Is Glossy Ray"], _mx.inputs[0])
wnt.links.new(BG.outputs[0], _mx.inputs[1]); wnt.links.new(BGH.outputs[0], _mx.inputs[2])
wnt.links.new(_mx.outputs[0], wnt.nodes["World Output"].inputs[0])

def set_world(color, strength, hdr):
    BG.inputs[0].default_value = (*color, 1)
    BG.inputs[1].default_value = strength if PASS != "halo" else 0.0
    BGH.inputs[1].default_value = hdr if PASS != "halo" else 0.0

def area(name, loc, target, size, power, color=(1, 1, 1), size_y=None, spread=None):
    ld = bpy.data.lights.new(name, "AREA")
    ld.shape = "RECTANGLE" if size_y else "SQUARE"
    ld.size = size
    if size_y:
        ld.size_y = size_y
    ld.energy = power if PASS != "halo" else 0.0
    ld.color = color
    if spread:
        ld.spread = spread
    lo = link(bpy.data.objects.new(name, ld))
    lo.location = loc
    lo.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return lo

def point(name, loc, power, color=(1.0, 0.75, 0.5), radius=0.03):
    ld = bpy.data.lights.new(name, "POINT"); ld.energy = power if PASS != "halo" else 0.0
    ld.color = color; ld.shadow_soft_size = radius
    lo = link(bpy.data.objects.new(name, ld)); lo.location = loc
    return lo

cam_d = bpy.data.cameras.new("Cam"); cam_d.sensor_fit = "HORIZONTAL"; cam_d.sensor_width = 36
cam = link(bpy.data.objects.new("Cam", cam_d)); scene.camera = cam
FSTOP = [None]

def frame(loc, tgt, regions, fstop=None, lens=None, shift=None):
    """regions: aspect -> (W, H) metres at the target that must be visible, or a full
    override aspect -> dict(loc=, tgt=, W=, H=, lens=)."""
    r = regions.get(ASPECT, regions.get("wide"))
    if isinstance(r, dict):
        loc = r.get("loc", loc); tgt = r.get("tgt", tgt); lens_o = r.get("lens"); W, H = r.get("W", 1), r.get("H", 1)
        shift = r.get("shift", shift)
    else:
        W, H = r; lens_o = None
    cam.location = loc
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    d = (Vector(tgt) - Vector(loc)).length
    a = RES[0] / RES[1]
    vis_w = max(W, H * a)
    cam_d.lens = lens_o or lens or 36 * d / vis_w
    if shift:
        cam_d.shift_x, cam_d.shift_y = shift
    if fstop:
        cam_d.dof.use_dof = True
        cam_d.dof.focus_distance = d
        cam_d.dof.aperture_fstop = fstop

EXPOSURE = [0.35]
LOOK = ["AgX - Medium High Contrast"]

# =============================================================== scenes
def warm_wall(color=(0.82, 0.74, 0.62), floor_z=-1.5, floor=True):
    w = box("Wall", (8, 0.05, 5), (0, -0.025, 0.5), mat=mat_plaster("WallPaint", color))
    if floor:
        box("Floor", (8, 6, 0.02), (0, 3.0, floor_z - 0.01), mat=cached("planks", lambda: mat_planks(
            "Floor", (0.16, 0.10, 0.06), (0.22, 0.14, 0.08))))
    return w

def hero_lighting(strength=1.0):
    set_world((0.040, 0.027, 0.015), 0.65 * strength, 0.12)
    area("RoomLamp", (-0.80, 1.40, 0.05), (0, 0.03, 0), 0.25, 3.5 * strength, color=(1.0, 0.78, 0.55), size_y=0.6)
    area("Fill", (1.8, 2.4, 0.9), (0, 0, 0), 1.5, 2.0 * strength, color=(1.0, 0.86, 0.72))

def hero_props():
    vine([(-0.24, 0.26, 0.75), (-0.21, 0.22, 0.40), (-0.18, 0.26, 0.12), (-0.21, 0.30, -0.15), (-0.18, 0.26, -0.42)],
         n=26, seed=2)
    vine([(-0.32, 0.32, 0.70), (-0.29, 0.36, 0.30), (-0.27, 0.32, -0.05)], n=14, seed=5)
    picture_frame(0.31, 0.77, -0.30, 0.34, art=(0.30, 0.22, 0.16), frame="black")

def sc_hero(cap):
    warm_wall()
    sconce("Sconce", "12", cap, "label_halo", spin=0.0)
    if ASPECT == "tall":
        picture_frame(0.31, 0.77, -0.30, 0.34, art=(0.30, 0.22, 0.16), frame="black")
    else:
        hero_props()
    hero_lighting()
    frame((0.62, 1.12, 0.14), (0.04, 0.02, -0.02),
          dict(wide=(0.70, 0.40), square=(0.56, 0.56), tall=(0.43, 0.76)), fstop=5.6)

def sc_single7():
    warm_wall()
    sconce("Sconce7", "7", "chrome", "label_ember45", spin=0.0)
    vine([(-0.42, 0.25, 0.45), (-0.38, 0.22, 0.20), (-0.36, 0.26, -0.05), (-0.40, 0.30, -0.30)], n=18, seed=8,)
    hero_lighting(0.8)
    frame((0.38, 0.72, 0.09), (0.02, 0.01, -0.01),
          dict(wide=(0.44, 0.25), square=(0.34, 0.34), tall=(0.27, 0.48)), fstop=5.6)

def sc_set(cap="chrome", wallc=(0.82, 0.74, 0.62), props=True):
    warm_wall(wallc, floor_z=-1.42)
    sconce("S12", "12", cap, "label_halo", spin=0.0)
    sconce("S7L", "7", cap, "label_ember45", loc=(-0.285, 0, -0.005), spin=0.0)
    sconce("S7R", "7", cap, "label_lantern45", loc=(0.285, 0, -0.005), spin=0.0)
    if props:
        vine([(-0.62, 0.20, 0.55), (-0.58, 0.22, 0.30), (-0.56, 0.26, 0.05), (-0.60, 0.30, -0.18)], n=20, seed=4)
        picture_frame(0.56, 0.98, -0.22, 0.36, art=(0.30, 0.22, 0.16))
        credenza(-0.85, 0.85, 0.02, 0.42, -0.66, -1.42)
        pot((-0.62, 0.22, -0.66), 0.09, 0.15)
        vine([(-0.62, 0.22, -0.50), (-0.70, 0.30, -0.52), (-0.78, 0.40, -0.70), (-0.80, 0.48, -0.95)], n=14, seed=9)
        rnd = random.Random(4)
        for i in range(6):
            box("LeanSleeve", (0.315, 0.004, 0.315), (0.40 + i * 0.006, 0.07 + i * 0.012, -0.66 + 0.155),
                rot=(-0.12, 0, 0), mat=sleeve_mat(rnd), bevel=0.0008, seg=1)
    hero_lighting()
    BGH.inputs[1].default_value = 0.0
    bpy.data.objects["Fill"].data.energy = 0.4
    area("SideLamp", (-1.3, 1.2, 0.35), (0, 0.03, 0), 0.3, 4.0, color=(1.0, 0.75, 0.5), size_y=0.8)
    # two small lamps near the camera's mirror direction: draw the groove sheen arcs seen in the reference
    area("Sheen1", (-0.45, 1.6, 0.55), (0, 0.03, 0), 0.12, 0.8, color=(1.0, 0.8, 0.6))
    area("Sheen2", (0.50, 1.6, -0.45), (0, 0.03, 0), 0.12, 0.6, color=(1.0, 0.8, 0.6))
    frame((0.16, 1.75, 0.10), (0.0, 0.0, -0.01),
          dict(wide=(1.18, 0.60), square=(0.88, 0.88), tall=dict(W=0.86, H=1.5, tgt=(0, 0, -0.30), loc=(0.08, 1.75, -0.22))),
          fstop=8)

def sc_living():
    FZ = -1.45
    warm_wall((0.60, 0.42, 0.31), floor_z=FZ)
    sconce("Sconce", "12", "chrome", "label_halo", loc=(-0.10, 0, 0.0), spin=0.0)
    credenza(-0.85, 0.85, 0.02, 0.44, -0.85, FZ)
    turntable(-0.12, 0.25, -0.85)
    for sx in (-0.66, 0.62):
        speaker(sx, 0.20, -0.85)
    # cube record shelf, 2 x 4
    rnd = random.Random(11)
    sx0, cw, ct, dep = -1.85, 0.37, 0.018, 0.39
    shelf_m = cached("shelfwhite", lambda: mat_simple("ShelfPaint", (0.80, 0.78, 0.74), 0.45))
    for i in range(3):
        box("ShelfV", (ct, dep, 4 * cw + ct), (sx0 + i * (cw + ct), dep / 2 + 0.01, FZ + (4 * cw + ct) / 2 + 0.06), mat=shelf_m, bevel=0.002)
    for j in range(5):
        box("ShelfH", (2 * cw + 3 * ct, dep, ct), (sx0 + cw + ct, dep / 2 + 0.01, FZ + 0.06 + j * (cw + ct) + ct / 2), mat=shelf_m, bevel=0.002)
    for i in range(2):
        for j in range(4):
            if (i, j) == (1, 3):
                continue
            x0 = sx0 + ct / 2 + i * (cw + ct)
            record_row(x0 + 0.01, x0 + cw - (0.06 if rnd.random() < 0.5 else 0.01), 0.04, 0.33, FZ + 0.06 + ct + j * (cw + ct), rnd)
    pot((-1.45, 0.18, FZ + 0.06 + 3 * (cw + ct) + ct), 0.08, 0.13)
    vine([(-1.45, 0.20, FZ + 1.30), (-1.40, 0.32, FZ + 1.25), (-1.36, 0.42, FZ + 1.05), (-1.38, 0.45, FZ + 0.85)], n=14, seed=12)
    snake_plant((1.15, 0.30, FZ), H=0.8)
    # floor lamp right, warm shade
    lx, ly = 1.55, 0.55
    cyl("LampPole", 0.008, 1.45, loc=(lx, ly, FZ + 0.72), mat=M_("brass_pol"))
    cyl("LampBase", 0.14, 0.02, loc=(lx, ly, FZ + 0.01), mat=M_("black"), bevel=0.004)
    shade = lathe("Shade", [(0.16, 0.0), (0.161, 0.0), (0.131, 0.26), (0.13, 0.26)], steps=96, sm=0,
                  mat=cached("shade", lambda: mat_simple("Shade", (0.9, 0.82, 0.68), 0.8, trans=0.0, sss=0.0)))
    shade.location = (lx, ly, FZ + 1.30)
    shade.modifiers.new("s", "SOLIDIFY").thickness = 0.002
    point("LampBulb", (lx, ly, FZ + 1.42), 18, color=(1.0, 0.70, 0.42), radius=0.04)
    # rug
    box("Rug", (2.6, 1.8, 0.012), (0.0, 1.35, FZ + 0.006), mat=mat_fabric("Rug", (0.42, 0.33, 0.25), scale=300), bevel=0.004)
    set_world((0.020, 0.024, 0.032), 0.6, 0.10)
    area("Window", (2.6, 2.2, 0.4), (0, 0.3, -0.6), 1.2, 6.0, color=(0.65, 0.75, 1.0), size_y=1.6)
    area("Fill", (0.2, 3.5, 0.5), (0, 0, -0.4), 2.0, 2.0, color=(1.0, 0.86, 0.72))
    EXPOSURE[0] = 1.0
    frame((1.45, 3.1, -0.30), (-0.30, 0.0, -0.45),
          dict(wide=(2.9, 1.63), square=(2.1, 2.1), tall=dict(W=1.45, H=2.58, tgt=(-0.15, 0, -0.42), loc=(1.0, 3.2, -0.30))),
          fstop=8)

def sc_bar():
    FZ = -1.50
    green = (0.13, 0.035, 0.032)
    warm_wall(green, floor_z=FZ)
    sconce("Sconce", "12", "brass", "label_afterhours", loc=(0, 0, 0.05), spin=0.0)
    rnd = random.Random(21)
    sm = walnut()
    liquids = [(0.85, 0.45, 0.12), (0.95, 0.95, 0.92), (0.7, 0.25, 0.08), (0.9, 0.6, 0.2), (0.5, 0.12, 0.06)]
    for side in (-1, 1):
        x0, x1 = (-1.35, -0.36) if side < 0 else (0.36, 1.35)
        for zs in (-0.32, 0.10, 0.50):
            box("Shelf", (x1 - x0, 0.24, 0.035), ((x0 + x1) / 2, 0.12, zs), mat=sm, bevel=0.003)
            # under-shelf warm LED
            box("ShelfLED", (x1 - x0 - 0.04, 0.01, 0.003), ((x0 + x1) / 2, 0.20, zs - 0.019),
                mat=cached("shelfled", lambda: mat_emit("ShelfLED", (1.0, 0.62, 0.30), 6.0)))
            x = x0 + 0.06
            while x < x1 - 0.06:
                if zs > 0.4 and rnd.random() < 0.3:
                    x += 0.08; continue
                bottle((x, 0.12 + rnd.uniform(-0.03, 0.03), zs + 0.0175), rnd.choice([0, 1, 2]), rnd.choice(liquids), rnd)
                x += rnd.uniform(0.10, 0.13)
    # back counter
    box("BackCab", (2.9, 0.50, 0.86), (0, 0.27, FZ + 0.43), mat=sm, bevel=0.006)
    box("BackTop", (2.94, 0.54, 0.03), (0, 0.27, FZ + 0.875), mat=mat_simple("Marble", (0.85, 0.83, 0.80), 0.15, coat=0.4, bump_scale=8, bump_str=0.02), bevel=0.004)
    for x in (-0.9, -0.55, 0.6, 0.95):
        bottle((x, 0.30, FZ + 0.89), rnd.choice([0, 1]), rnd.choice(liquids), rnd)
    # foreground bar top
    box("BarTop", (3.2, 0.60, 0.05), (0.0, 1.75, -0.47), mat=walnut(), bevel=0.01)
    box("BarFront", (3.2, 0.10, 1.0), (0.0, 2.0, -1.0), mat=walnut(), bevel=0.006)
    rocks_glass((0.18, 1.62, -0.445), 0.55)
    rocks_glass((-0.12, 1.78, -0.445), 0.4)
    box("Coaster", (0.1, 0.1, 0.004), (0.18, 1.62, -0.447), mat=M_("felt"), bevel=0.002)
    set_world((0.010, 0.012, 0.012), 0.5, 0.0)
    area("Pendant", (0.6, 1.7, 0.4), (0.4, 1.7, -0.47), 0.15, 6, color=(1.0, 0.7, 0.45))
    area("Fill", (-1.5, 2.6, 1.6), (0, 0, -0.3), 1.0, 1.2, color=(1.0, 0.85, 0.7))
    EXPOSURE[0] = 0.55
    frame((0.55, 2.75, -0.08), (0.0, 0.0, -0.10),
          dict(wide=(2.5, 1.40), square=(1.7, 1.7), tall=dict(W=1.08, H=1.92, tgt=(0.05, 0.0, -0.30), loc=(0.40, 2.75, -0.15))),
          fstop=4.0)
    cam_d.dof.focus_distance = (Vector((0, 0.05, 0.05)) - cam.location).length

def sc_studio():
    FZ = -1.50
    warm_wall((0.13, 0.13, 0.135), floor_z=FZ)
    sconce("S12", "12", "black", "label_promo_white", loc=(0, 0, 0.0), spin=0.0)
    sconce("S7L", "7", "black", "label_ember45", loc=(-0.29, 0, -0.005), spin=0.0)
    sconce("S7R", "7", "black", "label_lantern45", loc=(0.29, 0, -0.005), spin=0.0)
    pm = mat_fabric("Panel", (0.32, 0.16, 0.10), scale=500)
    pm2 = mat_fabric("Panel2", (0.25, 0.25, 0.26), scale=500)
    for x, m in ((-1.05, pm), (1.05, pm), (-1.5, pm2), (1.5, pm2)):
        box("AcPanel", (0.40, 0.05, 1.0), (x, 0.025, -0.05), mat=m, bevel=0.01)
    # desk
    top = -0.75
    box("DeskTop", (1.8, 0.75, 0.035), (0, 0.42, top - 0.0175), mat=oak(), bevel=0.004)
    for lx in (-0.85, 0.85):
        box("DeskLeg", (0.05, 0.65, 0.04), (lx, 0.42, FZ + 0.02), mat=M_("black"))
        box("DeskLegV", (0.05, 0.05, top - FZ - 0.035), (lx, 0.42, (top + FZ) / 2 - 0.0175), mat=M_("black"))
    for sx in (-0.62, 0.62):
        box("SpkStand", (0.16, 0.18, 0.10), (sx, 0.22, top + 0.05), mat=mat_fabric("Foam", (0.05, 0.05, 0.05), scale=200), bevel=0.004)
        box("Monitor", (0.19, 0.25, 0.30), (sx, 0.22, top + 0.10 + 0.15), rot=(0, 0, -0.25 * (1 if sx > 0 else -1)),
            mat=M_("black_plastic"), bevel=0.01)
        rz = 0.25 * (1 if sx > 0 else -1)
        nx, ny = math.sin(rz) * 0.126, math.cos(rz) * 0.126
        for zz, rr in ((top + 0.10 + 0.11, 0.065), (top + 0.10 + 0.235, 0.022)):
            c = lathe("Driver", [(0.0001, -0.010), (rr * 0.5, -0.006), (rr, 0.0), (rr + 0.006, 0.002), (rr + 0.006, 0.0), (0.0001, 0.0)],
                      steps=64, mat=cached("driver", lambda: mat_simple("Driver", (0.25, 0.25, 0.26), 0.45)))
            c.location = (sx - nx * 0.0 + math.sin(-rz) * -0.0, 0.22 + 0.126, zz)
            c.rotation_euler = (-math.pi / 2, 0, -rz)
            c.location = (sx + math.sin(-rz) * -0.126 * -1 * 0 , 0.22, zz)
            c.location = (sx - math.sin(rz) * 0.126 * -1, 0.22 + math.cos(rz) * 0.126, zz)
    # laptop
    box("LaptopBase", (0.31, 0.215, 0.012), (-0.30, 0.45, top + 0.006), rot=(0, 0, 0.12), mat=M_("alu"), bevel=0.003)
    scr = box("LaptopLid", (0.31, 0.006, 0.205), (-0.31, 0.34, top + 0.11), rot=(math.radians(-12), 0, 0.12), mat=M_("alu"), bevel=0.003)
    box("Screen", (0.29, 0.002, 0.18), (-0.312, 0.346, top + 0.11), rot=(math.radians(-12), 0, 0.12),
        mat=mat_emit("Screen", (0.25, 0.32, 0.55), 0.35))
    # keyboard controller
    kx, ky = 0.10, 0.60
    box("KeyBody", (0.78, 0.22, 0.05), (kx, ky, top + 0.025), mat=M_("black_plastic"), bevel=0.006)
    wk = cached("whitekey", lambda: mat_simple("WhiteKey", (0.9, 0.9, 0.88), 0.3))
    for i in range(29):
        box("WKey", (0.0225, 0.12, 0.012), (kx - 0.33 + i * 0.0235, ky + 0.04, top + 0.056), mat=wk, bevel=0.001, seg=1)
        if i % 7 not in (2, 6):
            box("BKey", (0.013, 0.075, 0.012), (kx - 0.33 + i * 0.0235 + 0.0117, ky + 0.015, top + 0.066), mat=M_("black"), bevel=0.001, seg=1)
    for i in range(8):
        cyl("Knob", 0.008, 0.012, loc=(kx - 0.25 + i * 0.05, ky - 0.075, top + 0.056), mat=M_("alu"))
    lathe("Mug", [(0.0001, 0), (0.040, 0), (0.042, 0.095), (0.038, 0.095), (0.037, 0.008), (0.0001, 0.008)], steps=48,
          mat=M_("ceramic")).location = (0.55, 0.55, top)
    snake_plant((-1.15, 0.45, FZ), H=0.9, seed=6)
    set_world((0.012, 0.014, 0.020), 1.0, 0.0)
    area("Fill", (1.8, 2.4, 1.6), (0, 0.4, -0.6), 1.2, 6.0, color=(0.85, 0.9, 1.0))
    area("DeskKey", (-1.2, 1.6, 0.3), (0, 0.4, -0.75), 0.6, 6.0, color=(1.0, 0.8, 0.6))
    EXPOSURE[0] = 0.9
    frame((0.55, 2.55, -0.20), (0.0, 0.0, -0.32),
          dict(wide=(2.5, 1.40), square=(1.7, 1.7), tall=dict(W=1.08, H=1.92, tgt=(0.0, 0.0, -0.40), loc=(0.40, 2.55, -0.25))),
          fstop=5.6)
    cam_d.dof.focus_distance = (Vector((0, 0.05, -0.1)) - cam.location).length

def pillow(loc, size, rot=(0, 0, 0), color=(0.85, 0.82, 0.76)):
    me = bpy.data.meshes.new("Pillow"); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0); bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new("Pillow", me))
    me.transform(Matrix.Diagonal((*size, 1)))
    sub = ob.modifiers.new("sub", "SUBSURF"); sub.levels = 3; sub.render_levels = 3
    sub.levels = 2; sub.render_levels = 2
    for p in me.polygons:
        p.use_smooth = True
    ob.location = loc; ob.rotation_euler = rot
    ob.data.materials.append(cached("pil" + str(color), lambda: mat_fabric("Linen", color, scale=700)))
    return ob

def sc_bedroom():
    global SIDE_K
    SIDE_K = 1.4
    FZ = -1.40
    warm_wall((0.55, 0.47, 0.39), floor_z=FZ)
    sconce("Sconce", "12", "chrome", "label_meridian", loc=(-0.98, 0, 0.0), spin=0.0)
    # headboard + bed (queen, centred x=0.25)
    bx = 0.30
    hb = mat_fabric("Headboard", (0.30, 0.26, 0.22), scale=500)
    for i in range(5):
        box("HBpanel", (0.32, 0.08, 1.05), (bx - 0.64 + i * 0.32, 0.05, FZ + 0.62), mat=hb, bevel=0.03, seg=4)
    box("BedBase", (1.62, 2.05, 0.30), (bx, 1.12, FZ + 0.15), mat=hb, bevel=0.02)
    box("Mattress", (1.58, 2.0, 0.22), (bx, 1.12, FZ + 0.41), mat=mat_fabric("Sheet", (0.86, 0.84, 0.80), scale=900), bevel=0.04, seg=4)
    duvet = box("Duvet", (1.68, 1.45, 0.10), (bx, 1.40, FZ + 0.55), mat=mat_fabric("Duvet", (0.70, 0.62, 0.52), scale=700), bevel=0.045, seg=5)
    dsp = duvet.modifiers.new("sub", "SUBSURF"); dsp.levels = 2; dsp.render_levels = 2
    tx = bpy.data.textures.new("lumps", "CLOUDS"); tx.noise_scale = 0.25
    dd = duvet.modifiers.new("disp", "DISPLACE"); dd.texture = tx; dd.strength = 0.025
    box("Throw", (1.70, 0.45, 0.03), (bx, 1.95, FZ + 0.60), mat=mat_fabric("Throw", (0.18, 0.22, 0.20), scale=300), bevel=0.012, seg=3)
    pillow((bx - 0.38, 0.30, FZ + 0.66), (0.62, 0.18, 0.42), rot=(math.radians(-25), 0, 0))
    pillow((bx + 0.38, 0.30, FZ + 0.66), (0.62, 0.18, 0.42), rot=(math.radians(-25), 0, 0))
    pillow((bx - 0.20, 0.48, FZ + 0.62), (0.45, 0.14, 0.32), rot=(math.radians(-35), 0, 0.1), color=(0.55, 0.35, 0.22))
    # nightstand
    nx = -0.98
    box("Nightstand", (0.48, 0.40, 0.52), (nx, 0.22, FZ + 0.26), mat=walnut(), bevel=0.006)
    box("NSDrawer", (0.44, 0.006, 0.16), (nx, 0.423, FZ + 0.40), mat=walnut(), bevel=0.002)
    box("NSPull", (0.08, 0.012, 0.008), (nx, 0.432, FZ + 0.40), mat=M_("brass_pol"), bevel=0.002)
    top = FZ + 0.52
    rnd = random.Random(31)
    zz = top
    for i, c in enumerate([(0.55, 0.15, 0.10), (0.85, 0.80, 0.70), (0.12, 0.20, 0.30)]):
        t = rnd.uniform(0.022, 0.035)
        box("Book", (0.22 - i * 0.02, 0.16, t), (nx + 0.06, 0.20, zz + t / 2), rot=(0, 0, rnd.uniform(-0.2, 0.2)),
            mat=cached("book" + str(c), lambda: mat_simple("Book", c, 0.6)), bevel=0.002)
        zz += t
    lathe("WaterGlass", [(0.0001, 0), (0.032, 0), (0.035, 0.11), (0.032, 0.11), (0.030, 0.006), (0.0001, 0.006)],
          steps=48, mat=cached("rglass", mat_glass)).location = (nx - 0.14, 0.26, top)
    lathe("Water", [(0.0001, 0.0065), (0.0298, 0.0065), (0.0315, 0.08), (0.0001, 0.08)], steps=48,
          mat=cached("water", lambda: mat_liquid((0.97, 0.98, 1.0)))).location = (nx - 0.14, 0.26, top)
    box("Rug", (2.2, 1.6, 0.012), (bx, 1.5, FZ + 0.006), mat=mat_fabric("Rug", (0.35, 0.30, 0.26), scale=300), bevel=0.004)
    # the sconce is the only light
    set_world((0.0, 0.0, 0.0), 0.0, 0.03)
    # the sconce's own forward spill (its side LEDs + record bounce), modelled as a soft warm panel at the sconce
    area("SconceSpill", (-0.98, 0.07, -0.02), (-0.6, 2.0, -0.9), 0.30, 2.5, color=(1.0, 0.55, 0.22))
    EXPOSURE[0] = 1.7
    frame((0.85, 2.75, -0.55), (-0.55, 0.0, -0.50),
          dict(wide=(2.6, 1.46), square=(1.8, 1.8), tall=dict(W=1.1, H=1.96, tgt=(-0.85, 0.0, -0.55), loc=(0.35, 2.7, -0.60))),
          fstop=4.0)
    cam_d.dof.focus_distance = (Vector((-0.98, 0.04, 0.0)) - cam.location).length

def sc_macro():
    warm_wall()
    sconce("Sconce", "12", "chrome", "label_halo", spin=0.0)
    hero_lighting()
    BGH.inputs[1].default_value = 0.45
    # a window and a lamp across the room for the dome to reflect
    area("WindowR", (0.9, 2.6, 0.6), (0, 0.04, 0), 1.0, 5.0, color=(0.95, 0.9, 0.85), size_y=1.4)
    zc = HUB_T + BP_T + SO_T + REC_T + WASH_T + 0.006
    tgt = (0.0, zc, 0.0)
    frame((0.085, zc + 0.125, 0.055), tgt,
          dict(wide=(0.115, 0.065), square=(0.085, 0.085), tall=(0.062, 0.11)), fstop=3.2)

def sc_swap(step):
    warm_wall()
    vine([(-0.24, 0.26, 0.75), (-0.21, 0.22, 0.40), (-0.18, 0.26, 0.12), (-0.21, 0.30, -0.15), (-0.18, 0.26, -0.42)], n=26, seed=2)
    hero_lighting()
    if step == 1:
        sconce("Sconce", "12", "chrome", "label_halo", spin=0.0, cap_off=(0.0, 0.0, 0.11), wash_off=(0.0, 0.0, 0.065))
    elif step == 2:
        sconce("Sconce", "12", "chrome", "label_halo", spin=0.0, rec_off=(0.0, -0.07, 0.15), rec_tilt=math.radians(-14),
               cap_off=(0.20, 0.07, 0.14), wash_off=(0.20, 0.07, 0.115))
    else:
        sconce("Sconce", "12", "chrome", "label_meridian", spin=0.0)
    frame((0.78, 1.25, 0.16), (0.06, 0.07, -0.02),
          dict(wide=(0.86, 0.48), square=(0.66, 0.66), tall=(0.50, 0.89)), fstop=8)

def sc_flatlay():
    # tabletop: pale oak, top-down
    box("Table", (3, 3, 0.04), (0, 0, -0.02), mat=mat_plaster("Concrete", (0.36, 0.34, 0.31), var=0.12, scale=12))
    kraft = cached("kraft", lambda: mat_simple("Kraft", (0.40, 0.27, 0.15), 0.85, spec=0.2, bump_scale=900, bump_str=0.08))
    pulp = cached("pulp", lambda: mat_simple("Pulp", (0.42, 0.39, 0.34), 0.95, spec=0.15, bump_scale=300, bump_str=0.35))
    L = dict(
        wide=dict(box=(-0.25, 0.0), lid=(-0.56, 0.12), dome=(0.03, 0.10), c45=(0.03, -0.01), plate=(0.15, 0.09),
                  adapt=(0.12, -0.09), card=(0.33, 0.03), hw=(0.07, -0.20), W=0.98, H=0.55),
        square=dict(box=(-0.17, 0.12), lid=(-0.20, -0.40), dome=(0.12, 0.24), c45=(0.23, 0.24), plate=(0.18, 0.08),
                    adapt=(0.14, -0.12), card=(0.33, -0.08), hw=(0.15, -0.28), W=0.80, H=0.80),
        tall=dict(box=(0.0, 0.22), lid=(-0.03, 0.66), dome=(-0.12, -0.06), c45=(-0.12, -0.16), plate=(0.05, -0.08),
                  adapt=(0.12, -0.21), card=(-0.07, -0.30), hw=(0.06, -0.425), W=0.52, H=0.93),
    )[ASPECT]
    # box base (open) with pulp tray holding the backplate
    bxp = L["box"]; S = 0.33; bh = 0.075
    for (sx, sy, px, py) in ((S, 0.008, 0, S / 2), (S, 0.008, 0, -S / 2), (0.008, S, S / 2, 0), (0.008, S, -S / 2, 0)):
        box("BoxWall", (sx, sy, bh), (bxp[0] + px, bxp[1] + py, bh / 2), mat=kraft, bevel=0.0015)
    box("BoxFloor", (S, S, 0.004), (bxp[0], bxp[1], 0.002), mat=kraft)
    tray = box("Tray", (S - 0.01, S - 0.01, 0.05), (bxp[0], bxp[1], 0.03), mat=pulp, bevel=0.004)
    cut = cyl("TrayCut", 5.4 * IN, 0.05, loc=(bxp[0], bxp[1], 0.055))
    mm = tray.modifiers.new("cut", "BOOLEAN"); mm.object = cut; mm.solver = "EXACT"; cut.hide_render = True; cut.hide_viewport = True
    # backplate in the tray, face up: show LED rim + pads + insert (no record: kit)
    kit = empty("KitBP", (bxp[0], bxp[1], 0.03 - HUB_T + 0.004), (0, 0, 0))
    s = SPEC["12"]; bpr = s["bp_r"]
    lathe("bp", [(0.0050, 0.0), (bpr - 0.0012, 0.0), (bpr, 0.0012), (bpr, BP_T - 0.0012), (bpr - 0.0012, BP_T), (0.0050, BP_T)],
          parent=kit, z=HUB_T, mat=M_("bp"))
    lathe("led", [(bpr - 0.0002, 0.0030), (bpr + 0.0008, 0.0030), (bpr + 0.0008, 0.0100), (bpr - 0.0002, 0.0100)],
          parent=kit, z=HUB_T, mat=M_("white"))
    lathe("ins", [(0.0032, 0.0), (0.0050, 0.0), (0.0050, BP_T + 0.0004), (0.0032, BP_T + 0.0004)], steps=48, parent=kit,
          z=HUB_T, mat=M_("brass_pol"))
    for rr in (bpr - 0.012, bpr * 0.55):
        for i in range(3):
            a = math.radians(-90 + 120 * i + (60 if rr < bpr * 0.6 else 0))
            cyl("pad", 0.00635, SO_T, loc=(rr * math.cos(a), rr * math.sin(a), HUB_T + BP_T + SO_T / 2), mat=M_("felt"), parent=kit, verts=24)
    # lid, flipped, print up
    lid = box("Lid", (S + 0.01, S + 0.01, 0.03), (L["lid"][0], L["lid"][1], 0.015), rot=(0, 0, 0.06), mat=kraft, bevel=0.002)
    lp = box("LidPrint", (S - 0.01, S - 0.01, 0.0006), (L["lid"][0], L["lid"][1], 0.0305), rot=(0, 0, 0.06))
    lp.data.uv_layers.new(name="UV")
    uv = lp.data.uv_layers[0]
    for poly in lp.data.polygons:
        for li in poly.loop_indices:
            v = lp.data.vertices[lp.data.loops[li].vertex_index].co
            uv.data[li].uv = (v.x + 0.5, v.y + 0.5)
    lp.data.materials.append(mat_image("BoxPrint", "box_print", 0.85))
    # dome cap + felt washer beside it
    d = empty("DomeE", (L["dome"][0], L["dome"][1], 0.0))
    dome_cap(d, "chrome", 0.0, post=0.0)
    lathe("Wash", [(0.0036, 0.0), (0.0210, 0.0), (0.0212, WASH_T * 0.5), (0.0210, WASH_T), (0.0036, WASH_T)], steps=96,
          mat=M_("felt")).location = (L["dome"][0] + 0.06, L["dome"][1] - 0.01, 0)
    # threaded post shown lying next to the dome
    cyl("Post", 0.0032, 0.03, loc=(L["dome"][0] - 0.005, L["dome"][1] - 0.045, 0.0032), rot=(0, math.pi / 2, 0.3), mat=M_("chrome"))
    e45 = empty("C45E", (L["c45"][0], L["c45"][1], 0.0019))
    adapter45_cap(e45, "chrome", 0.0)
    # steel wall plate with bayonet studs + slots
    pe = empty("PlateE", (L["plate"][0], L["plate"][1], 0.0))
    pr = 2.0 * IN
    plate = lathe("MountPlate", [(0.5 * IN, 0.0), (pr - 0.0006, 0.0), (pr, 0.0006), (pr, 0.0019), (0.5 * IN, 0.0019)],
                  steps=128, parent=pe, mat=M_("steel"))
    cutters = []
    for k in range(4):
        ang = k * math.pi / 2 + math.pi / 4
        for j in (-1, 0, 1):
            a = ang + j * math.radians(9)
            cutters.append(cyl("sc", 0.0024, 0.02, loc=(0.0425 * math.cos(a), 0.0425 * math.sin(a), 0.001), parent=pe))
    for c in cutters:
        m = plate.modifiers.new("c", "BOOLEAN"); m.object = c; m.solver = "EXACT"; c.hide_render = True; c.hide_viewport = True
    for k in range(3):
        a = math.radians(90 + 120 * k)
        lathe("Bayonet", [(0.0001, 0.0), (0.0024, 0.0), (0.0024, 0.0032), (0.0044, 0.0032), (0.0044, 0.0050), (0.0036, 0.0054),
                          (0.0001, 0.0054)], steps=32, parent=pe, z=0.0019, mat=M_("chrome")).location = (0.040 * math.cos(a), 0.040 * math.sin(a), 0.0019)
    # 12 V adapter with coiled black lead and barrel plug
    ax, ay = L["adapt"]
    box("Adapter", (0.045, 0.062, 0.036), (ax, ay, 0.018), mat=M_("black_plastic"), bevel=0.005)
    for dx in (-0.006, 0.006):
        box("Prong", (0.0016, 0.016, 0.006), (ax + dx, ay + 0.039, 0.018), mat=M_("steel"))
    pts = [(ax, ay - 0.031, 0.006)]
    for i in range(1, 40):
        t = i / 39 * 2.6 * math.pi
        pts.append((ax + 0.075 + 0.055 * math.sin(t) + 0.004 * i / 39, ay - 0.08 + 0.055 * -math.cos(t) * 0.9, 0.003 + 0.0015 * (i % 2)))
    tube("Lead", pts, 0.0017, M_("black_plastic"))
    cyl("Barrel", 0.005, 0.035, loc=(ax + 0.16, ay - 0.13, 0.005), rot=(0, math.pi / 2, -0.4), mat=M_("black_plastic"))
    # insert card
    cx, cy = L["card"]; cw, ch = 0.105, 0.147
    card = box("Card", (cw, ch, 0.0008), (cx, cy, 0.0004), rot=(0, 0, -0.04))
    card.data.uv_layers.new(name="UV")
    uv = card.data.uv_layers[0]
    for poly in card.data.polygons:
        for li in poly.loop_indices:
            v = card.data.vertices[card.data.loops[li].vertex_index].co
            uv.data[li].uv = (v.x + 0.5, v.y + 0.5)
    card.data.materials.append(mat_image("Card", "insert_card", 0.8))
    # hardware row: 2 screws, 2 anchors, set screw, L key
    hx, hy = L["hw"]
    for i in range(2):
        s_ = lathe("WScrew", [(0.0001, -0.028), (0.0012, -0.026), (0.0021, -0.004), (0.0021, 0.0), (0.0045, 0.0),
                              (0.0045, 0.0012), (0.0030, 0.0026), (0.0001, 0.0028)], steps=32, mat=M_("steel"))
        s_.location = (hx - 0.06 + i * 0.03, hy, 0.0045); s_.rotation_euler = (math.pi / 2, 0, 0)
        a_ = lathe("Anchor", [(0.0022, -0.030), (0.0046, -0.030), (0.0046, -0.001), (0.0060, -0.001), (0.0060, 0.0), (0.0022, 0.0)],
                   steps=32, mat=cached("anchor", lambda: mat_simple("Anchor", (0.85, 0.80, 0.30), 0.6)))
        a_.location = (hx + 0.01 + i * 0.03, hy, 0.006); a_.rotation_euler = (math.pi / 2, 0, 0)
    tube("LKey", [(hx + 0.08, hy - 0.01, 0.0015), (hx + 0.08, hy + 0.025, 0.0015), (hx + 0.095, hy + 0.025, 0.0015)], 0.0012, M_("black"))
    set_world((0.9, 0.88, 0.85), 0.2, 0.3)
    area("Window", (-1.2, 0.8, 1.6), (0, 0, 0), 1.6, 75, color=(1.0, 0.97, 0.92))
    area("Bounce", (1.0, -0.6, 1.4), (0, 0, 0), 2.0, 30, color=(1.0, 0.95, 0.9))
    EXPOSURE[0] = 0.2
    LOOK[0] = "AgX - Base Contrast"
    frame((0.0, -0.001, 1.6), (0.0, 0.0, 0.0), {ASPECT: (L["W"], L["H"])}, fstop=11)

def sc_darkroom():
    """Video loop base: one sconce, dark room, faint blue moonlight; halo pass is separate."""
    FZ = -1.4
    warm_wall((0.72, 0.64, 0.54), floor_z=FZ)
    sconce("Sconce", "12", "chrome", "label_halo", spin=0.0)
    credenza(-0.7, 0.7, 0.02, 0.42, -0.72, FZ)
    pot((0.30, 0.22, -0.72), 0.08, 0.13)
    vine([(0.30, 0.22, -0.56), (0.37, 0.30, -0.58), (0.43, 0.40, -0.76), (0.45, 0.46, -1.0)], n=12, seed=14)
    set_world((0.004, 0.005, 0.009), 1.0, 0.03)
    area("Moon", (-1.6, 1.6, 0.8), (0, 0, -0.3), 0.8, 9.0, color=(0.55, 0.65, 1.0), size_y=1.4)
    EXPOSURE[0] = 0.6
    frame((0.30, 2.1, -0.10), (0.0, 0.0, -0.22), dict(tall=(0.78, 1.39), wide=(1.6, 0.9), square=(1.1, 1.1)), fstop=8)

SCENES = dict(hero_chrome=lambda: sc_hero("chrome"), hero_brass=lambda: sc_hero("brass"), hero_black=lambda: sc_hero("black"),
              single7=sc_single7, set=sc_set, living=sc_living, bar=sc_bar, studio=sc_studio, bedroom=sc_bedroom,
              macro=sc_macro, swap1=lambda: sc_swap(1), swap2=lambda: sc_swap(2), swap3=lambda: sc_swap(3),
              flatlay=sc_flatlay, darkroom=sc_darkroom)
SCENES[SCENE]()

# =============================================================== render
scene.render.engine = "CYCLES"
cy = scene.cycles
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"; prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    cy.device = "GPU"
except Exception as e:
    print("GPU setup failed, CPU:", e)
cy.samples = SAMPLES
cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.006 if not PREVIEW else 0.05
cy.use_denoising = True
cy.denoiser = "OPENIMAGEDENOISE"
cy.max_bounces = 10; cy.glossy_bounces = 6; cy.transmission_bounces = 10; cy.transparent_max_bounces = 16
cy.caustics_reflective = False; cy.caustics_refractive = False
cy.sample_clamp_indirect = 8.0
scene.render.resolution_x, scene.render.resolution_y = RES
scene.render.resolution_percentage = int(opt("--pct", "25")) if PREVIEW else 100
scene.view_settings.view_transform = "AgX"
try:
    scene.view_settings.look = LOOK[0]
except Exception:
    pass
scene.view_settings.exposure = float(opt("--exp", str(EXPOSURE[0])))
if EXR:
    scene.render.image_settings.file_format = "OPEN_EXR"
    scene.render.image_settings.color_depth = "32"
else:
    scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUT
os.makedirs(os.path.dirname(OUT), exist_ok=True)
if "--save" in argv:
    bpy.ops.wm.save_as_mainfile(filepath=OUT.rsplit(".", 1)[0] + ".blend")
bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
