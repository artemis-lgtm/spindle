# Page bodies for build.py. Plain HTML strings. No em-dashes. No band names, logos or album titles.
#
# TRUTH RULES (audit 2026-11-11, audits/AUDIT-website.md):
#   * Nothing has been physically built or measured yet. Never write as if units exist, shipped, or were tested.
#   * Heat numbers are a CALCULATION (cad/THERMAL.md). Always say so. No "will not warp", no "safe for any record".
#   * "UL listed" describes ONLY the plug-in power adapter. The Spindle as a whole is not UL listed.
#   * cad/gates.py greps these pages: product.html must contain "up to 6 W"; faq.html must contain
#     "sits on the back of the backplate, facing the wall"; no page may say the light is on the rim.

# ------------------------------------------------------------------ PRICES AND SWITCHES (one place)
KIT_PRICE = 89            # DECISION OWED (Austin). build/cost-model.md (2026-11-11, parts $78.04 at 100 units):
                          #   the $89 Kit LOSES $19.90 an order before ads, $99 loses about $10, and the Kit
                          #   needs about $125 to clear $15. (Older figures, $47.46 parts and "$89 clears $16",
                          #   are superseded.) The $129 Sconce clears $12.77 and the $179 Named $33.32.
                          # Change this ONE number and run build.py; every page, the JSON-LD, the meta
                          # descriptions and js/config.js follow.
SCONCE_PRICE = 129        # Kit plus a vintage LP, our pick
NAMED_PRICE = 179         # Kit plus a title from the menu (menu is NOT published; needs the IP lawyer hour first)
SET_PRICE = 249           # 12-inch + two 7-inch, customer's records
SET_RECORDS_PRICE = 329   # same, with our records
DEPOSIT = 25
SET_OPEN = False          # The 7-inch single is NOT on the heat-safe layout (cad/FIXES-heat-layout.md: no room
                          # for the ring) and its cap is unquoted. While False the Set cannot be reserved and is
                          # shown as "later". Flip to True only when the 7-inch is engineered.
FINISHES_OPEN = False     # audits/AUDIT-product.md: only the chrome cap is a specified part (RS-CAP-12 rev D).
                          # Brass and black have no real part or quote. While False the site sells chrome only,
                          # hides the finish picker and uses no brass/black render.
NO_SHIP_PLACES = "the City of Los Angeles or North Carolina"   # ops/safety.md audit section: local rules there
                          # require the whole light to be listed. Empty string once the fixture is listed.
SHIPPING_LINE = "Free shipping in the lower 48"   # ops/policies/shipping.md: contiguous US included; AK/HI pay the difference

def usd(n):
    return f"${n}"

def pic(name, widths, alt, sizes="100vw", cls="", loading="lazy", ext="jpg", ratio=None):
    """Static picture with webp + jpg fallbacks. name like 'living', widths like (900,1600). ratio = height/width."""
    ws = sorted(widths)
    webp = ", ".join(f"img/{name}-{w}.webp {w}w" for w in ws)
    jpg = ", ".join(f"img/{name}-{w}.{ext} {w}w" for w in ws)
    if ratio is None:
        ratio = 1 if "sq" in name else 9 / 16
    return (f'<picture class="{cls}"><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="img/{name}-{ws[-1]}.{ext}" srcset="{jpg}" sizes="{sizes}" alt="{alt}" loading="{loading}" decoding="async" width="{ws[-1]}" height="{round(ws[-1]*ratio)}"></picture>')

def fpic(prefix, widths, alt, sizes="100vw", loading="lazy", finish="chrome"):
    """Finish-swappable picture. prefix like 'sq' or 'hero'. main.js swaps {finish}."""
    ws = sorted(widths)
    tw = ", ".join(f"img/{prefix}-{{finish}}-{w}.webp {w}w" for w in ws)
    tj = ", ".join(f"img/{prefix}-{{finish}}-{w}.jpg {w}w" for w in ws)
    h = ws[-1] if prefix == "sq" else round(ws[-1] * 1080 / 1200)
    return (f'<picture data-src-tpl="img/{prefix}-{{finish}}-{ws[-1]}.jpg">'
            f'<source type="image/webp" data-srcset-tpl="{tw}" srcset="{tw.replace("{finish}", finish)}" sizes="{sizes}">'
            f'<img src="img/{prefix}-{finish}-{ws[-1]}.jpg" data-srcset-tpl="{tj}" srcset="{tj.replace("{finish}", finish)}" sizes="{sizes}" alt="{alt}" loading="{loading}" decoding="async" width="{ws[-1]}" height="{h}"></picture>')

_SWATCHES_ON = """<div class="swatches" role="group" aria-label="Finish">
  <div data-swatch-group="{target}" style="display:flex;gap:12px">
    <button class="swatch" type="button" data-finish="chrome" aria-pressed="true" aria-label="Chrome"><span></span></button>
    <button class="swatch" type="button" data-finish="brass" aria-pressed="false" aria-label="Brass"><span></span></button>
    <button class="swatch" type="button" data-finish="black" aria-pressed="false" aria-label="Black"><span></span></button>
  </div>
  <span class="swatch-name">Chrome</span>
</div>"""

class _Off:
    def format(self, **k): return ""
SWATCHES = _SWATCHES_ON if FINISHES_OPEN else _Off()
FINISH_PHRASE = "in your finish" if FINISHES_OPEN else "in mirror chrome"

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'

TRUST = f"""<div class="trust">
  <div>{CHECK}<span>Nothing glued, drilled or stuck to your record.</span></div>
  <div>{CHECK}<span>Swap the record any time. One cap, a few turns, no tools.</span></div>
  <div>{CHECK}<span>Low voltage (12 V). Plugs into a normal outlet.</span></div>
  <div>{CHECK}<span><span data-deposit>$25</span> hold, refundable any time before it ships.</span></div>
</div>"""

# Shown next to every reserve button. Plain words, no promise we cannot keep.
STATUS_NOTE = """<div class="status-note">
  <b>Where this stands today.</b> Spindle is designed and engineered, and the first units have not been built yet. Nothing ships until our heat test on real units passes. That is why today is a refundable <span data-deposit>$25</span> hold and not a purchase.
</div>"""

GUARANTEE = f"""<ul class="assure">
  <li>{CHECK}<span><b>Refundable hold.</b> Your <span data-deposit>$25</span> comes back any time before it ships, for any reason.</span></li>
  <li>{CHECK}<span><b>30-day returns</b> once it arrives. <a href="returns.html">How returns work</a></span></li>
  <li>{CHECK}<span><b>2-year limited warranty</b> on the light. <a href="warranty.html">Read it</a></span></li>
  <li>{CHECK}<span><b>{SHIPPING_LINE}.</b> <a href="shipping.html">Shipping and ship date</a></span></li>
</ul>"""

