# Heat-safe halo layout made canonical (2026-11-11)

Austin's instruction: "the heat safe spec needs to be the same for the light version and the cap without the light version". This file records what was changed to do that, every file touched, every number that moved, how each claim was checked, and what is not done.

Applied 2026-11-11 by claude-fable-5-2. Nothing was sent, ordered, published, pushed or committed.

## In one paragraph

On the 12 in MDF sconce the LED strip used to sit in a rabbet on the RIM of the backplate. The record is wider than the backplate, so its outer 19 mm hung 3.45 mm in front of that strip with only air between. The strip now sits on the BACK of the backplate, facing the wall, stuck to a 1 mm aluminium ring that spreads its heat, with a 1.6 mm (1/16 in) cork ring between the aluminium and the wood. The LEDs cannot see the record. There is ONE halo stack in the CAD, and both the plain-cap sconce and the lit-cap sconce use it (`assembly_lit.py` builds on `assembly.py`; a gate checks the seven halo solids are identical in both).

## Build result (run in this session)

`cad/.venv/bin/python build_all.py` ends with:

```
gates: 199 pass, 0 FAIL
```

That is the 105 gates from the Fable 5.2 review plus 94 new ones: 69 tagged HEAT or HEAT-7 and 25 new document checks. All are listed with their values at the top of `checks.md`.

Interference (pairwise boolean intersection of every solid, anything over 0.5 mm3 is a hit):

| Assembly | Solids | Hits |
|---|---|---|
| 12 in MDF, plain cap | 30 | none |
| 7 in MDF | 24 | none |
| 12 in aluminium 5 mm | 23 | none |
| 12 in aluminium 3 mm | 23 | none |
| 12 in MDF, lit cap, nominal record | 42 | none |
| 12 in MDF, lit cap, thin record | 42 | none |
| 12 in MDF, lit cap, thick record | 42 | none |

Negative control: an aluminium ring with no screw holes, put in the same place, IS reported as an interference with the screw. So "none" is a live result, not a blind one.

## The layout, final dimensions

Stack on the backplate back face, going toward the wall:

| Layer | Part | Thickness | From the centre |
|---|---|---|---|
| Cork ring | RS-CK-12 rev A (new) | 1.6 mm (1/16 in) | r 100 to 130 (OD 260, ID 200) |
| Aluminium ring | RS-HR-12 rev A (new), 5052-H32, 0.040 in | 1.0 mm | r 100 to 130 (OD 260, ID 200) |
| LED strip, 8 mm wide | purchased | 1.6 mm (estimate) | r 111 to 119, centred on r 115, LEDs toward the wall |

- Rings stop 3.35 mm inside the backplate rim (r 133.35) and 36.5 mm outside the hub (r 63.5).
- Stack depth 4.2 mm at the strip, 4.7 mm at a screw head, inside the 25.4 mm gap. Strip face 21.2 mm from the wall.
- The strip is 14.35 mm inside the backplate rim, behind the wood. 15.3 mm of aluminium, cork and MDF sit between the strip and the record.

### How it is fastened (decision made here)

- The cork is laid on the ALUMINIUM on the bench (stuck to it if the cork bought has an adhesive face; plain cork is accepted), so cork + aluminium + strip become one sub-assembly. No adhesive is asked to hold on painted MDF.
- Four #4 x 3/8 in pan-head screws (the same screw as the hub's P-clip screw) go through the aluminium (D 3.3 holes) and the cork (D 4.0 holes) into four blind D 2.2 x 8.0 pilots in the back of the backplate, on r 105.5 at 45, 135, 225 and 315 degrees. The ring can come off for service.
- The screws go 6.9 mm into the 12.7 mm MDF. The tips stop 5.8 mm behind the front face and the pilot bottoms 4.7 mm behind it (1.1 mm of pilot is left past the screw tip), so nothing can show on the record side. Nearest felt-pad target is 24.7 mm away in plan, the lead channel 70 mm, the hub edge 39 mm, the nearest hub screw 57 mm, the insert 99 mm.
- Screw heads (D 5.6) sit in the 11 mm band between the ring's inner edge and the strip: 2.7 mm from the strip, hole edge 3.85 mm from the ring's inner edge.

### Lead routing

