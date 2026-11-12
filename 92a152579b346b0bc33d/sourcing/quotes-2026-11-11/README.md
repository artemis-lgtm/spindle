# Quotes for the two heat rings (pulled live 2026-11-11, guest quotes, no account)

## Aluminium heat ring RS-HR-12
SendCutSend instant quote of the CANONICAL file `cad/parts/RS-HR-12.dxf` (OD 260 mm, ID 200 mm, four 3.3 mm holes on a 211 mm bolt circle), 5052 H32 aluminium 0.040 in, laser cut, no finishing. Re-quoted 2026-11-11 after the CAD was finished.

| Quantity | Each |
|---|---|
| 1 | $27.10 |
| 2 | $20.34 |
| 10 | $13.83 |
| 50 | $10.85 |
| 100 | $7.38 |
| 1000 | $4.69 |

Arrives in 3 days. Shipping and tax not shown until checkout.

The first quote that day used `RS-HR-12_heat-ring_5052-040.dxf` in this folder, a ring WITHOUT the four holes, and came to $7.19 at 100 ($26.48 at 1, $19.87 at 2, $13.50 at 10, $10.57 at 50, $4.57 at 1000; screenshot `scs_alu_a.png`). That file is not the part; do not order from it.

## Cork ring RS-CK-12
Plain 2 mm cork sheet is not a stocked size. 1/16 in (1.6 mm) and 1.5 mm are. The spec moved to 1/16 in on 2026-11-11 and the CAD, drawing and heat study now say 1.6 mm (`cad/parts/RS-CK-12.dxf`; the ring needs four 4.0 mm holes punched on the same bolt circle as the aluminium ring).

| Source | Price | Rings | Per ring |
|---|---|---|---|
| WidgetCo 1/16 in x 12 in x 30 ft cork roll | $66.00 a roll | 35 | $1.89 |
| The Cork Store CR117 1.5 mm, 36 x 24 in, pack of 15 | $90.00 | 90 | $1.00 |
| The Cork Store CR117 1.5 mm, carton of 200 | $950.00 | 1,200 | $0.79 |
| SendCutSend "Rubberized Cork .063", cut for us | $55.83 at 1, $30.97 at 10, $22.99 at 100 | | rejected |

https://www.widgetco.com/products/1-16-x-12-x-30-feet-cork-roll
https://www.corkstore.com/products/1-5mm-cr117-cork-sheets

The cheap cork arrives as a roll or sheet, so we cut the rings ourselves (cork cuts with a blade). The cutting tool is not picked yet. SendCutSend will cut a cork ring for us but charges $23 each at a hundred, which is not worth it: in the heat model the cork is worth about half a degree.
Prices are from each store's live catalog on 2026-11-11. Shipping not included.


## Evening re-check and new quotes (product audit, 2026-11-11)

Guest instant quotes, no account, nothing ordered, nobody contacted. Screenshots: `audit-evening/`.

### Steel wall plate RS-WP-01 (SendCutSend, `cad/parts/RS-WP-01_flat.dxf` as it was that afternoon, rev A outline)

| Configuration | 1 | 10 | 100 | Arrives |
|---|---|---|---|---|
| Mild steel 0.074 in, laser only | $12.26 | $5.32 | $3.41 | Nov 16 |
| + one 90 degree bend | $26.03 | $7.77 | $5.15 | Nov 16 |
| + bend + 3 PEM FH-832-10 studs pressed | $33.30 | $8.85 | $5.95 | Nov 16 |
| + bend + studs + textured black powder coat | $48.18 | $12.96 | $8.32 | Nov 18 |
| G90 galvanized 0.074 in, bend + studs, no finish | $33.29 | $8.83 | $6.03 | Nov 19 |

**SendCutSend refused the stud on that file:** "Hole Collision Issue, 1 hole affected, Hardware". The stud hole at 75 degrees sat 6.83 mm from the end of the single-gang arc slot; PEM FH-832 needs 7.14 mm (0.281 in) from hole centre to the nearest edge. The CAD is fixed (RS-WP-01 rev B: that slot pair is +/-8 degrees, 7.36 mm, gated). **The rev B file was re-quoted at 21:10 the same evening and accepted (next table).** Zinc plating is not offered on 0.074 in steel there (their plating page starts at 0.187 in). The BOM carries the galvanized line.

