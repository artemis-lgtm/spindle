# Prototype shopping list: three 12 in Spindle sconces

Rewritten 2026-11-11 by the product audit (`../audits/AUDIT-product.md`) for the canonical CAD. The list from 2026-11-10 (glued stainless dome, panel jack, rim strip, HitLights COB reel) is in `SUPERSEDED/sample-kit-shopping-list-2026-11-10.md` and must not be ordered from.

Nothing has been ordered. Prices are what the vendor page or the guest instant quote showed on 2026-11-11 unless marked "est" (estimate) or "not checked". Three units, because the tests in `QC-test-plan.md` section 4 need three.

## A. Custom parts (need a file upload or a quote)

| # | Part | Qty | Where | Price seen | Lead time | Note |
|---|---|---|---|---|---|---|
| A1 | Chrome cap RS-CAP-12 rev D | 3 | PCBWay guest pre-quote, brass C360 + chrome | $155.93 each at 1, $139.91 at 5 | 8 to 10 business days + 2 to 4 shipping | THE LONG POLE and the biggest cost. Email quotes will be lower; the RFQ packet `../cad/rfq/dome-cap-RS-CAP-12-revD.zip` is ready and unsent. Cheaper for prototypes: JLCCNC polished brass, no chrome, $42.72 at 1, $180.40 for 5 (thread needs the drawing uploaded) |
| A1b | Stand-in cap so testing does not wait for A1 | 3 | Outwater STD-40CAP-PC, 1-1/4 in chrome cap, 1/4-20 | $4.50 | in stock | Flat, 31.75 mm, thread 3/4 in long: cut the thread to 12 mm. Good enough for the heat, mount and drop tests; not for photos |
| A2 | Wall plate RS-WP-01 rev B, galvanized, bent, 3 studs pressed | 3 (order 10) | SendCutSend | $33.24 at 1, $9.22 each at 10 | about 8 days | Upload `../cad/parts/RS-WP-01_flat.dxf` (rev B). Re-quoted 2026-11-11: accepted with the bend and three studs. The old rev A file was refused for the stud |
| A3 | Aluminium ring RS-HR-12 | 3 (order 10) | SendCutSend | $27.10 at 1, $13.83 each at 10 | about 5 days | `../cad/parts/RS-HR-12.dxf` |
| A4 | Backplate RS-BP-12-MDF rev C | 3 | Local CNC shop | est $25 to $40 each for three | not checked | No shop has quoted the rev C file. Material: one Home Depot 1/2 in MDF panel, $14.58 (page not checked 11-11) |
| A5 | Hub RS-HUB-01 rev C | 3 | Own printer or a print service | est $6 each in filament; service est $25 to $40 each | overnight, or 5 to 10 days | Print the rev C file. A rev B hub cannot be twisted onto the plate |

## B. Stock parts

| # | Part | Qty | Where | Price seen | Note |
|---|---|---|---|---|---|
| B1 | E-Z Lok 400-4 insert | 5 | Albany County Fasteners | $1.90 each | Drive tool on the same page, $17.63 |
| B2 | LED strip, 12 V, 8 mm, 1.46 W/ft, ETL | 1 x 3 m | Ecolocity Ribbon Star low-power 2835 | $44.99 | Enough for 4 rings. The page says 2900 to 3200K. Do NOT buy the HitLights COB reel (10 W per metre) |
| B2b | Second strip to compare | 1 x 5 m | Armacost 131232, UL, 2700K | $29.99 | Wattage is not on its page: measure it. Buy only if both are wanted on the bench |
| B3 | Adapter, UL Class 2, 12 V 2 A | 3 | LED Updates | $12.99 each | |
| B4 | Inline dimmer | 3 | Ecolocity LC-OL-8DIM | $3.99 each (sale; 7 in stock) | |
| B5 | Pigtail with inline female 5.5 x 2.1 jack | 3 | cctvcameraworld | $4.00 each | Check the wire gauge on arrival (18 AWG wanted) |
| B6 | Felt pads 1/2 in, bag of 100 | 1 | Durofelt SAW12BK-100 | $7.00 | |
| B7 | Adhesive felt sheet, 1/16 in, for the cap felt and centre ring | 1 | not checked | est $8 | Punch by hand for prototypes: 1-1/4 in and 3/8 in hollow punches, est $20 |
| B8 | Clear matte PET film 0.010 in, one sheet | 1 | not checked | est $8 | Cut three 37.5 x 7.5 mm washers |
| B9 | Cork roll 1/16 in x 12 in x 30 ft | 1 | WidgetCo | $66.00 | 35 rings. Smaller: The Cork Store CR117 sheets, 15 for $90 |
| B10 | #4 x 3/8 pan-head sheet-metal screws, box of 100 | 1 | Tanner Bolt | $2.90 | Ring screws and P-clip screw |
| B11 | #8 x 1 in flat-head wood screws; #8 x 1-1/4 pan-head; 8-32 nylon lock nuts; 1/4 in nylon P-clips | 1 box each | hardware store | est $20 | |
| B12 | Unflanged drywall anchors, Toggler Alligator | 1 box | toggler.com dealer | not checked, est $12 | Use the anchor the kit will ship with |
| B13 | M3 heat-set inserts, 50 | 1 | Adafruit 4255 | $5.95 | |
| B14 | M3 x 12 flat-point set screws; 1.5 mm x 100 mm straight hex driver | 10; 3 | not checked | est $15 | |
| B15 | 22 AWG and 18 AWG red/black wire, heat-shrink assortment | 1 | hardware store | est $15 | |
| B16 | Box 13 x 13 x 3, bundle of 25 | 1 | Uline S-19090 | $1.62 each | Single wall, 200 lb. Foam est $20 |
| B17 | Test records: two 180 g, two thin (about 120 g), two paper-label throwaways | 6 | thrift | est $12 | |

## C. Test equipment (once)

| # | Item | Price | For |
|---|---|---|---|
| C1 | 4-channel thermocouple logger with type K probes (two, or one 8 to 12 channel logger) | est $60 to $180 | Heat soak T1 needs 10 channels |
| C2 | Fine-wire type K thermocouples, 10 | est $25 | T1 |
| C3 | Polyimide tape, thermal paste | est $12 | T1 |
| C4 | Bench supply 0 to 30 V with current display | est $50 | Strip current, 24 V fault test |
| C5 | Luggage scale, steel straightedge 300 mm, feeler gauges | est $30 | T2, flatness |
| C6 | 24 V 1 A adapter with a 5.5 x 2.1 plug | est $10 | T1 run C |

## Totals (three prototypes)

| Path | Custom parts | Stock parts | Test gear | Total |
|---|---|---|---|---|
| With three real chrome caps (A1 at about $140 to $156 each) | about $760 to $810 | about $370 | about $190 to $310 | **about $1,320 to $1,490** |
| With stand-in caps first (A1b), real caps ordered after a proper quote | about $350 | about $370 | about $190 to $310 | **about $910 to $1,030** |

About half the entries carry an estimate. The quoted ones are A1, A1b, A2, A3, B1 to B6, B9, B10, B13, B16.

## Order of work

1. Today: upload the rev B plate and the ring to SendCutSend; order B1 to B6, B9, B10, B13; send the hub to the printer; take the backplate file to a CNC shop.
2. Today: decide the cap route. Stand-in caps let every test in the QC plan start in about 8 days. Waiting for chrome caps means about 3 weeks before the first test.
3. When parts land: build one unit by `assembly-SOP.md`, run test T1 run A the same day.
