"""Copy renders-studio/src/studio.py -> labellight.py, adding the cap label light (--labellight) and a 3/4 close-up scene."""
import os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "../../renders-studio/src/studio.py")).read()

# 1. flag + light ring helper, inserted right before the sconce builder
helper = '''
LABEL_LIGHT = "--labellight" in argv
LL_K = [float(opt("--llk", "1.0"))]

def label_ring(parent, z, r_led, r_lip, name, n=16, power=0.006):
    """Thin chrome skirt flaring off the cap base, hiding a ring of tiny warm side-emitting LEDs
    that graze the label. Lights sit under the skirt, just above the label surface."""
    t = 0.0006
    lip = [(r_led - 0.0030, 0.0042), (r_lip, 0.0030), (r_lip + 0.0004, 0.0024), (r_lip, 0.0020),
           (r_lip - 0.0004, 0.0024), (r_led - 0.0030, 0.0042 - t)]
    lathe(name + "_skirt", lip, steps=192, parent=parent, z=z, mat=M_("chrome"), sm=40)
    for i in range(n):
        a = 2 * math.pi * i / n
        ld = bpy.data.lights.new(name + "_led", "POINT")
        ld.energy = power * LL_K[0]
        ld.color = (1.0, 0.72, 0.42)
        ld.shadow_soft_size = 0.0015
        ob = link(bpy.data.objects.new(name + "_led", ld), parent)
        ob.visible_camera = False; ob.visible_glossy = False
        ob.location = (r_led * math.cos(a), r_led * math.sin(a), z + 0.0014)

'''
src = src.replace("def sconce(name, size=\"12\"", helper + "def sconce(name, size=\"12\"", 1)

# 2. hook into sconce(): after each cap is placed
src = src.replace(
    "            c.location = (cap_off[0], cap_off[1], capz + WASH_T + cap_off[2])\n",
    "            c.location = (cap_off[0], cap_off[1], capz + WASH_T + cap_off[2])\n"
    "            if LABEL_LIGHT:\n"
    "                label_ring(root, capz + WASH_T, 0.0218, 0.0240, name + \"_ll\")\n", 1)
src = src.replace(
    "            c.location = (cap_off[0], cap_off[1], capz + cap_off[2])\n",
    "            c.location = (cap_off[0], cap_off[1], capz + cap_off[2])\n"
    "            if LABEL_LIGHT:\n"
    "                label_ring(root, capz, 0.0262, 0.0282, name + \"_ll\", n=12, power=0.005)\n", 1)

# 3. close-up scene: dark charcoal panel wall, 3/4 view
scene = '''
def sc_lab_close():
    warm_wall((0.10, 0.095, 0.09))
    sconce("Sconce", "12", "chrome", "label_sunroom", spin=0.0)
    set_world((0.010, 0.009, 0.008), 0.35, 0.0)
    area("Fill", (-0.9, 1.1, 0.8), (0, 0, 0), 1.2, 9.0, color=(1.0, 0.86, 0.72))
    EXPOSURE[0] = 0.55
    frame((0.40, 0.62, 0.10), (0.0, 0.03, 0.0), dict(wide=(0.62, 0.35), square=(0.42, 0.42), tall=(0.32, 0.56)), fstop=5.6)

'''
a, b = src.split("SCENES = dict(", 1)
b = b.replace("band_grid=sc_band_grid)", "band_grid=sc_band_grid, lab_close=sc_lab_close)")
src = a + scene + "SCENES = dict(" + b
open(os.path.join(H, "labellight.py"), "w").write(src)
print("ok", src.count("label_ring("))
