# build/ : build and economics for the record sconces

Written 2026-11-10 (overnight build). Nothing was ordered, no one was contacted, no accounts created. Decisions in BRIEF.md, NOTES.md, scope-report.md, engineering-report.md, mounting-report.md and design-report.md are taken as fixed and not re-argued.

## What is here

| File | What it is |
|---|---|
| `BOM.md` | Final bill of materials per SKU (Kit 12", Sconce 12" vintage and named, 7" unit, 3-piece Set, in-wall kit add-on). Every line: spec, supplier URL, unit cost at qty 1 / 20 / 100 / 500, and a fetch status (V confirmed tonight, P confirmed 11/9 and rate-limited tonight, S snippet, E estimate). Dome cap and in-wall lines are the sibling agents' final picks, credited. |
| `BOM.csv` | The same lines, machine-readable. Generated. |
| `sample-kit-shopping-list.md` | Everything to buy this week to hand-build 3 x 12" + 1 x 7" prototypes with off-the-shelf stand-ins (MDF backplate, glued MDF hub, uxcell stainless hemisphere + bolt as the chrome dome, Rockler brass knob, Outwater flat cap, Westinghouse crossbar as the plate), with links and a total (about $400 parts), plus the tools list ($300 to $360) and what the prototypes must answer. |
| `assembly-SOP.md` | Step-by-step build of one unit with minutes per step (about 20 min at batch), six jigs, COB-to-barrel-jack wiring with polarity (centre positive, red +), strain relief, dome cap bonding, in-wall kit bag assembly, 100-unit batch rhythm. |
| `QC-test-plan.md` | 2-hour heat soak with IR thermometer at 8 points (record under 35 C target), pull/drop/bump/twist/swap tests on the wall mount, dimmer flicker checks by eye and 30/240 fps camera, ISTA 3A-lite packaging drop test, and a printable pass/fail sheet. |
| `cost-model.md` | Landed cost, real USPS Ground Advantage commercial rates (Notice 123, cubic 0.30 tier for 13x13x3) blended over a zone mix from Fort Lauderdale, Stripe 2.9% + 30c, CPA scenarios $25/$39/$60/$80, contribution per SKU at BRIEF prices, break-even CPA, cash for the first 100 units (about $5,300 out before the first ship, $7,600 through the batch). |
| `cost-model.csv` | Per-tier, per-SKU economics. Generated. |
| `cost-model.py` | The single source of the numbers. Edit a price here, run `python3 cost-model.py`, both CSVs regenerate and the console prints the tables. |

## The six things Austin needs to know
1. 12" parts are $38 at 100 units (not the $27 in the engineering report) because the twist-lock steel plate, the bonded chrome dome, the separate dimmer and the jack were added by later decisions.
2. Sconce $129: $58 contribution at 100, break-even CPA $58, $19 left at the $39 median. Named $179: $78 contribution. Set $249/$329: $108/$172, and it survives an $80 CPA.
3. Kit $89 clears $25 at 100 and loses money at any CPA above $25. It needs a price change, a cheaper spec (keyhole + flat cap), or to be sold only as an organic/upsell SKU. Not decided here.
4. Ship in 13 x 13 x 3: it is under the 0.30 cu ft cubic tier, $8.79 to $15.22 by zone, cheaper than the 3 or 4 lb weight rate everywhere. Blended $13.15 label plus insurance.
5. First-week spend: about $400 parts + $300 to $360 tools for three prototypes.
6. Cash before the first production unit ships: about $5,300 (parts $3,807, records $420, prototypes and jigs, $279 insurance); 100 deposits at $25 cover half.

## What is open
- 7" cap (chromed 45-adapter look): not quoted by dome-cap; carried at the 12" dome cost.
- Bayonet studs, M3 set screw, pull string: estimates; inwall-parts was not assigned them.
- Steel plate price: upload the DXF to SendCutSend.
- COB strip vendor and UL file, adapter 100-unit price, Uline 13x13x3 SKU: confirm in a browser; those hosts block curl.
- 7" Kit standalone price and in-wall kit price are not in BRIEF; the model uses $59 and $29 as placeholders.
- Zone mix and $1.50 insurance top-up are estimates; replace with the first 20 real labels.
- The 7" and Set shipping assumes one adapter per unit (design-report.md); a Y-lead would save about $14 per Set.

## Fetch log
Confirmed live tonight (HTTP 200, price read from page): Albany County Fasteners (E-Z Lok 400-4, brass thumbscrew), Rockler brass knob, aluminumspacers.com standoff, Durofelt (both washers), Ecolocity (2835 strip, PWM dimmer), Adafruit 610 jack, Outwater cap, AV Outlet Arlington LV1, Zack Electronics Datacomm plate, SendCutSend pricing page, Stripe pricing, USPS Notice 123, Pirate Ship rate pages, Diode LED wire page (no price), Uline (catalog reachable, search 404). Rate-limited (429) because several agents hit them at once: Hardwick & Sons, LED Updates, Woodpeckers, Wood Art Supply, HitLights, Sleeve City. Bot-blocked (403/503): Home Depot, Amazon, eBay, Monoprice, Harbor Freight, Lowe's, Tayda. WebSearch budget for the session was exhausted before this task started; all verification was curl.