- The strip's joint and its two leads are at 6 o'clock. The leads run inward over the aluminium, drop over the ring's inner edge at r 100, enter the back channel in the backplate at r 97 and follow it to r 60, where the hub's existing front channel takes them to the splice cavity. The hub is unchanged.
- The backplate's back channel is shortened to r 60 to 97 (it used to run from a notch in the rim). It stops 3 mm short of the cork so the cork sits on unbroken wood.
- The solder joints and the leads get heat-shrink where they cross the ring's inner edge: the ring is bare metal and the strip is 12 V. This is a note on the RS-HR-12 drawing. The leads themselves are not modelled as solids (they were not before either).

### Rim rabbet and rim notch: removed

Both are deleted from the 12 in MDF backplate. I looked for a reason to keep them and found none: nothing sits in the rabbet any more, and the notch only existed to bring the leads off the rim. Removing them also makes the 12 in part a plain two-sided routing job with no rim pass. The 12 in backplate is now **RS-BP-12-MDF rev C**.

## 7 in sconce: STOPPED, left unchanged

The 7 in backplate (D 152.4, r 76.2) was NOT moved to this layout. Numbers:

- Ring outer edge at the same 3.35 mm rim margin: r 72.85.
- Hub edge: r 63.5 (the same 127 mm hub).
- Back face available outside the hub: 72.85 minus 63.5 = **9.35 mm**.
- With 1 mm of clearance to the hub that is an **8.35 mm** ring for an **8 mm** strip: 0.17 mm to spare each side, and no room at all for a 5.6 mm screw head or the leads.

A ring can be drawn there but it cannot be built, so the variant is left exactly as it was: rim rabbet, rim strip, RS-BP-7-MDF rev B. Two gates hold it still (its rim rabbet is still in the solid; its volume equals the rev B volume to 0.1 mm3). Its drawing, RFQ text, BOM lines and assembly sheet now say in words that it is not on the heat-safe layout. The 7 in record overhangs its backplate by 12.7 mm, so the original problem still exists there. Ways out, none chosen: a 5 mm strip, a smaller hub for the 7 in, or a smaller margin to the rim.

## Aluminium-backplate variants: not covered

RS-BP-12-AL5, -AL3 and RS-BP-7-AL5 (floating record, neon flex ring on the back) are untouched. They are not covered by this layout and are not in the heat model. Their assembly sheet says so.

## Numbers that moved

| What | Before | After |
|---|---|---|
| RS-BP-12-MDF revision | B | C |
| 12 in backplate rim | rabbet 10.2 x 1.5, notch 6.35 at 6 o'clock | plain square edge |
| 12 in backplate back channel | rim notch to r 60 | r 60 to r 97 |
| 12 in backplate back face | no pilots | 4 blind pilots D 2.2 x 8.0 on r 105.5 |
| 12 in backplate volume | 691,542 mm3 | 704,991 mm3 |
| LED strip, 12 in | on the rim at r 133.4, facing out, z 27.75 to 35.75 from the wall | on the back at r 111 to 119, facing the wall, z 21.2 to 22.8 |
| Strip length, 12 in | about 838 mm round the rim | 723 mm round at r 115 (about 700 mm cut) |
| New parts | none | RS-HR-12 rev A, RS-CK-12 rev A, 4 screws |
| Solids in the 12 in MDF assembly | 24 | 30 |
| Solids in the lit assembly | 36 | 42 |
| Assembly sheet RS-ASM-12-MDF | rev A | rev B |
| Assembly sheet RS-ASM-12L | rev B | rev B.1 (lit cap parts stay rev B) |
| Outer felt target to the rim | 5.2 mm to the rabbet floor | 6.7 mm to the rim |
| Record, normal case (4 W, 30 C room) | 34.9 C | 33.1 C |
| Record, stacked worst case (6 W, still air, 35 C room) | 49.6 C | 45.2 C |
| Gates | 105 | 198 |
| 12 in parts total at 100 (build/BOM.md, BOM.csv, cost-model.py) | $38.07 | $47.46 (adds $7.38 aluminium ring + $1.89 cork ring + $0.12 screws) |
| 12 in parts total for one unit | $62.79 | $91.98 |
| $89 Kit, contribution before ads at 100 (cost-model.py) | $25.07 | $15.68 |
| Cork ring thickness, first pass of this change vs final | 2.0 mm | 1.6 mm (1/16 in), by ruling after the live quotes |

