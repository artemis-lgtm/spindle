# Band-room renders (2026-11-10)

Austin asked for the room shots to read as a studio / band room, styled after his Lord Decor basement-studio reference, with the sconces hung the way a designer would.

Finals (png/, Blender 5.0.1 Cycles, Metal GPU, 448 samples, OIDN, AgX):
- band_set_wide.png: the room. Set of three behind the kit, 3x3 statement grid on the side wall.
- band_grid_wide.png: close-up of the 3x3 statement wall. Strongest image.
- band_row_wide.png: symmetric front view, row of three 12 in over the kit.
- band_set_ad.png: 1080x1350 vertical for Meta ads.

Source: src/band_scenes.py (new scene code), src/build_studio.py splices it into a copy of renders-final/src/final.py to make src/studio.py (original untouched). Re-render: `Blender -b -P src/studio.py -- band_set wide --samples 448` (scenes band_set band_row band_grid; aspects wide square tall ad).
Fictional labels only. No band names, logos or album art. References in refs.md.

Open: the drum kit, amps and organ are procedural set dressing; for a billboard-grade shot, buy real asset models. Ad crop puts the set top-left rather than centred.
