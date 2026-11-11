# Band-room scenes, spliced into a copy of renders-final/src/final.py by build_studio.py.
# Reference: Austin's 11/10 photo (Lord Decor "Basement Music Room Ideas With Studio Style"):
# charcoal fabric panels, perimeter LED seams (warm amber here so the halos own the colour),
# coffered dark ceiling with track spots + cans, wood diffusers, drum kit on a round rug,
# walnut organ, guitar on a stand, two amps, grey shag carpet tiles.

RW, RD = 2.6, 7.2          # half-width, depth
BFZ = -1.45                # floor (sconce centres sit near z=0 = 57 in)
BCZ = BFZ + 2.75           # ceiling

def spot(name, loc, target, power, angle=0.6, blend=0.4, color=(1.0, 0.78, 0.55), radius=0.02):
    ld = bpy.data.lights.new(name, "SPOT"); ld.energy = power if PASS != "halo" else 0.0
    ld.spot_size = angle; ld.spot_blend = blend; ld.color = color; ld.shadow_soft_size = radius
    lo = link(bpy.data.objects.new(name, ld)); lo.location = loc
    lo.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return lo

def strip_mat(k=1.0):
    return cached("strip" + str(k), lambda: mat_emit("LEDStrip", (1.0, 0.50, 0.20), 5.0 * k if PASS != "halo" else 0.0))

def panel_mat():
    return cached("bandpanel", lambda: mat_fabric("BandPanel", (0.105, 0.105, 0.11), scale=700, rough=0.95, sheen=0.3))

def band_room(strips=1.0):
    pm = panel_mat()
    seam = cached("seam", lambda: mat_simple("Seam", (0.01, 0.01, 0.01), 0.9))
    H = BCZ - BFZ
    # structural shells (behind panels)
    box("BackShell", (2 * RW + 0.4, 0.05, H + 0.4), (0, -0.08, BFZ + H / 2), mat=seam)
    for s in (-1, 1):
        box("SideShell", (0.05, RD + 0.4, H + 0.4), (s * (RW + 0.08), RD / 2, BFZ + H / 2), mat=seam)
    # back wall panels in bays (face at y=0), 0.012 dark seams between
    bay = 0.62
    n = int((2 * RW - 0.16) / bay)
    x0 = -n * bay / 2
    for i in range(n):
        box("BPanel", (bay - 0.012, 0.05, H - 0.16), (x0 + bay * (i + 0.5), -0.025, BFZ + H / 2), mat=pm, bevel=0.006)
    # side walls panels (face at x = +-RW)
    m = int((RD - 0.2) / bay)
    for s in (-1, 1):
        for j in range(m):
            box("SPanel", (0.05, bay - 0.012, H - 0.16), (s * (RW + 0.025), 0.08 + bay * (j + 0.5), BFZ + H / 2), mat=pm, bevel=0.006)
    # perimeter LED seams: top + bottom of each wall, vertical at the back corners
    sm = strip_mat(strips)
    for z in (BFZ + 0.07, BCZ - 0.07):
        box("StripB", (2 * RW - 0.1, 0.02, 0.018), (0, 0.004, z), mat=sm)
        for s in (-1, 1):
            box("StripS", (0.02, RD, 0.018), (s * (RW - 0.004), RD / 2 + 0.05, z), mat=sm)
    for s in (-1, 1):
        box("StripV", (0.018, 0.02, H - 0.14), (s * (RW - 0.03), 0.02, BFZ + H / 2), mat=strip_mat(0.6 * strips))
    # ceiling: dark field, coffer beams, recessed cans, two track runs
    cm = cached("ceil", lambda: mat_simple("Ceil", (0.035, 0.035, 0.037), 0.8))
    bm_ = cached("beam", lambda: mat_simple("Beam", (0.05, 0.05, 0.052), 0.7))
    box("Ceiling", (2 * RW + 0.4, RD + 0.4, 0.05), (0, RD / 2, BCZ + 0.025), mat=cm)
    for y in (1.2, 2.6, 4.0, 5.4):
        box("BeamX", (2 * RW, 0.22, 0.16), (0, y, BCZ - 0.08), mat=bm_, bevel=0.004)
    box("BeamY", (0.5, RD, 0.16), (0, RD / 2, BCZ - 0.08), mat=bm_, bevel=0.004)
    can_m = cached("can", lambda: mat_emit("Can", (1.0, 0.85, 0.65), 6.0 if PASS != "halo" else 0.0))
    for x in (-1.5, 1.5):
        for y in (0.6, 1.9, 3.3, 4.7):
            cyl("Can", 0.045, 0.01, loc=(x, y, BCZ - 0.005), mat=can_m)
            spot("CanSpot", (x, y, BCZ - 0.02), (x, y, BFZ), 30, angle=1.0, blend=0.6, color=(1.0, 0.88, 0.74))
    trk = M_("black")
    for x in (-0.95, 0.95):
        box("Track", (0.03, RD - 0.6, 0.03), (x, RD / 2, BCZ - 0.03), mat=trk)
    return pm

