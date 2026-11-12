# Assembly procedure: 12 in Spindle sconce, MDF backplate, plain chrome cap

Rewritten 2026-11-11 by the product audit (`../audits/AUDIT-product.md`) to match the canonical CAD: backplate RS-BP-12-MDF rev C, hub RS-HUB-01 rev C, wall plate RS-WP-01 rev B, cap RS-CAP-12 rev D, aluminium ring RS-HR-12 rev A, cork ring RS-CK-12 rev A. The procedure from 2026-11-10 (glued dome cap, a jack fixed in the hub, LED strip on the edge of the backplate) is in `SUPERSEDED/assembly-SOP-2026-11-10.md` and must not be used.

Nothing has been built yet. Every time below is an estimate. The first three units are prototypes and go through `QC-test-plan.md` section 4 before anything is sold.

Not covered here, because the design is not settled: the 7 in sconce, the lit cap, the aluminium-backplate variants.

## Before you start: two decisions this procedure assumes

1. **The LED strip is laid as seven straight pieces.** A flat LED strip cannot bend sideways into a circle on a flat ring. This procedure uses seven 100 mm pieces of ordinary 8 mm strip laid as a seven-sided ring and joined with short jumpers. The CAD proves that fits the aluminium ring and misses the four screws (gates tagged AUDIT in `../cad/checks.md`). If an S-shape strip that bends sideways is chosen instead, step 6 becomes one piece and no jumpers.
2. **Strip power is 5 W or less at 12.0 V.** The heat study assumes 4 W and treats 6 W as the wrong part. Do not use the HitLights COB reel named in the old sample plan: it is 10 W per metre, which is 7 W on this ring.

## Tools and jigs

