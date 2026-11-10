# Assembly SOP: one 12" unit (build/assembly-SOP.md)

Prepared 2026-11-10. Builds one Kit or Sconce from the BOM.md parts. Times are for one person with the jigs in section 1 already made; the first three prototypes will take about double. Target: 20 minutes per unit at batch 100 (cost-model.md assumes 25 minutes for the first 20, 20 minutes at 100). Dimensions come from engineering-report.md section 6 and mounting-report.md section 1 and are not re-derived.

Safety rule that governs every step: nothing in this fixture carries more than 12 V DC. The UL-listed adapter is the only part that touches 120 V and it is never opened, modified or placed inside a wall.

## 1. Jigs to make once (about 2 hours total)

| Jig | What it is | Why |
|---|---|---|
| J1 Felt-pad template | A 10.5" paper or 1/8" hardboard disc with a 25/64" centre hole and six 1/2" holes: three at 5.00" radius and three at 2.75" radius, 120 degrees apart, one of each at 12 o'clock. Mark 12 o'clock on the edge. | Pads land in the same place every time; the three-point plane is what stops warp and rotation. |
| J2 Hub centring jig | A 10.5" ring of 1/4" ply with a 5.00" hole in the centre and a 12 o'clock notch. Drop over the backplate's back, the hub goes in the hole. | Hub concentric to the plate within 1/32" so the record sits centred over the hub. |
| J3 Dome fill fixture | A block of 2x4 with four 38 mm holes drilled 10 mm deep, open side up. | Holds four shells level while the epoxy cures; bolt stands vertical in each. |
| J4 Strip start mark | A 1/4" wide saw kerf at 6 o'clock in the rim rabbet, cut when the backplate is made. | Every strip starts and ends at the lead notch; the leads come out at 6 o'clock to the jack. |
| J5 Polarity tester | A spare 5.5 x 2.1 barrel plug on 6" of wire with a red LED + 1 kohm resistor across it. Lights only when centre is positive. | Thirty-second polarity check before any unit is powered. |
| J6 Pull-test hook | A #8 screw with a loop of cord, and a 1-gallon water jug (8.3 lb). | QC-test-plan.md pull test. |

## 2. Build steps

Stack convention: 12 o'clock is up on the wall. Looking at the FRONT (record side) of the backplate, the lead notch and the jack are at 6 o'clock.

