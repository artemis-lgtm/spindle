# Page bodies for build.py. Plain HTML strings. No em-dashes. No band names, logos or album titles.

def pic(name, widths, alt, sizes="100vw", cls="", loading="lazy", ext="jpg"):
    """Static picture with webp + jpg fallbacks. name like 'exploded', widths like (900,1600)."""
    ws = sorted(widths)
    webp = ", ".join(f"img/{name}-{w}.webp {w}w" for w in ws)
    jpg = ", ".join(f"img/{name}-{w}.{ext} {w}w" for w in ws)
    return (f'<picture class="{cls}"><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="img/{name}-{ws[-1]}.{ext}" srcset="{jpg}" sizes="{sizes}" alt="{alt}" loading="{loading}" decoding="async" width="{ws[-1]}" height="{ws[-1] if name.startswith("sq") else round(ws[-1]*9/16)}"></picture>')

def fpic(prefix, widths, alt, sizes="100vw", loading="lazy", finish="chrome"):
    """Finish-swappable picture. prefix like 'sq' or 'hero'. main.js swaps {finish}."""
    ws = sorted(widths)
    tw = ", ".join(f"img/{prefix}-{{finish}}-{w}.webp {w}w" for w in ws)
    tj = ", ".join(f"img/{prefix}-{{finish}}-{w}.jpg {w}w" for w in ws)
    h = ws[-1] if prefix == "sq" else round(ws[-1] * 1080 / 1200)
    return (f'<picture data-src-tpl="img/{prefix}-{{finish}}-{ws[-1]}.jpg">'
            f'<source type="image/webp" data-srcset-tpl="{tw}" srcset="{tw.replace("{finish}", finish)}" sizes="{sizes}">'
            f'<img src="img/{prefix}-{finish}-{ws[-1]}.jpg" data-srcset-tpl="{tj}" srcset="{tj.replace("{finish}", finish)}" sizes="{sizes}" alt="{alt}" loading="{loading}" decoding="async" width="{ws[-1]}" height="{h}"></picture>')

SWATCHES = """<div class="swatches" role="group" aria-label="Finish">
  <div data-swatch-group="{target}" style="display:flex;gap:12px">
    <button class="swatch" type="button" data-finish="chrome" aria-pressed="true" aria-label="Chrome"><span></span></button>
    <button class="swatch" type="button" data-finish="brass" aria-pressed="false" aria-label="Brass"><span></span></button>
    <button class="swatch" type="button" data-finish="black" aria-pressed="false" aria-label="Black"><span></span></button>
  </div>
  <span class="swatch-name">Chrome</span>
</div>"""

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'

TRUST = f"""<div class="trust">
  <div>{CHECK}<span>12-volt plug-in. Nothing above 12 V inside the fixture or the wall.</span></div>
  <div>{CHECK}<span>Nothing glued, drilled or stuck to your record. Ever.</span></div>
  <div>{CHECK}<span>Swap the record in under a minute. One cap, one turn.</span></div>
  <div>{CHECK}<span>30-day returns on the fixture. Refundable deposit until it ships.</span></div>
</div>"""

FAQ_ITEMS = [
 ("Will the light heat up or warp my record?",
  "<p>No. The LED ring sits on the back of the backplate, facing the wall, where it cannot see the record at all. It is mounted on a thin aluminium ring that spreads its warmth, with a layer of cork and half an inch of wood between it and the record. The whole ring draws about 4 watts, and never more than 6, spread over a 28-inch circle. Vinyl starts to soften around 130 to 140 F; our heat calculation puts the record about 6 F above the room. The only way this record gets hot is if you hang it over a radiator or in direct sun, which the hang sheet tells you not to do. Our acceptance test for every batch is record face under 95 F in a 75 F room after a two-hour soak, and we publish the numbers once measured.</p>"),
 ("Is my record safe? What touches it?",
  "<p>Felt and one clear washer. The record rests on six felt pads and a felt ring on the backplate; a thin clear polyester washer lies on the label so the cap never turns against the paper, and the cap's own felt sits on that. The cap carries its own threaded stud, which passes through the spindle hole into a brass insert in the backplate; the smooth collar under the cap is a hair smaller than the hole, so nothing is forced and the record centres itself. You could take the record off tomorrow and play it. Three pads near the edge, three part-way in and the ring behind the label hold it flat, which is more support than a record gets in a sleeve on a shelf.</p>"),
 ("Can I change the record?",
  "<p>Yes, that is the point. Unscrew the dome cap, lift the record off, set the next one on, screw the cap back. Under a minute, no tools, and the fixture stays on the wall. Collectors tell us this is the whole reason they want the Kit.</p>"),
 ("How does it get power? Do I need an electrician?",
  "<p>No electrician. A UL-listed 12-volt adapter plugs into a normal outlet and feeds the sconce through a thin low-voltage cable. The default install hides that cable inside the wall: a 1-inch hole behind the fixture, the cable drops down the stud bay to a small jack plate at outlet height, and the adapter plugs in there. Low-voltage Class 2 cable is allowed inside walls without conduit in every US jurisdiction that follows the National Electrical Code (NEC 725). The adapter itself never goes in the wall. If you would rather not cut a hole, the surface option runs a braided cord down the wall, or inside a paintable raceway.</p>"),
 ("I rent. Can I still hang it?",
  "<p>Yes. The surface option needs two screw holes for the mounting plate, same as a picture. The plate also bolts to any existing single-gang or round box if you have a dead sconce location you want to reuse. The in-wall option needs a 1-inch hole and a single-gang cutout at outlet height, which is a patch job when you leave; many renters do it anyway, but check your lease.</p>"),
 ("How bright is it? Can I dim it?",
  "<p>It is a mood light, not a reading light. Warm 2700K, high colour-rendering, dotless ring that throws an amber halo about 4 inches past the edge of the record. The inline dimmer takes it from a full glow to a candle. There is no colour-changing mode and no remote, on purpose.</p>"),
 ("Which records work?",
  "<p>Any standard 12-inch LP. The 7-inch singles in the Set use a chromed adapter cap that fills the large centre hole. Picture discs and coloured vinyl look spectacular with light behind them. Warped records will sit a little proud at the edge but still hang fine.</p>"),
 ("What record comes with the $129 Spindle 12?",
  "<p>A genuine used LP from the decade you choose (60s, 70s or 80s), our pick of title, cleaned and graded for display. Label wear is part of the piece. If you want to name the album, the $179 Named option lets you pick from a menu of ten classic titles; we will send the menu with your deposit confirmation. We never show cover art or logos and we are not affiliated with any artist or label.</p>"),
 ("When does batch two ship?",
  "<p><span data-ship>the week of [SHIP DATE]</span>. That date has a two-week buffer built in. If we cannot ship by then, we will email you with a new date and you can cancel for a full refund at that point or any time before shipping. Batch two is capped at <span data-batch-two-cap>100</span> units; deposits after that go on the batch three list and we tell you so before you pay.</p>"),
 ("Is the $25 deposit really refundable?",
  "<p>Yes, fully, at any time before your sconce ships, for any reason. Email us and the refund goes back to your card. The deposit is applied to the balance; you pay the rest when we are ready to ship your unit.</p>"),
 ("Shipping and returns?",
  "<p>Free US shipping on every order. Fixtures ship in a 13 x 13 x 3 inch box with the record (if included) in its own sleeve. Returns: 30 days from delivery on the fixture, unused, in its packaging, for a full refund less return shipping. Records are graded and photographed before they leave, so a record is returnable only if it arrives damaged. Details on the <a href='shipping.html'>shipping</a> and <a href='returns.html'>returns</a> pages.</p>"),
 ("Is it UL listed?",
  "<p>The parts that touch mains power or run inside your wall are UL or ETL listed: the 12-volt adapter, the LED strip and the cable. The only parts we make are the wooden backplate, the hub, the steel plate and the cap, none of which carry current above 12 volts DC. The 120-volt side of the system lives entirely inside the listed adapter at your outlet. That is the same architecture as every LED strip kit sold in the US.</p>"),
]

