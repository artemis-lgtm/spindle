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


## Product audit additions, 2026-11-11 evening (`../audits/AUDIT-product.md`)

These correct or add to the sections above. Sources are pages opened that day unless marked "secondary" (a reputable summary, not the primary text) or "not checked".

1. **The NEC rule that bites is 411, not only 410.6.** Lighting systems at 30 V or less must be a listed system or be assembled from listed parts, and being Class 2 does not exempt them (secondary: https://www.waveformlighting.com/home-residential/do-led-strip-lights-require-ul-listing ; the NFPA text itself was not readable). The Spindle fixture (wood disc, printed hub, our wiring) is neither a listed system nor only listed parts. The standard a lab would test it to is UL 2108, low voltage lighting systems, with UL 8750 for the LED parts (https://www.intertek.com/lighting/ul-2108-low-voltage-lighting-systems-fs ; https://iaeimagazine.org/columns/ul-question-corner/ul-question-corner-low-voltage-led-luminaire-drivers/). UL 1310 covers only the adapter. UL 1598 would apply to a hardwired version.
2. **Selling it unlisted is not a federal offence, but two places name sale.** Los Angeles Municipal Code 93.0402 requires electrical equipment to be approved or listed (https://dbs.lacity.gov/services/core-services/plan-check-permit/product-approval/electrical-test-lab). North Carolina GS 66-25 says electrical devices "shall be evaluated" by a qualified lab (https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/BySection/Chapter_66/GS_66-25.html). Chicago and New York City: not checked. Until the fixture is listed, do not ship to Los Angeles or North Carolina, or take advice first.
3. **2023 NEC renumbering.** Class 2 cable listing and installation moved to Article 722; Article 725 keeps the Class 2 circuit rules (https://cablinginstall.com/standards/article/14276764/revisions-to-cable-requirements-in-the-2023-national-electrical-code). Florida is still on the 2020 NEC, where it is all in 725. Site and card copy should say "Class 2 low-voltage wiring; check your local code" and not cite an article or say "legal everywhere".
4. **In-wall practicalities the card must state:** exterior and insulated walls and walls with horizontal fire blocking will stop the cable drop; the barrel connection ends up inside the wall where it cannot be reached; do not run the cable through a wall cavity used as an air return unless the cable is CL2P.
5. **Vinyl softening temperature was overstated.** Record compound starts to lose stiffness at 48 to 50 C and has a glass transition of 52 to 54 C (US patent 3,975,321, Table III, https://patents.google.com/patent/US3975321A/en), not 55 to 60 C. See `../cad/THERMAL.md`.
6. **A 24 V adapter fits the same jack.** A 12 V strip on 24 V overheats in seconds and the vendors call it a fire hazard (https://hitlights.com/blogs/premium-led-strip-lighting/can-you-use-a-12v-led-strip-on-a-24v-system). Nothing in the fixture prevents it. The "12 V DC ONLY" label is the only guard. Options are in the audit.
7. **Dimmer with a coin-cell remote = Reese's Law** (16 CFR 1263: warnings, secure battery door, certification). CPSC recalled a 390-unit LED strip product on exactly this in 2025 (https://www.cpsc.gov/Business--Manufacturing/Business-Education/Business-Guidance/Button-Cell-and-Coin-Battery). Use the inline knob dimmer with no remote, or comply.
8. **Recalls that look like our failure modes:** lighted mirrors whose glass came off the wall base (Lowe's, 2025), illuminated mirrors with loose parts overheating (RH, 2022, 3,300 units), LED fixtures whose plastic pins degraded and dropped the LED board (NetZero, 2025). All on cpsc.gov/Recalls. A printed plastic hub holding a 1 kg disc on a wall is the same family. The mount test (QC plan T2, T3) is a safety test, not a nicety.
9. **Duty to report.** Section 15(b): report to CPSC within 24 hours of information that reasonably supports a substantial hazard; up to 10 working days to investigate first (https://www.cpsc.gov/Business--Manufacturing/Recall-Guidance/Duty-to-Report-to-the-CPSC-Your-Rights-and-Responsibilities). Keep the serial number and lot records listed in the QC plan section 5 so a recall can be scoped.
10. **Prop 65: the small-business exemption did not protect a lookalike.** Vinylux, a small maker of products from recycled vinyl records, received a lead notice in 2015 and settled for $3,000 in penalties plus $21,500 in fees (https://oag.ca.gov/system/files/prop65/settlements/2015-00902S4760.pdf). Old PVC records can carry lead stabiliser; brass contains lead. A short-form warning on California orders costs nothing.
11. **MDF: we are a "fabricator" under TSCA Title VI.** Buy panels labelled TSCA Title VI compliant and keep the supplier's invoice or statement for 3 years. Finished goods with 144 square inches or less of composite wood are excepted from the labelling duty; a 10.5 in disc is about 87 (https://www.epa.gov/formaldehyde/frequent-questions-regulated-stakeholders-about-implementing-formaldehyde-standards).
12. **FCC.** The dimmer is an unintentional radiator and needs authorisation before marketing (47 CFR 15.101); when a system is assembled from parts the assembler is the responsible party (47 CFR 2.909). Buy a dimmer and adapter that carry an FCC statement and a named US responsible party, and keep the page.
13. **Adapter energy rule.** Check for the "VI" efficiency mark (10 CFR 430.32). California Title 20: flexible LED strips are not regulated per the Energy Commission FAQ (search snippet only, not confirmed).
14. **What a listing costs** (published figures, not quotes): about $6,000 for a single-luminaire safety evaluation (LD+A, Dec 2025, https://read.nxtbook.com/sage/lda/december_2025/safety.html); vendor blogs give $5,000 to $15,000 and 4 to 8 weeks for ETL, plus a factory inspection and roughly $3,500 a year in follow-up fees (weak source). QAI advertises batch certification for small runs (https://qai.org/electrical/testing-and-certification-for-lighting-products/). No lab has been asked.
15. **Insurance.** No authoritative source says insurers require a listing; typical product liability premiums for small sellers are $700 to $3,000 a year (https://www.insurancecanopy.com/product-liability-insurance). The $279 ACT policy is a crafters' programme: get "12 V plug-in electrical lighting is covered" in writing before relying on it.

Not checked: NFPA code text, Amazon Seller Central, Etsy, Walmart and Wayfair policy pages (login or 403), fcc.gov and ftc.gov guidance pages (403), Chicago and New York City code, any real lab quote.
