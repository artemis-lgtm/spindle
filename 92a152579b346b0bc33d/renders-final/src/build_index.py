"""Build renders-final/index.html (contact sheet) + thumbs/ from png/ and video/."""
import os, html
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PNG, TH = os.path.join(ROOT, "png"), os.path.join(ROOT, "thumbs")
os.makedirs(TH, exist_ok=True)

SECTIONS = [
    ("Heroes", "Warm cream plaster, dusk, the halo doing the work. 12 in LP, 1.5 in dome cap.",
     [("hero_chrome", "Chrome dome (lead finish)"), ("hero_brass", "Brushed brass dome"), ("hero_black", "Gloss black dome, chrome bezel")]),
    ("7 in single", "Chromed 45-adapter cap on a 6 in backplate.", [("single7", "7 in single, chrome")]),
    ("The Set", "12 in centre + two 7 in, reference-1 composition.", [("set", "3-piece set, chrome")]),
    ("Lifestyle", "Same fixture, four rooms.",
     [("living", "Living room: turntable + record shelf"), ("bar", "Home bar: brass dome, oxblood wall"),
      ("studio", "Creative studio: black-dome set"), ("bedroom", "Bedroom: the sconce is the only light")]),
    ("Macro", "Chrome dome on the label, reflecting the room.", [("macro", "Dome macro")]),
    ("Change the record", "Three frames, no hands: dome off, record off, new record on.",
     [("swap1", "1. Dome off"), ("swap2", "2. Record lifted"), ("swap3", "3. New record on")]),
    ("Kit flat-lay", "Box + pulp tray, backplate, dome + felt washer, 45 cap, steel wall plate, 12 V adapter, insert card, hardware.",
     [("flatlay", "Kit contents")]),
    ("Install", "In-wall cutaway: CL2 cable down the stud bay to a keystone DC plate; adapter stays at the outlet.",
     [("install", "In-wall cutaway, halo on")]),
]
ASPECTS = [("wide", "1920x1080"), ("square", "1600x1600"), ("tall", "1080x1920")]

def thumb(name):
    src = os.path.join(PNG, name + ".png")
    if not os.path.exists(src):
        return None
    dst = os.path.join(TH, name + ".jpg")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        im = Image.open(src).convert("RGB")
        im.thumbnail((720, 720))
        im.save(dst, quality=84)
    return f"thumbs/{name}.jpg"

parts = []
for title, blurb, items in SECTIONS:
    parts.append(f"<section><h2>{html.escape(title)}</h2><p class=b>{html.escape(blurb)}</p>")
    for key, cap in items:
        parts.append(f"<h3>{html.escape(cap)}</h3><div class=row>")
        for a, res in ASPECTS:
            n = f"{key}_{a}"
            t = thumb(n)
            if t:
                parts.append(f'<figure class={a}><a href="png/{n}.png"><img loading=lazy src="{t}" alt="{html.escape(cap)} {res}"></a>'
                             f"<figcaption>{res} . png/{n}.png</figcaption></figure>")
            else:
                parts.append(f"<figure class='{a} missing'><div>not rendered</div><figcaption>{res}</figcaption></figure>")
        parts.append("</div>")
    if key == "swap3" and os.path.exists(os.path.join(ROOT, "png", "swap_triptych.png")):
        t = "thumbs/swap_triptych.jpg"
        im = Image.open(os.path.join(ROOT, "png", "swap_triptych.png")).convert("RGB"); im.thumbnail((1400, 1400)); im.save(os.path.join(ROOT, t), quality=84)
        parts.append(f'<h3>Triptych</h3><div class=row><figure class=strip><a href="png/swap_triptych.png"><img src="{t}"></a><figcaption>png/swap_triptych.png</figcaption></figure></div>')
    parts.append("</section>")
vid = "video/halo_fade_loop_1080x1920.mp4"
if os.path.exists(os.path.join(ROOT, vid)):
    parts.append(f"<section><h2>Video loop</h2><p class=b>8 s, 1080x1920, halo fades on in a dark room and back off (seamless loop).</p>"
                 f"<div class=row><figure class=tall><video src='{vid}' autoplay muted loop playsinline controls></video>"
                 f"<figcaption>{vid}</figcaption></figure></div></section>")

page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Record Sconce Renders</title><style>
:root{{--bg:#16130f;--fg:#efe7da;--mute:#a89c8a;--card:#221d17;--line:#3a3127;--acc:#e9a25a}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif}}
header{{padding:32px 16px 8px;max-width:1500px;margin:auto}} h1{{margin:0;font-weight:600;letter-spacing:.01em}}
header p{{color:var(--mute);max-width:70ch}} section{{max-width:1500px;margin:auto;padding:8px 16px 24px;border-top:1px solid var(--line)}}
h2{{color:var(--acc);font-weight:600;margin:20px 0 2px}} h3{{font-weight:500;margin:14px 0 6px}} .b{{color:var(--mute);margin:0 0 6px}}
.row{{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap}} figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:6px}}
figure img,figure video{{display:block;width:100%;height:auto;border-radius:3px}} figcaption{{color:var(--mute);font-size:12px;margin-top:4px;word-break:break-all}}
.wide{{flex:1 1 420px;max-width:560px}} .square{{flex:1 1 280px;max-width:330px}} .tall{{flex:1 1 180px;max-width:200px}} .strip{{flex:1 1 100%}}
.missing div{{aspect-ratio:1;display:grid;place-items:center;color:var(--mute)}}
@media (max-width:600px){{.wide,.square,.tall{{max-width:100%;flex-basis:100%}}}}
</style></head><body><header><h1>Record sconce: product image set</h1>
<p>Blender Cycles renders (never EEVEE), OpenImageDenoise, AgX. Labels are invented (no real labels, bands or logos). Click any image for the full-size PNG. Built from render/sconce_v2.py geometry: 1 in hub, 10.5 in backplate, rear COB ring, felt pads, 1/4-20 dome cap.</p></header>
{''.join(parts)}</body></html>"""
open(os.path.join(ROOT, "index.html"), "w").write(page)
print("index ok")
