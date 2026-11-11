# Pessimist review: RS-CAP-12 (plain, rev B -> rev C) and RS-CAP-12L (lit) in the full sconce

2026-11-10. Reviewer brief: assume everything fails, find out how, fix what can be fixed in the CAD/spec/BOM, say what cannot.
Scope: both caps, the E-Z Lok insert, hub RS-HUB-01, backplate RS-BP-12-MDF, felt pads, halo strip, hub contact module.
Numbers come from `sconce_cad.py` / `sconce_lit.py` via `checks.md` (regenerated) unless marked E (estimate).
Nothing was sent to anyone. Rev B zip (`rfq/dome-cap-RS-CAP-12-revB.zip`) is kept untouched because it already went out;
the rev C zip sits beside it.

Severity: S1 = destroys hardware or the customer's record; S2 = product does not work as sold / visible defect; S3 = reliability
over years; S4 = cosmetic or process.

## Findings, worst first

### 1. S1, FIXED: a plain RS-CAP-12 rev B in a lit sconce crushes the centre spring pin
- Rev B stud 13.3 vs lit 11.6. In a lit sconce the plain stud reached the Mill-Max 0919 at 3.4 mm compression (nominal) and
  4.5 mm with a thin record; the pin's whole stroke is 3.0. Beyond the stroke the plunger coil-binds, and the user then puts a
  hand-tightened 1/4-20's preload (~800 N at 1 N.m) on a 1.07 mm plunger: barrel pushed through the PEEK bore, PCB pad torn,
  pin dead. DESIGN.md called this "not dangerous" and relied on "ship lit sconces with lit caps". It is not a packing problem:
  plain caps are sold in three finishes as their own product and a lit-sconce owner buying a black plain cap for the look is
  the normal case.
- Fix: **RS-CAP-12 rev C**, stud 13.3 -> 11.7, identical to the lit stud (`assert LC_STUD_L == S.CAP12_STUD_L` in the lit
  source so they cannot drift again). Plain cap in a lit sconce now compresses the pin 0.83..2.98, the same as the lit cap,
  and only shorts the 20 mA regulator. Plain cap in a plain sconce: engagement 7.5 mm (6.0 threaded), worst-case stud end (1.5 mm record,
  no felt) 4.1 mm short of the backplate back face (rev B: 2.5 mm short; neither was ever proud). Dome, band, recess unchanged, so the
  shop re-quotes one dimension. New zip: `rfq/dome-cap-RS-CAP-12-revC.zip`.

### 2. S1/S2, PARTLY FIXED: the 3.0 mm pogo stroke is too small for real records
- Design envelope was 1.3..2.4 mm at the label. Real: RCA Dynaflex and other late-70s flexi pressings are 1.0..1.2; 1950s
  deep-groove and many 180/200 g pressings have a raised label area at 2.6..3.0. Stack variation the pin must absorb = record
  range + felt pads (1.4..1.6) + cap felt (0.15..0.6). With 11.6 the thin case already used 2.78 of 3.0; a 1.2 record bottomed it.
- Fix: stud 11.7 and envelope re-centred to **1.2..2.7** (compression 2.98 / 1.80 / 0.83 thin/nominal/thick, rated 0.76..3.00).
  That is everything the 0919 can give. Below 1.2 the pin bottoms (hard stop, same damage as finding 1); above 2.7 the light
  may flicker. Not fixable in CAD: it needs a 4 mm+ stroke spring pin (then 1.0..3.2 would fit). Flagged in DESIGN.md failure
  modes; measure 10 real records before the PCB order and pick the pin then.

### 3. S2, FIXED (spec): the halo strip can cook the record's top edge
- Engineering report allows 8..10 W of COB on the MDF rim. MDF is an insulator; COB strips are quoted at 45..65 C surface ON
  ALUMINIUM in a <30 C room. On MDF, under the record's 19 mm overhang (the strip top is 3 mm behind the record's back face,
  the record edge 19 mm radially outboard), the strip surface runs 60 C+ at 30 C ambient (E) and the record's top edge sits in
  its plume at 40..45 C, with the strip radiating at it from 3..10 mm. Vinyl softens at 55..60 C; the same report cites slow
  warping from 30..38 C under load. The interior is fine: the record's back face is 1.6 mm off a mostly-ambient MDF front face,
  so the label area stays within ~5 K of room (E). The danger is the free overhanging edge at 12 o'clock, and the strip's own
  phosphor life.