def drum(name, r, depth, loc, rot, wrap, head_front=None, parent=None):
    e = empty(name, loc, rot, parent)
    cyl(name + "_shell", r, depth, mat=wrap, parent=e, verts=96, bevel=0.002)
    hm = cached("head", lambda: mat_simple("DrumHead", (0.80, 0.79, 0.74), 0.55, spec=0.3, bump_scale=900, bump_str=0.03))
    for s in (-1, 1):
        cyl(name + "_head", r - 0.004, 0.003, loc=(0, 0, s * depth / 2), mat=head_front if (s > 0 and head_front) else hm,
            parent=e, verts=96)
        lathe(name + "_hoop", [(r - 0.002, -0.009), (r + 0.006, -0.009), (r + 0.006, 0.009), (r - 0.002, 0.009)],
              steps=96, mat=M_("chrome"), parent=e, z=s * depth / 2, sm=0)
    nlug = 8 if r > 0.15 else 6
    for i in range(nlug):
        a = 2 * math.pi * i / nlug
        box(name + "_lug", (0.012, 0.016, min(0.05, depth * 0.3)), (math.cos(a) * (r + 0.006), math.sin(a) * (r + 0.006), 0),
            mat=M_("chrome"), parent=e, bevel=0.003)
    return e

def cymbal(name, r, loc, tilt=(0.0, 0.0)):
    cm = cached("cym", lambda: mat_simple("Cymbal", (0.78, 0.55, 0.26), 0.28, metallic=1.0, bump_scale=1500, bump_str=0.04))
    prof = [(0.004, 0.024), (0.035, 0.021), (0.045, 0.011), (r, 0.0), (r, -0.0015), (0.045, 0.0095), (0.035, 0.0195), (0.004, 0.0225)]
    c = lathe(name, prof, steps=128, mat=cm)
    c.location = loc; c.rotation_euler = (tilt[0], tilt[1], 0)
    return c

def cym_stand(base, top):
    sm = M_("chrome")
    tube("CStand", [base, ((base[0] + top[0]) / 2, (base[1] + top[1]) / 2, (base[2] + top[2]) / 2), top], 0.0085, sm)
    for i in range(3):
        a = 2 * math.pi * i / 3 + 0.4
        tube("CLeg", [(base[0], base[1], base[2] + 0.30), (base[0] + 0.26 * math.cos(a), base[1] + 0.26 * math.sin(a), base[2] + 0.005)],
             0.006, sm)

