"""renders-zep/src/zep.py -> renders-lit/src/lit.py: swaps the 12 in cap for RS-CAP-12L (label light) and lights the label
with the ray-traced distribution of the real design (cad/label-light/RS-CAP-12L.ies, from cad/label-light/optics.py).
Geometry numbers are from cad/sconce_lit.py (mm -> m). CYCLES only."""
import os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "../../renders-zep/src/zep.py")).read()
IES = os.path.normpath(os.path.join(H, "../../cad/label-light/RS-CAP-12L.ies"))

helper = '''
LIT12L = "--lit12l" in argv
LIT_K = [float(opt("--litk", "1.0"))]
LIT_WIN = [float(opt("--litwin", "6.0"))]
IES_PATH = %r

def lit_cap(parent, cap, zc, name="LitCap"):
    """RS-CAP-12L as built (cad/sconce_lit.py): black core flange rim 0..0.6 mm, frosted window ring r 17.55..18.05
    z 0.6..4.75, chrome dome with the RS-CAP-12 outside profile on a lip at z 4.8. zc = cap contact face."""
    mm = 0.001
    # core underside + rim (black, nickel + paint)
    lathe(name + "_core", [(0.0035, 0.0), (0.0180, 0.0), (0.0183, 0.0003), (0.0183, 0.0006), (0.0176, 0.0006), (0.0176, 0.0013),
                           (0.0050, 0.0013)], steps=192, parent=parent, z=zc, mat=M_("black"), sm=30)
    # window ring: frosted PC, glowing from inside
    wm = bpy.data.materials.new("LitWindow"); nb = NB(wm)
    gl = nb.bsdf(**{"Base Color": (1.0, 0.95, 0.9), "Roughness": 0.35, "Transmission Weight": 1.0, "IOR": 1.585})
    em = nb.n("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.70, 0.42, 1)
    em.inputs["Strength"].default_value = LIT_WIN[0] if PASS != "ambient" else 0.0
    add = nb.n("ShaderNodeAddShader"); nb.link(gl.outputs[0], add.inputs[0]); nb.link(em.outputs[0], add.inputs[1])
    nb.link(add.outputs[0], nb.out.inputs[0])
    lathe(name + "_win", [(0.01755, 0.0006), (0.01805, 0.0006), (0.01805, 0.00475), (0.01755, 0.00475)], steps=192,
          parent=parent, z=zc, mat=wm, sm=0)
    # louver fins seen through the window (black)
    for zf in (0.0019, 0.00255, 0.0032, 0.00385, 0.0045):
        lathe(name + "_fin", [(0.0125, zf), (0.0175, zf - 0.0005), (0.0175, zf - 0.00025), (0.0125, zf + 0.00025)], steps=96,
              parent=parent, z=zc, mat=M_("black"), sm=0)
    # dome: lip face at 4.8 mm, band 1.6, sphere R 25.8 x 8.4 (same outside as RS-CAP-12)
    z0, rr, rim_h, dome_h = 0.0048, 0.01905, 0.0016, 0.0084
    sph_R = (rr ** 2 + dome_h ** 2) / (2 * dome_h); sph_c = z0 + rim_h + dome_h - sph_R
    prof = [(0.0125, z0), (rr - 0.0008, z0), (rr - 0.00023, z0 + 0.00023), (rr, z0 + 0.0008), (rr, z0 + rim_h)]
    a0 = math.asin((z0 + rim_h - sph_c) / sph_R)
    for i in range(1, 49):
        a = a0 + (math.pi / 2 - a0) * i / 48
        prof.append((max(sph_R * math.cos(a), 0.00005), sph_c + sph_R * math.sin(a)))
    c = lathe(name, prof, steps=256, parent=parent, z=zc, sm=40)
    dm, rm = cap_mats(cap); c.data.materials.append(dm)
    # label light: 48 emitters on the window ring carrying the traced intensity distribution (IES)
    n = 48
    for i in range(n):
        a = 2 * math.pi * i / n
        ld = bpy.data.lights.new(name + "_ies", "POINT")
        ld.energy = 0.010 * LIT_K[0] if PASS != "ambient" else 0.0
        ld.color = (1.0, 0.74, 0.47)          # 2700 K
        ld.shadow_soft_size = 0.0004
        ld.use_nodes = True
        nt = ld.node_tree
        ies = nt.nodes.new("ShaderNodeTexIES"); ies.mode = "EXTERNAL"; ies.filepath = IES_PATH
        emn = [x for x in nt.nodes if x.type == "EMISSION"][0]
        nt.links.new(ies.outputs[0], emn.inputs["Strength"])
        ob = link(bpy.data.objects.new(name + "_ies", ld), parent)
        ob.visible_camera = False; ob.visible_glossy = False
        ob.location = (0.0183 * math.cos(a), 0.0183 * math.sin(a), zc + 0.0027)
        ob.rotation_euler = (0, 0, a + math.pi / 2)     # IES H=0 is the light's -Y: point it radially out
    return c

''' % IES
src = src.replace("def sconce(name, size=\"12\"", helper + "def sconce(name, size=\"12\"", 1)

