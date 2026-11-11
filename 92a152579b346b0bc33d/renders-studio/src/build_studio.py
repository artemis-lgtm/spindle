"""Splice band_scenes.py into a copy of renders-final/src/final.py -> studio.py (original untouched)."""
import os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "../../renders-final/src/final.py")).read()
band = open(os.path.join(H, "band_scenes.py")).read()
src = src.replace('TEX = os.path.join(ROOT, "tex")', 'TEX = os.path.normpath(os.path.join(ROOT, "..", "renders-final", "tex"))')
src = src.replace('RES = dict(wide=(1920, 1080), square=(1600, 1600), tall=(1080, 1920))',
                  'RES = dict(wide=(1920, 1080), square=(1600, 1600), tall=(1080, 1920), ad=(1080, 1350))')
a, b = src.split("SCENES = dict(", 1)
b = b.replace("flatlay=sc_flatlay, darkroom=sc_darkroom)",
              "flatlay=sc_flatlay, darkroom=sc_darkroom, band_set=sc_band_set, band_row=sc_band_row, band_grid=sc_band_grid)")
open(os.path.join(H, "studio.py"), "w").write(a + band + "\n\nSCENES = dict(" + b)
print("ok")