FAQ_ITEMS = [
 ("Is this a finished product I can buy today?",
  "<p>Not yet, and we would rather say so. The design and engineering are done. The first units have not been built or tested yet. Today you can place a refundable <span data-deposit>$25</span> hold. You pay the rest only when your sconce is built, tested and ready to ship, and you can take your <span data-deposit>$25</span> back at any point before then.</p>"),
 ("Will the light heat up or warp my record?",
  "<p>It is designed not to, and we will test it on real units before anything ships. The LED strip sits on the back of the backplate, facing the wall, so it shines away from your record. It is stuck to a thin aluminium ring that spreads its warmth, with a layer of cork and half an inch of wood between it and the record. The whole light uses about 4 watts, about what a small night light bulb uses.</p><p>Our heat calculation puts the record about 6 F warmer than the room (92 F in an 86 F room). Record vinyl starts to lose its stiffness at roughly 120 F. Our figure is a calculation, not a measurement, and a calculation can be wrong, which is why we test. Before the first unit ships we run the light for two hours with temperature probes on the record, and it only passes if the record stays within 9 F of the room. We will post the measured numbers here.</p><p>What can hurt a record is the room: do not hang any record above a radiator or heater, or where direct sun hits it.</p>"),
 ("What touches my record?",
  "<p>Felt and one clear washer. The record rests on soft felt pads on the backplate. A thin clear washer lies on the label so the cap never rubs the paper, and the cap has its own felt underneath. The cap's screw goes through the centre hole, the same hole a turntable uses, into a brass thread in the backplate. Nothing is glued, taped or drilled, so you can take the record down and play it.</p>"),
 ("Can I change the record?",
  "<p>Yes, that is the point. Unscrew the dome cap by hand, lift the record off, set the next one on, screw the cap back. No tools, and the light stays on the wall.</p>"),
 ("How does it get power? Do I need an electrician?",
  "<p>The standard setup needs no electrician. A 12-volt power adapter plugs into a normal outlet and a thin cord runs to the sconce. You can let the cord show, cover it with a paintable cord cover, or hide a low-voltage cable inside the wall with our optional kit.</p><p>Only the thin low-voltage cable may go inside a wall. The adapter and its cord always stay out in the open at the outlet. This is Class 2 low-voltage wiring. Rules for it vary, so check your local code or ask an electrician before you cut into a wall. Spindle is a plug-in light and is not made to be hardwired to house wiring.</p>"),
 ("Is it UL listed?",
  "<p>The Spindle itself is not UL listed. The plug-in power adapter we ship is a UL-listed Class 2 adapter, and it is the only part connected to house power. Everything we make (the wooden backplate, the mount and the cap) carries 12 volts or nothing at all. We check the adapter's UL file number before we ship any unit. If your building or landlord requires the whole light fixture to be listed, this is not the right product for that wall yet. " + (f"For the same reason we do not ship to {NO_SHIP_PLACES} for now." if NO_SHIP_PLACES else "") + "</p>"),
 ("I rent. Can I still hang it?",
  "<p>Yes. The standard setup is two screws in the wall, like a heavy picture frame, and a cord down to the outlet. Hiding the cable inside the wall means cutting two small holes, which you would need to patch when you leave, so check your lease first.</p>"),
 ("How bright is it? Can I dim it?",
  "<p>It is a mood light, not a reading light. The light is warm white, about the colour of an old filament bulb, and it glows on the wall around the record. A dimmer on the cord takes it from full glow down to faint. There is no colour changing and no remote, on purpose.</p>"),
 ("Which records work?",
  "<p>Any standard 12-inch LP, including coloured vinyl and picture discs. A badly warped record will not sit flat. 7-inch singles do not fit the Spindle 12; a 7-inch version is planned for later.</p>"),
 (f"What record comes with the {usd(SCONCE_PRICE)} Spindle 12?",
  f"<p>A real, used LP from the decade you choose (60s, 70s or 80s). We pick the title, clean it and check it for looks. These are old records chosen for display, so expect some wear, and we do not promise they play well. If you want a specific album, the {usd(NAMED_PRICE)} Named option lets you choose from a short menu, which we email you before you pay your balance. We never show cover art or logos and we are not affiliated with any artist or label.</p>"),
 ("When does it ship?",
  "<p>Batch two is planned to ship <span data-ship>the week of [SHIP DATE]</span>. That is our honest estimate, not a guarantee, because the units are not built yet. If we will miss it, we email you before that date with a new one, and you choose: keep your place or take a full refund. The first batch of <span data-batch-size>20</span> ships before batch two. Batch two is capped at <span data-batch-two-cap>100</span>.</p>"),
 ("Is the $25 really refundable? When do I pay the rest?",
  "<p>Yes. Any time before your sconce ships, for any reason, email us and the <span data-deposit>$25</span> goes back to your card within 5 business days. When your sconce is ready we email you a link to pay the rest (the price minus your <span data-deposit>$25</span>). Nothing is charged automatically.</p>"),
 ("Shipping, returns and warranty?",
  f"<p>{SHIPPING_LINE} states. You have 30 days from delivery to return it for a refund, less a flat $12 for the return label unless it arrived damaged or faulty. The light is covered by a two-year limited warranty; the record is not. Details on the <a href='shipping.html'>shipping</a>, <a href='returns.html'>returns</a> and <a href='warranty.html'>warranty</a> pages.</p>"),
]

def faq_html(items):
    return "<div class=\"faq\">" + "".join(f"<details><summary>{q}</summary><div class=\"a\">{a}</div></details>" for q, a in items) + "</div>"

def faq_pick(*starts):
    """Pick FAQ items by the start of the question, so reordering the list never shows the wrong ones."""
    out = []
    for s in starts:
        m = [it for it in FAQ_ITEMS if it[0].startswith(s)]
        if len(m) != 1:
            raise SystemExit(f"faq_pick: {s!r} matched {len(m)} questions")
        out.append(m[0])
    return out

import json as _json, re as _re
FAQ_JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
""" + ",\n".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (
        _json.dumps(q), _json.dumps(_re.sub("<[^>]+>", "", a.replace("</p><p>", " "))))
    for q, a in FAQ_ITEMS) + """
]}
</script>
"""

_offers = [
 ("Spindle Kit", KIT_PRICE, "product.html#kit"),
 ("Spindle 12", SCONCE_PRICE, "product.html"),
 ("Spindle 12, Named", NAMED_PRICE, "product.html#named"),
] + ([("Spindle Set", SET_PRICE, "product.html#set")] if SET_OPEN else [])
PRODUCT_JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product","name":"Spindle 12","brand":{"@type":"Brand","name":"Spindle"},
"description":"A wall light that holds a real 12-inch vinyl record and glows warm on the wall behind it. Low-voltage plug-in, mirror-chrome dome cap. Nothing glued to the record. Pre-order: not yet shipping.",
"image":["https://example.com/img/sq-chrome-1080.jpg"],
"offers":[
""" + ",\n".join(
    ' {"@type":"Offer","name":"%s","price":"%d","priceCurrency":"USD","availability":"https://schema.org/PreOrder","url":"https://example.com/%s"}' % o
    for o in _offers) + """
]}
</script>
"""

RESERVE_BLOCK = f"""
<section class="section" id="reserve">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Batch two</p>
    <h2>First batch of <span data-batch-size>20</span> sold out<span data-sold-date></span>. Batch two is open.</h2>
    <p class="lede">Two ways in. A refundable <span data-deposit>$25</span> hold saves you a unit. The free list just gets an email when the next batch opens.</p>
    <div class="reserve-grid" style="margin-top:32px">
      <div class="offer primary">
        <span class="pill">Saves your unit</span>
        <h3>Hold one for <span data-deposit>$25</span>, refundable</h3>
        <div class="price"><span data-deposit>$25</span> <span class="muted" style="font-size:1rem;font-family:var(--font-body)">today, taken off your price</span></div>
        <ul>
          <li><b>Refundable.</b> Any time before it ships, for any reason. Back on your card within 5 business days.</li>
          <li><b>Not built yet.</b> The first units get built and heat-tested first. Nothing ships until that test passes.</li>
          <li><b>Planned to ship <span data-ship>the week of [SHIP DATE]</span>.</b> An estimate, not a guarantee. If we will miss it, we email you first and you can keep your place or take a full refund.</li>
          <li><b>You pay the rest later.</b> When yours is ready we email you a link. Nothing is charged automatically.</li>
          <li>Capped at <span data-batch-two-cap>100</span> units. You have <b data-sku-name>Spindle 12</b> selected. <a href="reserve.html" class="u">Change it</a></li>
        </ul>
        <a class="btn btn-primary btn-block" data-deposit-link href="reserve.html"><span>Hold mine for <span data-deposit>$25</span>, refundable</span></a>
        <p class="form-note">Secure card checkout by Stripe. We ask for your shipping address before we ship, not today.</p>
      </div>
      <div class="offer">
        <span class="pill">Free</span>
        <h3>Join the waitlist</h3>
        <p class="muted small">One email when batch two is ready to order, one when batch three opens. Nothing else.</p>
        <form id="waitlist-form" action="#" method="get" novalidate>
          <input type="hidden" name="_next" value="thanks.html">
          <input type="hidden" name="_subject" value="Spindle waitlist signup">
          <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="field"><label for="wl-email">Email</label><input id="wl-email" type="email" name="email" required autocomplete="email" inputmode="email" placeholder="you@example.com"><span class="field-err" id="wl-err" role="alert" hidden>Please enter a valid email and tick the box below.</span></div>
          <div class="field"><label for="wl-finish">Which one are you leaning toward?</label>
            <select id="wl-finish" name="version"><option value="kit">Kit, my own record</option><option value="sconce">With a vintage LP</option><option value="named">I want to name the album</option><option value="undecided">Not sure yet</option></select></div>
          <label class="consent"><input type="checkbox" name="consent" required><span>Email me about batch two and three. Unsubscribe any time. See the <a href="privacy.html" class="u">privacy policy</a>.</span></label>
          <button class="btn btn-ghost btn-block" type="submit">Join the free waitlist</button>
        </form>
      </div>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ HOME
CAPS_BLOCK = ("""      <div class="swap reveal" style="grid-template-columns:repeat(3,1fr)">
        <figure><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-chrome.webp"><img src="img/cap-chrome.jpg" alt="Rendering of the chrome dome cap on a record label" loading="lazy" decoding="async" width="500" height="500"></picture></div><figcaption>Chrome</figcaption></figure>
        <figure><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-brass.webp"><img src="img/cap-brass.jpg" alt="Rendering of the brass dome cap on a record label" loading="lazy" decoding="async" width="500" height="500"></picture></div><figcaption>Brass</figcaption></figure>
        <figure><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-black.webp"><img src="img/cap-black.jpg" alt="Rendering of the gloss black dome cap on a record label" loading="lazy" decoding="async" width="500" height="500"></picture></div><figcaption>Black</figcaption></figure>
      </div>
    </div>
  </div>
