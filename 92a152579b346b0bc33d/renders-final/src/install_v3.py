"""Install cutaway v3 (from render/sconce_v2.py, original untouched): bigger sconce in frame,
halo ON, real label, warm dim room. Cycles only.
  Blender -b -P install_v3.py -- cutaway --aspect wide|square|tall [--preview] [--samples N]
(Based on) Record sconce v2: mounting plate + hub + in-wall wiring.

Usage:
  Blender -b -P sconce_v2.py -- cutaway  [--res 1920x1080] [--samples 384] [--out path.png]
  Blender -b -P sconce_v2.py -- rear     [--res 1920x1080] [--samples 384] [--out path.png]

Assembly space (as in sconce.py): parts are lathed on local Z (Z = out of the
wall) inside an empty rotated so local Z == world +Y. Wall face is world y=0,
world Z is up. In the cutaway the sconce centre is world z=0 and the floor is
60 in below it.

v2 adds (behind the backplate, hidden by the record in use):
  * 4 in steel mounting plate, 1 in centre hole, four arc slots (single-gang
    83.3 mm and round-box 88.9 mm spacing, #8 screws), three 8-32 shoulder
    screws as bayonet studs, set-screw tab at 6 o'clock.
  * 5 in x 1 in hub: rear recess for the plate, three J-slots, centre pocket
    with the DC barrel jack, 6 o'clock surface-cord channel.
  * CL2 18/2 cable leaving the hub's back centre through a 1 in hole in the
    drywall, down the stud bay to a keystone DC jack plate at outlet height,
    12 V UL adapter plugged into the existing receptacle.
"""
import bpy, bmesh, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = argv[0] if argv else "cutaway"
def opt(name, default):
    return argv[argv.index(name) + 1] if name in argv else default
ASPECT = opt("--aspect", "wide")
RES = list(dict(wide=(1920, 1080), square=(1600, 1600), tall=(1080, 1920))[ASPECT])
PREVIEW = "--preview" in argv
SAMPLES = int(opt("--samples", "384"))
HERE = os.path.dirname(os.path.abspath(__file__))
CAP = opt("--cap", "chrome")   # chrome | brass | black
OUT = opt("--out", os.path.join(HERE, "..", "preview" if PREVIEW else "png", f"install_{ASPECT}.png"))
REAR = MODE == "rear"
CUT = MODE == "cutaway"
LED_S = float(opt("--led", "160"))
LABELS = opt("--labels", "1") == "1"

# ---------------------------------------------------------------- dimensions (m)
IN = 0.0254
REC_R = 12 * IN / 2
HOLE_R = 0.00362
LABEL_R = 0.0505
BP_R = 10.5 * IN / 2         # backplate 10.5"
BP_T = 0.0127                # 1/2" MDF
SO_T = 0.004                 # felt pads
REC_T = 0.0019
WASH_T = 0.0022
DOME_R = 0.0203
DOME_H = 0.0178
RIM_R = 0.0213
RIM_H = 0.0016
WASH_R = 0.0222
HUB_R = 2.5 * IN             # hub 5"
HUB_T = 1.0 * IN             # hub 1" = wall gap
HUB_REC = 0.0065             # rear recess depth (plate + bayonet heads)
PLATE_R = 2.0 * IN           # steel plate 4"
PLATE_T = 0.0019             # 14 ga
PLATE_HOLE_R = 0.5 * IN      # 1" cable hole
BAY_R = 0.040                # bayonet stud circle
SLOT_R = 0.0425              # mounting-slot mean radius (covers 83.3 and 88.9 mm)
DW_T = 0.0127                # 1/2" drywall
WALL_HOLE_R = 0.5 * IN
CABLE_R = 0.0023             # 18/2 CL2 ~4.6 mm OD
REC_Z = HUB_T + BP_T + SO_T  # record back face

# exploded offsets along the axis (rear view)
OFF = dict(plate=0.0, hub=0.0, backplate=0.0, record=0.0, washer=0.0, screw=0.0)
if REAR:
    OFF = dict(plate=0.12, hub=0.24, backplate=0.40, record=0.52, washer=0.60, screw=0.67)

# ---------------------------------------------------------------- reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def smooth(ob, angle=50):
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))

def lathe(name, profile, steps=256, do_smooth=True):
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
    if do_smooth:
        smooth(ob)
    return ob

