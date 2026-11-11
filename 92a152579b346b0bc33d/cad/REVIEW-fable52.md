# Pessimist review 2: RS-CAP-12 rev C, RS-CAP-12L rev A.1 and the sconce they screw into

Reviewer model: claude-fable-5-2. Date 2026-11-11. Read-only on every design file; this report is the only file written.
Nothing sent, nothing committed.

Method: numbers were taken from `sconce_cad.py`, `sconce_lit.py`, `drawings*.py`, the RFQ SPEC files and the rendered
drawing PNGs, not from the prose. Geometry was re-probed by importing the CAD modules from a scratch dir (point-in-solid
probes, booleans, stack re-computation). Items marked (calc) are my own hand calculations and need a bench check; items
marked (unverified part) depend on a purchased part whose drawing nobody has opened yet.

Headline: rev C / rev A.1 fixed what the first review found, but the first review assumed the record stays at pad height
under the cap. It does not. There is nothing behind the record at the centre, and that one omission breaks flatness, the
label, and the entire pogo stack. Second headline: the lit cap cannot be assembled as drawn (two stack bugs inside the
cap that the interference check cannot see because threads are modelled at major diameter). Third: the surface-cord
(plug-in) option cannot physically be plugged in.

---

## MUST-FIX

### M1. Nothing supports the record behind the centre clamp: it dishes 1.4 to 1.6 mm, lands on the insert, and voids the pogo stack
- Where: `sconce_cad.py:44-46` (pads only at R 127 and R 69.85), `sconce_cad.py:451-458`, `assembly.py:63`,
  `sconce_lit.py:284-293` (`stack()` assumes record back face = pad height at the axis).
- Number: record back face sits 1.6 mm (pad) off the backplate; nearest support to the clamp is 69.85 mm away.
  Plate stiffness of an LP (E about 3 GPa, 1.4 mm mean thickness for a 140 g pressing, simply supported at R 70):
  about 0.3 mm per newton at the centre; even a 2.0 mm 180 g record is about 0.1 mm/N (calc). So 5 to 15 N of clamp
  force closes the whole 1.6 mm gap. Hand torque on the cap gives 50 to 150 N (M9 below).
- Why it fails:
  1. The record is bent into a 1.6 mm dish over a 70 mm radius and held there for years in a warm room. PVC creeps:
     the customer gets a permanently dished record. This is the exact "warp over years" Austin asked about, and it is
     mechanical, not thermal.
  2. The B-side label is clamped against the slotted end of the brass insert and painted MDF. Embossed ring, possible
     paint blocking onto the paper in Florida humidity. "Nothing touches your record but felt" (site/faq.html:31) is false.
  3. The stud goes 1.4 to 1.6 mm deeper than `stack()` assumes. Centre pogo compression becomes 3.40 nominal and
     4.38 with a thin record against a 3.00 stroke (re-computed with pad = 0). Every lit sconce that is tightened
     normally crushes the Mill-Max 0919. Rev C's "same stud length" fix does not help because both caps share the error.
- Fix: add a centre backing ring on the backplate front face, same thickness as the pads, directly opposite the cap
  felt: 1-1/4 OD x 3/8 ID x 1/16 felt (or better the M8 material), in a D 32.4 x 0.5 target pocket concentric with the
  insert bore. Add it to `felt_pads()`, the backplate drawing and BOM line 6. Then clamp force goes felt-record-felt in
  a straight line with zero bending, and `stack()` becomes true. Re-run the stack with both felts at their compressed
  thickness (backing ring 1.6 free, about 1.1 loaded).

### M2. Lit cap: the 0.9 mm D-key is taller than the 0.8 mm PCB, so the dome boss bottoms on the key and never clamps the PCB
- Where: `sconce_lit.py:44-45` (`SPG_KEY_H = 0.9`), `sconce_lit.py:83` (`LPCB_T = 0.8`), `drawings_lit.py:28-29, 56`.
- Number: key top at z 5.70, PCB top at z 5.60, boss face must reach 5.60. The key is an unthreaded D 8.0 shank; the
  boss thread minor is D 7.46. The boss cannot pass over it. Gap left over the PCB: 0.10 mm nominal (0.02 to 0.18 with
  a +/-10 % board).