</section>

""" if FINISHES_OPEN else """      <div class="reveal"><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-chrome.webp"><img src="img/cap-chrome.jpg" alt="Rendering of the chrome dome cap on a record label" loading="lazy" decoding="async" width="500" height="500" style="width:100%"></picture></div></div>
    </div>
  </div>
</section>

""")

FINISH_SECTION = (f"""<section class="section" id="finishes">
  <div class="wrap two">
    <div class="frame dark finish-img reveal">{fpic("sq", (640, 1080), "Rendering of the Spindle, close on the record and dome cap, in the selected finish", sizes="(min-width: 900px) 50vw, 100vw")}</div>
    <div class="reveal">
      <p class="eyebrow"><span class="dot"></span>Three finishes, one price</p>
      <h2>Chrome. Brass. Black.</h2>
      <p class="muted">Chrome is the lead: a mirror against matte vinyl. Brass reads warmer in a room full of wood. Black disappears and lets the glow do the talking. Tap a finish to see it.</p>
      <div style="margin:22px 0 28px">{SWATCHES.format(target="#finishes picture")}</div>
      <a class="btn btn-primary" href="product.html">Choose yours</a>
    </div>
  </div>
</section>""" if FINISHES_OPEN else f"""<section class="section" id="finishes">
  <div class="wrap two">
    <div class="frame dark reveal">{pic("macro", (640, 1080), "Close rendering of the mirror-chrome dome cap sitting on a record label", sizes="(min-width: 900px) 50vw, 100vw", ratio=1)}</div>
    <div class="reveal">
      <p class="eyebrow"><span class="dot"></span>The cap</p>
      <h2>One mirror at the centre.</h2>
      <p class="muted">The dome is solid brass, polished and chrome plated: a small mirror against matte vinyl. It is the only part you touch, so it is the part we spend the money on.</p>
      <p class="muted small">Chrome is the only finish for now. Brass and black are ideas we like and have not engineered yet, so we are not selling them.</p>
      <a class="btn btn-primary" href="product.html" style="margin-top:12px">See Spindle 12</a>
    </div>
  </div>
</section>""")

HOME = f"""
<section class="hero" id="top" aria-label="The Spindle in a dark room">
  <div class="hero-media">
    <picture>
      <source type="image/webp" srcset="img/sq-chrome-640.webp 640w, img/sq-chrome-1080.webp 1080w" sizes="(min-width: 900px) 66vw, 100vw">
      <img src="img/sq-chrome-1080.jpg" srcset="img/sq-chrome-640.jpg 640w, img/sq-chrome-1080.jpg 1080w" sizes="(min-width: 900px) 66vw, 100vw" alt="A black 12-inch record mounted flat on a wall with a mirror-chrome dome at its centre and a warm amber glow on the wall behind it. Computer rendering of the design." fetchpriority="high" decoding="async" width="1080" height="1080">
    </picture>
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="hero-vignette" aria-hidden="true"></div>
  </div>
  <div class="wrap hero-content">
    <div>
      <p class="eyebrow"><span class="dot"></span>First batch of <span data-batch-size>20</span> sold out</p>
      <h1>Change the record.<br>Change the room.</h1>
      <p class="tagline slogan">YOUR favorite records light up <em>YOUR favorite room</em></p>
      <p class="hero-price">A wall light that holds a real record. From <b>{usd(KIT_PRICE)}</b> with your own record, <b>{usd(SCONCE_PRICE)}</b> with a vintage LP.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="reserve.html"><span>Hold mine for <span data-deposit>$25</span>, refundable</span></a>
        <a class="btn btn-ghost" href="product.html">See Spindle 12</a>
      </div>
      <p class="hero-fine">Pre-order. Not built yet: pay <span data-deposit>$25</span> now, the rest when yours is ready. {SHIPPING_LINE}.</p>
    </div>
    <div>
      <div class="dimmer"><label for="dimmer">Dimmer</label><input id="dimmer" type="range" min="0" max="100" value="100" aria-label="Hero light dimmer"></div>
    </div>
  </div>
</section>

<section class="section tight"><div class="wrap">{TRUST}</div></section>

<section class="section" id="story">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Your record. Our light.</p>
    <h2 style="max-width:16em">Twelve inches of what you love, lit from behind.</h2>
    <div class="story-grid reveal" style="margin-top:40px">
      <div class="beat"><h3>Light behind it, not on it</h3><p>A ring of warm LEDs hides behind the record and shines at the wall, not at your vinyl. The record sits about an inch and a half off the wall in its own amber glow.</p></div>
      <div class="beat"><h3>One piece of jewellery</h3><p>The only hardware you see is the dome at the centre: solid metal, polished to a mirror. It screws through the record's centre hole and holds it on with felt.</p></div>
      <div class="beat"><h3>Your record, every time</h3><p>Unscrew the dome, lift the record, set the next one down. No tools, and the light never leaves the wall. Bring your own record with the Kit, or let us send a vintage LP from the decade you pick.</p></div>
    </div>
  </div>
</section>

<section class="section alt" id="room">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>In a room</p>
    <h2 style="max-width:14em">A foot wide. Two inches deep. One warm glow.</h2>
    <div class="frame dark reveal" style="margin-top:32px;max-width:980px">{pic("living", (900, 1600), "Rendering of the Spindle on a living room wall above a turntable and speakers, glowing warm around a black record", sizes="(min-width: 1000px) 980px, 100vw")}</div>
    <p class="caption">A computer rendering, not a photograph. The real glow may differ. Real photographs replace this once the first units are built. The record is 12 inches across and the cap sticks out about 2 inches from the wall.</p>
  </div>
</section>

{FINISH_SECTION}

