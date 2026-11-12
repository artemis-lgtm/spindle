# Spindle: launch site

Static, mobile-first, no build step. Twelve plain HTML pages, one stylesheet, one script, self-hosted fonts, compressed renders. Built 2026-11-09 night. Not deployed anywhere.

## What is here

| Path | What |
|---|---|
| `index.html` | Home. Dark-room hero that turns on (scroll, tap, or the dimmer slider), "Your record. Your light." story, finish picker, how it works, change-the-record, true-numbers proof strip, FAQ preview, reserve block. |
| `product.html` | The Spindle. Gallery with finish-swapping main image, SKU picker (Kit $89 / Sconce $129 / Named $179 / Set $249 or $329 with records), swatches (chrome, brass, black), what is in the box per SKU, spec table, sticky mobile buy bar. |
| `install.html` | Mount, in-wall default (cutaway), surface option, hardwired option, heat in numbers. |
| `faq.html` | Twelve questions (heat, warping, record safety, wiring, renters, brightness, which records, what record ships, ship date, deposit refund, shipping and returns, UL). FAQPage JSON-LD. |
| `about.html` | Fort Lauderdale story, the no-glue rule, non-affiliation statement. |
| `reserve.html` | Model + finish picker, then the two offers: $25 refundable Stripe deposit and the free waitlist form. |
| `thanks.html` | Waitlist confirmation. Fires the Meta `Lead` event. |
| `thanks-deposit.html` | Deposit confirmation (Stripe success redirect target). Fires `Purchase` (value 25 USD). |
| `shipping.html`, `returns.html`, `privacy.html`, `terms.html` | Policy pages with the FTC Mail Order Rule language (16 CFR 435) and the non-affiliation / first-sale wording from scope-report.md section 4. |
| `css/style.css`, `css/fonts.css`, `fonts/` | Spindle tokens from `brand/tokens.json` (Vinyl, Soot, Plaster, Label, Halo, Ember, Chrome, Brass; halo is the single accent and appears as light). Inter Tight + Instrument Serif italic + JetBrains Mono, latin subsets, self-hosted (no third-party font request). Layout was first verified against the Oura DESIGN.md lane, then re-tokened when the brand landed. |
| `js/config.js` | **Every placeholder and the brand constant.** See below. |
| `js/main.js` | Brand substitution, pixel wrapper, hero dimmer, swatch image swap, SKU picker, sticky bar, waitlist form, thanks-page events, reveal-on-scroll with a safety timer. |
| `img/` | WebP + JPEG at two widths each, 2.0 MB total for 50 files. Heroes and squares now come from `renders-final/png`; exploded, cutaway, rear and the cap tiles still come from `render/`. |
| `_gen/build.py`, `_gen/pages.py` | Optional generator that stamps the shared header and footer into each page. The HTML files are hand-editable; rerun only if you want to change the shell everywhere at once. Fails on any em-dash. |
| `_gen/import-finals.sh` | Re-crops and compresses whatever exists in `../renders-final/png` into `img/`. Safe to rerun as more finals land. |
| `screenshots/` | Full-page desktop (1440) and mobile (390, 2x) captures of all twelve pages, plus hero off/on states. |
| `RESEARCH.md` | The CRO teardown (Gantri, Schoolhouse, Teenage Engineering, Rejuvenation, Ember, Our Place, Tom Dixon, Poplight and others, Baymard, FTC), 145 cited URLs, and the patterns applied. |

## Placeholders that must be filled before launch (all in `js/config.js`)

