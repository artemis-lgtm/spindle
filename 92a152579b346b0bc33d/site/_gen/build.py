#!/usr/bin/env python3
"""Stamps the shared head/header/footer into each page and writes plain HTML into site/.
Optional: the output files are hand-editable. Run: python3 _gen/build.py (from site/)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from pages import PAGES

BRAND = "Spindle"          # static-tag fallback; js/config.js is the live constant
DOMAIN = "https://example.com"  # PLACEHOLDER for OG urls

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
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
<link rel="preload" as="font" type="font/woff2" href="fonts/jetbrains-mono-latin.woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/style.css">
{preload}{jsonld}<script src="js/config.js"></script>
<script src="js/main.js" defer></script>
</head>
<body data-page="{page}"{bodyattrs}>
<a class="sr-only" href="#main">Skip to content</a>
<div class="bar">First batch of <span data-batch-size>20</span> sold out. Batch two is open for <span data-deposit>$25</span> refundable deposits.</div>
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
        <p style="margin-top:12px;max-width:28em">Wall sconces built around a real 12-inch record. Warm 2700K halo, 12-volt plug-in, nothing glued to your vinyl. Made in Fort Lauderdale, Florida.</p>
        <p><a data-email href="mailto:hello@example.com">hello@example.com</a></p>
      </div>
      <div>
        <h4>Shop</h4>
        <a href="product.html">Spindle 12</a>
        <a href="product.html#kit">Spindle Kit</a>
        <a href="product.html#set">Spindle Set</a>
        <a href="reserve.html">Reserve batch two</a>
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
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
      </div>
    </div>
    <div class="disclaimer">
      <p>Every record we ship is a genuine, previously owned pressing. Label wear is part of the piece. <span data-brand>{brand}</span> is not affiliated with, sponsored by or endorsed by any artist, band or record label. Album names, where they appear, describe the material only. We never reproduce cover art or logos.</p>
      <p>Pre-order terms: deposits are fully refundable at any time before your sconce ships. Batch two ships <span data-ship>the week of [SHIP DATE]</span>. If we cannot ship by then we will tell you and you may cancel for a full refund.</p>
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
            preload=p.get("preload", ""), jsonld=p.get("jsonld", "")
        ) + p["body"] + FOOT.format(brand=BRAND, extra=p.get("extra", ""))
        if "—" in html or "–" in html:
            raise SystemExit("em/en dash found in " + p["file"])
        with open(os.path.join(SITE, p["file"]), "w") as f:
            f.write(html)
        print("wrote", p["file"], len(html), "bytes")

if __name__ == "__main__":
    build()