def faq_html(items):
    return "<div class=\"faq\">" + "".join(f"<details><summary>{q}</summary><div class=\"a\">{a}</div></details>" for q, a in items) + "</div>"

FAQ_JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
""" + ",\n".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (
        __import__("json").dumps(q), __import__("json").dumps(__import__("re").sub("<[^>]+>", "", a).replace("the week of [SHIP DATE]", "the week of [SHIP DATE]")))
    for q, a in FAQ_ITEMS) + """
]}
</script>
"""

PRODUCT_JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Product","name":"Spindle 12","brand":{"@type":"Brand","name":"Spindle"},
"description":"Halo-backlit wall sconce built around a real 12-inch vinyl record. Warm 2700K LED ring, 12-volt plug-in, chrome, brass or black dome cap. Nothing glued to the record.",
"image":["https://example.com/img/sq-chrome-1080.jpg","https://example.com/img/sq-brass-1080.jpg","https://example.com/img/sq-black-1080.jpg"],
"offers":[
 {"@type":"Offer","name":"Spindle Kit","price":"89","priceCurrency":"USD","availability":"https://schema.org/PreOrder","url":"https://example.com/product.html#kit"},
 {"@type":"Offer","name":"Spindle 12","price":"129","priceCurrency":"USD","availability":"https://schema.org/PreOrder","url":"https://example.com/product.html"},
 {"@type":"Offer","name":"Spindle 12, Named","price":"179","priceCurrency":"USD","availability":"https://schema.org/PreOrder","url":"https://example.com/product.html#named"},
 {"@type":"Offer","name":"Spindle Set","price":"249","priceCurrency":"USD","availability":"https://schema.org/PreOrder","url":"https://example.com/product.html#set"}
]}
</script>
"""

RESERVE_BLOCK = """
<section class="section" id="reserve">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Batch two</p>
    <h2>First batch of <span data-batch-size>20</span> sold out<span data-sold-date></span>. Batch two is open.</h2>
    <p class="lede">Two ways in. A refundable <span data-deposit>$25</span> deposit holds a unit and your finish. The free list just hears when the next batch opens.</p>
    <div class="reserve-grid" style="margin-top:32px">
      <div class="offer primary">
        <span class="pill">Holds your unit</span>
        <h3>Reserve with a <span data-deposit>$25</span> refundable deposit</h3>
        <div class="price"><span data-deposit>$25</span> <span class="muted" style="font-size:1rem;font-family:var(--font-body)">today, applied to your balance</span></div>
        <ul>
          <li>Fully refundable at any time before your sconce ships, for any reason.</li>
          <li>Ships <span data-ship>the week of [SHIP DATE]</span>. Miss it and you get a new date plus the option of a full refund.</li>
          <li>Capped at <span data-batch-two-cap>100</span> units. Deposit <span style="white-space:nowrap">No. 101</span> goes on the batch three list, and we tell you before you pay.</li>
          <li>Pick your model and finish at checkout: <b data-sku-name>Spindle 12</b> in <b data-finish-name>Chrome</b> is what you have selected.</li>
        </ul>
        <a class="btn btn-primary btn-block" data-deposit-link href="#">Reserve batch two, <span data-deposit>$25</span> refundable</a>
        <p class="form-note">Secure checkout by Stripe. Shipping address and record preference are collected at checkout.</p>
      </div>
      <div class="offer">
        <span class="pill">Free</span>
        <h3>Join the waitlist</h3>
        <p class="muted small">One email when batch two opens for balance payment, one when batch three opens. Nothing else.</p>
        <form id="waitlist-form" action="#" method="get" novalidate>
          <input type="hidden" name="_next" value="thanks.html">
          <input type="hidden" name="_subject" value="Spindle waitlist signup">
          <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
          <div class="field"><label for="wl-email">Email</label><input id="wl-email" type="email" name="email" required autocomplete="email" inputmode="email" placeholder="you@example.com"></div>
          <div class="field"><label for="wl-finish">Finish you are leaning toward</label>
            <select id="wl-finish" name="finish"><option value="chrome">Chrome</option><option value="brass">Brass</option><option value="black">Black</option><option value="undecided">Not sure yet</option></select></div>
          <label class="consent"><input type="checkbox" name="consent" required> Email me about batch two and three. Unsubscribe any time. See the <a href="privacy.html">privacy policy</a>.</label>
          <button class="btn btn-ghost btn-block" type="submit">Join the free waitlist</button>
        </form>
      </div>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ HOME
HOME = f"""
<section class="hero" id="top" aria-label="The Spindle in a dark room">
  <div class="hero-media">
    <picture>
      <source type="image/webp" srcset="img/sq-chrome-640.webp 640w, img/sq-chrome-1080.webp 1080w" sizes="(min-width: 900px) 66vw, 100vw">
      <img src="img/sq-chrome-1080.jpg" srcset="img/sq-chrome-640.jpg 640w, img/sq-chrome-1080.jpg 1080w" sizes="(min-width: 900px) 66vw, 100vw" alt="A black 12-inch record mounted flat on a plaster wall with a mirror-chrome dome at its centre and a warm amber halo of light spilling onto the wall behind it" fetchpriority="high" decoding="async" width="1080" height="1080">
    </picture>
    <div class="hero-glow" aria-hidden="true"></div>
    <div class="hero-vignette" aria-hidden="true"></div>
    <div class="tap-hint" aria-hidden="true"><span class="pulse"></span>Scroll or tap to turn it on</div>
  </div>
  <div class="wrap hero-content">
    <div>
      <p class="eyebrow"><span class="dot"></span>First batch of <span data-batch-size>20</span> sold out</p>
      <h1>Change the record.<br>Change the room.</h1>
      <p class="lede">Your record, lit from behind. A 2700 K halo on the wall, a chrome dome where the spindle would be. Nothing glued, nothing drilled.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="reserve.html">Reserve batch two, <span data-deposit>$25</span> refundable</a>
        <a class="btn btn-ghost" href="product.html">See Spindle 12</a>
      </div>
      <p class="hero-price">From <b>$89</b> for the Kit with your own record. <b>$129</b> with a vintage LP. Free US shipping.</p>
    </div>
    <div>
      <div class="dimmer"><label for="dimmer">Dimmer</label><input id="dimmer" type="range" min="0" max="100" value="0" aria-label="Hero light dimmer"></div>
    </div>
  </div>
