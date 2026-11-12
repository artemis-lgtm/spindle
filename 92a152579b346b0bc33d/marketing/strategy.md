# Spindle: launch marketing strategy (v2, rewritten after the 2026-11-11 audit)

Rewritten 2026-11-11 by the marketing auditor. The v1 plan (2026-11-09) is superseded; what changed and why is in CHANGELOG.md and in ../audits/AUDIT-marketing.md. Nothing here has been posted, sent, bought or registered.

Three facts drive every change below.

1. Nothing has been built or heat-tested. The product photos are renders, some of them show a "post" that does not exist, and the 7 in single is not on the heat-safe layout (../NOTES.md, 2026-11-11 entries; ../renders-final/README.md).
2. The margins moved, twice. The v1 plan was written on a parts cost of about $27. The product audit re-priced the bill of materials at prices that can be bought today: $78.04 at 100 units and $211.33 at 20, with the chrome cap carried as a $15.00 placeholder that no supplier has quoted (../build/cost-model.md and cost-model.csv, rewritten the evening of 2026-11-11; ../audits/AUDIT-product.md). An earlier draft of this file used $47.46; that figure is superseded.
3. A $25 deposit is a partial payment. Under the FTC mail order rule the clock starts when a partial payment is received, and with no ship time stated the seller must have a reasonable basis to ship within 30 days (16 CFR 435.1(c) and 435.2(a)(1), read 2026-11-11 at https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-435). So the deposit button cannot be live until there is a ship week with records behind it.

The plan is therefore gated on what physically exists, not on calendar dates.

## 1. Positioning

One sentence: Spindle is a wall light that turns the record you already own into a lit object, and lets you change it whenever you like.

In the customer's words: a warm ring of light sits behind a real 12 in LP and throws a halo on the wall. A chrome dome screws the record on through the spindle hole. Nothing is glued. Plug-in, low voltage.

Honest competitive picture (v1 said nobody lights the record; that is wrong):

| Product | What it is | Price / proof shown on its own page | Opened 2026-11-11 |
|---|---|---|---|
| Vylumi Nova | Backlit, sound-reactive display for one record, desk stand or wall hanger, USB power. Sells on record safety: "100% SAFE FOR YOUR RECORDS. Runs cool to the touch with no heat and no warping" and "low-heat / low-UV LEDs, two air gaps to kill heat transfer". Says "FUNDED IN 9 MIN" on Kickstarter, August 2026. | "4.82, 125 reviews" | https://vylumi.com/ |
| PETRU Smart Now Playing Stand | Stand that holds the sleeve with an audio-reactive light. Father and son business. Lists "Find a retailer". | $239.90, "812 reviews" | https://petrudesign.com/ and https://petrudesign.com/pages/about-us |
| Gantri wall lights | Designer plug-in wall lights. Spec line on the home page: "Warm, inviting 2700K light. True-to-life color with 90+ CRI. 600+ lumens, fully dimmable." | $248 to $298 | https://www.gantri.com/ |
| Poplight | Renter wall sconce, stick-on. | $89 to $99, "Hundreds of 5 star reviews" in the page title | https://thepoplight.com/ |
| Record Props | Wall and tabletop record display, no light. | holiday banner, 60-day returns | https://recordprops.com/ |
| Art Vinyl Flip Frame | Swap-without-unhanging record frame. What Hi-Fi reports "some 200,000 customers" for the 12 in frame. | about 30 to 40 GBP | https://www.whathifi.com/news/artvinyl-launches-vinyl-storage-kickstarter |

