> **REV B (2026-11-11, Fable 5.2 pessimist review: ../REVIEW-fable52.md, every change in ../FIXES-fable52.md).** Rev A and A.1 are superseded and must not be quoted: the D-key stood taller than the LED PCB, so the cap could not be assembled as drawn, and the centre spring pin had 0.09 mm of margin. What changed: the record now sits on a centre backing ring; a clear PET washer lies between cap and label; the lit cap has no felt and no felt recess (flat flange); stud 11.65; smooth D 7.1 shoulder; key 0.55 + boss counterbore; lip raised to a 0.25 gap; stepped bore, headed pin; the centre contact is a 4.9 mm travel gold plunger inside a PEEK guard tube (no catalogue pin has more than 3 mm); the hub relief is 9.1 deep (RS-HUB-01 rev B); TVS parts corrected. checks.md is the generated source of truth for every number.

# RS-CAP-12L "label light": engineering design

2026-11-10, revised 2026-11-11. Nothing sent to anyone, nothing ordered. The lit sconce needs RS-HUB-01 rev B (deeper centre relief) and RS-BP-12-MDF rev B (centre backing ring); it reuses the E-Z Lok insert, adapter and dimmer.

## Summary (plain English)
1. Power reaches the cap through the screw: the hollow 1/4-20 stud is one wire (through the brass insert) and an insulated gold pin down its middle is the other, touching a sprung gold plunger waiting at the back of the insert.
2. A 20 mA regulator on the hub side feeds only that plunger, so nothing the customer does at the cap can short the adapter or kill the halo; a reverse diode protects against a wrong adapter.
3. The hot ring in the first renders was physics (a low light source falls off with the cube of distance). This design hides six warm LEDs in a white cavity and lets light out only through a slatted louver that aims it almost flat across the label. Simulated result (re-run for rev B): about 4.0:1 smooth fall-off from the cap edge to the label edge, against 270:1 for the old concept.
4. From the front it is the same chrome dome; it sits on a 5.0 mm lit pedestal, so from the side you see a soft frosted glowing band under the chrome lip (that band is where the light has to come out).
5. Added cost is about +$31 per sconce at 100 and about +$16 at 500 with a moulded louver (BOM-delta.md, regenerated for rev B). Only about $2 of that is verified purchased parts; the rest is RFQ-dependent machining and the louver.

## 1. The hard question: getting 12 V through the 7.26 mm spindle hole

**Chosen: coaxial stud.** The stud is the return conductor (cap body, core, stud thread, E-Z Lok insert). A headed hard-gold brass pin in a PEEK sleeve runs down the stud bore; its D 2.4 gold face sits 0.05 mm below the stud tip and is the +12 V contact. Behind the backplate, in the 14 x 9.1 relief of RS-HUB-01 rev B, a PEEK carrier pilots its 4.80 spigot into the back of the insert's thread. That spigot is also a guard tube: a gold plunger on a small compression spring rides inside it and its D 1.2 nose stands out of the top. A Mill-Max 0919 spring pin presses on the insert's back end to pick up the return. The record still swaps exactly as today: unscrew the cap, lift the record, screw the cap back on.

Why it works here:
- The insert is in MDF (an insulator), so the insert can be a pole; it already sits on the axis, and its back end is exposed in the hub relief.
- Travel. The stud tip moves 1.5 mm between a 1.2 and a 2.7 mm record, and the tolerances (stud, MDF thickness and swell, felt, printed relief depth, PCB) add 0.94 one way and 1.29 the other. That is 3.7 mm; the longest catalogue spring pin has 3.0. The plunger has 4.9. With everything stacked the wrong way it still has 0.56 mm of compression on the thickest record.
- Guard. The guard tube's top is 2.1 mm above the backplate back face, 0.56 mm below the lowest place a correct lit-cap stud can reach. A wrong, longer screw lands on PEEK; the plunger just retracts flush with 0.7 mm of spring left. Nothing a customer threads in can crush the contact.
- All three caps (RS-CAP-12L rev B, RS-CAP-12 rev D, RS-CAP-7 rev C) put their stud TIP at the same depth; the build asserts it. The lit stud is 11.65 and the plain one 11.95 only because the plain cap stands 0.3 higher on its felt.
- The + contact is a small target in the middle of an insulator. Worst-case misalignment plus the nose radius reaches r 1.16; the gold head is r 1.2 and brass starts at r 1.575. **The plunger can only ever land on gold or PEEK, so screwing in cannot short.**
- The regulator is in series with the plunger, so even a deliberate short (screwdriver, metal chip, a plain cap) draws 20 mA.

