# RS-CAP-12L PCB spec sheet, rev B (quote-ready: JLCPCB / PCBWay)

> Rev B, 2026-11-11 (../FIXES-fable52.md). Supersedes the rev A / A.1 sheet. LED board: return ring on BOTH faces with stitching vias, Z1 unidirectional. Hub board: no holes, centre gold spring pad instead of a spring pin, the 0919 moves to the return position, Z1 15 V standoff, F1 added.

Two boards. Outlines are in `pcb/RS-PCB-12L-LED.dxf` and `pcb/RS-PCB-12L-HUB.dxf` (mm, R2010, layer OUTLINE = board edge, DRILL = holes, COMP_* = component bodies for reference). Component positions: `pcb/placement.csv` (board origin = board centre, mm, rotation in degrees). Nothing has been ordered.

## 1. RS-PCB-12L-LED (inside the cap)

| Item | Spec |
|---|---|
| Outline | Ring, OD 24.60, centre hole D 8.20 with a FLAT at x = +3.70 (D-shape, routed; keys the core's spigot flat so the dome boss cannot rotate the board), no other holes |
| Stack | 2-layer FR4, **0.8 mm**, 1 oz Cu, ENIG |
| Solder mask | **White, both sides** (it is part of the light-mixing cavity; reflectance matters). No silkscreen on the bottom except designators outside the LED rows. |
| Copper | Exposed ENIG ring r 4.10..6.00, no mask, on BOTH faces, stitched by D 0.3 vias on r 5.2 (none on the D-flat side): LED return. The bottom ring sits on the nickel column top, the top ring is clamped by the dome boss, so either face makes the return. Bottom: exposed pad D 1.2 at r 6.40, 60 deg: LED+ (hand-solder the 30 AWG PTFE lead). |
| Assembly | **Bottom side only**, 8 parts (JLCPCB standard SMT, single side) |
| Qty for quote | 10 (proto), 100, 500 |

| Ref | Part | Qty | Link (loaded 2026-11-10) | Price |
|---|---|---|---|---|
| D1-D6 | Lumileds LUXEON 2835 L128-2790SA35A0DF1, 2700 K, CRI 90 (min), 31 lm typ @ 65 mA, 2.7 V, 3.5 x 2.8 x 0.8, 120 deg | 6 | https://www.digikey.com/en/products/detail/lumileds/L128-2790SA35A0DF1/27376536 | $0.19 / 1, $0.0876 / 100, $0.06982 / 500 (67,550 in stock) |
| Z1 | ESD/TVS 12 V standoff, UNIDIRECTIONAL, 0402, cathode to LED+, anode to LED-. A static-charged record discharging into the pin must not pass through the LEDs: forward ESD is clamped at about 15 V, reverse ESD at one diode drop (a bidirectional part let the reverse strike reach about -25 V across the 3-LED strings) | 1 | - (part not picked) | ~$0.03 E |
| R1, R2 | 100 ohm 1 % 0603 (Yageo RC0603FR-07100RL or the JLC basic-part equivalent) | 2 | https://www.digikey.com/en/products/detail/yageo/RC0603FR-07100RL/726888 | $0.10 / 1, $0.0136 / 100 (Digi-Key stock 0 on 11/10, JLC basic part is fine) |

Schematic (two strings in parallel, 10 mA each, fed by the 20 mA regulator on the hub board):

```
LED+ pad --+--[D1>|--D2>|--D3>|]--[R1 100R]--+-- LED- ring (bottom)
           |                                 |
           +--[D4>|--D5>|--D6>|]--[R2 100R]--+
```
LEDs face DOWN (toward the white flange), on r 8.50 at 30/90/150/210/270/330 deg, long side tangential. Use one flux and Vf bin for all six (current sharing between the strings: about +/-12 % for a 0.3 V string mismatch with 100 ohm ballast).

## 2. RS-PCB-12L-HUB (in the hub's centre relief)

| Item | Spec |
|---|---|
| Outline | Disc OD 13.00 |
| Stack | 2-layer FR4, **1.6 mm**, 1 oz, ENIG (the spring pad and the 0919 pad must be flat gold) |
| Holes | 2x D 0.90 plated at (-1.2, +5.2) / (+1.2, +5.2) for the two 26 AWG leads from the splice cavity. No other holes. |
| Centre pad | Flat ENIG pad D 2.60 at (0, 0), no mask, no via in pad: the contact spring sits on it and carries the 20 mA |
| Assembly | Top side: U1, D1, Z1, F1, P2 (SMT, reflow). Nothing is soldered at P1. |
| Copper | U1 (CCR) pads: >= 25 mm2 pour on each, stitched to the bottom layer. With the contact shorted (plain cap, metal chip) U1 dissipates 0.24 W continuously inside a PEEK pocket; without the pour it runs 80 K+ over ambient. |
| Z1 | TVS, 15 V standoff, unidirectional, 0402 / SOD-523, from the P1 (contact) node to return, at (3.0, 3.6). With the cap off the node floats up to the 12 V rail, so a 12 V-standoff part would sit at its limit and leak; 15 V does not |
| F1 | PTC resettable fuse, 100 mA hold, 0603, in the +12 V tap ahead of D1, at (-3.0, 3.6): the 26 AWG tap comes off a 2 A rail |

| Ref | Part | Qty | Link (loaded 2026-11-10) | Price |
|---|---|---|---|---|
| P2 | Mill-Max 0919-0-15-20-89-14-11-0, SMT spring pin, 3.0 mm stroke, 9.63 free, 85 gf mid-stroke, Au. RETURN contact at (-3.80, 0), working height 7.5 on the insert's back end | 1 | https://www.digikey.com/en/products/detail/mill-max-manufacturing-corp/0919-0-15-20-89-14-11-0/6193088 | $1.52 / 1, $1.0954 / 100, $0.97772 / 500 (9,852 in stock) |
| P1 | no purchased part: RS-HUB-12L-PLUNGER + compression spring (OD 2.3, wire 0.20, free 11.2) in the carrier, on the centre pad | 1 + 1 | RFQ / catalogue spring not yet picked | E |
| U1 | onsemi NSI45020AT1G constant-current regulator 20 mA +/-10 %, 45 V, SOD-123 | 1 | https://www.digikey.com/en/products/detail/onsemi/NSI45020AT1G/2096220 | $0.21 / 1, $0.1096 / 100 (84,000 in stock) |
| D1 | 1N4148WS, SOD-323, reverse-polarity block | 1 | (estimate, not loaded) | ~$0.02 E |

Schematic:
```
pigtail + (+12 V) --[F1 PTC]--[D1 >|]--[U1 CCR 20 mA, A->K]--+-- P1 spring + plunger --> gold pin in the cap --> LED+
                                                              +--[Z1 15 V]-- return
pigtail - ---------------------------------------------------- P2 return pin (0919) <-- E-Z Lok insert <-- cap stud <-- LED-
```
The halo strip is spliced straight to the pigtail in the hub's splice cavity; it does not go through this board. OPEN (review S5): the barrel is the universal 5.5 x 2.1, so a 24 V brick would quadruple the strip power. A 0.75 A hold PTC + 15 V TVS on the rail at the splice is the fix and is not yet a designed part; until then the hub is marked 12 V DC ONLY.

## 3. Electrical numbers

| | Value | Status |
|---|---|---|
| Supply | 12 V DC Class 2 (existing UL adapter), inline PWM dimmer | existing |
| Label-light current | 20 mA total (CCR), 10 mA per LED | design |
| String voltage | 3 x ~2.55 V (Vf at 10 mA, estimated from the 2.7 V @ 65 mA datasheet point) + 1.0 V ballast = 8.65 V | E |
| CCR headroom | 12.0 - 0.7 (D1) - 8.65 = 2.65 V (11.4 V adapter: 2.05 V; NSI45020 regulates from ~1.8 V) | E |
| Power | 0.24 W from the adapter; 0.17 W inside the cap; 0.05 W in the CCR (hub) | E |
| Dimming | Same PWM as the halo: the CCR switches with the supply, label light tracks the halo 1:1 | E (bench check) |
| Short at the cap / plain cap in a lit sconce | current is limited to 20 mA by U1; halo unaffected | design |
| Reverse-polarity adapter | D1 blocks | design |
