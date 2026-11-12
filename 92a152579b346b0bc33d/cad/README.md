# Record Sconce: manufacturer-ready CAD

> **Product audit, 2026-11-11 evening (`../audits/AUDIT-product.md`).** Changes in this folder: RS-HUB-01 is **rev C** (the set-screw tab pocket is now an arc covering the whole 20 degree twist; the rev B hub could not be hung, the plate tab hit solid hub, 114 mm3 of overlap at every step). RS-WP-01 is **rev B** (single-gang arc slots +/-8 degrees instead of +/-10, so every PEM stud hole has 7.14 mm of steel to the nearest edge; stud holes D 4.17, inside PEM's 4.14 to 4.22). New gates, tag AUDIT: the hang-and-twist motion is checked for overlap at 13 positions with a negative control; PEM edge distance is probed on the solid; the seven-straight-piece strip layout is proven to fit the ring and miss the screws. The halo strip solid is still drawn as a circle, which no flat strip can follow: see `sconce_cad.py` at `HALO_POLY_N`. `THERMAL.md` has a corrected vinyl limit (48 to 52 C, sourced) and a sensitivity table.

> **Current revisions (2026-11-11):** RS-CAP-12 **rev D**, RS-CAP-7 **rev C**, RS-CAP-12L (lit cap + hub module) **rev B**, RS-BP-12-MDF **rev C**, RS-BP-7-MDF **rev B**, new RS-HR-12 (aluminium heat ring) and RS-CK-12 (cork ring) **rev A**, RS-HUB-01 **rev B**; RS-WP-01 and the aluminum plates are rev A.
> **Heat-safe halo (2026-11-11):** on the 12 in MDF sconce, plain cap and lit cap alike, the LED strip is on the BACK of the backplate facing the wall, on a 1.0 aluminium ring over a 1.6 (1/16 in) cork ring. It is no longer on the rim. What changed, every file touched and what is not verified: `FIXES-heat-layout.md`. The numbers: `THERMAL.md`. The 7 in sconce and the aluminium-backplate variants are NOT covered by this layout.
> Everything older is SUPERSEDED: do not quote or build it. What changed and why: `FIXES-fable52.md` (answering `REVIEW-fable52.md`) and `FIXES-heat-layout.md`. The index of quote packets is `rfq/README.md`; old zips are in `rfq/SUPERSEDED-do-not-quote/`.
> `build_all.py` now ends with regression gates (`gates.py`, printed at the top of `checks.md`): it exits non-zero if any fixed dimension or stale claim comes back.

Built 2026-11-09 (overnight brief). Parametric CadQuery 2.8 source, STEP as the master format, with STL for printed parts,
DXF for flat parts, 2D drawings (PDF + PNG) and per-vendor RFQ packets. Nothing has been sent or ordered; the RFQ text is
drafted to files only. All decisions follow ../NOTES.md, ../engineering-report.md, ../mounting-report.md and
../design-report.md; where the CAD had to add a detail the reports did not fix, it is listed under "Design calls made here".

## Folder map

| Path | What |
|---|---|
| `sconce_cad.py` | every part as a function of named parameters (mm). Edit here, never the STEP. |
| `assembly.py` | placement of all solids, boolean interference check, derived clearance numbers |
| `sconce_lit.py`, `assembly_lit.py`, `drawings_lit.py`, `label-light/` | the lit cap RS-CAP-12L and its hub contact module |
| `thermal.py`, `THERMAL.md`, `thermal-results.json` | heat model of the halo strip against the record; re-run by every build on the CAD's own dimensions |
| `explode_view.py`, `explode_lit.py`, `explode_fix.py` | labelled exploded drawings in `../renders-exploded/` (plain, lit, heat-safe with side cut), all from the canonical parts |
| `gates.py` | regression gates: clearances, point-in-solid probes on the built parts, stale-sentence checks on the BOM / site / reports |
| `drawings.py`, `dxf_out.py`, `preview.py`, `blender_preview.py` | 2D drawings, DXF export, PNG previews, Cycles renders |
| `build_all.py` | one command rebuilds everything: `.venv/bin/python build_all.py` (about 45 s) |
| `parts/` | STEP / STL / DXF per part |
| `assemblies/` | STEP assemblies (named, coloured): 12 in MDF, 7 in MDF, 12 in aluminum 5 mm and 3 mm |
| `drawings/` | PDF + PNG drawing sheets with dimensions, tolerances, material and finish notes |
| `previews/` | PNG preview of each part (front + rear), assembly previews, `*_cycles.png` Blender renders, `*_dxf.png` what the laser vendor sees |
| `rfq/<part>/` | files + `SPEC.txt` a shop or online quoter accepts (SendCutSend, OSH Cut, Xometry, a local CNC shop, a brass turner + plater) |
| `checks.md`, `checks.json` | interference + clearance report |
| `.venv/` | Python 3.12 venv with cadquery, ezdxf, matplotlib (gitignored) |

## Parts list

| Part no. | Part | Qty / unit | Process, material | Files |
|---|---|---|---|---|
| RS-BP-12-MDF | Backplate 12 in record, D 266.7 x 12.70 +/-0.15, 6 felt targets + centre-ring witness circle, plain rim (no rabbet), 4 blind pilots on the back (rev C) | 1 | CNC router, 1/2 in MDF only (no birch), painted matte black all over | step, stl, dxf, drawing |
| RS-HR-12 | Heat ring, flat, OD 260 x ID 200 x 1.0, 4x D 3.3 on R 105.5: carries the LED strip and spreads its heat (rev A) | 1 (12 in MDF) | laser cut 5052-H32 aluminium 0.040 in, bare | step, dxf, drawing |
| RS-CK-12 | Cork ring, OD 260 x ID 200 x 1.6 (1/16 in), 4x D 4.0 on R 105.5: heat break between the aluminium ring and the MDF (rev A) | 1 (12 in MDF) | die / knife cut 1/16 in cork sheet or roll | step, dxf, drawing |
| RS-BP-7-MDF | Backplate 7 in record, D 152.4 x 12.7, rim rabbet for a rim strip (rev B, not on the heat-safe layout) | 1 (7 in SKU) | same as RS-BP-12-MDF | step, stl, dxf, drawing |
| RS-BP-12-AL5 / -AL3 | Backplate 12 in, flat aluminum 5 mm / 3 mm (floating-record configuration) | alt | laser/waterjet 5052, powder coat | step, dxf, drawing |
| RS-BP-7-AL5 | Backplate 7 in, flat aluminum 5 mm | alt | same | step, dxf, drawing |
| RS-HUB-01 | Hub, D 127 x 25.4, twist-lock (locks clockwise), power pigtail + P-clip, 9.1 centre relief (rev B) | 1 | FDM PETG/ASA now, injection mould later | step, stl, drawing |
| RS-WP-01 | Wall mounting plate, D 101.6, 14 ga steel, one bent tab, 3 PEM studs | 1 | laser + bend + PEM, zinc | step, flat dxf, drawing |
| RS-CAP-12 | Dome cap D 38.1 x 10.0, integral 1/4-20 x 11.95 stud, D 7.10 smooth shoulder, dog point (rev D) | 1 | turned brass C360, polished, plated (-CR / -BR / -BK) | step, stl, drawing |
| RS-CAP-7 | Dome cap D 48.0 x 8.5 with D 37.6 locating boss, 1/4-20 x 12.6 stud (rev C) | 1 (7 in SKU) | same | step, stl, drawing |

Purchased parts modelled for fit (envelopes, not vendor CAD): E-Z Lok 400-4 insert, 8 mm LED strip, 4x #4 x 3/8 pan-head heat-ring screws, 1/2 in felt pads,
centre backing ring and cap felt (die-cut 1-1/4 x 3/8 x 1/16 in), PET label washer, PEM FH-832-10 studs, 8-32 nylon lock nuts,
#8 pan-head wall screws, 150 mm power pigtail with inline 5.5 x 2.1 jack + P-clip + the adapter's plug, M3 x 12 set screw, 3/8 in x 1 in 1/4-20 standoff and 1/4-20 flat/pan head (aluminum variant), 6 x 12 neon-flex ring
(aluminum variant), the customer's 12 in / 7 in record.

## Key dimensions (mm, inches in brackets)

- Wall gap (hub thickness) 25.4 [1.00]; record overhang past the backplate 19.05 (12 in) / 12.7 (7 in).
- Halo, 12 in MDF (heat-safe layout, plain and lit): 8 mm strip on the BACK of the backplate, LEDs toward the wall, centred on
  R 115 (R 111 to 119), on the aluminium ring RS-HR-12 (1.0) over the cork ring RS-CK-12 (1.6, 1/16 in); both rings R 100 to 130
  (OD 260, ID 200), 3.35 inside the backplate rim and 36.5 outside the hub. 4x #4 x 3/8 pan-head screws on R 105.5 at
  45/135/225/315 into D 2.2 x 8.0 blind pilots (6.9 into the MDF, tip 5.8 behind the front face). Stack 4.2 deep (4.7 at a
  screw head) in the 25.4 gap; strip face 21.2 from the wall.
- Backplate 12 in (rev C): D 266.7 [10.50] x 12.7 [0.50]; insert bore 9.92 [25/64] through; plain rim, NO rabbet, NO rim notch;
  rear channel 6 x 4 from R 60 to R 97 at 6 o'clock; 4 blind pilots as above. Backplate 7 in (rev B): D 152.4 [6.00]; rim
  rabbet 10.2 wide x 1.5 deep centred on the rim (8 mm COB strip sits 0.1 proud); lead notch 6.35 at 6 o'clock; rear channel
  6 x 4 from the notch to R 60. Both: rear jack
  pocket 16 x 13 x 6.5 at (0, +15); felt targets D 13.3 x 0.5 on R 120 and R 69.85 at 90/210/330 deg (all six are in the STEP;
  rev A's STEP had only three); scored witness circle D 32.4 for the centre backing ring; 3x #8 countersinks on R 45 at
  90/210/330 (front face, hidden by the record). Record seat plane 1.1 above the front face.
- Hub: D 127 x 25.4; rear recess D 107 x 5.5; J-slots on R 33 (entry D 10.8 at stud angle MINUS 20 deg, slot 4.8, nut pocket
  11.5 wide to z 19: locks clockwise seen from the room); rear cable pocket 27 wide, y -13.5..+22, 12 deep; pigtail hole
  D 6.5 at (0, +15) through a 3.1 web; P-clip pilot D 2.4 at (-9.5, +4); splice cavity 14 x 13 open to the front; front
  centre relief D 14 x 9.1; cord channel 9.5 x 12 (rear, 6 o'clock); lead channel 6 x 4 (front, 6 o'clock); M3 heat-set
  insert at 250 deg, z 9.5; 3x D 3.2 x 14 pilots on R 45.
- Wall plate: D 101.6 [4.00] x 1.90 [14 ga]; centre slot 30 x 37 (y -15..+22); arc slots 4.8 wide +/-10 deg on D 83.3
  (90/270) and D 88.9 (0/180); PEM holes D 4.22 on R 33 at 75/195/315; tab 8 wide, 12.0 tall, D 3.4 hole at z 9.5,
  bend Ri 1.9, K 0.44, BA 4.30, flat tab length 12.50 from the plate edge.
- Caps: RS-CAP-12 rev D D 38.1 [1.50], 10.0 tall (1.6 band + 8.4 sphere segment R 25.8), base R 0.8, underside recess D 33 x 1.00 +/-0.05,
  smooth shoulder D 7.10 x 2.0, stud 1/4-20 x 11.95 +/-0.05 with a D 4.80 +0/-0.10 x 1.5 dog point; RS-CAP-7 rev C D 48.0 [1.89],
  8.5 tall (2.0 band + 6.5 dome R 47.6), boss D 37.6 x 1.6, stud 12.6. All cap stud TIPS land at the same depth (asserted).
- Stud engagement in the 12.7 insert: 8.27 mm (12 in, 6.77 threaded past the dog point) / 8.25 mm (7 in). Never proud of the back face.

## Checks that ran (see checks.md)

- Pairwise boolean interference of every solid in each of the four plain assemblies and three lit ones: 0 hits (the heat ring,
  cork ring, back-face strip and their 4 screws are in the 12 in MDF and all three lit assemblies).
- Derived clearances, point-in-solid probes and a tolerance stack, all listed in checks.md; the regression gates at the top of that file must all pass.
- Every solid is a single valid closed solid (asserted in build_all.py). Volumes in build-log.json
  (hub about 249 cm3 solid, about 100 g at 40% infill in PETG; brass cap 12 rev D: 54.8 g; cap 7 rev C: 99.5 g).

## Design calls made here (not in the reports; flag if you disagree)

1. Bayonet head = PEM FH-832-10 self-clinching stud (8-32 x 5/8) + 8-32 nylon-insert lock nut set at a 7.2 mm gauge. The mounting
   report said "8-32 shoulder screws"; a shoulder screw needs a tapped plate (14 ga is too thin to tap 8-32 reliably), so a
   pressed stud + lock nut gives the same geometry with off-the-shelf parts and an adjustable preload.
2. Set screw sits at the 250 deg position (about 6:40) instead of exactly 6 o'clock, because the 6 o'clock position carries the
   surface-cord channel. The set screw lands in a hole in a bent-up tab on the plate, which locks rotation and lift in both
   directions; a radial screw bearing on a flat plate edge only blocks one direction.
3. Rev B: there is no DC jack in the hub. A wall-facing jack 7.5 mm off the wall cannot take a straight plug on a surface
   install. Power enters on a 150 mm pigtail with an inline jack, P-clipped in the rear pocket; the pass-through stays offset
   15 mm toward 12 o'clock to keep clear of the cap stud axis. The plate keeps its 30 x 37 slot; the wall hole for the in-wall
   route is 1 in on the plate centre (the inline jack is 11.5 mm). The 6.5 mm rear pocket in the backplate now sits over the
   splice.
4. Cap studs are 11.95 (12 in) and 12.6 (7 in), not 1 in (engineering report) or 5/8 in (rev A): they never protrude behind
   the backplate and they put their tips where the lit sconce's centre contact expects them. Engagement is 8.3 mm.
5. Hub fastens to the backplate with 3x #8 x 1 in flat-head screws from the FRONT of the backplate (hidden by the record) rather
   than glue alone, so a hub can be swapped. Glue is still fine as a second line.
6. The 7 in cap carries a D 37.6 x 1.6 boss that centres it in the 1.5 in hole, replacing the plastic 45 adapter for the 7 in SKU
   (the plastic adapter is still shipped for a 7 in on a 12 in backplate). It needs a 47 x 39 x 1.6 felt ring (custom die-cut).
7. Thin aluminum backplates (3 / 5 mm) cannot take a rim rabbet or a 12.7 mm insert, so they are modelled as the engineering
   report's FLOATING configuration: 1/4-20 flat head countersunk from the back (5 mm) or pan head in the hub relief (3 mm) into
   the 3/8 in x 1 in F-F standoff on the front; LED is a 6 x 12 mm top-emitting COB neon-flex ring on the back face (it bends
   in-plane, a flat COB strip does not). Different look (double halo), own BOM line. The 1/2 in CNC MDF path is the primary.
8. Hub recess is a uniform 5.5 deep so any pan-head wall screw or box screw clears; J-slot web 3.0 thick.

## Standard dimensions used, with sources

- LP spindle hole 0.286 in (7.26 mm); 45 rpm hole 1.5 in: engineering-report.md sec. 1
  (https://allforturntables.com/2023/07/28/vinyl-record-spindle-hole/,
  https://www.audio-technica.com/en-us/support/audio-solutions-question-of-the-week-what-do-i-need-to-know-about-45-rpm-records).
- E-Z Lok 400-4: 1/4-20, 0.500 in long, 25/64 in drill: https://www.albanycountyfasteners.com/1-4-20-brass-thread-inserts-wood-400-4-p/117012.htm
  and https://www.ezlok.com/assets/documents/EZ-LOKBrochure_2023.pdf.
- Box spacings 83.3 mm (single gang) and 88.9 mm (round / octagon): mounting-report.md sec. 1 (verify against the specific LV bracket).
- 14 ga steel = 0.0747 in (1.897 mm): US standard sheet gauge for steel; SendCutSend lists 0.075 in mild steel
  (https://sendcutsend.com/materials/processing-min-max/). Bend radius 1t and K 0.44 are typical CRS values; the vendor will apply
  its own K, which is why the formed STEP is the master and the DXF is marked as derived.
- PEM FH self-clinching studs: 8-32, lengths in 1/16 in steps, clinch hole about 0.166 in for 0.060 in+ sheet
  (PEM bulletin FH, https://www.pemnet.com). Marked "verify" in the RFQ: the exact hole for 0.075 in sheet must be read off the bulletin.
- 8-32 nylon-insert lock nut 11/32 in across flats (ASME B18.16.6 / common catalogue), height about 0.23 in: envelope only.
- 1/4-20 pan head 0.492 dia x 0.133 high; 1/4 flat head 0.507 dia, 82 deg (ASME B18.6.3): envelopes for clearance only.
- 3/8 in OD x 1 in 1/4-20 F-F aluminum standoff: https://www.aluminumspacers.com/as38-1420-64 (engineering-report sec. 1).
- Felt: pads 1/2 in x 1/4 in x 1/16 in are Durofelt SAW12BK (https://www.durofelt.com/categories/self-adhesive-felt-washers). The cap felt and the
  centre backing ring are 1-1/4 x 3/8 x 1/16 in, which Durofelt does NOT stock (page checked 2026-11-11): die-cut.
- Power pigtail: inline female 5.5 x 2.1 jack modelled as D 11.5 x 28, plug body D 10.5 x 22: generic envelopes, estimates;
  confirm against the pigtail actually bought.
- COB strip 8 mm wide x about 1.6 thick: engineering-report sec. 2 (HitLights / Ecolocity class), estimate for thickness.
- Halo gap 1 in: engineering-report sec. 1 and 2 (sign-industry halo-letter guidance). That report put the LED on the rim facing
  outward; the 12 in sconce no longer does (heat-safe layout, 2026-11-11). The 7 in still does.
- #4 x 3/8 Type AB pan-head screw: major 2.9, root 2.1, head D 5.6 x 2.1 (ASME B18.6.3 class envelope, from memory, not
  looked up against a vendor sheet): confirm against the screws actually bought.
- Plating spec ASTM B456 SC2 (copper + bright nickel + decorative chrome) is the normal interior decorative chrome callout;
  PVD and black-chrome alternatives are listed in the RFQ for the plater to choose.

## Open questions

1. Confirm the pigtail actually purchased (inline jack diameter and length) and re-run `build_all.py` with `INLINE_JACK`
   adjusted. Measure how far the felt backing ring compresses under the cap and set `CENTER_RING_SET` (0.5 assumed).
2. PEM FH-832 clinch hole for 0.075 in sheet: read it off bulletin FH and set `STUD_HOLE_D` before cutting.
3. 7 in SKU felt ring 47 x 39 x 1.6 is not a stock Durofelt size: die-cut quote or use three 1/2 in pads on the cap underside.
4. Aluminum variant is a different product (floating record, neon-flex ring, double halo). Keep as an upsell or drop; the
   decision changes which RFQ goes out.
5. MDF jack pocket leaves 6.2 mm of MDF under the pocket; fine for MDF, check tear-out in birch ply.
6. Hub as printed is 25.4 tall with 5.8 of material above the DC pocket; for injection moulding the designer should add drafts,
   core out the solid ring between R 54 and R 63 and gate at the rim. The RFQ asks the print vendor for this DFM review.
7. Thermal. DECIDED 2026-11-11 for the 12 in MDF sconce (plain and lit): the halo strip is on the BACK face on the aluminium
   ring + cork ring (`THERMAL.md`, `FIXES-heat-layout.md`). Calculated record temperature: 33.1 C in a 30 C room with a 4 W
   strip; 45.2 C in the stacked worst case (wrong 6 W strip, still air, 35 C room). Strip spec: the 4 W class (low-power 2835
   60/m at 1.46 W/ft is about 3.4 W on the 700 mm this layout uses). 6 W stays the absolute cap and is only the wrong-part case;
   the 2026-11-10 review's warning that a back-face strip in the 1 in cavity should be held to 4 W is honoured by that spec.
   NOT the 10-12 W/m COB class. STILL OPEN: nothing is measured. Acceptance on the first sample: 2 h soak, still room, record
   back at R 114, record top edge and (lit) under the cap no more than 5 K above the room; strip surface <= 55 C.
   STILL OPEN: the 7 in sconce keeps the rim strip under a 12.7 mm record overhang (no room for the ring outside the hub) and
   the aluminium-backplate variants are not modelled.
8. Cosmetic threads: STEP studs and bores are plain cylinders at major / drill diameter (standard for shop quotes); the 2D sheets
   carry the thread callouts.
