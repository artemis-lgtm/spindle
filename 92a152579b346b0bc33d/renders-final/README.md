# Record sconce: final product image set

> **Flag, 2026-11-11 (cad/FIXES-fable52.md):** two things in this image set do not match the product the CAD builds. (1) The swap shots and the kit flat-lay show a fixed "post" the record lifts off, and a loose post in the box. There is no post: the 1/4-20 stud is part of the dome cap and comes away with it. STILL OPEN. (2) CLOSED 2026-11-11 (cad/FIXES-heat-layout.md): the halo in these images was lit with an LED ring on the BACK face of the backplate aimed at the wall, and the CAD, BOM and drawings now put the strip there too (heat-safe layout: strip on an aluminium ring over a cork ring). Two small differences remain and were not re-rendered: the images put the ring 4 to 14 mm inside the backplate rim (centre R 124) and add a weaker strip on the rim; the product's strip is 14 to 22 mm inside the rim (centre R 115) and there is no rim strip. The real halo should be compared with these images on the first prototype. Do not use the swap or flat-lay shots as assembly reference.

Open `index.html` for the contact sheet (thumbnails link to the full PNGs).

All stills are Blender 5.0.1 Cycles (Metal GPU, never EEVEE), OpenImageDenoise, AgX view
transform, 448 adaptive samples. Every PNG was opened and checked by eye after rendering.
Labels are invented ("Halo Pressings", "Meridian", "Ember", "Lantern", "After Hours",
"sunroom", promo blanks). No real labels, band names, logos or album art anywhere.

## What is in here

| Shot | Files (`png/`) | Notes |
|---|---|---|
| Heroes | `hero_chrome_*`, `hero_brass_*`, `hero_black_*` | 12 in LP on warm cream plaster, 3/4 view like the chrome hero Austin liked. Brass = brushed, black = gloss black dome with a chrome bezel. |
| 7 in single | `single7_*` | Chromed 45-adapter cap with a small jewel dome, 6 in backplate. |
| The Set | `set_*` | 12 in centre + two 7 in, reference-1 composition. Tall version adds a credenza with leaning sleeves. |
| Living room | `living_*` | Credenza, turntable, bookshelf speakers, cube record shelf, floor lamp, snake plant. Chrome. |
| Home bar | `bar_*` | Brushed brass dome on an oxblood wall, back-bar shelves of bottles, rocks glasses. (Dark green was tried first: the amber halo turned olive on it.) |
| Creative studio | `studio_*` | Black-dome 3-piece set over a desk with monitors, controller keyboard, laptop. |
| Bedroom | `bedroom_*` | Over the nightstand, the sconce is the only light source. |
| Macro | `macro_*` | Chrome dome on the label, room reflected in it, shallow depth of field. |
| Change the record | `swap1_*`, `swap2_*`, `swap3_*`, `swap_triptych.png` | No hands: dome + felt washer off, record lifted off the post (felt pads and brass insert visible), new record on. |
| Kit flat-lay | `flatlay_*` | Kraft box with pulp tray and backplate, printed lid, dome + washer + post, 45 cap, steel wall plate with bayonet studs, 12 V adapter with lead, insert card, screws/anchors/L key. |
| Install | `install_*` | In-wall cutaway rebuilt from `render/sconce_v2.py`: halo on, real label, bigger sconce in frame, warm dim room. |
| Video | `video/halo_fade_loop_1080x1920.mp4` | 8 s loop, 30 fps, 240 frames: dark room, halo eases on, holds, eases off. `video/pass_*.exr` kept so the timing can be changed in seconds; `video/qa_frame_*.png` are the dark / mid / full check frames. |

Each still exists in three formats: `_wide` 1920x1080, `_square` 1600x1600, `_tall` 1080x1920.

## How it was made

- `src/make_textures.py` (PIL): fictional labels, insert card, box lid print -> `tex/`.
- `src/final.py`: every scene except the install. Geometry follows `render/sconce_v2.py`
  (1 in hub = wall gap, 10.5 in backplate, felt pads, 1/4-20 dome on a felt washer, brass insert).
  One change for the look: a rear-facing COB ring just inside the backplate rim (plus a weaker
  side strip). With the hub's 1 in gap, a rim-only strip gave a wide washed-out glow; aiming the
  ring at the wall gives the tight amber halo of reference 1. Worth telling engineering: the halo
  in these images assumes LEDs facing the wall near the rim.
