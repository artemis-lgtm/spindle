# Safety and electrical compliance

Written 2026-11-10. Not an electrician's opinion. Design facts from engineering-report.md and mounting-report.md: 12 V DC COB LED ring 8 to 10 W, UL-listed Class 2 plug-in adapter with inline dimmer, nothing above 12 V inside our housing.

## 1. The architecture is the safety case

All 120 V lives inside a UL-listed Class 2 adapter (UL 1310 Class 2 power units, https://www.ul.com/services/class-2-power-supplies; estimate on the exact page). Class 2 caps output at 100 VA and is treated as low shock and fire risk by code. Our parts (wood or aluminum backplate, PETG hub, steel plate, brass cap) carry 12 V DC only.

Rules that protect that:
- Ship only a listed adapter, and check its UL or ETL file number on UL Product iQ (https://productiq.ulprospector.com/) before buying in volume. sourcing/ flagged the Alibaba "UL" adapter and COB claims as unverified; HitLights COB has UL file E362417 (verified per sourcing/README).
- Never a 120 V option inside our housing in batch one or two.
- Adapter never goes inside a wall (on the card and in terms already).

## 2. In-wall wiring (the default install)

Low-voltage Class 2 cable may run inside a wall without conduit when it is rated CL2 or better (NEC Article 725 in the 2020 NEC, which the 8th edition Florida Building Code adopts; https://www.floridabuilding.org/c/default.aspx). The 2023 NEC reorganised these rules into Articles 722, 724 and 725; same substance, different numbers, so cite "NEC power-limited Class 2 rules" in customer copy, not an article number. Our in-wall kit uses CL2 18/2 (Diode LED, sourcing/).

## 3. What needs an electrician

| Install | Electrician? | Why |
|---|---|---|
| A: surface cord or raceway | No | Plug-in, cord-connected, like any LED strip kit. |
| B: in-wall CL2 to a low-voltage jack plate (default) | No in most homes | Low-voltage only in the wall; the adapter plugs into an existing outlet. Renters: lease, not code. |
| C: hardwired to a junction box with a Class 2 driver | Yes | 120 V work. And NEC 410.6 requires luminaires to be listed, which an inspector sees on a hardwired install. |

## 4. The gap we should name honestly (conflict with current site copy)

NEC 410.6 says luminaires shall be listed. A finished Spindle is not a listed luminaire; it is assembled from listed components. For A and B that is the same position as every plug-in LED strip kit and Etsy lighting maker (scope-report.md section 1). But the site FAQ currently says "Low-voltage Class 2 cable is allowed inside walls without conduit in every US jurisdiction that follows the NEC" and "No electrician." Both are defensible for B, but "every US jurisdiction" overreaches (some cities, Los Angeles is the one cited in scope-report.md, treat any unlisted product as unsellable). Recommendation: soften to "allowed inside walls in most US homes under the National Electrical Code; check local rules if you're unsure." Not edited yet, waiting on Austin's word since it touches launch copy.

Longer term, a whole-fixture listing to UL 2108 (low-voltage lighting systems) through ETL/Intertek is the path if option C or retail wholesale ever matters. Estimate $5,000 to $15,000 and 8 to 12 weeks; scope-report.md cites $10,000+ for UL 153. Not needed to launch.

## 5. CPSC

No mandatory CPSC standard covers a 12 V decorative wall light. Two obligations still apply from the first sale:
- Duty to report: if we learn of a defect that could create a substantial hazard (a fire, a burn, a fall), Section 15(b) requires a report to CPSC within 24 hours of knowing (https://www.cpsc.gov/Business--Manufacturing/Recall-Guidance/Duty-to-Report-to-the-CPSC-Your-Rights-and-Responsibilities).
- Keep a build log: unit serial, date, parts batch. The warranty card already has serial and date lines.

## 6. California Prop 65

Prop 65 only binds businesses with 10 or more employees (https://www.p65warnings.ca.gov/new-proposition-65-warnings/businesses), so we are exempt as sellers today. Two caveats: brass (lead content) and PVC cords and vinyl records are the usual triggers, and marketplaces (Amazon, Etsy) and wholesale buyers often demand the warning anyway. When either happens, add the short-form warning for lead (brass) to the product page and box. Estimate, confirm then.

## 7. Heat and mounting tests before batch two ships

build/QC-test-plan.md already defines them: 2-hour heat soak (record face under 35 C), pull, drop, twist, swap, and ISTA 3A-lite packaging drop. Run on the sample run, publish the heat numbers as the FAQ promises.

## Open
- Soften the "every US jurisdiction" FAQ line (Austin's call).
- Verify UL/ETL file numbers on the adapter and COB actually bought.
- Electrician review of ops/policies/safety-install.md before printing the card.