</section>

<section class="section tight"><div class="wrap">{TRUST}</div></section>

<section class="section" id="story">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Your record. Our light.</p>
    <h2 style="max-width:16em">Twelve inches of what you love, lit at 2700 K.</h2>
    <div class="story-grid reveal" style="margin-top:40px">
      <div class="beat"><h3>Light behind it, not on it</h3><p>A ring of warm 2700K LEDs sits on the back of a 10.5-inch backplate and throws its light at the wall. The record floats an inch off the plaster in its own amber halo. The grooves catch the edge light. The label sits in shadow, the way it does on a turntable.</p></div>
      <div class="beat"><h3>One piece of jewellery</h3><p>The only hardware you see is the dome at the centre: solid metal, mirror chrome by default, brass or gloss black if your room asks for it. It threads through the spindle hole onto a brass insert and holds the record with a felt washer. It is the whole product in one part.</p></div>
      <div class="beat"><h3>Your record, every time</h3><p>Unscrew the dome, lift the record, set the next one down. Under a minute, no tools, the fixture never leaves the wall. Buy the Kit and mount what you already own. Buy the Spindle and we send a vintage LP from the decade you pick.</p></div>
    </div>
  </div>
</section>

<section class="section alt" id="finishes">
  <div class="wrap two">
    <div class="frame dark finish-img reveal">{fpic("sq", (640, 1080), "The Spindle sconce, close on the record and dome cap, in the selected finish", sizes="(min-width: 900px) 50vw, 100vw")}</div>
    <div class="reveal">
      <p class="eyebrow"><span class="dot"></span>Three finishes, one price</p>
      <h2>Chrome. Brass. Black.</h2>
      <p class="muted">Chrome is the lead: reflective against matte vinyl, warm light only. Brass reads warmer in a room full of wood. Black disappears and lets the halo do the talking. Tap a finish to see it rendered.</p>
      <div style="margin:22px 0 28px">{SWATCHES.format(target="#finishes picture")}</div>
      <a class="btn btn-primary" href="product.html">Configure yours</a>
    </div>
  </div>
</section>

<section class="section" id="how">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>How it works</p>
    <h2 style="max-width:14em">Five parts. The record is one of them.</h2>
    <div class="two" style="margin-top:32px">
      <div class="frame reveal">{pic("exploded", (900, 1600), "Exploded view: wall, backplate with LED ring and cord, standoff, record, felt washer and chrome dome cap in a line", sizes="(min-width: 900px) 50vw, 100vw")}</div>
      <div class="steps reveal" style="grid-template-columns:1fr">
        <div class="step"><h3>Steel plate on the wall</h3><p>Four-inch plate, levels after the screws are in, fits drywall anchors, a stud, or any existing single-gang or round box.</p></div>
        <div class="step"><h3>Hub twist-locks on</h3><p>Three bayonet slots drop over the plate studs and turn twenty degrees. A set screw at six o'clock stops it ever untwisting.</p></div>
        <div class="step"><h3>Backplate carries the light</h3><p>A 10.5-inch matte black disc with the dotless LED ring on its back, facing the wall, and a brass threaded insert at the centre.</p></div>
        <div class="step"><h3>Your record, then the dome</h3><p>Record on the felt pads, dome through the spindle hole, finger-tight. Plug in the 12-volt adapter. Dim to taste.</p></div>
      </div>
    </div>
    <p class="center" style="margin-top:32px"><a class="btn btn-ghost" href="install.html">Install guide, in-wall and surface</a></p>
  </div>
</section>