def box(name, size, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    if mat:
        ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob

def cyl(name, r, depth, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, parent=None, verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name = name
    if mat:
        ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob

def apply_all(ob):
    with bpy.context.temp_override(object=ob, active_object=ob, selected_objects=[ob],
                                   selected_editable_objects=[ob]):
        for m in list(ob.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)

def boolean_cut(target, cutters):
    """Subtract cutter objects (already positioned in target's parent space) from target."""
    for c in cutters:
        c.parent = target.parent
        c.hide_render = True
        c.hide_viewport = True
        m = target.modifiers.new("cut", "BOOLEAN")
        m.operation = "DIFFERENCE"
        m.solver = "EXACT"
        m.object = c
    apply_all(target)
    for c in cutters:
        bpy.data.objects.remove(c, do_unlink=True)

# ---------------------------------------------------------------- node helpers (from sconce.py)
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
    mod = nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0041))
    h = nb.math("MULTIPLY", music, nb.math("MULTIPLY", mod, 0.3))
    runout = band(nb, r, 0.051, 0.0605)
    ro = nb.math("MULTIPLY", runout, nb.math("GREATER_THAN",
                 nb.math("SINE", nb.math("MULTIPLY", r, 2 * math.pi / 0.0021)), 0.93))
    h = nb.math("ADD", h, nb.math("MULTIPLY", ro, -1.0))
    bump = nb.n("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.18
    bump.inputs["Distance"].default_value = 0.00002
    nb.link(h, bump.inputs["Height"])
    noise = nb.n("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 900
    rough = nb.math("ADD", nb.math("MULTIPLY", music, 0.05), 0.035)
    rough = nb.math("ADD", rough, nb.math("MULTIPLY", noise.outputs[0], 0.015))
    tan = nb.n("ShaderNodeTangent", direction_type="RADIAL", axis="Z")
    vin = nb.bsdf(**{"Base Color": (0.006, 0.006, 0.007), "Roughness": rough, "Specular IOR Level": 0.55})
    an = nb.math("ADD", nb.math("MULTIPLY", music, 0.6), 0.1)
    nb.link(an, vin.inputs["Anisotropic"])
    nb.link(tan.outputs[0], vin.inputs["Tangent"])
    nb.link(bump.outputs[0], vin.inputs["Normal"])
    lab_noise = nb.n("ShaderNodeTexNoise")
    lab_noise.inputs["Scale"].default_value = 4000
    lab_noise.inputs["Detail"].default_value = 6
    lb = nb.n("ShaderNodeBump")
    lb.inputs["Strength"].default_value = 0.12
    nb.link(lab_noise.outputs[0], lb.inputs["Height"])
    tc2 = nb.n("ShaderNodeTexCoord"); mp = nb.n("ShaderNodeMapping")
    mp.inputs["Location"].default_value = (0.5, 0.5, 0)
    mp.inputs["Scale"].default_value = (-1 / (2 * LABEL_R), -1 / (2 * LABEL_R), 1)
    nb.link(tc2.outputs["Object"], mp.inputs[0])
    paper = nb.n("ShaderNodeTexImage")
    paper.image = bpy.data.images.load(os.path.join(HERE, "..", "tex", "label_halo.png"))
    paper.extension = "EXTEND"
    nb.link(mp.outputs[0], paper.inputs[0])
    lab = nb.bsdf(**{"Roughness": 0.62, "Specular IOR Level": 0.35})
    nb.link(paper.outputs[0], lab.inputs["Base Color"])
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

def mat_brass(polished=True):
    m = bpy.data.materials.new("Brass")
    nb = NB(m)
    noise = nb.n("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 300
    rough = nb.math("ADD", nb.math("MULTIPLY", noise.outputs[0], 0.02), 0.06)
    p = nb.bsdf(**{"Base Color": (0.88, 0.62, 0.30), "Metallic": 1.0, "Roughness": rough, "Anisotropic": 0.2})
    tan = nb.n("ShaderNodeTangent", direction_type="RADIAL", axis="Z")
    nb.link(tan.outputs[0], p.inputs["Tangent"])
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

def mat_wood(name="Stud"):
    m = bpy.data.materials.new(name)
    nb = NB(m)
    tc = nb.n("ShaderNodeTexCoord")
    mp = nb.n("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0, 1.0, 0.05)
    nb.link(tc.outputs["Object"], mp.inputs[0])
    wave = nb.n("ShaderNodeTexWave")
    wave.inputs["Scale"].default_value = 60
    wave.inputs["Distortion"].default_value = 6
    wave.inputs["Detail"].default_value = 3
    nb.link(mp.outputs[0], wave.inputs[0])
    col = nb.n("ShaderNodeMix", data_type="RGBA")
    col.inputs[6].default_value = (0.78, 0.60, 0.38, 1)
    col.inputs[7].default_value = (0.58, 0.40, 0.22, 1)
    nb.link(wave.outputs[0], col.inputs[0])
    p = nb.bsdf(**{"Roughness": 0.75, "Specular IOR Level": 0.3})
    nb.link(col.outputs[2], p.inputs["Base Color"])
    nb.link(p.outputs[0], nb.out.inputs[0])
    return m

def mat_emit(name, color, strength=1.0):
    m = bpy.data.materials.new(name)
    nb = NB(m)
    em = nb.n("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    nb.link(em.outputs[0], nb.out.inputs[0])
    return m

def mat_led(strength):
    m = bpy.data.materials.new("LED")
    nb = NB(m)
    r, a, z = radius_angle(nb)
    n_led = round(2 * math.pi * BP_R * 60)
    dot_a = nb.math("SINE", nb.math("MULTIPLY", a, n_led))
    dot = nb.math("GREATER_THAN", dot_a, 0.55)
    zc = band(nb, z, 0.0032, 0.0098)
    dot = nb.math("MULTIPLY", dot, zc)
    em = nb.n("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.42, 0.10, 1)
    s = nb.math("ADD", nb.math("MULTIPLY", dot, strength), strength * 0.25)
    nb.link(s, em.inputs["Strength"])
    pcb = nb.bsdf(**{"Base Color": (0.85, 0.83, 0.78), "Roughness": 0.4})
    add = nb.n("ShaderNodeAddShader")
    nb.link(pcb.outputs[0], add.inputs[0])
    nb.link(em.outputs[0], add.inputs[1])
    nb.link(add.outputs[0], nb.out.inputs[0])
    return m

M = dict(
    steel=mat_simple("ZincSteel", (0.17, 0.18, 0.20), 0.50, metallic=0.25, bump_scale=400, bump_str=0.05),
    hub=mat_simple("HubPETG", (0.09, 0.09, 0.10), 0.55, spec=0.4, bump_scale=1500, bump_str=0.08),
    black=mat_simple("Black", (0.02, 0.02, 0.02), 0.5),
    drywall=mat_simple("Drywall", (0.80, 0.75, 0.67), 0.9, spec=0.2, bump_scale=600, bump_str=0.04),
    drywall_core=mat_simple("Gypsum", (0.80, 0.80, 0.78), 1.0, spec=0.1, bump_scale=900, bump_str=0.3),
    stud=mat_wood(),
    cable=mat_simple("CL2Jacket", (0.42, 0.44, 0.47), 0.45, spec=0.4),
    plastic=mat_simple("WhitePlastic", (0.92, 0.92, 0.90), 0.35, spec=0.5),
    chrome=mat_chrome(),
    felt=mat_simple("Felt", (0.085, 0.012, 0.012), 1.0, sheen=0.15, spec=0.1, bump_scale=6000, bump_str=0.4),
    bp=mat_simple("BackplatePaint", (0.03, 0.03, 0.032), 0.75, spec=0.25, bump_scale=2500, bump_str=0.05),
    label=mat_emit("LabelInk", (0.02, 0.02, 0.02), 1.0),
    leader=mat_emit("Leader", (0.05, 0.05, 0.05), 1.0),
)

# ---------------------------------------------------------------- assembly root
root = bpy.data.objects.new("Assembly", None)
scene.collection.objects.link(root)
root.rotation_euler = (-math.pi / 2, 0, 0)   # local Z -> world +Y, local -Y -> world +Z
# NOTE: local +Y -> world -Z (down). 12 o'clock on the wall is local -Y.
def place(ob, z, x=0.0, y=0.0):
    ob.parent = root
    ob.location = (x, y, z)

# ---------- steel mounting plate (4", 14 ga, zinc)
plate = lathe("MountPlate", [(PLATE_HOLE_R, 0.0), (PLATE_R - 0.0006, 0.0), (PLATE_R, 0.0006),
                             (PLATE_R, PLATE_T), (PLATE_HOLE_R, PLATE_T)], steps=192)
plate.data.materials.append(M["steel"])
plate.location = (0, 0, OFF["plate"])
# four arc slots for #8 screws (covers 83.3 mm single-gang and 88.9 mm round box spacing)
cutters = []
for k in range(4):
    ang = k * math.pi / 2 + math.pi / 4          # at 45/135/225/315 so 12 o'clock stays clear
    for j in (-1, 0, 1):
        a = ang + j * math.radians(9)
        cx, cy = SLOT_R * math.cos(a), SLOT_R * math.sin(a)
        c = cyl(f"slotcut{k}{j}", 0.0024, 0.02, loc=(cx, cy, OFF["plate"] + PLATE_T / 2))
        cutters.append(c)
        if j < 1:
            b = ang + (j + 0.5) * math.radians(9)
            bx, by = SLOT_R * math.cos(b), SLOT_R * math.sin(b)
            seg = box(f"slotbox{k}{j}", (SLOT_R * math.radians(9) * 1.05, 0.0048, 0.02),
                      loc=(bx, by, OFF["plate"] + PLATE_T / 2), rot=(0, 0, b + math.pi / 2))
            cutters.append(seg)
    # radial slot too (lets the plate hang on one stud screw first)
# set-screw tab hole at 6 o'clock (local +Y is down)
cutters.append(cyl("tabcut", 0.0012, 0.02, loc=(0, PLATE_R - 0.004, OFF["plate"] + PLATE_T / 2)))
boolean_cut(plate, cutters)
place(plate, OFF["plate"])

# bayonet studs: three 8-32 shoulder screws standing off the plate
for k in range(3):
    a = math.radians(90 + 120 * k) + math.pi   # one at 6 o'clock-ish, others 120 deg
    sx, sy = BAY_R * math.cos(a), BAY_R * math.sin(a)
    sh = lathe(f"Bayonet{k}", [(0.0001, 0.0), (0.0024, 0.0), (0.0024, 0.0032), (0.0044, 0.0032),
                               (0.0044, 0.0050), (0.0036, 0.0054), (0.0001, 0.0054)], steps=48)
    sh.data.materials.append(M["chrome"])
    place(sh, OFF["plate"] + PLATE_T, x=sx, y=sy)

# wall screws (#8 pan head) in two of the slots, with drywall anchors behind
def wall_screw(name, x, y, z_plate):
    s = lathe(name, [(0.0001, -0.028), (0.0012, -0.026), (0.0021, -0.004), (0.0021, 0.0),
                     (0.0045, 0.0), (0.0045, 0.0012), (0.0030, 0.0026), (0.0001, 0.0028)], steps=48)
    s.data.materials.append(M["steel"])
    place(s, z_plate + PLATE_T, x=x, y=y)
    an = lathe(name + "_anchor", [(0.0022, -0.030), (0.0046, -0.030), (0.0046, -0.001), (0.0060, -0.001),
                                  (0.0060, 0.0), (0.0022, 0.0)], steps=32)
    an.data.materials.append(mat_simple("Anchor", (0.85, 0.80, 0.30), 0.6))
    place(an, 0.0 if REAR else z_plate, x=x, y=y)
for k in range(4):
    ang = k * math.pi / 2 + math.pi / 4
    wall_screw(f"WallScrew{k}", SLOT_R * math.cos(ang), SLOT_R * math.sin(ang), OFF["plate"])

# ---------- hub (5" x 1", printed PETG)
POCKET_R = 0.0135
POCKET_D = 0.0165
bev = 0.0012
hub = lathe("Hub", [
    (POCKET_R, POCKET_D), (POCKET_R, HUB_REC), (PLATE_R + 0.0015, HUB_REC), (PLATE_R + 0.0015, 0.0),
    (HUB_R - bev, 0.0), (HUB_R, bev), (HUB_R, HUB_T - bev), (HUB_R - bev, HUB_T), (0.0001, HUB_T),
    (0.0001, POCKET_D)], steps=192)
hub.data.materials.append(M["hub"])
cut = []
# three J-slots: round entry + short arc, pockets in the rear web
for k in range(3):
    a = math.radians(90 + 120 * k) + math.pi
    ex, ey = BAY_R * math.cos(a), BAY_R * math.sin(a)
    cut.append(cyl(f"jent{k}", 0.0052, 0.03, loc=(ex, ey, HUB_REC + 0.004)))
    for j in range(1, 7):
        b = a - math.radians(3.2 * j)            # arc goes one way: twist to lock
        cut.append(cyl(f"jarc{k}{j}", 0.0030, 0.03, loc=(BAY_R * math.cos(b), BAY_R * math.sin(b), HUB_REC + 0.004)))
# surface-cord channel at 6 o'clock (local +Y) from the pocket to the rim, in the rear face
cut.append(box("chan", (0.0095, HUB_R - POCKET_R + 0.01, 0.012),
               loc=(0, (HUB_R + POCKET_R) / 2, HUB_REC + 0.0), rot=(0, 0, 0)))
# set-screw hole, radial at 6 o'clock
cut.append(cyl("setcut", 0.0016, 0.03, loc=(0, HUB_R - 0.008, HUB_REC / 2), rot=(math.pi / 2, 0, 0)))
boolean_cut(hub, cut)
place(hub, OFF["hub"])
# barrel jack (panel-mount 5.5x2.1) at the bottom of the pocket
jack = lathe("BarrelJack", [(0.0028, 0.0), (0.0055, 0.0), (0.0055, 0.0018), (0.0040, 0.0018),
                            (0.0040, 0.0120), (0.0028, 0.0120)], steps=48)
jack.data.materials.append(M["black"])
place(jack, OFF["hub"] + POCKET_D - 0.0121)
# set screw (M3 black, in the hub rim at 6 o'clock)
ss = cyl("SetScrew", 0.0014, 0.010, loc=(0, HUB_R - 0.004, OFF["hub"] + HUB_REC / 2), rot=(math.pi / 2, 0, 0), mat=M["black"])
ss.parent = root

# ---------- backplate + LED ring + insert
bp = lathe("Backplate", [
    (0.0050, 0.0), (BP_R - bev, 0.0), (BP_R, bev), (BP_R, BP_T - bev), (BP_R - bev, BP_T), (0.0050, BP_T)])
bp.data.materials.append(M["bp"])
place(bp, HUB_T + OFF["backplate"])
led = lathe("LEDStrip", [(BP_R - 0.0002, 0.0030), (BP_R + 0.0008, 0.0030),
                         (BP_R + 0.0008, 0.0100), (BP_R - 0.0002, 0.0100)])
led.data.materials.append(mat_led(LED_S * 0.25))
cob = lathe("COB", [(BP_R - 0.014, -0.0012), (BP_R - 0.004, -0.0012), (BP_R - 0.004, 0.0), (BP_R - 0.014, 0.0)], do_smooth=False)
cob.data.materials.append(mat_emit("COBEmit", (1.0, 0.42, 0.10), LED_S * 0.45))
place(cob, HUB_T + OFF["backplate"])
place(led, HUB_T + OFF["backplate"])
ins = lathe("Insert", [(0.0032, 0.0), (0.0050, 0.0), (0.0050, BP_T), (0.0032, BP_T)], steps=48)
ins.data.materials.append(mat_brass())
place(ins, HUB_T + OFF["backplate"])
# felt pads (6)
for i in range(6):
    rr = 5.0 * IN if i < 3 else 2.75 * IN
    a = math.radians(-90 + 120 * (i % 3))
    pad = cyl(f"Pad{i}", 0.00635, SO_T, loc=(rr * math.cos(a), rr * math.sin(a), HUB_T + BP_T + SO_T / 2 + OFF["backplate"]), mat=M["felt"], verts=32)
    pad.parent = root

# ---------- record
rec = lathe("Record", [
    (HOLE_R, 0.0), (REC_R - 0.0005, 0.0), (REC_R, 0.0004), (REC_R, 0.0013),
    (REC_R - 0.0006, 0.0018), (0.1490, 0.0017), (0.1465, 0.0015), (0.0610, 0.0015),
    (0.0560, 0.0016), (0.0515, 0.0018), (LABEL_R, REC_T), (HOLE_R + 0.0002, REC_T),
    (HOLE_R, REC_T - 0.0002)], steps=512)
rec.data.materials.append(mat_vinyl())
place(rec, REC_Z + OFF["record"])

# ---------- felt washer
wa = lathe("FeltWasher", [(0.0036, 0.0), (WASH_R, 0.0), (WASH_R + 0.0002, WASH_T * 0.5),
                          (WASH_R, WASH_T), (0.0036, WASH_T)], steps=128)
wa.data.materials.append(M["felt"])
place(wa, REC_Z + REC_T + OFF["washer"])

# ---------- dome cap on 1/4-20 stud
shaft_len = REC_T + WASH_T + SO_T + BP_T - 0.002
sph_R = (DOME_R ** 2 + DOME_H ** 2) / (2 * DOME_H)
sph_c = RIM_H + DOME_H - sph_R
prof = [(0.0001, -shaft_len), (0.0030, -shaft_len), (0.0032, -shaft_len + 0.0006),
        (0.0032, 0.0), (RIM_R - 0.0004, 0.0), (RIM_R, 0.0004), (RIM_R, RIM_H - 0.0004),
        (RIM_R - 0.0004, RIM_H), (DOME_R + 0.0002, RIM_H), (DOME_R, RIM_H + 0.0002)]
a0 = math.asin(max(-1, min(1, (RIM_H + 0.0002 - sph_c) / sph_R)))
for i in range(1, 41):
    a = a0 + (math.pi / 2 - a0) * i / 40
    prof.append((max(sph_R * math.cos(a), 0.00005), sph_c + sph_R * math.sin(a)))
cap = lathe("DomeCap", prof, steps=256)
smooth(cap, angle=40)
cap.data.materials.append({"chrome": mat_chrome, "brass": mat_brass, "black": mat_black_chrome}[CAP]())
place(cap, REC_Z + REC_T + WASH_T + OFF["screw"])

# ---------------------------------------------------------------- cable helper
def tube(name, pts, r, mat, parent=None, smooth_handles=True):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for b, p in zip(sp.bezier_points, pts):
        b.co = p
        b.handle_left_type = b.handle_right_type = "AUTO" if smooth_handles else "VECTOR"
    ob = bpy.data.objects.new(name, cu)
    scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob

def barrel_plug(name, z0, parent):
    """5.5x2.1 barrel plug pointing +Z (into the jack), body behind it."""
    p = lathe(name, [(0.0001, 0.0), (0.0027, 0.0), (0.0027, 0.009), (0.0050, 0.009), (0.0050, 0.030),
                     (0.0035, 0.034), (0.0001, 0.034)], steps=48)
    p.data.materials.append(M["black"])
    p.parent = parent
    p.location = (0, 0, z0)
    p.rotation_euler = (math.pi, 0, 0)   # tip at z0 pointing down -Z in local... flip so tip points +Z
    return p

# ---------------------------------------------------------------- labels
LABEL_ITEMS = []   # (text, anchor_world, label_world)
def label(text, anchor, pos):
    LABEL_ITEMS.append((text, Vector(anchor), Vector(pos)))

def build_labels(cam, size):
    if not LABELS:
        return
    font = None
    try:
        font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    except Exception:
        pass
    for i, (text, anchor, pos) in enumerate(LABEL_ITEMS):
        cu = bpy.data.curves.new(f"lbl{i}", "FONT")
        cu.body = text
        d0 = (LABEL_ITEMS[0][2] - cam.location).length
        sz = size * max(1.0, (pos - cam.location).length / d0)   # keep far labels readable
        cu.size = sz
        right = cam.rotation_euler.to_matrix() @ Vector((1, 0, 0))
        cu.align_x = "LEFT" if (pos - anchor).dot(right) > 0 else "RIGHT"
        cu.align_y = "CENTER"
        cu.extrude = 0.0
        if font:
            cu.font = font
        t = bpy.data.objects.new(f"Label{i}", cu)
        scene.collection.objects.link(t)
        t.data.materials.append(M["label"])
        t.location = pos
        t.rotation_euler = cam.rotation_euler
        # leader from the anchor to the label edge
        gap = right * (sz * 0.3) * (1 if cu.align_x == "LEFT" else -1)
        tube(f"leader{i}", [tuple(anchor), tuple(pos - gap)], size * 0.045, M["leader"], smooth_handles=False)
        # small dot at the anchor
        d = cyl(f"dot{i}", size * 0.08, size * 0.08, loc=tuple(anchor), mat=M["leader"], verts=16)
        d.rotation_euler = cam.rotation_euler

# ---------------------------------------------------------------- scene per mode
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
wnt = world.node_tree
bg = wnt.nodes["Background"]
hdr_dir = [d for d in __import__("glob").glob("/Applications/Blender.app/Contents/Resources/*/datafiles/studiolights/world")][0]
env = wnt.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(os.path.join(hdr_dir, "studio.exr"))
mapn = wnt.nodes.new("ShaderNodeMapping")
tcw = wnt.nodes.new("ShaderNodeTexCoord")
wnt.links.new(tcw.outputs["Generated"], mapn.inputs[0])
mapn.inputs["Rotation"].default_value = (0, 0, math.radians(200))
wnt.links.new(mapn.outputs[0], env.inputs[0])
bg_hdr = wnt.nodes.new("ShaderNodeBackground")
wnt.links.new(env.outputs[0], bg_hdr.inputs[0])
lp = wnt.nodes.new("ShaderNodeLightPath")
mixw = wnt.nodes.new("ShaderNodeMixShader")
wnt.links.new(lp.outputs["Is Camera Ray"], mixw.inputs[0])
wnt.links.new(bg_hdr.outputs[0], mixw.inputs[1])
wnt.links.new(bg.outputs[0], mixw.inputs[2])
wnt.links.new(mixw.outputs[0], wnt.nodes["World Output"].inputs[0])
bg.inputs[0].default_value = (0.42, 0.42, 0.41, 1)   # flat studio grey seen by camera
bg.inputs[1].default_value = 1.0
bg_hdr.inputs[1].default_value = 0.35

def area(name, loc, target, size, power, color=(1, 1, 1), size_y=None):
    ld = bpy.data.lights.new(name, "AREA")
    ld.shape = "RECTANGLE" if size_y else "SQUARE"
    ld.size = size
    if size_y:
        ld.size_y = size_y
    ld.energy = power
    ld.color = color
    lo = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(lo)
    lo.location = loc
    lo.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return lo

cam_d = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam
def aim(loc, tgt, lens):
    cam.location = loc
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = lens

if CUT:
    FLOOR = -60 * IN                     # sconce centre 60" above floor
    OUT_Z = FLOOR + 12 * IN              # receptacle centre 12" above floor
    LV_X = 0.0                            # keystone plate right under the cable
    RCPT_X = -0.115                       # existing duplex receptacle to its left
    STUD_X = 8 * IN                       # 16" o.c. -> stud centres at +-8"
    STUD_W, STUD_D = 1.5 * IN, 3.5 * IN
    BAY_Y0 = -DW_T                        # back of front drywall
    BAY_Y1 = -DW_T - STUD_D               # front of back drywall
    WIN_TOP = 0.0                         # window top: through the hole centre
    WIN_BOT = OUT_Z + 2.25 * IN + 0.03    # window bottom: 1.2" above the LV plate top
    WALL_L, WALL_R = -1.4, 1.2
    WALL_TOP = 1.0

    # front drywall as four slabs around the window (between the stud inner faces)
    bay_l, bay_r = -STUD_X + STUD_W / 2, STUD_X - STUD_W / 2
    def slab(name, x0, x1, z0, z1):
        s = box(name, (x1 - x0, DW_T, z1 - z0), loc=((x0 + x1) / 2, -DW_T / 2, (z0 + z1) / 2))
        s.data.materials.append(M["drywall"])
        s.data.materials.append(M["drywall_core"])
        # cut faces get the gypsum core material
        for p in s.data.polygons:
            n = p.normal
            if abs(n.y) < 0.5:
                p.material_index = 1
        return s
    slab("DW_left", WALL_L, bay_l, FLOOR, WALL_TOP)
    slab("DW_right", bay_r, WALL_R, FLOOR, WALL_TOP)
    slab("DW_bot", bay_l, bay_r, FLOOR, WIN_BOT)
    top = slab("DW_top", bay_l, bay_r, WIN_TOP, WALL_TOP)
    # 1" cable hole through the top slab (its lower half is cut by the window edge)
    hole = cyl("holecut", WALL_HOLE_R, 0.1, loc=(0, -DW_T / 2, 0), rot=(math.pi / 2, 0, 0))
    hole.parent = None
    m = top.modifiers.new("hole", "BOOLEAN"); m.operation = "DIFFERENCE"; m.solver = "EXACT"; m.object = hole
    hole.hide_render = True
    apply_all(top)
    bpy.data.objects.remove(hole, do_unlink=True)
    # studs, plates, back drywall
    for sx in (-STUD_X, STUD_X):
        box("Stud", (STUD_W, STUD_D, WALL_TOP - FLOOR), loc=(sx, (BAY_Y0 + BAY_Y1) / 2, (FLOOR + WALL_TOP) / 2), mat=M["stud"])
    box("SolePlate", (bay_r - bay_l, STUD_D, STUD_W), loc=(0, (BAY_Y0 + BAY_Y1) / 2, FLOOR + STUD_W / 2), mat=M["stud"])
    box("BackDrywall", (WALL_R - WALL_L, DW_T, WALL_TOP - FLOOR), loc=((WALL_L + WALL_R) / 2, BAY_Y1 - DW_T / 2, (FLOOR + WALL_TOP) / 2),
        mat=mat_simple("BackDW", (0.36, 0.35, 0.34), 0.9, spec=0.1))
    # floor + baseboard
    box("Floor", (4.0, 3.0, 0.02), loc=(0.2, 1.5, FLOOR - 0.01), mat=mat_simple("Floor", (0.32, 0.22, 0.14), 0.5, bump_scale=200, bump_str=0.05))
    box("Baseboard", (WALL_R - bay_r, 0.012, 3.5 * IN), loc=((bay_r + WALL_R) / 2, 0.006, FLOOR + 1.75 * IN), mat=M["plastic"])
    box("Baseboard2", (bay_l - WALL_L, 0.012, 3.5 * IN), loc=((WALL_L + bay_l) / 2, 0.006, FLOOR + 1.75 * IN), mat=M["plastic"])

    # keystone DC jack plate on a low-voltage old-work bracket
    PLATE_W, PLATE_H = 2.75 * IN, 4.5 * IN
    box("LVPlate", (PLATE_W, 0.006, PLATE_H), loc=(LV_X, 0.003, OUT_Z), mat=M["plastic"])
    box("Keystone", (0.016, 0.004, 0.020), loc=(LV_X, 0.007, OUT_Z), mat=M["black"])
    # the in-wall bracket, visible only as a thin flange behind the plate edge (hidden); skip
    # existing duplex receptacle (Decora style)
    box("RcptPlate", (PLATE_W, 0.006, PLATE_H), loc=(RCPT_X, 0.003, OUT_Z), mat=M["plastic"])
    box("RcptFace", (0.033, 0.004, 0.067), loc=(RCPT_X, 0.007, OUT_Z), mat=M["plastic"])
    for dz in (-0.019,):
        for dx, w, h in ((-0.006, 0.0025, 0.008), (0.006, 0.0025, 0.008), (0.0, 0.005, 0.005)):
            box("Prong", (w, 0.004, h), loc=(RCPT_X + dx, 0.0095, OUT_Z + dz + (-0.006 if dx == 0 else 0.003)), mat=M["black"])
    # 12 V UL adapter plugged into the top receptacle
    wart = box("Adapter", (0.042, 0.038, 0.062), loc=(RCPT_X, 0.009 + 0.019, OUT_Z + 0.019), mat=M["plastic"])
    # bevel the adapter
    bm_ = wart.modifiers.new("bev", "BEVEL"); bm_.width = 0.004; bm_.segments = 4
    apply_all(wart)
    smooth(wart, 40)
    # adapter DC lead -> keystone jack (short loop on the wall surface)
    tube("AdapterLead", [(RCPT_X, 0.028, OUT_Z - 0.012), (RCPT_X, 0.030, OUT_Z - 0.06),
                         ((RCPT_X + LV_X) / 2, 0.022, OUT_Z - 0.075), (LV_X, 0.018, OUT_Z - 0.045), (LV_X, 0.014, OUT_Z - 0.008)],
         0.0018, M["black"])
    lead_plug = cyl("LeadPlug", 0.0045, 0.022, loc=(LV_X, 0.022, OUT_Z), rot=(math.pi / 2, 0, 0), mat=M["black"])

    # CL2 cable: hub pocket -> through the hole -> down the bay -> behind the plate
    tube("CL2", [(0, HUB_T * 0 + 0.010, 0.0), (0, -0.030, -0.004), (0.004, -0.062, -0.09),
                 (-0.006, -0.062, -0.55), (0.004, -0.060, -1.00), (0, -0.045, OUT_Z + 0.09),
                 (0, -0.020, OUT_Z + 0.04)], CABLE_R, M["cable"])

    # labels (anchor -> text position), all in world space
    LX, LY = dict(wide=(-0.19, 0.10), square=(-0.24, 0.10), tall=(-0.165, 0.10))[ASPECT]
    label("Steel mounting plate, 4 screws", (0.052, 0.003, 0.03), (LX, LY, 0.16))
    label("Hub: bayonet twist + set screw", (0.064, 0.012, -0.03), (LX, LY, 0.07))
    label("Cable exits hub back, 1 in hole", (0.0, -0.02, -0.01), (LX, LY, -0.02))
    label("Record swaps from the front", (0.08, 0.055, -0.13), (LX, LY, -0.11))
    label("Surface option: cord out at 6 o'clock", (0.0, 0.012, -HUB_R), (LX, LY, -0.21))
    label("CL2 18/2 cable inside the stud bay", (0.0, -0.062, -0.60), (LX, LY, -0.58))
    label("Keystone DC jack plate", (LV_X + 0.035, 0.006, OUT_Z + 0.03), (LX, LY, OUT_Z + 0.10))
    label("12 V adapter stays at the outlet", (RCPT_X + 0.021, 0.045, OUT_Z + 0.03), (LX, LY, OUT_Z - 0.02))

    CAMS = dict(wide=((0.50, 0.78, 0.42), (-0.07, 0.0, -0.40), 15.5),
                square=((0.50, 0.86, 0.18), (-0.05, 0.0, -0.50), 19.0),
                tall=((0.70, 1.45, -0.28), (-0.05, 0.0, -0.53), 36.0))
    c = CAMS[ASPECT]
    aim(c[0], c[1], float(opt("--lens", str(c[2]))))
    bg.inputs[0].default_value = (0.05, 0.04, 0.032, 1)
    bg_hdr.inputs[1].default_value = 0.08
    area("Key", (1.2, 2.6, 1.0), (0, 0, -0.5), 2.0, 4, color=(1.0, 0.85, 0.7))
    area("Fill", (-2.0, 2.0, 0.2), (0, 0, -0.6), 2.5, 1.5, color=(1.0, 0.9, 0.8))
    area("Bay", (-0.3, 0.9, -0.5), (0, -0.06, -0.6), 0.3, 9, size_y=1.6, color=(1.0, 0.9, 0.8))
    LABEL_SIZE = dict(wide=0.028, square=0.028, tall=0.021)[ASPECT]
else:
    # rear 3/4 exploded: drywall section with the hole, parts fanned along the axis
    S = 0.30
    slab = box("Drywall", (S, DW_T, S), loc=(0, -DW_T / 2, 0))
    slab.data.materials.append(M["drywall"])
    slab.data.materials.append(M["drywall_core"])
    for p in slab.data.polygons:
        if abs(p.normal.y) < 0.5:
            p.material_index = 1
    hole = cyl("holecut", WALL_HOLE_R, 0.1, loc=(0, -DW_T / 2, 0), rot=(math.pi / 2, 0, 0))
    m = slab.modifiers.new("hole", "BOOLEAN"); m.operation = "DIFFERENCE"; m.solver = "EXACT"; m.object = hole
    hole.hide_render = True
    apply_all(slab)
    bpy.data.objects.remove(hole, do_unlink=True)
    # cable: from the hub pocket (exploded) back through the hole and away behind the wall
    zc = OFF["hub"] + POCKET_D - 0.0125
    plug = barrel_plug("CablePlug", OFF["hub"] - 0.012, root)
    plug.rotation_euler = (0, 0, 0)
    plug.location = (0, 0, OFF["hub"] - 0.012 - 0.0)
    tube("CL2", [(0, OFF["hub"] - 0.012 - 0.034 + 0.002, 0), (0, OFF["plate"] - 0.01, 0.0), (0, -0.02, 0.0),
                 (0, -0.12, -0.03), (0.02, -0.20, -0.20)], CABLE_R, M["cable"])
    # labels
    ZA, ZB = 0.20, -0.22
    label("Drywall, 1 in hole", (0.0, -0.002, 0.10), (0.0, -0.05, ZA + 0.08))
    label("Steel plate: arc slots fit single-gang or round box, anchors or a stud", (0.0, OFF["plate"], -PLATE_R), (0.0, 0.12, ZB - 0.14))
    label("CL2 18/2 cable, barrel plug into the hub jack", (0.0, OFF["hub"] - 0.03, -0.005), (0.0, 0.17, ZA + 0.08))
    label("Hub: bayonet slots, set screw at 6 o'clock, cable pocket", (0.0, OFF["hub"] + 0.003, HUB_R), (0.0, 0.21, ZA))
    label("Backplate: LED ring on the rim, 1/4-20 insert", (0.0, HUB_T + OFF["backplate"] + 0.004, -BP_R), (0.0, 0.42, ZB - 0.04))
    label("Record (customer's own)", (0.0, REC_Z + OFF["record"], REC_R), (0.0, 0.54, ZA + 0.08))
    label("Felt washer", (0.0, REC_Z + REC_T + OFF["washer"], -WASH_R), (0.0, 0.62, ZB - 0.14))
    label("Chrome dome, 1/4-20 stud", (0.0, REC_Z + REC_T + WASH_T + OFF["screw"] + 0.006, DOME_R), (0.0, 0.73, ZA))

    aim((1.25, -0.30, 0.62), (0.0, 0.30, -0.02), 40)
    bg.inputs[0].default_value = (0.62, 0.62, 0.61, 1)
    area("Key", (1.2, -0.3, 1.2), (0, 0.3, 0), 1.6, 55, color=(1.0, 0.97, 0.93))
    area("Fill", (0.9, 1.4, 0.3), (0, 0.3, 0), 2.0, 35)
    area("Rim", (-0.8, 0.9, 0.9), (0, 0.3, 0), 1.0, 30)
    area("Under", (0.8, 0.2, -1.1), (0, 0.3, 0), 1.5, 18)
    LABEL_SIZE = 0.013

build_labels(cam, LABEL_SIZE)

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
cy.adaptive_threshold = 0.008
cy.use_denoising = True
cy.denoiser = "OPENIMAGEDENOISE"
cy.max_bounces = 8
cy.glossy_bounces = 4
cy.caustics_reflective = False
cy.caustics_refractive = False
cy.sample_clamp_indirect = 6.0
scene.render.resolution_x, scene.render.resolution_y = RES
scene.render.resolution_percentage = int(opt("--pct", "25")) if PREVIEW else 100
scene.view_settings.view_transform = "AgX"
try:
    scene.view_settings.look = "AgX - Base Contrast"
except Exception:
    pass
scene.view_settings.exposure = float(opt("--exp", "-1.0"))
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = OUT

bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
