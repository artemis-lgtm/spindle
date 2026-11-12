# Spindle product audit (pessimist pass, 2026-11-11)

Auditor: claude-fable-5-2. Scope: the product itself. The CAD and how it mounts and works (`cad/`, `mounting-report.md`, `engineering-report.md`), parts and sourcing (`sourcing/`, `build/`), the renders as a description of the real product, and compliance (`ops/`). Nothing was sent, ordered, committed, published or signed up for. Guest instant quotes were read; nobody was contacted.

## Verdict

**Not ready to build, and not ready to sell.** The 12 in design is close and the heat-safe layout was the right call, but when I tested the things nobody had tested I found three faults that would each have stopped the first prototype on the bench: the hub could not physically be twisted onto its wall plate, the LED strip is drawn in a circle that no flat strip can follow, and the laser shop refuses to press a stud into the wall plate as drawn. All three are now fixed or worked around in the CAD and held by new gates. What is left is bigger than geometry. The parts cost at live prices is **$78.04 at 100 units, not $47.46**, so the $89 Kit loses about $20 an order before advertising, and the chrome cap has no price at 100 from anyone (the only live numbers are $121 to $156 each). The fixture has no safety listing, and the electrical code rule that applies to it is stricter than the one the notes cite. The vinyl softening temperature everyone has been quoting (55 to 60 C) is too high: the sourced figure is 48 to 54 C. Normal use is still safe on paper with about 13 K in hand. The stacked worst case is not. Nothing has been built or measured, the 7 in sconce is not buildable, and the 20 pre-sold units are very likely already inside a Federal Trade Commission shipping deadline.

## What I ran