<section class="section alt" id="how">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>How it works</p>
    <h2 style="max-width:14em">Four steps. The record is the last one.</h2>
    <div class="two" style="margin-top:32px">
      <div>
        <div class="frame diagram reveal">{pic("layout", (900, 1600), "Drawing of every part pulled apart in a line: wall plate, hub, the light strip on its aluminium and cork rings, the black backplate, the record, a clear washer, a felt washer and the chrome cap", sizes="(min-width: 900px) 50vw, 100vw", ratio=688/1600)}</div>
        <p class="caption">Drawn from the current design files. Left to right: wall plate (1), hub (2), power lead (3), light strip on its aluminium and cork rings (4 to 6), backplate (7), felt pads (8), your record (9), clear washer, felt washer and cap (10 to 12).</p>
      </div>
      <div class="steps reveal" style="grid-template-columns:1fr">
        <div class="step"><h3>Screw the plate to the wall</h3><p>A small steel plate goes up with two screws. You can level it after the screws are in.</p></div>
        <div class="step"><h3>Twist the light on</h3><p>The light pushes onto the plate and twists to lock. One small screw keeps it from ever twisting off.</p></div>
        <div class="step"><h3>Plug it in</h3><p>The power adapter plugs into a normal outlet. A dimmer on the cord sets the mood.</p></div>
        <div class="step"><h3>Your record, then the dome</h3><p>Set the record on the felt pads, screw the dome through the centre hole by hand. Done.</p></div>
      </div>
    </div>
    <p class="center" style="margin-top:32px"><a class="btn btn-ghost" href="install.html">See the install guide</a></p>
  </div>
</section>

<section class="section" id="swap">
  <div class="wrap">
    <div class="two rev">
      <div class="reveal">
        <p class="eyebrow"><span class="dot"></span>The sconce that takes requests</p>
        <h2>Put up what you are playing this month.</h2>
        <p class="muted">The dome is the only fastener. Unscrew it, lift the record, set the next one down, screw it back. A picture disc for a party. The pressing you found at the flea market. The album you have been meaning to frame for ten years.</p>
        <p class="muted">Nothing is glued, taped or drilled. Felt holds the record and a clear washer guards the label.</p>
      </div>
{CAPS_BLOCK}<section class="section alt" id="proof">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Straight answers</p>
    <h2 style="max-width:16em">What is true today, in plain numbers.</h2>
    <div class="proof reveal" style="margin-top:28px">
      <div class="card"><div class="num"><span data-batch-size>20</span> of <span data-batch-size>20</span></div><div class="label">First batch sold out<span data-sold-date></span> before this site went up. Those ship first. Batch two is capped at <span data-batch-two-cap>100</span>.</div></div>
      <div class="card"><div class="num">+6 F</div><div class="label">How much warmer than the room we calculate your record gets. Calculated, not yet measured. We test real units before any ship and post the results.</div></div>
      <div class="card"><div class="num">12 V</div><div class="label">Low voltage from a UL-listed plug-in adapter. The adapter is the listed part; the Spindle as a whole is not UL listed.</div></div>
    </div>
    <div style="margin-top:24px">{STATUS_NOTE}</div>
  </div>
</section>

<section class="section" id="faq-preview">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>The questions everyone asks</p>
    <h2>Heat, your record, wiring, refunds.</h2>
    <div style="margin-top:20px">{faq_html(faq_pick("Is this a finished", "Will the light heat", "What touches", "How does it get power", "Is the $25"))}</div>
    <p style="margin-top:24px"><a class="btn btn-ghost" href="faq.html">All the questions</a></p>
  </div>
</section>
{RESERVE_BLOCK}
"""

# ------------------------------------------------------------------ PRODUCT
def sku(id_, tag, name, blurb, price, checked=False):
    return f"""<label class="sku{' selected' if checked else ''}" id="{id_}">
      <input type="radio" name="sku" value="{id_}"{' checked' if checked else ''}>
      <span><span class="t">{tag}</span><br><span class="n">{name}</span><span class="b" style="display:block">{blurb}</span></span>
      <span class="pr">{price}</span>
    </label>"""

SET_SKU_LONG = sku("set", "12-inch + two 7-inch", "Spindle Set", f"One Spindle 12 and two 7-inch singles. {usd(SET_PRICE)} with your records, {usd(SET_RECORDS_PRICE)} with ours.", usd(SET_PRICE)) if SET_OPEN else ""
SET_SKU_SHORT = sku("set", "12-inch + two 7-inch", "Spindle Set", f"{usd(SET_PRICE)} with your records, {usd(SET_RECORDS_PRICE)} with ours.", usd(SET_PRICE)) if SET_OPEN else ""
SET_OPTS = f"""<div id="set-options" hidden style="margin-top:-6px;margin-bottom:12px">
        <label class="consent" style="margin:0"><input type="checkbox" id="set-records"><span>Include three records from us (total {usd(SET_RECORDS_PRICE)})</span></label>
      </div>""" if SET_OPEN else ""
SET_LATER = "" if SET_OPEN else '<p class="tiny" style="margin:-4px 0 12px">A three-piece Set with two 7-inch singles is planned for later. It is not open for holds yet. <a href="reserve.html#waitlist-form" class="u">Join the free list</a> to hear when it is.</p>'

def thumb(full, small, alt, pressed=False, finish=False):
    return (f'<button type="button" aria-pressed="{"true" if pressed else "false"}" data-full="{full}"{" data-finish-img" if finish else ""}>'
            f'<img src="{small}" alt="{alt}" loading="lazy" decoding="async" width="320" height="320"></button>')

PRODUCT = f"""
<section class="wrap pdp">
  <div class="gallery">
    <div class="main finish-img" id="pdp-main">{fpic("sq", (640, 1080), "Rendering of the Spindle in the selected finish, lit, on a warm plaster wall", sizes="(min-width: 900px) 50vw, 100vw", loading="eager")}</div>
    <div class="thumbs" role="group" aria-label="Gallery">
      {thumb("img/sq-{finish}-1080.webp", "img/sq-chrome-640.webp", "Lit, front view", True, True)}
      {thumb("img/cap-chrome.webp", "img/cap-chrome.webp", "Dome cap close up")}
      {thumb("img/living-sq-1080.webp", "img/living-sq-640.webp", "On a living room wall")}
      {thumb("img/macro-1080.webp", "img/macro-640.webp", "Chrome cap, very close")}
      {thumb("img/layout-1600.webp", "img/layout-900.webp", "Drawing of every part pulled apart").replace("<button ", "<button data-contain ")}
    </div>
    <p class="caption">Computer renderings of the design, not photographs. No unit has been built yet and the real glow may differ.</p>
  </div>
  <div class="buy">
    <p class="eyebrow"><span class="dot"></span>Pre-order. First batch of <span data-batch-size>20</span> sold out.</p>
    <h1 data-product>Spindle 12</h1>
    <p class="lede" style="font-size:1.35rem">A wall light that holds a real 12-inch record and glows warm behind it.</p>
    <div class="pricing"><span class="p" data-price>{usd(SCONCE_PRICE)}</span><span class="anchor"><span data-deposit>$25</span> today holds it. The rest when yours is ready. {SHIPPING_LINE}.</span></div>

    <div class="opt-row">
      <div class="lbl"><span>{"1. " if FINISHES_OPEN else ""}Pick your version</span></div>
      <div class="skus">
        {sku("kit", "Your record", "Spindle Kit", "The light, the mount and the cap. You put your own record on it.", usd(KIT_PRICE))}
        {sku("sconce", "With a vintage LP", "Spindle 12", "The Kit plus a real used LP from the decade you pick. We choose the title.", usd(SCONCE_PRICE), True)}
        {sku("named", "You name the album", "Spindle 12, Named", "The Kit plus an original pressing you choose from our short menu.", usd(NAMED_PRICE))}
        {SET_SKU_LONG}
      </div>
      {SET_OPTS}{SET_LATER}
    </div>

    {'<div class="opt-row"><div class="lbl"><span>2. Pick your finish: <b data-finish-name>Chrome</b></span><span class="tiny">Same price</span></div>' + SWATCHES.format(target="#pdp-main picture") + '</div>' if FINISHES_OPEN else '<p class="tiny" style="margin:0 0 14px">Finish: mirror chrome. It is the only finish for now.</p>'}

    <a class="btn btn-primary btn-block" data-deposit-link data-sticky-anchor href="reserve.html"><span>Hold my <span data-sku-name>Spindle 12</span> for <span data-deposit>$25</span>, refundable</span></a>
    <p class="form-note" style="text-align:center">Secure card checkout by Stripe. <a href="reserve.html#waitlist-form" class="u">Prefer the free waitlist?</a></p>

    <div class="sold-note">Planned to ship <span data-ship>the week of [SHIP DATE]</span>. That is an estimate: this batch is not built yet. If the date moves we email you first and you can take a full refund.</div>
    {GUARANTEE}
    {STATUS_NOTE}

    <div class="includes" style="margin-top:24px" data-includes="kit">
      <b>In the Kit box</b>
      <ul><li>The light: a black 10.5-inch backplate with the warm LED strip on its back</li><li>Dome cap {FINISH_PHRASE}, with its felt and a clear label washer</li><li>Wall plate, screws and wall anchors</li><li>UL-listed 12 V plug-in power adapter with a 6 ft cord, and a dimmer for the cord</li><li>A one-page hanging and safety sheet. You supply the 12-inch record.</li></ul>
    </div>
    <div class="includes" style="margin-top:24px" data-includes="sconce" hidden>
      <b>In the Spindle 12 box</b>
      <ul><li>Everything in the Kit</li><li>A real used 12-inch LP from the decade you choose (60s, 70s or 80s), cleaned, in its own sleeve</li><li>We pick the title. It is an old record chosen for looks, so expect some wear.</li></ul>
    </div>
    <div class="includes" style="margin-top:24px" data-includes="named" hidden>
      <b>In the Named box</b>
      <ul><li>Everything in the Kit</li><li>An original pressing of the album you pick from our short menu. We email the menu before you pay your balance.</li><li>Not affiliated with any artist or label.</li></ul>
    </div>
    {'<div class="includes" style="margin-top:24px" data-includes="set" hidden><b>In the Set box</b><ul><li>One Spindle 12 with everything in the Kit</li><li>Two 7-inch singles with their own plates and adapters</li><li>Optional: three records from us</li></ul></div>' if SET_OPEN else ''}

    <h2 class="spec-h">The details</h2>
    <table class="spec">
      <tr><th>Size</th><td>12 inches across with a record on. Sticks out about 2 inches from the wall (record face 1.6 in, cap tip 2.0 in).</td></tr>
      <tr><th>Record</th><td>Any standard 12-inch LP. Held between felt, with a clear washer over the label. Nothing glued.</td></tr>
      <tr><th>Light</th><td>Warm white LED strip on the back of the backplate, facing the wall. About 4 W, up to 6 W. Dimmer on the cord. The exact strip is not chosen yet, so we do not quote a colour number.</td></tr>
      <tr><th>Power</th><td>12 V DC from a UL-listed Class 2 plug-in adapter, 6 ft cord. Optional in-wall low-voltage cable kit. Not for hardwiring.</td></tr>
      <tr><th>Cap</th><td>Solid brass dome, about 1.5 inches across, with its own screw. Mirror chrome.</td></tr>
      <tr><th>Backplate</th><td>10.5 inch, 1/2 inch thick, matte black, 1 inch off the wall.</td></tr>
      <tr><th>Where</th><td>Indoors, dry walls only. Not above a heater or in direct sun.</td></tr>
      <tr><th>Weight</th><td>Roughly 2.5 lb with a record. Calculated from the design, not yet weighed.</td></tr>
      <tr><th>Testing</th><td>Record temperature is calculated at about 6 F above the room. Not yet measured; real units are tested before any ship. The Spindle as a whole is not UL listed.</td></tr>
      <tr><th>Built</th><td>To be assembled by hand in Fort Lauderdale, Florida.</td></tr>
    </table>
  </div>
