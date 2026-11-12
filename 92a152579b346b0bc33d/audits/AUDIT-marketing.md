# Audit: the Spindle marketing plan

Auditor: pessimist marketing auditor (Fable 5.2), 2026-11-11. Scope: every file in marketing/. Edits were made only inside marketing/ (see marketing/CHANGELOG.md). Nothing was sent, posted, bought, registered or committed. Every source cited was opened in this session on 2026-11-11 unless it says otherwise; what could not be opened is listed in section 5.

## 0. Update, evening of 2026-11-11: the economics got worse after this audit's first pass

The product audit (AUDIT-product.md) re-priced the parts the same evening. I read build/cost-model.md and cost-model.csv to confirm: 12 in parts are $78.04 at 100 and $211.33 at 20, and the chrome cap is a $15.00 placeholder with live prices of $121 to $156 each at 1 to 50 pieces. Contribution before ads at 100: $89 Kit minus $19.90, $129 Sconce $12.77, $179 Sconce $33.32, Set kit $45.01. At 20 units every 12 in SKU loses more than $100.

Where findings below quote $47.46 parts, $15.68 or $48.35 contribution, a $24 deposit ceiling, a $93 gift unit or a $76.61 landed cost, those were the figures on file at the time and are superseded. The findings stand and are more severe:

- S1-5 and S1-6: no 12 in SKU can carry paid advertising. The deposit ceiling for the $129 Sconce is $6.39. Paid is now switched off in the plan until a real cap quote and new prices give the hero SKU at least $45 of contribution; that needs roughly $165 on the Sconce at today's costs.
- New: the first 20, if promised at $89 or $129, lose roughly $2,500 to $3,100 as a batch at 20-unit prices.
- S2-2: a gifted unit costs $242.64 at 20-unit prices and $106.02 at 100. Seeding is cut to three units.
- S1-4: the product audit puts the softening of record compound at 48 to 50 C, not 55 to 60 C, so the modelled worst case (45.2 C, or higher with the plume it adds) sits on the limit. Heat claims stay barred and the worst case is now part of the filmed test.
- New: brass, black and lit caps have no real part; "2700K" is not supported by the only priced low-power strip (2900 to 3200K). All such copy is removed. Chrome only.
- Images: the product audit's ruling is adopted (only macro_* true as it stands; hero_chrome_*, swap3_*, living_* with a "rendering" line; the rest unused).
- Marketing cash with paid off: under $800 before the first 100 ship.

Top decision for Austin is now price: get a real quote for 100 caps, then re-set every price before anything is sold or advertised.

## 1. Verdict

The v1 marketing plan could not be executed and would have lost money and created legal exposure if it had been. It was a calendar that started on 11/10 with a live deposit link, ads the next day and ten gift units shipping the day after, for a product that does not exist: nothing is built, nothing is heat-tested, the product photos are renders and some show a part that is not in the design. Its money math ran on a parts cost of about $27 when today's figure is $47.46 at 100 units and $68.00 at 20, and its main pass mark (cost per deposit at or under $45) loses money on every sellable SKU because a deposit is not a sale. Several emails and ads described owners, photos and a built batch that do not exist. The research underneath it (creator list, subreddit rules, reference ads) is useful and was kept. The plan has been rewritten around four gates tied to what physically exists, with the economics redone, the claims cut back to what can be proven, and the TikTok research applied honestly as 10 laws and 14 shot-by-shot concepts. With those fixes the plan is executable by one person on under $800 of marketing cash with paid ads switched off (see section 0), and it cannot start selling until the product is built, tested and re-priced.

## 2. Findings, ranked by severity

Severity: S1 = would cause legal exposure, a false public claim, or a guaranteed loss. S2 = would waste the budget or mislead the decision. S3 = weak or unsupported, worth fixing.