- `cad/.venv/bin/python cad/build_all.py` before touching anything: `gates: 199 pass, 0 FAIL`.
- The same after my changes: **`gates: 225 pass, 0 FAIL`** (199 + 14 new geometry gates tagged AUDIT + 12 new document gates). All seven assemblies still report no interference.
- `cad/.venv/bin/python cad/thermal.py`: reproduces 33.1 C normal and 45.2 C stacked worst case.
- A motion check the build never had: the hub rotated through the 20 degree twist and lifted through the push-on, intersected with the plate, studs and nuts at 13 positions.
- A sensitivity run of the heat model with one assumption changed at a time (table below and in `cad/THERMAL.md`).
- Four research passes (compliance, live sourcing with guest quotes, render review, engineering data). Their source links are in the sections below. I opened the two screenshots that carry the most weight myself (the cap price table and the laser shop's stud refusal).

## Findings, ranked

### Safety

**S1. The fixture is unlisted and the rule is stricter than `ops/safety.md` said.**
Evidence: the notes cite NEC 410.6. The rule that fits a 12 V product is NEC 411: lighting at 30 V or less must be a listed system or built only from listed parts, and being Class 2 does not exempt it (secondary source, the NFPA text was not readable). A wood disc on a printed hub with our own wiring is neither. Selling it is not a federal offence, but Los Angeles (LAMC 93.0402) and North Carolina (GS 66-25) require listing or lab evaluation of electrical equipment. The standard a lab would use is UL 2108 with UL 8750. Sources in `ops/safety.md`, audit section.
Fix applied: `ops/safety.md` corrected and extended. **Decision needed:** the compliance path (section below), and whether to ship to Los Angeles and North Carolina before a listing.

**S2. The heat margin is thinner than stated.**
Evidence: `cad/THERMAL.md` and four other files said vinyl softens at 55 to 60 C. US patent 3,975,321, Table III, puts standard record compound at 48 to 50 C for loss of stiffness and 52 to 54 C glass transition. The model also leaves out the warm air rising behind the backplate; a chimney estimate gives 4 to 7 K of warmer air at 4 W and the model says the record takes 0.31 K per 1 K of it. With that, the stacked worst case goes from 45.2 C to 48.7 C, or 51.0 C with an inefficient strip. And the "wrong 6 W strip" in the worst case is not hypothetical: `sourcing/sample-run-plan.md` orders the HitLights COB reel, which is 10 W per metre, 7 W on this ring.
Fix applied: `THERMAL.md` corrected with the source and a sensitivity table; a gate now fails the build if the old sentence comes back; the assembly procedure rejects any ring that draws more than 0.42 A at 12.0 V (5 W); the sample plan is bannered "do not order"; `build/QC-test-plan.md` test T1 is a full two-hour soak with ten thermocouple positions and pass limits. **Decision needed:** none until T1 is run. Nothing ships before it.

**S3. A 24 V adapter fits the same jack and nothing stops it.**
Evidence: 5.5 x 2.1 mm is the commonest barrel size for both 12 V and 24 V LED supplies. On 24 V a 12 V strip draws several times its power; the model puts the strip near 76 C and rising within minutes and vendors call it a fire hazard (hitlights.com page in `ops/safety.md`). The only guard is a label.
Options: (a) label only, as now, free; (b) a resettable fuse (0.5 A hold) plus a 15 V clamp diode soldered into the hub splice, about $0.40 and two minutes a unit, which also covers a shorted strip; (c) a less common plug size (for example 5.5 x 2.5 mm) on the pigtail and the supplied adapter, free, but the in-wall barrel pairs must match. **Recommendation: (b).** Test T1 run C checks whichever is chosen.

**S4. The wall mount depends on parts and steps that were left vague.**
Evidence, hand calculation from the CAD: the hung parts weigh about 1.0 kg (2.2 lb), centre of gravity 30 mm off the wall, so the static load on two anchors is under 1 lb each. That is not the risk. A 10 lb outward tug on the backplate rim, which is what taking it down wrongly looks like, puts about 18 lb on each anchor, and the BOM said "hardware store" anchors. A good plastic anchor (Toggler Alligator, 85 lb ultimate tension in 1/2 in drywall per a retailer listing; the maker's table was not opened) has a working load near 21 lb at the usual 4 to 1. A generic ribbed anchor does not. Second: unscrewing the cap turns the same way that unlocks the hub. Only the set screw stops it, and the set screw sits 70 mm in under the backplate at about 6:40, in a 21 mm gap, right beside the LED strip. The BOM supplied a 1.5 mm L key whose long arm is about 45 mm. It cannot reach. People will skip the screw.
Fix applied: BOM names the anchor class and replaces the L key with a 100 mm straight hex driver; tests T2 and T3 added (pull test, 50 hang cycles, a stranger fitting the set screw in under two minutes, and what happens when the cap is unscrewed with the set screw out). **Decision needed after T3:** if the hub unlocks with the screw out, add a snap detent to the twist-lock so it cannot unlock without the screw. That is a hub change and was not made.

**S5. Things the safety card must say, and one legal trap.** Direct sun on a black record is worse than anything the LEDs do. Not above a radiator. Not in a closed niche. Exterior walls and walls with fire blocking stop the in-wall cable. A dimmer with a coin-cell remote brings Reese's Law labelling; use the knob dimmer. A small maker of recycled-record products was hit with a Prop 65 lead notice in 2015 and paid $24,500 despite the small-business exemption. All in `ops/safety.md`.

**S6. The 20 pre-sold units.** Under 16 CFR 435 they must ship within the time promised, or within 30 days of payment if none was promised. The cap alone is two to three weeks after an order that cannot yet be placed. A delay notice with a right to cancel is almost certainly owed. `ops/legal.md` has the rule. **Needs from Austin: who the 20 are, when each paid, how much, and what they were told.**

### Will it work

**W1. The hub could not be hung on the wall plate. FIXED.**
Evidence: every interference check in the build ran with the hub already locked. The wall plate has a bent tab that stands 12 mm tall. The hub's pocket for it was 10 mm wide, at the locked position only. To hang the sconce the hub goes on 20 degrees off and twists home, and for that whole twist the tab was inside solid plastic: 114 mm3 of overlap at every step, measured on the solids. The first prototype would not have gone on the wall.
Fix applied: `cad/sconce_cad.py`, the tab pocket is now an arc from 224 to 256 degrees; RS-HUB-01 is **rev C**. New gates check the motion at 13 positions and prove the check catches the old hub.

**W2. The LED strip is drawn as a circle that no flat strip can follow. Worked around, decision needed.**
Evidence: a flat LED strip bends the easy way (round a drum), not sideways in its own plane. `engineering-report.md` said so on 11/9 and gave it as the reason for the rim mount. When the strip moved to the back face it was modelled as a flat circle 115 mm from the centre and the BOM said "700 mm, one piece".
Options: (a) seven straight 100 mm pieces laid as a seven-sided ring with six jumpers. I proved in the CAD that this fits the existing aluminium ring and misses the four screws (2.4 mm to the nearest screw head, 1.8 mm inside the ring edge, no LED within 8.8 mm of the backplate rim, 9.8 mm between pieces for the jumper). It works with the listed strip already identified. It adds about 10 minutes of soldering a unit. (b) An "S-shape" strip made to bend sideways: one piece, no jumpers, but no listed 4 W part has been found. **Recommendation: (a) for prototypes, look for (b) for production.** Fix applied: constants and gates in the CAD, `build/assembly-SOP.md` step 6, BOM lines. The strip solid in the model is still a circle (the heat model uses it).

**W3. The laser shop refused to press a stud into the wall plate as drawn. FIXED and re-quoted.**
Evidence: SendCutSend guest quote, "Hole Collision Issue, 1 hole affected, Hardware" (screenshot `sourcing/quotes-2026-11-11/audit-evening/scs_plate_plating.png`). The stud hole at 75 degrees was 6.83 mm from the end of an arc slot; the stud maker (PEM, FH-832) requires 7.14 mm.
Fix applied: RS-WP-01 **rev B**: that slot pair is +/-8 degrees instead of +/-10, giving 7.36 mm, probed on the solid by a gate. Stud holes 4.17 mm (were 4.22, the very top of PEM's band). I re-uploaded the rev B file the same evening: SendCutSend accepted the bend and all three studs with no collision ($6.40 each at 100 in galvanized, arrives in 8 days; screenshots `sourcing/quotes-2026-11-11/audit-evening/scs_plate_revB_*.png`). The plate still levels 8 degrees on a single-gang box and 10 on a round box. `mounting-report.md` still says "about +/-9 degrees" (not my file to edit).

**W4. The threaded insert is the wrong family for MDF.**
Evidence: E-Z Lok's own guide lists the knife-thread insert (400-4) for hardwoods and a different, hex-drive type for "soft woods, plywood, MDF". Its pull-out table has no MDF column (535 lb in spruce). Pull-out is not the worry at these loads; turning is. Unscrewing a tight cap puts loosening torque straight on the insert.
Fix applied: glue step kept in the procedure; test T4 (300 cycles, a stuck-cap test, 200 N pull). **Decision if T4 fails:** an insert or tee nut with a flange on the BACK face, which the cap pulls tighter instead of out. The hub's centre relief would need to grow to take the flange.

**W5. The 7 in sconce cannot be built.** Four separate reasons: the halo has no heat-safe design (known); `build/BOM.md` prices a 4 in hub with a keyhole plate while the CAD builds it on the 5 in hub and steel plate; that keyhole plate is sold out with no second source; and the 7 in cap has a 37.6 mm boss that only fits big-hole 45s, so a small-hole 7 in record (most UK and many modern singles) sits on the boss with no washer under it. Options below.

**W6. What it looks like from the side, and at 6 o'clock.** From the CAD: standing beside the wall, the bare edge of the aluminium and cork rings comes into view under the backplate rim at 64.5 degrees off straight-on, and the corners of the seven-piece strip at 63.4 degrees. In a hallway that is the normal view. On a surface-cord install the connector hangs 8 to 10 mm in front of the strip at 6 o'clock, and the strip has a gap there too. The approved pictures were lit from 124 mm with an extra rim strip; the product lights from 115 mm with none, so the real halo will be narrower and dimmer than the pictures. None of this can be judged without a prototype (test T8). Cheap fix if the metal shows: paint the ring's outer edge black.

**W7. Smaller items.** The only listed 4 W strip with a price is 2900 to 3200K, not the 2700K in the copy. The dimmer's switching frequency is unknown; cheap ones flicker on camera and make adapters whine (test T9). Standard MDF grows about 0.3% between 50 and 80% humidity, 0.8 mm across the disc: every routed surface must be painted (test T6). A thin record may cup slightly when warm from the temperature difference across it; my rough estimate says a 120 g record could show it in the worst case, which is why T1 includes a flatness check hot and cold. The shipping box found is single wall, the BOM says double wall, and the 55 g brass cap must not ride loose next to a record (test T7).

**W8. The lit cap's centre contact has never been built.** Options below.

### Cost

**C1. Parts are $78.04 at 100, not $47.46, and the $89 Kit loses money.**
Evidence: `build/BOM.md` section 2, every line re-opened on 2026-11-11. The old total priced a glued shell for the cap ($3.40), a guessed strip ($2.50), a hoped-for bulk adapter ($8.50), a sale-price dimmer as if 100 could be bought (7 in stock), an out-of-stock panel jack the design no longer uses, and left two washers out. At live prices: cap $15.00 (a placeholder), strip $11.25, adapter $12.99, plate with bend and studs $6.40. Result at 100 units, before advertising: **$89 Kit: minus $19.90. $99 Kit: about minus $10. $129 Sconce: plus $12.77. $179 Sconce: plus $33.32.** The Kit needs to be about $125 to clear $15. Cash for the first 100: about $8,200, not $5,200.
Fix applied: `cost-model.py`, `BOM.md`, `BOM.csv`, `cost-model.csv`, `cost-model.md` all rewritten and gated to agree. With a $10 cap, an $8.50 adapter and the cheaper Armacost strip (wattage unverified) the total is about $62. It does not get back to $47.

**C2. The cap is the unknown that decides everything.** PCBWay guest pre-quote, brass with chrome: $155.93 at 1, $131.70 at 10, $121.36 at 50, "customized quote" at 100. JLCCNC polished brass without plating: $42.72 at 1, $32.81 at 10. No price at 100 exists. Emailed quotes are normally far below instant pre-quotes, but nobody has been asked: all 13 RFQ drafts are unsent.

**C3. The 20 pre-sold units at 20-unit prices cost about $211 each in parts with real caps** ($132 of it the cap). With a $4.50 stock chrome cap as a declared stand-in, about $84.

**C4. Not in the model at all:** a safety listing ($5,000 to $15,000, published figures), product liability insurance ($700 to $3,000 a year), test equipment (about $200 to $300), and the extra labour (40 minutes a unit, not 25).

### Schedule

**T1. The chrome cap is the long pole:** 8 to 10 business days to make plus 2 to 4 to ship, after a quote that does not exist. Two to three weeks at best. The "3 week" sample plan has no slack for it. Stand-in caps let testing start in about 8 days.
**T2. Second: the die-cut felt and PET washers** have no vendor; 5 to 7 business days after a quote and tooling. Hand punches remove the wait for prototypes.
**T3. The wall plate** ships in about a week. Only the rev B file can be ordered.
**T4. A listing, if wanted, is 6 to 12 weeks.**
**T5. Nothing has been built.** Every test in the QC plan is still ahead.

## Options where I was told not to redesign

### The 7 in sconce

| Option | What | Numbers | For | Against |
|---|---|---|---|---|
| A. Smaller hub, same heat-safe stack | A 4 in (101.6 mm) hub, which the BOM already assumes. Ring from 53 to 72.85 mm radius (19.85 mm wide), strip centred at 66 mm, four screws at 56.5 mm | Eight 50 mm strip pieces fit as an octagon (corners at 71.3 mm, inside the ring edge). About 400 mm of strip, about 1.9 W | Same construction as the 12 in; LEDs cannot see the record | New hub, new small rings, needs its own mount (the 4 in steel plate does not fit inside a 4 in hub), needs its own heat run |
| B. Keep the 5 in hub, 5 or 6 mm strip | Ring 8.35 mm wide in the 9.35 mm band | 1.2 to 1.7 mm each side of the strip, no room for a screw | No new hub | Glue only, on painted MDF; a straight-piece layout does not fit (needs 9.6 mm); only an S-shape strip would work |
| C. Keep the rim strip, narrow and low power, on the wall-side half of the rim | 5 mm strip, about 3 W per metre | Old rim layout at 4.8 W per metre: record +4.9 K normal, 49.6 C worst. Scaled to 3 W per metre: about +3 K normal, about 44 C worst | No new parts; a rim strip bends the easy way | LEDs still face the record's overhang 9 mm away; worst case not modelled, only scaled |
| D. Do not sell the 7 in or the Set in the first batch | | | Costs nothing, removes four open problems | No Set at launch |

**Recommendation: D now, then A.** Also decide whether the 7 in is "big-hole 45s only" or ships with the 12 in style cap and a small felt ring for small-hole records (the two caps already land at the same depth).

### The lit cap's centre contact

| Option | What | Cost and risk |
|---|---|---|
| 1. Build it as designed and bench-test | Custom gold plunger, catalogue spring, PEEK guard tube, 4.9 mm travel | Three tiny custom parts, estimated $10 to $20 a unit at 100. Unproven. Pass test: contact resistance under 0.1 ohm and no flicker over 500 record swaps, thin and thick records |
| 2. Replace plunger and spring with a stock leaf-spring contact on the hub board | A stamped battery-style spring finger has 3 to 6 mm of travel as a stock part; the PEEK tube stays as the hard stop | Under $1, one stock part instead of two custom ones. No part number picked (not checked). Needs a small redesign of the hub module |
| 3. Launch with the plain cap only | Hub rev C already has the 9.1 mm centre relief, so a lit cap can be added later without changing the hub or backplate | Free. The lit cap becomes a second-batch upsell |

**Recommendation: 3 now, test 1 on the bench, fall back to 2 if the plunger sticks or the price is silly.**

## Heat: sensitivity table

Final geometry, one assumption changed at a time. "Plume" is warm air in the gap behind the backplate, which `thermal.py` leaves out. Limits to stay under: 48 C (stiffness starts to go) and 52 C (glass transition).

| Case | Record hottest spot | Rise | Strip |
|---|---|---|---|
| Baseline in `THERMAL.md`: 4 W, 30 C room | 33.1 C | +3.1 K | 39.2 C |
| Cheap strip, only 20% of power leaves as light | 33.9 C | +3.9 K | 41.3 C |
| All light absorbed behind the plate (upper bound) | 34.8 C | +4.8 K | 44.1 C |
| Stray light on the record's overhang 5 times larger | 33.2 C | +3.2 K | 39.2 C |
| Gap film coefficient quartered (niche, shelf above, corner) | 35.6 C | +5.6 K | 45.6 C |
| All film coefficients halved (dead air) | 36.8 C | +6.8 K | 44.1 C |
| Plume, low estimate (gap air +3 K) | 33.9 C | +3.9 K | 41.0 C |
| Plume, high estimate (gap air +6 K) | 34.7 C | +4.7 K | 42.9 C |
| Hot wall behind (gap air +10 K: radiator below, sunlit or attic-side wall) | 35.8 C | +5.8 K | 45.4 C |
| The sample plan's strip: 7 W | 35.5 C | +5.5 K | 46.0 C |
| 7 W strip with its plume | 38.2 C | +8.2 K | 52.5 C |
| 35 C room, 4 W, plume | 39.7 C | +4.7 K | 47.9 C |
| `THERMAL.md` stacked worst case: 6 W, films halved, 35 C room | 45.2 C | +10.2 K | 56.2 C |
| Same, plus plume (gap air +12 K) | **48.7 C** | +13.7 K | 62.4 C |
| Same, plus plume, plus cheap strip | **51.0 C** | +16.0 K | 67.3 C |
| 12 V strip on a 24 V adapter, first minutes (about 16 W) | 46.5 C | +16.5 K | 75.9 C and rising |

**Is the 12 in safe on paper?** In normal use, yes: about 34 to 35 C in a 30 C room once the plume is counted, 13 K or more under the lowest limit. In the stacked worst case, no: it lands on the limit. The film coefficients (8 and 6 W/m2K) are ordinary textbook values for still indoor air; the 35% light fraction matters little; the plume and the strip wattage matter most. **The one measurement that proves it:** a thermocouple on the back of the record, 114 mm from the centre at 12 o'clock, after two hours at full brightness on a real wall in still air. Pass: 6 K or less above the room.

## Compliance path

How comparable products handle it: the record-display lights found either avoid mains entirely (Sharper Image lighted album frame, 3 AA batteries; Vylumi record backlight, USB) or, like 12 V neon signs, lean on a "UL-listed power supply" claim for the adapter only. No product was found that puts a real record on a mains-adapter LED fixture with a fixture listing, and no warping reports were found for the battery and USB ones. Links: sharperimage.com/products/lighted-album-cover-frame, vylumi.com, neonific.com/products/retro-disc.

| Path | What | Cost | Time | Good for |
|---|---|---|---|---|
| Cheapest defensible | Plug-in only (drop the hardwired version). Say "listed Class 2 adapter" and nothing more about the fixture. In-wall copy becomes "Class 2 low-voltage wiring, check your local code". Verify the adapter's listing file, level VI mark and FCC statement. Knob dimmer, no coin-cell remote. Run and keep the heat soak and pull tests. Insurance with electrical cover confirmed in writing. Prop 65 short-form warning on California orders. No shipments to Los Angeles or North Carolina. Serial numbers and lot records. Delay notices to the 20 buyers | $1,500 to $4,000 (insurance, test gear, an hour of a lawyer) | 2 to 4 weeks | The first 100 from our own site |
| Proper | All of the above, plus an ETL or QAI listing of the fixture with its named adapter to UL 2108 and UL 8750, lit cap included if it will ever be sold | $7,000 to $18,000 in year one; about $3,500 a year after (published figures, not quotes) | 6 to 12 weeks | Amazon, wholesale, any hardwired version, Los Angeles, peace of mind |

Amazon, Etsy, Walmart and Wayfair policy pages could not be opened (login or 403). A secondary summary says Amazon wants a test report from an accredited lab for decorative lighting. Treat marketplace sale as needing the proper path until someone logs in and reads the real requirement.

## Sourcing: live check, 2026-11-11

Full table with every link: `build/BOM.md` section 2. Evidence and screenshots: `sourcing/quotes-2026-11-11/README.md` and `audit-evening/`.

| Part | Old BOM at 100 | Live at 100 | Second source | Lead time | Verdict |
|---|---|---|---|---|---|
| Chrome cap | $3.40 (wrong part) | no price; $121.36 at 50 | JLCCNC, no plating, $32.81 at 10 | 2 to 3 weeks | **Long pole. Unknown cost** |
| LED strip | $2.50 est | $11.25 (Ecolocity, ETL, 1.46 W/ft; 2900 to 3200K) | Armacost UL 2700K, $4.28, wattage unknown | stock | Planned HitLights reel is over the heat cap |
| Adapter | $8.50 est | $12.99 | GXILEE with dimmer, $13.88 | stock | No bulk price exists |
| Dimmer | $2.50 est | $3.99 sale, 7 in stock | Super Bright LEDs $7.99, out of stock | stock | Cannot buy 100 today |
| Pigtail | $2.36 (panel jack, out of stock) | $4.00 at 1; bulk not checked | none found | stock | Old line priced the wrong part |
| Wall plate + 3 studs | $4.40 est | $6.40 galvanized; $8.69 black powder (rev B file) | Westinghouse crossbar $3.73 as a stand-in | about 8 days | Rev B accepted with studs |
| Aluminium ring | $7.38 | $7.38 (re-confirmed) | none | about 5 days | Matches |
| Cork | $1.89 | $1.89 (roll $66; page says both 1/16 in and 2 mm; no adhesive shown) | The Cork Store, 1.5 mm, peel-and-stick option, about $1.00 | stock | Measure on arrival |
| Insert | $1.70 | $1.70 | ezlok.com (price needs login) | stock | Old "$17.63 per 10" was the drive tool |
| Felt pads | $0.42 | $0.42 | none found | stock | Single source |
| Felt washer, centre ring, PET washer | $0.16 (two not counted) | $0.65 est | CS Hyde, Strouse: no published price | 5 to 7 business days | No vendor |
| Ring screws | $0.12 est | $0.12 (Tanner Bolt, $2.90 per 100) | hardware store | stock | Head 5.56 x 2.03 mm per the standard table: CAD's 5.6 x 2.1 is safe. Thread diameters not found |
| Box | $3.50 est | box $1.48; foam and sleeve est | none | next day | Single wall, not double |
| Backplate, hub | $4.50, $3.00 est | not checked | | 1 to 2 weeks | No quote from any shop |
| In-wall kit | $6.47 | LV1 bracket $1.80 and recessed plate $2.97 confirmed; cable $33.42 per 100 ft | Sunco brackets; JacobsParts plugs | plugs arrive 11/19 to 11/27 | PowerBridge add-on is out of stock |

Estimates that move the 100-unit total by more than $0.50: cap (+$11.60), strip (+$8.75), adapter (+$4.49), wall plate, studs and nuts (+$2.22 galvanized, +$4.51 powder), set screw kit (+$1.60), dimmer (+$1.49). Still estimates and each worth more than $0.50 either way: backplate ($4.50), hub ($3.00), packaging foam and sleeve (about $2.00), cap.

## Renders: where the pictures show what the product does not do

Full re-render list: `renders-final/README.md` (audit section).

| Images | What is shown that is not true | Level |
|---|---|---|
| `renders-zep/*` (8) | Real Atlantic label, band name, the four symbols, producer credit, track list | Misleading, and a legal problem |
| `swap1_*`, `swap2_*`, `swap_triptych` | Record stays on the wall with the cap off; LED dots on the backplate rim; captions "lift the record off" a post; cap has no stud; no clear washer | Misleading |
| `flatlay_*` | A loose post that does not exist; no dimmer; no clear washer; a second chrome cap instead of the 45 adapter; rim strip on the backplate; wrong wall plate; card says set screw at 6 o'clock (it is at about 6:40) | Misleading |
| `install_*` | "4 screws" (the kit has 2 screws and 2 anchors); shows in-wall cable and a wall jack that are not in the box; no dimmer | Misleading labels |
| `single7_*`, `set_*`, `studio_*`, `band_set_*` | 7 in units with the 12 in halo; the 7 in halo is not designed. No cords on any | Misleading |
| `hero_brass_*`, `hero_black_*`, `bar_*`, `close_off` | Cap finishes with no real part. Black shown with a chrome bezel that exists nowhere | Misleading |
| `bedroom_*` | A 4 W strip lighting a whole room | Misleading |
| `hero_chrome_*`, `living_*`, `swap3_*`, `band_row_wide`, `band_grid_wide` | Halo wider and brighter than a 4 W ring at 115 mm will make; perfectly even, no gap at 6 o'clock; no cord (so in-wall installs only) | Look may differ |
| `renders-labellight/close_on`, `ab_close`, `band_grid_labellight` | Lit cap drawn with a wide skirt, about 54% of the label (real: 38 mm on a 100 mm label); a visible white crescent of light source | Misleading geometry |
| `macro_*` | Dome reads taller than the real 10 mm; a felt ring shows where the clear washer would | Minor |
| Three labelled drawings in `renders-exploded/` | Match the CAD. The plain exploded view has no callout for the insert or the screws; the heat-safe drawing calls a stud a "post" in one label | Fine, two small fixes |
| Every image | None shows the 1 in gap, the 5 in hub, or the side view | Missing |

Safe to use today as they are: `macro_*` and the three labelled drawings. Usable with a "rendering, real glow may differ" line until a photo exists: `hero_chrome_*`, `swap3_*`, `living_*`.

## What I changed

CAD (`cad/`): `sconce_cad.py` (hub tab pocket arc, plate slot angle, stud hole size, straight-strip layout constants), `gates.py` (14 geometry gates tagged AUDIT, 12 document gates, updated BOM total gates), `build_all.py` (hub rev C, plate rev B, RFQ text), `drawings.py`, `dxf_out.py`; everything `build_all.py` regenerates (STEP, STL, DXF, drawings, RFQ packets, `checks.md`); `THERMAL.md`, `README.md`, `FIXES-heat-layout.md` (correction notes).

Build (`build/`): `assembly-SOP.md`, `QC-test-plan.md`, `sample-kit-shopping-list.md`, `cost-model.md` rewritten; `BOM.md` section 2, 4, 6, 7 rewritten; `cost-model.py` re-priced, which regenerates `BOM.csv` and `cost-model.csv`; `README.md`. The versions they replace are in `build/SUPERSEDED/`.

Sourcing: `quotes-2026-11-11/README.md` (new quotes), `quotes-2026-11-11/audit-evening/` (11 screenshots), banner on `sample-run-plan.md`.

Ops: audit sections added to `ops/safety.md` and `ops/legal.md`.

Renders: audit section and re-render list in `renders-final/README.md`. No image was re-rendered.

Not touched: `site/`, `marketing/`, `mounting-report.md`, `engineering-report.md`, `START-HERE.html`, `PARTS-SIMPLE.html`, `NOTES.md`. Several of those now disagree with the CAD and the BOM: any "$47" or "$38" parts figure, "vinyl softens at 55 to 60 C", "+/-9 degrees" of levelling, "1.5 mm L key", "legal everywhere" in-wall claims, 2700K.

## What I could not verify

- Anything physical. No part exists. Every temperature, load and fit is a calculation.
- A cap price at 100 pieces from anyone. Xometry, Protolabs Network and RapidDirect guest pricing (upload did not advance).
- Toggler's own load table and safety factor; any pull-out figure for a flangeless anchor; E-Z Lok data in MDF; brass thread wear over cycles; #4 screw thread diameters.
- Record warp over time at 35 to 45 C: Library of Congress, National Archives and IASA guidance pages did not load. PVC creep data by temperature: not found. The softening figures rest on one patent.
- The plume: my chimney estimate is a hand calculation, not a flow model.
- Whether a thin record cups when warm: a rough plate-buckling estimate only.
- Strip details: the Armacost strip's wattage, any listed S-shape strip, the real adhesive on any strip, strip thickness (1.6 mm is assumed).
- Dimmer switching frequency, whine, radio noise. The adapter's listing file number.
- Home Depot MDF, eBay adapters, Monoprice cable, McMaster, Zoro, Digi-Key (blocked or not opened).
- NFPA code text, Amazon, Etsy, Walmart and Wayfair policies, fcc.gov and ftc.gov guidance pages, Chicago and New York City code, any lab or insurance quote.
- The aluminium-backplate variants and the lit cap's heat. Not modelled, not audited beyond noting they are open.
- `renders-lit/`, the halo video, and the images under `site/img/` were not reviewed.
- Who the 20 buyers are and what they were promised.

## The five ways this fails in a customer's home

1. **It comes off the wall.** The customer skips the set screw because they cannot reach it, later unscrews a tight cap to change the record, the hub turns with it and unlocks, and a 1 kg disc with a record on it drops. Or they pull it straight off the wall and the anchors come with it.
2. **The record warps and they blame the light.** A sunny wall, a spot above a radiator, a tight niche, or a unit built with too strong a strip. The record is theirs, sometimes valuable, and "we calculated 33 C" is not a defence without a measurement.
3. **Someone plugs in the wrong adapter.** A 24 V supply from a drawer fits the jack. The strip cooks within minutes, on a wooden disc, on a wall.
4. **The in-wall install defeats them.** Fire blocking or insulation stops the cable, or an inspector or landlord objects to an unlisted fixture wired through the wall, and the default story becomes a refund.
5. **It does not look like the pictures.** A narrower, dimmer halo than the renders, a cord nobody was shown, a dark notch at 6 o'clock, bright metal visible from the hallway, a hum or flicker from a $4 dimmer. Returned, with a review.

## Decisions for Austin

1. Price: the $89 Kit loses money. Raise it (about $125), drop it, or accept a loss leader knowingly.
2. Cap: send the RFQ (nothing can be priced without it), and say whether the first units may ship with a declared stand-in cap.
3. Strip: seven straight pieces now, or wait for an S-shape strip.
4. Compliance path: cheapest defensible or proper. And Los Angeles and North Carolina.
5. The 20 buyers: the list, the dates, what they were told. Delay notices.
6. 7 in and Set: out of the first batch (recommended) or pick an option.
7. Lit cap: second batch (recommended).
8. 24 V protection in the hub: yes (recommended) or label only.
9. Approve about $900 to $1,500 for three prototypes and the test gear, so that test T1 can be run.
