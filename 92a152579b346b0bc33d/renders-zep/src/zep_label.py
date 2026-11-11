"""Mockup label: a real-band record (Led Zeppelin IV, side one) for Austin's close-up.
Original typesetting only, no copied label logo or album art. Internal mockup, not a product."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "renders-final", "src"))
from make_textures import Image, ImageDraw, S, C, OUT, font, ctext, ring, tracks, paper

def label_zep():
    im = Image.new("RGB", (S, S), (150, 34, 40))
    d = ImageDraw.Draw(im)
    cream, deep = (238, 226, 200), (96, 18, 24)
    ring(d, 990, 18, deep); ring(d, 950, 4, cream); ring(d, 440, 4, cream)
    ctext(d, 400, "LED ZEPPELIN", font("copper", 140), cream)
    ctext(d, 485, "STEREO  .  SD 7208", font("futura", 50), cream)
    d.text((300, C), "SIDE 1", font=font("futura_b", 56), fill=cream, anchor="lm")
    d.text((S - 300, C), "33 1/3", font=font("futura_b", 56), fill=cream, anchor="rm")
    tracks(d, 1600, ["1. BLACK DOG  4:55", "2. ROCK AND ROLL  3:40",
                     "3. THE BATTLE OF EVERMORE  5:38", "4. STAIRWAY TO HEAVEN  8:02"],
           font("futura", 42), cream, 54)
    return paper(im, 12, 21)

if __name__ == "__main__":
    p = os.path.join(OUT, "label_zep.png"); label_zep().save(p); print(p)