| Item | What it is for |
|---|---|
| Bench supply, 12.0 V, with a current display (or a 12 V adapter and a multimeter in series) | Step 6 and step 9 power checks |
| Soldering iron, 60/40 or lead-free solder, 22 AWG red/black wire, 3 mm and 5 mm heat-shrink | Strip jumpers, leads, splice |
| M3 heat-set insert tip for the iron | Hub set-screw insert |
| Isopropyl alcohol and lint-free wipes | Degrease the aluminium ring before the strip goes on |
| J1 strip template: a 260 mm card or acrylic ring printed with the seven-sided layout (each side 100 mm, its middle 114 mm from the centre, one corner at 6 o'clock) and the four screw holes | Lays the strip pieces in the right place |
| J2 nut gauge: a 7.2 mm thick slotted shim | Sets the three lock nuts on the wall plate studs |
| J3 master wall plate screwed to a board | Trial hang of every hub |
| Circle cutter and a 4 mm hollow punch (only if cork rings are cut in-house) | Cork ring |
| #1 Phillips, #2 Phillips, 1.5 mm hex driver | Screws |
| Thin CA glue | Insert bore |

## Steps

| # | Step | Min | How | Check before moving on |
|---|---|---|---|---|
| 1 | Backplate in | 1 | Take a painted RS-BP-12-MDF rev C. Front face has six shallow felt targets and a scored circle round the centre hole. Back face has one short channel (60 to 97 mm from the centre, toward 6 o'clock) and four small blind holes. The rim is a plain square edge. | No step cut into the rim (that is the old rev B). Paint covers every routed surface, including the channel, the targets and the edge. Raw MDF anywhere = back to paint. |
| 2 | Threaded insert | 2 | Wick thin CA into the centre bore, wait 30 seconds, drive the E-Z Lok 400-4 in from the FRONT until it is flush to 0.2 mm below the front face. Let it cure 10 minutes before any screw goes in. | Flush or just below. Not proud (a proud insert dishes the record). Thread clean: the cap spins in by fingers. |
| 3 | Felt | 2 | Six 1/2 in felt pads into the six targets. Centre felt ring (1-1/4 x 3/8 x 1/16 in) inside the scored circle, round the insert. | All seven pieces seated flat, none overhanging its target. |
| 4 | Hub prep | 4 | Heat-set the M3 insert into the hole in the hub rim (about 220 C, flush). Thread the M3 x 12 set screw in from outside until its tip is flush with the inside of the tab pocket (not into it). Fix the pigtail in the rear pocket with the nylon P-clip and one #4 x 3/8 screw: 150 mm free beyond the clip, bare ends up through the 6.5 mm hole into the front splice cavity. Stick the "12 V DC ONLY" label beside the cord channel. | Tug the pigtail with about 2 kg: it must not move in the clip. Set screw turns freely. |
| 5 | Hub to backplate | 3 | Hub front face to the backplate back face, hub's front lead channel at 6 o'clock lined up with the backplate's back channel. Three #8 x 1 in flat-head wood screws from the FRONT of the backplate into the hub pilots, heads flush in their countersinks. Snug only: the pilots are in printed plastic. No glue is needed and wood glue does not bond PETG. | Heads flush or below (a proud head touches the record). Hub does not rock. |
| 6 | Halo ring, on the bench | 12 | Wipe the aluminium ring with alcohol. Lay the cork ring under it, holes lined up (if the cork has an adhesive face, stick it to the aluminium). Lay template J1 on the aluminium. Cut seven 100 mm strip pieces on the cut marks. Peel and press each piece onto the aluminium on a template side, LEDs up, all with + on the same edge, 30 seconds of firm thumb pressure along each piece. Solder six jumper pairs (about 15 mm, + to + and - to -) across six of the seven corners. Leave the corner at 6 o'clock open: solder the red and black leads (250 mm) to the two pads at one side of that corner. Slide 5 mm heat-shrink over each lead where it will cross the ring's inner edge. | Power the ring at 12.0 V: all seven pieces light, even colour. **Current between 0.20 and 0.42 A (2.4 to 5 W). Above 0.42 A: wrong strip, reject.** No bare copper within 2 mm of a screw hole. |
| 7 | Ring to backplate | 3 | Ring onto the back of the backplate, cork against the wood, strip facing away from the wood, open corner at 6 o'clock. Four #4 x 3/8 pan-head screws through the aluminium and cork into the four blind holes. Stop when the head touches: the thread is in MDF and strips easily. | Look at the FRONT face: no bulge or crack over any of the four screws. Ring does not rattle. Screw heads do not touch the strip. |
| 8 | Leads and splice | 5 | Run the two leads inward over the ring's inner edge (heat-shrink at the edge), into the backplate's back channel, into the hub's front channel, to the splice cavity. Solder to the pigtail (red to centre pin). Heat-shrink each joint, then one sleeve over both. Press into the cavity. | Continuity check, no short between + and - (meter). Polarity: centre positive at the jack. |
| 9 | Burn-in | 2 + 30 unattended | Plug in the kit's own adapter and dimmer. Run at full for 30 minutes. | Still lit, no dark piece, no smell. Touch the aluminium ring beside the strip: warm, not hot (about 40 C). Dimmer sweeps smoothly with no flicker to the eye and no whine from the adapter at arm's length. |
| 10 | Trial hang | 2 | Offer the hub to master plate J3 with the unit turned about 20 degrees anticlockwise (the top of the unit at about 11 o'clock), push it flat, twist CLOCKWISE until it stops. Drive the set screw in with the straight hex driver until it stops in the plate tab. Back the screw out, twist off. | It goes on, turns the full 20 degrees without scraping, the set screw finds the tab hole, and the unit cannot be turned back by hand with the screw in. Leave the set screw backed out flush. |
| 11 | Wall plate kit | 2 | Wall plate arrives with its three studs pressed in. Spin a lock nut onto each stud down to gauge J2 (7.2 mm between plate and nut). Bag: plate, two #8 x 1-1/4 screws, two named drywall anchors, the 1.5 mm x 100 mm straight hex driver. | Three nuts at gauge height. An L-shaped hex key is not a substitute: it cannot reach the set screw. |
| 12 | Cap | 1 | Felt washer into the recess under the chrome cap. Bag the cap with one clear PET washer. | Stud thread clean, cap spins into a test insert by fingers. No chrome flakes on the thread. |
| 13 | Record (Sconce only) | 4 | Record on the six pads, label out. PET washer on the label, matte side to the paper. Cap through the washer and the record into the insert, finger tight. | Record sits flat on all six pads (slide a strip of paper under each pad position: it should drag). Cap stops firmly. Record does not rattle when the unit is shaken. For shipping, take the record off again: it ships in its own sleeve, not clamped. |
| 14 | Label and final check | 2 | Rating label on the hub: "Spindle. 12 V DC, 0.5 A max. Use only the supplied Class 2 adapter. Indoor, dry locations only." plus a serial number and build date. Run the per-unit checklist in `QC-test-plan.md` section 3. | Checklist signed. |
| 15 | Pack | 3 | See `QC-test-plan.md` test T7 for the pack that passed the drop test. Cap in its own foam pocket, never loose. | |

Total: about 40 minutes of hands-on time a unit for the first units, about 32 once jigged, plus the unattended burn-in. A Sconce adds step 13.

## Rework and scrap rules

- A screw that spins in the MDF (step 7): do not glue it and ship. Fill with CA and MDF dust, re-drill 2.2 mm, or scrap the backplate.
- A strip piece that lifts at an end after burn-in: replace the piece; do not press it back.
- Any unit over 0.42 A at 12.0 V: strip the ring and rebuild with the right strip.
- A record that will not sit on all six pads is a warped record: use another record. Do not tighten the cap to flatten it.

## Batch flow for 100

Day 1: receive and inspect (section 1 of the QC plan), inserts and felt on all backplates. Day 2: hub prep and hub to backplate. Days 3 to 5: ring sub-assemblies (about 5 an hour), ring to backplate, splice, burn-in in groups of 10. Day 6: trial hang, wall plate kits, caps, labels. Day 7: pack. One person, about 55 hours in all. This is a plan, not a measurement.