- Fix: hard limit **6 W per 12 in sconce** (low-power 2835 60/m at 1.46 W/ft = 4 W, or COB of no more than 8 W/m), written
  into cad/README.md "Open questions 7" and build/BOM.md 4b, with an acceptance test (4 h at 30 C: record edge <= 40 C, label
  <= 38 C, strip <= 55 C). If the ring moves behind the backplate facing the wall (the renders-final flag, still unresolved
  in the CAD), the 1 in cavity traps the heat and the limit drops to 4 W unless the hub is vented. Not changed: the strip
  position itself (that is an open design conflict, not mine to pick).
- Lit cap heat: 0.17 W in a 38 mm brass cap. Convection-only worst case +11 K, with conduction into the record and stud +5..8 K
  (E): cap at 36..38 C in a 30 C room. No risk to the label paper or the vinyl. Hub CCR 0.07 W normally, 0.24 W when the pin is
  shorted: see finding 7.

### 4. S2, FIXED: insert sitting 0.3 proud crushes the hub contact module
- The E-Z Lok 400-4 is 0.500 long in a 0.500 backplate and is hand-driven, so +/-0.3 flush is realistic. The carrier top was
  0.05 below the insert's back face with the PCB hard on the relief floor and nothing compliant in between: a proud insert
  meant the hub could not seat or the PCB cracked when the three #8 screws went in.
- Fix: carrier top 0.35 below the insert face (CAR_Z1 -0.05 -> -0.35, carrier 2.55 tall). Return pogo height is unchanged at
  2.90 (2.50..3.48 covers +/-0.3). Spigot still pilots 1.65 into the insert.

### 5. S2, FIXED: the dome boss drags the LED PCB round when it is torqued down
- The PCB ring (ID 8.2 on an 8.0 spigot) is clamped by screwing the dome's boss down on it. Friction turns the board with the
  dome for the last turn: the 30 AWG lead soldered at r 6.4 winds around the column and tears, and the six LEDs (at 30/90/...
  deg) end up behind the louver ribs (also at 30/90/... deg) which the optics model assumed they avoid.
- Fix: the first 0.9 mm of the spigot above the column is an unthreaded D (flat at 3.6 from the axis); the PCB centre hole is
  a matching D (flat at 3.7). The board cannot rotate; the dome's thread engagement goes 3.2 -> 3.1 (still 6 turns of M8x0.5).
  In `sconce_lit.py`, `pcb.py` (DXF outline), PCB-SPEC.md, rfq-SPEC.txt.

### 6. S3, FIXED (spec + BOM): static discharge from the record through the LEDs
- A vinyl record coming out of a sleeve carries kilovolts. The cap's stud tip exposes the gold pin (LED+) and the dome is LED-:
  a customer holding the dome and touching the tip to anything, or a charged record brushing the pin during the swap, puts the
  discharge through six 2835 LEDs (1..2 kV HBM class). On the hub side the exposed pogo node leads straight into the CCR.
- Fix: Z1, a 12 V bidirectional 0402 ESD/TVS on each board (LED+ to LED- in the cap; pogo node to return in the hub).
  +$0.06 per sconce at 100 (BOM-delta regenerated: +$30.87 at 100, was +$30.81).

### 7. S3, FIXED (spec): the CCR cooks when the pin is shorted
- With a plain cap, a metal chip, or a screwdriver in the insert, U1 (NSI45020, SOD-123) dissipates 12 V x 20 mA = 0.24 W
  continuously inside a PEEK pocket on a 13 mm board inside MDF. Its rating assumes a copper pour; on bare pads that is
  80 K+ over ambient (E). The CCR's negative tempco saves it from dying, not from running at 100 C against the PEEK and MDF.
