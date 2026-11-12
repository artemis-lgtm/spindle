# Spindle website audit (pessimist pass, 2026-11-11)

Auditor: claude-fable-5-2. Scope: `projects/record-sconces/site/` only. Nothing deployed, sent, bought or committed.

## Verdict

Mechanically the site was already clean (no horizontal scroll, no console errors, no broken links, light pages). The words were the problem. The site described a product that does not exist yet as if it had been built, shipped to 20 people and tested: "hand-built", "went to friends who saw the prototype on a wall", "collectors tell us", a UL claim covering parts nobody has bought, a weight that is off by about a pound, a heat pass mark twice as loose as the engineering one, and a reserve button that, in its unconfigured state, told a visitor "your deposit is in" without taking a cent. All of that is fixed in the generator and regenerated. The site is now honest and follows the page laws below (25 of 30, from 10), but it still cannot sell: there is no ship date, no checkout link, no email address, no real photograph and no real customer voice. Those five need Austin, not code.

## Second pass, same day: facts from the product audit

After the first pass the product auditor sent findings that change site copy (`audits/AUDIT-product.md`). I read the cited lines there before acting, did not re-derive its sources, and took the more cautious wording in every case. Applied in the generator and rebuilt; the audit and click-through scripts were re-run afterwards (0 overflow, 0 errors on 14 pages x 2 sizes; flow output unchanged except "swatches on page: 0").

| Product-audit fact | Site before | Site now |
|---|---|---|
| Record vinyl loses stiffness at 48 to 54 C (118 to 129 F), not 55 to 60 C | "Vinyl starts to soften around 130 to 140 F" | "Record vinyl starts to lose its stiffness at roughly 120 F" (FAQ, install page, heat card) |
| The only priced listed 4 W strip is 2900 to 3200 K | "2700 K" in a heading, the FAQ and the spec table | No colour number anywhere. "Warm white ... The exact strip is not chosen yet, so we do not quote a colour number." The home heading "Twelve inches of what you love, lit at 2700 K." now ends "lit from behind." (this edits a brand tagline; Austin to confirm) |
| Brass and black caps are not real parts | Three finishes, picker on three pages | `FINISHES_OPEN = False`: chrome only, no picker, no brass or black render used, "Brass and black are ideas we like and have not engineered yet, so we are not selling them." |
| `bedroom_*` shows a 4 W strip lighting a whole room | Used on the home page and in the gallery (my first pass added it) | Removed. Gallery uses `macro` instead |
| Renders need a "real glow may differ" line | "Computer renderings" only | Added to the room image and the product gallery captions |
| Los Angeles and North Carolina require a listed fixture | Not mentioned | `NO_SHIP_PLACES`: stated on the shipping page and in the UL answer |
| In-wall wiring: say "Class 2 low-voltage wiring, check your local code" | "allowed inside walls in most US homes under the National Electrical Code" | Reworded to exactly that, no code citation |
| Parts are $78.04 at 100 at live prices (`build/cost-model.md`, read by me); the $89 Kit loses $19.90 an order before ads, $99 about $10 | Comment on `KIT_PRICE` said $89 clears about $16 | Comment now quotes cost-model.md and marks the old figure superseded. Price still not chosen |

Score effect: law 12 (few choices) goes to 2, total 25 / 30. Law 15 stays at 1 because the hero is still a pre-change render.

## How I checked (all run in this session)

- Served `site/` with `python3 -m http.server 8739`, loaded every page at 390x844 (2x, touch) and 1440x900 in headless Chromium via Playwright, before and after. Script: scratchpad `audit.py`. Server killed afterwards (`curl` returned 000).
- Clicked the reserve path, the waitlist form, the version picker, the gallery, the mobile menu and the thank-you pages. Script: scratchpad `flow.py`.
- Looked at the screenshots (fold and full page, both sizes).
- Compared every product claim with `cad/THERMAL.md`, `cad/FIXES-heat-layout.md`, `build/BOM.md`, `NOTES.md`, `ops/safety.md` and `ops/policies/*.md`.
- Grepped the built pages for the strings `cad/gates.py` requires and forbids.

