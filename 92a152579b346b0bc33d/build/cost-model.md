# Cost model (build/cost-model.md)

Rewritten 2026-11-11 by the product audit (`../audits/AUDIT-product.md`). Every table below is printed from `cost-model.py` (run `python3 cost-model.py`; it also writes `cost-model.csv` and `BOM.csv`). The version from 2026-11-10 is in `SUPERSEDED/cost-model-2026-11-10.md`. Its numbers are wrong for the product in the CAD and must not be quoted.

## The answer first

- At the prices that can be bought today, a 12 in unit costs **$78.04 in parts at 100 units**, not $47.46 and not the $38 or $27 of earlier reports. Line by line: `BOM.md` section 2.
- **The $89 Kit loses $19.90 on every order at 100 units before any advertising.** At $99 it still loses about $10. The Kit needs to be about $125 to clear $15 before ads at these costs.
- The $129 Sconce clears $12.77 and the $179 Sconce $33.32 before ads. A $39 Meta purchase cost (the median used in the scope report) wipes out both.
- The chrome cap is carried at $15.00 at 100. That is a placeholder. The only live prices are $121 to $156 each for 1 to 50 pieces (PCBWay guest pre-quote). Until a real quote for 100 exists, nothing below is firm.
- First 100 units need about **$8,224** for parts and records (it was $5,166), plus about $1,465 of postage at ship time and $1,333 of labour.
- One prototype costs about $279 in parts, because the cap is $156 for one.

## 1. Inputs

Parts: `BOM.md`. 12" unit $278.98 / $211.33 / $78.04 / $60.29 at 1 / 20 / 100 / 500. 7" unit $44.33 / $40.99 / $33.58 / $24.35. In-wall kit $10.20 / $9.62 / $6.47 / $5.35.

Records: $2.00 craft-grade, $30.00 named title (scope-report.md).

Labour: $25 an hour. 40 minutes per 12" unit for the first units, 32 at 100, 28 at 500. This went up from 25 / 20 / 18 because the heat-safe halo adds a ring sub-assembly: cut and punch the cork, lay seven strip pieces, solder six jumpers, drive four screws (`assembly-SOP.md`). Nothing has been built, so nothing has been timed. A Sconce adds 10 minutes for the record; a 7" unit is 70% of a 12"; the Set adds 5 minutes.

Shipping: USPS Ground Advantage Commercial through Pirate Ship, cubic rate for the 13 x 13 x 3 box, blended over an estimated zone mix from Fort Lauderdale: 12" $14.65, 7" $12.54, Set $20.18 including $1.50 of insurance top-up. Rates fetched 2026-11-10 from USPS Notice 123, not re-checked on 11-11. Keep the box at 13 x 13 x 3: the next cubic tier costs about $1.50 more per parcel. The shipped weight is about 3 lb (hung parts about 2.2 lb, plus plate, adapter and box).

Stripe: 2.9% + $0.30 (stripe.com/pricing, fetched 2026-11-10).

Ad cost per purchase scenarios: $25 / $39 / $60 / $80.

## 2. Landed cost and contribution per SKU

Contribution = price minus parts, record, labour, shipping and Stripe. A negative number is a loss on every order before advertising.

### At 100 units (the first production batch)

| SKU | Price | Parts | Record | Labour | Ship | Stripe | Landed | Contribution | Margin | Net at $25 ad cost | $39 | $60 | $80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kit 12" | $89 | $78.04 | $0.00 | $13.33 | $14.65 | $2.88 | $106.02 | **-$19.90** | -22% | -$45 | -$59 | -$80 | -$100 |
| Sconce, vintage | $129 | $78.04 | $2.00 | $17.50 | $14.65 | $4.04 | $112.19 | **$12.77** | 10% | -$12 | -$26 | -$47 | -$67 |
| Sconce, named | $179 | $78.04 | $30.00 | $17.50 | $14.65 | $5.49 | $140.19 | **$33.32** | 19% | $8 | -$6 | -$27 | -$47 |
| 7" Kit (placeholder $59, not buildable yet) | $59 | $33.58 | $0.00 | $9.33 | $12.54 | $2.01 | $55.45 | **$1.54** | 3% | -$23 | -$37 | -$58 | -$78 |
| Set, kit (not buildable yet) | $249 | $142.20 | $0.00 | $34.08 | $20.18 | $7.52 | $196.47 | **$45.01** | 18% | $20 | $6 | -$15 | -$35 |
| Set, with records (not buildable yet) | $329 | $142.20 | $6.00 | $42.42 | $20.18 | $9.84 | $210.80 | **$108.36** | 33% | $83 | $69 | $48 | $28 |
| In-wall kit add-on ($29) | $29 | $6.47 | $0.00 | $2.08 | $0.00 | $1.14 | $8.55 | **$19.31** | 67% | -$6 | -$20 | -$41 | -$61 |

### At 20 units (the pre-sold batch)