- Fix: PCB-SPEC.md now calls out >= 25 mm2 copper on each U1 pad stitched to the bottom layer. The plain-cap short itself is
  now rare (finding 1) and benign.

### 8. S3, FIXED: cross-threading and vinyl shavings in the insert
- A 0.5 chamfer on a 1/4-20 stud entered a brass insert blind, through a record with 0.45 mm of radial slop: cross-threading
  brass-on-brass (galling, insert ruined, the backplate with it) is a matter of time across 100 customers and 500 swaps.
  Separately, the record is slid down over thread crests at every swap, which shaves PVC into the insert, and in the lit
  sconce the shavings land on the 1 mm pogo plunger and switch the label light off.
- Fix: both caps (and RS-CAP-7) get an unthreaded **dog point D 4.8 x 1.5** at the tip: it enters the insert's minor diameter
  before any thread can bite, and the record's hole rides a smooth pilot. Threaded engagement with a nominal 12 in record is
  6.3 mm (lit) / 6.0 mm (plain), 5.3 mm with a 2.7 record: still over 4 threads of 1/4-20 in brass, about 8 kN before the
  thread strips (E), against a 160 g record and a sub-1 kN hand preload. The card should still say "if the label light goes
  out after a swap, blow out the centre hole".

### 9. S3, FIXED (spec): the return contact relies on a bare insert back face, but the SOP puts CA in the hole
- The engineering report says to wet the 25/64 bore with CA or epoxy before driving the insert. Squeeze-out on the insert's
  back end face is an insulating film under the 0906 return pogo: no label light, and it is behind the hub where nobody can
  reach it. Also, PEEK sleeve retention with Loctite 609: anaerobics do not bond PEEK.
- Fix (spec only): adhesive in the bore only, wipe the back face, continuity < 1 ohm from stud to hub PCB at final test
  (DESIGN.md failure modes); stake the bore mouth at 3 points after pressing the sleeve (rfq-SPEC.txt).

### 10. S3, NOT CHANGED: preload decays, the record ends up loose
- The clamp runs through 1.6 mm of felt pads, 2 mm of PVC, the label paper and 0.6 mm of cap felt. Felt takes 30..50 %
  compression set under load in warm rooms; PVC creeps. Over weeks the ~800 N preload goes to near zero and the cap can be
  turned with a finger; the record does not fall (nothing unscrews it) but it can rattle on the pads and rotate when a door
  slams. Rev B's recess already makes this benign: once the felt has crept, the chrome band (plain) or the nickel flange (lit)
  bottoms on the label at 1 MPa (E), a hard stop that stops the creep. The customer re-snugs once. Not fixable without a spring
  element, and a spring element would show. Keep "snug by hand, re-snug after a week" on the card. Thermal cycling and the
  MDF's humidity swelling (+/-0.05 mm) are noise next to the felt.

### 11. S3, NOT CHANGED: insert squareness tilts the cap
- A hand-driven E-Z Lok can sit 1..2 deg off the backplate normal. Over the 38 mm cap that is 0.33..0.66 mm: the band seats on
  one side and shows the rev A shadow gap on the other (the very thing rev B was meant to kill), and in the lit sconce 1 deg
  moves the stud tip 0.2 mm, eating the entire 0.25 mm misalignment budget of the coax contact (the brass-to-pogo guard still
  has 0.59 mm left at 1 deg, 0.39 at 2 deg: no short). Fix is in the SOP, not the CAD: drill the bore on the CNC (it is), drive
  the insert in a drill press with a 1/4-20 arbor, squareness within 0.5 deg.

### 12. S4, NOT CHANGED: things the spec already handles or cannot
- Centre hole 7.24 vs stud 6.35: 0.45 mm of slop means the record hangs 0.45 low on the stud, invisible on a 19 mm overhang;
  friction after clamping holds it. Oversize worn holes to ~7.6 are fine. Nothing centres the record on the cap; nothing needs to.