Screenshots: `site/screenshots/audit-2026-11-11/before/` (48 images + results.json) and `.../after/` (56 page images, 6 flow images, results.json).

Result table, after the fixes (from `after/results.json`):

| Check | Before | After |
|---|---|---|
| Horizontal overflow, 12 then 14 pages x 2 sizes | 0 px on all | 0 px on all |
| Console errors / failed requests / 4xx | 0 / 0 / 0 | 0 / 0 / 0 |
| Images without alt / broken images | 0 / 0 | 0 / 0 |
| Internal links and anchors that go nowhere | 0 | 0 |
| Home page weight, mobile | 235 KB, 14 requests | 272 KB, 16 requests (two room images added, lazy) |
| Product page weight, mobile | 370 KB | 246 KB (thumbnails moved from JPEG to WebP) |
| Largest image on first paint | sq-chrome WebP, 25 KB | same |
| `[SHIP DATE]` or example.com visible on a page | every page | every page (needs Austin; build now has a launch check) |
| 404 page | server default | `404.html` exists |

Headless Chromium on a local server is not evidence about real mobile Safari or a real network. Load times are not reported for that reason.

## Findings, worst first

### 1. The site wrote about an unbuilt product as if it existed (fixed)

Nothing has been built or measured (`cad/THERMAL.md`: "Nothing has been measured"; NOTES 2026-11-11). The old copy said otherwise. Line numbers are from `site/_gen/pages.py` as it stood before this audit (backup of the old generator: scratchpad `_gen.orig/`).

| Old line | Old claim | Why it is false or unprovable | Now |
|---|---|---|---|
| pages.py 440 | "The first 20 went to friends and the people who saw the prototype on a wall" | There is no prototype | "The first 20 were spoken for before this site went up. Those get built and tested first." |
| 226 | "20 of 20 ... Every unit hand-built in Fort Lauderdale" | No unit is built | "First batch sold out before this site went up. Those ship first." |
| 45 | "Collectors tell us this is the whole reason they want the Kit" | Invented testimonial | Deleted |
| 49 | "many renters do it anyway" | Invented | Deleted |
| 263 | "Photographs of the batch-one units replace these as they are shot" | Implies units exist | "Computer renderings of the design, not photographs. No unit has been built yet." |
| 434, build.py 77 | "Built in Fort Lauderdale", "Made in Fort Lauderdale" | Not built; and "Made in" is an origin claim the imported LED strip and adapter cannot support | "Designed in", "To be assembled by hand in" |
| 41 | "Will the light warp my record? No." | An absolute on a calculation | "It is designed not to, and we will test it on real units before anything ships", with the numbers labelled calculated |
| 41, 406 | Pass mark "record face under 95 F in a 75 F room" (20 F rise) | THERMAL.md accepts no more than 5 K, which is 9 F | "within 9 F of the room" |
| 51 | "throws an amber halo about 4 inches past the edge" | Never measured, and the renders were lit before the layout change | "glows on the wall around the record" |
| 53 | "Picture discs and coloured vinyl look spectacular with light behind them"; "Warped records ... still hang fine" | The light is behind an opaque backplate; neither tried | "including coloured vinyl and picture discs. A badly warped record will not sit flat." |
| 319 | "Weight: about 1.5 lb with record" | Backplate 705 cm3 of MDF is about 530 g, hub 200 to 250 g (BOM), heat ring 58 g and cap 55 g (checks.md), plate about 100 g, record about 140 g: roughly 1.1 to 1.2 kg | "Roughly 2.5 lb with a record. Calculated from the design, not yet weighed." |
| 35, 210, 211 | "one turn", "two turns" | Thread engagement not specified to the customer anywhere | "a few turns" |
| 270 | "Designer ringed-disc sconces run $740 to $755; this one holds a real record" | One reference (a $755 lamp) stretched into a market claim | Deleted |
| 168 | "The record floats an inch off the plaster" | Record face is 1.62 in from the wall; the backplate is 1 in | "about an inch and a half off the wall" |

### 2. UL and electrical wording over-claimed (fixed)