### S1-1. The whole plan was sequenced ahead of a product that does not exist
Evidence: NOTES.md 2026-11-11: "nothing is measured, first prototype needs the thermocouple test"; renders-final/README.md flags the phantom post as "STILL OPEN". v1 strategy week 1: page live with deposit link 11/10, ads 11/11, "first UGC gifting wave: 10 creators" 11/12, gift-guide pitches by 11/14 offering "a unit for review".
Fix applied: strategy.md section 3 replaces the calendar with Gates 0 to 3 (paper; one tested unit; a ship week with a reasonable basis; 20 delivered) and assigns every action in every file to a gate. organic-plan.md starts as a build diary. Gift guides and press move to after Gate 3.
Needs Austin: order the sample-run parts. Marketing cannot pass Gate 0 without a unit.

### S1-2. Taking a $25 deposit with no ship date breaks the mail order rule
Evidence: 16 CFR 435.1(c): an order is received when "the buyer tenders full or partial payment"; 435.2(a)(1)(ii): without a stated time the seller needs a reasonable basis to ship "within thirty (30) days"; 435.2(a)(4): no "records or other documentary proof" creates a presumption against the seller (https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-435). The FTC business guide confirms partial payment starts the clock (https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule, fetched through the fetch agent). v1 put the deposit link live while "dates for batch two ship are placeholders".
Fix applied: deposits and flows 2, 3, 4, 6, 7 are off until Gate 2. Flow 7 (delay notice) rewritten into the two versions the rule requires: v1's single version left out that silence counts as consent for a delay of 30 days or less and that the order cancels automatically for a longer or open-ended delay (435.2(b)(1)(ii) and (iii)).
Needs Austin: if the first 20 already paid, they are orders today. Flow 8 gives them a ship estimate or a refund offer.

### S1-3. False statements about a built batch, owners and photos
Evidence (v1 text): email 1.2 "People who have the first batch are already swapping with the season"; email 1.3 "Three ways the first twenty went up. Most ran the low-voltage cable inside the wall"; email 2.3 "A photo of a first-batch unit on a dark green wall is attached"; ad copy 26 "We built 20. They sold."; ad concept 14 "quick cuts: three finished units"; organic post 20 "How the first 20 hung theirs". Nothing has been built, and who the 20 buyers are and what they paid is not on file (ops/legal.md section 4: "We do not have it yet").
Fix applied: all removed. "First batch of 20 sold out" is held until 20 units are delivered (Gate 3); from Gate 2, and only with the ledger, the wording is "the first 20 are spoken for". A true version of the story is video concept 13 ("Twenty people paid for this before one existed. This is number one.").
Needs Austin: the ledger.

### S1-4. Heat and record-safety claims with no measurement, some describing the old layout
Evidence (v1 text): "cool 12V light on the rim", "Nothing warm", "no heat near the vinyl", "the record never touches anything warm", "Your record is safer on this wall than in the crate". The rim layout was abandoned on 2026-11-11 for heat reasons; the model for the new layout gives 33.1 C in a 30 C room and 45.2 C stacked worst case (NOTES.md), and vinyl softens around 55 to 60 C by the project's own notes. Nothing is measured. A direct competitor makes safety its headline ("Runs cool to the touch with no heat and no warping", https://vylumi.com/), so buyers will ask.
Fix applied: claims register (strategy.md section 2) bars every heat adjective; the only allowed form is the measured reading. The heat test itself becomes content (video concepts 2 and 7) and email 1.2. Kill line added: if the test fails, all marketing stops.

### S1-5. The pass mark treated a deposit as a sale; at today's costs it loses money on every sellable SKU
Evidence: build/cost-model.csv (regenerated 2026-11-11): contribution before ads at 100 units is $15.68 (Kit $89), $48.35 (Sconce $129), $68.90 (named $179), $98.83 (Set kit), $162.18 (Set with records). v1 pass mark: cost per deposit at or under $45; v1's own sources put deposit-to-purchase at 20 to 40%. At $45 per deposit and 50% paying, cost per customer is $90. The one source I opened on deposit conversion says "typically 30 to 50% of the deposit list" for $1 crowdfunding reservations (https://www.boostyourcampaign.com/blog/kickstarter-reservation-funnel); nothing measured exists for a $25 deposit on a $129 product.
Fix applied: strategy.md section 4 gives break-even CAC, break-even ROAS and deposit ceilings per SKU. The ceiling for the $129 Sconce at 50% is $24.18. Recommendation added to offer a full pre-order as the main button so there is no deposit leak.
Needs Austin: deposit, full pre-order, or both.