### Steel wall plate RS-WP-01 REV B, re-quoted 2026-11-11 21:10

Same guest flow, the regenerated `cad/parts/RS-WP-01_flat.dxf`. The bend and all three studs were accepted. No "Hole Collision" dialog. Screenshots `audit-evening/scs_plate_revB_*.png`.

| Configuration | 1 | 2 | 10 | 50 | 100 | 1,000 | Arrives |
|---|---|---|---|---|---|---|---|
| G90 galvanized 0.074 in, bend + 3 studs, no finish (the BOM line) | $33.24 | $18.85 | $9.22 | $6.73 | $6.40 | $5.11 | Thu Nov 19 |
| Mild steel 0.074 in, bend + 3 studs + textured black powder | $48.12 | $26.50 | $13.33 | $9.47 | $8.69 | $7.03 | Wed Nov 18 |

### Aluminium ring RS-HR-12, re-confirmed
5052 0.040 in, canonical file with four holes: $27.10 at 1, $13.83 at 10, $7.38 at 100. Unchanged from the afternoon.

### Chrome cap RS-CAP-12 (STEP only, uploaded as a generic file name, no drawing)

| Service | Material and finish | 1 | 5 | 10 | 50 | 100 | Lead time shown |
|---|---|---|---|---|---|---|---|
| PCBWay | Brass C360, chrome plating | $155.93 | $139.91 | $131.70 | $121.36 | "Customized Quote" | 8 to 10 business days + DHL 2 to 4 days ($26.55) |
| PCBWay | Brass C360, as machined | $43.87 | | | | | 3 to 5 business days |
| JLCCNC | Brass H59, mirror polish, no plating offered on brass | $42.72 | $36.08 | $32.81 | "Manual Quote" | "Manual Quote" | 3 to 11 days shown for the default config + UPS 2 to 4 days ($26.60) |

Both pages call these pre-quotes subject to manual review. JLCCNC's price leaves the thread out until a drawing is uploaded. Xometry, Protolabs Network and RapidDirect show a guest upload box but the upload did not advance (not checked). Fictiv and Protolabs need a login. **There is no price at 100 pieces from anyone.**

Stock stand-in for prototypes: Outwater STD-40CAP-PC, 1-1/4 in polished chrome flat cap on a 1/4-20 thread, $4.50, in stock. Its thread is 3/4 in long against the 11.95 mm design stud, so it must be cut down. Not fitted.

### Other live checks that changed a number
- LED Updates adapter: $12.99 (was $11.99). No bulk price on the page.
- Ecolocity dimmer: $3.99 is a sale price (list $12.99), 7 in stock.
- Adafruit 610: out of stock, and it is a panel jack, which the design no longer uses. Real part: a pigtail with an inline female jack, $4.00 at cctvcameraworld (wire gauge not stated).
- Albany County Fasteners, E-Z Lok 400-4: $1.90, $1.70 at 100, $1.50 at 1,000. The "$17.63 per 10" in the old BOM was the drive tool.
- HitLights 12 V COB (the strip in `sample-run-plan.md`): 3.05 W per foot = 10 W per metre, 10 mm wide. That is 7 W on this ring, over the 6 W cap, and it does not fit an 8 mm layout. Do not order it.
- Ecolocity low-power 2835 strip: $17.99 per 1 m, $44.99 per 3 m, in stock; the page says 2900 to 3200K, not 2700K.
- Armacost 131232: $29.99 per 5 m, UL Listed, 2700K, 8 mm, 30 LEDs per metre; wattage not on the page.
- WidgetCo cork roll: $66 ($52 each at 5 rolls), in stock; the page calls it both "1/16 inch" and "2mm" and shows no adhesive back.
- Uline S-19090 13 x 13 x 3: $1.62 at 25, $1.48 at 100. It is a 200 lb single-wall box, not double wall.
- Hardwick keyhole plate (7 in unit): sold out. PowerBridge kit (linked add-on): out of stock.
- Not checked (blocked or not opened): Home Depot MDF, eBay 45 adapters, Monoprice cable, McMaster, Zoro, Digi-Key.