- `src/install_v3.py`: copy of `render/sconce_v2.py` (original untouched) with the camera, light,
  label and halo changes.
- `src/video_comp.py`: the loop is built from two linear EXR passes of the same frame (room only,
  halo only). Light adds linearly, so ambient + k(t) x halo is exactly what a dimmer does, at the
  cost of two renders instead of 240. Tone-mapped with Blender's own OCIO AgX so it matches the stills.
- Bar and studio glossy reflections use no HDR (it tinted the vinyl navy); living room exposure was raised after the first pass.
- `src/batch.sh`: detached renderer (nohup, absolute PATH), skips finished files. `src/build_index.py`
  makes `index.html` and `thumbs/`.

Re-render one image: `Blender -b -P src/final.py -- <scene> <wide|square|tall> --samples 448`
(scenes: hero_chrome hero_brass hero_black single7 set living bar studio bedroom macro swap1 swap2 swap3 flatlay darkroom).

## Open items

- Plants, furniture and props are procedural and read as set dressing, not hero objects. Fine for
  ads and the site. If one image goes on a billboard, buy a real plant/furniture asset pack.
- Brand name is not final, so nothing carries a brand. The kit box lid says "SCONCE KIT No. 001".
- The 7 in cap is rendered as the design report's chromed 45 adapter; the 12 in dome is 1.5 in
  diameter, low segment of sphere. Both still need machine-shop quotes (mounting-report.md).
- Nothing was sent anywhere.


## Product audit, 2026-11-11 evening: what these images show that the product does not do

Full table: `../audits/AUDIT-product.md`, section "Renders". Nothing was re-rendered. The real product: the stud is part of the cap (no post anywhere); one LED strip on the BACK of the backplate, 115 mm from the centre, facing the wall, about 4 W; record front 1.62 in off the wall on a 5 in hub; power by a cord from 6 o'clock or through the wall; only the chrome cap has a real part.

Safe to use today as they are: `macro_*` only (the dome reads a little taller than the real 10 mm cap).

Usable only with a visible line such as "Rendering. In-wall wiring shown. Real glow may differ." and only until a photo of a real unit exists: `hero_chrome_*`, `swap3_*`, `living_*`.

Do not use: `swap1_*`, `swap2_*`, `swap_triptych.png` (record stays on the wall with the cap off; LED dots on the rim; captions describe a post), `flatlay_*` (loose post, no dimmer, no PET washer, wrong wall plate, rim strip), `install_*` (says 4 screws, shows parts that are not in the box, no dimmer), `single7_*`, `set_*`, `studio_*` (the 7 in halo is not designed), `hero_brass_*`, `hero_black_*`, `bar_*` (finishes with no real part), `bedroom_*` (a 4 W strip lighting a whole room).

Re-render list, in order:
1. `swap1`: a hand holds the record flat while the cap, with its stud showing, comes out. Clear washer on the label.
2. `swap2`: the bare backplate face on: brass threaded hole, six felt pads, felt ring, nothing sticking out. No LED dots on the rim.
3. `swap_triptych`: rebuild from 1 and 2. Captions: "Unscrew the cap", "Take the record away", "Hold the next one up, screw the cap in".
4. `flatlay`: remove the post. Add the inline dimmer, the clear washer, the real 45 adapter, the straight hex driver. Stud on the cap. Hub fixed to the backplate. Real wall plate (30 x 37 slot, four arc slots, bent tab, three studs). Card text: set screw at about 6:40. Same contents in all three crops.
5. `install`: "2 screws + 2 anchors". Draw the surface cord with dimmer and adapter. Mark in-wall parts "not included". Leaders off the record face.
6. Every lit scene, starting with `hero_chrome` and `bedroom`: move the light to one ring 115 mm from the centre on the back face, delete the rim strip, expose for about 4 W. Add the cord or say it is in the wall.
7. New: one true side view showing the 1 in gap, the 5 in hub and the record 1.62 in off the wall. One room shot with a surface cord.
8. `single7`, `set`, `studio`: hold until the 7 in halo is designed.
9. Label names "Ember", "Meridian": check against real record labels before any paid use (Ember Records was a real UK label).
