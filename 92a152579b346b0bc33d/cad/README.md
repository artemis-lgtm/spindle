# Record Sconce: manufacturer-ready CAD

Built 2026-11-09 (overnight brief). Parametric CadQuery 2.8 source, STEP as the master format, with STL for printed parts,
DXF for flat parts, 2D drawings (PDF + PNG) and per-vendor RFQ packets. Nothing has been sent or ordered; the RFQ text is
drafted to files only. All decisions follow ../NOTES.md, ../engineering-report.md, ../mounting-report.md and
../design-report.md; where the CAD had to add a detail the reports did not fix, it is listed under "Design calls made here".

## Folder map

| Path | What |
|---|---|
| `sconce_cad.py` | every part as a function of named parameters (mm). Edit here, never the STEP. |
| `assembly.py` | placement of all solids, boolean interference check, derived clearance numbers |
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
| RS-BP-12-MDF | Backplate 12 in record, D 266.7 x 12.7 | 1 | CNC router, 1/2 in MDF or Baltic birch, painted matte black | step, stl, dxf, drawing |
| RS-BP-7-MDF | Backplate 7 in record, D 152.4 x 12.7 | 1 (7 in SKU) | same | step, stl, dxf, drawing |
| RS-BP-12-AL5 / -AL3 | Backplate 12 in, flat aluminum 5 mm / 3 mm (floating-record configuration) | alt | laser/waterjet 5052, powder coat | step, dxf, drawing |
| RS-BP-7-AL5 | Backplate 7 in, flat aluminum 5 mm | alt | same | step, dxf, drawing |
| RS-HUB-01 | Hub, D 127 x 25.4, twist-lock, DC jack carrier | 1 | FDM PETG/ASA now, injection mould later | step, stl, drawing |
| RS-WP-01 | Wall mounting plate, D 101.6, 14 ga steel, one bent tab, 3 PEM studs | 1 | laser + bend + PEM, zinc | step, flat dxf, drawing |
| RS-CAP-12 | Dome cap D 38.1 x 10.0, integral 1/4-20 x 5/8 stud | 1 | turned brass C360, polished, plated (-CR / -BR / -BK) | step, stl, drawing |
| RS-CAP-7 | Dome cap D 48.0 x 8.5 with D 37.6 locating boss (chromed 45-adapter form) | 1 (7 in SKU) | same | step, stl, drawing |

Purchased parts modelled for fit (envelopes, not vendor CAD): E-Z Lok 400-4 insert, 8 mm COB LED strip, 1/2 in felt pads,
1 in felt washer, PEM FH-832-10 studs, 8-32 nylon lock nuts, #8 pan-head wall screws, panel-mount 5.5 x 2.1 DC jack and
plug, M3 x 12 set screw, 3/8 in x 1 in 1/4-20 standoff and 1/4-20 flat/pan head (aluminum variant), 6 x 12 neon-flex ring
(aluminum variant), the customer's 12 in / 7 in record.

## Key dimensions (mm, inches in brackets)

- Wall gap (hub thickness) 25.4 [1.00]; record overhang past the backplate 19.05 (12 in) / 12.7 (7 in).
- Backplate: D 266.7 [10.50] / 152.4 [6.00] x 12.7 [0.50]; insert bore 9.92 [25/64] through; rim rabbet 10.2 wide x 1.5 deep
  centred on the rim (8 mm COB strip sits 0.1 proud); lead notch 6.35 at 6 o'clock; rear channel 6 x 4 to R 60; rear jack
  pocket 16 x 13 x 6.5 at (0, +15); felt targets D 13.3 x 0.5 on R 127 and R 69.85 at 90/210/330 deg; 3x #8 countersinks
  on R 45 at 90/210/330 (front face, hidden by the record).
- Hub: D 127 x 25.4; rear recess D 107 x 5.5; J-slots on R 33 (entry D 10.8, slot 4.8, 20 deg lock arc, nut pocket 11.5 wide
  to z 19); DC pocket 27 wide, y -13.5..+28.5, 16.5 deep; jack hole D 8.0 at (0, +15) through a 3.1 web; jack-body cavity
  14 x 13 open to the front; cord channel 9.5 x 12 (rear, 6 o'clock); lead channel 6 x 4 (front, 6 o'clock); M3 heat-set
  insert at 250 deg, z 9.5; 3x D 3.2 x 14 pilots on R 45.
- Wall plate: D 101.6 [4.00] x 1.90 [14 ga]; centre slot 30 x 37 (y -15..+22); arc slots 4.8 wide +/-10 deg on D 83.3
  (90/270) and D 88.9 (0/180); PEM holes D 4.22 on R 33 at 75/195/315; tab 8 wide, 12.0 tall, D 3.4 hole at z 9.5,
  bend Ri 1.9, K 0.44, BA 4.30, flat tab length 12.50 from the plate edge.
