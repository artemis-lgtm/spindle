"""labellight.py + a tight close-up on a Led Zeppelin label (label light on)."""
import os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "../../renders-labellight/src/labellight.py")).read()

# solid chrome collar: bezel drops over the felt washer and seats on the record, taller so it reads as metal
src = src.replace("rim_r=0.0201, rim_h=0.0016, post=0.020", "rim_r=0.0193, rim_h=0.0030, post=0.020", 1)
old = "(0.0032, 0.0),\n            (rim_r - 0.0004, 0.0), (rim_r, 0.0004)"
assert old in src
src = src.replace(old, "(0.0032, -0.0022),\n            (rim_r - 0.0006, -0.0022), (rim_r, -0.0016)", 1)

scene = '''
def sc_zep_close():
    warm_wall((0.10, 0.095, 0.09))
    sconce("Sconce", "12", "chrome", "label_zep_photo", spin=0.0)
    set_world((0.010, 0.009, 0.008), 0.35, 0.0)
    area("Fill", (-0.9, 1.1, 0.8), (0, 0, 0), 1.2, 9.0, color=(1.0, 0.86, 0.72))
    EXPOSURE[0] = 0.55
    frame((0.17, 0.40, 0.07), (0.0, 0.035, 0.0), dict(wide=(0.32, 0.18), square=(0.24, 0.24), tall=(0.18, 0.32)), fstop=4.0)


def sc_zep_bright():
    warm_wall((0.16, 0.15, 0.14))
    sconce("Sconce", "12", "chrome", "label_zep_photo", spin=0.0)
    set_world((0.03, 0.026, 0.022), 0.6, 0.0)
    area("Fill", (-0.9, 1.1, 0.8), (0, 0, 0), 1.2, 14.0, color=(1.0, 0.92, 0.84))
    area("Key", (0.7, 0.9, 0.5), (0, 0, 0), 0.8, 5.0, color=(1.0, 0.95, 0.9))
    area("WindowR", (0.9, 2.6, 0.6), (0, 0.04, 0), 1.0, 12.0, color=(0.95, 0.9, 0.85), size_y=1.4)
    area("Softbox", (0.25, 0.9, 0.35), (0, 0.04, 0), 0.6, 4.0, color=(1.0, 0.97, 0.93), size_y=0.6)
    # the room behind the camera, seen only in reflections, so the dome reads as chrome
    rm = bpy.data.materials.new("RoomRefl"); rm.use_nodes = True
    em = rm.node_tree.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (0.85, 0.78, 0.70, 1); em.inputs[1].default_value = 0.6
    rm.node_tree.links.new(em.outputs[0], rm.node_tree.nodes["Material Output"].inputs[0])
    for nm, sz, lc in (("ReflBack", (3.0, 0.02, 2.4), (0.0, 1.8, 0.2)), ("ReflCeil", (3.0, 2.0, 0.02), (0.0, 0.9, 1.3))):
        rp = box(nm, sz, lc, mat=rm)
        rp.visible_camera = False; rp.visible_diffuse = False; rp.visible_shadow = False
    EXPOSURE[0] = 0.6
    frame((0.36, 0.60, 0.08), (0.0, 0.03, 0.0), dict(wide=(0.56, 0.315), square=(0.40, 0.40), tall=(0.30, 0.53)), fstop=8.0)


def sc_zep_macro():
    warm_wall()
    sconce("Sconce", "12", "chrome", "label_zep_photo", spin=0.0)
    hero_lighting()
    BGH.inputs[1].default_value = 0.45
    area("WindowR", (0.9, 2.6, 0.6), (0, 0.04, 0), 1.0, 5.0, color=(0.95, 0.9, 0.85), size_y=1.4)
    zc = HUB_T + BP_T + SO_T + REC_T + WASH_T + 0.006
    tgt = (0.0, zc, 0.0)
    frame((0.085, zc + 0.125, 0.055), tgt,
          dict(wide=(0.115, 0.065), square=(0.085, 0.085), tall=(0.062, 0.11)), fstop=3.2)


WALL_C = [(0.82, 0.74, 0.62)]
def sc_zep_dark():
    WALL_C[0] = (0.075, 0.062, 0.052)
    sc_zep_room()

def sc_zep_room():
    warm_wall(WALL_C[0])
    sconce("Sconce", "12", "chrome", "label_zep_photo", spin=0.0)
    hero_lighting(0.8)
    BGH.inputs[1].default_value = 0.45
    area("WindowR", (0.9, 2.6, 0.6), (0, 0.04, 0), 1.0, 5.0, color=(0.95, 0.9, 0.85), size_y=1.4)
    # late-afternoon window light raking across the wall from the left
    area("Window", (-2.2, 1.0, 0.9), (0.4, 0.0, -0.2), 1.2, 42.0, color=(1.0, 0.88, 0.72), size_y=1.6)
    frame((0.36, 0.60, 0.08), (0.0, 0.03, 0.0), dict(wide=(0.56, 0.315), square=(0.40, 0.40), tall=(0.30, 0.53)), fstop=5.6)

'''
a, b = src.split("SCENES = dict(", 1)
b = b.replace("lab_close=sc_lab_close)", "lab_close=sc_lab_close, zep_close=sc_zep_close, zep_bright=sc_zep_bright, zep_macro=sc_zep_macro, zep_room=sc_zep_room, zep_dark=sc_zep_dark)")
assert "zep_close" in b
open(os.path.join(H, "zep.py"), "w").write(a + scene + "SCENES = dict(" + b)
print("ok")