Numbers that did NOT move, measured on the rebuilt assemblies and gated:

| From the wall | Before | After |
|---|---|---|
| Record front face | 41.23 mm | 41.23 mm |
| Plain cap tip (furthest point of the plain sconce) | 51.78 mm | 51.78 mm |
| Lit cap tip (furthest point of the lit sconce) | 56.48 mm | 56.48 mm |
| RS-BP-7-MDF volume | 220,801.9 mm3 | 220,801.9 mm3 |

## Thermal model on the final geometry

`thermal.py` now carries the final geometry as config F and reads it from `sconce_cad.py`. `build_all.py` re-runs it every build. Full table and caveats: `THERMAL.md`.

| Case | Strip | Record hottest spot | Where |
|---|---|---|---|
| Normal: 4 W strip, 30 C (86 F) room | 39.2 C (+9.2 K) | 33.1 C (+3.1 K), 92 F | r 114 mm |
| Stacked worst: 6 W strip, film coefficients halved, 35 C (95 F) room | 56.2 C (+21.2 K) | 45.2 C (+10.2 K), 113 F | r 114 mm |

Cork thickness, same geometry otherwise: 2.0 mm gives 33.04 / 44.92 C, 1.6 mm gives 33.14 / 45.16 C, 1.5 mm gives 33.17 / 45.22 C, no cork 33.55 / 45.98 C. The table is in `THERMAL.md`. The model's grid through the thickness was refined from 0.25 mm to 0.1 mm so it can tell 1.6 from 1.5; a few older rows moved by 0.1 (old rim strip worst case 49.7 became 49.6).

Vinyl softens at about 55 to 60 C. Lit cap: it adds 0.17 W at the centre; `label-light/DESIGN.md` section 4 estimates the cap's own rise at about 11 K worst case, 5 to 7 K expected, and the halo adds 0.02 K (normal) to 0.30 K (worst) under the cap, so the two do not stack. The cap is not in the heat model.

## What was verified, and how

| Claim | How it was checked in this session |
|---|---|
| Nothing overlaps | `interference_report` on all 7 assemblies, 0 hits; negative control passes |
| Ring clear of the hub, studs, power connector and plug | minimum distance between the placed solids (OCCT): hub 36.5, studs 65.1, inline jack 9.35, plug and cable 8.25 mm |
| Rabbet and notch are really gone from the 12 in solid | point-in-solid probes on the solid that becomes the STEP |
| Four pilots exist, are blind, and the front face is whole above them | point-in-solid probes |
| Ring OD, ID, thickness, four holes | bounding box and probes on both ring solids |
| Plain and lit carry the same halo | the 7 halo solids compared by bounding box and volume across both assemblies |
| Projection unchanged | bounding boxes of the rebuilt assemblies against the values measured before any edit |
| 7 in backplate unchanged | volume against the pre-change volume; rabbet probe |
| Heat numbers belong to this geometry | build re-runs the model; gate compares the model's geometry with the CAD and checks `THERMAL.md` quotes the same four temperatures |
| Side cut in the heat-safe drawing is true | every bar is computed from `sconce_cad.py`; compared against the assembly's bounding boxes for hub, backplate, cork, aluminium, strip, record, washer, centre ring, insert, cap, screw (all matched) |
| Drawings and labels are readable | every changed sheet and all three exploded drawings were opened and looked at; overlapping labels were moved |
| Stale text cannot come back | 14 new STALE patterns and 11 new REQUIRED patterns in `gates.py` (including: no 2 mm cork, no unpriced rings, BOM.md total $47.46, BOM.csv total matching it, ring price $7.38 from the canonical file) |

## Files touched