<section class="section alt" id="swap">
  <div class="wrap">
    <div class="two rev">
      <div class="reveal">
        <p class="eyebrow"><span class="dot"></span>The sconce that takes requests</p>
        <h2>The dome comes off in two turns. Put on what you are playing this month.</h2>
        <p class="muted">The dome cap is the only fastener. Two turns, lift the record, set the next one down, two turns back. A picture disc for a party. The pressing you found at the flea market. The album you have been meaning to frame for ten years. The sconce stays on the wall; the record is the part that moves.</p>
        <p class="muted">Nothing is glued, taped or drilled. Felt holds the record; a clear washer guards the label.</p>
      </div>
      <div class="swap reveal" style="grid-template-columns:repeat(3,1fr)">
        <figure><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-chrome.webp"><img src="img/cap-chrome.jpg" alt="Chrome dome cap on a record label" loading="lazy" decoding="async" width="500" height="500"></picture></div><figcaption>Chrome</figcaption></figure>
        <figure><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-brass.webp"><img src="img/cap-brass.jpg" alt="Brass dome cap on a record label" loading="lazy" decoding="async" width="500" height="500"></picture></div><figcaption>Brass</figcaption></figure>
        <figure><div class="frame dark"><picture><source type="image/webp" srcset="img/cap-black.webp"><img src="img/cap-black.jpg" alt="Gloss black dome cap with chrome rim on a record label" loading="lazy" decoding="async" width="500" height="500"></picture></div><figcaption>Black</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="section" id="proof">
  <div class="wrap">
    <div class="proof reveal">
      <div class="card"><div class="num"><span data-batch-size>20</span> of <span data-batch-size>20</span></div><div class="label">First batch sold out<span data-sold-date></span>. Every unit hand-built in Fort Lauderdale.</div></div>
      <div class="card"><div class="num">2700K</div><div class="label">Warm, dotless, high colour-rendering LED ring. Dimmable to a candle. No colour-changing modes, no remote.</div></div>
      <div class="card"><div class="num">12 V</div><div class="label">Class 2 low voltage from a UL-listed plug-in adapter. Nothing above 12 volts inside the fixture or the wall.</div></div>
    </div>
  </div>
</section>

<section class="section alt" id="faq-preview">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>The questions everyone asks</p>
    <h2>Heat, safety, wiring, renters.</h2>
    <div style="margin-top:20px">{faq_html(FAQ_ITEMS[:5])}</div>
    <p style="margin-top:24px"><a class="btn btn-ghost" href="faq.html">All twelve questions</a></p>
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

PRODUCT = f"""
<section class="wrap pdp" data-sticky-anchor>
  <div class="gallery">
    <div class="main finish-img" id="pdp-main">{fpic("sq", (640, 1080), "The Spindle sconce in the selected finish, lit, on a warm plaster wall", sizes="(min-width: 900px) 50vw, 100vw", loading="eager")}</div>
    <div class="thumbs" role="group" aria-label="Gallery">
      <button type="button" aria-pressed="true" data-full="img/sq-{{finish}}-1080.jpg" data-finish-img><img src="img/sq-chrome-640.jpg" alt="Sconce lit, front view" loading="lazy" width="640" height="640"></button>
      <button type="button" aria-pressed="false" data-full="img/cap-chrome.jpg"><img src="img/cap-chrome.jpg" alt="Chrome dome cap detail" loading="lazy" width="500" height="500"></button>
      <button type="button" aria-pressed="false" data-full="img/exploded-1600.jpg"><img src="img/exploded-900.jpg" alt="Exploded view of the parts" loading="lazy" width="900" height="506"></button>
      <button type="button" aria-pressed="false" data-full="img/rear-1600.jpg"><img src="img/rear-900.jpg" alt="Rear view of the mount and hub" loading="lazy" width="900" height="506"></button>
      <button type="button" aria-pressed="false" data-full="img/cutaway-1600.jpg"><img src="img/cutaway-900.jpg" alt="Wall cutaway showing the in-wall cable" loading="lazy" width="900" height="506"></button>
    </div>
    <p class="caption">Renders of the production design. Photographs of the batch-one units replace these as they are shot. Labels shown are plain house labels; your record is your own.</p>
  </div>
  <div class="buy">
    <p class="eyebrow"><span class="dot"></span>First batch of <span data-batch-size>20</span> sold out. Batch two open.</p>
    <h1 data-product>Spindle 12</h1>
    <p class="lede" style="font-size:1.35rem">Twelve inches of what you love, lit at 2700 K.</p>
    <p class="mono" style="margin:-4px 0 14px">Spindle 12 &middot; <span data-finish-name>Chrome</span> &middot; 2700 K &middot; 12 V Class 2</p>
    <div class="pricing"><span class="p" data-price>$129</span><span class="anchor">Free US shipping. Designer ringed-disc sconces run $740 to $755; this one holds a real record.</span></div>

    <div class="opt-row">
      <div class="lbl"><span>Model</span><span class="tiny">Choose one</span></div>
      <div class="skus">
        {sku("kit", "Your record", "Spindle Kit", "The light, the mount and the cap. You supply the record.", "$89")}
        {sku("sconce", "With a vintage LP", "Spindle 12", "The kit plus a genuine used LP from the decade you pick. Our choice of title.", "$129", True)}
        {sku("named", "You name the album", "Spindle 12, Named", "The kit plus an original pressing from our menu of ten classic titles.", "$179")}
        {sku("set", "12-inch + two 7-inch", "Spindle Set", "One Spindle 12 and two Spindle 7 singles with chromed 45-adapter caps. $249 with your records, $329 with ours.", "$249")}
      </div>
      <div id="set-options" hidden style="margin-top:-6px;margin-bottom:12px">
        <label class="consent" style="margin:0"><input type="checkbox" id="set-records"> Include three records from us (+$80, total $329)</label>
      </div>
    </div>

    <div class="opt-row">
      <div class="lbl"><span>Finish: <b data-finish-name>Chrome</b></span><span class="tiny">Same price, any finish</span></div>
      {SWATCHES.format(target="#pdp-main picture")}
    </div>

    <div class="sold-note">Batch two is capped at <span data-batch-two-cap>100</span> units and ships <span data-ship>the week of [SHIP DATE]</span>. A <span data-deposit>$25</span> refundable deposit holds your model and finish; the balance is charged when your unit is ready to ship.</div>

    <a class="btn btn-primary btn-block" data-deposit-link href="#">Reserve <span data-sku-name>Spindle 12</span> with a <span data-deposit>$25</span> refundable deposit</a>
    <p class="form-note" style="text-align:center">Secure checkout by Stripe. Refundable any time before shipping. <a href="reserve.html#waitlist-form" style="text-decoration:underline">Prefer the free waitlist?</a></p>

    <div class="includes" style="margin-top:24px" data-includes="kit">
      <b>In the Kit box</b>
      <ul><li>Backplate with 2700K dotless LED ring and brass 1/4-20 insert</li><li>Dome cap in your finish with felt washer</li><li>Hub with a short power pigtail, steel mounting plate with three bayonet studs, set screw and key</li><li>Screws and anchors, 12 V UL-listed dimming adapter with 6 ft lead</li><li>The one-page hang sheet. You supply the 12-inch record.</li></ul>
    </div>
    <div class="includes" style="margin-top:24px" data-includes="sconce" hidden>
      <b>In the Spindle 12 box</b>
      <ul><li>Everything in the Kit</li><li>A genuine used 12-inch LP from the decade you choose (60s, 70s or 80s), cleaned and graded for display, in its own sleeve</li><li>Our pick of title. Label wear is part of the piece.</li></ul>
    </div>
    <div class="includes" style="margin-top:24px" data-includes="named" hidden>
      <b>In the Named box</b>
      <ul><li>Everything in the Kit</li><li>An original pressing of the title you pick from our menu of ten classics, sent with your deposit confirmation</li><li>Graded, cleaned, photographed before it ships. Not affiliated with any artist or label.</li></ul>
    </div>
    <div class="includes" style="margin-top:24px" data-includes="set" hidden>
      <b>In the Set box</b>
      <ul><li>One Spindle 12 with everything in the Kit</li><li>Two Spindle 7 singles with smaller backplates, chromed 45-adapter caps, their own plates and adapters</li><li>Optional: three records from us, one LP and two singles, for $80 more</li></ul>
    </div>

    <table class="spec" style="margin-top:28px">
      <tr><th>Record</th><td>Any standard 12-inch LP (7-inch singles in the Set). Held between felt, with a clear washer protecting the label. Nothing glued.</td></tr>
      <tr><th>Light</th><td>2700K warm white, CRI 90+, dotless COB ring on the back of the backplate, facing the wall. About 4 W, up to 6 W. Inline dimmer.</td></tr>
      <tr><th>Power</th><td>12 V DC Class 2 from a UL-listed plug-in adapter, 6 ft lead. Optional in-wall CL2 cable kit.</td></tr>
      <tr><th>Cap</th><td>Solid metal dome, about 1.5 inch, on a 1/4-20 stud. Mirror chrome, brushed brass or gloss black.</td></tr>
      <tr><th>Backplate</th><td>10.5 inch matte black, 1/2 inch, brass threaded insert. 1 inch wall gap.</td></tr>
      <tr><th>Mount</th><td>4 inch steel plate (box, anchors or stud), bayonet hub with set screw. Levels after screwing.</td></tr>
      <tr><th>Weight</th><td>About 1.5 lb with record.</td></tr>
      <tr><th>Made</th><td>Hand-assembled in Fort Lauderdale, Florida.</td></tr>
    </table>
  </div>
</section>

<section class="section alt" style="margin-top:56px">
  <div class="wrap">
    <h2>Questions before you reserve</h2>
    <div style="margin-top:20px">{faq_html([FAQ_ITEMS[0], FAQ_ITEMS[1], FAQ_ITEMS[7], FAQ_ITEMS[8], FAQ_ITEMS[9]])}</div>
    <p style="margin-top:24px"><a class="btn btn-ghost" href="faq.html">All twelve questions</a></p>
  </div>
</section>
"""

