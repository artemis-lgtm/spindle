"""Record sconce: procedural model + Cycles render.

Usage:
  Blender -b -P sconce.py -- hero     [--res 1920x1080] [--samples 768] [--out path.png]
  Blender -b -P sconce.py -- exploded [--res 1920x1080] [--samples 512] [--out path.png]

Assembly space: every part is built with its axis on local Z (Z = out of the
wall), inside an empty rotated so local Z == world +Y. The wall is world y=0.
"""
import bpy, bmesh, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = argv[0] if argv else "hero"
def opt(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
RES = [int(v) for v in opt("--res", "1920x1080").split("x")]
SAMPLES = int(opt("--samples", "768"))
HERE = os.path.dirname(os.path.abspath(__file__))
CAP = opt("--cap", "chrome")   # chrome | brass | black
OUT = opt("--out", os.path.join(HERE, f"sconce_{MODE}_{CAP}.png"))
EXPLODED = MODE == "exploded"
LED_S = float(opt("--led", "70"))
HDR_S = float(opt("--hdr", "0.12"))
RIP_W = float(opt("--rip", "0.0"))

# ---------------------------------------------------------------- dimensions (m)
IN = 0.0254
REC_R = 12 * IN / 2          # 0.1524
HOLE_R = 0.00362             # 7.24 mm spindle hole
LABEL_R = 0.0505
BP_R = 11 * IN / 2           # backplate 11"
BP_T = 0.014
SO_T = 0.004                 # standoff / spacer (record sits ~0.7" off the wall)
REC_T = 0.0019
WASH_T = 0.0022
DOME_R = 0.0203               # 1.6" dia dome
DOME_H = 0.0178               # 0.7" tall
RIM_R = 0.0213
RIM_H = 0.0016
WASH_R = 0.0222
REC_Z = BP_T + SO_T          # record back face ~ 1" off wall

# exploded offsets along the axis
OFF = dict(backplate=0.0, standoff=0.0, record=0.0, washer=0.0, screw=0.0)
if EXPLODED:
    OFF = dict(backplate=0.10, standoff=0.20, record=0.29, washer=0.38, screw=0.45)

# ---------------------------------------------------------------- reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def lathe(name, profile, steps=256):
    """Revolve a closed (r, z) profile around local Z."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0.0, z)) for r, z in profile]
    es = [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1),
                   angle=2 * math.pi, steps=steps, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    smooth(ob)
    return ob

def smooth(ob, angle=50):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))

# ---------------------------------------------------------------- node helpers
class NB:
    def __init__(self, mat):
        mat.use_nodes = True
        self.nt = mat.node_tree
        self.nt.nodes.clear()
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
            if isinstance(v, (int, float, tuple)):
                p.inputs[k].default_value = v if not isinstance(v, tuple) or len(v) != 3 else (*v, 1)
            else:
                self.link(v, p.inputs[k])
        return p

def obj_xyz(nb):
    tc = nb.n("ShaderNodeTexCoord")
    sep = nb.n("ShaderNodeSeparateXYZ")
    nb.link(tc.outputs["Object"], sep.inputs[0])
    return sep.outputs[0], sep.outputs[1], sep.outputs[2]

def radius_angle(nb):
    x, y, z = obj_xyz(nb)
    r = nb.math("SQRT", nb.math("ADD", nb.math("MULTIPLY", x, x), nb.math("MULTIPLY", y, y)))
    a = nb.math("ARCTAN2", y, x)
    return r, a, z

def band(nb, r, lo, hi):
    return nb.math("MULTIPLY", nb.math("GREATER_THAN", r, lo), nb.math("LESS_THAN", r, hi))

# ---------------------------------------------------------------- materials
def mat_vinyl():
    m = bpy.data.materials.new("Vinyl")
    nb = NB(m)
    r, a, z = radius_angle(nb)
    grooved = band(nb, r, 0.0605, 0.1462)
    gaps = None
    for ri in (0.0742, 0.0893, 0.1031, 0.1158, 0.1305):
        g = nb.math("COMPARE", r, ri)
        g.node.inputs[2].default_value = 0.0009
        gaps = g if gaps is None else nb.math("MAXIMUM", gaps, g)
    music = nb.math("MULTIPLY", grooved, nb.math("SUBTRACT", 1.0, gaps))
    # fine groove ripple (pitch ~0.3 mm) plus slower modulation = "loud" passages
    rip = nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0003))
    mod = nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0041))
    # (sub-pixel groove ripple is carried by the anisotropic BSDF; a bump that fine
    # just randomises normals and turns the disc grey)
    h = nb.math("MULTIPLY", music, nb.math("ADD", nb.math("MULTIPLY", rip, RIP_W),
                                           nb.math("MULTIPLY", mod, 0.3)))
    # run-out: a few widely spaced locked/lead-out grooves
    runout = band(nb, r, 0.051, 0.0605)
    ro = nb.math("MULTIPLY", runout, nb.math("GREATER_THAN",
                 nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0021)), 0.93))
    h = nb.math("ADD", h, nb.math("MULTIPLY", ro, -1.0))
    bump = nb.n("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.18
    bump.inputs["Distance"].default_value = 0.00002
    nb.link(h, bump.inputs["Height"])
    # roughness: music bands slightly rougher than the glassy gaps/run-out
    noise = nb.n("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 900
    rough = nb.math("ADD", nb.math("MULTIPLY", music, 0.05), 0.035)
    rough = nb.math("ADD", rough, nb.math("MULTIPLY", noise.outputs[0], 0.015))
    tan = nb.n("ShaderNodeTangent", direction_type="RADIAL", axis="Z")
    vin = nb.bsdf(**{"Base Color": (0.006, 0.006, 0.007), "Roughness": rough,
                     "Anisotropic": 0.0, "Specular IOR Level": 0.55})
    vin.inputs["Anisotropic"].default_value = 0.0
    an = nb.math("ADD", nb.math("MULTIPLY", music, 0.6), 0.1)
    nb.link(an, vin.inputs["Anisotropic"])
    nb.link(tan.outputs[0], vin.inputs["Tangent"])
    nb.link(bump.outputs[0], vin.inputs["Normal"])

    # paper label
    lab_noise = nb.n("ShaderNodeTexNoise")
    lab_noise.inputs["Scale"].default_value = 4000
    lab_noise.inputs["Detail"].default_value = 6
    lb = nb.n("ShaderNodeBump")
    lb.inputs["Strength"].default_value = 0.12
    nb.link(lab_noise.outputs[0], lb.inputs["Height"])
    ink = nb.math("MAXIMUM", band(nb, r, 0.0462, 0.0468), band(nb, r, 0.0236, 0.0240))
    paper = nb.n("ShaderNodeMix", data_type="RGBA")
    paper.inputs[6].default_value = (0.80, 0.72, 0.56, 1)
    paper.inputs[7].default_value = (0.20, 0.12, 0.08, 1)
    nb.link(ink, paper.inputs[0])
    lab = nb.bsdf(**{"Roughness": 0.62, "Specular IOR Level": 0.35})
    nb.link(paper.outputs[2], lab.inputs["Base Color"])
    nb.link(lb.outputs[0], lab.inputs["Normal"])

    is_label = nb.math("LESS_THAN", r, LABEL_R)
    mix = nb.n("ShaderNodeMixShader")
    nb.link(is_label, mix.inputs[0])
    nb.link(vin.outputs[0], mix.inputs[1])
    nb.link(lab.outputs[0], mix.inputs[2])
    nb.link(mix.outputs[0], nb.out.inputs[0])
    return m

def mat_chrome():
    m = bpy.data.materials.new("Chrome")
    nb = NB(m)
    p = nb.bsdf(**{"Base Color": (0.93, 0.93, 0.94), "Metallic": 1.0, "Roughness": 0.035})
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_black_chrome():
    m = bpy.data.materials.new("BlackChrome")
    nb = NB(m)
    p = nb.bsdf(**{"Base Color": (0.10, 0.10, 0.11), "Metallic": 1.0, "Roughness": 0.04,
                   "Coat Weight": 1.0, "Coat Roughness": 0.02})
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_brass(knurl=False, thread=False, polished=False):
    m = bpy.data.materials.new("Brass")
    nb = NB(m)
    r, a, z = radius_angle(nb)
    noise = nb.n("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 300
    rough = nb.math("ADD", nb.math("MULTIPLY", noise.outputs[0], 0.02 if polished else 0.06),
                    0.06 if polished else 0.24)
    p = nb.bsdf(**{"Base Color": (0.88, 0.62, 0.30), "Metallic": 1.0, "Roughness": rough,
                   "Anisotropic": 0.2 if polished else 0.7})
    tan = nb.n("ShaderNodeTangent", direction_type="RADIAL", axis="Z")
    nb.link(tan.outputs[0], p.inputs["Tangent"])
    h = None
    if knurl:   # diamond knurl on the cap side (local z 0.0015..0.0062)
        side = band(nb, z, 0.0012, 0.0064)
        k1 = nb.math("SINE", nb.math("ADD", nb.math("MULTIPLY", a, 36), nb.math("MULTIPLY", z, 2600)))
        k2 = nb.math("SINE", nb.math("SUBTRACT", nb.math("MULTIPLY", a, 36), nb.math("MULTIPLY", z, 2600)))
        h = nb.math("MULTIPLY", side, nb.math("MULTIPLY", k1, k2))
    if thread:  # threads on the shaft (local z < 0)
        sh = nb.math("LESS_THAN", z, -0.0002)
        t = nb.math("SINE", nb.math("MULTIPLY", z, 2 * math.pi / 0.0008))
        th = nb.math("MULTIPLY", sh, t)
        h = th if h is None else nb.math("ADD", h, th)
    if h is not None:
        b = nb.n("ShaderNodeBump")
        b.inputs["Strength"].default_value = 0.8
        b.inputs["Distance"].default_value = 0.0003
        nb.link(h, b.inputs["Height"])
        nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_simple(name, color, rough, metallic=0.0, sheen=0.0, bump_scale=None, bump_str=0.2, spec=0.5):
    m = bpy.data.materials.new(name)
    nb = NB(m)
    p = nb.bsdf(**{"Base Color": color, "Roughness": rough, "Metallic": metallic,
                   "Sheen Weight": sheen, "Sheen Roughness": 0.6, "Specular IOR Level": spec})
    if bump_scale:
        nz = nb.n("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = bump_scale
        nz.inputs["Detail"].default_value = 8
        b = nb.n("ShaderNodeBump")
        b.inputs["Strength"].default_value = bump_str
        nb.link(nz.outputs[0], b.inputs["Height"])
        nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_led(strength):
    m = bpy.data.materials.new("LED")
    nb = NB(m)
    r, a, z = radius_angle(nb)
    # discrete LED dots along the strip (~60/m) on a white PCB
    n_led = round(2 * math.pi * BP_R * 60)
    dot_a = nb.math("SINE", nb.math("MULTIPLY", a, n_led))
    dot = nb.math("GREATER_THAN", dot_a, 0.55)
    zc = band(nb, z, 0.0072, 0.0108)
    dot = nb.math("MULTIPLY", dot, zc)
    em = nb.n("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.42, 0.10, 1)   # warm amber 2200-2700K
    s = nb.math("ADD", nb.math("MULTIPLY", dot, strength), strength * 0.25)
    nb.link(s, em.inputs["Strength"])
    pcb = nb.bsdf(**{"Base Color": (0.85, 0.83, 0.78), "Roughness": 0.4})
    add = nb.n("ShaderNodeAddShader")
    nb.link(pcb.outputs[0], add.inputs[0])
    nb.link(em.outputs[0], add.inputs[1])
    nb.link(add.outputs[0], nb.out.inputs[0])
    return m

def mat_braid(y0):
    m = bpy.data.materials.new("Braid")
    nb = NB(m)
    x, y, z = obj_xyz(nb)
    a = nb.math("ARCTAN2", x, nb.math("SUBTRACT", y, y0))
    kz = nb.math("MULTIPLY", z, 2 * math.pi / 0.0045)
    p1 = nb.math("SINE", nb.math("ADD", kz, nb.math("MULTIPLY", a, 4)))
    p2 = nb.math("SINE", nb.math("SUBTRACT", kz, nb.math("MULTIPLY", a, 4)))
    weave = nb.math("MAXIMUM", p1, p2)
    fib = nb.n("ShaderNodeTexNoise")
    fib.inputs["Scale"].default_value = 3000
    h = nb.math("ADD", weave, nb.math("MULTIPLY", fib.outputs[0], 0.4))
    b = nb.n("ShaderNodeBump")
    b.inputs["Strength"].default_value = 0.9
    b.inputs["Distance"].default_value = 0.0006
    nb.link(h, b.inputs["Height"])
    col = nb.n("ShaderNodeMix", data_type="RGBA")
    col.inputs[6].default_value = (0.012, 0.010, 0.009, 1)
    col.inputs[7].default_value = (0.035, 0.03, 0.026, 1)
    nb.link(nb.math("MULTIPLY", nb.math("ADD", weave, 1), 0.5), col.inputs[0])
    p = nb.bsdf(**{"Roughness": 0.7, "Sheen Weight": 0.1, "Sheen Roughness": 0.5, "Specular IOR Level": 0.2})
    nb.link(col.outputs[2], p.inputs["Base Color"])
    nb.link(b.outputs[0], p.inputs["Normal"])
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

# ---------------------------------------------------------------- assembly root
root = bpy.data.objects.new("Assembly", None)
scene.collection.objects.link(root)
root.rotation_euler = (-math.pi / 2, 0, 0)   # local Z -> world +Y, local -Y -> world +Z
root.location = (0, 0, 0)

def place(ob, z):
    ob.parent = root
    ob.location = (0, 0, z)

# backplate (matte black, hidden behind the record)
bevel = 0.0012
bp = lathe("Backplate", [
    (0.0040, 0.0), (BP_R - bevel, 0.0), (BP_R, bevel), (BP_R, BP_T - bevel),
    (BP_R - bevel, BP_T), (0.0040, BP_T)])
bp.data.materials.append(mat_simple("BackplatePaint", (0.03, 0.03, 0.032), 0.75, spec=0.25, bump_scale=2500, bump_str=0.05))
place(bp, OFF["backplate"])

# LED strip on the backplate edge (emissive, wraps the rim)
led = lathe("LEDStrip", [(BP_R - 0.0002, 0.0050), (BP_R + 0.0008, 0.0050),
                         (BP_R + 0.0008, 0.0130), (BP_R - 0.0002, 0.0130)])
led.data.materials.append(mat_led(LED_S if not EXPLODED else 8.0))
place(led, OFF["backplate"])

# standoff spacer (black anodized)
so = lathe("Standoff", [(0.0035, 0.0), (0.0110, 0.0), (0.0115, 0.0005), (0.0115, SO_T - 0.0005),
                        (0.0110, SO_T), (0.0035, SO_T)], steps=96)
so.data.materials.append(mat_simple("Anodized", (0.025, 0.025, 0.027), 0.3, metallic=0.8))
place(so, BP_T + OFF["standoff"])

# vinyl record
rec = lathe("Record", [
    (HOLE_R, 0.0), (REC_R - 0.0005, 0.0), (REC_R, 0.0004), (REC_R, 0.0013),
    (REC_R - 0.0006, 0.0018), (0.1490, 0.0017), (0.1465, 0.0015), (0.0610, 0.0015),
    (0.0560, 0.0016), (0.0515, 0.0018), (LABEL_R, REC_T), (HOLE_R + 0.0002, REC_T),
    (HOLE_R, REC_T - 0.0002)], steps=512)
rec.data.materials.append(mat_vinyl())
place(rec, REC_Z + OFF["record"])

# fictional label text (record-local; rotated so it reads upright from the front)
ink = mat_simple("Ink", (0.20, 0.12, 0.08), 0.5)
font = None
try:
    font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Futura.ttc")
except Exception:
    pass
for body, size, yoff in (("HALO PRESSINGS", 0.0058, -0.032), ("SIDE A", 0.0040, 0.029),
                         ("33 1/3", 0.0036, 0.036)):
    cu = bpy.data.curves.new("txt", "FONT")
    cu.body = body
    cu.size = size
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    if font:
        cu.font = font
    t = bpy.data.objects.new("Label_" + body, cu)
    scene.collection.objects.link(t)
    t.data.materials.append(ink)
    t.parent = rec
    t.location = (0, yoff, REC_T + 0.00004)
    t.rotation_euler = (0, 0, math.pi)

# felt washer
wa = lathe("FeltWasher", [(0.0036, 0.0), (WASH_R, 0.0), (WASH_R + 0.0002, WASH_T * 0.5),
                          (WASH_R, WASH_T), (0.0036, WASH_T)], steps=128)
wa.data.materials.append(mat_simple("Felt", (0.085, 0.012, 0.012), 1.0, sheen=0.15, spec=0.1,
                                    bump_scale=6000, bump_str=0.4))
place(wa, REC_Z + REC_T + OFF["washer"])

# center cap: low mirror dome on a thin bezel ring, threaded post hidden underneath
# that runs back through the spindle hole into the backplate.
shaft_len = REC_Z + REC_T + WASH_T - 0.003
sph_R = (DOME_R ** 2 + DOME_H ** 2) / (2 * DOME_H)        # sphere radius of the cap
sph_c = RIM_H + DOME_H - sph_R                             # sphere centre (local z)
prof = [(0.0001, -shaft_len), (0.0030, -shaft_len), (0.0032, -shaft_len + 0.0006),
        (0.0032, 0.0), (RIM_R - 0.0004, 0.0), (RIM_R, 0.0004), (RIM_R, RIM_H - 0.0004),
        (RIM_R - 0.0004, RIM_H), (DOME_R + 0.0002, RIM_H), (DOME_R, RIM_H + 0.0002)]
a0 = math.asin(max(-1, min(1, (RIM_H + 0.0002 - sph_c) / sph_R)))
for i in range(1, 41):
    a = a0 + (math.pi / 2 - a0) * i / 40
    prof.append((max(sph_R * math.cos(a), 0.00005), sph_c + sph_R * math.sin(a)))
cap = lathe("DomeCap", prof, steps=256)
smooth(cap, angle=40)
dome_mat = {"chrome": mat_chrome, "brass": lambda: mat_brass(polished=True),
            "black": mat_black_chrome}[CAP]()
cap.data.materials.append(dome_mat)
# bezel: chrome on chrome/black, brass on brass. Assign the rim faces (z < RIM_H) a 2nd slot.
rim_mat = mat_brass(polished=True) if CAP == "brass" else mat_chrome()
cap.data.materials.append(rim_mat)
for poly in cap.data.polygons:
    zc = sum(cap.data.vertices[v].co.z for v in poly.vertices) / len(poly.vertices)
    poly.material_index = 1 if zc < RIM_H + 0.0001 else 0
place(cap, REC_Z + REC_T + WASH_T + OFF["screw"])

# braided cord: leaves the bottom of the backplate and drops along the wall
cord_cu = bpy.data.curves.new("Cord", "CURVE")
cord_cu.dimensions = "3D"
cord_cu.bevel_depth = 0.0034
cord_cu.bevel_resolution = 6
sp = cord_cu.splines.new("BEZIER")
y0 = 0.0070 + OFF["backplate"]
if EXPLODED:
    pts = [(0, y0, -BP_R + 0.02), (0, y0, -BP_R - 0.06), (0.03, y0 - 0.02, -BP_R - 0.20), (0.06, y0 - 0.05, -BP_R - 0.30)]
else:
    pts = [(0, y0, -BP_R + 0.02), (0, y0 - 0.002, -BP_R - 0.08), (0, 0.006, -0.9), (0.02, 0.008, -1.6)]
sp.bezier_points.add(len(pts) - 1)
for bpnt, p in zip(sp.bezier_points, pts):
    bpnt.co = p
    bpnt.handle_left_type = bpnt.handle_right_type = "AUTO"
cord = bpy.data.objects.new("Cord", cord_cu)
scene.collection.objects.link(cord)
cord.data.materials.append(mat_braid(y0))

# strain-relief grommet where the cord exits the backplate
gr = lathe("Grommet", [(0.0034, 0.0), (0.0060, 0.0), (0.0060, 0.0040), (0.0034, 0.0060)], steps=48)
gr.data.materials.append(mat_simple("Rubber", (0.02, 0.02, 0.02), 0.6))
gr.location = (0, y0, -BP_R + 0.004)
gr.rotation_euler = (math.pi, 0, 0)

# ---------------------------------------------------------------- environment
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
wnt = world.node_tree
bg = wnt.nodes["Background"]
hdr_dir = [d for d in __import__("glob").glob("/Applications/Blender.app/Contents/Resources/*/datafiles/studiolights/world")][0]
env = wnt.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(os.path.join(hdr_dir, "studio.exr" if EXPLODED else "interior.exr"))
mapn = wnt.nodes.new("ShaderNodeMapping")
tcw = wnt.nodes.new("ShaderNodeTexCoord")
wnt.links.new(tcw.outputs["Generated"], mapn.inputs[0])
mapn.inputs["Rotation"].default_value = (0, 0, math.radians(200))
wnt.links.new(mapn.outputs[0], env.inputs[0])
bg_hdr = wnt.nodes.new("ShaderNodeBackground")
wnt.links.new(env.outputs[0], bg_hdr.inputs[0])
lp = wnt.nodes.new("ShaderNodeLightPath")
mixw = wnt.nodes.new("ShaderNodeMixShader")
wnt.links.new(lp.outputs["Is Glossy Ray"], mixw.inputs[0])
wnt.links.new(bg.outputs[0], mixw.inputs[1])
wnt.links.new(bg_hdr.outputs[0], mixw.inputs[2])
wnt.links.new(mixw.outputs[0], wnt.nodes["World Output"].inputs[0])

def area(name, loc, target, size, power, color=(1, 1, 1), shape="RECTANGLE", size_y=None):
    ld = bpy.data.lights.new(name, "AREA")
    ld.shape = shape
    ld.size = size
    if size_y:
        ld.size_y = size_y
    ld.energy = power
    ld.color = color
    lo = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(lo)
    lo.location = loc
    d = Vector(target) - Vector(loc)
    lo.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return lo

if not EXPLODED:
    # big painted wall, warm off-white, eggshell
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    wall = bpy.context.active_object
    wall.data.materials.append(mat_simple("WallPaint", (0.82, 0.76, 0.66), 0.85,
                                          bump_scale=900, bump_str=0.03))
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 3, -1.6))
    floor = bpy.context.active_object
    floor.data.materials.append(mat_simple("Floor", (0.10, 0.07, 0.05), 0.45))
    bg.inputs[0].default_value = (0.040, 0.027, 0.015, 1)
    bg.inputs[1].default_value = 0.65
    bg_hdr.inputs[1].default_value = HDR_S
    # a dim, distant lamp across the room: gives the grooves and brass something to catch
    # lamp across the room roughly in the record's mirror direction: the grooves streak it
    area("RoomLamp", (-0.80, 1.40, 0.05), (0, 0.03, 0), 0.25, 3.5, color=(1.0, 0.78, 0.55), size_y=0.6)
    area("Fill", (1.8, 2.4, 0.9), (0, 0, 0), 1.5, 2.0, color=(1.0, 0.86, 0.72))
    cam_loc, cam_tgt, lens = (0.62, 1.12, 0.14), (0.04, 0.02, -0.02), 62
else:
    # wall section as its own slab so it reads as a part
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.015, 0))
    slab = bpy.context.active_object
    slab.scale = (0.40, 0.03, 0.40)
    slab.data.materials.append(mat_simple("WallPaint", (0.80, 0.76, 0.69), 0.85,
                                          bump_scale=900, bump_str=0.03))
    bg.inputs[0].default_value = (0.30, 0.295, 0.29, 1)
    bg.inputs[1].default_value = 0.6
    bg_hdr.inputs[1].default_value = 0.35
    area("Key", (1.4, 1.2, 1.3), (0, 0.25, 0), 1.6, 110, color=(1.0, 0.97, 0.93))
    area("Fill", (-1.2, 1.4, 0.5), (0, 0.25, 0), 2.0, 110)
    area("Rim", (0.4, -0.6, 1.4), (0, 0.25, 0), 1.0, 70)
    area("Under", (0.6, 1.0, -1.2), (0, 0.25, 0), 1.5, 40)
    # strip light in the record's mirror direction so the grooves streak
    area("Streak", (-1.0, 0.95, -0.15), (0, 0.31, 0), 0.12, 6, size_y=1.0)
    cam_loc, cam_tgt, lens = (1.10, 0.80, 0.30), (0.0, 0.225, -0.02), 52

cam_d = bpy.data.cameras.new("Cam")
cam_d.lens = lens
cam = bpy.data.objects.new("Cam", cam_d)
scene.collection.objects.link(cam)
cam.location = cam_loc
cam.rotation_euler = (Vector(cam_tgt) - Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam
if not EXPLODED:
    cam_d.dof.use_dof = True
    cam_d.dof.focus_distance = (Vector(cam_tgt) - Vector(cam_loc)).length
    cam_d.dof.aperture_fstop = 5.6

# ---------------------------------------------------------------- render
scene.render.engine = "CYCLES"
cy = scene.cycles
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    cy.device = "GPU"
except Exception as e:
    print("GPU setup failed, CPU:", e)
cy.samples = SAMPLES
cy.use_adaptive_sampling = True
cy.adaptive_threshold = 0.006
cy.use_denoising = True
cy.denoiser = "OPENIMAGEDENOISE"
cy.max_bounces = 10
cy.glossy_bounces = 6
cy.caustics_reflective = False
cy.caustics_refractive = False
cy.sample_clamp_indirect = 8.0
scene.render.resolution_x, scene.render.resolution_y = RES
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = "AgX"
try:
    scene.view_settings.look = "AgX - Medium High Contrast" if not EXPLODED else "AgX - Base Contrast"
except Exception:
    pass
scene.view_settings.exposure = float(opt("--exp", "0.35" if not EXPLODED else "0.0"))
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUT
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, f"sconce_{MODE}_{CAP}.blend"))
bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