Source (hand edits):
- `cad/sconce_cad.py`: halo constants, `halo_layout()`, `backplate()` rev C branch, `heat_ring()`, `cork_ring()`, `led_strip_back()`, `halo_screw()`; `led_strip()` renamed `led_strip_rim()` (7 in only).
- `cad/assembly.py`: halo parts in `build()`, `halo_numbers()`.
- `cad/assembly_lit.py`: NOT edited. It inherits the halo from `assembly.build()`, which is the point.
- `cad/gates.py`: `halo_probes()`, the HEAT gates, new document patterns.
- `cad/thermal.py`: named cases (normal, worst), config F from the CAD, record temperature under the cap.
- `cad/build_all.py`: two new parts, their DXF, sheets and RFQ packets, per-part backplate revisions, `thermal_numbers()`, `checks.md` text.
- `cad/drawings.py`: backplate sheet (rev C branch), `draw_halo_ring()`, `halo_detail()`, assembly sheet with wall line and projection dimensions.
- `cad/drawings_lit.py`: halo detail and notes on RS-ASM-12L.
- `cad/dxf_out.py`: `halo_ring_dxf()`, backplate DXF notes.
- `cad/explode_view.py`, `cad/explode_lit.py`, `cad/explode_fix.py`: all three draw the halo from the canonical parts. `explode_fix.py` no longer injects fake rings; its side cut is computed from the parameters.
- `cad/preview.py`, `cad/blender_preview.py`: cork colour (and the missing P-clip colour that had broken the Cycles preview script since rev B).

Text (hand edits):
- `cad/THERMAL.md` (rewritten for the final numbers), `cad/README.md`, `cad/FIXES-fable52.md` (one update line), `cad/label-light/DESIGN.md`, this file.
- `build/BOM.md` (line 1, line 8, new lines 8a and 8b with live prices, 8c estimated, the 12 in total, the Set total, 7 in lines, section 4b). `build/cost-model.py` (three new lines), with `cost-model.csv` and `BOM.csv` regenerated from it. `sourcing/quotes-2026-11-11/README.md` (aluminium table replaced by the quote of the canonical file). Banners only on `build/assembly-SOP.md`, `build/QC-test-plan.md`, `build/sample-kit-shopping-list.md`, `build/cost-model.md`, `build/README.md`.
- `renders-final/README.md` (halo flag closed, phantom-post flag stays open).
- `site/_gen/pages.py` and the four pages it regenerates (`index.html`, `faq.html`, `product.html`, `install.html`).
- `START-HERE.html`, `PARTS-SIMPLE.html` (two sentences), `NOTES.md`.
- `marketing/ad-copy-bank.md` (2 lines), `marketing/ad-concepts.md` (1 line), `marketing/email-sms-flows.md` (1 line): "light on the rim" became "light on the back of the plate".
- Banners on `engineering-report.md`, `sourcing/sample-run-plan.md`, `sourcing/vendors.md` and the two unsent backplate RFQ drafts in `sourcing/rfq-drafts/` (they ask for the rim rabbet).

Regenerated by `build_all.py`:
- `cad/parts/`: every STEP / STL / DXF, including new `RS-HR-12.step`, `RS-HR-12.dxf`, `RS-CK-12.step`, `RS-CK-12.dxf` and the rev C `RS-BP-12-MDF.*`.
- `cad/assemblies/`: all five STEP assemblies.
- `cad/drawings/`: 21 sheets, including new `RS-HR-12` and `RS-CK-12`, and changed `RS-BP-12-MDF` (rev C), `RS-BP-7-MDF` (new note), `RS-ASM-12-MDF` (rev B), `RS-ASM-12L` (rev B.1), `RS-ASM-7-MDF`, `RS-ASM-12-AL5`.
- `cad/previews/`: all part and assembly previews, DXF previews for both rings.
- `cad/checks.md`, `cad/checks.json`, `cad/build-log.json`, `cad/thermal-results.json`.
- `cad/rfq/`: new `heat-ring-aluminum/` and `cork-ring/` (STEP, DXF, drawing, SPEC.txt), updated `backplate-mdf-cnc/`, `README.md`, both cap zips, `label-light/` copies.

Regenerated by hand-run scripts:
- `renders-exploded/spindle-exploded-labelled.png`, `spindle-lit-exploded-labelled.png`, `spindle-heat-safe-layout.png` and their six raw renders.
- `cad/previews/*_cycles.png` (five Cycles previews; they dated from 2026-11-09).
- Every `.md` to its sibling `.html` (`_publish/md2html.py`).

Moved to superseded:
- `cad/rfq/SUPERSEDED-do-not-quote/SUPERSEDED-backplate-RS-BP-12-MDF-revB/`: the rev B backplate packet (STEP, STL, DXF, drawing, SPEC) and the two assembly sheets that showed the rim strip.