STICKY = """<div class="sticky-bar" aria-live="polite">
  <div class="meta"><b data-sticky-name>Spindle 12, Chrome</b><span data-sticky-price>$129 at ship. $25 refundable deposit today.</span></div>
  <a class="btn btn-primary" data-deposit-link href="#">Reserve, $25</a>
</div>"""

# ------------------------------------------------------------------ INSTALL
INSTALL = f"""
<section class="section tight">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>How it works</p>
    <h1 style="max-width:11em">The wire disappears. The record stays yours.</h1>
    <p class="lede">Two install paths. In-wall is the default because that is what most people want: no cord on the wall, the adapter at the outlet where it belongs. Surface takes fifteen minutes and two screws.</p>
  </div>
</section>

<section class="section tight">
  <div class="wrap two">
    <div class="frame">{pic("rear", (900, 1600), "Rear exploded view: drywall with 1-inch hole, steel plate with bayonet studs, hub with set screw and cable pocket, backplate with LED ring, record, felt washer and chrome dome", sizes="(min-width: 900px) 50vw, 100vw", loading="eager")}</div>
    <div>
      <h2>The mount</h2>
      <p class="muted">A 4-inch steel plate screws to the wall over a 1-inch hole. Its arc slots match a single-gang low-voltage bracket and a round box, and take two screws into anchors or a stud when there is no box. The slots give about nine degrees of rotation, so you level the plate after the screws are started.</p>
      <p class="muted">The hub on the back of the sconce has three J-slots that drop over the plate's bayonet studs and twist about twenty degrees to lock. One set screw at six o'clock stops a knock from ever untwisting it. The hub carries a short power lead with a socket on its end; the low-voltage cable plugs into it, in the wall or just behind the backplate.</p>
      <p class="muted">The record is clamped from the front by the dome cap, so swapping a record never touches the mount.</p>
    </div>
  </div>
</section>

<section class="section alt" id="in-wall">
  <div class="wrap">
    <p class="eyebrow"><span class="dot"></span>Option A, the default</p>
    <h2>In-wall. About 45 minutes, no electrician.</h2>
    <div class="two" style="margin-top:28px">
      <div class="frame">{pic("cutaway", (900, 1600), "Wall cutaway: the sconce at eye level, a CL2 cable running inside the stud bay down to a keystone jack plate beside an outlet, the 12-volt adapter plugged in at the outlet", sizes="(min-width: 900px) 50vw, 100vw")}</div>
      <div>
        <p class="muted">Only the 12-volt side goes inside the wall, in cable rated CL2, which the National Electrical Code allows in walls without conduit (NEC 725). The plug-in adapter never goes in the wall: NEC 400.12 prohibits concealed power cords, so the adapter and its cord stay at the receptacle, where a wall-wart belongs.</p>
        <p class="muted">What you see when it is done: the sconce, a white single-gang plate beside your outlet with a small DC jack in it, a 6-inch jumper, and the adapter. Nothing on the wall between.</p>
        <p class="muted small">Want the adapter hidden too? A recessed power kit (PowerBridge, Legrand, Datacomm) puts a recessed receptacle inside the wall behind a flush plate. We link to them in the hang sheet; we do not sell them.</p>
      </div>
    </div>
    <div class="steps four" style="margin-top:32px">
      <div class="step"><h3>Pick the spot</h3><p>Record centre at 58 to 62 inches is typical. Stud finder: the hole must sit between studs, in the same bay as the outlet below.</p></div>
      <div class="step"><h3>Mark and cut</h3><p>Plate on the wall, bubble level on its top edge, mark two slots. Cut the 1-inch hole at centre. Cut the single-gang opening beside the outlet with the bracket's template.</p></div>
      <div class="step"><h3>Pull the cable</h3><p>Fish the CL2 cable from the top hole down to the bottom opening. Land the bottom end in the keystone coupler, screw the plate to the bracket.</p></div>
      <div class="step"><h3>Plate, hub, level</h3><p>Screw the plate on a quarter-turn loose, level, tighten. Plug the cable into the hub's power lead and tuck it through the plate. Hang, twist clockwise, set screw.</p></div>
      <div class="step"><h3>Record and dome</h3><p>Record on the felt pads, dome through the spindle hole with its felt washer, finger-tight.</p></div>
      <div class="step"><h3>Plug in</h3><p>Adapter lead into the jack plate, adapter into the outlet. Set the dimmer. Done.</p></div>
    </div>
    <p class="tiny" style="margin-top:18px">In-wall kit (15 ft CL2 cable, old-work bracket, keystone plate and DC coupler, pull string, drill card) is sold as an add-on at checkout.</p>
  </div>
</section>

<section class="section" id="surface">
  <div class="wrap two rev">
    <div>
      <p class="eyebrow"><span class="dot"></span>Option B</p>
      <h2>Surface. About 15 minutes, two screws.</h2>
      <p class="muted">Same plate, same hub. The hub's short power lead comes out through the channel at six o'clock and the 6-foot braided adapter lead plugs into it, hidden behind the backplate, then runs down the wall to the outlet. Add a paintable raceway if you want it flush, or let the braided cord be part of the look.</p>
      <p class="muted">Renters: two screw holes, same as a picture frame. If you have a dead sconce box on the wall already, the plate bolts straight to it.</p>
      <p class="eyebrow" style="margin-top:28px"><span class="dot"></span>Option C</p>
      <h3>Hardwired, by your electrician</h3>
      <p class="muted small">A listed Class 2 12-volt driver in a standard box behind the sconce, switched from the wall. Our plate bolts to the box ears. The sconce itself remains a 12-volt device with no 120-volt parts. We supply a one-page sheet for the electrician.</p>
    </div>
    <div class="frame dark finish-img">{fpic("hero", (800, 1200), "The Spindle lit on a warm wall with the braided cord running down to the floor", sizes="(min-width: 900px) 50vw, 100vw")}</div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2>Heat, in numbers</h2>
    <div class="two">
      <div>
        <p class="muted">Vinyl softens around 130 to 140 F. A low-power LED strip in open air runs well under that, and in this design the strip points away from the record: it sits on the back of the backplate facing the wall, on an aluminium ring that spreads its warmth, with a layer of cork and half an inch of wood between it and the record. About four watts over a 28-inch ring is calculated to lift the record about 6 F above the room; we publish the measured number once the first units are tested.</p>
        <p class="muted">Our acceptance test for every batch is a two-hour soak with an infrared thermometer at three points: strip surface, record back at the pad radius, and the label. Pass is record face under 95 F in a 75 F room. The numbers get printed here once measured.</p>
        <p class="muted small">The one real heat risk is the room, not the lamp. Do not hang any record over a radiator or in direct sun.</p>
      </div>
      <div class="frame">{pic("exploded", (900, 1600), "Exploded view showing the LED ring on the backplate rim, separated from the record by the standoff", sizes="(min-width: 900px) 50vw, 100vw")}</div>
    </div>
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
    <p class="lede">Heat, warping, record safety, wiring, renters, shipping and returns. If yours is not here, email <a data-email href="mailto:hello@example.com" style="text-decoration:underline">hello@example.com</a>.</p>
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
    <h1 style="max-width:12em">Built in Fort Lauderdale by people who could not find this anywhere.</h1>
    <div class="two" style="margin-top:32px">
      <div>
        <p class="muted">The idea was simple and the market had nothing: a wall light built around a real record that looked like a lighting fixture, not a craft project. What existed was either a resin miniature with three AAA batteries, a glued stack of LPs on a wooden arm, or an acrylic "now playing" shelf. Nobody was treating the record as the object and the light as the frame.</p>
        <p class="muted">So we designed one the way a lighting company would. Low-voltage Class 2 power from a listed adapter. A steel plate that levels and bolts to any box. A dotless 2700K ring that throws its light at the wall and never at the vinyl. And one piece of real metal at the centre, because the only thing you touch should feel like it cost something.</p>
        <p class="muted">The rule we will not break: nothing is ever glued, drilled or stuck to a record. Your pressing goes on the wall and comes off the wall exactly as it went on.</p>
        <p class="muted">The first <span data-batch-size>20</span> went to friends and the people who saw the prototype on a wall and asked where to get one. Batch two is the first one open to everyone, capped at <span data-batch-two-cap>100</span> so we can hand-build every unit and keep the promise on the ship date.</p>
        <p class="muted small"><span data-brand>Spindle</span> is an independent company. We are not affiliated with, sponsored by or endorsed by any artist, band or record label. Records we include are genuine previously owned pressings described factually; we never reproduce cover art or logos.</p>
      </div>
      <div class="frame dark finish-img">{fpic("sq", (640, 1080), "The Spindle in the selected finish", sizes="(min-width: 900px) 50vw, 100vw")}</div>
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
    <h1 style="max-width:12em">Hold a Spindle 12 from batch two.</h1>
    <p class="lede">Pick your model and finish, then choose the deposit or the free list below. The deposit is the only way to guarantee a unit.</p>
    <div class="two" style="margin-top:28px;align-items:start">
      <div class="frame dark finish-img">{fpic("sq", (640, 1080), "The Spindle in the selected finish", sizes="(min-width: 900px) 50vw, 100vw", loading="eager")}</div>
      <div>
        <div class="opt-row"><div class="lbl"><span>Model</span></div>
          <div class="skus">
            {sku("kit", "Your record", "Spindle Kit", "You supply the record.", "$89")}
            {sku("sconce", "With a vintage LP", "Spindle 12", "A used LP from your decade, our pick.", "$129", True)}
            {sku("named", "You name the album", "Spindle 12, Named", "Pick from our menu of ten.", "$179")}
            {sku("set", "12-inch + two 7-inch", "Spindle Set", "$249 with your records, $329 with ours.", "$249")}
          </div>
          <div id="set-options" hidden><label class="consent" style="margin:0"><input type="checkbox" id="set-records"> Include three records from us (total $329)</label></div>
        </div>
        <div class="opt-row"><div class="lbl"><span>Finish: <b data-finish-name>Chrome</b></span></div>{SWATCHES.format(target=".pdp-reserve-img picture, #reserve-img picture")}</div>
        <p class="muted small">Price at ship: <b data-price style="color:var(--ink)">$129</b>, free US shipping. Today: <span data-deposit>$25</span>, refundable.</p>
      </div>
    </div>
  </div>
</section>
{RESERVE_BLOCK}
"""