- Felt clamp pressure: plain 1.1 MPa over the 31.75 washer (E); lit 8 MPa over the tiny 12.7 x 6.35 washer (E) until the felt
  bottoms and the flange takes over at ~0.9 MPa. That embosses a faint ring in the label paper around the spindle hole, where
  every record already carries spindle wear. Enlarging the lit felt is not possible: the core's web over a bigger recess would
  be 0.3 mm under the louver floor. Accepted.
- Warped records: the centre clamp pulls the label flat and the three outer pads define the plane; the 19 mm overhang shows
  whatever warp the record has. Customer's record, not ours.
- Chrome dome is the return conductor at up to 12 V from a Class 2 source (floating, 2-prong adapter): touch-safe by any
  standard; with a low-side PWM dimmer it toggles 0..12 V, still Class 2. Unscrewing live: the pin leaves the pogo 1..3 mm
  before the thread lets go, 20 mA, no arc; the exposed pogo then sits 12 mm down a 5 mm hole behind a 20 mA limit.
- UL/ETL: the sconce is a cord-connected 12 V Class 2 device fed by a listed adapter, sold like every LED strip kit; that is
  honest for the plug-in version. Nobody will list the lit cap separately. The hardwired option C needs UL 2108 before it is
  advertised as such, and product-liability insurance will ask. Not a CAD matter.
- Dropping the lit cap: brass dome, PC window, 0.25 mm SLA fins. A drop onto tile cracks the window or louver. The cap is not
  serviceable (Loctite 270 LH joint). Price a spare-cap SKU.
- Hub PETG at Tg 80 C is fine at the 6 W limit; if the halo ever moves into the hub cavity, re-check it.
- Drawing sheets still print DATE 2026-11-09 (constant in drawings.py); left alone.

## What changed (files)
- `cad/sconce_cad.py`: `CAP12_STUD_L` 13.3 -> 11.7 (rev C), `CAP_STUD_DOG_D/L` 4.8 x 1.5, `stud_tip()` used by both caps.
- `cad/sconce_lit.py`: `LC_STUD_L` 11.7 (+ assert equal to plain), `CAR_Z1` -0.35, `SPG_KEY_X/H` spigot flat, D-hole PCB,
  record envelope 1.2..2.7, dog point, new clearance keys.
- `cad/drawings.py` (rev C sheet, dog point, derived text), `cad/drawings_lit.py` (dog point + key notes).
- `cad/build_all.py`: rev C RFQ text derived from the parameters; builds `rfq/dome-cap-RS-CAP-12-revC.zip` on every run.
- `cad/label-light/pcb.py`, `PCB-SPEC.md`, `bom_delta.py` (+BOM-delta.md/.csv), `rfq-SPEC.txt`, `DESIGN.md`.
- `cad/README.md` (rev C numbers, halo thermal limit), `build/BOM.md` 4b.
- Rebuilt: all STEP/STL/DXF, drawings, previews, `checks.md` (0 interferences in 7 assemblies incl. thin/thick lit cases),
  both RFQ zips.

## Final spec headlines
- **RS-CAP-12 rev C (plain):** brass C360, chrome (or brass / black), D 38.1 x 10.0 (1.6 band + R 25.8 dome), underside recess
  D 33 x 1.0 for a 1-1/4 x 3/8 x 1/16 felt, integral 1/4-20 UNC-2A stud 11.7 long with a D 4.8 x 1.5 dog point. Engagement 7.5
  mm (6.0 threaded) in the E-Z Lok 400-4.
- **RS-CAP-12L rev A.1 (lit):** same outside; hollow chrome dome on an EN-nickel brass core, 14.8 tall over the label (4.8 mm
  frosted light band under the lip), hollow 1/4-20 stud 11.7 + dog point, coax: gold pin in a PEEK sleeve down the stud bore,
  stud/insert = return. 6x LUXEON 2835 2700 K at 10 mA, 20 mA CCR in the hub, 0.24 W from the 12 V adapter, 0.17 W in the cap,
  records 1.2..2.7 mm at the label. Halo strip limit 6 W per sconce.