def drum_kit(cx, cy, fz):
    wrap = cached("wrap", lambda: mat_simple("DrumWrap", (0.62, 0.63, 0.66), 0.18, metallic=0.85, bump_scale=4000, bump_str=0.06, coat=0.6))
    kf = cached("kickfront", lambda: mat_simple("KickFront", (0.86, 0.84, 0.79), 0.5, spec=0.3))
    # kick, axis toward camera (+y)
    drum("Kick", 0.28, 0.40, (cx, cy, fz + 0.29), (-math.pi / 2, 0, 0), wrap, head_front=kf)
    cyl("KickPort", 0.06, 0.006, loc=(cx + 0.11, cy + 0.205, fz + 0.22), rot=(-math.pi / 2, 0, 0), mat=M_("black"))
    lathe("KickPortRing", [(0.058, 0.0), (0.068, 0.0), (0.068, 0.006), (0.058, 0.006)], steps=64, sm=0, mat=M_("chrome")
          ).location = (cx + 0.11, cy + 0.206, fz + 0.22)
    for s in (-1, 1):
        tube("KickSpur", [(cx + s * 0.26, cy + 0.10, fz + 0.14), (cx + s * 0.36, cy + 0.16, fz + 0.005)], 0.006, M_("chrome"))
    # rack toms on the kick
    drum("Tom1", 0.13, 0.20, (cx - 0.15, cy - 0.02, fz + 0.72), (-math.pi / 2 + 0.55, 0, 0.18), wrap)
    drum("Tom2", 0.15, 0.22, (cx + 0.17, cy - 0.02, fz + 0.73), (-math.pi / 2 + 0.55, 0, -0.18), wrap)
    tube("TomPost", [(cx, cy - 0.05, fz + 0.55), (cx, cy - 0.05, fz + 0.68)], 0.012, M_("chrome"))
    # floor tom right (camera-left is -x; kit faces +y so drummer's right is -x... keep studio-photo layout)
    ft = drum("FloorTom", 0.20, 0.40, (cx + 0.58, cy - 0.10, fz + 0.48), (0, 0, 0), wrap)
    for i in range(3):
        a = 2 * math.pi * i / 3 + 0.3
        tube("FTLeg", [(cx + 0.58 + 0.215 * math.cos(a), cy - 0.10 + 0.215 * math.sin(a), fz + 0.45),
                       (cx + 0.58 + 0.25 * math.cos(a), cy - 0.10 + 0.25 * math.sin(a), fz + 0.005)], 0.007, M_("chrome"))
    # snare left on stand
    drum("Snare", 0.18, 0.14, (cx - 0.52, cy - 0.05, fz + 0.62), (0.12, 0, 0), wrap)
    cym_stand((cx - 0.52, cy - 0.05, fz), (cx - 0.52, cy - 0.05, fz + 0.54))
    # hi-hat far left
    cym_stand((cx - 0.88, cy - 0.12, fz), (cx - 0.88, cy - 0.12, fz + 0.92))
    cymbal("HatB", 0.18, (cx - 0.88, cy - 0.12, fz + 0.86))
    cymbal("HatT", 0.18, (cx - 0.88, cy - 0.12, fz + 0.88))
    # crash + ride
    cym_stand((cx - 0.62, cy - 0.30, fz), (cx - 0.48, cy - 0.20, fz + 1.18))
    cymbal("Crash", 0.22, (cx - 0.48, cy - 0.20, fz + 1.20), tilt=(0.30, -0.20))
    cym_stand((cx + 0.86, cy - 0.20, fz), (cx + 0.74, cy - 0.12, fz + 1.08))
    cymbal("Ride", 0.27, (cx + 0.74, cy - 0.12, fz + 1.10), tilt=(0.25, 0.22))
    cym_stand((cx + 0.40, cy - 0.40, fz), (cx + 0.34, cy - 0.30, fz + 1.30))
    cymbal("Crash2", 0.20, (cx + 0.34, cy - 0.30, fz + 1.32), tilt=(0.32, 0.10))
    # throne
    cyl("Throne", 0.17, 0.09, loc=(cx, cy - 0.62, fz + 0.58), mat=cached("throne", lambda: mat_fabric("Throne", (0.03, 0.03, 0.03))), bevel=0.02)
    tube("ThronePost", [(cx, cy - 0.62, fz + 0.54), (cx, cy - 0.62, fz + 0.25)], 0.014, M_("chrome"))