# ------------------------------------------------------------------ THANKS
THANKS_LEAD = """
<section class="section thanks">
  <div class="wrap">
    <div class="ring" aria-hidden="true"></div>
    <p class="eyebrow"><span class="dot"></span>You are on the list</p>
    <h1>We will write when batch two opens.</h1>
    <p class="lede" style="margin:0 auto">One email when batch two opens for balance payment, one when batch three opens. If you want to skip the line, a <span data-deposit>$25</span> refundable deposit holds a unit today.</p>
    <div class="hero-ctas" style="justify-content:center;flex-direction:row;flex-wrap:wrap">
      <a class="btn btn-primary" data-deposit-link href="#">Reserve with a <span data-deposit>$25</span> deposit</a>
      <a class="btn btn-ghost" href="index.html">Back to Spindle</a>
    </div>
  </div>
</section>
"""

THANKS_DEPOSIT = """
<section class="section thanks">
  <div class="wrap">
    <div class="ring" aria-hidden="true"></div>
    <p class="eyebrow"><span class="dot"></span>Reserved</p>
    <h1>Your Spindle is held.</h1>
    <p class="lede" style="margin:0 auto">Thank you. Your <span data-deposit>$25</span> deposit for <b data-thanks-selection>Spindle 12 in Chrome</b> is in, and a receipt from Stripe is on its way to your inbox.</p>
    <p class="tagline" style="margin-top:10px">Put something on.</p>
    <div class="offer" style="max-width:36em;margin:28px auto 0;text-align:left">
      <h3>What happens next</h3>
      <ul>
        <li>Batch two ships <span data-ship>the week of [SHIP DATE]</span>. We charge the balance only when your unit is ready to ship, and we email you first.</li>
        <li>If we cannot ship by that date we will email you a new date and you can cancel for a full refund.</li>
        <li>Your deposit is fully refundable at any time before shipping. Reply to the receipt email and it goes back to your card.</li>
        <li>Named model: the title menu comes in your confirmation email. Spindle 12: tell us your decade by replying.</li>
      </ul>
      <p class="tiny" style="margin:0">Need to change the finish or model? Reply to the receipt email. Nothing is locked until we build it.</p>
    </div>
    <p style="margin-top:28px"><a class="btn btn-ghost" href="install.html">Read the install guide while you wait</a></p>
  </div>
</section>
"""

