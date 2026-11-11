"""Labelled exploded view of the 12 in MDF sconce, from the live CAD (sconce_cad.py / assembly.py).
  .venv/bin/python explode_view.py export
  /Applications/Blender.app/Contents/MacOS/Blender -b -P explode_view.py -- render <out.png> [main|centre]
  .venv/bin/python explode_view.py annotate <render.png> <out.png> [main|centre]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, ".render-tmp", "explode")
MAN = os.path.join(TMP, "manifest.json")

# explode offset (mm along the wall normal) per part-name prefix; first match wins
# 2026-11-11 heat-safe halo: the strip, the aluminium ring, the cork ring and their 4 screws come from the canonical CAD
# (assembly.build) and explode between the hub and the backplate, in their real order.
OFFSETS = [("wall_screw_head", 55), ("wall_plate", 0), ("pem_stud", 0), ("lock_nut", 0),
           ("hub", 120), ("pigtail_cord", 120), ("cord_p_clip", 120), ("inline_jack", 120), ("adapter_plug", 120),
           ("set_screw_m3", 120), ("heat_ring_screw", 158), ("led_cob_strip", 185), ("heat_ring_alu", 222), ("cork_ring", 259),
           ("backplate", 310), ("ez_lok_insert", 310),
           ("felt_pads", 365), ("centre_backing_ring", 365), ("record", 560), ("pet_label_washer", 660),
           ("felt_washer", 710), ("dome_cap", 780)]
# callout groups: key -> (part-name prefixes, number, title, plain-English line)
CALLOUTS = [
    ("wall",   ("wall_plate",), "1", "Steel wall plate", "Screws to the wall or a junction box. Three studs stick out of it."),
    ("hub",    ("hub",), "2", "Hub", "Twists onto the three studs and locks with one small screw. Holds the power lead."),
    ("power",  ("inline_jack", "adapter_plug", "pigtail_cord"), "3", "Power lead", "Short 12 V pigtail with a plug-in connector. The wall adapter cable plugs in here."),
    ("led",    ("led_cob_strip",), "4", "LED strip", "Warm strip on the back, facing the wall. This is the halo. It cannot see the record."),
    ("alu",    ("heat_ring_alu",), "5", "Aluminium ring", "Thin metal ring the strip sticks to. Spreads the heat. Four small screws hold it on."),
    ("cork",   ("cork_ring",), "6", "Cork ring", "A thin layer of cork (1/16 in) between the warm metal ring and the wood."),
    ("bp",     ("backplate",), "7", "Backplate", "Black 1/2 in MDF disc, a little smaller than the record. Brass threaded insert in the centre."),
    ("pads",   ("felt_pads", "centre_backing_ring"), "8", "Felt pads + centre ring", "The record rests on these, so it never touches wood and cannot dish."),
    ("record", ("record",), "9", "Your record", "Any 12 in LP. Nothing is glued, drilled or modified."),
    ("pet",    ("pet_label_washer",), "10", "Clear label washer", "Thin clear disc that protects the paper label."),
    ("felt",   ("felt_washer",), "11", "Felt washer", "Cushion between the chrome and the label."),
    ("cap",    ("dome_cap",), "12", "Chrome dome cap", "Solid brass, chrome plated, screw built in. Goes through the record's hole into the brass insert."),
]
COLORS = {"steel": (0.55, 0.57, 0.60), "chrome": (0.9, 0.9, 0.92), "nut": (0.6, 0.6, 0.55), "petg": (0.10, 0.11, 0.13),
          "black": (0.02, 0.02, 0.02), "mdf": (0.035, 0.035, 0.04), "alu": (0.6, 0.62, 0.65), "brass": (0.8, 0.6, 0.25),
          "led": (1.0, 0.7, 0.35), "felt": (0.62, 0.55, 0.44), "vinyl": (0.012, 0.012, 0.014), "plastic": (0.05, 0.05, 0.05),
          "pet": (0.8, 0.9, 1.0), "cork": (0.55, 0.38, 0.22)}
METAL = {"steel": 1, "chrome": 1, "nut": 1, "alu": 1, "brass": 1}
ROUGH = {"chrome": 0.06, "brass": 0.25, "steel": 0.42, "nut": 0.5, "petg": 0.5, "black": 0.4, "plastic": 0.4,
         "mdf": 0.7, "vinyl": 0.28, "felt": 0.95, "led": 0.5, "pet": 0.05, "cork": 0.9, "alu": 0.3}


def offset_for(name):
    for k, v in OFFSETS:
        if name.startswith(k):
            return v
    return 0


def export():
    import assembly as A
    import sconce_cad as S
    from cadquery import exporters
    os.makedirs(TMP, exist_ok=True)
    man = []
    for n, p, c, k in A.build("12", "mdf", explode=0.0):
        dz = offset_for(n)
        q = p.translate((0, 0, dz))
        f = os.path.join(TMP, n.replace("/", "-") + ".stl")
        exporters.export(q, f, exportType="STL", tolerance=0.02, angularTolerance=0.06)
        bb = q.val().BoundingBox()
        if n.startswith("pet_label"):
            c = "pet"
        man.append(dict(name=n, file=f, color=c, kind=k, dz=dz,
                        bb=[bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]))
    meta = dict(rec_d=S.REC12_D, bp_d=S.BP12_D, rec_t=S.REC12_T)
    json.dump(dict(parts=man, meta=meta), open(MAN, "w"), indent=1)
    for m in man:
        print(f"{m['name']:22s} dz={m['dz']:4d}  z {m['bb'][4]:7.1f}..{m['bb'][5]:7.1f}  r {max(abs(m['bb'][0]), abs(m['bb'][1])):6.1f}")


def render(out, mode="main"):
    import bpy, math, mathutils
    from bpy_extras.object_utils import world_to_camera_view
    data = json.load(open(MAN))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 220
    sc.cycles.use_denoising = True
    W, H = (3200, 1800) if mode == "main" else (1800, 1000)
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = W, H
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
        pr.compute_device_type = "METAL"; pr.get_devices()
        for d in pr.devices:
            d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        pass
    mats, objs = {}, {}
    for item in data["parts"]:
        bpy.ops.wm.stl_import(filepath=item["file"])
        ob = bpy.context.selected_objects[0]
        ob.name = item["name"]
        ob.scale = (0.001, 0.001, 0.001)
        c = item["color"]
        if c not in mats:
            m = bpy.data.materials.new(c); m.use_nodes = True
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = (*COLORS.get(c, (0.5, 0.5, 0.5)), 1)
            b.inputs["Metallic"].default_value = METAL.get(c, 0)
            b.inputs["Roughness"].default_value = ROUGH.get(c, 0.5)
            if c == "led":
                b.inputs["Emission Color"].default_value = (1.0, 0.62, 0.28, 1)
                b.inputs["Emission Strength"].default_value = 3.0
            if c == "pet":
                b.inputs["Transmission Weight"].default_value = 0.92
                b.inputs["IOR"].default_value = 1.5
            mats[c] = m
        ob.data.materials.append(mats[c])
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
        except Exception:
            pass
        objs[item["name"]] = ob
    bpy.context.view_layer.update()
    # paper label on the record (both faces) so it reads as a record
    rec = next(i for i in data["parts"] if i["name"].startswith("record"))
    for z in (rec["bb"][5] + 0.05, rec["bb"][4] - 0.05):
        bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=0.050, depth=0.00008, location=(0, 0, z / 1000))
        lab = bpy.context.object
        m = bpy.data.materials.new("label"); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.72, 0.16, 0.08, 1); b.inputs["Roughness"].default_value = 0.6
        lab.data.materials.append(m)
        # hole through the label
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.0038, depth=0.0002, location=(0, 0, z / 1000))
        hole = bpy.context.object
        mh = bpy.data.materials.new("hole"); mh.use_nodes = True
        mh.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
        hole.data.materials.append(mh)
    # wall slab behind the plate
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.008))
    wall = bpy.context.object
    wall.scale = (0.34, 0.40, 0.014)
    m = bpy.data.materials.new("wall"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.80, 0.76, 0.69, 1); b.inputs["Roughness"].default_value = 0.9
    wall.data.materials.append(m)
    # floor-less studio: big soft world light
    sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.93, 0.93, 0.94, 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.30
    # camera: orthographic, looking across the stack. wall on the left, cap on the right.
    cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
    sc.camera = cam
    cam_d.type = "ORTHO"
    if mode == "main":
        zmid = 0.415; az = math.radians(27); el = math.radians(14)
        cam_d.ortho_scale = 1.14
        tgt = mathutils.Vector((0, 0.0, zmid))
    else:
        zmid = 0.765; az = math.radians(16); el = math.radians(10)
        cam_d.ortho_scale = 0.215
        tgt = mathutils.Vector((0, 0.0, zmid))
    # camera sits on the -X side, swung toward +Z (front) by az, raised by el. Up = +Y.
    dvec = mathutils.Vector((-math.cos(az) * math.cos(el), math.sin(el), math.sin(az) * math.cos(el)))
    cam.location = tgt + dvec * 3.0
    f = (tgt - cam.location).normalized()
    right = f.cross(mathutils.Vector((0, 1, 0))).normalized()
    up = right.cross(f).normalized()
    rot = mathutils.Matrix((right, up, -f)).transposed()
    cam.matrix_world = mathutils.Matrix.Translation(cam.location) @ rot.to_4x4()
    cam_d.clip_end = 20

    def area(name, loc, power, size):
        ld = bpy.data.lights.new(name, "AREA"); ld.energy = power; ld.size = size
        lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo); lo.location = loc
        d = tgt - mathutils.Vector(loc)
        lo.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    area("key", (-0.9, 0.9, 1.3), 34, 1.4)
    area("fill", (-1.2, -0.3, 0.2), 10, 1.6)
    area("rim", (0.8, 0.5, 0.6), 16, 1.0)
    try:
        sc.view_settings.view_transform = "Standard"
    except Exception:
        pass
    if mode != "main":
        keep = ("pet_label_washer", "felt_washer", "dome_cap")
        for ob in sc.objects:
            if ob.type == "MESH" and not ob.name.startswith(keep):
                ob.hide_render = True
        sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.12
        sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.35, 0.33, 0.30, 1)
    bpy.context.view_layer.update()
    # project anchor points for callouts
    anchors = {}
    for key, prefixes, num, title, line in CALLOUTS:
        its = [i for i in data["parts"] if i["name"].startswith(prefixes)]
        if not its:
            continue
        zs = [i["bb"][4] for i in its] + [i["bb"][5] for i in its]
        r = max(max(abs(i["bb"][0]), abs(i["bb"][1]), abs(i["bb"][2]), abs(i["bb"][3])) for i in its)
        zc = (min(zs) + max(zs)) / 2
        pts = dict(centre=(0, 0, zc), top=(0, r, zc), bottom=(0, -r, zc), front=(0, 0, max(zs)))
        if key == "power":
            i0 = next(i for i in its if i["name"].startswith("inline_jack"))      # point at the connector itself
            pts = dict(centre=((i0["bb"][0] + i0["bb"][1]) / 2, (i0["bb"][2] + i0["bb"][3]) / 2, (i0["bb"][4] + i0["bb"][5]) / 2))
        if key == "pads":
            p0 = next(i for i in its if i["name"].startswith("felt_pads"))
            pts["top"] = (0, max(abs(p0["bb"][2]), abs(p0["bb"][3])) - 8, zc)
        out_pts = {}
        for nm, p in pts.items():
            co = world_to_camera_view(sc, cam, mathutils.Vector(p) / 1000)
            out_pts[nm] = [co.x * W, (1 - co.y) * H]
        anchors[key] = out_pts
    json.dump(dict(size=[W, H], anchors=anchors), open(out + ".anchors.json", "w"), indent=1)
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)


def annotate(out):
    from PIL import Image, ImageDraw, ImageFont
    R = os.path.join(HERE, "..", "renders-exploded")
    main = Image.open(os.path.join(R, "exploded_main_raw.png")).convert("RGBA")
    ins = Image.open(os.path.join(R, "exploded_centre_raw.png")).convert("RGBA")
    am = json.load(open(os.path.join(R, "exploded_main_raw.png.anchors.json")))["anchors"]
    ai = json.load(open(os.path.join(R, "exploded_centre_raw.png.anchors.json")))["anchors"]
    W, H = main.size
    LEG = 1060
    BG, INK, MUTE, ACC = (244, 241, 235, 255), (26, 26, 28, 255), (105, 102, 96, 255), (196, 84, 40, 255)
    cv = Image.new("RGBA", (W, H + LEG), BG)
    cv.alpha_composite(main, (0, 60))
    d = ImageDraw.Draw(cv)
    F = "/System/Library/Fonts/Helvetica.ttc"
    f_t = ImageFont.truetype(F, 84, index=1); f_s = ImageFont.truetype(F, 40)
    f_n = ImageFont.truetype(F, 44, index=1); f_h = ImageFont.truetype(F, 46, index=1); f_b = ImageFont.truetype(F, 38)
    d.text((90, 70), "Spindle: how it goes together", font=f_t, fill=INK)
    d.text((92, 172), "12 in record sconce, current CAD (cap rev D, backplate rev C, heat-safe light). Wall on the left, everything stacks toward you.", font=f_s, fill=MUTE)

    def bubble(x, y, n, r=40):
        d.ellipse((x - r, y - r, x + r, y + r), fill=ACC, outline=(255, 255, 255, 255), width=4)
        tw = d.textlength(n, font=f_n)
        d.text((x - tw / 2, y - 25), n, font=f_n, fill=(255, 255, 255, 255))

    def call(pt, dx, dy, n, oy=60):
        x, y = pt[0], pt[1] + oy
        d.line((x, y, x + dx, y + dy), fill=ACC, width=5)
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=ACC)
        bubble(x + dx, y + dy, n)
    # centre axis hint
    a0, a1 = am["wall"]["centre"], am["cap"]["centre"]
    # main callouts: (key, anchor, dx, dy)
    plan = [("wall", "top", -40, -150, "1"), ("hub", "top", -20, -170, "2"), ("power", "centre", -160, 60, "3"),
            ("led", "top", -70, -190, "4"), ("alu", "top", 0, -230, "5"), ("cork", "top", 70, -190, "6"),
            ("bp", "bottom", -150, 110, "7"), ("pads", "top", 150, -110, "8"),
            ("record", "top", 30, -170, "9"), ("pet", "centre", -50, -230, "10"), ("felt", "centre", 10, -330, "11"),
            ("cap", "centre", 60, -230, "12")]
    for key, anc, dx, dy, n in plan:
        call(am[key][anc], dx, dy, n)
    # inset: the centre stack, bigger
    iw, ih = 900, 500
    ins = ins.resize((iw, ih), Image.LANCZOS)
    ix, iy = W - iw - 70, H - ih + 20
    d.rounded_rectangle((ix, iy, ix + iw, iy + ih), radius=26, fill=(214, 209, 200, 255), outline=(190, 185, 176, 255), width=3)
    cv.alpha_composite(ins, (ix, iy))
    d = ImageDraw.Draw(cv)
    d.text((ix + 30, iy + 22), "Close-up: what holds the record", font=f_h, fill=INK)
    sc_ = iw / 1800
    for key, n, dy in (("pet", "10", 170), ("felt", "11", 170), ("cap", "12", 170)):
        px, py = ai[key]["centre"][0] * sc_ + ix, ai[key]["centre"][1] * sc_ + iy
        d.line((px, py, px, py + dy), fill=ACC, width=5); d.ellipse((px - 9, py - 9, px + 9, py + 9), fill=ACC)
        bubble(px, py + dy, n)
    # legend, two columns
    y0 = H + 110
    d.line((90, y0 - 40, W - 90, y0 - 40), fill=(200, 195, 186, 255), width=3)
    colw = (W - 180) // 2

    def wrap(text, font, maxw):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        return lines
    for i, (key, _p, n, title, line) in enumerate(CALLOUTS):
        col, row = divmod(i, 6)
        x, y = 90 + col * colw, y0 + row * 152
        bubble(x + 40, y + 44, n)
        d.text((x + 105, y), title, font=f_h, fill=INK)
        for j, ln in enumerate(wrap(line, f_b, colw - 150)[:2]):
            d.text((x + 105, y + 54 + j * 42), ln, font=f_b, fill=MUTE)
    cv.convert("RGB").save(out, quality=95)
    print("saved", out, cv.size)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export()
    elif len(sys.argv) > 1 and sys.argv[1] == "annotate":
        annotate(sys.argv[2])
    elif "--" in sys.argv:
        a = sys.argv[sys.argv.index("--") + 1:]
        if a[0] == "render":
            render(*a[1:])