def round_rug(cx, cy, fz, r=1.35):
    cream = cached("rugc", lambda: mat_fabric("RugCream", (0.62, 0.58, 0.52), scale=400))
    dark = cached("rugd", lambda: mat_fabric("RugDark", (0.10, 0.10, 0.10), scale=400))
    mid = cached("rugm", lambda: mat_fabric("RugMid", (0.30, 0.29, 0.27), scale=400))
    for rr, h, m in ((r, 0.010, dark), (r - 0.06, 0.012, cream), (r - 0.14, 0.014, dark), (r - 0.20, 0.016, mid),
                     (r * 0.45, 0.018, cream), (r * 0.45 - 0.05, 0.019, dark)):
        cyl("Rug", rr, h, loc=(cx, cy, fz + h / 2), mat=m, verts=128)

def carpet_tiles(fz):
    g1 = cached("shag1", lambda: mat_simple("Shag1", (0.16, 0.16, 0.165), 1.0, sheen=0.6, bump_scale=900, bump_str=0.6))
    g2 = cached("shag2", lambda: mat_simple("Shag2", (0.09, 0.09, 0.095), 1.0, sheen=0.6, bump_scale=900, bump_str=0.6))
    g3 = cached("shag3", lambda: mat_simple("Shag3", (0.24, 0.235, 0.23), 1.0, sheen=0.6, bump_scale=900, bump_str=0.6))
    base = cached("concrete", lambda: mat_simple("Concrete", (0.20, 0.20, 0.20), 0.7, bump_scale=60, bump_str=0.1))
    box("Floor", (2 * RW + 0.4, RD + 0.4, 0.02), (0, RD / 2, fz - 0.01), mat=base)
    rnd = random.Random(31)
    t = 0.98
    for i in range(-3, 3):
        for j in range(0, 8):
            m = rnd.choice([g1, g1, g2, g3])
            box("Tile", (t - 0.06, t - 0.06, 0.008), ((i + 0.5) * t, 0.55 + j * t, fz + 0.004), mat=m, bevel=0.003)

def organ(cx, cy, fz, rotz=0.0):
    e = empty("Organ", (cx, cy, fz), (0, 0, rotz))
    wm = walnut()
    box("OrgSideL", (0.03, 0.50, 0.80), (-0.52, 0, 0.40), mat=wm, parent=e, bevel=0.004)
    box("OrgSideR", (0.03, 0.50, 0.80), (0.52, 0, 0.40), mat=wm, parent=e, bevel=0.004)
    box("OrgBack", (1.04, 0.03, 0.62), (0, -0.20, 0.45), mat=wm, parent=e, bevel=0.003)
    box("OrgTop", (1.10, 0.42, 0.10), (0, -0.04, 0.85), mat=wm, parent=e, bevel=0.006)
    box("OrgLid", (1.10, 0.14, 0.12), (0, -0.20, 0.96), mat=wm, parent=e, bevel=0.006)
    wk = cached("whitekey", lambda: mat_simple("WhiteKey", (0.86, 0.84, 0.78), 0.3))
    for row, (yy, zz) in enumerate(((0.05, 0.91), (-0.06, 0.95))):
        for i in range(36):
            box("WKey", (0.0245, 0.11, 0.014), (-0.44 + i * 0.0253, yy, zz), mat=wk, parent=e, bevel=0.001, seg=1)
            if i % 7 not in (2, 6) and i < 35:
                box("BKey", (0.014, 0.07, 0.014), (-0.44 + i * 0.0253 + 0.0126, yy - 0.02, zz + 0.012), mat=M_("black"),
                    parent=e, bevel=0.001, seg=1)
    tabs = [(0.7, 0.15, 0.1), (0.85, 0.8, 0.7), (0.1, 0.1, 0.1), (0.85, 0.8, 0.7)]
    for i in range(16):
        c = tabs[i % 4]
        box("Drawbar", (0.012, 0.02, 0.05), (-0.20 + i * 0.026, -0.14, 1.03),
            mat=cached("tab" + str(c), lambda: mat_simple("Tab", c, 0.35)), parent=e, bevel=0.002)
    box("Pedals", (0.9, 0.35, 0.05), (0, 0.10, 0.03), mat=wm, parent=e, bevel=0.004)
    box("Bench", (0.7, 0.32, 0.04), (0, 0.55, 0.50), mat=wm, parent=e, bevel=0.006)
    for lx in (-0.32, 0.32):
        box("BenchLeg", (0.03, 0.30, 0.48), (lx, 0.55, 0.24), mat=wm, parent=e, bevel=0.003)
    return e