| Step | Minutes | What to do | Check |
|---|---|---|---|
| 1. Backplate prep | 3 (0 if CNC-cut arrives finished) | Confirm 10.50" diameter, 25/64" centre hole, rim rabbet 0.40" wide x 0.06" deep centred on the rim, 1/4" lead notch at 6 o'clock running to the back face. Sand 220, two coats matte black, front, rim and back. Dry 1 hour between coats. | Paint fully cured before felt or strip; tacky paint lifts adhesive within a week. |
| 2. Insert | 1 | Wet the centre hole with thin CA, wait 30 seconds, drive the E-Z Lok 400-4 from the FRONT with the hex drive (or a 1/4-20 bolt and two jam nuts) until the insert is flush with the front face. The insert is 0.500" long and fills the full plate thickness. | Thread a 1/4-20 bolt through from the front; it must turn freely and protrude about 1/4" out the back. |
| 3. Felt pads | 1 | Lay J1 on the front, 12 o'clock to 12 o'clock. Press one 1/2" pad through each of the six holes. Remove J1, burnish each pad with a thumb for 3 seconds. | Six pads, none on the rim, none over the hole. |
| 4. Hub prep | 2 | Printed PETG hub (5" x 1"): press the DC jack (Adafruit 610) into the 8 mm pocket at the 6 o'clock edge from the outside, nut on the inside, lugs pointing into the cable channel. Fit the M3 set screw into its rim boss (two turns). Press the two silicone bumpers at 5 and 7 o'clock on the wall face. | Jack nut tight; jack sits flush with the hub rim. |
| 5. Hub to plate | 2 + cure | Wood glue (MDF plate) on the hub's plate face. Drop J2 over the back of the plate, set the hub in J2's hole with the jack at 6 o'clock aligned with the lead notch, and the J-slot "12" mark at 12 o'clock. Two #8 x 3/4" screws from the hub side into the plate at 3 and 9 o'clock, away from the insert's 0.30" clearance pocket. Clamp flat, 30 minutes. | The 1/4-20 bolt from step 2 must still turn freely: the clearance pocket is behind the insert. |
| 6. Strip | 4 | Cut 36" of COB at the nearest cut mark (COB cut marks every 1" to 2"). Peel 2" of liner, start at J4 (the 6 o'clock notch), LEDs facing OUTWARD (radially), press into the rabbet. Work clockwise, peeling as you go, keeping the strip centred in the rabbet. The strip is a face bend at 5.25" radius; never fold it edgewise. Finish at the notch; trim at the last cut mark so the ends meet with a 1/8" gap. Burnish the whole ring with a soft cloth. | No lifted edges; both ends at the notch; the strip edge flush with the rim. |
| 7. Solder leads | 3 | Tin the strip's + and - pads at the START end (the end that still has the factory solder pads; if neither, use a COB solder-pad connector). Solder 12" of 18 AWG: RED to +, BLACK to -. Slide 3/16" heat shrink over each joint and shrink. Route both leads through the lead notch to the back, along the hub's cable channel to the jack. Solder RED to the jack's CENTRE pin lug, BLACK to the SLEEVE (outer) lug. Heat shrink both lugs. | Centre positive. Our adapter and dimmer are centre-positive 5.5 x 2.1; a reversed COB simply does not light, but the convention must match the in-wall barrel pairs the customer may wire later. |
| 8. Polarity + smoke test | 1 | Plug J5 into the adapter + dimmer chain: red LED lights = centre positive. Then plug the chain into the hub jack. Full brightness, then dim to minimum: no flicker visible to the eye, no dead segments. Hold 60 seconds. | Any dark segment = re-seat or replace the strip. Any flicker at low dim = swap the dimmer (QC-test-plan.md section 4). |
| 9. Strain relief | 1 | A pea of hot glue over each solder joint at the strip, and a hot-glue dab holding the lead in the notch and in the hub channel at two points so a tug on the jack cannot reach the COB pads. | Pull the leads with 2 lb; nothing moves. |
| 10. Dome cap assembly (batched, 4 at a time in J3) | 3 per 4 caps + 24 h cure | Degrease the inside of a 38 mm shell with alcohol. Thread the 1/4-20 x 1" bolt through the 1-1/2" fender washer, head on the washer. Set the shell open-side-up in J3, fill to 3 mm below the rim with mixed JB Weld, lower the bolt head into the epoxy so the washer seats on the shell's rim, bolt pointing straight up. Check plumb with a square. Cure 24 h. Stick one 1" felt washer (Durofelt SAW1GY-50) to the washer face, centred on the stud. | After cure: grip the dome, turn the stud with fingers; zero rotation. Stud protrudes 0.73" to 0.78" below the felt. |
| 11. Mount plate + studs | 1 | Fit the three 8-32 shoulder screws into the steel plate's stud holes, heads on the wall side, shoulders towards the room. Bag with 2 x #8 x 1-1/4" screws, 2 anchors, the M3 key. | Studs tight, all three the same height. |
| 12. Record fit (Sconce only; Kit skips) | 2 | Set the LP label-out on the six pads, spindle hole over the insert. Drop the dome's stud through the hole, turn until finger-snug (about 1/4 turn past contact). Push the record's edge firmly sideways: no rotation. Unscrew, bag the dome. | The clamp stack is record 0.07" + felt 0.125" + pads 0.0625" = about 0.27"; the stud bottoms in the insert before the dome bottoms on the label. If the dome bottoms first, add a second felt washer. |
| 13. Pack | 2 | 13 x 13 x 3 box, foam corners. Backplate face up (hub down) on the corners. Record (if any) in a black poly-lined sleeve on top of the backplate. Dome in its pouch sitting in the centre where the spindle hole is, so it is the first thing seen. Adapter, dimmer, mount plate bag and 45 adapter in the corner pockets. Card on top. Tape. Weigh and write the weight on the box for the shipping log. | Shake test: nothing moves. Weight 3 to 4 lb for a Sconce (cost-model.md assumption; log the real number). |

Total: about 26 minutes of touch time plus cures on the first units; 20 minutes once the dome caps and hubs are batched ahead.

## 3. In-wall kit assembly (the add-on bag)

| Step | Minutes | What to do |
|---|---|---|
| 1 | 2 | Cut CL2 18/2 to 8 ft. Strip 1/4" from both conductors at both ends. |
| 2 | 2 | Top end: screw-terminal MALE barrel plug (goes into the hub jack). Red (or the ribbed/marked conductor) to the terminal marked + or to the centre pin, black to -. Tighten; tug. This end passes through the 1" wall hole and the plate's centre; a 5.5 mm plug body is 10 mm wide and fits. |
| 3 | 2 | Bottom end: screw-terminal FEMALE barrel jack, same colours. The adapter's own male lead plugs into this at outlet height behind the Datacomm plate. |
| 4 | 1 | Check with J5 from the bottom end: plug the adapter into the female, J5 into the male; red LED must light. |
| 5 | 1 | Bag: cable, Arlington LV1 bracket, Datacomm 45-0001-WH plate, 10 ft pull string, the drill-size card (1" hole saw at the sconce centre, single-gang cutout from the LV1 template, 12 to 18" off the floor, same stud bay as the outlet). |

Note from inwall-parts (2026-11-10): the DC keystone coupler idea is dropped; the common 5.5 x 2.1 keystone is rated 0.5 A and the COB ring draws about 1 A. The barrel pair above replaces it.

## 4. Polarity and connector reference
- Barrel: 5.5 mm OD x 2.1 mm ID, centre POSITIVE, throughout (adapter, dimmer, hub jack, in-wall pair).
- Wire colour: red = +, black = -. If the CL2 cable is two black conductors, the ribbed or printed one is +.
- COB strip: 12 V DC; 36" of a 16.4 ft reel rated about 3 W/ft draws about 9 W = 0.75 A at 12 V. A 2 A adapter has margin for the Set's three units on one adapter if that design change is ever made (27 W would exceed a 24 W adapter; it is not assumed).
- Never splice the adapter's own cord; never put the adapter inside the wall (NEC 400.12, mounting-report.md).

## 5. Batch rhythm for 100 units
Day 1: receive CNC backplates, paint all (2 coats, racks). Day 2: inserts + pads on all (steps 2 to 3), 25 dome caps in J3 x 6 fixtures. Day 3: hubs + jacks + glue (4 to 5), strip and solder (6 to 9) on 25 units. Days 3 to 6: 25 units per day through steps 6 to 13, heat-soak the first 10 (QC-test-plan.md), ship as they pass. Two people halve the calendar.