# ------------------------------------------------------------------ LEGAL STUBS
def legal(title, intro, sections):
    body = f'<section class="section tight"><div class="wrap legal"><p class="eyebrow"><span class="dot"></span>Policy</p><h1>{title}</h1><p class="lede">{intro}</p>'
    for h, ps in sections:
        body += f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps)
    body += '<p class="tiny" style="margin-top:40px">Last updated: November 2026. Questions: <a data-email href="mailto:hello@example.com">hello@example.com</a>.</p></div></section>'
    return body

SHIPPING = legal("Shipping", "Free US shipping on every order. Here is how pre-orders and delivery work.", [
  ("Pre-orders and ship dates", [
    "Batch two ships <span data-ship>the week of [SHIP DATE]</span>. That date is set with a two-week buffer on top of our parts lead time and build schedule. Under the FTC Mail, Internet, or Telephone Order Merchandise Rule (16 CFR Part 435) we must have a reasonable basis for any ship date we advertise, and we do.",
    "If we cannot ship by the stated date, we will email you before it passes with a revised date. You may accept the new date or cancel for a full refund of everything you have paid. If we need a second delay, we will not ship without your express consent.",
    "Batch two is capped at <span data-batch-two-cap>100</span> units. If you reserve after the cap is reached you will be told before paying that you are on the batch three list.",
  ]),
  ("Carriers and transit", [
    "Fixtures ship from Fort Lauderdale, Florida by UPS or USPS Ground in a 13 x 13 x 3 inch double-wall box. Transit is typically 2 to 6 business days in the continental US. Tracking is emailed when the label is created.",
    "Alaska, Hawaii and US territories ship free by USPS; allow extra time. We do not ship internationally during batch two.",
  ]),
  ("Records in transit", [
    "Records travel in their own poly-lined sleeve in a dedicated slot in the tray, separate from the fixture. If a record arrives cracked or warped beyond the condition photographed before shipping, email a photo within 7 days and we will replace it.",
  ]),
])