</section>

<section class="section alt" style="margin-top:56px">
  <div class="wrap">
    <h2>Questions before you reserve</h2>
    <div style="margin-top:20px">{faq_html(faq_pick("Is this a finished", "Will the light heat", "What touches", "Is it UL", "What record comes", "When does it ship", "Is the $25"))}</div>
    <p style="margin-top:24px"><a class="btn btn-ghost" href="faq.html">All the questions</a></p>
  </div>
</section>
"""

STICKY = f"""<div class="sticky-bar">
  <div class="meta"><b data-sticky-name>Spindle 12</b><span data-sticky-price>{usd(SCONCE_PRICE)} when it ships. $25 refundable hold today.</span></div>
  <a class="btn btn-primary" data-deposit-link href="reserve.html"><span>Hold, <span data-deposit>$25</span></span></a>
</div>"""

# ------------------------------------------------------------------ INSTALL
INSTALL = f"""
<section class="section tight">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>How it works</p>
    <h1 style="max-width:11em">Two screws and a plug. The record stays yours.</h1>
    <p class="lede">Two ways to hang it. Cord showing takes two screws and about fifteen minutes. Cord hidden in the wall takes longer and two small holes. Times are our estimates from the design; we will update them once real units are hung.</p>
  </div>
</section>

<section class="section tight">
  <div class="wrap two">
    <div>
      <div class="frame diagram">{pic("layout", (900, 1600), "Drawing of every part pulled apart in a line: wall plate, hub, the light strip on its aluminium and cork rings, the black backplate, the record, a clear washer, a felt washer and the chrome cap", sizes="(min-width: 900px) 50vw, 100vw", loading="eager", ratio=688/1600)}</div>
      <p class="caption">Drawn from the current design files. Left to right: wall plate (1), hub (2), power lead (3), light strip on its aluminium and cork rings (4 to 6), backplate (7), felt pads (8), your record (9), clear washer, felt washer and cap (10 to 12).</p>
    </div>
    <div>
      <h2>How it holds on</h2>
      <p class="muted">A 4-inch steel plate screws to the wall with two screws, into a stud or into the wall anchors we include. You can turn the plate a little after the screws are in, so getting it level is easy.</p>
      <p class="muted">The light pushes onto three pins on the plate and twists to lock. One small screw at the bottom stops it from ever twisting off by accident.</p>
      <p class="muted">The record is held from the front by the dome cap, so changing a record never touches the mount.</p>
    </div>
  </div>
</section>

<section class="section alt" id="surface">
  <div class="wrap two rev">
    <div>
      <p class="eyebrow"><span class="dot"></span>Option A, the simple one</p>
      <h2>Cord showing. About 15 minutes, two screws.</h2>
      <p class="muted">The 6-foot cord plugs into a short lead tucked behind the light and runs down the wall to the outlet. Add a paintable cord cover from the hardware store if you want it neat, or let the cord be part of the look.</p>
      <p class="muted">Renters: this is two screw holes, like a heavy picture frame.</p>
      <div class="steps" style="margin-top:20px">
        <div class="step"><h3>Pick the spot</h3><p>The centre of the record usually looks right 58 to 62 inches from the floor. Make sure the cord reaches an outlet.</p></div>
        <div class="step"><h3>Plate up</h3><p>Hold the plate level, mark two holes, drive the screws, check level, tighten.</p></div>
        <div class="step"><h3>Twist the light on</h3><p>Plug the cord into the light's lead. Push the light onto the plate, twist until it stops, snug the small screw.</p></div>
        <div class="step"><h3>Record, dome, plug</h3><p>Record on the felt pads, dome through the centre hole by hand. Plug in and set the dimmer.</p></div>
      </div>
    </div>
    <div class="frame dark finish-img">{fpic("hero", (800, 1200), "Rendering of the Spindle lit on a warm wall", sizes="(min-width: 900px) 50vw, 100vw")}</div>
  </div>
</section>

<section class="section" id="in-wall">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Option B</p>
    <h2>Cord hidden in the wall. No cord on show.</h2>
    <div class="two" style="margin-top:28px">
      <div class="frame">{pic("cutaway", (900, 1600), "Drawing of a wall cut open: the sconce at eye level, a thin cable running inside the wall down to a small jack plate beside an outlet, and the power adapter plugged in at the outlet", sizes="(min-width: 900px) 50vw, 100vw")}</div>
      <div>
        <p class="muted">A thin low-voltage cable runs inside the wall from behind the light down to a small jack plate next to your outlet. The power adapter plugs in there, out in the open.</p>
        <p class="muted"><b>The one rule:</b> only the thin low-voltage cable goes in the wall. The power adapter and its cord never go inside a wall, ceiling or floor.</p>
        <p class="muted">This is Class 2 low-voltage wiring, and the cable must be rated for in-wall use (marked CL2 or better). Rules vary by town and by building, so check your local code. If you are not sure, or you are not comfortable cutting into a wall, ask an electrician.</p>
        <p class="muted small">You will cut a 1-inch hole behind the light and a small opening by the outlet, both in the same gap between wall studs, then feed the cable down. We estimate about 45 minutes with a stud finder and a drill.</p>
      </div>
    </div>
    <p class="tiny" style="margin-top:18px">The in-wall kit (rated cable, wall bracket, jack plate, pull string) will be offered as an add-on when you pay your balance. Its price is not set yet; you will see it before you pay.</p>
    <p class="tiny">Not for hardwiring. Spindle is a plug-in light. It is not a listed light fixture and should not be wired directly to house wiring or a wall switch.</p>
  </div>
