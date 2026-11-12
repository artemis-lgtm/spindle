#!/usr/bin/env python3
"""Stamps the shared head/header/footer into each page and writes plain HTML into site/.
Optional: the output files are hand-editable. Run: python3 _gen/build.py (from site/)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from pages import PAGES, PRICES, SET_OPEN, SHIPPING_LINE

BRAND = "Spindle"          # static-tag fallback; js/config.js is the live constant
DOMAIN = "https://example.com"  # PLACEHOLDER for OG urls

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">{robots}
<link rel="canonical" href="{domain}/{file}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{brand}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{domain}/{file}">
<meta property="og:image" content="{domain}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{domain}/img/og.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="fonts/inter-tight-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/instrument-serif-italic-latin.woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/style.css">
{preload}{jsonld}<script src="js/config.js"></script>
<script src="js/main.js" defer></script>
<noscript><style>.reveal{{opacity:1;transform:none}}</style></noscript>
</head>
<body data-page="{page}"{bodyattrs}>
<a class="sr-only" href="#main">Skip to content</a>
<div class="bar">First <span data-batch-size>20</span> sold out. Batch two: <span data-deposit>$25</span> refundable hold.</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="{brand} home"><span class="mark" aria-hidden="true"></span><span data-brand>{brand}</span></a>
    <nav class="nav" aria-label="Primary">
      <a href="product.html">Spindle 12</a>
      <a href="install.html">How it works</a>
      <a href="faq.html">FAQ</a>
      <a href="about.html">About</a>
    </nav>
    <div class="header-cta"><a class="btn btn-primary" href="reserve.html">Reserve batch two</a></div>
    <button class="menu-btn" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile">
    <a href="product.html">Spindle 12</a>
    <a href="install.html">How it works</a>
    <a href="faq.html">FAQ</a>
    <a href="about.html">About</a>
    <a href="reserve.html">Reserve batch two</a>
  </nav>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a href="index.html" aria-label="{brand} home"><img class="footer-lockup" src="img/lockup-horizontal.svg" alt="{brand}" width="546" height="158" loading="lazy"></a>
        <p class="tagline" style="margin-top:14px">Change the record. <em>Change the room.</em></p>
        <p class="slogan-foot">YOUR favorite records light up YOUR favorite room</p>
        <p style="margin-top:12px;max-width:28em">A wall light built around a real 12-inch record. Warm glow, low-voltage plug-in, nothing glued to your vinyl. Designed and assembled in Fort Lauderdale, Florida.</p>
        <p><a data-email href="mailto:hello@example.com">hello@example.com</a></p>
      </div>
      <div>
        <h4>Shop</h4>
        <a href="product.html">Spindle 12</a>
        <a href="product.html#kit">Spindle Kit</a>
{setlink}        <a href="reserve.html">Reserve batch two</a>
      </div>
      <div>
        <h4>Learn</h4>
        <a href="install.html">How it works</a>
        <a href="install.html#in-wall">In-wall install</a>
        <a href="faq.html">FAQ</a>
        <a href="about.html">About</a>
      </div>
      <div>
        <h4>Policies</h4>
        <a href="shipping.html">Shipping</a>
        <a href="returns.html">Returns</a>
        <a href="warranty.html">Warranty</a>
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
      </div>
    </div>
    <div class="disclaimer">
      <p>Every record we supply is a real, previously owned pressing. Label wear is part of the piece. <span data-brand>{brand}</span> is not affiliated with, sponsored by or endorsed by any artist, band or record label. Album names, where they appear, describe the material only. We never reproduce cover art or logos.</p>
      <p>Pre-order terms: this is a pre-order for a product that has not been built yet. Deposits are fully refundable at any time before your sconce ships. Batch two is planned to ship <span data-ship>the week of [SHIP DATE]</span>, which is an estimate. If we cannot ship by then we will tell you first and you may cancel for a full refund. Images are computer renderings. The Spindle is not UL listed; its plug-in power adapter is.</p>
      <p>&copy; <span data-year>2026</span> <span data-brand>{brand}</span>. All rights reserved. <span class="mono" style="color:var(--ash)">Change the record. Change the room.</span></p>
    </div>
  </div>
</footer>
{extra}
</body>
</html>
"""