- Old FAQ (pages.py 63): "The parts that touch mains power or run inside your wall are UL or ETL listed: the 12-volt adapter, the LED strip and the cable." The strip and cable are not bought, `ops/safety.md` says the file numbers still need checking, and the strip does not touch mains. Now: "The Spindle itself is not UL listed. The plug-in power adapter we ship is a UL-listed Class 2 adapter ... If your building or landlord requires the whole light fixture to be listed, this is not the right product for that wall yet." Every UL sentence on the built site now refers to the adapter only (listed by script; 14 pages carry "The Spindle is not UL listed; its plug-in power adapter is" in the footer).
- Old Kit box (297): "12 V UL-listed dimming adapter". The BOM has a listed adapter (line 9) plus a separate, unlisted inline dimmer (line 10). Now two separate items.
- Old FAQ (47): cable allowed in walls "in every US jurisdiction that follows the National Electrical Code". `ops/safety.md` section 4 flagged this as over-reach. Now "in most US homes ... check your local rules, or ask an electrician".
- Old install page (392 to 394) offered "Option C: hardwired, by your electrician" with "a one-page sheet for the electrician". `ops/safety.md`: NEC 410.6 wants a listed luminaire on a hardwired install and the Spindle is not one. Option C is removed; the page says "Not for hardwiring."
- Old install page (381): in-wall kit "sold as an add-on at checkout". Checkout is a $25 Stripe link with no add-ons, and the kit has no price (BOM: "not set"). Now: offered when you pay the balance, price shown before you pay.

### 3. The deposit flow could tell someone their money was taken when it was not (fixed), and still has no real checkout (needs Austin)

- With the placeholder Stripe link, every reserve button went to `thanks-deposit.html`, which said "Your Spindle is held ... your $25 deposit is in" and fired a Meta Purchase event. Anyone opening that page directly got the same. Now: demo mode shows a red "TEST MODE. Nothing was sent and no payment was taken" banner; opening the page without a Stripe `session_id` shows "No hold found on this page"; Purchase fires only with a session id. Verified: `flow.py` lines 6, 7, 8.
- The waitlist form accepted "notanemail" and did not enforce the consent box (the form is `novalidate` and the script returned early without stopping the submit). Now it stops and shows a message. Verified: `flow.py` lines 9, 10, 11.
- Old copy said "the balance is charged when your unit is ready". A Stripe Payment Link cannot charge later. Now: "we email you a link to pay the rest. Nothing is charged automatically", which matches `ops/policies/shipping.md`.
- Old copy said "Shipping address and record preference are collected at checkout." Not known to be true of the link. Now: "We ask for your shipping address before we ship, not today."
- New: `python3 _gen/build.py --launch-check` exits 1 and lists six blockers (ship date, Stripe link, waitlist endpoint, contact email, pixel id, domain). It currently prints "6 blockers, do not deploy".

### 4. Deposits for an unbuilt, untested, non-listed light were not described honestly (fixed in copy; the date is Austin's)

The old reserve block promised "Ships the week of [SHIP DATE]" with "we do" have a reasonable basis (shipping page), for a product with no prototype. The FTC guide (opened): "you must have a reasonable basis for stating or implying that you can ship within a certain time." Aptera's reservation page (opened) shows the pattern for an unfinished product: "$100 Due Today", "Vehicle shown is in testing and validation; specifications are subject to change."

Now, next to every reserve button: "Where this stands today. Spindle is designed and engineered, and the first units have not been built yet. Nothing ships until our heat test on real units passes. That is why today is a refundable $25 hold and not a purchase." The reserve card lists: refundable within 5 business days, not built yet, planned ship week is an estimate, you pay the rest by emailed link, capped at 100. The footer of every page repeats it in one paragraph.

### 5. The site sold a version that is not engineered (switched off, needs Austin)

The Spindle Set includes two 7-inch singles. `cad/FIXES-heat-layout.md`: the 7-inch "was NOT moved to this layout", its record still overhangs a rim strip, and its cap is unquoted. Every heat sentence on the site describes the 12-inch. `SET_OPEN = False` in `site/_gen/pages.py` now removes the Set from the picker, the footer, the JSON-LD and `config.js`, and shows "planned for later, join the free list". Flip it to `True` when the 7-inch is real.