Rejected (one line each):
- Thin 2-wire pass-through beside the stud: 7.26 hole minus 6.35 stud leaves 0.45 mm per side; no room, and the wires twist every swap.
- 2 wires through a hollow stud to a connector: the cap rotates when screwed, so the wire winds up; the connector would be behind the backplate where nobody can reach it.
- Battery: ruled out by Austin (must be always on like the halo).
- Inductive (Qi-style) power through the record: the cap is solid brass, so it shields the coil and heats from eddy currents; also adds an RF driver and an FCC question.
- Split stud (two insulated half-threads): weak 1/4-20, alignment-dependent, and expensive.
- Pin-and-socket coax (pin sticking out of the stud into a socket): works, but leaves an exposed pin on the customer-handled part; the flat target + wall-side spring is more robust.
- Spring pin in the cap and a flat target on the wall side: same physics, but puts the fragile part on the piece people drop.

## 2. Stack-up (full table and the tolerance stack in checks.md, section "Label light")

Record seat = 1.1 mm above the backplate front face (pads in their targets, centre backing ring loaded). PET washer 0.25. No felt under the lit cap.

| | Thin record (1.2) | Nominal (2.03) | Thick record (2.7) |
|---|---|---|---|
| Thread engagement in the insert (threaded, past the 1.5 dog point) | 9.10 (7.60) | 8.27 (6.77) | 7.60 (6.10) |
| Centre contact compression (usable 0.5..4.9) | 3.35 | 2.52 | 1.85 |
| Stud tip above the guard tube | 1.50 | 2.33 | 3.00 |
| Same, every tolerance against us | 0.56 above the guard | | 0.56 compression |

Other numbers: return pin working height 7.5 (rated 6.63..8.87; worst case 6.79..8.01); carrier top 0.6 below the backplate back face; spigot radial clearance in the insert minor 0.09..0.23; hollow stud wall at the thread root 0.82, tensile area 10.3 mm2; flange solid 1.3 (no recess); LED PCB edge to dome wall 0.2; dome lip 0.25 above the louver and window; lip overhangs the window by 1.0; lit cap height 15.0 above its contact face (plain cap 10.0).

Cap stack (cap frame, contact face z=0 on the PET washer): flat core flange 0..1.3 with an 8 deg cone under the louver (to 0.60 at r 17.5) | louver ring 0.60..4.75, r 12.5..17.5 | window ring r 17.55..18.05 | LED PCB 4.8..5.6 on the column top, LEDs facing down | dome lip at 5.00, band to 6.6, sphere to 15.0 | dome boss (face 0.60 above the lip) screws onto an M8x0.5 LH spigot on the column and clamps the PCB. The boss is the hard stop.

## 3. Electrical schematic