What that means for us:
- Our real difference is narrow and still true: it is a room light (a halo on the wall, dimmable), the record is held by a visible piece of hardware, and it reads as a fixture, not a gadget. Say that. Do not say "the only one that lights the record".
- Collectors already pay about $240 for a lit display with 812 reviews behind it, and design buyers pay $248 to $298 for a 2700K, 90+ CRI wall light. Those are the price anchors to use. They are close comparables with real prices on pages we opened. The $755 designer sconce is a weaker anchor and naming that brand in an ad adds risk for nothing.
- Every comparable shows a review count on the first screen. We have zero reviews and zero photos of a real unit. Closing that gap is the first marketing job, ahead of any ad.
- Record safety is a headline claim in this category. We may not use it until the thermocouple test is done (section 3), and when it is done we publish the measured number, which beats an adjective.

One-liner ladder:
- 3 words: Your record, lit.
- 7 words: The wall light built around your records.
- Full: A warm halo behind a real record. A chrome dome screws it on. Change the record, change the room.

## 2. What we may and may not say (claims register)

A claim goes in an ad, a post, an email or the page only when the "proof needed" column is satisfied and the proof is saved in ../audits/ or ../build/.

| Claim | Status today | Proof needed before use |
|---|---|---|
| "First batch of 20 sold out" | Hold. Austin reported 20 pre-sold; who bought and what they paid is not on file (../ops/legal.md section 4 says the same). | A ledger: name, date, amount, what was promised. Then the honest wording is "The first 20 are spoken for", because nothing was built. "Sold out" comes back once the 20 have shipped. |
| "We built 20", "people who have the first batch", "how the first twenty hung theirs", any photo "of a first-batch unit" | False today. Removed everywhere. | 20 delivered units. |
| "Nothing glued to your record", "felt pads", "chrome dome screws it on" | True to the CAD. | A photo of the real stack. |
| "Cool", "nothing warm", "no heat near the vinyl", "safer on this wall than in the crate" | Not allowed. The thermal model says 33.1 C in a 30 C room and 45.2 C stacked worst case, and the product audit found that standard record compound starts to lose stiffness at 48 to 50 C, lower than the 55 to 60 C the project had assumed, so the worst case lands on the limit (../audits/AUDIT-product.md). Nothing is measured. | Thermocouple on the back edge of the record, 2-hour soak, per ../build/QC-test-plan.md. Then state the number: "after two hours the record measured N F in a 75 F room". Never "safer than the crate". |
| "Swap in ten seconds", "one hand" | Unmeasured. | Time it on camera on the real unit and use the real number. Drop "one hand" unless it is true on video. |
| "15-minute install", "45 minutes in-wall" | Unmeasured. | Time both on camera. |
| "2700K, CRI 90+, dotless, dimmable" | Not allowed yet. The product audit found the only priced 4 W strip is 2900 to 3200K, not 2700K, and the dimmer is untested for flicker on camera. Say "warm, dimmable" until then. | The datasheet of the strip actually bought, and a flicker check on video. |
| "UL-listed 12V adapter" | Only on the page and the spec sheet, never in an ad headline or on-screen text, and always with "the fixture itself is not UL listed". | The UL file number of the adapter actually bought (../ops/safety.md lists this as open). |
| "No electrician", "legal to run in the wall" | "Plug-in, no electrician" is fine for the surface cord. In-wall: "allowed inside walls in most US homes under the National Electrical Code; check local rules" (../ops/safety.md section 4). | None beyond the softer wording. |
| "Made in Fort Lauderdale", "made to order in Fort Lauderdale" | Not allowed as written. The FTC treats references to a US factory location as a possible US-origin claim, and an unqualified claim needs "all or virtually all" US content (https://www.ftc.gov/business-guidance/resources/complying-made-usa-standard, fetched 2026-11-11; 16 CFR 323.1 to 323.3). The LED strip, adapter and dimmer are catalogue electronics that are very likely imported (the BOM does not record country of origin). | Use "Designed and assembled in Fort Lauderdale from US and imported parts". The FTC guide gives "Made in USA of U.S. and imported parts" as an example of a qualified claim. Ask the IP lawyer in the same hour. |
| Any band, artist, album or label name; any real label in a render | Never in ads, posts, emails or renders. The band-label renders in ../renders-zep/ (a computer-made label carrying a band name and track titles) are not marketing assets: 17 USC 113(c) covers "pictures or photographs" of the real article (https://www.law.cornell.edu/uscode/text/17/113), and a render is our own reproduction of someone's label. | Named-title tier stays off until the IP lawyer hour. |
| "Ships by", any countdown, any stock number | Never until a ship week exists with a reasonable basis and the count is read from Stripe. | Sample run finished, supplier lead times in writing. |
| A competitor's name in an ad | Never. | n/a |

## 3. The gates (sequence replaces the dated calendar)

v1 had the page live with a deposit link on 11/10, ads on 11/11 and ten gift Kits shipping on 11/12. None of that could happen: there is no unit. The order below is the fix. Dates are estimates from ../sourcing/ lead times (sample run about 3 weeks from order, chrome caps the long pole) and nothing has been ordered.

### Gate 0: paper (now). Cost: under $50.

Done when all of these are true:
- The ledger of the 20 exists (who, when, how much, what they were told about delivery). If money was taken, each of those 20 is already an order under the mail order rule and needs a ship date or a refund offer; that is the first email (email-sms-flows.md, flow 8).
- spindlelighting.com and @spindlelighting (TikTok, Instagram) are registered under a Spindle identity. Nothing runs through Ghost Audio, Elbo Room or Higney International accounts: new Meta business and ad account, new pixel, its own email tool login, its own sending mailbox on the Spindle domain. v1 proposed the HI Mailchimp, the Ghost Postiz and an HI email address; all three are removed.
- The public page has the free waitlist only. The deposit button is off. Every render on it carries the caption "Render. First units are being built now." and the swap and flat-lay renders with the phantom post are not used.
- A real quote for 100 chrome caps is in hand, and Austin has re-set the prices from it (section 4), and decided deposit versus full pre-order (section 5).
- The sample-run parts are ordered. Marketing cannot move past this gate on its own.

Marketing allowed at Gate 0: the build-in-public series from the real bench (tiktok-laws-and-video-concepts.md, concepts 1 to 4), the waitlist, and account warm-up. No paid, no outreach, no press, no "sold out".

### Gate 1: one real unit that passes the heat test. Estimate: late November at the earliest.

Done when: one unit hangs on a real wall; the 2-hour soak is logged with the record's back-edge temperature; swap and install are timed on camera; the halo has been compared with the renders (../renders-final/README.md asks for this).

Then, and only then:
- Shoot the real asset library in one evening: switch-on in the dark, the swap with a visible timer, the dome macro, the install in real time, the wall at dusk, the heat reading. This replaces every render in ads and organic.
- Daily organic begins (organic-plan.md).
- One comment in the r/vinyl projects megathread (pr-and-communities.md).
- Austin's 15-second founder clip.

### Gate 2: a ship week with a reasonable basis. Estimate: mid December or later.

Done when: the sample run of 8 is assembled and has survived the QC plan; lead times for the 100-unit parts order are in writing; the first 20 are scheduled; product liability insurance is bound (../ops/insurance.md); the ship week is chosen with a two-week buffer; the 7 in question is answered (either the 7 in is on the heat-safe layout or the Set stays off sale).

Then:
- The deposit or pre-order button goes live with the ship week printed next to it and in the confirmation email.
- Paid ads stay off unless section 7's margin condition is met.
- The first three creators get real units (ugc-creators.md).

### Gate 3: the first 20 are delivered.

Then: "First batch of 20 sold out" is fully true; review requests go to all 20; customer photos replace our own; the second creator wave and any scaling of paid begin.

### Holiday 2026, plainly

No Spindle can be promised for Christmas 2026. Parts are not ordered, the sample run takes about three weeks, and Christmas is 44 days out. Black Friday and Cyber Monday (11/27 to 11/30) are not a sales event for us this year; they are four days of bench content and waitlist building. The printable gift certificate is fine only after Gate 2, with the real ship week printed on it. v1's Black Friday offer (free in-wall kit on Set deposits) is cancelled: the Set is not sellable and deposits are not open.

## 4. Unit economics (updated the evening of 2026-11-11 from the product audit's cost model)

Contribution before ads = price minus parts, record, labour, shipping and Stripe. Every figure is from ../build/cost-model.csv as rewritten by the product audit. "Break-even ROAS" is price divided by contribution. "Deposit ceiling" is the most a deposit can cost if half of deposits become paid orders (the 50% is a planning assumption; no source exists for a $25 deposit on a product like this).

| SKU | Price | Contribution at 100 | Break-even ROAS | Deposit ceiling at 50% paid | Contribution at 20 |
|---|---|---|---|---|---|
| Kit | $89 | minus $19.90 | none, loses money | none | minus $156.52 |
| Sconce, vintage record | $129 | $12.77 | 10.1x | $6.39 | minus $123.85 |
| Sconce, named title | $179 | $33.32 | 5.4x | $16.66 | minus $103.30 |
| Set, kit (not buildable today) | $249 | $45.01 | 5.5x | $22.51 | minus $110.10 |
| Set, with records (not buildable today) | $329 | $108.36 | 3.0x | $54.18 | minus $46.75 |
| In-wall kit add-on | $29 | $19.31 | attach only | n/a | $16.16 |

These are soft in the worst direction. The chrome cap is in the model at $15.00 at 100 units and the only live prices are $121 to $156 each for 1 to 50 pieces; one prototype costs about $279 in parts (cost-model.md). If the cap quote for 100 comes back above $15, every row drops by the difference.

The one benchmark panel I opened that publishes its spread (19 managed DTC accounts, $2.88M spend, October 2025 to September 2026, https://topgrowthmarketing.com/dtc-ecommerce-benchmarks/meta-ads-benchmarks/): median cost per purchase $33.80, middle half $24.97 to $51.09; median ROAS 2.55, middle half 1.82 to 3.87. Those are experienced accounts; a new one should expect worse. A second source puts art and home decor at 0.61% conversion and $26.16 CAC (https://lebesgue.io/facebook-ads/facebook-benchmarks-by-industry-ctr-cpm-cr-and-cac; method not shown).

What the numbers say:
- No 12 in SKU can carry paid advertising at today's prices and costs. The best case, the $179 named-title Sconce, needs a 5.4x return, above the 75th percentile of an experienced panel, and it is not on sale until the IP lawyer hour. The $129 Sconce clears $12.77; even the panel's best quartile cost per purchase ($24.97) loses money on it.
- The Kit at $89 loses $19.90 on every order before any marketing. The cost model says it needs to be about $125 to clear $15.
- The first 20, built at 20-unit prices, lose over $100 each on every SKU. If those 20 were promised at $89 or $129, that is a loss of roughly $2,500 to $3,100 on the batch before marketing. Not a marketing decision, but Austin should see the number.
- For marketing to have any budget per order, the contribution has to be about $45 or more. At today's costs that means roughly $165 for the Sconce and $155 for the Kit (price times 0.971, minus $112.49 or $106.32 of cost and fees), or a cap quote far under the placeholder. A $149 Sconce clears about $32.20 and a $169 Sconce about $52.
- The price anchors in section 1 say $149 to $179 is not out of range for this buyer: PETRU sells a lit record stand at $239.90 with 812 reviews, and Gantri's wall lights are $248 to $298. That is a pricing argument Austin can use; whether buyers accept it is untested.
- v1's pass mark was "cost per deposit at or under $45". At today's contribution the ceiling for the $129 Sconce is $6.39. That is not a reachable number.
- Wholesale to record stores is far underwater: half of $129 is $64.50 and the landed cost is $112.19.
- The $29 in-wall kit adds $19.31, more than a $129 Sconce earns. Attach matters more than ever.

Decisions this forces (Austin): the price of every SKU, after a real cap quote for 100 pieces. Until then no price appears in any ad or email, and the page should not take money at $89 or $129.

## 5. Offer ladder (v2)

| Rung | Offer | Price | Live from | Notes |
|---|---|---|---|---|
| 0 | Free waitlist, email only | $0 | Gate 0 | No SMS at launch (email-sms-flows.md explains why). |
| 1 | Reserve a batch-two unit | $25 refundable deposit, or full price | Gate 2 | Ship week printed beside the button. Recommendation: offer full pre-order as the main button and the deposit as the second, because a full pre-order has no deposit-to-paid leak and the allowable CAC is the whole contribution. Austin's call. |
| 2 | Spindle Sconce with a vintage record, our pick from your decade | $129 today; under review (section 4) | Gate 2 | The hero SKU. |
| 3 | Spindle Kit, your own record | $89 today loses $19.90 an order; about $125 clears $15 | Gate 2, and only after it is re-priced | Never advertised below a price that clears a margin. |
| 4 | Named-title Sconce | $179 | After the IP lawyer hour | Off until then. |
| 5 | The Set | $249 / $329 | After the 7 in is on the heat-safe layout and its cap is quoted | Off until then. No Set creative runs before that. |
| Add-on | In-wall wiring kit | $29 | Gate 2 | Offered on the page and in the confirmation email. |

Finishes: chrome only. The product audit found no real part behind the brass and black caps, and the lit cap's centre contact has never been built (../audits/AUDIT-product.md). No brass, black or lit-cap copy or image is used until those parts exist.

Rules: no discounts; no urgency that is not a real date or a Stripe-read number; the gift certificate carries the real ship week or does not exist.

## 6. Channels, in the order they can actually run

1. Organic TikTok and Reels, starting as a build-in-public series (Gate 0) and becoming product video at Gate 1. This is the lead channel because it is free, it is where the comparables grew (Poplight: "we've gone multi viral on TikTok", https://thepoplight.com/blogs/news/how-it-all-started; Custom Neon: "During the first 12 months, we didn't need to spend a dime on advertising, instead relying on user-generated content (UGC) and word-of-mouth", https://buffer.com/resources/side-hustle-to-business/), and it produces the footage every other channel needs. The laws and 14 shot-by-shot concepts are in tiktok-laws-and-video-concepts.md.
2. Email waitlist. Three plain emails, then quiet until there is a date (email-sms-flows.md).
3. The first 20 buyers. They are the only source of reviews and real-wall photos for months. Custom Neon's version: "Every time we ship a sign, we include a note asking a customer to share the final result ... and tag us" (same Buffer article). A card in every box does the same.
4. Communities: one megathread comment at Gate 1, real-photo posts only after Gate 3 (pr-and-communities.md).
5. Creator seeding, small: three real units at Gate 2, more only if those produce video (ugc-creators.md).
6. Paid Meta, last and small, as an amplifier of organic posts that already worked and as retargeting of people who visited the page. Not as the engine. Section 4 shows why.
7. Press and gift guides: not this year. Nothing to photograph or send, and most 2026 guides closed in the autumn. Pitch the rolling lists once there are reviews and real photos; pitch the 2027 guides in August 2027.

Not now: TikTok Ads, Google Shopping, Pinterest Ads, Amazon, Etsy, Kickstarter. On Kickstarter see pr-and-communities.md section 3; the decision is Austin's and the audit asks him to look at it again, because every close comparable (Poplight, Vylumi, Art Vinyl) used it for exactly this stage.

## 7. Paid ads: off until the margin exists

At today's costs there is no paid test worth running. The $129 Sconce clears $12.77 and the cheapest quartile of experienced advertisers pays $24.97 per purchase (section 4). Spending to learn that an ad loses money on a product that loses money is not a test.

Paid switches on only when all of these are true: Gate 2 is passed; a real cap quote is in the cost model; the hero SKU clears at least $45 before ads at the price on the page.

If and when that happens, the test is:
- $20 a day for 21 days, $420 total, one campaign, one ad set, Advantage+ audience, US, 25 to 54. Three or four ads, all real footage. Austin sets the account spending limit to $450.
- Read the funnel stage by stage: link click-through (under 1% after 3,000 impressions means the creative failed; the opened panels put the 10th percentile at 1.16%), page view to checkout start, checkout start to order.
- Verdict after $420 or 12 orders, whichever comes first: cost per order at or under half the contribution, continue; up to the full contribution, keep only a $3 a day retargeting ad set aimed at people who visited the page; above it, stop.
- $420 still leaves wide error bars. A pass is permission to spend the next $400, not proof.

v1's test was $15 a day with a verdict after $150. At a true cost per deposit of $45 that buys about 3 deposits; its "stop at $80" rule would fire 15% of the time on a healthy campaign and miss a $100 campaign 44% of the time (Poisson arithmetic). It could not tell good from bad, and its pass mark was eight times today's ceiling.

Creator budget: ugc-creators.md. A gifted unit costs about $242 at 20-unit prices and $106 at 100-unit prices, so seeding is three units, not twenty.

Total marketing cash before the first 100 units ship, with paid off: about $50 for names, $320 to $730 of gifted units, $0 to $20 a month for email. Under $800. The $420 test is extra and conditional.

## 8. KPIs and kill lines

Gate 0 to 1 (no product): posts made (target 5 a week), waitlist signups (any), median views per post. Expectation set from our own history, not hope: the Ghost Audio TikTok account, run by the same operator, sat at 93 to 194 views per daily post and 590 followers after months (../../../memory/research/tiktok-pattern-strategy-2026-09-17.md and tiktok-audience/analytics-2026-10-12.json). A different niche, but the same starting point: a new account with no audience. v1's targets (1,000 followers per platform, 10 posts over 10k, 2 over 100k in 30 days) had no basis and are withdrawn.

30 days after Gate 1: median views per post over 500; one post over 10,000; 100 waitlist signups; saves per 1,000 views tracked on every post (in our harvest, outliers saved at 26 per 1,000 against 13 for the rest).

After Gate 2: deposits or pre-orders counted in Stripe, cost per deposit from section 7, in-wall kit attach rate (target 25%, estimate), refund rate on deposits.

Kill lines:
- Heat test fails (record back edge over 35 C in the 2-hour soak, the QC plan's own limit): all marketing stops until engineering fixes it. Nothing that has been posted may have promised otherwise.
- Paid: stays off until section 7's conditions are met.
- Any ad disapproved for a misleading claim: pause everything, fix page and copy the same day.
- Deposit refunds over 20% before ship: stop acquisition and find out why.
- Any rights holder asks for a title to come down: down within two business days, no argument (../ops/legal.md).
- Ship week slips: flow 7 goes out before the promised date, in the form the rule requires.

## 9. What Austin owes marketing

1. The ledger of the 20: who, when, how much, what they were told. Until it exists the "first 20" line is off.
2. Order the sample-run parts. Every later gate waits on this.
3. A real quote for 100 chrome caps, then new prices for every SKU (section 4). At today's costs the Kit loses money at $89 and the $129 Sconce clears $12.77.
4. Deposit, full pre-order, or both (recommendation: both, pre-order first).
5. Register the domain and handles under a Spindle identity, and a Spindle ad account (no spend until section 7's condition is met).
6. A valid postal address for the email footer (required by 15 USC 7704(a)(5)(A)(iii)).
7. One hour with an IP lawyer: the "assembled in Fort Lauderdale" wording, the named-title tier, and whether a creator's video showing real labels can be run as our ad.
8. A second look at Kickstarter for batch two (pr-and-communities.md section 3).
9. Fifteen seconds on camera once unit one is on the wall.