### 6. Site policies disagreed with `ops/policies/` (fixed)

| Topic | Site said | ops/policies says | Now |
|---|---|---|---|
| Free shipping | "Free US shipping on every order", Alaska and Hawaii free | Contiguous US included; AK, HI, APO pay the difference | "Free shipping in the lower 48" everywhere (one constant, `SHIPPING_LINE`) |
| Return shipping | "deducted from the refund" (amount not given) | Flat $12 | Flat $12 |
| Refund timing | "within 7 business days"; deposits "within one billing cycle" | 5 business days for both | 5 business days |
| Returning a record we supplied | Only if it arrives damaged | Send it back with the sconce | Matches ops |
| Named-title return | Not mentioned | $25 restocking fee | Added |
| Warranty | One paragraph covering "LED ring, adapter and hub" | Two-year limited warranty on the whole light, record excluded; must be readable before purchase (16 CFR 702) | New `warranty.html`, linked from the buy box and footer |
| Second delay | "will not ship without your express consent" | Same, plus "if we do not hear from you, we refund you" | Matches ops |

The ops policies are marked "DRAFT. Have a lawyer review before publishing." So are these pages, in effect.

### 7. Layout and usability defects found in the screenshots (fixed)

- Mobile hero text sat flush against the left edge of the screen, with the orange dot half cut off (`.hero-content` zeroed the gutter). See `before/index-m-fold.png`.
- The product was a black box for up to 2.8 s on load ("Scroll or tap to turn it on"). It is now visible, dim, in the first frame and comes up after 0.7 s; lit by default with JavaScript off. See `after/flow-0-home-250ms.png`.
- On a phone the price was below the fold on the home page and the product page, and the reserve button was cut by the fold. Both are now above it (`after/index-m-fold.png`, `after/product-m-fold.png`).
- The mobile sticky buy bar on the product page only appeared after scrolling past the entire page section, which is never while choosing. It now shows whenever the main reserve button is off screen (`flow.py` line 14: shown True).
- The long reserve button split into two columns ("Reserve batch two," | "$25 refundable") and the "privacy policy" link floated away from its sentence (flex layout splitting text). Both wrapped in one span.
- Small grey text (`--ash` #5F6468 on #16130F) was about 3.1:1 contrast. It now uses the existing `--mute` token (about 6:1).
- Tap targets: Menu button 36 px high, footer links 28 px, consent checkbox 13 px. Now 44, 44 and 22 px.
- Austin's slogan line in the hero had been typed into `index.html` by hand and was not in the generator. A rebuild would have deleted it. It is now in `pages.py`.
- Sections faded in by script and stayed invisible with JavaScript off. A `noscript` rule shows them.
- Three different labels for the one action ("Reserve batch two, $25 refundable", "Reserve Spindle 12 with a $25 refundable deposit", "Reserve, $25"). Now one phrase: "Hold mine for $25, refundable".

### 8. Jargon (fixed outside the spec table)

Removed from customer copy: Class 2, CL2 (kept once, explained), NEC 725, NEC 400.12, 16 CFR Part 435, bayonet, J-slots, COB, dotless, CRI (kept in the spec table), keystone coupler, single-gang, old-work bracket, 1/4-20 insert, first-sale doctrine. The colour number "2700 K" was removed entirely in the second pass (see above); the light is described as "about the colour of an old filament bulb".

## Price decision (not made here)

`site/_gen/pages.py`, top of file: `KIT_PRICE = 89`, marked DECISION OWED. The comment quotes `build/cost-model.md`: parts $78.04 at 100, so the $89 Kit loses $19.90 an order before ads, $99 loses about $10, and the Kit needs about $125 to clear $15. The earlier "$89 clears about $16" figure is superseded. Change that one number, run `python3 _gen/build.py`, and the pages, meta descriptions, JSON-LD and `js/config.js` follow (build prints "synced js/config.js prices"). Verified at $89: picker shows $89, button reads "Hold my Spindle Kit for $25, refundable".

## Reference pages actually opened (2026-11-11)

Fetched through the web-fetch agent, which sees HTML without scripts. "Not visible" means not in the fetched HTML, not "absent".

| Page | URL | Above the fold | Price | Proof | Trust near the button | Ship promise | Safety wording |
|---|---|---|---|---|---|---|---|
| Gantri sconce | https://www.gantri.com/products/10326/premiere-wall-sconce-by-simon-schmitz?sku=10326-0-sedona | Photos, title | $398 on the listing | "2 Reviews", 4.0 | "returned within 30 days of delivery if unused", "Industry leading 3-year warranty" | "Made to order. 30 day returns. 3 year warranty." | "UL Listed for US and Canada" |
| Humanhome sconce | https://humanhome.co/products/gallery-sconce | 5 photos, title, price | "Regular price $540.00" | not visible | "Free 30 Day Returns", "1 Year Warranty" | "3 - 5 Business Days" beside Add to cart | "CERTIFICATIONS: UL and cUL Listed" |
| Tom Dixon lamp | https://www.tomdixon.net/lighting/portable/jack-large-portable-light-white-japo01whun | Carousel, title, prices, "Add To Bag" | "£425" struck, "£331.50" | not visible | "hassle-free returns within 14 days" | not visible | "Fully IP65 rated", no UL wording |
| Oura Ring 5 | https://ouraring.com/store/rings/oura-ring-5 | Gallery, title, "Shop Now" | $399 / $499 by finish | "99% Heart Rate Accuracy" style stats | not visible | not visible | n/a |
| Ember (home page only) | https://ember.com/ | Video hero, "Buy Mug 3", "How Ember works" | "$149.95 USD $99.99 USD" | "Over 4 Million Sold", press row | "30-day returns", "Free shipping", warranty line | not visible | n/a |
| HexClad pan (buy box only) | https://hexclad.com/products/12-hexclad-pan-with-lid | Title, "$199.00", "Add to Cart" | $199.00 | cut off | cut off | bar: "FREE SHIPPING" | n/a |
| Daylight | https://daylightcomputer.com | "Order now" | not visible | not visible | not visible | "In stock · Ships in 3-5 business days" | n/a |
| Aptera reserve | https://aptera.us/reserve/ | Price, "$100 Due Today", "CHECKOUT" | "Target Price $40,000" | n/a | none found | none stated | "Vehicle shown is in testing and validation; specifications are subject to change." |
| Toneoptic | https://www.toneoptic.com | Brand line | "From $325" | Press logos, named critics | not visible | "Taxes and shipping calculated at checkout" | none |
| Record Props | https://www.recordprops.com | "Get Versatile with your vinyl Record Display" | "$20.00 ea", sale from $22 | Press logos | "30 Day Return Policy" | "Free Shipping on all U.S. Domestic Orders" | none |
| Flipbin | https://www.flipbin.com | "Fill! Flip! Play! Display!" | "$99.00" struck, "$89.00" | "226 reviews" | not visible | not visible | none |

Guidance opened: Baymard, https://baymard.com/blog/current-state-ecommerce-product-page-ux (return policy link "should be prominently displayed on the product page"; show full order cost); NN/g, https://www.nngroup.com/articles/ecommerce-product-pages/ ("Price, including any additional product-specific charges", "Communicate product availability"); NN/g, https://www.nngroup.com/articles/trustworthy-design/ (upfront disclosure of all charges); FTC, https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule ("you must have a reasonable basis for stating or implying that you can ship within a certain time").

NOT CHECKED (fetch refused or empty): Ridge (403), Dyson (403), Tesla (403), Kickstarter (403), Etsy (403), Lumens (403), Rejuvenation product (403), Pooky, Tala and Schoolhouse product pages (429), Allbirds and Ember product pages (429), Rivian and Framework knowledge base (script-only), Baymard trust article (paywall), any UL page stating the rule on "UL Listed" claims for assemblies. Sticky buy bars could not be seen in any fetched page, so law 13 rests on general practice, not on these fetches.

## The laws, and the score

Scored 0 (fails), 1 (partly), 2 (meets).

| # | Law | Seen at | Before | After | Note |
|---|---|---|---|---|---|
| 1 | The product is visible in the first frame | Gantri, Humanhome, Oura, Ember | 1 | 2 | Was a dark box for up to 2.8 s |
| 2 | Name, price and the one button above the fold on a phone | HexClad, Humanhome, NN/g | 0 | 2 | |
| 3 | One action, one phrase, everywhere | Ember, Daylight | 1 | 2 | |
| 4 | When it ships, stated beside the button, and true | Humanhome, Daylight, FTC | 1 | 1 | Still "[SHIP DATE]". Needs Austin |
| 5 | Returns, warranty and shipping in a strip by the button, each linked | Ember, Humanhome, Gantri, Baymard | 1 | 2 | Warranty page did not exist |
| 6 | Full cost up front, no surprises | Baymard, NN/g | 1 | 2 | $12 return fee and AK/HI now stated |
| 7 | Real proof from real people | Ember, Flipbin, Toneoptic, Gantri | 0 | 0 | None exists. One invented line removed |
| 8 | Plain specs; certification stated exactly | Gantri, Humanhome | 0 | 2 | |
| 9 | Show it in a room, at scale | Gantri | 0 | 1 | Room renders were sitting unused in `img/`; now on the home page and gallery. Renders, not photos |
| 10 | How it works in three or four plain steps | Ember | 1 | 2 | Old diagram showed the old design |
| 11 | A pre-order says what is unfinished, what you pay today and how you get it back | Aptera, FTC | 0 | 2 | |
| 12 | Few choices | Oura, HexClad | 1 | 2 | Four versions down to three, one finish; "Named" still has no menu |
| 13 | A buy bar that follows you on a phone | general practice | 1 | 2 | |
| 14 | Fast, light, no errors | all | 2 | 2 | |
| 15 | Every picture and sentence true of the product | FTC | 0 | 1 | Words fixed; pictures are still pre-change renders |
| | **Total** | | **10 / 30** | **25 / 30** | |

## Images to re-render (nothing was faked or retouched)

| File(s) | Used on the site now | Problem |
|---|---|---|
| `img/exploded-900/1600.*` | No (removed from home, product, install) | Old design: light on the rim, felt washer only, no heat rings |
| `img/rear-900/1600.*` | No (removed from install and product gallery) | Callouts say "LED ring on the rim" and "barrel plug into the hub jack"; the hub jack is now a pigtail |
| `img/swap1/2/3-*`, `renders-final/png/swap*`, `swap_triptych.png` | No | Phantom fixed post |
| `img/flatlay-*`, `renders-final/png/flatlay*` | No | Loose "post" in the box that does not exist; no heat rings, no clear washer |
| `img/bedroom-*`, `img/bar-*`, `img/sq-brass-*`, `img/sq-black-*`, `img/hero-brass-*`, `img/hero-black-*`, `img/cap-brass.*`, `img/cap-black.*` | No (second pass) | Bedroom: a 4 W strip lighting a whole room. The rest: cap finishes with no real part |
| `img/sq-chrome-*`, `img/hero-chrome-*`, `img/living-*`, `img/og.jpg` | Yes | Lit before the layout change with a ring near the rim. The strip is now 14 mm further in, so the real halo may be softer or narrower. Captioned as renderings. Re-render from the final CAD, then replace with photographs of a built unit |
| `img/set-*`, `img/studio-*` | No | Show 7-inch singles, which are not on the heat-safe layout |
| `img/cutaway-*` | Yes (install) | Callout "Cable exits hub back centre"; the lead hole is 15 mm off centre. Minor |
| `img/cap-*`, `img/macro-*` | cap: yes | No clear washer visible under the cap. Minor |
| New: `img/layout-900/1600.*` | Yes | Cropped from `renders-exploded/spindle-heat-safe-layout.png` (the current design). A light technical drawing inside a dark site: accurate, not pretty. A dark-styled render of the same view would fit the look |

## What I changed

All inside `site/`. Generated HTML was never hand-edited.

- `_gen/pages.py`: rewritten copy per the findings; price and switch constants at the top; FAQ now 13 questions with "Is this a finished product I can buy today?" first; new warranty and 404 pages; room images and the current-design drawing added; old exploded and rear images removed.
- `_gen/build.py`: writes prices into `js/config.js`; `--launch-check`; footer and announcement bar wording; `noindex` on thank-you and 404 pages; `noscript` fallback.
- `js/main.js`: hero timing; honest thank-you logic; waitlist validation; sticky bar trigger; Set switch.
- `js/config.js`: `SET_OPEN`, comment that prices are generated.
- `css/style.css`: gutter, contrast, tap targets, the new blocks. Same tokens, same fonts, same look. No new colours except the diagram's own paper background and a red test-mode banner.
- New files: `warranty.html`, `404.html`, `img/layout-*.{jpg,webp}`, `screenshots/audit-2026-11-11/`.
- `README.md` in `site/`: section added describing the above.

Not changed: brand, palette, type, the hero tagline, the slogan, the "First batch of 20 sold out" line (Austin's decision, recorded as true on 2026-11-09), the $25 deposit, the 100 cap. Changed in the second pass and owed a yes from Austin: chrome only, and the "lit at 2700 K" heading.

## Needs Austin

1. **Kit price**: 89, 99, or about 125 (`KIT_PRICE`). Per `build/cost-model.md` both 89 and 99 lose money on every order before ads.
2. **Ship week**, with a basis. No prototype exists, the chrome cap is the long pole, and the first 20 ship first. Until a date exists the honest options are a wide window or waitlist only.
3. **The 20**: who they are and whether they paid. The site says "sold out" on his word; if they are verbal, "20 reserved" is the true phrase. It now says they have not shipped.
4. **Stripe link, waitlist endpoint, contact email, pixel id, domain** (the launch check lists them).
5. **Chrome only** (`FINISHES_OPEN`) and **no Los Angeles or North Carolina** (`NO_SHIP_PLACES`): both switched on the product audit's word. **Set**: stay closed until the 7-inch is engineered? And **Named**: keep it on sale before the album menu and the IP lawyer hour exist?
6. **In-wall as the default**: he said most people will want it. On the page the two-screw plug-in route now comes first because it is the one a renter and a nervous buyer can say yes to; in-wall is option B. Swap back if he prefers.
7. **Lawyer** on the four policy pages and the warranty (ops drafts say so).
8. **Seller identity**: the terms and warranty name no legal entity or address.

## Could not verify

- Real mobile Safari, real Android, any real network speed. Headless Chromium only.
- Real Stripe checkout, the redirect back with `session_id`, real waitlist delivery, the Meta pixel in Events Manager.
- Lighthouse or Core Web Vitals (not run).
- Whether the 20 pre-sales are real, paid or verbal.
- Whether the renders match what a built unit looks like. Nothing is built.
- `img/og.jpg` was checked for size (1200x630, 112 KB) but I did not open it to judge the picture.
- Mount details I simplified but did not re-derive (4-inch plate, three pins, one set screw, "about 15 minutes", "about 45 minutes"): taken from `mounting-report.md` and labelled as estimates.
- `cad/build_all.py` was not run. I grepped the built pages for the gate strings instead: "up to 6 W" on product.html (1), "sits on the back of the backplate, facing the wall" on faq.html (2), none of the forbidden strings on any page.

## Top five reasons this site would still fail to sell

1. **No proof it is real.** Every picture is a rendering and the page now says so. A stranger from an ad is asked to trust a product nobody has photographed.
2. **No date.** "Planned to ship the week of [SHIP DATE]" is a blank. A deposit page without a date converts badly and a date without a basis is an FTC problem.
3. **No voices.** Zero reviews, zero photos from the 20, zero press. The reference pages all lead with one of those.
4. **The honest heat answer is "calculated, not measured".** For a record collector that is the whole objection. One thermocouple photo from a real unit is worth more than every sentence on the page.
5. **The money.** At $89 the Kit loses $19.90 on every order before ads (`build/cost-model.md`). The $129 Sconce clears $12.77, which one average ad purchase wipes out. A page that converts loses money faster.