```
 UL Class 2 adapter 12 V --- inline PWM dimmer --- 5.5x2.1 plug --- inline jack on the RS-HUB-01 pigtail
   pigtail (+) -----+----------------------------------------------------------------- halo COB strip (+)  [unchanged]
                     +--[F1 PTC]--[D1 1N4148WS >|]--[U1 NSI45020 20 mA]-- P1 spring + gold plunger
                                                                   | (gold plunger on the gold pin head)
                                                                 pin -> 30 AWG PTFE up the stud bore -> LED PCB (+)
                                                                 LED PCB: 2 strings x (3x LUXEON 2835 + 100R) in parallel
                                                                 LED PCB (-) rings (both faces) -> column + dome boss -> core -> stud thread
                                                                   | (thread contact)
   pigtail (-) -----+-- P2 return pin (0919) on the insert back end <- E-Z Lok insert
                     +----------------------------------------------------------------- halo COB strip (-)  [unchanged]
```
- **Polarity:** + is the shrouded centre pin; the big metal parts (dome, stud, insert) are the return. D1 blocks a centre-negative adapter.
- **Is the chrome at a voltage?** The dome is bonded to the return. With a low-side PWM dimmer (the usual inline type) the return toggles between 0 and +12 V relative to the adapter's negative during the off-time. Either way it is at most 12 V DC from a Class 2 source: below the 30 V dry / 15 V wet touch limits, so it is touch-safe. With the cap off, the plunger nose sits 5+ mm deep inside the insert behind a 20 mA limit.
- **Short while screwing in:** the threads engage first (same pole, no event); the pin head meets the plunger only in the last few mm and cannot touch brass (sec. 1). A chip of metal bridging plunger to insert draws 20 mA through U1, the halo stays lit, and the adapter never sees a short.
- **Plain RS-CAP-12 rev D or RS-CAP-7 rev C in a lit sconce:** its solid stud shorts the plunger to the return (20 mA, harmless: 0.24 W in U1, which needs the 25 mm2 copper called out in PCB-SPEC.md). Its tip lands where the lit cap's does, so the plunger is compressed the same amount and nothing is damaged. An older cap (rev C or earlier, or any longer screw) stops on the guard tube instead.
- **Dimming:** U1 switches with the PWM supply, so the label light tracks the halo 1:1 through the existing dimmer; no extra control. Headroom 2.65 V at 12.0 V, 2.05 V at 11.4 V (U1 needs about 1.8 V).

## 4. Power budget and thermal

| | Value | Status |
|---|---|---|
| Label circuit from the adapter | 12 V x 20 mA = 0.24 W (adapter 24 W, halo unchanged) | design |
| In the cap | 6 x 10 mA x ~2.55 V + 2 x (10 mA)^2 x 100 = 0.17 W | E (Vf at 10 mA estimated) |
| In the hub (U1 + D1) | ~0.07 W | E |
| LED flux | ~5.3 lm per LED at 10 mA, 31 lm total | E (scaled from 31 lm @ 65 mA, +10 % low-current efficacy) |
| On the label | 2.9 % of LED flux = 0.92 lm, about 134 lux average over the label annulus | simulated x estimated flux |
| Cap temperature rise | Worst case with convection only (h ~7 W/m2K on ~2,100 mm2; chrome barely radiates, emissivity ~0.06; the black band adds a little): 0.17 W / 0.016 W/K = **about 11 K**. With conduction into the record and stud it should be closer to 5 to 7 K. | E (must be measured) |

Halo strip and the lit cap together (added 2026-11-11): the lit sconce uses the SAME heat-safe halo as the plain one (strip on the back of the backplate on an aluminium ring over a cork ring; `assembly_lit.py` builds on `assembly.py`, and a gate checks the two stacks are identical). The halo's warm band is at r 114 on the record; this cap is at the centre, 95 mm away. `../THERMAL.md` gives the halo's contribution under the cap as 0.02 K (normal) to 0.30 K (stacked worst case), so the cap rise in the table above is the whole story at the centre. Neither number is measured.

The thermal ceiling drove the optics: a chrome cap sitting on a customer's favourite record must stay near room temperature, so the design spends light (2.9 % efficiency) rather than power. Brightness can go up 25 to 50 % by swapping U1 for NSI45025/NSI45030 (same footprint) **only after** a thermocouple test on the first prototype.