def build():
    for p in PAGES:
        html = HEAD.format(
            title=p["title"], desc=p["desc"], domain=DOMAIN, file=p["file"], brand=BRAND,
            ogtype=p.get("ogtype", "website"), page=p["page"], bodyattrs=p.get("bodyattrs", ""),
            preload=p.get("preload", ""), jsonld=p.get("jsonld", ""),
            robots=('\n<meta name="robots" content="%s">' % p["robots"]) if p.get("robots") else ""
        ) + p["body"] + FOOT.format(brand=BRAND, extra=p.get("extra", ""),
            setlink='        <a href="product.html#set">Spindle Set</a>\n' if SET_OPEN else "")
        if "—" in html or "–" in html:
            raise SystemExit("em/en dash found in " + p["file"])
        with open(os.path.join(SITE, p["file"]), "w") as f:
            f.write(html)
        print("wrote", p["file"], len(html), "bytes")

def sync_config():
    """Prices live in pages.py. Push them into js/config.js so the live picker can never disagree with the pages."""
    path = os.path.join(SITE, "js", "config.js")
    s = open(path).read()
    def sub(pattern, value):
        nonlocal s
        s, n = re.subn(pattern, lambda m: m.group(1) + str(value), s, count=1)
        if n != 1:
            raise SystemExit("config.js sync failed for " + pattern)
    sub(r"(kit:\s*\{[^}]*?price:\s*)\d+", PRICES["kit"])
    sub(r"(sconce:\s*\{[^}]*?price:\s*)\d+", PRICES["sconce"])
    sub(r"(named:\s*\{[^}]*?price:\s*)\d+", PRICES["named"])
    sub(r"(set:\s*\{[^}]*?price:\s*)\d+", PRICES["set"])
    sub(r"(priceWithRecords:\s*)\d+", PRICES["set_records"])
    sub(r"(DEPOSIT_AMOUNT:\s*)\d+", PRICES["deposit"])
    sub(r"(SET_OPEN:\s*)(?:true|false)", "true" if PRICES["set_open"] else "false")
    sub(r"(FINISHES_OPEN:\s*)(?:true|false)", "true" if PRICES["finishes_open"] else "false")
    open(path, "w").write(s)
    print("synced js/config.js prices:", PRICES)

def launch_check():
    """python3 _gen/build.py --launch-check : exits 1 while anything a customer would see is still a placeholder."""
    cfg = open(os.path.join(SITE, "js", "config.js")).read()
    blockers = []
    def val(key):
        m = re.search(key + r":\s*'([^']*)'", cfg); return m.group(1) if m else ""
    if "[" in val("SHIP_WINDOW"): blockers.append("SHIP_WINDOW is still a placeholder: every page prints '[SHIP DATE]' (FTC rule needs a date with a reasonable basis)")
    if "REPLACE" in val("STRIPE_PAYMENT_LINK"): blockers.append("STRIPE_PAYMENT_LINK is a placeholder: the reserve button takes no money and lands on a TEST MODE page")
    if "REPLACE" in val("WAITLIST_FORM_ACTION"): blockers.append("WAITLIST_FORM_ACTION is a placeholder: waitlist emails are saved nowhere")
    if "example.com" in val("CONTACT_EMAIL"): blockers.append("CONTACT_EMAIL is hello@example.com: refunds are promised by email to an address that does not exist")
    if "REPLACE" in val("META_PIXEL_ID"): blockers.append("META_PIXEL_ID is a placeholder: ads cannot be measured")
    if "example.com" in DOMAIN: blockers.append("DOMAIN in _gen/build.py is example.com: canonical, og:image and JSON-LD urls are wrong")
    for b in blockers: print("LAUNCH BLOCKER:", b)
    print("launch check:", "PASS" if not blockers else "%d blockers, do not deploy" % len(blockers))
    return 1 if blockers else 0

if __name__ == "__main__":
    if "--launch-check" in sys.argv:
        raise SystemExit(launch_check())
    build(); sync_config()