- Caps: RS-CAP-12 D 38.1 [1.50], 10.0 tall (1.6 band + 8.4 sphere segment R 25.8), base R 0.8, stud 1/4-20 x 15.9 [5/8];
  RS-CAP-7 D 48.0 [1.89], 8.5 tall (2.0 band + 6.5 dome R 47.6), boss D 37.6 x 1.6, same stud.
- Stud engagement in the 12.7 insert: 9.0 mm (12 in, with 3.2 felt washer) / 10.8 mm (7 in). Never proud of the back face.

## Checks that ran (see checks.md)

- Pairwise boolean interference of all 20 solids in each of the four assemblies: 0 hits.
- 30 derived clearances (wall-screw head under the recess, nut and stud under the pocket ceiling, set-screw reach, plug through
  the plate slot and a 1-1/4 in wall hole, thread engagement, jack body vs insert bore, hub screw pilot depth).
- Every solid is a single valid closed solid (asserted in build_all.py). Volumes in build-log.json
  (hub 245 cm3 solid, about 100 g at 40% infill in PETG; brass cap 12 = 7.4 cm3 = 63 g; cap 7 = 11.8 cm3 = 100 g).

## Design calls made here (not in the reports; flag if you disagree)

1. Bayonet head = PEM FH-832-10 self-clinching stud (8-32 x 5/8) + 8-32 nylon-insert lock nut set at a 7.2 mm gauge. The mounting
   report said "8-32 shoulder screws"; a shoulder screw needs a tapped plate (14 ga is too thin to tap 8-32 reliably), so a
   pressed stud + lock nut gives the same geometry with off-the-shelf parts and an adjustable preload.
2. Set screw sits at the 250 deg position (about 6:40) instead of exactly 6 o'clock, because the 6 o'clock position carries the
   surface-cord channel. The set screw lands in a hole in a bent-up tab on the plate, which locks rotation and lift in both
   directions; a radial screw bearing on a flat plate edge only blocks one direction.
3. DC jack axis is offset 15 mm toward 12 o'clock so the jack body never shares the axis with the cap stud and the insert; the
   plate centre hole is therefore a 30 x 37 slot and the customer's wall hole is 1-1/4 in centred 6 mm above the plate centre.
   The jack body (10 mm long) also needs a 6.5 mm rear pocket in the backplate (hidden by the record) because the hub's
   25.4 mm cannot hold pocket + web + body.
4. Cap stud is 5/8 in, not 1 in (engineering report), so it never protrudes behind the backplate (which would hit the jack).
   Engagement stays at 7 to 8 threads for a 160 g record.
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
- Felt washer 1 in OD x 3/8 in ID x 1/8 in, pads 1/2 in x 1/16 in: https://www.durofelt.com/categories/self-adhesive-felt-washers.
- Panel-mount 5.5 x 2.1 DC jack with 8 mm threaded barrel (DC-022B class) and plug body about 10 mm dia: generic envelope, estimate;
  confirm against the jack actually bought before the hub is tooled.
- COB strip 8 mm wide x about 1.6 thick: engineering-report sec. 2 (HitLights / Ecolocity class), estimate for thickness.
- Halo gap 1 in, LED on the rim facing outward: engineering-report sec. 1 and 2 (sign-industry halo-letter guidance).
- Plating spec ASTM B456 SC2 (copper + bright nickel + decorative chrome) is the normal interior decorative chrome callout;
  PVD and black-chrome alternatives are listed in the RFQ for the plater to choose.

## Open questions

1. Confirm the DC jack and plug actually purchased (barrel length, body size, plug body diameter) and re-run `build_all.py`
   with `JACK_BARREL_L`, `JACK_BODY_L`, `POCKET_W` adjusted. The hub and plate geometry depend on it.
2. PEM FH-832 clinch hole for 0.075 in sheet: read it off bulletin FH and set `STUD_HOLE_D` before cutting.
3. 7 in SKU felt ring 47 x 39 x 1.6 is not a stock Durofelt size: die-cut quote or use three 1/2 in pads on the cap underside.
4. Aluminum variant is a different product (floating record, neon-flex ring, double halo). Keep as an upsell or drop; the
   decision changes which RFQ goes out.
5. MDF jack pocket leaves 6.2 mm of MDF under the pocket; fine for MDF, check tear-out in birch ply.
6. Hub as printed is 25.4 tall with 5.8 of material above the DC pocket; for injection moulding the designer should add drafts,
   core out the solid ring between R 54 and R 63 and gate at the rim. The RFQ asks the print vendor for this DFM review.
7. Thermal: unchanged from the engineering report (strip on the rim, 0.7 in from the record edge). The first sample still needs
   the 2-hour IR soak before a page claim.
8. Cosmetic threads: STEP studs and bores are plain cylinders at major / drill diameter (standard for shop quotes); the 2D sheets
   carry the thread callouts.
