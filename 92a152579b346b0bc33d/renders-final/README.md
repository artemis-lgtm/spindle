# Record sconce: final product image set

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