</section>

<section class="section alt" id="heat">
  <div class="wrap">
    <h2>Heat, honestly</h2>
    <div class="two" style="align-items:start">
      <div>
        <p class="muted">Heat is the first thing a record owner asks about, so here is exactly what we know and what we do not.</p>
        <p class="muted"><b>How it is built.</b> The LED strip is on the back of the backplate, facing the wall. It shines away from the record and cannot shine on it. The strip is stuck to an aluminium ring that spreads its warmth, and a cork ring and half an inch of wood sit between that and your record. The light uses about 4 watts.</p>
        <p class="muted"><b>What we calculated.</b> In an 86 F room, the warmest spot on the record works out to about 92 F, roughly 6 F above the room. Record vinyl starts to lose its stiffness at roughly 120 F.</p>
        <p class="muted"><b>What we have not done yet.</b> That number is a calculation. No unit has been built or measured. Before any Spindle ships, we run real units for two hours with temperature probes on the record. A unit passes only if the record stays within 9 F of the room. We will post the measured numbers on this page.</p>
        <p class="muted small">The real risk to any record is the room. Do not hang a record above a radiator or heater, or where direct sun hits it.</p>
      </div>
      <div class="proof" style="grid-template-columns:1fr">
        <div class="card"><div class="num">about 4 W</div><div class="label">Power of the whole light. About what a small night light bulb uses.</div></div>
        <div class="card"><div class="num">+6 F</div><div class="label">Calculated record warmth above the room. Not yet measured.</div></div>
        <div class="card"><div class="num">about 120 F</div><div class="label">Where record vinyl starts to lose its stiffness.</div></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="safety">
  <div class="wrap legal">
    <h2 style="margin-top:0">Safety basics</h2>
    <ul>
      <li>Indoors, on a dry wall. Not in a bathroom, over a stove, on a porch or anywhere damp.</li>
      <li>Use only the power adapter that comes in the box.</li>
      <li>Keep the adapter in the open at the outlet. Do not cover it and never put it or its cord inside a wall.</li>
      <li>Not above a radiator, heater or fireplace, and not in direct sun.</li>
      <li>If anything flickers, buzzes or smells warm, unplug it and email us.</li>
    </ul>
  </div>
</section>
{RESERVE_BLOCK}
"""

# ------------------------------------------------------------------ FAQ
FAQ = f"""
<section class="section tight">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>FAQ</p>
    <h1>Everything people ask before they reserve.</h1>
    <p class="lede">Heat, your record, wiring, renters, refunds. If yours is not here, email <a data-email href="mailto:hello@example.com" class="u">hello@example.com</a>.</p>
    <div style="margin-top:28px">{faq_html(FAQ_ITEMS)}</div>
  </div>
</section>
{RESERVE_BLOCK}
"""

# ------------------------------------------------------------------ ABOUT
ABOUT = f"""
<section class="section tight">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>About</p>
    <h1 style="max-width:12em">Designed in Fort Lauderdale by people who could not find this anywhere.</h1>
    <div class="two" style="margin-top:32px">
      <div>
        <p class="muted">The idea was simple and we could not find it for sale: a wall light built around a real record that looks like a light fixture, not a craft project. What we found was battery-powered miniatures, records glued to wooden arms, and clear "now playing" shelves. Nobody was treating the record as the object and the light as the frame.</p>
        <p class="muted">So we designed one. Low-voltage power from a UL-listed plug-in adapter. A steel plate that is easy to level. Warm light that shines at the wall and not at the vinyl. And one piece of real metal at the centre, because the only thing you touch should feel like it cost something.</p>
        <p class="muted">The rule we will not break: nothing is ever glued, drilled or stuck to a record. Your record goes on the wall and comes off the wall exactly as it went on.</p>
        <p class="muted">Where we are: the first <span data-batch-size>20</span> were spoken for before this site went up. Those get built and tested first. Batch two is the first one open to everyone, capped at <span data-batch-two-cap>100</span> so every unit can be assembled and checked by hand.</p>
        <p class="muted small"><span data-brand>Spindle</span> is an independent company. We are not affiliated with, sponsored by or endorsed by any artist, band or record label. Records we include are real, previously owned pressings described factually; we never reproduce cover art or logos.</p>
      </div>
      <div class="frame dark finish-img">{fpic("sq", (640, 1080), "Rendering of the Spindle in the selected finish", sizes="(min-width: 900px) 50vw, 100vw")}</div>
    </div>
  </div>
</section>
{RESERVE_BLOCK}
"""

# ------------------------------------------------------------------ RESERVE
RESERVE = f"""
<section class="section tight">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Reserve</p>
    <h1 style="max-width:12em">Hold a Spindle from batch two.</h1>
    <p class="lede">Pick your version. Then hold it for a refundable <span data-deposit>$25</span>, or join the free list.</p>
    <div class="two" style="margin-top:28px;align-items:start">
      <div class="frame dark finish-img" id="reserve-img">{fpic("sq", (640, 1080), "Rendering of the Spindle in the selected finish", sizes="(min-width: 900px) 50vw, 100vw", loading="eager")}</div>
      <div>
        <div class="opt-row"><div class="lbl"><span>Pick your version</span></div>
          <div class="skus">
            {sku("kit", "Your record", "Spindle Kit", "You put your own record on it.", usd(KIT_PRICE))}
            {sku("sconce", "With a vintage LP", "Spindle 12", "A used LP from your decade, our pick.", usd(SCONCE_PRICE), True)}
            {sku("named", "You name the album", "Spindle 12, Named", "Choose from our short menu.", usd(NAMED_PRICE))}
            {SET_SKU_SHORT}
          </div>
          {SET_OPTS}
        </div>
        {'<div class="opt-row"><div class="lbl"><span>2. Pick your finish: <b data-finish-name>Chrome</b></span></div>' + SWATCHES.format(target="#reserve-img picture") + '</div>' if FINISHES_OPEN else ''}
        <p class="muted small">Price when it ships: <b data-price style="color:var(--ink)">{usd(SCONCE_PRICE)}</b>. {SHIPPING_LINE}. Today: <span data-deposit>$25</span>, refundable.</p>
        <a class="btn btn-primary btn-block" data-deposit-link data-sticky-anchor href="#reserve"><span>Hold my <span data-sku-name>Spindle 12</span> for <span data-deposit>$25</span>, refundable</span></a>
        {GUARANTEE}
      </div>
    </div>
  </div>
</section>
{RESERVE_BLOCK}
"""

# ------------------------------------------------------------------ THANKS
DEMO_BANNER = '<p class="demo-banner" data-demo-banner hidden>TEST MODE. Nothing was sent and no payment was taken. The checkout link and the waitlist form are not connected yet (js/config.js).</p>'

THANKS_LEAD = f"""
<section class="section thanks">
  <div class="wrap">
    {DEMO_BANNER}
    <div class="ring" aria-hidden="true"></div>
    <p class="eyebrow"><span class="dot"></span>You are on the list</p>
    <h1>We will write when batch two is ready.</h1>
    <p class="lede" style="margin:0 auto">One email when batch two is ready to order, one when batch three opens. If you would rather save a unit now, a refundable <span data-deposit>$25</span> holds one.</p>
    <div class="hero-ctas" style="justify-content:center;flex-direction:row;flex-wrap:wrap">
      <a class="btn btn-primary" href="reserve.html"><span>Hold one for <span data-deposit>$25</span></span></a>
      <a class="btn btn-ghost" href="index.html">Back to Spindle</a>
    </div>
  </div>
