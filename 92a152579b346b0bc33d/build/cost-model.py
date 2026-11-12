#!/usr/bin/env python3
"""Record Sconces cost model. Single source of truth for cost-model.csv and the
numbers quoted in BOM.md / cost-model.md. Run: python3 cost-model.py
Every line carries a source tag. "est" = estimate, not a quoted price.
Tiers are per-unit cost when buying for 1 / 20 / 100 / 500 units.
Prices as fetched 2026-11-09 to 2026-11-10, then the 12 in unit re-opened line by line on 2026-11-11 (audits/AUDIT-product.md).
2026-11-11: the 12 in unit gained the two heat-safe rings and their screws (three lines above the box line).
The box line must stay LAST in PARTS_12 and PARTS_7: the Set total subtracts parts[-1]."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
TIERS = ["q1", "q20", "q100", "q500"]

# name, (q1, q20, q100, q500), source tag
# status: V = price confirmed on page by curl this session; P = confirmed 11/9 by an
# earlier report, page rate-limited/blocked tonight; S = search snippet; E = estimate
PARTS_12 = [
    # AUDIT 2026-11-11 (audits/AUDIT-product.md): every line below now describes the part the canonical CAD builds, and every
    # price was re-opened on the vendor page that day where the page would load. V = seen on the page 2026-11-11.
    ("Backplate RS-BP-12-MDF rev C, 10.5in x 1/2in MDF, CNC-cut both faces, painted matte black", (6.00, 5.00, 4.50, 3.50), "E (HD ProWood panel $14.58 = $1.82/disc + CNC + paint; Home Depot page not checked, blocks bots; no CNC shop quote)"),
    ("Hub RS-HUB-01 rev C, 5in x 1in PETG print", (6.00, 4.50, 3.00, 2.00), "E (PETG $0.02-0.03/g, about 175 g printed at 40% infill + machine time; no print-service quote)"),
    ("Threaded insert E-Z Lok 400-4 brass 1/4-20 x 0.5in", (1.90, 1.90, 1.70, 1.70), "V Albany County Fasteners $1.90 ea, $1.70 at 100, $1.50 at 1,000, in stock (the old $17.63 per 10 was the drive tool)"),
    ("Dome cap RS-CAP-12 rev D, turned C360 brass, one piece with its stud, mirror polish + chrome", (155.93, 131.70, 15.00, 10.00), "q1 and q20: V PCBWay guest pre-quote 2026-11-11, brass C360 + chrome ($155.93 at 1, $131.70 at 10, $121.36 at 50; 100 = manual quote). q100 and q500: E, NOT a quote, a placeholder. This is the biggest unknown in the model"),
    ("Felt washer under the cap, 1-1/4in x 3/8in x 1/16in adhesive felt, die-cut or punched in-house", (0.50, 0.40, 0.25, 0.15), "E no vendor picked (CS Hyde and Strouse take small runs, tooling paid by us, no published price)"),
    ("Centre backing ring, same felt blank, on the backplate front", (0.50, 0.40, 0.25, 0.15), "E same order as the cap felt"),
    ("PET label washer 37.5 x 7.5 x 0.25 mm, clear, matte one side", (0.40, 0.30, 0.15, 0.10), "E no vendor picked"),
    ("Felt pads x6, 1/2in OD x 1/16in self-adhesive (Durofelt SAW12BK-100)", (0.42, 0.42, 0.42, 0.36), "V Durofelt $7.00/100, in stock; no second source found"),
    ("45 rpm snap-in adapter (ships in every box)", (0.50, 0.50, 0.15, 0.13), "P eBay $36.99/250 (eBay not checked 2026-11-11, blocks bots); qty1 local shop est"),
    ("LED strip 12V warm white 8 mm, 4 W class, listed, 700 mm as seven 100 mm pieces", (12.59, 11.25, 11.25, 9.00), "V Ecolocity Ribbon Star 2835 60/m 1.46 W/ft ETL: $17.99 per 1 m, $44.99 per 3 m (4 units), in stock; the page says 2900-3200K, not 2700K. q500 E. Unverified cheaper option: Armacost 131232 UL 2700K $29.99 per 5 m ($4.28 a unit), wattage not on its page"),
    ("Strip jumpers x6 (22 AWG pair, 15 mm) + heat shrink", (0.30, 0.25, 0.15, 0.10), "E; needed because a flat strip cannot bend sideways into a ring"),
    ("Power adapter UL Class 2 12V 2A 24W, 5.5x2.1 barrel, 6 ft", (12.99, 12.99, 12.99, 9.00), "V LED Updates $12.99 (was $11.99); no bulk price published; q500 E. Second source GXILEE B09J4KCY4T $13.88 with a dimmer in the cord"),
    ("Inline PWM dimmer 12-24V 2A, barrel in/out (Ecolocity LC-OL-8DIM)", (3.99, 3.99, 3.99, 3.00), "V Ecolocity $3.99 SALE price (list $12.99) with 7 in stock: 100 cannot be bought there today. Second source Super Bright LEDs LDP-2A $7.99, out of stock. q500 E"),
    ("Power pigtail, 150 mm 18 AWG with inline FEMALE 5.5x2.1 jack", (4.00, 4.00, 2.00, 1.00), "q1 V cctvcameraworld $4.00 (5 in lead, wire gauge not stated); bulk E, not looked up"),
    ("Steel wall plate RS-WP-01 rev B, G90 galvanized 0.074in, laser cut + one bend + 3 PEM FH-832-10 studs pressed, no finish", (33.24, 9.22, 6.40, 6.40), "V SendCutSend guest quote of the REV B file cad/parts/RS-WP-01_flat.dxf, 2026-11-11 21:10: accepted with bend and 3 studs, no hole collision. $33.24 at 1, $9.22 at 10, $6.73 at 50, $6.40 at 100, $5.11 at 1,000; q20 uses the 10 price, q500 the 100 price. Black powder coat on mild steel instead: $48.12 / $13.33 / $8.69"),
    ("8-32 nylon-insert lock nuts x3", (0.30, 0.25, 0.22, 0.15), "E not looked up"),
    ("M3 x 12 set screw + M3 heat-set insert + 1.5 mm x 100 mm straight hex driver", (3.50, 2.50, 1.80, 1.20), "insert V Adafruit 4255 $5.95/50; screw and driver E. A 45 mm L key cannot reach the screw, it is 70 mm in under the backplate"),
    ("Wall screws #8 x 1-1/4in x2 + 2 named flangeless anchors (Toggler Alligator class)", (0.80, 0.60, 0.45, 0.35), "E no price captured"),
    ("Silicone bumpers x2 clear self-adhesive", (0.13, 0.13, 0.13, 0.10), "V eBay 100/$6.51, 1 to 2 weeks"),
    ("Lead wire 18 AWG 12in, heat shrink", (0.30, 0.25, 0.15, 0.10), "E"),
    ("Hang + safety card, printed", (0.50, 0.40, 0.20, 0.10), "E"),
    # Heat-safe halo, added 2026-11-11 (cad/FIXES-heat-layout.md). Evidence: sourcing/quotes-2026-11-11/README.md
    ("Aluminium heat ring RS-HR-12, 5052-H32 0.040in, OD 260 ID 200, 4 holes, laser cut", (27.10, 13.83, 7.38, 7.38), "V SendCutSend guest quote of the canonical cad/parts/RS-HR-12.dxf, re-confirmed 2026-11-11 evening: $27.10 @1, $13.83 @10, $7.38 @100; q20 uses the 10 price, q500 the 100 price"),
    ("Cork ring RS-CK-12, 1/16in cork, OD 260 ID 200, 4 punched holes, cut in-house", (1.89, 1.89, 1.89, 1.49), "V material: WidgetCo 1/16in x 12in x 30ft roll $66 ($52 at 5 rolls) = 35 rings; the page shows no adhesive back and calls it both 1/16 inch and 2 mm; cutting labour is in LABOR. Second source The Cork Store CR117 1.5 mm, peel-and-stick option, about $1.00 a ring"),
    ("Heat-ring screws x4, #4 x 3/8in pan head sheet-metal", (0.20, 0.16, 0.12, 0.08), "V Tanner Bolt $2.90 per 100 (thread type not stated on the page)"),
    ("Box 13x13x3 + foam corners + inner poly sleeve + cap pouch", (5.00, 4.50, 3.50, 2.75), "box V Uline S-19090 $1.62 at 25, $1.48 at 100 (200 lb single wall, NOT double wall); foam, sleeve and pouch E"),
]
PARTS_7 = [
    ("Backplate 6in x 1/2in MDF, CNC-cut, painted", (3.00, 2.50, 2.00, 1.50), "E same panel, 20+ discs"),
    ("Hub, 4in x 1in PETG print", (4.50, 3.50, 2.25, 1.50), "E"),
    ("Threaded insert E-Z Lok 400-4", (1.90, 1.76, 1.70, 1.60), "V Albany"),
    ("7in cap (chromed 45-adapter look) - PENDING, carried at 12in dome cost", (5.15, 4.65, 3.40, 2.65), "E pending dome-cap"),
    ("Felt washer 1in OD", (0.16, 0.16, 0.16, 0.14), "V Durofelt"),
    ("Felt pads x3", (0.21, 0.21, 0.21, 0.18), "V Durofelt"),
    ("45 rpm adapter", (0.50, 0.50, 0.15, 0.13), "P eBay"),
    ("COB LED strip ~1.6 ft (19in rim)", (2.75, 2.20, 1.40, 1.10), "E"),
    ("Power adapter UL 12V 2A", (12.99, 12.99, 12.99, 9.00), "V LED Updates $12.99; q500 E"),
    ("Inline PWM dimmer", (3.99, 3.99, 3.99, 3.00), "V Ecolocity sale price, 7 in stock"),
    ("Power pigtail with inline female jack", (4.00, 4.00, 2.00, 1.00), "q1 V cctvcameraworld; bulk E"),
    ("Keyhole plate heavy gauge (Hardwick & Sons) + #8 screw + anchor", (0.75, 0.75, 0.60, 0.50), "P Hardwick $0.45; SOLD OUT on 2026-11-11, no second source"),
    ("Silicone bumpers x2", (0.13, 0.13, 0.13, 0.10), "P eBay"),
    ("Lead wire, heat shrink", (0.30, 0.25, 0.15, 0.10), "E"),
    ("Hang card", (0.50, 0.40, 0.20, 0.10), "E"),
    ("Box 10x10x3 + foam + sleeve", (3.50, 3.00, 2.25, 1.75), "E"),
]
INWALL_KIT = [
    ("Screw-terminal barrel plug pair 5.5x2.1 (Oiyagai 10 pr $13.50)", (1.35, 1.35, 0.50, 0.50), "inwall-parts: S Amazon B07D67B3HM; bulk E"),
    ("CL2 18/2 in-wall cable, 8 ft (Monoprice 50 ft $18.54)", (3.00, 3.00, 1.60, 1.20), "inwall-parts: S Monoprice p_id 4044; 1000 ft reel est"),
    ("Arlington LV1 old-work low-voltage bracket", (1.80, 1.80, 1.10, 0.95), "V avoutlet $1.80; eBay 10/$10.99 S; 500 E"),
    ("Datacomm 45-0001-WH recessed LV plate", (3.45, 2.97, 2.97, 2.50), "V zackelectronics $3.45, $2.97 @20+; 500 E"),
    ("Pull string + drill-size card + bag", (0.60, 0.50, 0.30, 0.20), "E pending"),
]
RECORD_ANON = 2.00    # scope report: $0.50-3 craft grade; use $2
RECORD_NAMED = 30.00  # scope report: $20-40 marquee title in player grade

# Labor at $25/hr. AUDIT 2026-11-11: the heat-safe halo added a ring sub-assembly (cut and punch the cork, lay seven strip
# pieces, solder six jumpers, four screws): 25 min became 40 min, 20 min became 32 min. Timed on nothing; nothing is built.
LABOR = {"q1": 40/60*25, "q20": 40/60*25, "q100": 32/60*25, "q500": 28/60*25}
LABOR_7 = {k: v*0.7 for k, v in LABOR.items()}
LABOR_SET_EXTRA = 5/60*25  # packing three units in one box

# Shipping: USPS Ground Advantage Commercial (Pirate Ship pricing) from Notice 123,
# fetched 2026-11-10 from https://pe.usps.com/text/dmm300/Notice123.htm
GA_CUBIC_030 = {1: 8.79, 2: 8.85, 3: 9.21, 4: 9.63, 5: 11.51, 6: 13.38, 7: 14.03, 8: 15.22}  # 13x13x3 = 0.293 cu ft
GA_CUBIC_020 = {1: 8.22, 2: 8.29, 3: 8.54, 4: 8.74, 5: 9.92, 6: 11.21, 7: 11.60, 8: 12.39}   # 10x10x3 = 0.174 cu ft
GA_WT_3LB = {1: 9.04, 2: 9.06, 3: 9.54, 4: 10.07, 5: 12.12, 6: 14.14, 7: 14.91, 8: 16.30}
GA_WT_4LB = {1: 9.93, 2: 9.99, 3: 10.35, 4: 11.30, 5: 13.89, 6: 16.21, 7: 17.24, 8: 19.06}
GA_WT_7LB = {1: 10.61, 2: 10.67, 3: 11.27, 4: 12.55, 5: 15.95, 6: 18.70, 7: 20.28, 8: 22.88}  # Set box, 14x14x5 is >0.5 cu ft so no cubic
# Zone mix for a national US customer base shipped from Fort Lauderdale FL (estimate):
ZONE_MIX = {1: 0.01, 2: 0.02, 3: 0.03, 4: 0.06, 5: 0.15, 6: 0.33, 7: 0.17, 8: 0.23}
INSURANCE_EXTRA = 1.50  # est: Pirate Ship includes $100 on GA; top-up to item value
def blend(tbl): return sum(tbl[z]*w for z, w in ZONE_MIX.items())
SHIP_12 = blend(GA_CUBIC_030) + INSURANCE_EXTRA
SHIP_7 = blend(GA_CUBIC_020) + INSURANCE_EXTRA
SHIP_SET = blend(GA_WT_7LB) + INSURANCE_EXTRA

STRIPE_PCT, STRIPE_FIX = 0.029, 0.30  # V stripe.com/pricing 2026-11-10

PRICES = {  # BRIEF.md
    "Kit 12in": 89.00,
    "Sconce 12in (vintage record)": 129.00,
    "Sconce 12in (named title)": 179.00,
    "7in Kit": 59.00,            # NOT in BRIEF; derived so the Set = 89 + 2x~80, flagged open
    "Set kit (12in + two 7in)": 249.00,
    "Set with records": 329.00,
    "In-wall kit add-on": 29.00,  # NOT in BRIEF; proposal
}
CPAS = [25, 39, 60, 80]

def total(parts, t):
    i = TIERS.index(t)
    return sum(p[1][i] for p in parts)

def sku_rows():
    rows = []
    for t in TIERS:
        p12 = total(PARTS_12, t); p7 = total(PARTS_7, t)
        box12 = PARTS_12[-1][1][TIERS.index(t)]; box7 = PARTS_7[-1][1][TIERS.index(t)]
        setbox = {"q1": 7.00, "q20": 6.00, "q100": 4.50, "q500": 3.50}[t]
        pset = (p12 - box12) + 2*(p7 - box7) + setbox + 0.50  # one card
        defs = [
            ("Kit 12in", p12, 0, LABOR[t], SHIP_12),
            ("Sconce 12in (vintage record)", p12, RECORD_ANON, LABOR[t] + 10/60*25, SHIP_12),
            ("Sconce 12in (named title)", p12, RECORD_NAMED, LABOR[t] + 10/60*25, SHIP_12),
            ("7in Kit", p7, 0, LABOR_7[t], SHIP_7),
            ("Set kit (12in + two 7in)", pset, 0, LABOR[t] + 2*LABOR_7[t] + LABOR_SET_EXTRA, SHIP_SET),
            ("Set with records", pset, RECORD_ANON*3, LABOR[t] + 2*LABOR_7[t] + LABOR_SET_EXTRA + 20/60*25, SHIP_SET),
            ("In-wall kit add-on", total(INWALL_KIT, t), 0, 5/60*25, 0.0),  # ships in the sconce box
        ]
        for name, parts, rec, lab, ship in defs:
            price = PRICES[name]
            stripe = price*STRIPE_PCT + STRIPE_FIX
            landed = parts + rec + lab + ship
            contrib = price - landed - stripe
            r = {"tier": t, "sku": name, "price": price, "parts": parts, "record": rec, "labor": lab,
                 "shipping": ship, "stripe": stripe, "landed_cost": landed, "contribution_before_ads": contrib,
                 "margin_pct": contrib/price*100, "breakeven_cpa": contrib}
            for c in CPAS: r[f"net_at_cpa_{c}"] = contrib - c
            rows.append(r)
    return rows

if __name__ == "__main__":
    rows = sku_rows()
    with open(os.path.join(HERE, "cost-model.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows: w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    with open(os.path.join(HERE, "BOM.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["sku", "part", "q1", "q20", "q100", "q500", "source"])
        for sku, parts in [("12in (kit and sconce)", PARTS_12), ("7in kit", PARTS_7), ("in-wall kit", INWALL_KIT)]:
            for p in parts: w.writerow([sku, p[0], *p[1], p[2]])
            w.writerow([sku, "TOTAL parts", *[round(total(parts, t), 2) for t in TIERS], ""])
    print(f"ship blended: 12in ${SHIP_12:.2f}  7in ${SHIP_7:.2f}  set ${SHIP_SET:.2f}")
    for t in TIERS:
        print(f"\n== {t}: parts 12in ${total(PARTS_12,t):.2f} | 7in ${total(PARTS_7,t):.2f} | inwall ${total(INWALL_KIT,t):.2f}")
        for r in rows:
            if r["tier"] == t:
                print(f"  {r['sku']:<32} price {r['price']:>6.0f} landed {r['landed_cost']:>6.2f} stripe {r['stripe']:>5.2f} contrib {r['contribution_before_ads']:>6.2f} ({r['margin_pct']:.0f}%)  net@25/39/60/80: " + " / ".join(f"{r[f'net_at_cpa_{c}']:.0f}" for c in CPAS))
    # cash for first 100 units at q100 tier: 70 sconces (60 vintage, 10 named) + 30 kits
    t = "q100"; p12 = total(PARTS_12, t)
    parts_cash = 100*p12
    records_cash = 60*RECORD_ANON + 10*RECORD_NAMED
    cap = [p for p in PARTS_12 if p[0].startswith("Dome cap")][0][1][2]
    kit = [r for r in rows if r["tier"] == "q100" and r["sku"] == "Kit 12in"][0]["contribution_before_ads"]
    print(f"\nCap sensitivity at 100 (the cap is carried at ${cap:.2f}, an estimate): Kit contribution before ads")
    for c in (8, 15, 25, 40, 121.36):
        print(f"  cap ${c:>6.2f}: 12in parts ${p12 - cap + c:>7.2f}, $89 Kit clears ${kit + cap - c:>7.2f}, $99 Kit clears ${kit + cap - c + 10*(1-STRIPE_PCT):>7.2f}")
    print(f"\nCash, first 100 x 12in (70 sconce/30 kit): parts ${parts_cash:,.0f} + records ${records_cash:,.0f} = ${parts_cash+records_cash:,.0f}")
    print(f"  plus shipping at ship time 100 x ${SHIP_12:.2f} = ${100*SHIP_12:,.0f}; labor 100 x ${LABOR[t]:.2f} = ${100*LABOR[t]:,.0f}")
