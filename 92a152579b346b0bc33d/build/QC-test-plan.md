# Test and inspection plan: 12 in Spindle sconce

Rewritten 2026-11-11 by the product audit (`../audits/AUDIT-product.md`) for the canonical CAD (strip on the back of the backplate on an aluminium ring over cork; turned one-piece cap; pigtail power; twist-lock hub rev C). The plan from 2026-11-10 is in `SUPERSEDED/QC-test-plan-2026-11-10.md`.

Nothing in this file has been run. Nothing exists to test yet. Section 4 is the list of tests the first three prototypes must pass **before any unit is sold or shipped**, including the 20 already pre-sold.

## 1. Incoming inspection

| Part | Check | Tool | Accept | Sample |
|---|---|---|---|---|
| Backplate RS-BP-12-MDF rev C | Diameter 266.7; thickness 12.70 +/-0.15; plain square rim; four blind holes on the back, none through; six felt targets; paint covers every routed surface | Caliper, eyes | All in tolerance; no raw MDF | Every part of the first lot, then 1 in 10 |
| Hub RS-HUB-01 rev C | Hangs and twists on the master plate; the tab pocket is the long arc (about 32 degrees), not a 10 mm notch | Master plate | Full 20 degree twist, no scrape | Every part |
| Wall plate RS-WP-01 rev B | Three studs tight (cannot be turned by hand with pliers on the thread at about 2 N m); tab square; flat within 0.3 | Pliers, square | No loose stud | Every part of the first lot |
| Aluminium ring RS-HR-12 | OD 260, ID 200, 1.0 thick, four holes; flat on a table within 0.5; no burr on the inner edge (the leads cross it) | Caliper, finger | As listed | 1 in 10 |
| Cork | Thickness: measure it. The supplier's page says both 1/16 in and 2 mm. | Caliper | 1.5 to 2.0 mm; record which | Every roll |
| LED strip | Cut one 700 mm length, power at 12.0 V, read the current after 5 minutes | Bench supply | **0.20 to 0.42 A. Over 0.42 A the reel is rejected** | Every reel |
| LED strip | Listing mark printed on the strip or reel (UL or ETL file number) | Eyes | Present; write the number in the lot record | Every reel |
| Adapter | Marked 12 V DC, Class 2 (or LPS), UL or ETL listed with a file number, efficiency level VI, centre positive, FCC statement | Eyes, meter | All present; open-circuit voltage 11.4 to 12.6 V | Every lot, 3 pieces |
| Dimmer | Passes 12 V at 100%; no coin-cell remote in the box (a coin-cell remote triggers Reese's Law labelling) | Meter | As listed | Every lot, 3 pieces |
| Cap RS-CAP-12 rev D | Stud length 11.95 +/-0.05; shoulder 7.10 +0/-0.05; thread accepts a 1/4-20 nut by fingers after plating; no pits or burn in the chrome | Caliper, nut | As listed | Every part |
| Insert E-Z Lok 400-4 | 1/4-20 internal, 12.7 long | Caliper | As listed | 3 per bag |

## 2. In-process checks

These are the right-hand column of `assembly-SOP.md`. The three that stop a unit: ring current over 0.42 A (step 6), a bulge on the front face over a ring screw (step 7), a short at the splice (step 8).

## 3. Final check, every unit

| # | Check | Accept |
|---|---|---|
| 1 | Current at 12.0 V, full brightness | 0.20 to 0.42 A |
| 2 | 30 minute burn-in done | No dark piece, no flicker, no smell |
| 3 | Dimmer sweep | Smooth, no visible flicker, no whine at arm's length |
| 4 | Trial hang on the master plate, set screw in and out | Pass |
| 5 | Cap spins in by fingers, stops firmly, comes out again | Pass |
| 6 | Front face under the record area | No bulge over ring screws, insert flush, hub screws flush, seven felt pieces in place |
| 7 | Box contents against the packing list (including the straight hex driver and the PET washer) | Complete |
| 8 | Rating label and serial number on the hub | Present, readable |

## 4. Prototype tests. All must pass before any sale.

Three prototypes. Keep photos and the raw readings in `build/test-records/` (folder does not exist yet).

### T1. Two-hour heat soak (the test that decides whether the record is safe)

Why: `../cad/THERMAL.md` is a calculation. It predicts the record 3.1 C above the room with a 4 W strip. It leaves out the warm air that rises behind the backplate, which the audit estimates adds 1 to 2 C. Record vinyl begins to lose stiffness at about 48 to 50 C and its glass transition is 52 to 54 C (US patent 3,975,321, Table III).

Set-up:
- Room 20 to 26 C, steady within 1 C for the whole run. Still air: air conditioning vents closed or off, doors shut, nobody walking past, no sun on the test wall.
- The sconce hangs on a real interior drywall wall, or on a piece of 1/2 in drywall at least 600 x 600 mm backed with 50 mm of foam board. Centre of the sconce about 1.5 m from the floor. Nothing within 300 mm above it for run A.
- In-wall style install (no surface cord under the unit).
- The kit's own adapter and dimmer, dimmer at full. Measure and write down the voltage at the pigtail jack and the current.
- A black 180 g record for runs A and B. Repeat run A once with a thin record (about 120 g).
- Thermocouples: type K or T, fine wire (30 AWG or thinner), each bead taped flat with polyimide tape and a dab of thermal paste. A data logger or a multi-channel meter read every minute.

| Channel | Where | Why |
|---|---|---|
| TC1 | Record BACK face, 114 mm from the centre, at 12 o'clock | The predicted hot spot, at the top where the rising warm air also arrives |
| TC2 | Record back face, 114 mm from the centre, at 6 o'clock | Same radius, no rising air |
| TC3 | Record back face, 143 mm from the centre (the overhang), at 12 o'clock | The edge that hangs past the backplate |
| TC4 | Record FRONT face, 25 mm from the centre, beside the cap | Under-cap region |
| TC5 | Aluminium ring, beside the strip, at 12 o'clock | Strip temperature |
| TC6 | Backplate FRONT face, 114 mm from the centre, at 12 o'clock (under the record) | Checks the model's wood temperature |
| TC7 | Air, in the gap behind the backplate at the top (125 mm above the centre, mid-gap), bead shielded from the LED light with a foil flag | The rising air the model leaves out |
| TC8 | Wall surface behind the strip at 12 o'clock | Wall heating |
| TC9 | Hub side wall at 12 o'clock | Plastic temperature |
| TC10 | Room air, 1 m to the side at the same height, shielded from the halo | Reference |

Procedure: start logging with the light off for 15 minutes (all channels must agree within 0.5 C; if not, fix the thermocouples). Switch on at full. Log for at least 120 minutes and until no channel moves more than 0.5 C in 15 minutes.

| Run | Condition | Pass: rise above TC10 at the end |
|---|---|---|
| A | Normal: production strip, open wall | Record (TC1 to TC4) **6.0 C or less**. Aluminium ring (TC5) 15 C or less. Gap air (TC7) 8 C or less. Wall (TC8) 15 C or less. Hub (TC9) 10 C or less |
| B | Abnormal: a shelf or board fixed 50 mm above the top of the record, full width, and the supply raised to 13.2 V (or a 6 W strip fitted) | Record **10.0 C or less** (so that in a 35 C room it stays at or under 45 C). Aluminium ring 30 C or less |
| C | Wrong adapter: 24 V on the jack, behind a shield, fire extinguisher in reach, 10 minutes or until the strip dies | No flame, no smoke that continues after the strip fails, no charring of the MDF, record 48 C or less. Write down what failed and how long it took |

If run A fails: do not sell. Lower the strip power and repeat. If run A passes with less than 1 C of margin, treat it as a fail.

Flatness, same runs: before switching on, lay a steel straightedge across the record on three diameters and measure the largest gap with feeler gauges. Repeat at the end of run A while hot, and again 2 hours after switching off. Pass: the hot reading within 0.5 mm of the cold one, and the cooled reading within 0.2 mm of the first. A thin record that cups when warm and does not come back is a fail even if every temperature passes.

Endurance: leave one prototype on at full for 500 hours. Each week: flatness, every strip piece still stuck down at both ends, current unchanged within 10%.

### T2. Wall mount

Mount a prototype on 1/2 in drywall with the kit's own two anchors and screws, away from a stud.
- 67 N (15 lb) outward on the backplate rim at 12 o'clock, held 1 minute, with a luggage scale and a strap.
- 133 N (30 lb) straight down on the cap, held 1 minute.
- Pass: nothing moves more than 1 mm, no anchor pulls, the hub does not unlock, nothing cracks.
- Then pull outward on the rim until something fails. Write down the force and what failed. Why: a 10 lb tug on the backplate rim puts about 18 lb on each anchor (hand calculation in the audit), which is the working limit of a good plastic anchor.

### T3. Twist-lock

- 50 hang, twist, set-screw-in, set-screw-out, twist-off cycles on one hub and plate. Pass: still locks, no white stress marks or cracks at the J-slots.
- With the set screw IN: 2 N m anticlockwise on the backplate by hand. Pass: does not unlock.
- With the set screw OUT: hold the record and unscrew a firmly tightened cap. Write down whether the hub unlocks from the plate. If it does, the install card must make the set screw step impossible to skip.
- Hand the unit, the plate on a wall and the straight hex driver to someone who has not seen it. Pass: they fit the set screw in under 2 minutes without help and without touching the LED strip.

### T4. Threaded insert in MDF

Why: E-Z Lok lists this knife-thread insert for hardwood and points to a different type for MDF.
- 300 cap on and off cycles at finger torque. Pass: insert has not turned or risen; cap thread shows brass-coloured wear at most, no flaking that jams the thread.
- Tighten the cap hard by hand, then unscrew: the insert must stay put (5 times).
- Pull the cap straight out with 200 N (45 lb). Pass: insert does not move.

### T5. Label

50 cap cycles on a paper-label record with the PET washer in place. Pass: no ring worn into the label, no tear at the centre hole.

### T6. Humidity

One finished backplate (insert, felt, ring screwed on) for 7 days in a closed tote at room temperature over a saturated salt solution (potassium chloride gives about 84% relative humidity), then 2 days in a normal room. Pass: thickness change 0.3 mm or less, no cracked paint, insert not proud, ring screws still tight, ring still flat. Standard MDF moves about 0.3% in length between 50 and 80% humidity, which is 0.8 mm across this disc.

### T7. Shipping drop

Packed as it will ship, with a record in the box for the Sconce. Ten drops from 760 mm (30 in) onto concrete: the ISTA 1A height for a parcel under 21 lb. One on each face, then corners and edges. Pass: backplate edge not chipped, paint intact, cap still in its pocket and not dented, record not cracked or scuffed, strip lights, hub not cracked.

### T8. What it looks like

- Photograph the lit halo straight on in a dim room and in a daylit room, beside the approved render. The product's strip is at 115 mm; the approved images were lit at 124 mm with an extra rim strip, so the real halo may be narrower and dimmer. Austin signs the photo or the design changes.
- Stand beside the wall. From about 65 degrees off straight-on the bare edge of the aluminium and cork rings comes into view under the backplate rim, and the strip corners soon after. Photograph at 65 and 80 degrees. If the bright metal edge shows, paint the ring's outer edge black.
- Surface-cord install: check for a shadow notch in the halo at 6 o'clock from the cord and connector.

### T9. Electrical

- Dimmer at 10%, 50%, 100%: phone slow-motion video of the halo. No rolling bands at any setting. If a scope is to hand, the PWM frequency should be 1.25 kHz or higher.
- Quiet room at night, 1 m away: no whine from adapter or dimmer at any setting.
- An AM radio 1 m away: no new buzz when the dimmer is at 50%.
- Reverse polarity for 1 minute (centre negative): no damage, lights normally afterwards.
- Short the jack for 10 seconds on the kit adapter: adapter shuts down and recovers, nothing warm.

## 5. Records

For every lot: strip reel listing number and measured current, adapter model and listing number, cork thickness, T1 run sheets, who built and who checked each serial number. These are also the documents an insurer or a safety lab will ask for.