- Why it fails: the boss clamp is the only LED return contact and the only thing holding the PCB. Result: no light or
  flicker, PCB rattles, and the dome's hard stop is 0.1 high so the lip-to-louver gap is wrong too. The interference
  check passes only because the dome bore is modelled at the M8 major diameter (`sconce_lit.py:165`).
- Fix: `SPG_KEY_H = 0.55` (below the 0.72 minimum board) and add a D 8.3 x 0.4 counterbore plus 0.2 chamfer to the
  boss mouth on RS-CAP-12L-DOME. Add a thread relief (D 7.3 x 0.5) on the spigot above the key so the LH thread has
  somewhere to run out. Add a top-side ENIG ring with vias on the LED PCB so the boss face is a second return contact.

### M3. Lit cap: 0.05 mm lip-to-louver gap against a tolerance stack of about +/-0.4 mm
- Where: `sconce_lit.py:64` (`LOUV_TOP = COL_TOP - 0.05`), `:68` (window same), `drawings_lit.py:28-30`.
- Number: the gap depends on column top (drawn "4.8", so +/-0.3 by the title block), boss-face-to-lip step (5.6 and
  4.8, both one-decimal, +/-0.3), PCB 0.8 +/-0.08, louver top +0/-0.05, window -0.05/-0.10. Budget 0.05.
- Why it fails: on roughly half of all builds the lip lands on the SLA louver or the 0.5 mm PC window before the boss
  clamps the PCB. Then either the louver ribs are crushed by the 1.5 N.m dome torque or the PCB is loose (no return).
- Fix: louver and window top at z 4.55 (gap 0.25). Tolerance the three datums explicitly: column top 4.80 +/-0.02,
  boss face to lip face 0.80 +/-0.02, PCB 0.80 +/-0.08. State on both drawings that the boss is the stop.

### M4. Lit cap: the whole flange hangs on a 0.3 mm brass web
- Where: `sconce_lit.py:35, 40` (recess 13.2 x 1.0 under a 1.3 flange), confirmed by point probes: for r 5.0 to 6.6
  the only metal is z 1.0 to 1.3.
- Number: web 0.30 thick, 1.6 wide, at r 5. Once the tiny felt (94 mm2) bottoms, the flange face is the hard stop.
  Bending stress at the web root for 50 N reacting at r 8: about 300 MPa (calc), at or above C360 yield.
- Why it fails: a normal hand-tightening permanently cones the flange upward. The rim rises into the louver and window
  (gap 0.05, see M3), so the brittle SLA ribs and PC ring become the structural stop. Cracked window, crushed fins,
  light pattern gone. It also dishes more on every swap.
- Fix: flange 1.8 thick with the recess kept at 1.0 (web 0.8), shift cone, column and dome up 0.5 (cap 15.3 tall), or
  shrink the recess to D 9.6 x 1.0 with a 9.5 OD felt so the web sits under the D 10 column in compression. Either way
  add the full-face interface from M5 so the flange is not the stop.

### M5. Chrome band (plain) and nickel/painted flange (lit) rotate on the label under load at every swap
- Where: `sconce_cad.py:140-142`, `drawings.py:311-313`, `sconce_lit.py:34-36`; prior review item 10 accepts the band as
  "a hard stop".
- Number: plain felt stands 0.6 proud; recess depth is drawn "1.0" so +/-0.3, felt thickness is +/-0.2 at best. Band
  annulus r 16.5 to 18.25 touches at about 70 N or less. Lit: felt bottoms at about 30 to 95 N, then a D 36.6 flange with
  a black-painted rim turns on the paper.
- Why it fails: a burnished or scuffed ring at D 33 to 38 on the customer's label, plus black paint transfer on the lit
  cap. Violates "nothing damaged when swapping records". Many pressings also have a stamper ring near r 16 to 18, right
  under the band (measure 10 records).
- Fix: ship a clear 0.25 mm PET label-saver washer (OD 37.5, ID 7.5) under every cap so slip happens metal-on-PET, and
  add 0.25 to both studs (11.95) to keep engagement and pogo numbers. Tolerance the plain recess 1.00 +/-0.05 and
  specify felt by compressed thickness.