</section>
"""

THANKS_DEPOSIT = f"""
<section class="section thanks">
  <div class="wrap">
    {DEMO_BANNER}
    <div data-no-session hidden>
      <p class="eyebrow"><span class="dot"></span>Reserve</p>
      <h1>No hold found on this page.</h1>
      <p class="lede" style="margin:0 auto">This page appears after checkout. If you paid a deposit, your Stripe receipt email is your proof and your place is safe. If you have not, you can hold one below.</p>
      <p style="margin-top:28px"><a class="btn btn-primary" href="reserve.html"><span>Hold one for <span data-deposit>$25</span></span></a></p>
    </div>
    <div data-has-session>
    <div class="ring" aria-hidden="true"></div>
    <p class="eyebrow"><span class="dot"></span>Reserved</p>
    <h1>Your Spindle is held.</h1>
    <p class="lede" style="margin:0 auto">Thank you. Your <span data-deposit>$25</span> hold for <b data-thanks-selection>Spindle 12</b> is in, and a receipt from Stripe is on its way to your inbox.</p>
    <p class="tagline" style="margin-top:10px">Put something on.</p>
    <div class="offer" style="max-width:36em;margin:28px auto 0;text-align:left">
      <h3>What happens next</h3>
      <ul>
        <li>Your batch is not built yet. We build and heat-test the first units, then yours. It is planned to ship <span data-ship>the week of [SHIP DATE]</span>.</li>
        <li>If we will miss that date we email you before it with a new one, and you can keep your place or take a full refund.</li>
        <li>When yours is ready we email you a link to pay the rest. Nothing is charged automatically.</li>
        <li>Your <span data-deposit>$25</span> is refundable any time before shipping. Reply to the receipt email and it goes back to your card within 5 business days.</li>
        <li>Spindle 12: reply with your decade. Named: we email the album menu before you pay your balance.</li>
      </ul>
      <p class="tiny" style="margin:0">Need to change the version? Reply to the receipt email. Nothing is locked until we build it.</p>
    </div>
    <p style="margin-top:28px"><a class="btn btn-ghost" href="install.html">Read the install guide while you wait</a></p>
    </div>
  </div>