## Not done, or not verifiable here

1. **No physical test exists.** Every temperature is a calculation. Nothing has been built. First prototype: thermocouple on the record's back at r 114 mm, at the top edge and under the cap, two hours on, still room.
2. **7 in sconce is not on the layout** (see above). It still has the original overhang problem.
3. **Aluminium-backplate variants are not covered** and not modelled.
4. **Cork thickness: settled at 1.6 mm (1/16 in)** by ruling the same evening, because 2 mm sheet is not stocked. The CAD constant, stack, gates, heat model, drawings, RFQ, BOM and legends all say 1.6. Still open on the cork: the quote notes do not say whether the WidgetCo roll has an adhesive face (the drawing prefers one and accepts plain cork), the in-house cutting tool is not picked, cutting labour is not in the $1.89, and the ring needs its 4 holes punched.
5. **Prices.** The aluminium ring is now a real quote of the canonical `cad/parts/RS-HR-12.dxf` with its four holes: $7.38 at 100, $27.10 for one (the first quote, of a ring without holes, was $7.19). The BOM's Qty 20 and Qty 500 columns for that ring reuse the 10-piece and 100-piece prices. The screws are an estimate. The cork price has no cutting labour in it. `cost-model.py`, `cost-model.csv` and `BOM.csv` contain all three lines; the tables written out in `build/cost-model.md` do NOT and are bannered as out of date. The Set parts row in `BOM.md` was already inconsistent with `cost-model.py` at 1, 20 and 500 before this change; it now prints what the script computes and says so. `PARTS-SIMPLE.html` (not mine to edit) still shows $7.19 and "about $47".
6. **Screw details are from memory, not a vendor sheet:** #4 Type AB major 2.9, root 2.1, pan head 5.6 x 2.1. The 2.2 mm pilot in MDF is a judgement; confirm on the first part that the front face does not bulge.
7. **The four screws are a small heat path through the cork** that the axisymmetric model cannot hold. Hand estimate: 2 percent more than the cork alone. With 1.6 mm cork the pilot is only 1.1 mm deeper than the screw tip (gate floor 1.0): hold the 8.0 +0.5/-0 pilot depth.
8. **Strip thickness 1.6 mm is an estimate**, as it was before. Strip cut pitch (700 mm assumed on a 50 mm pitch) depends on the strip bought.
9. **How the halo looks is not verified.** The approved photos put the ring 4 to 14 mm inside the rim (centre r 124) and added a faint rim strip; the product's strip is centred on r 115 with no rim strip. On a surface-cord install the power connector and cable hang in front of the strip at 6 o'clock, 8 mm from it; whether that throws a visible shadow in the halo can only be seen on a prototype.
10. **Images not re-rendered:** `renders-final/` product images (the phantom-post flag stays open), and `site/img/exploded-*.jpg` on the install page, which is an old render with the light on the rim. Its alt text still says "rim" because that is what the picture shows.
11. **Build documents not rewritten:** `build/assembly-SOP.md`, `QC-test-plan.md`, `sample-kit-shopping-list.md`, `cost-model.md` carry dated banners only. The SOP has no timed steps for the ring sub-assembly.
12. **Historical documents left as written** (`engineering-report.md` body, `design-report.md`, `BRIEF.md`, `REVIEW-fable52.md`, `label-light/REVIEW-pessimist.md`, `mounting-report.md`, older `NOTES.md` entries, the old render scripts): they describe the rim strip as it was on their date. `engineering-report.md` has a banner because its heat argument is the one that was wrong.
13. **The lit RFQ zip keeps its name** (`dome-cap-lit-RS-CAP-12L-revB.zip`) although the assembly sheet inside it is now rev B.1. The lit cap parts did not change. Nothing was ever sent, so no one holds the older zip.
14. **A 24 V adapter fault** (four times the strip power) is not covered by the heat study. It was an open item before and still is.
15. **START-HERE.html** now says "Four decisions you owe" and the LED card is marked done for both caps. The Kit price card's numbers were updated for the ring cost ($16 at $89, $25 at $99); the recommendation on that card was written when those were $25 and $35 and has not been revisited.