### M6. Centre pogo: 2.15 mm of the 2.24 mm working window is consumed by the nominal design, leaving 0.09 for all tolerances
- Where: `sconce_lit.py:21, 101, 109-111`; `checks.md:76-84` (0.83 / 1.80 / 2.98 against 0.76..3.00).
- Number: tolerances not in the stack: stud 11.70 +/-0.1, MDF thickness "as supplied" (`rfq/backplate-mdf-cnc/SPEC.txt:10`)
  plus humidity swell 0.2 to 0.5, FDM relief depth 4.5 +/-0.2, PCB 1.6 +/-0.16, felt pads +/-0.3, pogo free height.
  Worst case about +/-0.9, RSS about +/-0.45. The RFQ also invites 1/2 in Baltic birch (SPEC.txt:3), which is 12.0 mm:
  compression 2.50 nominal, 3.68 thin (re-computed), and the 12.7 insert stands 0.7 proud, crushing the carrier
  (0.35 gap) and bottoming the return pogo (2.2 < 2.50 min).
- Why it fails: pin crushed on thin records or no contact on thick ones in a meaningful fraction of units, even after M1.
- Fix: a spring pin with at least 5 mm stroke centred on the stack (unverified part: pick from the Mill-Max long-stroke
  families and re-centre), AND a PEEK guard tube around the plunger (extend the carrier spigot) whose top sits at the
  pin's max-compression plane so no stud can ever bottom the pin. Delete birch from the lit-sconce backplate RFQ or
  spec thickness 12.70 +/-0.15. Print the tolerance stack in `checks.md`, not just three nominal cases.

### M7. Any screw other than the two 11.7 caps destroys the lit module, and the product ships such screws
- Where: `sconce_cad.py:134, 430` (RS-CAP-7 still 15.875), `build/BOM.md` line 4 (bonded cap on a 1/4-20 x 1 in bolt),
  engineering-report sec. 1 ("replace it at any hardware store").
- Number: RS-CAP-7 in a lit 12 in sconce: pogo compression 4.81 nominal, 6.5 with a thin 45; stud tip 0.22 above the
  backplate back face against a carrier spigot top at 1.65, so it rams the spigot by 1.4 mm (re-computed). A 1 in bolt
  is 5.9 mm proud of the back face, into the hub relief floor.
- Why it fails: the 3-piece Set puts 7 in caps and a 12 in sconce in one box with the 45 adapter. The rev C assert only
  ties CAP-12 to CAP-12L.
- Fix: RS-CAP-7 stud to about 12.3 with the same assert on tip position (not length); supersede BOM line 4 with
  RS-CAP-12 rev C or cut the bonded cap's bolt to 11.7 exposed with a dog point; the M6 guard tube makes the module
  survive anything else.

### M8. Pin and sleeve have no positive stop against the pogo force
- Where: `sconce_lit.py:30-32` (bore D 3.15 runs 13.5 deep, sleeve 10.0, pin 9.0, pin D 1.588 in ID 1.588),
  `drawings_lit.py:134-136`.
- Number: the pogo pushes 0.85 N inward forever. Sleeve retention: 0.025 press on PEEK (relaxes; anaerobics do not
  bond PEEK, yet the pin drawing still says Loctite 609 while the SPEC says stake). Pin retention: a nominal 0.000 fit
  in tubing whose ID tolerance is about +/-0.05, plus a 30 AWG wire. There is 3.5 mm of empty bore above the sleeve.
- Why it fails: pin or sleeve walks up the bore over months, pogo runs out of force, light flickers then dies.
  Staking the bore mouth moves brass toward the + pin and raises burrs on the contact face.
- Fix: step the bore (D 3.15 x 10.0 from the tip, then D 2.2 to z 1.8) so the sleeve seats on a shoulder; give the
  pin a D 2.4 x 0.5 head that seats on the sleeve top. Delete the stake and the 609 note. Add pin recess 0.05 +0.05/-0.

### M9. Drawings: critical fits fall under the +/-0.3 general tolerance, and the tolerance line is clipped off the RS-CAP-12 sheet
- Where: `drawings.py:111` (x.x +/-0.3), `drawings.py:341` ("dog point D 4.8 x 1.5"), RS-CAP-12.png (title block ends
  at "UNITS"; the GENERAL TOLERANCES line is below the border), RS-CAP-12L-CORE.png (note 6 clipped; column 4.8,
  spigot, key, cone and relief carry no dimension lines).
