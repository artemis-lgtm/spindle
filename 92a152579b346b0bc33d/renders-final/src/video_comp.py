"""Halo fade-on loop, 1080x1920, from two linear EXR passes (light is additive, so
ambient + k(t) * halo is exactly what a dimmer does). Tone-mapped with Blender's own
OCIO AgX view so it matches the stills, piped to ffmpeg.

Run with Blender's Python:  Blender -b -P video_comp.py
"""
import bpy, os, sys, math, subprocess
import numpy as np
import PyOpenColorIO as OCIO

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.environ.get("VDIR", os.path.join(HERE, "..", "video"))
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FPS, SECONDS = 30, 8
EXPOSURE = 0.6
LOOK = "AgX - Medium High Contrast"

def load(name):
    im = bpy.data.images.load(os.path.join(V, name))
    w, h = im.size
    a = np.empty(w * h * 4, dtype=np.float32)
    im.pixels.foreach_get(a)
    a = a.reshape(h, w, 4)[::-1, :, :3].copy()   # Blender stores bottom-up
    return a, w, h

amb, W, H = load("pass_ambient.exr")
halo, _, _ = load("pass_halo.exr")

cfg = OCIO.Config.CreateFromFile(bpy.utils.resource_path("LOCAL") + "/datafiles/colormanagement/config.ocio")
t = OCIO.DisplayViewTransform(src="Linear Rec.709", display="sRGB", view="AgX")
lt = OCIO.LookTransform(src="Linear Rec.709", dst="Linear Rec.709", looks=LOOK)
grp = OCIO.GroupTransform([lt, t])
try:
    cpu = cfg.getProcessor(grp).getDefaultCPUProcessor()
except Exception as e:
    print("look failed, view only:", e)
    cpu = cfg.getProcessor(t).getDefaultCPUProcessor()

def k_of(f):
    """0..1 dimmer level: dark 1 s, ease on 3 s, hold 2.5 s, ease off 1.5 s (loops)."""
    s = f / FPS
    def ease(x):
        x = min(max(x, 0.0), 1.0)
        return x * x * (3 - 2 * x)
    if s < 1.0:
        v = 0.0
    elif s < 4.0:
        v = ease((s - 1.0) / 3.0)
    elif s < 6.5:
        v = 1.0
    else:
        v = 1.0 - ease((s - 6.5) / 1.5)
    return v ** 2.2          # perceptual dimmer curve

gain = 2.0 ** EXPOSURE
out = os.path.join(V, "halo_fade_loop_1080x1920.mp4")
cmd = [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", "-movflags", "+faststart", out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for f in range(FPS * SECONDS):
    k = k_of(f)
    lin = np.ascontiguousarray((amb + k * halo) * gain, dtype=np.float32)
    cpu.applyRGB(lin)
    rgb = (np.clip(lin, 0, 1) * 255 + 0.5).astype(np.uint8)
    p.stdin.write(rgb.tobytes())
    if f in (0, 75, 165):
        # QA stills: dark, mid fade, full on
        bpy.data.images.new("q", W, H)
        q = np.concatenate([lin, np.ones((H, W, 1), np.float32)], axis=2)[::-1].ravel()
        im = bpy.data.images.new(f"qa{f}", W, H)
        im.colorspace_settings.name = "Non-Color"
        im.pixels.foreach_set(q)
        im.filepath_raw = os.path.join(V, f"qa_frame_{f:03d}.png")
        im.file_format = "PNG"
        im.save()
p.stdin.close()
p.wait()
print("WROTE", out, p.returncode)
