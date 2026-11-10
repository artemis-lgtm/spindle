# sourcing/ : what is here, where it came from, what is open

Made overnight 2026-11-09 by the sourcing agent. Design decisions were taken as fixed from BRIEF.md, NOTES.md and the four reports; nothing was relitigated. No emails sent, no orders, no accounts, no payments.

## Files

vendors.md: one table per part (chrome dome cap, steel wall plate, backplate, hub, COB strip and UL adapter, in-wall kit, fasteners and felt, packaging, bulk records), 2 to 9 real vendors each with price, MOQ, lead time, URL and the HTTP result of tonight's fetch. Live prices are marked live; snippet-only prices and my estimates are marked as such.

sample-run-plan.md: the exact shopping list for 8 bodies (6 x 12", 2 x 7") plus 5 in-wall kits, by vendor, with a $1,300-1,700 total and a day-by-day timeline. Parts in hand in about 3 weeks (the chrome caps from Shenzhen are the long pole); photos possible at day 10 with brass knobs standing in or with three fast nickel caps from Xometry.

production-100-500.md: per-unit parts cost at 100 and 500 on a US path and a mixed path, margin check at $89 / $129 / $249, cash needed, and a lead-time table. Body parts land at about $57 (100, US), $41 (100, mixed), $45 (500, US), $29 (500, mixed). That is $12-15 above the engineering report's $27 because the decided mount (custom chrome dome, PEM-studded powder-coated plate, J-slot hub) replaced a $1.80 knob and a $0.41 keyhole.

rfq-drafts/: 13 ready-to-send emails (PCBWay, JLCCNC, Alibaba turned-parts shops, R & H Plating Fort Lauderdale, CNC Cut Service of Homestead, Market Wood Hialeah, HitLights wholesale, Adled COB strip, Anen Power UL adapter, Diode LED CL2 wire, Record Head, Custom Foam Parts, Pulp Packaging). Plain paragraphs, sender artemis@higneyintl.com cc austin@higneyintl.com, brand name left as "a wall sconce product line".

plate_4in.dxf and hub_127.stl: envelope-only placeholder geometry I generated from the mounting-report dimensions so instant-quote tools could price the size class. Not for vendors. The real STEP/DXF must be exported from render/sconce_v2.py.

## Live numbers worth knowing

Craftcloud (no account needed) quoted 10 PETG hubs at $69.51 plus $13.38 shipping, $8.29 each landed. Uline S-19090 13x13x3 is $1.62 at 25 and $1.17 at 1,000. Albany E-Z Lok 400-4 is $1.90 single, $170 per 100. HitLights 12V COB 2700K CRI90 reel is $37.28 with UL file IFDR.E362417 (holder HIT International Consulting LLC per UL Product iQ index). Checkered Records: 20 VG+ LPs $69, 100 for $250, free shipping. Durofelt 1" felt washers $8 per 50. Rockler brass knob $7.99 per 4. SendCutSend published 100-unit powder-coated examples $4.30 to $18.97 each.

## What is open

SendCutSend, PCBWay, JLCCNC, Xometry, Fictiv and Protolabs all need an account to show a price; Austin creates the accounts (or hands me a login) and I upload the real CAD. Packlane's configurator ignored my custom size and loaded a default box; a custom 13x13x3 quote still needs a few clicks in their editor. Dusty Groove is behind Cloudflare, Amazon, eBay, Home Depot, Monoprice, Cmple and Digi-Key block the scraper, so their prices are from search snippets. The Alibaba UL claims (Adled strip, Anen adapter) are unverified until the E-numbers come back and are checked on UL Product iQ. The session's web-search budget ran out two-thirds through, so Broward machine shops with a lathe are thin: APB (router and waterjet, no lathe) and R & H Plating are confirmed; a local turning shop still needs a phone call or the R & H referral in the RFQ. Brand name is still open and appears nowhere in the drafts.
