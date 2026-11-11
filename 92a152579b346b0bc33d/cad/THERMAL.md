# Record temperature from the halo strip (2026-11-11)

Question from Austin: will the light heat the vinyl, and what goes between them. Answered with a model this time, not a sentence.

Model: `cad/thermal.py`, steady-state axisymmetric finite-volume conduction (MDF, air gap, PVC record, aluminium, cork) with film coefficients to room air, plus the light and infrared that land on the record's overhang (view factor 0.32 for the rim strip). Results in `cad/thermal-results.json`. It is a calculation. The buoyant air plume is not modelled and nothing has been measured.

Geometry fact that was missed before: the record (304.8 mm) is wider than the backplate (266.7 mm). Its outer 19 mm overhangs the rim strip, 3.45 mm in front of it, with only air between.

Normal case: 4 W strip, 30 C (86 F) room. Temperatures are rise over room air.

| Layout | Strip | Record, hottest spot | Record in a 30 C room |
|---|---|---|---|
| A. Today: strip on the rim, facing out | +12.9 K | +4.9 K | 34.9 C (95 F) |
| B. Strip on the back face, bare MDF | +17.3 K | +4.5 K | 34.5 C |
| C. Back face on a 1 mm aluminium ring, 30 mm wide | +8.0 K | +3.5 K | 33.5 C |
| D. C plus 2 mm cork under the aluminium | +9.2 K | +3.0 K | 33.0 C (91 F) |
| E. D with the ring 10 mm further in | +9.9 K | +3.2 K | 33.2 C |

Stacked worst case: the wrong 6 W strip, dead-still air (film coefficients halved), 35 C (95 F) room.

| Layout | Record |
|---|---|
| A. Today | 49.7 C (121 F) |
| D. Aluminium ring + cork, back face | 44.9 C (113 F) |

Vinyl softens at about 55 to 60 C (130 to 140 F).

Recommendation: layout D. The strip moves to the back face of the backplate, about 15 mm in from the rim, facing the wall. It sits on a 1 mm aluminium ring (30 mm wide, r 103 to 133 mm) that spreads the heat, with a 2 mm cork ring between the aluminium and the wood. The LEDs then have no line of sight to the record at all, and the wood plus cork sit between them. This is also the layout the approved product photos were lit with, so it closes the halo-mismatch flag. Nothing gets thicker: ring + cork + strip is about 5 mm inside the 25.4 mm gap behind the backplate.

Not done yet: the CAD, drawings, BOM and RFQ packets still describe the rim strip. First prototype: thermocouple on the record's back at r 117 mm and at the top edge, 2 hours on, before anything ships.

Projection from the wall, installed and tightened (from `assembly.py` / `assembly_lit.py`):

| Surface | From the wall |
|---|---|
| Backplate back (the halo gap) | 25.40 mm = 1.00 in |
| Record front face | 41.23 mm = 1.62 in |
| Plain chrome cap tip | 51.78 mm = 2.04 in |
| Lit cap tip | 56.48 mm = 2.22 in |