RETURNS = legal("Returns and refunds", "Deposits refund any time before shipping. Fixtures return within 30 days. Records are a special case, explained below.", [
  ("Deposits", [
    "Your <span data-deposit>$25</span> deposit is fully refundable at any time before your sconce ships, for any reason. Email us or reply to your Stripe receipt. Refunds go back to the original card and typically appear within one billing cycle.",
  ]),
  ("Fixtures", [
    "You have 30 days from delivery to return the fixture for a full refund of the purchase price. It must be unused, undamaged and in its original packaging with all parts (cap, plate, hub, adapter, hardware). Return shipping is deducted from the refund unless the item arrived damaged or was our mistake, in which case we send a prepaid label.",
    "Email us first for a return authorisation and the ship-to address. Refunds are issued within 7 business days of receipt.",
  ]),
  ("Records", [
    "Every record we include is a genuine previously owned pressing, cleaned, graded for display and photographed before it leaves. Because it is a used item, a record is returnable only if it arrives damaged in a way the pre-shipment photo does not show. Label wear, light scuffs and the patina of age are part of the piece and are not defects.",
  ]),
  ("Warranty", [
    "The LED ring, adapter and hub are covered against defects for two years from delivery. Email us with a short video of the fault and we will repair or replace. The adapter is a UL-listed third-party component and also carries its manufacturer's warranty.",
  ]),
])

PRIVACY = legal("Privacy", "What we collect, why, and what we never do with it.", [
  ("What we collect", [
    "If you join the waitlist: your email address and the finish you are leaning toward. If you place a deposit: your name, email, shipping address and payment details, which are processed and stored by Stripe, not by us. We see the last four digits of your card and nothing more.",
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
    "Email us to see, correct or delete what we hold about you. We answer within 30 days. If you are in California, the CCPA gives you these rights by law and we honour them for everyone.",
  ]),
])

TERMS = legal("Terms of sale", "The plain-English rules for pre-ordering and owning a Spindle.", [
  ("Pre-order", [
    "A deposit reserves one unit in the model and finish you select. It is not a purchase of the finished product until we charge the balance, which we do only when your unit is ready to ship and only after emailing you. You may cancel for a full refund at any time before that charge. Our ship-date and delay obligations are described on the <a href='shipping.html'>shipping</a> page.",
  ]),
  ("Pricing", [
    "The balance you pay at ship is the price shown when you placed your deposit, less the deposit. Florida sales tax is added for Florida addresses. Prices for future batches may change; yours does not.",
  ]),
  ("Safety and intended use", [
    "The Spindle is an indoor, dry-location decorative wall light powered by a 12-volt Class 2 adapter. Use only the supplied adapter. Mount it as described in the hang sheet. Do not install it above a heat source or in direct sunlight. Do not place the adapter or its cord inside a wall. In-wall low-voltage cable must be CL2 or better; if you are unsure what your local code permits, ask an electrician.",
  ]),
  ("Your records", [
    "If you mount your own record, you accept that a record hung on a wall is exposed to the room: dust, light and temperature. Our fixture touches it only with felt and does not alter it. We are not responsible for changes to a record caused by its environment.",
  ]),
  ("Intellectual property", [
    "Records we include are genuine previously owned pressings sold under the first-sale doctrine and described factually. <span data-brand>Spindle</span> is not affiliated with, sponsored by or endorsed by any artist, band or record label. We do not reproduce cover art, logos or trademarks. If a rights holder asks us to stop offering a specific title, we will, within two business days.",
  ]),
  ("Limitation", [
    "To the extent the law allows, our liability is limited to the price you paid. Nothing here limits rights you have under consumer protection law that cannot be waived.",
  ]),
])

PAGES = [
  dict(file="index.html", page="home", title="Spindle | Change the record. Change the room.",
       desc="A halo-backlit wall sconce built around a real 12-inch vinyl record. Warm 2700K light, chrome dome, 12-volt plug-in, nothing glued to your vinyl. First batch of 20 sold out; reserve batch two with a $25 refundable deposit.",
       preload='<link rel="preload" as="image" href="img/sq-chrome-1080.webp" imagesrcset="img/sq-chrome-640.webp 640w, img/sq-chrome-1080.webp 1080w" imagesizes="(min-width: 900px) 66vw, 100vw" type="image/webp">\n',
       jsonld=PRODUCT_JSONLD, body=HOME),
  dict(file="product.html", page="product", title="Spindle 12 | Spindle", ogtype="product",
       desc="Configure the Spindle: Kit $89, with a vintage LP $129, named title $179, the Set from $249. Chrome, brass or black. Free US shipping. $25 refundable deposit holds your unit in batch two.",
       jsonld=PRODUCT_JSONLD, body=PRODUCT + STICKY),
  dict(file="install.html", page="install", title="How it works and how to install | Spindle",
       desc="Steel plate, twist-lock hub, in-wall low-voltage cable by default or a surface cord in fifteen minutes. No electrician. Heat numbers included.", body=INSTALL),
  dict(file="faq.html", page="faq", title="FAQ: heat, record safety, wiring, renters, shipping | Spindle",
       desc="Will it warp my record? Is it safe? Do I need an electrician? Can I change the record? Twelve honest answers.", jsonld=FAQ_JSONLD, body=FAQ),
  dict(file="about.html", page="about", title="About | Spindle", desc="Built in Fort Lauderdale by people who could not find a real-record wall light anywhere. Nothing glued to a record, ever.", body=ABOUT),
  dict(file="reserve.html", page="reserve", title="Reserve batch two | Spindle", desc="First batch of 20 sold out. Hold a Spindle from batch two with a $25 refundable deposit, or join the free waitlist.",
       body=RESERVE.replace('<div class="frame dark finish-img">', '<div class="frame dark finish-img" id="reserve-img">', 1) + STICKY),
  dict(file="thanks.html", page="thanks", title="You are on the list | Spindle", desc="Waitlist confirmed.", bodyattrs=' data-thanks="lead"', body=THANKS_LEAD),
  dict(file="thanks-deposit.html", page="thanks", title="Reserved | Spindle", desc="Deposit received.", bodyattrs=' data-thanks="purchase"', body=THANKS_DEPOSIT),
  dict(file="shipping.html", page="legal", title="Shipping | Spindle", desc="Free US shipping, pre-order ship dates and the FTC rule we follow.", body=SHIPPING),
  dict(file="returns.html", page="legal", title="Returns and refunds | Spindle", desc="Deposits refund any time before shipping. Fixtures return within 30 days.", body=RETURNS),
  dict(file="privacy.html", page="legal", title="Privacy | Spindle", desc="What we collect and what we never do with it.", body=PRIVACY),
  dict(file="terms.html", page="legal", title="Terms of sale | Spindle", desc="Plain-English terms for pre-ordering and owning a Spindle.", body=TERMS),
]