- Number: dog point 4.8 +/-0.3 gives 5.1 against the insert's 4.98 minimum minor: the cap will not start. Recess 1.0
  +/-0.3 moves the band-to-label gap from 0 to 0.9. Stud 11.70 is +/-0.1 against a 0.02 pogo margin.
- Fix: dog D 4.80 +0/-0.10; recess depth 1.00 +/-0.05; stud 11.70 +/-0.05; add all M3 datums; fix the sheet layout so
  notes and title block are fully inside the border; dimension the core properly instead of relying on notes.
  Also: thread class is before plating. EN 5 to 8 um adds up to 0.032 on pitch diameter, more than the 2A allowance
  (0.028): call "EN 5 um max, thread to accept a 2B GO gauge after plating".

### M10. Surface-cord (plug-in) option cannot be plugged in
- Where: `sconce_cad.py:72-80, 485-501`, mounting-report.md:19 and :35, engineering-report sec. 4.
- Number: jack axis is normal to the wall and its mouth is 7.5 mm from the wall plane. The modelled straight plug
  occupies z -8.5 to +7.5: 8.5 mm of plug body and then the cable are inside the wall.
- Why it fails: every UL adapter and inline dimmer ends in a straight moulded plug 20+ mm long. Without a hole in the
  wall it cannot mate; "the cable simply turns down" is not possible. The 9.5 x 12 cord channel leads to a jack the
  cord cannot reach. This is the default install for most buyers.
- Fix: replace the panel jack with a 150 mm 18 AWG pigtail ending in an inline female 5.5 x 2.1, clamped in the hub
  (P-clip or zip-tie anchor in the cord channel = real strain relief). Works for surface and in-wall. Or turn the jack
  90 degrees to exit at 6 o'clock.
- Related: mounting-report.md:28 tells the customer to cut a 1 in hole at the centre mark; the CAD needs 1-1/4 in
  centred 6 mm above centre (`checks.md:42`). A centred 1 in hole reaches y = 12.7, the plug spans y 10 to 20.

### M11. Contradictions that will cause a wrong build or a wrong claim
| # | Where | Says | CAD / truth | Fix |
|---|---|---|---|---|
| a | build/BOM.md line 5, cad/README.md:109 | cap felt 1 in OD x 1/8 in (SAW1GY) | `sconce_cad.py:137`: 1-1/4 x 3/8 x 1/16 in a 1.0 recess. The 1/8 felt stands 2.2 proud: rev A shadow gap back, engagement 5.9 | fix both; confirm the 1-1/4 x 1/16 SKU exists (unverified part) |
| b | rfq/backplate-mdf-cnc/SPEC.txt:7, drawing leader `drawings.py:173` | 6 felt pockets incl. 3 on R 127 | STEP has 3: the guard at `sconce_cad.py:215` is false (133.35 < 130.85), outer targets silently skipped; a D 13.3 pocket at R 127 would break through the rim | move outer pads to R 120, regenerate |
| c | rfq/dome-cap-brass/SPEC.txt:7-9, `drawings.py:320-321` | alt stud "cut to 17.7 (11.7 exposed)" | 6.0 in the cap from a 1.0 deep recess floor leaves 10.7 below the contact face | cut to 18.7; also say "5.1 x 7.0 MAX to the drill POINT" (a 118 deg point adds 1.5, leaving 0.5 under the apex) |
| d | mounting-report.md:31 | "twist clockwise" | `sconce_cad.py:305-310`: entries at stud angle +20, so locking is counter-clockwise from the room | mirror the J-slots so lock = clockwise (then cap-tightening torque seats the bayonet) |
| e | build/BOM.md lines 13, 14, 12, 2 | shoulder screws; M3 x 6 cup point; 1 in centre hole; jack at 6 o'clock | PEM FH-832-10 + lock nuts; M3 x 12 (6 cannot reach the tab); 30 x 37 slot; jack at (0, +15) | update BOM |
| f | site/faq.html:77, product.html:165 | ring draws "4 to 10 watts" | 6 W hard cap (README open question 7) | fix copy |
| g | site/faq.html:31, renders-final README (swap shots, flat-lay "post") | cap threads onto a post, record lifts off a post | no post exists; stud is part of the cap | see S1; fix copy or add the post |
| h | `build_all.py:146, 161, 165, 167` -> checks.md | 5/8 stud 9.0 engagement; thin 1.3 / thick 2.4; "plain cap bottoms the pogo, ship lit with lit" | 11.7 / 7.47; 1.2 / 2.7; fixed in rev C | regenerate the prose from parameters |
| i | renders-final README vs CAD | LED ring on the back face aimed at the wall plus a weak rim strip | MDF CAD, drawings, BOM: rim strip only (rear ring exists only on the aluminium variant) | still unresolved; product photos show a halo the CAD product will not make. Decide, then re-run thermal (4 W limit if rear) |
| j | PCB-SPEC.md:19, 40 | Z1 12 V bidirectional | reverse ESD is clamped at about -25 V across 3 LEDs; with the cap off the node floats to the rail and a 12 V-standoff part sits at its limit behind 20 mA | cap: unidirectional; hub: 15 V standoff |

