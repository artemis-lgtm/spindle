/* ------------------------------------------------------------------
   SITE CONFIG. Everything that may change lives here.
   Brand name is ONE constant: change BRAND and every page follows.
   (Static <title>/og tags also carry the brand; README has the one-line sed.)
   ------------------------------------------------------------------ */
window.SITE = {
  BRAND: 'Spindle',                // decided 2026-11-09 (brand/naming-report.md). Brand = product, like Poplight.
  PRODUCT: 'Spindle 12',           // the 12-inch sconce
  KIT: 'Spindle Kit',              // light-only SKU, customer's own record
  SET: 'Spindle Set',              // 12" + two 7"
  DOMAIN: 'https://example.com',   // PLACEHOLDER: set to the live domain for OG tags

  // The first 20 are pre-sold to people Austin knows (2026-11-09). The site says "spoken for", never "sold out"
  // (audits/AUDIT-marketing.md: "sold out" waits until 20 units are delivered). No countdowns, no fake scarcity.
  FIRST_BATCH_SIZE: 20,
  FIRST_BATCH_SOLD: 20,
  BATCH_TWO_CAP: 100,              // hard cap; deposit 101 goes to batch three list
  SHIP_WINDOW: 'the week of [SHIP DATE]',  // PLACEHOLDER: a real date with a 2-week buffer (FTC 16 CFR 435)

  // Deposit + waitlist plumbing (all placeholders until Austin creates them)
  DEPOSIT_AMOUNT: 25,
  STRIPE_PAYMENT_LINK: 'https://buy.stripe.com/REPLACE_WITH_PAYMENT_LINK',
  // Stripe Payment Link should redirect on success to: <DOMAIN>/thanks-deposit.html?session_id={CHECKOUT_SESSION_ID}
  // Waitlist endpoint. JSON POST. On Vercel set it to '/api/waitlist' (site/api/waitlist.js, writes a Google Sheet,
  // needs the SPINDLE_* env vars listed in that file). Any JSON endpoint works too (e.g. https://formspree.io/f/xxxx).
  // Placeholder = demo mode: nothing is sent, thanks.html shows TEST MODE.
  WAITLIST_FORM_ACTION: 'REPLACE_WITH_FORM_ENDPOINT',
  // Meta pixel id for SPINDLE'S OWN pixel. Never reuse Ghost Audio's pixel or ad account.
  // Placeholder = no Meta script loads; every event is still logged to window.SpindlePixel.log and the console.
  META_PIXEL_ID: 'REPLACE_WITH_PIXEL_ID',
  CONTACT_EMAIL: 'hello@example.com',                  // PLACEHOLDER

  // Label the live 3D model wears before the visitor types one. '' = the plain house label (drawn in the browser).
  // 'img/label-zep4.jpg' = Austin's 2026-11-12 pick, a photo of a real pressing: a trademark/copyright question,
  // so it is OFF on the public site until he decides. AUSTIN'S CALL.
  LABEL_REF: '',

  // Price ladder. DO NOT EDIT THE NUMBERS HERE: they are written by _gen/build.py from _gen/pages.py
  // (KIT_PRICE etc. at the top of that file). Edit there, then run python3 _gen/build.py.
  FINISHES_OPEN: false,            // generated. false = chrome only (brass and black caps are not real parts yet)
  SET_OPEN: false,                 // generated. false = the Set cannot be reserved (7-inch single is not engineered yet)
  SKUS: {
    kit:    { name: 'Spindle Kit',          price: 99,  tag: 'Your record',        blurb: 'The light, the mount and the cap. You supply the record.' },
    sconce: { name: 'Spindle 12',          price: 129, tag: 'With a vintage LP',  blurb: 'Same kit plus a genuine used LP from the decade you pick. Our choice of title.' },
    named:  { name: 'Spindle 12, Named',   price: 179, tag: 'You name the album', blurb: 'Same kit plus an original pressing of a title from our menu of ten classics.' },
    set:    { name: 'Spindle Set',              price: 249, priceWithRecords: 329, tag: '12" + two 7"', blurb: 'One 12" Spindle and two 7" singles.' }
  },
  FINISHES: {
    chrome: { name: 'Chrome', hex: '#d9dbdd' },
    brass:  { name: 'Brass',  hex: '#c9a35a' },
    black:  { name: 'Black',  hex: '#1a1a1a' }
  }
};