## 5. Optics: why the first renders made a hot ring, and the fix

A small source sitting 1 to 2 mm above the label lights it with irradiance proportional to h/d^3. Going from 2 mm to 30 mm from the cap edge that is a factor of a few hundred. The renders-labellight concept traces to **267:1** (cad/label-light/optics-results.json), which is exactly the hot ring with a dim edge Austin saw. A diffuser on its own makes it worse (a diffuse low source falls off even faster). Evening the label requires sending almost all the light out within a few degrees of horizontal, and only a little steeply down.

RS-CAP-12L does that with an angular filter, not a lens (a lens could not, because a 2835 LED is 1.8 mm across inside a 3 mm optic):
1. Six LUXEON 2835 (2700 K, CRI 90) face down onto a white flange (paint R >= 0.90) inside a closed white cavity under a white-mask PCB. No LED is visible from outside, so there are no hot spots.
2. The only way out is a 5-channel louver (0.25 fins at 0.65 pitch, 5 mm deep). Each channel only passes light within about +/-5 deg of its own axis; the floor and fins slope 8/8/8/7/6/4 deg down, bottom to top, so the low channels fill the label near the cap and the high ones reach the edge. The inner 30 % of each fin is white (recycles light); the outer 70 % is matte black.
3. A clear PC window with a light satin outer face (~3 deg) blends the five channel "sheets" into one wash and keeps dust out.
4. The chrome underside of the dome lip folds any upward-going light back down onto the label (glare to the room 0.2 %).

Monte Carlo result (3D rays through the real STEP dimensions, 1.2 M rays, cad/label-light/optics.py):

| | Old concept | RS-CAP-12L |
|---|---|---|
| Max/min irradiance, r 21.7..50.5 mm | 267 | **3.96** (rev B re-run: 1.141 at r 23, peak 1.583 near r 28, 0.4 at r 49; rev A.1 was 3.73) |
| Light landing on the label | 67 % | 2.9 % |
| Azimuthal ripple near cap / near edge | n/a | 1.26 / 1.11 |
| Tolerance cases (satin 1 or 6 deg, paint R 0.85, all-black fins) | | 3.73 / 5.1 / 3.86 / 4.5 |

The first 2.6 mm next to the cap (r 19..21.7) is in the lip's shadow and reads as a thin dark collar (visible in the render). Plot: optics-profile.png. The render renders-lit/png/lit_close_wide.png lights the label with this traced distribution (exported as RS-CAP-12L.ies on 48 emitters).

## 6. Cap body and the "one solid piece" look

- **Dome (RS-CAP-12L-DOME):** brass, same outside as RS-CAP-12 (D 38.1, R 25.80 x 8.4 on a 1.6 band, R 0.8 lip edge), chrome outside including the lip face. Hollow, with a centre boss threaded M8x0.5 LH onto the core and a D 8.3 x 0.4 counterbore in the boss mouth. Left-hand so unscrewing the cap tightens it; Loctite 270 (with activator on nickel) as well.
- **Core (RS-CAP-12L-CORE):** brass, electroless nickel 5 um max (the stud thread and column top are contacts, so no chrome). Hollow 1/4-20 stud with a stepped bore, smooth D 7.1 shoulder, FLAT underside, flange with an 8 deg louver floor, column, LH spigot with a 0.55 D-key and run-out groove, 45 deg wire hole.
- **No felt.** Rev A had a small felt in a recess that left a 0.3 mm web carrying the whole flange. Rev B's flange is solid 1.3 and sits flat on the PET label washer; the softness in the clamp comes from the felt backing ring behind the record.
- **Retention:** the dome boss clamps the LED PCB onto the column (return contact on both PCB faces). The boss is the hard stop; the lip stays 0.25 above the louver and window (tolerance stack 0.12), each of which has 3 dots of UV adhesive.
- **Look:** from the front you see only the chrome dome; the lip overhangs the window by 1.0 mm. From the side there is a 5.0 mm band under the chrome: a thin black flange rim, then the frosted window glowing warm. It reads as the chrome dome floating on light, not as a gap.