| Constant | Now | Set it to |
|---|---|---|
| `BRAND` | `Spindle` | Decided 2026-11-09 (brand/naming-report.md: Side A conflicts with a live SIDE A mark for vinyl sleeves). Brand = product, Poplight pattern: Spindle 12, Spindle 7, Spindle Kit, Spindle Set. If it ever changes again: edit the constant (updates every `data-brand` span and the title), then `BRAND` in `_gen/build.py` and rebuild for the static meta tags. Lockups for Deadwax and Side A already exist in `brand/logo/`. |
| `DOMAIN` | `https://example.com` | Live domain. Also replace in the `<link rel="canonical">`, `og:url`, `og:image` and JSON-LD of every page: `sed -i '' 's#https://example.com#https://yourdomain.com#g' *.html`. |
| `STRIPE_PAYMENT_LINK` | placeholder | The $25 "Spindle batch two deposit (refundable)" Payment Link. In Stripe: collect shipping address, add custom fields for model, finish and decade/title preference, and set the success URL to `https://<domain>/thanks-deposit.html?session_id={CHECKOUT_SESSION_ID}`. The site appends `client_reference_id=<sku>-<finish>` so the dashboard shows what each depositor picked. Until set, deposit buttons go to `thanks-deposit.html?demo=1` so the funnel can be tested end to end. |
| `WAITLIST_FORM_ACTION` | placeholder | Formspree / Tally / Mailchimp POST endpoint. The form sends `email`, `finish`, `consent`, a honeypot `_gotcha`, and `_next` = thanks.html. Until set, submit redirects locally to `thanks.html?demo=1`. |
| `META_PIXEL_ID` | placeholder | Pixel id. Until set, every event is logged to the console as `[pixel placeholder]` instead of loaded. Events wired: `PageView` (all), `ViewContent` (product page + SKU change), `InitiateCheckout` (deposit click), `Lead` (waitlist submit + thanks.html), `Purchase` value 25 USD (thanks-deposit.html). Verify Lead and Purchase in Events Manager before the ad goes live. |
| `SHIP_WINDOW` | `the week of [SHIP DATE]` | A real week with a two-week buffer. It appears in the footer of every page, the FAQ, the reserve block, shipping.html and the deposit thank-you. Required by the FTC rule; do not launch with the bracket in place. |
| `FIRST_BATCH_SOLD_OUT_DATE` | `''` | e.g. `'November 2026'`. Shown as "sold out in November 2026" when set; hidden when empty. |
| `CONTACT_EMAIL` | `hello@example.com` | Real address. |
| `BATCH_TWO_CAP` | `100` | Keep it real. Deposit 101 must actually go to a batch-three list (Stripe Payment Links can cap quantity: set the link's inventory to 100). |

Logo files are site-local copies of `brand/logo/` (favicon = icon-512, header mark = monogram with its background rect stripped, footer = horizontal lockup). `brand/` itself was not edited. Taglines in use: "Change the record. Change the room." (hero H1 and footer), "Twelve inches of what you love, lit at 2700 K." (product subhead), "Your record. Our light." (Kit eyebrow), "Put something on." (deposit thank-you), "Change the record. Change the room." (footer sign-off, per the guide).

## Truth rules baked in

- "First batch of 20 sold out" is the only scarcity claim, and it is true (Austin, 2026-11-09). No countdowns, no stock counters, no "almost gone".
- Deposit copy states refundable-any-time, the ship window, the delay-notice promise, and the hard cap, in the hero, the reserve block, the thank-you and the footer (FTC 16 CFR 435; FTC dark-patterns report 2022).
- No band names, logos, album titles or cover art anywhere. Labels in the renders are fictional ("Halo Pressings"). Non-affiliation statement in every footer, about.html and terms.html. The named-title menu is deliberately not on the site; it goes out by email after an IP lawyer hour (scope-report.md section 4).
- No fake reviews or testimonials. The proof strip uses only verifiable numbers (20 of 20, 2700K, 12 V).

## Running it locally

```
cd projects/record-sconces/site
python3 -m http.server 8731
open http://127.0.0.1:8731/
```

## Deploying

GitHub Pages: push the `site/` contents to a `gh-pages` branch or a repo root with Pages enabled; no build. Vercel: `vercel --prod` from `site/` with framework "Other"; no build command, output directory `.`. Both serve the relative paths as is. Add the real domain to `DOMAIN` and run the sed above first, then redo the OG tags check with the Meta Sharing Debugger.

## QA done

- 24 full-page renders (12 pages x desktop 1440 / mobile 390 @2x) with headless Chromium: zero horizontal overflow, zero console errors, zero failed requests after self-hosting the fonts.
- Fixed during QA: grid children overflowing on mobile (`min-width: 0`), eyebrow labels wrapping into columns (was inline-flex), long deposit button clipping on mobile (block buttons now wrap), reveal animation given a 1.8 s safety net so no section can stay hidden if an observer never fires, desktop hero recomposed so the halo is never cropped.
- Not run: Lighthouse (no Chrome DevTools binary in the sandbox). Page weight by inspection: home is roughly 330 KB over the wire on mobile (one 640 px WebP hero, two fonts at 169 KB total, 20 KB CSS+JS). Everything below the fold is lazy.

## Open

- All three finish heroes and squares (`img/hero-*`, `img/sq-*`) now come from `renders-final/png`. The exploded, cutaway, rear and cap-detail images still come from `render/`. Rerun `_gen/import-finals.sh` as the macro, swap, flat-lay and room scenes land; it picks them up automatically, then wire them into product.html thumbs and the swap section.
- The 8-second halo loop video (`renders-final/video/`) was not there yet; a `<video>` in the hero is the natural upgrade, autoplay muted, plain file, no clever loading (Austin's pedal-card rule).
- Heat numbers on install.html are the engineering acceptance criterion, not a measurement. Replace with the IR readings from the first prototype soak.

## Audit pass, 2026-11-11 (full report: ../audits/AUDIT-website.md)

- **The generator owns the HTML.** Edit `_gen/pages.py` and `_gen/build.py`, then run `python3 _gen/build.py`. Do not hand-edit the `.html` files: a hand edit (the hero slogan) was nearly lost that way.
- **Prices live in one place**: the constants at the top of `_gen/pages.py` (`KIT_PRICE`, `SCONCE_PRICE`, ...). The build writes them into the pages, the meta descriptions, the JSON-LD and `js/config.js`. The Kit price (89 or 99) is still Austin's decision.
- **`SET_OPEN = False`** hides the Set from the picker and footer until the 7-inch single is engineered.
- **`python3 _gen/build.py --launch-check`** exits 1 while any placeholder a customer would see is still in place (ship date, Stripe link, waitlist endpoint, contact email, pixel id, domain). Do not deploy until it prints PASS.
- **Truth rules** are at the top of `_gen/pages.py`: nothing is built or measured yet; heat numbers are calculated; "UL listed" describes the plug-in adapter only. `cad/gates.py` greps the built pages, so keep "up to 6 W" on product.html and "sits on the back of the backplate, facing the wall" on faq.html.
- Thank-you pages: with placeholders they show a red TEST MODE banner; `thanks-deposit.html` without a Stripe `session_id` says no hold was found and does not fire the Purchase event. Set the Stripe link's success URL to `<DOMAIN>/thanks-deposit.html?session_id={CHECKOUT_SESSION_ID}`.
- New pages: `warranty.html`, `404.html`. 14 pages now. The "QA done" and "Truth rules" sections above describe the site before this pass.
- Images no longer used because they show the old design: `exploded-*`, `rear-*`. Never used and wrong: `swap*`, `flatlay*` (phantom post), `set-*`, `studio-*` (7-inch). `layout-*` is cropped from `renders-exploded/spindle-heat-safe-layout.png`.
- **`FINISHES_OPEN = False`** sells chrome only (brass and black caps are not real parts). **`NO_SHIP_PLACES`** names where we do not ship until the fixture is listed. No colour temperature number is quoted until the strip is chosen. Vinyl softening is stated as roughly 120 F (product audit), not 130 to 140 F.