---

## SHOULD-FIX

- S1. Swap ergonomics. With the cap off there is no spindle: the customer holds a 12 in record against the wall with one
  hand and hunts for a 5 mm hole with a brass stud through the label with the other. Dropped records and scratched
  labels will happen. The record also slides over 8 mm of thread crests and then rests on them (the dog point is only
  the last 1.5 mm, so the prior review's "smooth pilot" claim is wrong). Add a fixed locating feature (short nylon
  pilot bushing around the insert, OD 7.10, standing 2.5 proud) or at least an unthreaded D 7.10 x 2.4 shoulder under
  each cap so the record sits on a smooth, near-fitting diameter (slop 0.14 to 0.22 instead of 0.9 to 1.2).
- S2. Preload decay. Real clamp force is about 100 N at 0.5 N.m because the felt face radius dominates (calc: T is about
  5 mm x F); the prior review's 800 N was a bare-fastener number. Wool felt takes 30 to 50 % set, so this goes to about
  zero in weeks: record can shift 0.5 mm on the stud and rattle, and the lit return path through the thread goes
  intermittent (visible flicker). Use a low-set microcellular urethane (PORON-class, 1.6 mm) for the cap washer and the
  M1 backing ring, wool felt only where it touches grooves.
- S3. Bayonet slop. `NUT_GAP` leaves 0.6 mm axial play (`sconce_cad.py:115`): the fixture leans out about 0.36 deg and clacks
  when touched. Ramp the J-web 0.6 over the 20 deg arc, or set the gauge to 6.7 with a wave washer. Specify flangeless
  drywall anchors: an anchor collar eats the 0.8 mm head clearance and the hub will not seat.
- S4. Halo strip thermal. 6 W on an 8 mm strip bonded to MDF, one face exposed: I get a 35 to 40 K rise (calc), so 65 to
  70 C in a 30 C room, above the review's own 55 C acceptance limit. Default to the 4 W 2835 strip, or put a 10 x 1
  aluminium flat under the strip. Paint or seal the rabbet (drawing says unpainted OK): tape on raw MDF at 60 C in
  Florida humidity lets go, and the strip is spring-loaded to straighten. Clip both ends at 6 o'clock.
- S5. Wrong adapter. 5.5 x 2.1 is the universal barrel; a 24 V brick triples strip power on wood under vinyl. Add a
  0.75 A hold PTC and a 15 V TVS at the jack, and mark "12 V DC ONLY" on the hub. Put a 100 mA PTC on the 26 AWG tap
  to the hub PCB (it sits upstream of the 20 mA limit on a 2 A rail).
- S6. Return pogo landing. It lands at r 3.8 on an insert end face modelled as a plain ring; the real E-Z Lok has a
  thread chamfer and a knife-thread lead (unverified part). Measure the flat land and put P2 at its mid radius.
  Carrier float in the D 14 relief is +/-0.5 but the spigot's capture range is 0.39: lead-in to 0.8 x 45.
  Insert minor diameter is 4.98 to 5.26, so spigot play is 0.09 to 0.23, not 0.09 (`sconce_lit.py:28, 318`).
- S7. Core finish note is self-contradictory ("EN all over ... mask the thread, the bore and the column top"). Say:
  EN everywhere, mask those areas from PAINT only. Loctite 270 needs activator on nickel and must be kept off the
  column top and the PCB ring.
- S8. The D 1.0 cross-hole breaks out through the column top face at az 60 (probe: seat missing from r 4.5 outward),
  not "the column side at z 4.6". Harmless if deburred, but the drawing note is wrong and the burr sits on the PCB seat.
