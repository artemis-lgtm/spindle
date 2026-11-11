# Record temperature from the halo strip (2026-11-11, updated for the final layout)

Question from Austin: will the light heat the vinyl, and what goes between them. Answered with a model, not a sentence.

**Status: the heat-safe layout is now the canonical CAD.** It is the same on the plain-cap sconce and the lit-cap sconce (12 in, MDF backplate). What changed in the CAD and every file touched: `cad/FIXES-heat-layout.md`.

Model: `cad/thermal.py`, steady-state axisymmetric finite-volume conduction (MDF, air gap, PVC record, aluminium, cork) with film coefficients to room air, plus the light and infrared that land on the record's overhang. Results in `cad/thermal-results.json`. `build_all.py` re-runs it on every build and reads the final geometry straight from `sconce_cad.py`, so the numbers below cannot drift from the CAD. It is a calculation. Nothing has been measured.

Geometry fact that was missed before: the record (304.8 mm) is wider than the backplate (266.7 mm). With the old rim strip, the record's outer 19 mm overhung the strip, 3.45 mm in front of it, with only air between.

## The final layout (what is in the CAD now)

- LED strip, 8 mm wide, on the BACK of the backplate, LEDs facing the wall, centred at r 115 mm (r 111 to 119).
- Aluminium ring RS-HR-12 under the strip: 1.0 mm thick, r 100 to 130 mm (OD 260, ID 200). It spreads the heat.
- Cork ring RS-CK-12 between the aluminium and the wood: 1.6 mm (1/16 in) thick, same OD and ID. It was 2.0 mm in the study; 2 mm sheet is not a stocked size and 1/16 in is, so 1/16 in is the spec (see the cork table below).
- Four small screws hold the two rings to the back of the backplate.
- The strip is 14.35 mm inside the backplate rim, on the far side of the wood. The LEDs cannot see the record. 15.3 mm of aluminium, cork and MDF sit between the strip and the record.
- Nothing gets thicker: the stack is 4.2 mm deep (4.7 mm at a screw head) inside the 25.4 mm gap behind the backplate. The strip face is 21.2 mm from the wall.

## Normal case: 4 W strip, 30 C (86 F) room

Temperatures in the "rise" columns are above room air.

| Layout | Strip rise | Record hottest spot, rise | Record in a 30 C room | Strip in a 30 C room |
|---|---|---|---|---|
| A. Old: strip on the rim, facing out | +13.0 K | +4.9 K | 34.9 C (95 F) | 43.0 C |
| B. Strip on the back face, bare MDF | +17.2 K | +4.5 K | 34.5 C | 47.2 C |
| C. Back face on a 1 mm aluminium ring, 30 mm wide | +8.0 K | +3.5 K | 33.5 C | 38.0 C |
| D. Study version: C plus 2 mm cork (ring r 103 to 133, strip r 114 to 122) | +9.2 K | +3.0 K | 33.0 C | 39.2 C |
| E. D with the ring 10 mm further in | +9.9 K | +3.2 K | 33.2 C | 39.9 C |
| **F  FINAL, as built in the CAD (ring r 100 to 130, strip r 111 to 119, cork 1.6 mm)** | **+9.2 K** | **+3.1 K** | **33.1 C (92 F)** | **39.2 C (102 F)** |

The record's hottest spot in the final layout is at r 114 mm, directly in front of the strip through the wood. The overhanging edge of the record rises 1.3 K.

## Stacked worst case: the wrong 6 W strip, dead-still air (every film coefficient halved), 35 C (95 F) room

| Layout | Record hottest spot, rise | Record | Strip |
|---|---|---|---|
| A. Old: strip on the rim | +14.6 K | 49.6 C (121 F) | 64.1 C |
| D. Study version | +9.9 K | 44.9 C (113 F) | 56.5 C |
| **F  FINAL, as built in the CAD** | **+10.2 K** | **45.2 C (113 F)** | **56.2 C (133 F)** |

Vinyl softens at about 55 to 60 C (130 to 140 F). The final layout keeps the record about 10 K below that even in the stacked worst case, and 22 K below it in the normal case.

The final geometry differs from the study version (D) in two ways: the ring is 3 mm further in, so it clears the rim by 3.35 mm, and the cork is 1.6 mm instead of 2.0 mm. Together that costs 0.1 K in the normal case and 0.3 K in the worst case.

## Why 1/16 in cork is fine

Same final geometry, only the cork thickness changed. Record hottest spot:

| Cork | Normal (4 W, 30 C room) | Stacked worst (6 W, still air, 35 C room) | Can we buy it |
|---|---|---|---|
| 2.0 mm | 33.04 C | 44.92 C | not a stocked sheet size |
| **1.6 mm (1/16 in), the spec** | **33.14 C** | **45.16 C** | yes, WidgetCo roll |
| 1.5 mm | 33.17 C | 45.22 C | yes, The Cork Store sheets |
| no cork at all | 33.55 C | 45.98 C | |

Going from 2.0 mm to 1/16 in costs 0.10 K in the normal case and 0.23 K in the worst case. The whole cork ring is worth about 0.4 K normal and 0.8 K worst. The aluminium ring and the move to the back face do most of the work.

Model note: the grid step through the thickness was refined from 0.25 mm to 0.1 mm for this run so that 1.6 mm and 1.5 mm are told apart. A few older rows moved by 0.1 as a result (for example the old rim strip's worst case reads 49.6 C, where the first run printed 49.7 C).

## The lit cap

The lit cap adds 0.17 W at the centre of the record, 95 mm away from the halo's warm band. `label-light/DESIGN.md` section 4 estimates the cap's own rise at about 11 K worst case with convection only, and 5 to 7 K once conduction into the record and screw is counted. The record under the cap cannot be warmer than the cap, so that is about 41 C worst case in a 30 C room (35 to 37 C expected). The halo adds 0.02 K at the centre in the normal case and 0.30 K in the stacked worst case, so the two do not stack. Both the cap figure and this combination are estimates: DESIGN.md marks the cap rise "must be measured", and the cap is not in `thermal.py`.

## What the model leaves out

- The buoyant air plume rising behind the backplate. Not modelled.
- The four steel screws through the cork. Hand calculation: each #4 screw buried 6.9 mm in MDF passes about 0.003 W/K into the wood (the wood around it is the bottleneck), 0.011 W/K for four, against about 0.61 W/K through the cork ring itself. That is 2 percent more heat path. Not in the model.
- The hub (it covers the back face inside r 63.5) and the cap. Not in the model.
- The 7 in sconce and the aluminium-backplate variants. Not modelled, and not on this layout.
- Strip efficiency is assumed 35 percent light, 65 percent heat. Stray light reaching the record's overhang off the wall is assumed 0.1 W at 4 W.

## First prototype test (not done, nothing exists to test yet)

Thermocouple on the record's back at r 114 mm, at the top edge, and under the cap. Two hours on, in a still room. Accept: record no more than 5 K above the room with the 4 W strip. Nothing ships before this.

## Projection from the wall, installed and tightened

Measured on the rebuilt assemblies (`gates.py`, section HEAT). Unchanged by the new layout.

| Surface | From the wall |
|---|---|
| LED strip face (now behind the backplate) | 21.20 mm = 0.83 in |
| Backplate back (the halo gap) | 25.40 mm = 1.00 in |
| Record front face | 41.23 mm = 1.62 in |
| Plain chrome cap tip | 51.78 mm = 2.04 in |
| Lit cap tip | 56.48 mm = 2.22 in |
