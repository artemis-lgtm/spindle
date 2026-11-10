# CRO research for the Spindle launch site

Compiled 2026-11-09 for the "Side A" launch page (The Spindle: Kit $89, Sconce with vintage record $129, Named title $179, 3-piece Set $249 kit or $329 with records; batch one of 20 sold out; batch two takes a $25 refundable deposit plus a free email waitlist).

Method: live fetches of each site on 2026-11-09 (WebFetch plus curl for Baymard), plus primary sources for the legal and benchmark claims. Every factual claim below carries the URL it came from. Anything I could not confirm on the live page is marked UNVERIFIED or ESTIMATE. Note the fetch date: it is Black Friday season, so several sites were running sale banners that are seasonal, not their resting state.

Limits of this pass, stated up front:
- Gantri product pages are client-rendered and returned only nav and footer to the fetcher, so Gantri PDP mechanics are from the homepage only.
- CXL, LaunchBoom, BackerKit and Kickstarter's handbook returned HTTP 403 to every fetch method I tried, so I could not pull their numbers directly.
- Schoolhouse and Our Place product URLs I guessed returned 404; their findings are homepage level.
- Godly (godly.website) now 301-redirects to recent.design, so it is not cited as a pattern source.

---

## Part 1: Site-by-site teardown

### 1. Gantri
URL: https://www.gantri.com

