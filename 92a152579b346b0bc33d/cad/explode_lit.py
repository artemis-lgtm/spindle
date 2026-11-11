"""Labelled exploded view of the LIT cap sconce (RS-CAP-12L rev B) from the live CAD (assembly_lit.py).
  .venv/bin/python explode_lit.py export
  Blender -b -P explode_lit.py -- <overview|cap|hub>
  python3 explode_lit.py annotate
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, ".render-tmp", "explode-lit")
OUT = os.path.join(HERE, "..", "renders-exploded")
MAN = os.path.join(TMP, "manifest.json")
CAP = ("lit_", "peek_sleeve", "led_pcb", "leds_2835")
HUBM = ("hub_pcb", "hub_carrier_guard", "ccr_sod123", "contact_plunger", "contact_spring", "pogo_return")
SCENES = {
    "overview": dict(res=(3200, 1300), ortho=1.14, zmid=0.415, az=27, el=14, only=None, wall=True,
                     # 2026-11-11 heat-safe halo: strip, aluminium ring, cork ring and screws come from the canonical CAD
                     # (assembly_lit builds on assembly.build) and are IDENTICAL to the plain-cap sconce.
                     offsets=[("wall_screw_head", 55), ("wall_plate", 0), ("pem_stud", 0), ("lock_nut", 0), ("hub_pcb", 185),
                              ("hub_carrier", 185), ("ccr_", 185), ("contact_", 185), ("pogo_", 185), ("hub", 110),
                              ("pigtail", 110), ("cord_p", 110), ("inline_jack", 110), ("adapter_plug", 110), ("set_screw", 110),
                              ("heat_ring_screw", 205), ("led_cob", 228), ("heat_ring_alu", 258), ("cork_ring", 288),
                              ("backplate", 335), ("ez_lok", 335), ("felt_pads", 388), ("centre_backing", 388),
                              ("record", 570), ("pet_label", 670), ("lit_", 760), ("peek_", 760), ("led_pcb", 760), ("leds_", 760)],
                     calls=[("A", HUBM, "top", 0, -210), ("B", ("lit_dome",), "top", 40, -210),
                            ("C", ("heat_ring_alu",), "top", 60, -130)]),
    "cap": dict(res=(2000, 1000), ortho=0.245, zmid=0.076, az=24, el=12, only=CAP + ("pet_label",), wall=False,
                offsets=[("pet_label", -8), ("lit_pin", -52), ("peek_sleeve", -30), ("lit_core", 6), ("lit_louver", 36),
                         ("lit_window", 56), ("leds_2835", 80), ("led_pcb", 80), ("lit_dome", 102)],
                calls=[("1", ("lit_dome",), "top", 0, -130), ("2", ("led_pcb", "leds_2835"), "bottom", 0, 150),
                       ("3", ("lit_window",), "top", 0, -130), ("4", ("lit_louver",), "bottom", 0, 150),
                       ("5", ("lit_core",), "top", 0, -130), ("6", ("lit_pin", "peek_sleeve"), "bottom", 0, 170),
                       ("7", ("pet_label",), "top", -60, -130)]),
    "hub": dict(res=(1300, 1000), ortho=0.105, zmid=0.049, az=24, el=12, only=HUBM, wall=False,
                offsets=[("hub_pcb", 0), ("ccr_", 0), ("hub_carrier", 16), ("pogo_", 16), ("contact_spring", 38), ("contact_plunger", 54)],
                calls=[("8", ("contact_plunger",), "top", 0, -170), ("9", ("contact_spring",), "bottom", 0, 190),
                       ("10", ("hub_carrier",), "top", 0, -150), ("11", ("hub_pcb",), "bottom", -40, 170)]),
}
LEGEND = [("C", "Heat-safe halo light", "LED strip on the back, facing the wall, on an aluminium ring and a cork ring. Same as the plain cap version."),
          ("1", "Chrome dome", "The shiny shell you see. Same look as the plain cap, a hair taller."),
          ("2", "LED board", "Six tiny warm LEDs facing down at the label. A sixth of a watt total."),
          ("3", "Clear window ring", "The light leaves through this thin band under the dome."),
          ("4", "Black louver", "Aims the light across the label and hides the LEDs from your eye."),
          ("5", "Core with the screw", "Brass, chrome plated. The screw is hollow so power can come up the middle."),
          ("6", "Gold pin in its sleeve", "Carries power up the centre of the screw. The sleeve keeps it from shorting."),
          ("7", "Clear label washer", "The cap sits on this, so no metal touches the paper label."),
          ("8", "Gold plunger", "Springs forward and touches the cap's pin when you screw the cap down."),
          ("9", "Spring", "Keeps the plunger pressed on the pin. Unscrew the cap and it just lets go."),
          ("10", "Guard carrier", "Holds the plunger straight inside the hub, behind the backplate."),
          ("11", "Small board", "Limits the label light to 20 mA no matter what. Power returns through the screw body.")]
COLORS = {"steel": (0.55, 0.57, 0.60), "chrome": (0.9, 0.9, 0.92), "nut": (0.6, 0.6, 0.55), "petg": (0.07, 0.20, 0.12),
          "black": (0.02, 0.02, 0.02), "mdf": (0.035, 0.035, 0.04), "brass": (0.85, 0.62, 0.22), "hub": (0.10, 0.11, 0.13),
          "led": (1.0, 0.7, 0.35), "felt": (0.62, 0.55, 0.44), "vinyl": (0.012, 0.012, 0.014), "plastic": (0.05, 0.05, 0.05),
          "pet": (0.8, 0.9, 1.0), "window": (1.0, 0.86, 0.6), "cork": (0.55, 0.38, 0.22), "alu": (0.75, 0.77, 0.80)}
METAL = {"steel": 1, "chrome": 1, "nut": 1, "brass": 1, "alu": 1}
ROUGH = {"chrome": 0.06, "brass": 0.22, "steel": 0.42, "nut": 0.5, "petg": 0.45, "hub": 0.5, "black": 0.45, "plastic": 0.4,
         "mdf": 0.7, "vinyl": 0.28, "felt": 0.95, "led": 0.5, "pet": 0.05, "window": 0.1, "cork": 0.9, "alu": 0.3}


def off(name, table):
    for k, v in table:
        if name.startswith(k):
            return v
    return 0


def export():
    import assembly_lit as L
    from cadquery import exporters
    os.makedirs(TMP, exist_ok=True)
    man = []
    for n, p, c, k in L.build_lit():
        f = os.path.join(TMP, n.replace("/", "-") + ".stl")
        exporters.export(p, f, exportType="STL", tolerance=0.01, angularTolerance=0.05)
        bb = p.val().BoundingBox()
        c = {"pet_label_washer": "pet", "lit_window": "window", "hub": "hub", "peek_sleeve": "felt"}.get(n, c)
        man.append(dict(name=n, file=f, color=c, bb=[bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]))
    json.dump(man, open(MAN, "w"), indent=1)
    print("exported", len(man))


def render(scene):
    import bpy, math, mathutils
    from bpy_extras.object_utils import world_to_camera_view
    S = SCENES[scene]
    man = json.load(open(MAN))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.samples = 220; sc.cycles.use_denoising = True
    W, H = S["res"]
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = True
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
        pr.compute_device_type = "METAL"; pr.get_devices()
        for d in pr.devices:
            d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        pass
    mats, used = {}, []
    for it in man:
        if S["only"] and not it["name"].startswith(S["only"]):
            continue
        bpy.ops.wm.stl_import(filepath=it["file"])
        ob = bpy.context.selected_objects[0]
        ob.name = it["name"]; ob.scale = (0.001, 0.001, 0.001)
        dz = off(it["name"], S["offsets"]); it["dz"] = dz
        ob.location.z = dz / 1000
        c = it["color"]
        if c not in mats:
            m = bpy.data.materials.new(c); m.use_nodes = True
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = (*COLORS.get(c, (0.5, 0.5, 0.5)), 1)
            b.inputs["Metallic"].default_value = METAL.get(c, 0)
            b.inputs["Roughness"].default_value = ROUGH.get(c, 0.5)
            if c == "led":
                b.inputs["Emission Color"].default_value = (1.0, 0.62, 0.28, 1); b.inputs["Emission Strength"].default_value = 3.0
            if c in ("pet", "window"):
                b.inputs["Transmission Weight"].default_value = 0.85; b.inputs["IOR"].default_value = 1.5
            mats[c] = m
        ob.data.materials.append(mats[c])
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
        except Exception:
            pass
        used.append(it)
    if S["wall"]:
        rec = next(i for i in used if i["name"].startswith("record"))
        for z in (rec["bb"][5] + rec["dz"] + 0.05, rec["bb"][4] + rec["dz"] - 0.05):
            bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=0.050, depth=0.00008, location=(0, 0, z / 1000))
            m = bpy.data.materials.new("label"); m.use_nodes = True
            m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.72, 0.16, 0.08, 1)
            bpy.context.object.data.materials.append(m)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.008))
        wall = bpy.context.object; wall.scale = (0.34, 0.40, 0.014)
        m = bpy.data.materials.new("wall"); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.80, 0.76, 0.69, 1); b.inputs["Roughness"].default_value = 0.9
        wall.data.materials.append(m)
    sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.93, 0.93, 0.94, 1) if S["wall"] else (0.45, 0.43, 0.40, 1)
    bg.inputs[1].default_value = 0.30 if S["wall"] else 0.25
    cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
    sc.camera = cam; cam_d.type = "ORTHO"; cam_d.ortho_scale = S["ortho"]; cam_d.clip_end = 20
    tgt = mathutils.Vector((0, 0, S["zmid"])); az, el = math.radians(S["az"]), math.radians(S["el"])
    dvec = mathutils.Vector((-math.cos(az) * math.cos(el), math.sin(el), math.sin(az) * math.cos(el)))
    loc = tgt + dvec * 3.0
    f = (tgt - loc).normalized(); right = f.cross(mathutils.Vector((0, 1, 0))).normalized(); up = right.cross(f).normalized()
    cam.matrix_world = mathutils.Matrix.Translation(loc) @ mathutils.Matrix((right, up, -f)).transposed().to_4x4()

    def area(name, off_, power, size):
        ld = bpy.data.lights.new(name, "AREA"); ld.energy = power; ld.size = size
        lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo); lo.location = tgt + mathutils.Vector(off_)
        lo.rotation_euler = (tgt - lo.location).to_track_quat("-Z", "Y").to_euler()
    area("key", (-0.9, 0.9, 0.9), 34, 1.4); area("fill", (-1.2, -0.3, -0.2), 10, 1.6); area("rim", (0.8, 0.5, 0.2), 16, 1.0)
    sc.view_settings.view_transform = "Standard"
    bpy.context.view_layer.update()
    anchors = {}
    for num, prefixes, anc, dx, dy in S["calls"]:
        its = [i for i in used if i["name"].startswith(prefixes)]
        zs = [i["bb"][4] + i["dz"] for i in its] + [i["bb"][5] + i["dz"] for i in its]
        r = max(max(abs(i["bb"][2]), abs(i["bb"][3])) for i in its)
        zc = (min(zs) + max(zs)) / 2
        p = dict(top=(0, r, zc), bottom=(0, -r, zc), centre=(0, 0, zc))[anc]
        co = world_to_camera_view(sc, cam, mathutils.Vector(p) / 1000)
        anchors[num] = [co.x * W, (1 - co.y) * H, dx, dy]
    out = os.path.join(OUT, f"lit_{scene}_raw.png")
    json.dump(anchors, open(out + ".anchors.json", "w"))
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)


def annotate():
    from PIL import Image, ImageDraw, ImageFont
    BG, INK, MUTE, ACC, PAN = (244, 241, 235, 255), (26, 26, 28, 255), (105, 102, 96, 255), (196, 84, 40, 255), (214, 209, 200, 255)
    W = 3200
    ov = Image.open(os.path.join(OUT, "lit_overview_raw.png")).convert("RGBA")
    cap = Image.open(os.path.join(OUT, "lit_cap_raw.png")).convert("RGBA")
    hub = Image.open(os.path.join(OUT, "lit_hub_raw.png")).convert("RGBA")
    A = {k: json.load(open(os.path.join(OUT, f"lit_{k}_raw.png.anchors.json"))) for k in SCENES}
    y_ov, y_pan, ph = 210, 1560, 960
    y_leg = y_pan + ph + 110
    H = y_leg + 6 * 150 + 60
    cv = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(cv)
    F = "/System/Library/Fonts/Helvetica.ttc"
    f_t = ImageFont.truetype(F, 84, index=1); f_s = ImageFont.truetype(F, 40); f_n = ImageFont.truetype(F, 44, index=1)
    f_h = ImageFont.truetype(F, 46, index=1); f_b = ImageFont.truetype(F, 38)
    d.text((90, 70), "Spindle with the lit cap: how it goes together", font=f_t, fill=INK)
    d.text((92, 172), "Premium version (lit cap rev B). Same sconce and the same heat-safe halo, but the cap lights the label and the hub feeds it power through the screw.", font=f_s, fill=MUTE)
    cv.alpha_composite(ov, (0, y_ov)); d = ImageDraw.Draw(cv)

    def bubble(x, y, n, r=40):
        d.ellipse((x - r, y - r, x + r, y + r), fill=ACC, outline=(255, 255, 255, 255), width=4)
        tw = d.textlength(n, font=f_n); d.text((x - tw / 2, y - 25), n, font=f_n, fill=(255, 255, 255, 255))

    def call(x, y, dx, dy, n):
        d.line((x, y, x + dx, y + dy), fill=ACC, width=5); d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=ACC); bubble(x + dx, y + dy, n)
    offs = {k: {c[0]: (c[3], c[4]) for c in v["calls"]} for k, v in SCENES.items()}     # leader offsets live in SCENES, so a
    for n, (x, y, _dx, _dy) in A["overview"].items():                                    # label can move without a re-render
        dx, dy = offs["overview"][n]
        call(x, y + y_ov, dx, dy, n)
    # panels
    cw, hw = 1900, 1140
    for (x0, w, img, key, title, tag) in ((70, cw, cap, "cap", "Inside the lit cap", "B"), (70 + cw + 50, hw, hub, "hub", "Contact inside the hub", "A")):
        d.rounded_rectangle((x0, y_pan, x0 + w, y_pan + ph), radius=26, fill=PAN, outline=(190, 185, 176, 255), width=3)
        s = min(w / img.size[0], (ph - 90) / img.size[1])
        im = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.LANCZOS)
        ox, oy = x0 + (w - im.size[0]) // 2, y_pan + 90 + (ph - 90 - im.size[1]) // 2
        cv.alpha_composite(im, (ox, oy)); d = ImageDraw.Draw(cv)
        bubble(x0 + 70, y_pan + 62, tag)
        d.text((x0 + 130, y_pan + 34), title, font=f_h, fill=INK)
        for n, (x, y, _dx, _dy) in A[key].items():
            dx, dy = offs[key][n]
            call(ox + x * s, oy + y * s, dx, dy, n)
    d.line((90, y_leg - 50, W - 90, y_leg - 50), fill=(200, 195, 186, 255), width=3)
    colw = (W - 180) // 2

    def wrap(text, font, maxw):
        lines, cur = [], ""
        for w_ in text.split():
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w_
        return lines + [cur]
    for i, (n, title, line) in enumerate(LEGEND):
        col, row = divmod(i, 6)
        x, y = 90 + col * colw, y_leg + row * 150
        bubble(x + 40, y + 44, n)
        d.text((x + 105, y), title, font=f_h, fill=INK)
        for j, ln in enumerate(wrap(line, f_b, colw - 150)[:2]):
            d.text((x + 105, y + 54 + j * 42), ln, font=f_b, fill=MUTE)
    out = os.path.join(OUT, "spindle-lit-exploded-labelled.png")
    cv.convert("RGB").save(out)
    print("saved", out, cv.size)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export()
    elif len(sys.argv) > 1 and sys.argv[1] == "annotate":
        annotate()
    elif "--" in sys.argv:
        render(sys.argv[sys.argv.index("--") + 1])
