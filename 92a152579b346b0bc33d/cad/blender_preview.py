"""Cycles previews of the placed assembly. Usage (from cad/):
  .venv/bin/python blender_preview.py export            # writes placed STLs + manifest to .render-tmp/
  /Applications/Blender.app/Contents/MacOS/Blender -b -P blender_preview.py -- <manifest.json> <out.png> <view>
view: front | rear | exploded
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, ".render-tmp")

COLORS = {"steel": (0.55, 0.57, 0.60), "chrome": (0.9, 0.9, 0.92), "nut": (0.6, 0.6, 0.55), "petg": (0.12, 0.13, 0.15),
          "black": (0.02, 0.02, 0.02), "mdf": (0.03, 0.03, 0.03), "alu": (0.6, 0.62, 0.65), "brass": (0.8, 0.6, 0.25),
          "led": (1.0, 0.7, 0.35), "felt": (0.4, 0.35, 0.28), "vinyl": (0.01, 0.01, 0.012)}
METAL = {"steel": 1, "chrome": 1, "nut": 1, "alu": 1, "brass": 1}
ROUGH = {"chrome": 0.05, "brass": 0.25, "steel": 0.45, "nut": 0.5, "alu": 0.35, "petg": 0.55, "black": 0.4,
         "mdf": 0.6, "vinyl": 0.25, "felt": 0.95, "led": 0.5}


def export():
    import assembly as A
    from cadquery import exporters
    os.makedirs(TMP, exist_ok=True)
    jobs = {"12mdf": ("12", "mdf", 0.0), "12mdf_x": ("12", "mdf", 45.0), "7mdf": ("7", "mdf", 0.0), "12al5": ("12", "al5", 0.0)}
    for key, (v, m, e) in jobs.items():
        parts = A.build(v, m, explode=e)
        man = []
        for n, p, c, k in parts:
            f = os.path.join(TMP, f"{key}_{n.replace('/', '-')}.stl")
            exporters.export(p, f, exportType="STL", tolerance=0.03, angularTolerance=0.08)
            man.append(dict(name=n, file=f, color=c, kind=k))
        with open(os.path.join(TMP, f"{key}.json"), "w") as fh:
            json.dump(man, fh)
        print("exported", key, len(man))


def render(manifest, out, view):
    import bpy, math
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 128
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1600, 1200
    sc.render.film_transparent = False
    try:
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "METAL"
        bpy.context.preferences.addons["cycles"].preferences.get_devices()
        for d in bpy.context.preferences.addons["cycles"].preferences.devices:
            d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        pass
    with open(manifest) as fh:
        man = json.load(fh)
    mats = {}
    zs = []
    for item in man:
        if view == "rear" and item["name"].startswith("record"):
            continue
        bpy.ops.wm.stl_import(filepath=item["file"]) if hasattr(bpy.ops.wm, "stl_import") else bpy.ops.import_mesh.stl(filepath=item["file"])
        ob = bpy.context.selected_objects[0]
        ob.scale = (0.001, 0.001, 0.001)
        c = item["color"]
        if c not in mats:
            m = bpy.data.materials.new(c); m.use_nodes = True
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = (*COLORS[c], 1)
            b.inputs["Metallic"].default_value = METAL.get(c, 0)
            b.inputs["Roughness"].default_value = ROUGH.get(c, 0.5)
            if c == "vinyl":
                b.inputs["Roughness"].default_value = 0.35
                for nm in ("Specular IOR Level", "Specular"):
                    if nm in b.inputs:
                        b.inputs[nm].default_value = 0.25
            if c == "led":
                b.inputs["Emission Color"].default_value = (1.0, 0.65, 0.3, 1)
                b.inputs["Emission Strength"].default_value = 6.0
            mats[c] = m
        ob.data.materials.append(mats[c])
        for p in ob.data.polygons:
            p.use_smooth = True
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
        except Exception:
            pass
        bb = [ob.matrix_world @ __import__("mathutils").Vector(v) for v in ob.bound_box]
        zs += [v.z for v in bb]
    zmid = (max(zs) + min(zs)) / 2
    # wall plane (only for front views)
    if view != "rear":
        bpy.ops.mesh.primitive_plane_add(size=1.2, location=(0, 0, -0.0005))
        wall = bpy.context.object
        m = bpy.data.materials.new("wall"); m.use_nodes = True
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.82, 0.76, 0.66, 1)
        m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
        wall.data.materials.append(m)
    # camera
    cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
    sc.camera = cam
    cam_d.lens = 60
    if view == "rear":
        loc, tgt = (0.25, -0.30, -0.28), (0, 0, 0.02)
    elif view == "exploded":
        loc, tgt = (0.32, -0.42, 0.45), (0, 0, zmid)
    else:
        loc, tgt = (0.42, -0.30, 0.12), (0, 0, 0.03)
    import mathutils
    cam.location = loc
    direction = mathutils.Vector(tgt) - mathutils.Vector(loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    # lights
    def area(name, loc, power, size):
        ld = bpy.data.lights.new(name, "AREA"); ld.energy = power; ld.size = size
        lo = bpy.data.objects.new(name, ld); sc.collection.objects.link(lo); lo.location = loc
        d = mathutils.Vector(tgt) - mathutils.Vector(loc)
        lo.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    area("key", (0.5, -0.5, 0.7), 70, 0.8)
    area("fill", (-0.6, -0.3, 0.3), 25, 1.0)
    area("rim", (0.1, 0.6, 0.4), 35, 0.6)
    sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.15
    try:
        sc.view_settings.view_transform = "AgX"
    except Exception:
        pass
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export()
    else:
        args = sys.argv[sys.argv.index("--") + 1:]
        render(*args)