</section>
"""

NOT_FOUND = """
<section class="section thanks">
  <div class="wrap">
    <div class="ring" aria-hidden="true"></div>
    <p class="eyebrow"><span class="dot"></span>Page not found</p>
    <h1>That page is not here.</h1>
    <p class="lede" style="margin:0 auto">The link may be old. The light is this way.</p>
    <div class="hero-ctas" style="justify-content:center;flex-direction:row;flex-wrap:wrap">
      <a class="btn btn-primary" href="index.html">Back to Spindle</a>
      <a class="btn btn-ghost" href="faq.html">Read the FAQ</a>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ LEGAL (plain-language versions of ops/policies/*.md, which are lawyer-review DRAFTS)
def legal(title, intro, sections):
    body = f'<section class="section tight"><div class="wrap legal"><p class="eyebrow"><span class="dot"></span>Policy</p><h1>{title}</h1><p class="lede">{intro}</p>'
    for h, ps in sections:
        body += f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps)
    body += '<p class="tiny" style="margin-top:40px">Last updated: November 2026. Questions: <a data-email href="mailto:hello@example.com" class="u">hello@example.com</a>.</p></div></section>'
    return body

SHIPPING = legal("Shipping", f"{SHIPPING_LINE} states. Here is how pre-orders and delivery work.", [
  ("Pre-orders and ship dates", [
    "A pre-order is a place in the next batch, held by a refundable <span data-deposit>$25</span> deposit. The sconces in this batch have not been built yet.",
    "Batch two is planned to ship <span data-ship>the week of [SHIP DATE]</span>. That date is our honest estimate based on parts lead times and build pace, with a two-week buffer. It is not a guarantee.",
    "If we cannot ship by that date, we will email you before it passes with a new date. You can keep your place or cancel for a full refund of everything you have paid. If we have to move the date a second time, we will not ship without your fresh okay; if we do not hear from you, we refund you.",
    "When your sconce is nearly ready we email you a link to pay the balance (the price minus your deposit). If we hear nothing 30 days after that email, we refund your deposit and release your place.",
    "Batch two is capped at <span data-batch-two-cap>100</span> units. If you try to reserve after the cap is reached you will be told before paying that you are on the batch three list.",
  ]),
  ("Cost and where we ship", [
    "Shipping inside the contiguous US (the lower 48 states) is included in the price. Alaska, Hawaii and APO/FPO addresses pay the actual carrier difference, shown before you pay your balance. We do not ship outside the US yet." + (f" We also do not ship to {NO_SHIP_PLACES} for now, because local rules there require the whole light to be listed and ours is not yet." if NO_SHIP_PLACES else ""),
  ]),
  ("Carriers and transit", [
    "Orders ship from Fort Lauderdale, Florida by USPS Ground Advantage or UPS Ground, usually 2 to 5 business days in transit. Tracking is emailed when the label is printed.",
  ]),
  ("Lost or damaged", [
    "If the box arrives damaged, or a record we supplied arrives cracked, take photos before you throw anything away and email us within 7 days of delivery. We send a replacement and deal with the carrier ourselves.",
  ]),
  ("Sales tax", [
    "Florida orders are charged Florida sales tax. Orders to other states are not charged sales tax at this time.",
  ]),
])

RETURNS = legal("Returns and refunds", "Deposits refund any time before shipping. After delivery you have 30 days to return it.", [
  ("Deposits", [
    "Your <span data-deposit>$25</span> deposit is fully refundable at any time before your sconce ships, no reason needed. Email us or reply to your Stripe receipt and it goes back to your card within 5 business days. Your bank may take a few more days to show it.",
  ]),
  ("30-day returns", [
    "If you do not love it, you can return any sconce or kit within 30 days of delivery for a refund of the product price. Email us first and we send a return label.",
    "It needs to come back in its box with all its parts, not damaged, painted, cut or glued to anything. If we supplied the record, send the record back with it. If you used your own record, keep it.",
    "We deduct a flat $12 from the refund for the return label, unless the item arrived damaged or faulty, in which case the return is free. Refunds are made within 5 business days of the box reaching us.",
  ]),
  ("Named-title sconces", [
    "A Named sconce is built around a record we bought for you. It can be returned in the same 30 days, and the refund is the product price less a $25 restocking fee.",
  ]),
  ("What we cannot take back", [
    "Sconces that were installed somewhere wet, modified, or damaged by a power adapter other than ours; in-wall kits once the cable has been cut; records you supplied yourself.",
  ]),
  ("Warranty", [
    "Faults after 30 days are covered by the two-year limited warranty. See the <a href='warranty.html' class='u'>warranty</a> page.",
  ]),
])

WARRANTY = legal("Two-year limited warranty", "The light is covered for two years. The record is not. Here is the whole thing in plain words.", [
  ("Who is covered", [
    "The original buyer of a <span data-brand>Spindle</span> sconce or kit bought from us directly. The warranty does not transfer.",
  ]),
  ("What is covered", [
    "For two years from the day your order is delivered, the light (the backplate, LED strip, hub, wall plate, dome cap and the power adapter we shipped) is covered against defects in materials and workmanship under normal home use.",
  ]),
  ("What we will do", [
    "If a covered part fails we will, at our choice, repair it, replace it, or refund the price you paid for it. We pay return shipping for a confirmed warranty claim inside the United States.",
  ]),
  ("What is not covered", [
    "The vinyl record, whether we supplied it or you did. Records are used, decades old and shown for their looks; wear, scratches, warps and label damage are never covered.",
    "Damage from use outdoors or in a bathroom, kitchen or any damp place; from any power adapter other than the one we shipped; from installation against the instructions or local code; from hanging it above a heat source or in direct sun; and normal wear, modification, misuse or accident.",
  ]),
  ("How to claim", [
    "Email us with your order number, a short description and a photo or short video. We reply within two business days. Please do not send anything back before you hear from us.",
  ]),
  ("Limits", [
    "To the extent allowed by law, this is the only warranty we make, and implied warranties are limited to the same two years. We are not responsible for incidental or consequential costs such as an electrician, wall repair or lost time, except where the law does not allow that limit. Some states do not allow these limits, so they may not apply to you. This warranty gives you specific legal rights, and you may have others that vary by state.",
  ]),
])

PRIVACY = legal("Privacy", "What we collect, why, and what we never do with it.", [
  ("What we collect", [
    "If you join the waitlist: your email address and the version you are leaning toward. If you place a deposit: your name, email and payment details, which are processed and stored by Stripe, not by us. We see the last four digits of your card and nothing more. We ask for your shipping address before we ship.",
  ]),
  ("Analytics and advertising", [
    "This site uses the Meta pixel to measure whether our advertising works. It records page views, waitlist signups and deposits and shares them with Meta under Meta's data policy. You can opt out of personalised advertising in your Facebook and Instagram settings, and most browsers let you block third-party trackers. We do not use any other analytics.",
  ]),
  ("How we use it", [
    "To build and ship your order, to email you about batch two and three, to refund you when you ask, and to measure our advertising. We send no newsletters beyond those batch emails unless you opt in separately. Unsubscribe links are in every email.",
  ]),
  ("What we never do", [
    "We never sell, rent or trade your information. We never share it with anyone except the services that make the order happen: Stripe (payment), our email provider (the batch emails), the carrier (your address on the label), and Meta (advertising measurement as above).",
  ]),
  ("Your rights", [
    "Email us to see, correct or delete what we hold about you. We answer within 30 days.",
  ]),
])

TERMS = legal("Terms of sale", "The plain-English rules for pre-ordering and owning a Spindle.", [
  ("Pre-order", [
    "A deposit holds one place in a batch, in the version you select. It is not a purchase of the finished product. You buy the product when you pay the balance, which we ask for by email only when your unit is nearly ready to ship. You may cancel for a full refund at any time before it ships. Our ship dates are honest estimates, not guarantees; what happens if we are late is on the <a href='shipping.html' class='u'>shipping</a> page.",
  ]),
  ("Pricing", [
    "The balance you pay is the price shown when you placed your deposit, less the deposit. Florida sales tax is added for Florida addresses. Prices for future batches may change; yours does not.",
  ]),
  ("The product", [
    "<span data-brand>Spindle</span> sconces are hand-assembled lights built around real vinyl records. Where we supply the record it is a used, decades-old record chosen for looks. Expect visible wear. Records are not sold as playable. Where you supply the record, you choose a record you are happy to display and we take no responsibility for its condition.",
  ]),
  ("Safety and intended use", [
    "The Spindle is an indoor, dry-location decorative wall light powered by a 12-volt Class 2 plug-in adapter. Use only the supplied adapter. Mount it as described in the hanging sheet. Do not install it above a heat source or in direct sunlight. Do not place the adapter or its cord inside a wall. Running low-voltage cable inside a wall is your decision and your responsibility: check your local building code and use an electrician where the law or your comfort requires. The Spindle is not a listed light fixture and is not to be hardwired.",
  ]),
  ("Your records", [
    "A record hung on a wall is exposed to the room: dust, light and temperature. Our light touches it only with felt and a clear washer and does not alter it. We are not responsible for changes to a record caused by its surroundings.",
  ]),
  ("Returns and warranty", [
    "The <a href='returns.html' class='u'>returns policy</a> and the <a href='warranty.html' class='u'>two-year limited warranty</a> are part of these terms.",
  ]),
  ("Not affiliated", [
    "Records we include are real, previously owned pressings described factually. <span data-brand>Spindle</span> is not affiliated with, sponsored by or endorsed by any artist, band or record label. We do not reproduce cover art, logos or trademarks. If a rights holder asks us to stop offering a specific title, we will, within two business days.",
  ]),
  ("Limits on our liability", [
    "To the extent the law allows, our total liability for any order is the amount you paid for that order, and we are not liable for indirect or consequential losses such as wall repair or electrician fees. This does not limit liability for injury caused by our negligence, for fraud, or for anything the law says cannot be limited.",
  ]),
  ("Law", [
    "These terms are governed by Florida law.",
  ]),
])

_kit, _sc, _nm = usd(KIT_PRICE), usd(SCONCE_PRICE), usd(NAMED_PRICE)
PAGES = [
  dict(file="index.html", page="home", title="Spindle | Change the record. Change the room.",
       desc=f"A wall light that holds a real 12-inch vinyl record and glows warm behind it. Nothing glued to your vinyl. From {_kit}. Pre-order: hold one from batch two with a refundable $25.",
       preload='<link rel="preload" as="image" href="img/sq-chrome-1080.webp" imagesrcset="img/sq-chrome-640.webp 640w, img/sq-chrome-1080.webp 1080w" imagesizes="(min-width: 900px) 66vw, 100vw" type="image/webp" fetchpriority="high">\n',
       jsonld=PRODUCT_JSONLD, body=HOME),
  dict(file="product.html", page="product", title="Spindle 12 | Spindle", ogtype="product",
       desc=f"Spindle 12: a wall light that holds a real record. Kit {_kit}, with a vintage LP {_sc}, named album {_nm}. Mirror-chrome cap. Pre-order with a refundable $25 hold.",
       jsonld=PRODUCT_JSONLD, body=PRODUCT + STICKY),
  dict(file="install.html", page="install", title="How it works and how to hang it | Spindle",
       desc="Two screws and a plug, or hide the cord in the wall. How the Spindle mounts, how it is powered, and an honest account of heat.", body=INSTALL),
  dict(file="faq.html", page="faq", title="FAQ: heat, your record, wiring, renters, refunds | Spindle",
       desc="Will it warm my record? Is it UL listed? Do I need an electrician? Is the deposit refundable? Straight answers.", jsonld=FAQ_JSONLD, body=FAQ),
  dict(file="about.html", page="about", title="About | Spindle", desc="Designed in Fort Lauderdale by people who could not find a real-record wall light anywhere. Nothing glued to a record, ever.", body=ABOUT),
  dict(file="reserve.html", page="reserve", title="Reserve batch two | Spindle", desc="First batch of 20 sold out. Hold a Spindle from batch two with a refundable $25, or join the free waitlist.",
       body=RESERVE + STICKY),
  dict(file="thanks.html", page="thanks", title="You are on the list | Spindle", desc="Waitlist confirmed.", bodyattrs=' data-thanks="lead"', robots="noindex", body=THANKS_LEAD),
  dict(file="thanks-deposit.html", page="thanks", title="Reserved | Spindle", desc="Deposit received.", bodyattrs=' data-thanks="purchase"', robots="noindex", body=THANKS_DEPOSIT),
  dict(file="shipping.html", page="legal", title="Shipping | Spindle", desc="Shipping, pre-order ship dates and what happens if we are late.", body=SHIPPING),
  dict(file="returns.html", page="legal", title="Returns and refunds | Spindle", desc="Deposits refund any time before shipping. 30-day returns after delivery.", body=RETURNS),
  dict(file="warranty.html", page="legal", title="Two-year limited warranty | Spindle", desc="The light is covered for two years. The record is not.", body=WARRANTY),
  dict(file="privacy.html", page="legal", title="Privacy | Spindle", desc="What we collect and what we never do with it.", body=PRIVACY),
  dict(file="terms.html", page="legal", title="Terms of sale | Spindle", desc="Plain-English terms for pre-ordering and owning a Spindle.", body=TERMS),
  dict(file="404.html", page="legal", title="Page not found | Spindle", desc="That page is not here.", robots="noindex", body=NOT_FOUND),
]

PRICES = dict(finishes_open=FINISHES_OPEN, kit=KIT_PRICE, sconce=SCONCE_PRICE, named=NAMED_PRICE, set=SET_PRICE, set_records=SET_RECORDS_PRICE, deposit=DEPOSIT, set_open=SET_OPEN)