- S9. Louver is located by nothing (three glue dots on a cone). Add a 0.3 locating step. 0.25 mm SLA fins spanning
  16 mm at 37 to 42 C will sag; the +/-0.03 channel tolerance is not a real SLA tolerance.
- S10. Label fading. About 134 lux average (more near the cap) 24/7 is over 1 Mlux.h per year; vintage reds and
  fluorescents fade in a few years, with a sharp unfaded disc under the cap. Disclose it and recommend dimming.
  UV itself is negligible for a 2700 K LED.
- S11. Decorative chrome: say where the plater may rack (stud only), require masking (do not allow "chase after
  plating", chrome flakes), add R 0.2 at the relief root. Rev C sheet prints DATE 2026-11-09 (`drawings.py:13`).
  README still says the brass cap is 63 g; rev C is 54.6 g.
- S12. UL claim (faq.html:41): "every electrical component is listed" will not be true of the two custom PCBs in the
  lit cap. Reword for the lit SKU. Hardwired option C stays unadvertised until UL 2108.

---

## VERIFIED-OK (number checked)

- Stud vs spindle hole: 6.35 max major in a 7.24 to 7.32 hole, 0.89 to 0.97 diametral clearance; never binds, even on
  tight new pressings. (Too loose to centre anything: see S1.)
- Plain cap geometry: D 38.10 x 10.00, sphere R 25.80, recess D 33.0 x 1.0, stud 11.70 from the band face, dog 4.8 x 1.5;
  CAD, drawing and RFQ SPEC agree. Valid single solid, 6.42 cm3.
- Plain and lit studs are the same length and the assert enforces it (`sconce_lit.py:25`).
- Thread engagement: plain 7.47 total / 5.97 threaded; lit thick-record worst 5.30 threaded (4.2 threads). Fine for a
  160 g record and 100 N preload. Stud end 5.23 short of the backplate back face; never proud.
- Hollow stud: wall 0.82 at the root, 10.3 mm2; over 2 kN in C360 against about 0.1 kN real preload.
- Short-circuit guard: even with my larger misalignment (thread 0.15 + spigot 0.23 + plunger wobble 0.15 + concentricity
  0.1 = 0.63) the plunger edge reaches r 1.17 against brass at r 1.575. It lands on gold or PEEK. A short costs 20 mA.
- Unscrewing live: the pin leaves the pogo before the thread releases; 12 V, 20 mA, no arc. Dome at up to 12 V from a
  Class 2 source is touch-safe. Halo is on its own branch and stays lit. D1 blocks a reversed adapter for the label
  circuit; a reversed strip just stays dark.
- Lit cap heat: 0.17 W in 49 g of brass. Convection-only 12 K, about 7 K with conduction into the record and stud
  (calc). Cap about 37 C in a 30 C room, 42 C in a 35 C room. No scorch or softening risk; no heat source touches
  vinyl. Do not raise the CCR above 20 mA without a thermocouple run.
- Hub CCR with a shorted pin: 0.24 to 0.26 W, covered by the 25 mm2 copper call-out.
- LH dome thread: unscrewing torque on the dome tightens the M8x0.5 LH joint (checked the handedness). Tightening
  torque loosens it, but 1 N.m is far below a cured 270 joint.
- Galling: C360 on a brass insert (plain) and EN on brass (lit) are benign pairs; chrome is kept off the thread.
- Cap internals with no overlap at nominal: all 12 cap part pairs intersect at 0.000 mm3; LED to louver 2.6, LED to
  flange 2.7, PCB edge to dome wall 0.20, cross-hole to recess corner wall 0.42.
- Hub screws: #8 x 1 in, 12.7 into a 14 deep D 3.2 pilot, 6.25 clear of the nut pockets, 16.5 clear of the DC pocket.
- Bayonet stack: nut 4.1 under the pocket ceiling, stud end 1.23 under it, entry hole 0.72 over the nut corners.
- Code position: plug-in 12 V Class 2 from a listed adapter is the same footing as any LED strip kit; in-wall is legal
  only in CL2 cable with the adapter outside the wall, which the docs say correctly.
- LED position: CAD, drawings and BOM agree with each other (rim strip on MDF). Only the renders disagree (M11 i).