| SKU | Price | Parts | Record | Labour | Ship | Stripe | Landed | Contribution | Margin | Net at $25 ad cost | $39 | $60 | $80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kit 12" | $89 | $211.33 | $0.00 | $16.67 | $14.65 | $2.88 | $242.64 | **-$156.52** | -176% | -$182 | -$196 | -$217 | -$237 |
| Sconce, vintage | $129 | $211.33 | $2.00 | $20.83 | $14.65 | $4.04 | $248.81 | **-$123.85** | -96% | -$149 | -$163 | -$184 | -$204 |
| Sconce, named | $179 | $211.33 | $30.00 | $20.83 | $14.65 | $5.49 | $276.81 | **-$103.30** | -58% | -$128 | -$142 | -$163 | -$183 |
| 7" Kit (placeholder $59, not buildable yet) | $59 | $40.99 | $0.00 | $11.67 | $12.54 | $2.01 | $65.19 | **-$8.21** | -14% | -$33 | -$47 | -$68 | -$88 |
| Set, kit (not buildable yet) | $249 | $289.31 | $0.00 | $42.08 | $20.18 | $7.52 | $351.58 | **-$110.10** | -44% | -$135 | -$149 | -$170 | -$190 |
| Set, with records (not buildable yet) | $329 | $289.31 | $6.00 | $50.42 | $20.18 | $9.84 | $365.91 | **-$46.75** | -14% | -$72 | -$86 | -$107 | -$127 |
| In-wall kit add-on ($29) | $29 | $9.62 | $0.00 | $2.08 | $0.00 | $1.14 | $11.70 | **$16.16** | 56% | -$9 | -$23 | -$44 | -$64 |

### Contribution before ads at each quantity

| SKU | Qty 1 | Qty 20 | Qty 100 | Qty 500 |
|---|---|---|---|---|
| Kit 12" | -$224.17 | -$156.52 | -$19.90 | -$0.48 |
| Sconce, vintage | -$191.50 | -$123.85 | $12.77 | $32.19 |
| Sconce, named | -$170.95 | -$103.30 | $33.32 | $52.74 |
| 7" Kit (placeholder $59, not buildable yet) | -$11.55 | -$8.21 | $1.54 | $11.93 |
| Set, kit (not buildable yet) | -$183.93 | -$110.10 | $45.01 | $84.47 |
| Set, with records (not buildable yet) | -$120.58 | -$46.75 | $108.36 | $147.82 |
| In-wall kit add-on ($29) | $15.58 | $16.16 | $19.31 | $20.43 |

## 3. The 20 pre-sold units

Built at the Qty 20 prices, 20 twelve-inch units cost $4,226.60 in parts, of which $2,634.00 is twenty caps at the live 10-piece price of $131.70. Whatever those 20 buyers paid, the batch loses money unless the cap comes in far lower by email quote, or the first 20 ship with a stock chrome cap (Outwater STD-40CAP-PC, 1-1/4 in flat chrome cap on a 1/4-20 thread, $4.50, in stock) and that is said plainly to the buyers. With the $4.50 stock cap the 20-unit parts cost is about $84.13 each. That cap is flat, smaller than the design (31.75 mm against 38.1 mm) and its 3/4 in thread must be cut down to 12 mm; it has not been fitted.

## 4. What the cap price does (100 units)

| Cap price at 100 | 12" parts | $89 Kit clears | $99 Kit clears | $129 Sconce clears |
|---|---|---|---|---|
| $5.00 | $68.04 | -$9.90 | -$0.19 | $22.77 |
| $8.00 | $71.04 | -$12.90 | -$3.19 | $19.77 |
| $10.00 | $73.04 | -$14.90 | -$5.19 | $17.77 |
| $15.00 | $78.04 | -$19.90 | -$10.19 | $12.77 |
| $25.00 | $88.04 | -$29.90 | -$20.19 | $2.77 |
| $40.00 | $103.04 | -$44.90 | -$35.19 | -$12.23 |
| $121.36 | $184.40 | -$126.26 | -$116.55 | -$93.59 |

## 5. What would improve it, in order of size

1. A real cap quote. The RFQ packet is ready (`../cad/rfq/dome-cap-RS-CAP-12-revD.zip`) and has not been sent to anyone.
2. Strip: the Armacost UL reel is $4.28 a unit against $11.25, if its wattage is 5 W or less over 700 mm (not on its page; measure one reel).
3. Adapter: a quoted bulk price. $8.50 instead of $12.99 is worth $4.49 a unit. No published bulk price was found.
4. One adapter with the dimmer in the cord (GXILEE, $13.88) instead of adapter + dimmer ($16.98) saves about $3 and one connection.
5. Price. The Kit carries every hard part and none of the record margin. At $89 it is the worst SKU; at $119 to $129 it works.

## 6. Not checked

Home Depot MDF price (blocked), eBay 45 adapters (blocked), USPS rates on 11-11, any CNC or print-service quote, bulk prices for the pigtail, lock nuts, anchors, set screw and driver, foam and sleeve prices. These are marked E in `BOM.md`.