## 7. Hub-side contact module (needs RS-HUB-01 rev B: centre relief 9.1 deep)
RS-HUB-12L-CARRIER (PEEK body + guard tube) on RS-PCB-12L-HUB (D 13, 1.6 mm): centre gold pad carrying the contact spring and RS-HUB-12L-PLUNGER, P2 Mill-Max 0919 return pin, U1 CCR, D1, Z1, F1. The two leads from the splice cavity run along the hub's front lead channel into the relief. The spigot pilots the module into the insert when the hub is screwed to the backplate (lead-in 0.6 x 45, capture 0.69 mm against a +/-0.5 float). The return pin and the spring hold the module back against the relief floor.

## 8. Contact reliability and plating
- Centre: hard-gold plunger nose (1.3 um Au over Ni) on the hard-gold pin head. Force 0.53 to 1.18 N from the spring (calc; the spring is a catalogue part not yet picked). Each swap wipes the contact under the last turn. The spring carries the 20 mA from a flat gold pad; at 20 mA a few ohms cost millivolts.
- Pin and sleeve cannot creep: the sleeve sits on a shoulder in the stud bore and the pin head sits in a counterbore in the sleeve. No adhesive, no staking.
- Return: nickel stud thread on the brass insert under the clamp load; every installation re-cuts the contact. The return pin on the insert end never moves (static, gold on brass). The insert's back-end land (flat between the thread chamfer and the knife thread) has not been measured: put P2 at its mid radius once an insert is on the bench.
- No chrome on any contact surface.

## 9. Failure modes
| Mode | Effect | Mitigation |
|---|---|---|
| Plain cap (rev D / rev C 7 in) in a lit sconce | contact shorted (20 mA), label light off, halo fine | same tip depth as the lit cap (asserted): no damage |
| Older cap, 1 in bolt, any long screw | would have crushed a 3 mm spring pin | lands on the PEEK guard tube; plunger retracts flush. Hand force only: a wrench can still crush PEEK |
| Metal debris in the insert | + to - path | U1 limits to 20 mA; halo unaffected |
| Centre-negative adapter | reverse bias | D1 blocks |
| 24 V adapter (5.5 x 2.1 is universal) | halo strip at 4x power (it now sits on the aluminium heat ring behind the backplate, not on the rim; cad/THERMAL.md does not cover a 24 V fault) | hub marked 12 V DC ONLY; F1 protects the label tap; a rail TVS + PTC at the splice is specified in PCB-SPEC.md but NOT yet a designed board (open item) |
| Record outside 1.2..2.7 mm at the label | thinner: stud stops on the guard, cap will not seat. Thicker: no contact, no light | measure 10 real records incl. a Dynaflex and a 200 g; the travel has 0.67 mm to spare after all tolerances |
| Static discharge from a charged record into the pin | LED or CCR killed | Z1 on both boards (cap: unidirectional 12 V; hub: 15 V standoff) |
| CA/epoxy on the insert's back face | return pin sees an insulating film, no light | SOP: adhesive in the bore only, wipe the back face, continuity < 1 ohm stud-to-hub-PCB at final test |
| Dome boss lands on the key instead of the PCB (rev A.1 as drawn) | PCB loose, no return, no light | key 0.55 under the thinnest board + boss counterbore; gated in checks.md |
| Dome lip lands on the louver / window | crushed fins or loose PCB | lip gap 0.25 vs stack 0.12; gated |
| Dome-core joint loosens | dome spins off the stud | LH thread + Loctite 270; unscrewing torque tightens it |
| Preload decay (felt takes a set) | record can shift a little, return path through the thread goes intermittent | open: try a low-set urethane (PORON class) for the backing ring and cap felt on the first samples |
| Label fading | about 134 lux 24/7 is over 1 Mlux.h a year: vintage reds and fluorescents fade in a few years, leaving a sharp unfaded disc under the cap | disclose it to customers; recommend dimming; UV itself is negligible at 2700 K |
| Thermal (cap too warm) | warm label/record | 0.17 W design; thermocouple test before raising current |
| PWM flicker on camera | same as the halo today | inherited from the dimmer |