- Above the fold: hero is a styled room shot of the Pleat Table Light, headline "Inspired lighting for creative living", single CTA "Shop best sellers". No price above the fold. (https://www.gantri.com)
- Spec line placed near the hero: "Warm, inviting 2700K light. True-to-life color with 90+ CRI. 600+ lumens, fully dimmable." (https://www.gantri.com)
- Variants: no swatches on the homepage hero, but one image shows three portable lights in white, red and black to imply the range. Product links carry a `?sku=` parameter per finish (for example `?sku=10065-sm-carbon` on the Gio wall light), which suggests each finish is a deep-linkable SKU. (https://www.gantri.com, observed in page links)
- Social proof: none above the fold on the homepage (no stars, no press logos). Nav includes an "Award winning" collection. (https://www.gantri.com)
- Made-to-order framing: "Made on demand in California" and "Less waste, from start to finish". (https://www.gantri.com)
- Sticky ATC, FAQ, PDP layout: UNVERIFIED (client-rendered PDP did not return content).
- Steal this: the spec line. Three numbers (2700K, 90+ CRI, 600+ lumens) answer the lighting buyer's real objection, "will it look warm and good in my room", before they click anything. The Spindle should publish its color temperature and lumen output in plain numbers right under the hero.

### 2. Schoolhouse
URL: https://www.schoolhouse.com

- Above the fold: seasonal campaign hero ("Layers of the Season") with a "SHOP NOW" CTA, then product tiles that each show name plus price plus "Shop Now", for example "Alabax Large Flush Mount $259.00" and "Evelyn Mini Table Lamp $299.00". (https://www.schoolhouse.com)
- Variants: no swatches on homepage tiles. PDP swatch behavior UNVERIFIED (product URL attempts returned 404).
- Social proof: brand-story rather than reviews, for example "pieces worth owning should stand the test of time". (https://www.schoolhouse.com)
- Lead time: a dedicated "Ready to Ship" collection exists, which implies the rest of the catalog carries lead times. (https://www.schoolhouse.com/collections/ready-to-ship, linked from the homepage)
- Returns: return policy linked in the footer. (https://www.schoolhouse.com)
- Steal this: price on every product tile. Schoolhouse sells $259 to $549 lighting and still shows the number on the homepage card. No "see price on next page" friction.

### 3. Teenage Engineering
URLs: https://teenage.engineering , https://teenage.engineering/store , https://teenage.engineering/store/ep-133

- Above the fold: deliberately playful, not conversion-optimized. The hero for one product uses copy like "THIS SHADOW IS unrealistically LONG... ARE YOU HIDING SOMETHING?" with a CTA "agree!" that routes to the product page, paired with a weekly email signup. (https://teenage.engineering)
- Store grid: "add to cart" on every card, "reduced price" labels on some items, footer promise "free shipping over $120" and a "14 day return policy". (https://teenage.engineering/store)
- PDP (EP-133): "buy" and "add to cart" CTAs, a tight spec list (built-in mic and speaker, 128MB sample storage, USB-C, dimensions 240 x 176 x 16 mm). No reviews section. (https://teenage.engineering/store/ep-133)
- Waitlist / notify: none visible at fetch time on the items checked. (https://teenage.engineering/store)
- Steal this: voice. A brand with a distinctive tone can skip reviews entirely when the object and the copy carry the proof. For a 20-unit hand-built batch with no review corpus yet, a confident, specific voice plus hard specs is the honest substitute.

### 4. Rejuvenation
URL: https://www.rejuvenation.com

- Above the fold: rotating carousel with "New Arrivals are In-Stock" and an explicit delivery window "At Your Door in 1-6 Weeks", plus a sale banner and "Free Shipping*". (https://www.rejuvenation.com)
- Made to order: "Made to Order. A Custom Lighting Experience. Explore hand-assembled collections from our Portland, Oregon factory." (https://www.rejuvenation.com)
- Services as proof: "Design Crew ... we're here to help, for free. BOOK AN APPOINTMENT" (paraphrased punctuation). (https://www.rejuvenation.com)
- Variants: finish swatches not visible at homepage level; PDP UNVERIFIED.
- Steal this: they state a delivery window range on the homepage itself ("1-6 Weeks") and name the place where things are assembled. A named workshop plus a stated window is exactly what a batch-made sconce should lead with.

### 5. Ember
URLs: https://ember.com , https://ember.com/products/ember-mug-3

- Above the fold (home): headline "Your coffee. Perfectly warm.", two CTAs "Buy Mug 3" and "How Ember works", price block "$149.95 USD $99.99 USD" (seasonal sale), "14 oz · 8 colors". (https://ember.com)
- Trust bar: "Over 4 Million Sold", "30-day returns", "Lifetime coaster warranty", "Free shipping", "Free sliding lid ($14.95 value) · coaster included". (https://ember.com)
- Variants: eight circular swatches; selecting one swaps the gallery to that color in multiple contexts. (https://ember.com/products/ember-mug-3)
- Social proof: "4.6 / 5 · 162 reviews" shown prominently on the PDP with expandable review cards. (https://ember.com/products/ember-mug-3)
- Sticky ATC: persistent "Add to cart" with quantity control. (https://ember.com/products/ember-mug-3)
- FAQ: answers the top functional objections in plain numbers, for example "over 3 hours with the included sliding lid, or 80 minutes without the lid". (https://ember.com/products/ember-mug-3)
- Steal this: "what's in the box" valued in dollars ("Free sliding lid ($14.95 value) · coaster included"). For the Spindle, "record included" on the $129 SKU is the same move: show what the record would cost on its own.

### 6. Our Place
URL: https://fromourplace.com

- Above the fold: sale hero "Save Up to 45%*" with a "Shop sale" CTA, and a set anchored against its parts: "Titanium Pro Cookware Set $399 ($698 value)". (https://fromourplace.com)
- Risk reversal in the header: "Free Shipping on $135+, 100-Day Trial", and a benefits bar "Free shipping $135+", "100 Day Trial", "Free Returns". (https://fromourplace.com)
- Variants: color names are part of the brand (Blue Salt, Sage, Char, Steam, Spice, Terracotta), with color-specific carousel imagery. (https://fromourplace.com)
- Referral: "Get $20" in the header. (https://fromourplace.com)
- Social proof, sticky ATC, FAQ: not visible in the homepage fetch; PDP UNVERIFIED (404 on guessed URL).
- Steal this: the set-versus-parts anchor ("$399 ($698 value)"). The Spindle 3-piece Set can be shown against three singles: $329 for three record sconces versus 3 x $129 = $387, so the set saves $58. That is a true, checkable number, not a manufactured "value".

### 7. Tom Dixon (price anchor)
URL: https://www.tomdixon.net

- Press Large Surface Light, "Clear Pressed Glass", listed at £510 in the homepage "Trending & Bestsellers" carousel (UK storefront; the US-specific deep link redirected to the US home, so the USD price is UNVERIFIED). (https://www.tomdixon.net)
- Presentation: image, name, material line, price. Nothing else on the card. (https://www.tomdixon.net)
- Steal this: a material line under the product name ("Clear Pressed Glass"). Ours is "Original 12-inch vinyl, warm halo backlight". And as an anchor: a designer surface light in the same visual category sits around £510, so a $129 sconce with a real record reads as accessible design, not a novelty. Use this framing internally for pricing confidence, not as a named comparison on the page.

### 8. Poplight
URLs: https://thepoplight.com , https://thepoplight.com/products/black

Closest direct comp: a DTC wall sconce in the same price band.
- Above the fold (PDP): "Matte Black Poplight", "Regular $99.00, Sale $89.00", "Add to cart". (https://thepoplight.com/products/black)
- Variants: eight color tiles as image thumbnails; selecting one swaps photos and details. (https://thepoplight.com/products/black)
- Social proof: "4.94/5 based on 224 reviews" directly below the price, with a star distribution lower on the page. (https://thepoplight.com/products/black)
- Shipping and returns, right at the buy box: "Fast Shipping (delivered within 4 days)", "Orders dispatched within 48 hours", "30-Day Money-Back Guarantee". (https://thepoplight.com/products/black)
- FAQ: accordion with the real objections: "How bright is Poplight?", "Can I change Poplight's bulb?", "How long does the battery last?". (https://thepoplight.com/products/black)
- Sticky ATC: yes. (https://thepoplight.com/products/black)
- Urgency: "64 people added to cart in the past 12 hours". This is the exact message shape the FTC lists as "False High Demand" when untrue (see Part 2). I cannot verify whether Poplight's number is real; the point is that we do not copy this widget. (https://thepoplight.com/products/black)
- Steal this: the three-line delivery promise stacked under the CTA (dispatch time, delivery time, guarantee). Also the FAQ question list, nearly verbatim in structure: brightness, bulb, power.

### 9. Allbirds
URL: https://www.allbirds.com/products/mens-wool-runners

- Above the fold: title, "$110", CTA that includes the price ("Add to Cart - $110"), "+ Free shipping". (https://www.allbirds.com/products/mens-wool-runners)
- Out-of-stock handling: when unavailable, the ATC is disabled and a "Notify Me" back-in-stock alternative appears in its place. (https://www.allbirds.com/products/mens-wool-runners)
- Fit reassurance next to the picker: "fits true-to-size for most customers" plus a Fit Guide link. (https://www.allbirds.com/products/mens-wool-runners)
- Steal this: the price inside the button label, and Notify Me living in the same slot as the buy button so the sold-out state never becomes a dead end. Our equivalent: the CTA slot shows "Reserve batch two, $25 deposit" and a secondary "Just notify me (free)".

### 10. Glossier
URL: https://www.glossier.com/products/cloud-paint

- Above the fold: "Cloud Paint", "Seamless cheek color", "Add to bag $24", subscription option "Save 10% on all subscription orders". (https://www.glossier.com/products/cloud-paint)
- Variants: 11 named shade tiles; selecting one swaps imagery to the shade on different models. (https://www.glossier.com/products/cloud-paint)
- Sticky "Add to bag", free-shipping threshold "$40+", per-customer quantity cap of 20, "Notify me" for out-of-stock shades, an engraving option. (https://www.glossier.com/products/cloud-paint)
- Steal this: named variants. Glossier names shades (Puff, Storm, Dusk) rather than numbering them. Our record finishes or label colors can carry names too, and the "Named title" SKU is literally personalization, the same psychological lever as Glossier's engraving.

### 11. Framework (pre-order deposit model, added because it is the closest working analog to our batch-two deposit)
URL: https://frame.work/products/laptop13-diy-amd-ai300

- Deposit copy: "Secure your pre-order with a deposit. Cancel any time before shipment for a full refund." (https://frame.work/products/laptop13-diy-amd-ai300)
- Batch mechanics: the configurator shows "Batch Number" and separate "Est. Price" and "Deposit" fields, so the buyer sees both what they pay now and what the full price will be. (https://frame.work/products/laptop13-diy-amd-ai300)
- Deposit amount and balance-charge timing: UNVERIFIED (the FAQ URL I tried returned 404).
- Steal this: the two-field display (deposit now, estimated total later) plus the one-sentence cancel promise. That is the whole batch-two buy box.

### Award and pattern sources
- Awwwards e-commerce category, recent honorees at fetch time: Spyker Cars (Site of the Day, 2026-10-30), Lajoya, Theobroma, Second Ride, Deadly Ponies (Honorable Mentions, October 2026). The category describes itself around "best UX practices for shopping cart, product display, customer service, checkout process". (https://www.awwwards.com/websites/e-commerce/) Note: Awwwards rewards visual craft; it is evidence of what looks premium, not of what converts. Use Baymard for conversion evidence.

---

## Part 2: Pattern evidence (benchmarks and law)

### Baymard Institute, product page UX
Source: https://baymard.com/blog/current-state-ecommerce-product-page-ux (updated 2026-03-18)
- Only 48% of leading desktop sites and 38% of mobile sites have "decent" or better product page UX.
- Top pitfalls with share of sites getting it wrong: no "In Scale" images (37% don't), no "Total Order Cost" estimate near the buy section (67% don't), return policy not displayed or linked from main product content (44% don't), not navigating reviews via reviewer images (63% don't), not responding to negative reviews (89% don't).

Source: https://baymard.com/blog/in-scale-product-images
- "42% of users will attempt to gauge the overall scale and size of a product from its product images."
- "56% of the test subjects' first actions upon arriving at a new product page was to begin exploring the product images, before reading titles, descriptions" (quote trimmed).

Source: https://baymard.com/blog/always-use-thumbnails-additional-images (2020-10-20)
- Only 24% of mobile benchmark sites use thumbnails for additional gallery images versus 100% on desktop; when only dot indicators were used, "50% of desktop users had trouble finding these additional product images".

### Baymard, cart abandonment
Source: https://baymard.com/lists/cart-abandonment-rate
- Average documented abandonment 70.22% across 50 studies.
- Reasons (excluding the browsers): extra costs too high 40%, delivery too slow 20%, distrust with card security 19%, forced account creation 18%, unsatisfactory returns policy 13%, could not see total cost upfront 12%.

### Shopify
Source: https://www.shopify.com/blog/ecommerce-conversion-rate (updated 2026-08-22)
- Home and furniture category average conversion 1.29%; global average 2.66% (Dynamic Yield benchmark cited by Shopify). Plan the funnel against roughly 1 to 1.5% for a lighting PDP, not the 3% headline numbers.
- 2025 US abandonment drivers repeated: extra costs 39%, slow delivery 21%.

Source: https://www.shopify.com/blog/pre-orders
- "Share the estimated shipping or delivery date wherever you promote the preorder, including: Announcement bars, Product pages, Checkout pages, Order confirmation emails."
- Payment structures named: pay now, "Pay Later: Deposit or payment at fulfillment" (described as a way to test demand), and subscription.
- "Send an email reminder before charging the stored payment method so the customer knows when the payment will occur."

### Reviews (Spiegel Research Center, Northwestern)
Source: https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/
- "The purchase likelihood for a product with five reviews is 270% greater than the purchase likelihood of a product with no reviews."
- Review impact is larger on higher-priced products: conversion rose 380% for higher-priced items versus 190% for lower-priced.
- "purchase likelihood typically peaks at ratings in the 4.0 to 4.7 range, and then begins to decrease as ratings approach 5.0."
- Implication: our first five real reviews from batch one are worth more than any other content on the page. Collect them before batch two ships.

### Speed
Source: https://www.deloitte.com/ie/en/services/consulting/research/milliseconds-make-millions.html
- A 0.1 second mobile speed improvement: "Retail conversions increased by 8.4% and average order value increased by 9.2%." Luxury page views per session rose 8.6%.

Source: https://web.dev/articles/vitals
- Good thresholds: LCP within 2.5 s, INP 200 ms or less, CLS 0.1 or less, measured at the 75th percentile of page loads, split by mobile and desktop.

### FTC dark patterns report
Source: https://www.ftc.gov/reports/bringing-dark-patterns-light (Staff Report, September 2022; PDF text extracted from the linked report)
- Lists as deceptive design: "False Low Stock Message: Creating pressure to buy immediately by saying inventory is low when it isn't. Example: 'Only 1 left in stock, order soon'".
- "False High Demand Message ... Example: '20 other shoppers have this item in their cart'".
- "Baseless Countdown Timer: ... a fake countdown clock that just goes away or resets when it times out".
- "False Limited Time Message: ... without a deadline or with a meaningless deadline that just resets when reached".
- "False Activity Messages: Making false claims about others' activity on a site or interest in a product. Example: '24 other people are viewing this listing'".
- The report quotes the UK CMA: "Numerous experiments and studies find an effect of scarcity claims on click-through rates, purchase, perceived value". So scarcity works, which is exactly why it must be true.

### FTC Mail, Internet, or Telephone Order Merchandise Rule (16 CFR Part 435)
Sources: https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule and https://www.ftc.gov/legal-library/browse/rules/mail-internet-or-telephone-order-merchandise-rule
- You must have a "reasonable basis" for any shipping claim, defined as information "that would under the circumstances satisfy a reasonable and prudent businessperson, acting in good faith, that the representation is true."
- If no time is stated, you must have a reasonable basis to ship "within thirty (30) days after receipt of a properly completed order."
- If you cannot ship on time, you must promptly send a delay notice with a revised date (or a statement that you don't know), the buyer's right to cancel, and a free way to cancel. For delays of 30 days or less, silence counts as consent; beyond that the buyer must affirmatively consent or the order is cancelled.
- Refunds for card payments are due within "seven (7) working days" of the refund right vesting.
- The rule covers internet orders regardless of payment method. Whether a $25 refundable deposit that reserves a place in a batch is an "order" under the rule is a legal question I did not resolve. ESTIMATE: treat it as one and comply anyway, because compliance costs us nothing and the copy below already does it.

### Deposit versus free waitlist conversion
- Verified: Shopify names deposits as a recognized preorder structure and specifically as a way to test demand (https://www.shopify.com/blog/pre-orders). Framework runs a production business on refundable deposits with batch numbers and cancel-anytime language (https://frame.work/products/laptop13-diy-amd-ai300).
- UNVERIFIED (could not fetch the sources, all 403): the crowdfunding agencies (LaunchBoom, BackerKit) publish that free email leads convert to buyers at low single-digit percentages while small paid reservations (often $1) convert at many times that rate. I have seen figures in the range of 2 to 5% for free emails and 20 to 50% for paid reservations quoted secondhand, but I could not open a primary page to confirm them, so treat them as ESTIMATES and do not put them in any deck as fact.
- Reasoned position (ESTIMATE): a deposit trades volume for intent. Expect far fewer deposits than emails, but each deposit is a much stronger demand signal. Running both, deposit as primary and free email as secondary, captures the committed buyer without losing the curious one. Measure: deposits per 100 PDP visits, emails per 100 PDP visits, and later, deposit-to-balance conversion. Those three numbers are the batch-two sizing data.

---

## Part 3: Patterns we apply

### 1. Above the fold: product, price, CTA, all three, on a 390 px screen
- Every comp that converts puts a price and a buy action in the first screen: Ember (https://ember.com), Poplight (https://thepoplight.com/products/black), Allbirds (https://www.allbirds.com/products/mens-wool-runners), Glossier (https://www.glossier.com/products/cloud-paint). Gantri and Teenage Engineering are the exceptions on their homepages, and they are brand plays with large catalogs, not single-product launches.
- Apply: hero image of the lit sconce on a wall (halo visible), product name, one line of material ("Original 12-inch vinyl, warm halo backlight"), "From $89", primary CTA "Reserve batch two, $25 refundable", secondary text link "Or join the free waitlist". Put the price inside the button where it fits, per Allbirds.
- Add the Gantri-style spec line within the first two screens: color temperature, lumens, power method, diameter. Use our real measured numbers only.

### 2. Social proof placement
- Directly under the price, the way Poplight ("4.94/5 based on 224 reviews") and Ember ("4.6 / 5 · 162 reviews") do it (https://thepoplight.com/products/black, https://ember.com/products/ember-mug-3).
- We have 20 real buyers and no review corpus yet. Do not show stars until we have at least five real reviews (Spiegel's five-review threshold, https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/). Until then the honest proof is: "Batch one: 20 made, 20 sold." That is true, specific and checkable.
- When reviews come in, include buyer photos of the sconce on their own walls: Baymard finds 63% of sites fail to let users browse reviews by reviewer images (https://baymard.com/blog/current-state-ecommerce-product-page-ux), and those photos double as in-scale images.
- If a reviewer got a free unit or knows us, disclose it; the FTC lists undisclosed connections under "Deceptive Consumer Testimonials" (https://www.ftc.gov/reports/bringing-dark-patterns-light).

### 3. Sticky ATC on mobile
- Ember, Poplight and Glossier all keep the buy action persistent on scroll (https://ember.com/products/ember-mug-3, https://thepoplight.com/products/black, https://www.glossier.com/products/cloud-paint).
- Apply: a bottom bar that appears once the hero CTA scrolls out of view, showing the selected SKU, its price, and "Reserve, $25". Keep it under about 64 px tall, respect the iOS safe-area inset, and do not let it cover the FAQ accordion toggles. Reserve its space in CSS so it causes no layout shift (CLS target 0.1 or less, https://web.dev/articles/vitals).

### 4. Swatch and SKU selector with image swap
- Ember, Poplight and Glossier all swap the gallery when a variant is chosen (https://ember.com/products/ember-mug-3, https://thepoplight.com/products/black, https://www.glossier.com/products/cloud-paint).
- Apply: four SKU buttons (Kit, Sconce with record, Named title, Set). Baymard says to use buttons, not dropdowns, for selection (57% of sites don't, https://baymard.com/blog/current-state-ecommerce-product-page-ux). Each button swaps the hero image to that SKU and updates the sticky bar price.
- The Set button shows the true savings against singles: $329 versus 3 x $129 = $387, save $58; kit set $249 versus 3 x $89 = $267, save $18. This is the Our Place anchor done honestly (https://fromourplace.com).
- Show gallery thumbnails on mobile, not just dots (only 24% of mobile sites do, https://baymard.com/blog/always-use-thumbnails-additional-images).
- Include one in-scale image: the sconce on a wall next to a light switch or a framed print, with the diameter stated (https://baymard.com/blog/in-scale-product-images).
- Include an "in the box" image for the Kit SKU, so the buyer knows the record is not included at $89.

### 5. FAQ as objection handling
- Poplight's FAQ is built from the real questions: brightness, bulb, battery (https://thepoplight.com/products/black). Ember answers with numbers (https://ember.com/products/ember-mug-3).
- Our list, in this order: How bright is it, and what color is the light? How does it power (plug-in cord, hardwire, battery)? How does it mount, and do I need an electrician? Is the record a real vintage pressing, and can I choose it? What does "Named title" mean and how do I pick? When will batch two ship? Is the $25 really refundable, and how? What is the return policy? Will the heat or light damage the record?
- Link the return policy from the buy box, not only the footer (44% of sites fail this, https://baymard.com/blog/current-state-ecommerce-product-page-ux; 13% of abandoners cite returns, https://baymard.com/lists/cart-abandonment-rate).
- Show shipping cost or "shipping calculated at balance" near the buy box. Extra costs are the top abandonment reason at 40% (https://baymard.com/lists/cart-abandonment-rate) and 67% of sites fail to show a total cost estimate (https://baymard.com/blog/current-state-ecommerce-product-page-ux).

### 6. Scarcity only when true
- The FTC report names false low stock, false high demand, baseless countdowns, false limited time offers and false activity messages as dark patterns (https://www.ftc.gov/reports/bringing-dark-patterns-light).
- What we can say, because it is true: "Batch one: 20 made, sold out." "Batch two is a small batch of N." (N must be the real planned quantity.) "N of N reserved", but only if the counter reads from the actual deposit records and updates; never a hardcoded number.
- What we never ship: "X people are viewing this", "X added to cart in the last 12 hours" (the Poplight widget, https://thepoplight.com/products/black), any countdown timer without a real fixed deadline, any "only 2 left" that is not a live inventory read.
- If batch two closes on a real date, a countdown to that date is fine, as long as it does not reset and the date is honored.

### 7. Deposit plus free waitlist
- Primary CTA: $25 refundable deposit via Stripe. Secondary: free email. Two separate slots, like Allbirds' ATC versus Notify Me (https://www.allbirds.com/products/mens-wool-runners).
- Copy pattern from Framework: "Secure your pre-order with a deposit. Cancel any time before shipment for a full refund." (https://frame.work/products/laptop13-diy-amd-ai300) Show both the deposit and the full price: "Due today: $25. Balance at shipping: $104 (Sconce with record, $129 total)."
- Before charging any balance, send a reminder email with the amount and date, per Shopify's preorder guidance (https://www.shopify.com/blog/pre-orders).
- Conversion expectations are ESTIMATES (see Part 2). Instrument both paths from day one.

### 8. Page speed and image weight
- Target LCP 2.5 s or less on mobile at p75, INP 200 ms or less, CLS 0.1 or less (https://web.dev/articles/vitals). A 0.1 s mobile speed gain moved retail conversion 8.4% in Deloitte's study (https://www.deloitte.com/ie/en/services/consulting/research/milliseconds-make-millions.html).
- Working budget (ESTIMATE, our own engineering targets, not from a cited source): hero image as AVIF or WebP at about 1200 px wide for mobile, ideally under 150 KB, served with `srcset` and `sizes`; preload the hero and set `fetchpriority="high"` on it; lazy-load everything below the fold; explicit `width` and `height` on every image to stop layout shift; total page weight under about 1 MB on first load; no third-party scripts in the head except Stripe on the checkout step; system or one self-hosted font file with `font-display: swap`.
- Halo glow is the product. Photograph it, do not fake it with CSS blur on top of a photo, which costs paint time and looks off.

### 9. Pre-order copy that satisfies the Mail Order Rule (16 CFR 435)
Rule basis: reasonable-basis shipping claims, 30-day default when no date is stated, delay notice with right to cancel, refunds within 7 working days for card payments (https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule).

Draft copy for the buy box and the confirmation email:
- "Batch two ships by [specific date]." Only state a date we have a reasonable basis for: parts in hand or on order with confirmed lead times, and build capacity known. If we cannot back a date, say "We expect to ship in [month]. We will email you a firm date before charging your balance." Never leave the date out entirely, since silence defaults us to a 30-day promise.
- "Your $25 deposit is fully refundable until your sconce ships. Reply to any of our emails or use the link in your confirmation to cancel. Refunds go back to your card within 7 business days." (The rule says 7 working days; stating the same window keeps us inside it.)
- "If batch two slips past [date], we will email you the new date and you can cancel for a full refund, no questions."
- "Your balance of $[X] is charged only when your sconce is ready to ship. We'll email you before we charge."
- Shipping cost shown or stated as included before the deposit is taken.
- Operationally: if the date slips, send the delay notice before the promised date passes, include a one-click cancel, and for any delay over 30 days, require the buyer to opt in or refund them automatically.

### 10. Small things the comps all do
- A named, visible delivery promise stacked under the CTA (Poplight: dispatch time, delivery time, guarantee, https://thepoplight.com/products/black; Rejuvenation: "At Your Door in 1-6 Weeks", https://www.rejuvenation.com).
- A named workshop (Gantri: "Made on demand in California", https://www.gantri.com; Rejuvenation: "hand-assembled ... Portland, Oregon factory", https://www.rejuvenation.com). Ours: where the Spindle is actually built, stated plainly.
- Named variants (Glossier shade names, https://www.glossier.com/products/cloud-paint; Our Place color names, https://fromourplace.com).
- Value stated in dollars for what is included (Ember's "$14.95 value" lid, https://ember.com). Ours: the record is included on the $129 SKU. Only state a dollar value for the record if we can source a real typical price for that pressing; otherwise just say "record included".

---

## Part 4: What not to copy
- Sale-price strikethroughs (Ember, Poplight, Our Place at fetch time) only make sense with a genuine former price. We have no former price for batch two, so no strikethrough. The FTC report lists "False Discount Claims" among the dark patterns (https://www.ftc.gov/reports/bringing-dark-patterns-light).
- Cart-activity widgets (Poplight). See Pattern 6.
- Mystery-first heroes (Teenage Engineering). It works for a cult brand with 143 products and an audience that already knows them (https://teenage.engineering/store). A brand-new single-product launch needs the product and price on screen one.
- Credit and financing banners (Rejuvenation's card offer, https://www.rejuvenation.com). Irrelevant at $89 to $329 and adds noise.

---

## Source list
- https://www.gantri.com
- https://www.schoolhouse.com
- https://teenage.engineering
- https://teenage.engineering/store
- https://teenage.engineering/store/ep-133
- https://www.rejuvenation.com
- https://ember.com
- https://ember.com/products/ember-mug-3
- https://fromourplace.com
- https://www.tomdixon.net
- https://thepoplight.com
- https://thepoplight.com/products/black
- https://www.allbirds.com/products/mens-wool-runners
- https://www.glossier.com/products/cloud-paint
- https://frame.work/products/laptop13-diy-amd-ai300
- https://www.awwwards.com/websites/e-commerce/
- https://baymard.com/blog/current-state-ecommerce-product-page-ux
- https://baymard.com/blog/in-scale-product-images
- https://baymard.com/blog/always-use-thumbnails-additional-images
- https://baymard.com/lists/cart-abandonment-rate
- https://www.shopify.com/blog/ecommerce-conversion-rate
- https://www.shopify.com/blog/pre-orders
- https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/
- https://www.deloitte.com/ie/en/services/consulting/research/milliseconds-make-millions.html
- https://web.dev/articles/vitals
- https://www.ftc.gov/reports/bringing-dark-patterns-light
- https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule
- https://www.ftc.gov/legal-library/browse/rules/mail-internet-or-telephone-order-merchandise-rule

Not reachable at fetch time (cited only as unverified): CXL product page guide, LaunchBoom reservation guides, BackerKit blog, Kickstarter handbook (all HTTP 403); Godly (redirects to recent.design).