### S1-6. The Kit cannot carry paid advertising, and the first 20 lose money on it
Evidence: Kit contribution is $15.68 at 100 units (break-even ROAS 5.7x) and minus $6.94 at 20 units. The one benchmark panel that publishes its spread (19 managed accounts, $2.88M spend) has median ROAS 2.55, 75th percentile 3.87, median cost per purchase $33.80 (https://topgrowthmarketing.com/dtc-ecommerce-benchmarks/meta-ads-benchmarks/). v1 made the Kit the lead product for its first audience and for gift ads.
Fix applied: paid points only at the $129 Sconce; the Kit is organic and email only unless the price moves. Table shows the Kit at $99 ($25.39, 3.9x) and $109 ($35.10, 3.1x).
Needs Austin: the Kit price.

### S1-7. The only SKU with good paid economics, the Set, cannot be sold
Evidence: NOTES.md: "the 7 in sconce is NOT on the layout (its back face outside the hub is 9.35 mm wide; an 8 mm strip plus screws does not fit) and keeps the rim strip"; BOM.md line 74: "not heat-modelled". v1 had a Set ad (concept 10), Set copy, a Set audience and a Black Friday Set offer.
Fix applied: every Set line parked or cut; Black Friday offer cancelled.

### S1-8. "Made in Fort Lauderdale" is an unqualified US-origin claim the product cannot support
Evidence: used about ten times in v1 ("Made in Fort Lauderdale", "Made to order in Fort Lauderdale", "Built to order in Fort Lauderdale"). FTC guidance: a claim "can be express or implied", references to "U.S. locations of headquarters or factories" may convey it, and an unqualified claim needs "all or virtually all" US content with "no, or negligible, foreign content"; the policy covers advertising, websites, email and social media (https://www.ftc.gov/business-guidance/resources/complying-made-usa-standard, fetched through the fetch agent). 16 CFR 323.2 makes mislabelling a rule violation (https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-323). The LED strip, adapter and dimmer are catalogue electronics that are very likely imported; the BOM does not record country of origin, so even the qualified wording needs the parts' origin confirmed.
Fix applied: replaced everywhere in marketing/ with "assembled" and, in body copy, "designed and assembled in Fort Lauderdale from US and imported parts" (the FTC guide lists "Made in USA of U.S. and imported parts" as an example of a qualified claim). Note the same guide says a simple "screwdriver" assembly "doesn't usually qualify" for a bare "Assembled in USA", which is why the qualified sentence is the default.
Needs Austin: confirm with the IP lawyer in the same hour as the named-title question. Outside this lane: site/ says "Designed in Fort Lauderdale" (fine) and "Orders ship from Fort Lauderdale" (fine).

### S1-9. SMS flows carried statutory-damages exposure for no upside
Evidence: v1 had six texts, one "immediately" and one "3 hours" after an abandoned checkout. 47 CFR 64.1200(f)(9): written consent that is not "a condition of purchasing"; 64.1200(c)(1): no calls "before the hour of 8 a.m. or after 9 p.m. (local time at the called party's location)"; 64.1200(a)(10): opt-out by "any reasonable method" (https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200). Florida has its own consent rule for automated texts with a private right of action (Fla. Stat. 501.059, leg.state.fl.us). The list will be dozens of people.
Fix applied: all SMS removed from launch; reasons and the conditions for adding it later recorded in email-sms-flows.md.

### S1-10. Spindle was wired into Higney International and Ghost Audio accounts
Evidence: v1 strategy: "Mailchimp (Austin already runs Mailchimp for HI)", "Postiz already runs for Ghost Audio"; v1 PR: "send from austin@higneyintl.com". Austin's standing rule is that these businesses are never mixed.
Fix applied: every file now requires a Spindle-only domain, mailbox, email tool, ad account and pixel.

### S1-11. Emails had no postal address and broke their own promise
Evidence: footers were "Austin / Spindle, Fort Lauderdale". 15 USC 7704(a)(5)(A)(iii) requires "a valid physical postal address of the sender" (https://www.law.cornell.edu/uscode/text/15/7704). Email 1.1 said "I'll send one email when the batch opens and one when it ships, and nothing else", then the flow sent two more sales emails and a text within five days.
Fix applied: [POSTAL ADDRESS] in every footer; welcome flow reduced to match the promise.
Needs Austin: the address.

### S1-12. Renders used as product photos, including a part that does not exist
Evidence: v1 ad 1 fallback "animate sconce_hero_chrome.png"; week-1 ads listed "render hero still"; README open item: "the renders carry the first ads". renders-final/README.md: swap and flat-lay shots show a post that does not exist. The market's own norm for pre-delivery sales: Kickstarter requires hardware creators to "show backers a prototype" and bars "photorealistic renderings anywhere" (https://www.kickstarter.com/rules/prototypes).
Fix applied: no renders in paid or organic video; any render on the page is captioned as a render; the phantom-post renders are barred; real-footage shot list at Gate 1.

### S1-13. Band-name renders and real labels
Evidence: renders-zep/png/zep_close.png (opened) is a computer-made label reading "LED ZEPPELIN" with four track titles. ops/legal.md relies on 17 USC 113(c) for showing a real label, and that section covers "pictures or photographs" of the lawfully made article (https://www.law.cornell.edu/uscode/text/17/113). A render of a band's label is our own reproduction, not a photograph of the article. v1 marketing already barred band names in ads, but allowed creators' label-showing videos to be whitelisted as our ads without saying so.
Fix applied: claims register bars renders-zep from all marketing; ugc-creators.md allows a creator video into our ad account only if no artist, label or cover is visible or spoken, pending the lawyer.
Needs Austin: the IP lawyer hour (ops/legal.md already lists it).

### S2-1. The $15 a day test could not tell a good campaign from a bad one
Evidence: at a true $45 per deposit, $150 buys about 3.3 deposits. Poisson arithmetic: the v1 kill rule ($80 per deposit after $150, that is 1 deposit or fewer) fires 15% of the time on a healthy $45 campaign and fails to fire 44% of the time on a $100 campaign.
Fix applied: $20 a day for 21 days ($420), read stage by stage, with a three-way verdict and a stated warning that even $420 leaves wide error bars.

### S2-2. Creator rates and gift costs were wrong in both directions
Evidence: v1 rate column priced a 100K TikTok creator at $1.0k to $2.5k a video from followers; v1's own budget section said $150 to $600. Our sponsorship research says to price on views and puts a 10k to 100k TikTok video at $100 to $400 (creator-sponsorship-norms-2026-08-31.md, sections 1b to 1d). v1 costed a gift Kit at about $45; cost-model.csv gives $93.07 at 20 units and $70.44 at 100. v1 expected "most will post"; the only figure found is a vendor's 20 to 40% (https://www.skeepers.io/us/blog/product-seeding/).
Fix applied: rate column deleted, view-based pricing and real gift costs written in, program cut to 5 units at Gate 2 with stage triggers.

### S2-3. Disclosure instructions to creators were too weak
Evidence: v1 allowed "#ad or #gifted ... in the caption and on screen". FTC: "the disclosure should be in the video and not just in the description"; do not rely on hashtags mixed with others (Disclosures 101, fetched through the fetch agent). TikTok: gifted product is branded content and "you must enable the commercial content disclosure toggle" (https://www.tiktok.com/legal/page/global/bc-policy/en). 16 CFR 255.1(d): "An advertiser may be liable for a deceptive endorsement even when the endorser is not liable."
Fix applied: on-screen statement plus toggle; monitoring step; sentiment-neutral gift wording per 16 CFR 465.4.

### S2-4. Organic targets had no basis
Evidence: v1: 1,000 followers per platform, ten posts over 10k, two over 100k, in 30 days, and a fifth of deposits from organic. Our own TikTok account for Ghost Audio sat at 93 to 194 views per daily post (September strategy note) and had 590 followers on 10/12 with 21% in the United States (analytics-2026-10-12.json).
Fix applied: targets withdrawn and reset (median over 500, one post over 10,000, 100 waitlist signups in the 30 days after Gate 1), with a US-share check.

### S2-5. The TikTok research was at risk of being over-claimed
Evidence: the memory note says the research was "wired in but NEVER exercised" and paused 10/20. My re-run of all 34 files: the "under 15 seconds wins" edge is 30.4x (n=61) against 20 to 25x elsewhere and the outlier rate is flat by length; the day-N pattern is 135x on n=9.
Fix applied: tiktok-laws-and-video-concepts.md states the sample for every law, drops length as a rule, and lists what does not transfer from music producers.

### S2-6. Positioning said nobody lights the record
Evidence: v1: "Nobody in that category uses a real record as the disc" and the swap "demonstrates the one thing no competitor can show". Vylumi sells a back-lit display for a real record with a wall hanger (https://vylumi.com/); Art Vinyl's frame is built around swapping without unhanging (What Hi-Fi).
Fix applied: honest competitor table; difference restated as "a room light and a fixture, not a gadget"; price anchors moved to close comparables (PETRU $239.90, Gantri $248 to $298).

### S2-7. Holiday plan sold something that cannot arrive
Evidence: v1 week 3 "Gift-certificate angle leads every email and ad from 11/24"; no parts ordered; sample run about 3 weeks; Christmas is 44 days from 11/11.
Fix applied: no holiday selling in 2026; certificate only at Gate 2 with a real ship week.

### S2-8. Selling through record stores loses money
Evidence: half of $129 is $64.50; landed cost at 100 is $76.61 (cost-model.csv).
Fix applied: stores are display only.

### S3-1. Unmeasured convenience numbers
"Swap in ten seconds", "one hand", "15-minute install", "45 minutes" in-wall. Fix: placeholders filled from timed footage (video concepts 6 and 10).

### S3-2. Hardware described wrongly
"Nothing touches your record but felt" and "three felt pads": the design has a clear PET washer on the label and six pads plus a backing ring (cad/FIXES-fable52.md; BOM.md lines 6, 6a). "Dotless" and "CRI 90+": BOM.md allows a 2835 strip, which is not dotless. Fix: copy corrected; spec words wait for the purchased strip's datasheet.

### S3-3. "UL-listed" next to the product name
Only the adapter is listed (ops/safety.md section 4). Fix: no "UL" in ads or on screen; on the page only, with "the fixture itself is not UL listed". The file number of the adapter actually bought is still open in ops/.

### S3-4. A named designer and a $755 comparison
"The Tom Dixon look for the price of a nice dinner", "$755 look. $129 price.", "Same halo. Better disc." Fix: cut.

### S3-5. Review flow filtered out unhappy buyers
v1 sent the second review ask "only if no review and no complaint". 16 CFR 465.4 and 465.7 are the relevant sections. Fix: every delivered customer gets both asks; reviews published as written.

### S3-6. Unsourced assertions presented as facts
"Reply in the first hour (algorithm)"; "founder ads outperform polished brand video"; "an ad still live after months is a winner by definition"; "CPMs spike 30 to 60%" in Black Friday week; "the day-30 supercut is the month's best-performing post"; "Houzz Pro ... ranks over time". Fix: removed or marked as untested.

### S3-7. Kickstarter was ruled out on figures that could not be confirmed
Poplight's total differs across its own pages; project pages returned 403 or 404. Fix: audit note added to pr-and-communities.md section 3 with the case for a second look. Needs Austin.

## 3. Comparables (all opened 2026-11-11)

| Brand | What I read | The repeatable law | URL |
|---|---|---|---|
| Poplight (renter sconce) | Founders' own story: two renters, a year of design, Kickstarter in February 2023 "raised over $175,000"; "we've gone multi viral on TikTok". Home page: $89 to $99, bundle builder, "Hundreds of 5 star reviews" in the title, "raised just under $200,000 in 22 minutes". Second Kickstarter built from a subscriber list and a survey of "nearly 500 customers". | A founder problem as the story; a pre-launch list before the launch; reviews in the first line; bundles to lift order size. | https://thepoplight.com/blogs/news/how-it-all-started ; https://thepoplight.com/ ; https://thepoplight.com/pages/all-about-our-kickstarter |
| Poplight press | "can be installed in under 20 seconds"; pre-orders "with a minimum pledge of $63". | One number that states the job. Launch price well under the later retail price. | https://hypebeast.com/2023/3/poplight-wall-light |
| Vylumi Nova (back-lit record display) | "Now live on Kickstarter", "Funded in 9 min", "4.82, 125 reviews", "fully refundable", early-backer bundle, "100% safe for your records ... no heat and no warping", desk stand and wall hanger. | The closest competitor. Safety is the headline; the bundle is the offer; refundable is said up front. | https://vylumi.com/ |
| PETRU (lit Now Playing stand) | $239.90, "812 reviews", "a father and son business", "Find a retailer", links to YouTube reviewers. | Collectors pay over $200 for lit display hardware when reviews exist; outside reviewers are shown on the product page. | https://petrudesign.com/ ; https://petrudesign.com/pages/about-us |
| Gantri (designer lighting) | Wall lights $248 to $298; spec line "2700K ... 90+ CRI ... fully dimmable"; first retail partnership with Room & Board announced. | The spec language we use is the premium category's own; retail comes after the direct business is proven. | https://www.gantri.com/ ; https://www.gantri.com/news/gantri-launches-first-retail-partnership-with-room-board |
| Custom Neon (LED neon signs) | Tested demand with local listings before buying stock; first stock cost about $250; "During the first 12 months, we didn't need to spend a dime on advertising"; a note in every box asking for a tagged photo; "$10,000 worth of signage per week" within three months. | Customer photos before ads; ask every buyer for a photo; spend little before demand is shown. | https://buffer.com/resources/side-hustle-to-business/ |
| Yellowpop (neon signs) | Agency case study: revenue "multiplied by more than 12 in one year" after paid was restructured across Meta, Pinterest, Snapchat. | Paid scaling came after a product with visual appeal and a catalogue existed. Self-reported by the agency. | https://junto.fr/en/references/yellowpop |
| Art Vinyl Flip Frame | "some 200,000 customers" for the 12 in frame over about ten years; Kickstarter for the 7 in at 23 to 30 GBP. | Swap-without-unhanging is a proven want; the proven price for a frame is low. | https://www.whathifi.com/news/artvinyl-launches-vinyl-storage-kickstarter |
| Record Props | Wall and tabletop display; holiday banner with 60-day returns; gift-guide blog posts of its own. | Generous returns in Q4; own the "gifts for vinyl lovers" search with your own page. | https://recordprops.com/ |
| Sunset lamp wave | "The $20 pick-me-up, made famous on TikTok ... on sale for $14". | The viral lighting wave was an impulse price. Do not expect its curve at $129. | https://www.domino.com/content/tiktok-sunset-lamp/ |
| Kickstarter rules | Hardware must "show backers a prototype"; no "photorealistic renderings anywhere". | The norm for asking for money before delivery. | https://www.kickstarter.com/rules/prototypes |
| Meta benchmark panel | 19 accounts, $2.88M: CPM $13.40, CPC $0.59, CTR 2.65%, ROAS 2.55 (middle half 1.82 to 3.87), cost per purchase $33.80 (middle half $24.97 to $51.09), click-to-purchase 1.79%. | The yardstick for section 4 of the strategy. Managed accounts with history; a new account should expect worse. | https://topgrowthmarketing.com/dtc-ecommerce-benchmarks/meta-ads-benchmarks/ |
| Lebesgue benchmarks | Art and home decor: CPM $8.09, CTR 2.92%, conversion 0.61%, CAC $26.16. | A second, lower conversion estimate. Method not shown. | https://lebesgue.io/facebook-ads/facebook-benchmarks-by-industry-ctr-cpm-cr-and-cac |

TikTok clips checked with yt-dlp: @alexjbauer 7067687660994710830 (27.2M views, 55 s); @pridoladesign 7507278189312347422 (492,100, 17 s); @creatively.crisp 7687237967068351774 (313,400, 30 s); @wexelart 7652467680317934862 (198,400, 26 s).

## 4. How the TikTok research was used

Read: tiktok-pattern-strategy-2026-09-17.md, viral-plugins-and-new-concept-2026-09-22.md, creator-sponsorship-norms-2026-08-31.md (sections 1, 2, 4, 5, 6, 7d), the outliers folder (the 10/19 report and a re-computation over all 34 JSON files: 4,063 unique videos, 732 unique outliers), the audience folder (9/17 map, 10/12 analytics), and the memory note with the verdict. Result: marketing/tiktok-laws-and-video-concepts.md. Ten laws transfer, each with its sample size; four findings are specific to music producers and are excluded; the research has never been tested by our own posting and the file says so.

## 5. What I could not verify

- ftc.gov pages returned 403 to my browser; the three FTC guides were read through the fetch agent, which reported verbatim text for roughly the first 40,000 characters of the two long guides and a summary of the rest. Whether the mail order guide addresses pre-orders or made-to-order goods specifically: not confirmed.
- Kickstarter project pages (Poplight 403, Vylumi 404 at a guessed URL). No campaign total in the plan is confirmed.
- The 17 Meta Ad Library references and 13 of the 17 TikTok references in ad-concepts.md: not re-opened.
- All 48 creator profiles: not re-read (v1 read them on 11/9). No creator's recent average views were checked.
- Subreddit rules: not re-read. PETRU's Reddit origin thread: found in search, could not be opened.
- Apartment Therapy and Magnetic Magazine pages: blocked. Twelve Inch Art and Deep Cut: the domains I tried did not resolve; not checked.
- Meta's rule on showing renders or taking pre-orders: only the general "Prohibited Commercial Practices" page was opened; it has no specific text on either.
- Stripe: the restricted-businesses page was opened and does not mention pre-orders; Stripe's handling of long-dated pre-orders and disputes was not checked.
- Florida quiet hours and message caps for texts: not checked (only 501.059 was opened).
- Whether "assembled in Fort Lauderdale from US and imported parts" is safe for this exact parts list: a lawyer's call.
- Deposit-to-purchase rate for a $25 deposit on a $129 product: no source exists that I could find; 50% is a planning assumption.
- site/ was not audited here. One grep shows site/index.html still says "First 20 sold out" next to the deposit offer; under this audit that line and the live deposit both wait for their gates. That is the website auditor's lane.

## 6. The five things most likely to make this campaign fail

1. The unit does not exist, and nothing can be sold honestly until it does. Every week without ordered parts is a week of build-diary posts and nothing else. Parts order and heat test are the campaign's real start date.
2. The product does not pay at these prices, with or without ads. The $129 Sconce clears $12.77 against a $34 median cost per purchase for experienced accounts, the Kit loses $19.90 an order, and the Set is not buildable. If the plan drifts back to "ads will get us to 100", it loses money on each order. The fixes are price (Kit), order size (in-wall kit, second unit), full pre-order, the 7 in redesign, or Kickstarter.
3. A claim gets ahead of the proof. One "runs cool" or "sold out" before the test and the ledger, and the brand is arguing with collectors, the people least forgiving about heat near a record, with a competitor already advertising "no warping".
4. A ship week is promised and missed. The first 20 are unbuilt, chrome caps are the long pole, and one person is both the factory and the marketing department. A missed date triggers refunds by rule and disputes in practice.
5. Organic never finds an audience. Our only track record is about 100 to 200 views a post on a different account. If 20 real-footage posts cannot pass 3,000 views once, there is no cheap channel, and the honest answer is a smaller, slower, word-of-mouth product or a crowdfunding launch, not a bigger ad budget.