## 10. Verified vs estimated
**Verified (by me, today):**
- Geometry: all parts build as valid single solids from sconce_lit.py; **0 interferences** in the lit assembly at nominal, thin (1.2 mm) and thick (2.7 mm) records, with the spigot thread modelled at its minor diameter so a clash inside the thread would show (checks.md). build_all.py still builds every existing part with 0 hits.
- Clearance stack numbers in sec. 2 (computed from the same parameters as the STEP).
- Optics: Monte Carlo results in sec. 5 (simulation, not a measurement: assumes Lambertian LEDs, ideal white diffuse paint R 0.92, white mask 0.85, chrome 0.65, a Gaussian satin model, axisymmetric fins; the 6 ribs are not in the sim).
- Prices and stock read off live pages today: LUXEON L128-2790SA35A0DF1, Mill-Max 0919, NSI45020AT1G, RC0603FR-07100RL (Digi-Key). See link-check.txt. (Rev B no longer uses the Mill-Max 0906, the PEEK tubing or a Durofelt washer in the cap.)
- Mill-Max 0919 stroke and free height (Digi-Key page + Mill-Max page). Mill-Max's own page calls the 3 mm 0919 family its longest travel (checked 2026-11-11), which is why the centre contact is no longer a catalogue pin.

**Estimated / needs a supplier answer:**
- All custom part prices (dome, core, pin, louver, window, carrier, PCB fab + SMT, labour): RFQ needed.
- Mill-Max 0919 barrel diameter (modelled as 1.6): check against the Mill-Max drawing before cutting the carrier.
- The contact spring (OD 2.3, wire 0.20, free 11.2, about 0.15 N/mm): calculated, not a picked catalogue part. The whole centre contact is new in rev B and has never been built.
- LUXEON Vf and flux at 10 mA (scaled from the 65 mA datasheet point); white paint reflectance; window satin grade.
- Whether a micro-SLA shop holds 0.25 fins x 5 mm reliably (BMF-class yes, desktop SLA maybe). That is the riskiest manufacturing question.
- Record thickness at the label for real pressings (1.2..2.7 assumed); measure 10.
- Cap temperature rise (11 K worst case calculated); measure on the first prototype.
- How much the felt backing ring compresses under the clamp (0.5 assumed, CENTER_RING_SET in sconce_cad.py): measure, edit that one number, rebuild.
- Plating house: masking the thread, the boss and the inside of the dome while chroming the lip face.

## 11. Files
- Source: cad/sconce_lit.py (parameters + parts), cad/assembly_lit.py, cad/drawings_lit.py, cad/label-light/optics.py + raytrace.py, cad/label-light/pcb.py, cad/label-light/bom_delta.py; build_all.py builds all of it.
- STEP: cad/label-light/step/ (and cad/parts/), assembly cad/assemblies/RS-ASM-12L-MDF.step.
- Drawings: cad/label-light/drawings/*.pdf.
- PCB: PCB-SPEC.md, pcb/*.dxf, pcb/placement.csv.
- BOM delta: BOM-delta.md / .csv. RFQ: cad/rfq/dome-cap-lit/ and cad/rfq/dome-cap-lit-RS-CAP-12L-revB.zip (rev A.1 zip is in cad/rfq/SUPERSEDED-do-not-quote/).
- Render: renders-lit/png/lit_close_wide.png (src: renders-lit/src/build.py -> lit.py).