def guitar(loc, rotz=0.0, body_col=(0.85, 0.83, 0.78), lean=0.22):
    e = empty("Guitar", loc, (lean, 0, rotz))
    bc = cached("gbody" + str(body_col), lambda: mat_simple("GuitarBody", body_col, 0.15, coat=1.0, spec=0.6))
    outline = [(0, 0), (0.10, 0.01), (0.155, 0.05), (0.17, 0.11), (0.16, 0.17), (0.13, 0.21), (0.118, 0.245), (0.128, 0.29),
               (0.14, 0.34), (0.13, 0.38), (0.105, 0.40), (0.082, 0.37), (0.062, 0.325), (0.035, 0.305), (-0.035, 0.305),
               (-0.058, 0.335), (-0.078, 0.40), (-0.098, 0.445), (-0.125, 0.435), (-0.142, 0.37), (-0.132, 0.30),
               (-0.118, 0.25), (-0.13, 0.21), (-0.16, 0.17), (-0.17, 0.11), (-0.155, 0.05), (-0.10, 0.01)]
    me = bpy.data.meshes.new("GBody"); bmg = bmesh.new()
    vs = [bmg.verts.new((x, 0.0225, z + 0.05)) for x, z in outline]
    f = bmg.faces.new(vs)
    ex = bmesh.ops.extrude_face_region(bmg, geom=[f])
    bmesh.ops.translate(bmg, vec=(0, -0.045, 0), verts=[v for v in ex["geom"] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bmg, faces=bmg.faces)
    bmg.to_mesh(me); bmg.free()
    gb = link(bpy.data.objects.new("GBody", me), e)
    gb.data.materials.append(bc)
    sd = gb.modifiers.new("sub", "SUBSURF"); sd.levels = 2; sd.render_levels = 3
    bv = gb.modifiers.new("bev", "BEVEL"); bv.width = 0.008; bv.segments = 3
    gb.modifiers.move(1, 0)
    for p_ in me.polygons:
        p_.use_smooth = True
    pg = cached("pickguard", lambda: mat_simple("Pickguard", (0.02, 0.02, 0.02), 0.25, coat=0.5))
    cyl("PG", 0.10, 0.004, loc=(0.03, -0.024, 0.26), rot=(math.pi / 2, 0, 0), mat=pg, parent=e, verts=48)
    for zz in (0.17, 0.23, 0.29):
        box("Pickup", (0.075, 0.006, 0.022), (0.0, -0.028, zz), mat=M_("white"), parent=e, bevel=0.002)
    box("Bridge", (0.08, 0.008, 0.03), (0, -0.026, 0.11), mat=M_("chrome"), parent=e, bevel=0.002)
    rw = cached("rosewood", lambda: mat_wood("Rosewood", (0.10, 0.05, 0.03), (0.16, 0.08, 0.04), scale=30))
    box("Neck", (0.050, 0.022, 0.52), (0, -0.005, 0.60), mat=rw, parent=e, bevel=0.004)
    box("Head", (0.075, 0.016, 0.18), (0, -0.003, 0.94), mat=cached("maple", lambda: mat_wood("Maple", (0.75, 0.58, 0.35), (0.82, 0.66, 0.42), scale=20)),
        parent=e, bevel=0.006)
    for i in range(6):
        cyl("Peg", 0.007, 0.03, loc=(0.045, -0.003, 0.88 + i * 0.022), rot=(0, math.pi / 2, 0), mat=M_("chrome"), parent=e)
    for i in range(6):
        box("String", (0.0009, 0.0009, 0.70), (-0.016 + i * 0.0065, -0.03, 0.52), mat=M_("chrome"), parent=e)
    for k in range(1, 12):
        box("Fret", (0.050, 0.004, 0.0015), (0, -0.017, 0.86 - k * 0.04), mat=M_("chrome"), parent=e)
    # stand
    sm = M_("black")
    x, y, z = loc
    for s in (-1, 1):
        tube("GStandL", [(x + s * 0.17, y + 0.20, z + 0.005), (x + s * 0.10, y + 0.06, z + 0.07)], 0.008, sm)
    tube("GStandB", [(x, y - 0.38, z), (x, y - 0.17, z + 0.62)], 0.008, sm)
    box("GCradle", (0.24, 0.07, 0.02), (x, y + 0.05, z + 0.075), mat=sm, bevel=0.005)
    return e

def amp(cx, cy, fz, w, h, d, tolex, grille, rotz=0.0, name="Amp"):
    e = empty(name, (cx, cy, fz), (0, 0, rotz))
    tm = cached("tolex" + str(tolex), lambda: mat_simple("Tolex", tolex, 0.65, spec=0.3, bump_scale=1800, bump_str=0.25))
    gm = cached("grille" + str(grille), lambda: mat_fabric("Grille", grille, scale=1200, sheen=0.3))
    box(name + "_cab", (w, d, h), (0, 0, h / 2), mat=tm, parent=e, bevel=0.012)
    box(name + "_grille", (w - 0.05, 0.004, h * 0.62), (0, d / 2 + 0.002, h * 0.36), mat=gm, parent=e, bevel=0.003)
    box(name + "_panel", (w - 0.05, 0.004, h * 0.18), (0, d / 2 + 0.002, h * 0.84), mat=M_("black"), parent=e, bevel=0.002)
    for i in range(6):
        cyl(name + "_knob", 0.011, 0.016, loc=(-w / 2 + 0.08 + i * (w - 0.16) / 5, d / 2 + 0.01, h * 0.84),
            rot=(math.pi / 2, 0, 0), mat=M_("chrome"), parent=e)
    box(name + "_handle", (0.16, 0.03, 0.02), (0, 0, h + 0.012), mat=M_("black"), parent=e, bevel=0.006)
    led = cached("ampled", lambda: mat_emit("AmpLED", (1.0, 0.15, 0.05), 30.0 if PASS != "halo" else 0.0))
    cyl(name + "_jewel", 0.007, 0.01, loc=(w / 2 - 0.05, d / 2 + 0.006, h * 0.84), rot=(math.pi / 2, 0, 0), mat=led, parent=e)
    return e

def diffuser(x, y, z, rotz, n=7, seed=5):
    e = empty("Diffuser", (x, y, z), (0, 0, rotz))
    om = oak()
    rnd = random.Random(seed)
    c = 0.055
    box("DiffBack", (n * c + 0.02, 0.02, n * c + 0.02), (0, 0.01, 0), mat=om, parent=e)
    for i in range(n):
        for j in range(n):
            d = rnd.choice([0.02, 0.05, 0.08, 0.11, 0.14])
            box("DiffBlk", (c - 0.004, d, c - 0.004), (-(n - 1) * c / 2 + i * c, 0.02 + d / 2, -(n - 1) * c / 2 + j * c),
                mat=om, parent=e, bevel=0.002, seg=1)
    return e

def side_sconce(name, size, cap, label, y, z, side=-1):
    """Sconce on a side wall (side=-1 left wall at x=-RW facing +x)."""
    par = empty(name + "_wall", (side * RW, 0, 0), (0, 0, -math.pi / 2 if side < 0 else math.pi / 2))
    lx = -y if side < 0 else y
    return sconce(name, size, cap, label, loc=(lx, 0, z), parent=par, spin=0.0)

LABELS12 = ["label_halo", "label_meridian", "label_afterhours", "label_sunroom", "label_promo_white", "label_promo_red", "label_promo_blue"]

def band_base(rear=1.15):
    global REAR_K
    REAR_K = rear
    band_room()
    carpet_tiles(BFZ)
    round_rug(0, 1.55, BFZ)
    drum_kit(0.0, 1.55, BFZ + 0.02)
    organ(-1.78, 0.62, BFZ, rotz=0.25)
    guitar((1.30, 0.95, BFZ + 0.03), rotz=math.pi - 0.35, body_col=(0.86, 0.84, 0.78), lean=-0.22)
    amp(1.72, 0.55, BFZ, 0.62, 0.48, 0.26, (0.04, 0.035, 0.03), (0.52, 0.40, 0.26), rotz=-0.30, name="AmpA")
    amp(2.10, 1.35, BFZ, 0.56, 0.44, 0.25, (0.55, 0.42, 0.25), (0.20, 0.14, 0.10), rotz=-0.85, name="AmpB")
    for k, (y, z) in enumerate(((2.0, 0.55), (2.0, -0.15))):
        diffuser(RW - 0.0, y, z, math.pi / 2, seed=5 + k)
    set_world((0.010, 0.010, 0.012), 1.0, 0.0)

def band_light(exp=1.15):
    # track spots on the kit + the wall art
    for x in (-0.95, 0.95):
        spot("TrackKit", (x, 2.6, BCZ - 0.12), (0, 1.55, BFZ + 0.6), 55, angle=0.55, blend=0.5)
    area("FillCam", (2.3, 6.2, 1.1), (0, 0.5, -0.6), 2.0, 11.0, color=(0.82, 0.86, 1.0))
    EXPOSURE[0] = exp

def sc_band_set():
    """Lead: 12 in + two 7 in set centred behind the kit, 3x3 statement grid on the left wall."""
    band_base()
    sconce("S12", "12", "chrome", "label_halo", loc=(0, 0, 0.42), spin=0.0)
    sconce("S7L", "7", "chrome", "label_ember45", loc=(-0.30, 0, 0.415), spin=0.0)
    sconce("S7R", "7", "chrome", "label_lantern45", loc=(0.30, 0, 0.415), spin=0.0)
    pitch = 0.395
    k = 0
    for r in range(3):
        for c in range(3):
            side_sconce(f"G{r}{c}", "12", "chrome", LABELS12[k % len(LABELS12)], 2.10 + (c - 1) * pitch, 0.18 + (1 - r) * pitch)
            k += 1
    band_light()
    frame((1.70, 6.8, 0.30), (-1.00, 1.0, -0.28),
          dict(wide=(6.0, 3.38), square=(4.3, 4.3),
               tall=dict(W=2.9, H=3.6, tgt=(-0.1, 0.0, -0.15), loc=(0.4, 6.9, 0.10)),
               ad=dict(W=3.0, H=3.75, tgt=(-0.55, 0.3, -0.12), loc=(1.2, 6.9, 0.20))))

def sc_band_row():
    """Row of three 12 in sconces centred over the kit, 3 in gaps, line of centres at 57 in + lift."""
    band_base()
    for i, lab in zip((-1, 0, 1), ("label_meridian", "label_halo", "label_afterhours")):
        sconce(f"R{i}", "12", "chrome", lab, loc=(i * 0.385, 0, 0.42), spin=0.0)
    band_light()
    frame((0.0, 6.6, 0.32), (0.0, 0.0, -0.30),
          dict(wide=(5.4, 3.04), square=(4.0, 4.0), tall=dict(W=2.8, H=3.5), ad=dict(W=2.9, H=3.6)))

def sc_band_grid():
    """Statement wall close-up: the left-wall 3x3 grid with the organ in front, three-quarter view."""
    band_base()
    sconce("S12", "12", "chrome", "label_halo", loc=(0, 0, 0.42), spin=0.0)
    sconce("S7L", "7", "chrome", "label_ember45", loc=(-0.30, 0, 0.415), spin=0.0)
    sconce("S7R", "7", "chrome", "label_lantern45", loc=(0.30, 0, 0.415), spin=0.0)
    pitch = 0.395
    k = 0
    for r in range(3):
        for c in range(3):
            side_sconce(f"G{r}{c}", "12", "chrome", LABELS12[k % len(LABELS12)], 2.10 + (c - 1) * pitch, 0.18 + (1 - r) * pitch)
            k += 1
    band_light()
    frame((1.0, 5.4, -0.05), (-2.45, 2.15, 0.05),
          dict(wide=(2.6, 1.46), square=(1.9, 1.9), tall=dict(W=1.5, H=1.9), ad=dict(W=1.6, H=2.0)), fstop=5.6)
    cam_d.dof.focus_distance = (Vector((-RW, 2.1, 0.18)) - cam.location).length