old = '''        wa = lathe(name + "_wash", [(0.0036, 0.0), (0.0210, 0.0), (0.0212, WASH_T * 0.5), (0.0210, WASH_T),
                                    (0.0036, WASH_T)], steps=128, parent=root, mat=M_("felt"))
        wa.location = (wash_off[0], wash_off[1], capz + wash_off[2])
        if show_cap:'''
assert old in src
src = src.replace(old, '''        if LIT12L and show_cap:
            lit_cap(root, cap, capz + 0.0003, name=name + "_lit")
        else:
          wa = lathe(name + "_wash", [(0.0036, 0.0), (0.0210, 0.0), (0.0212, WASH_T * 0.5), (0.0210, WASH_T),
                                    (0.0036, WASH_T)], steps=128, parent=root, mat=M_("felt"))
          wa.location = (wash_off[0], wash_off[1], capz + wash_off[2])
        if show_cap and not LIT12L:''', 1)

scene = '''
def sc_lit_close():
    """Close-up of the lit cap on a 12 in sconce, light ON, label_halo label, evening room, halo on."""
    warm_wall((0.11, 0.10, 0.095))
    sconce("Sconce", "12", "chrome", "label_halo", spin=0.0)
    set_world((0.010, 0.009, 0.008), 0.30, 0.0)
    area("Fill", (-0.9, 1.1, 0.8), (0, 0, 0), 1.2, 4.0, color=(1.0, 0.86, 0.72))
    rm = bpy.data.materials.new("RoomRefl"); rm.use_nodes = True
    emr = rm.node_tree.nodes.new("ShaderNodeEmission"); emr.inputs[0].default_value = (0.85, 0.78, 0.70, 1); emr.inputs[1].default_value = 0.25
    rm.node_tree.links.new(emr.outputs[0], rm.node_tree.nodes["Material Output"].inputs[0])
    for nm, sz, lc in (("ReflBack", (3.0, 0.02, 2.4), (0.0, 1.8, 0.2)), ("ReflCeil", (3.0, 2.0, 0.02), (0.0, 0.9, 1.3))):
        rp = box(nm, sz, lc, mat=rm)
        rp.visible_camera = False; rp.visible_diffuse = False; rp.visible_shadow = False
    EXPOSURE[0] = 0.6
    zc = HUB_T + BP_T + SO_T + REC_T + 0.006
    frame((0.075, zc + 0.215, 0.11), (0.0, zc - 0.004, 0.004),
          dict(wide=(0.20, 0.1125), square=(0.14, 0.14), tall=(0.11, 0.195)), fstop=6.3)

'''
a, b = src.split("SCENES = dict(", 1)
b = b.replace("zep_dark=sc_zep_dark)", "zep_dark=sc_zep_dark, lit_close=sc_lit_close)")
assert "lit_close" in b
open(os.path.join(H, "lit.py"), "w").write(a + scene + "SCENES = dict(" + b)
print("ok")
