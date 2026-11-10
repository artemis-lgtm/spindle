/* Side A / The Spindle: site behaviour. No dependencies. */
(function () {
  'use strict';
  var S = window.SITE || {};
  var isPlaceholder = function (v) { return !v || /REPLACE|example\.com|\[/.test(String(v)); };

  /* ---------- Brand substitution: one constant, every page ---------- */
  function applyBrand() {
    document.querySelectorAll('[data-brand]').forEach(function (el) { el.textContent = S.BRAND; });
    document.querySelectorAll('[data-product]').forEach(function (el) { el.textContent = S.PRODUCT; });
    document.querySelectorAll('[data-kit]').forEach(function (el) { el.textContent = S.KIT; });
    document.querySelectorAll('[data-ship]').forEach(function (el) { el.textContent = S.SHIP_WINDOW; });
    document.querySelectorAll('[data-email]').forEach(function (el) { el.textContent = S.CONTACT_EMAIL; if (el.tagName === 'A') el.href = 'mailto:' + S.CONTACT_EMAIL; });
    document.querySelectorAll('[data-batch-size]').forEach(function (el) { el.textContent = S.FIRST_BATCH_SIZE; });
    document.querySelectorAll('[data-batch-two-cap]').forEach(function (el) { el.textContent = S.BATCH_TWO_CAP; });
    document.querySelectorAll('[data-deposit]').forEach(function (el) { el.textContent = '$' + S.DEPOSIT_AMOUNT; });
    document.querySelectorAll('[data-sold-date]').forEach(function (el) { el.textContent = S.FIRST_BATCH_SOLD_OUT_DATE ? ' in ' + S.FIRST_BATCH_SOLD_OUT_DATE : ''; });
    if (document.title.indexOf('Spindle |') !== -1 && S.BRAND !== 'Spindle') document.title = document.title.replace(/Spindle \|/g, S.BRAND + ' |');
    var y = document.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();
  }

  /* ---------- Meta pixel wrapper ---------- */
  function initPixel() {
    if (isPlaceholder(S.META_PIXEL_ID)) {
      window.fbq = function () { if (window.console) console.log('[pixel placeholder]', Array.prototype.slice.call(arguments)); };
      window.fbq('init', 'PLACEHOLDER'); window.fbq('track', 'PageView');
      return;
    }
    /* Standard Meta pixel bootstrap */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', S.META_PIXEL_ID);
    window.fbq('track', 'PageView');
  }
  function track(name, params) { try { window.fbq && window.fbq('track', name, params || {}); } catch (e) {} }
  window.track = track;

  /* ---------- Selection state (shared between home, product, reserve) ---------- */
  var state = { sku: 'sconce', finish: 'chrome', withRecords: false };
  try { var saved = JSON.parse(localStorage.getItem('spindle-sel') || 'null'); if (saved) state = Object.assign(state, saved); } catch (e) {}
  function saveState() { try { localStorage.setItem('spindle-sel', JSON.stringify(state)); } catch (e) {} }
  function price() {
    var sku = S.SKUS[state.sku]; if (!sku) return 0;
    return (state.sku === 'set' && state.withRecords) ? sku.priceWithRecords : sku.price;
  }
  function depositUrl() {
    var ref = state.sku + '-' + state.finish + (state.sku === 'set' && state.withRecords ? '-records' : '');
    var base = S.STRIPE_PAYMENT_LINK;
    if (isPlaceholder(base)) return 'thanks-deposit.html?demo=1&ref=' + encodeURIComponent(ref);
    return base + (base.indexOf('?') === -1 ? '?' : '&') + 'client_reference_id=' + encodeURIComponent(ref);
  }
  function wireDepositLinks() {
    document.querySelectorAll('[data-deposit-link]').forEach(function (a) {
      a.href = depositUrl();
      a.addEventListener('click', function () {
        track('InitiateCheckout', { content_name: S.SKUS[state.sku].name + ' ' + S.FINISHES[state.finish].name, content_category: 'deposit', value: S.DEPOSIT_AMOUNT, currency: 'USD' });
        saveState();
      });
    });
  }

  /* ---------- Finish swatches: swap images ---------- */
  function wireSwatches() {
    var groups = document.querySelectorAll('[data-swatch-group]');
    groups.forEach(function (g) {
      var targets = document.querySelectorAll(g.getAttribute('data-swatch-group'));
      var nameEl = g.parentNode.querySelector('.swatch-name');
      function set(finish, animate) {
        state.finish = finish; saveState();
        g.querySelectorAll('.swatch').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-finish') === finish ? 'true' : 'false'); });
        if (nameEl) nameEl.textContent = S.FINISHES[finish].name;
        targets.forEach(function (t) {
          var tpl = t.getAttribute('data-src-tpl'); if (!tpl) return;
          var wrap = t.closest('.finish-img');
          var swapNow = function () {
            t.querySelectorAll('source').forEach(function (s) { s.srcset = s.getAttribute('data-srcset-tpl').replace(/\{finish\}/g, finish); });
            var img = t.querySelector('img') || t;
            img.src = tpl.replace(/\{finish\}/g, finish);
            if (img.getAttribute('data-srcset-tpl')) img.srcset = img.getAttribute('data-srcset-tpl').replace(/\{finish\}/g, finish);
          };
          if (wrap && animate) { wrap.classList.add('fading'); setTimeout(function () { swapNow(); wrap.classList.remove('fading'); }, 180); } else swapNow();
        });
        document.querySelectorAll('[data-finish-name]').forEach(function (el) { el.textContent = S.FINISHES[finish].name; });
        var th = document.querySelectorAll('.thumbs button'); if (th.length) { th.forEach(function (b, i) { b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false'); }); }
        wireDepositLinks(); updateSticky();
      }
      g.querySelectorAll('.swatch').forEach(function (b) {
        b.addEventListener('click', function () { set(b.getAttribute('data-finish'), true); });
      });
      set(state.finish, false);
    });
  }

  /* ---------- SKU picker (product page) ---------- */
  function wireSkus() {
    var list = document.querySelector('.skus'); if (!list) return;
    var recToggle = document.getElementById('set-records');
    function render() {
      list.querySelectorAll('.sku').forEach(function (l) {
        var v = l.querySelector('input').value; var on = v === state.sku;
        l.classList.toggle('selected', on); l.querySelector('input').checked = on;
      });
      var p = document.querySelector('[data-price]'); if (p) p.textContent = '$' + price();
      var n = document.querySelector('[data-sku-name]'); if (n) n.textContent = S.SKUS[state.sku].name;
      var setOpts = document.getElementById('set-options'); if (setOpts) setOpts.hidden = state.sku !== 'set';
      document.querySelectorAll('[data-includes]').forEach(function (el) { el.hidden = el.getAttribute('data-includes') !== state.sku; });
      wireDepositLinks(); updateSticky(); saveState();
    }
    list.querySelectorAll('input').forEach(function (r) {
      r.addEventListener('change', function () { state.sku = r.value; render(); track('ViewContent', { content_name: S.SKUS[state.sku].name, value: price(), currency: 'USD' }); });
    });
    if (recToggle) { recToggle.checked = !!state.withRecords; recToggle.addEventListener('change', function () { state.withRecords = recToggle.checked; render(); }); }
    render();
  }

  /* ---------- Sticky buy bar (mobile) ---------- */
  function updateSticky() {
    var bar = document.querySelector('.sticky-bar'); if (!bar) return;
    var n = bar.querySelector('[data-sticky-name]'); if (n) n.textContent = S.SKUS[state.sku].name + ', ' + S.FINISHES[state.finish].name;
    var p = bar.querySelector('[data-sticky-price]'); if (p) p.textContent = '$' + price() + ' at ship. ' + '$' + S.DEPOSIT_AMOUNT + ' refundable deposit today.';
  }
  function wireSticky() {
    var bar = document.querySelector('.sticky-bar'); if (!bar) return;
    document.body.classList.add('has-sticky');
    var anchor = document.querySelector('[data-sticky-anchor]');
    if (!anchor || !('IntersectionObserver' in window)) { bar.classList.add('show'); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { bar.classList.toggle('show', !e.isIntersecting && e.boundingClientRect.top < 0); }); }, { threshold: 0 }).observe(anchor);
  }

  /* ---------- Hero: the room turns on ---------- */
  function wireHero() {
    var hero = document.querySelector('.hero'); if (!hero) return;
    var range = hero.querySelector('input[type=range]');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var level = 0, armed = false;
    function setLevel(v, user) {
      level = Math.max(0, Math.min(1, v));
      hero.style.setProperty('--on', level.toFixed(3));
      hero.classList.toggle('is-on', level > 0.15);
      if (range && !user) range.value = Math.round(level * 100);
    }
    function turnOn() { if (armed) return; armed = true; setLevel(1); }
    setLevel(reduce ? 1 : 0);
    if (reduce) armed = true;
    /* turn on when the page is scrolled or the hero is tapped; fall back after 2.8s so no one stares at a black box */
    window.addEventListener('scroll', turnOn, { passive: true, once: true });
    hero.addEventListener('pointerdown', function (e) { if (e.target.closest('a,button,input,label')) return; if (armed) { setLevel(level > 0.5 ? 0.12 : 1); } else turnOn(); });
    setTimeout(turnOn, 2800);
    if (range) {
      range.addEventListener('input', function () { armed = true; setLevel(range.value / 100, true); });
      range.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
    }
  }

  /* ---------- Waitlist form ---------- */
  function wireWaitlist() {
    var f = document.getElementById('waitlist-form'); if (!f) return;
    var demo = isPlaceholder(S.WAITLIST_FORM_ACTION);
    if (!demo) { f.action = S.WAITLIST_FORM_ACTION; f.method = 'POST'; }
    var nxt = f.querySelector('input[name=_next]'); if (nxt) nxt.value = location.origin + location.pathname.replace(/[^/]*$/, '') + 'thanks.html';
    f.addEventListener('submit', function (e) {
      var email = f.querySelector('input[type=email]');
      if (!email || !email.validity.valid) return;
      track('Lead', { content_name: 'waitlist', content_category: 'waitlist' });
      try { localStorage.setItem('spindle-waitlist', JSON.stringify({ email: email.value, finish: state.finish, sku: state.sku, t: Date.now() })); } catch (err) {}
      if (demo) { e.preventDefault(); location.href = 'thanks.html?demo=1'; }
    });
  }

  /* ---------- Thanks pages fire the conversion events ---------- */
  function wireThanks() {
    var t = document.body.getAttribute('data-thanks'); if (!t) return;
    if (t === 'lead') track('Lead', { content_name: 'waitlist', status: 'confirmed' });
    if (t === 'purchase') track('Purchase', { value: S.DEPOSIT_AMOUNT, currency: 'USD', content_name: 'batch-two-deposit', content_type: 'product', contents: [{ id: state.sku + '-' + state.finish, quantity: 1 }] });
    var sel = document.querySelector('[data-thanks-selection]');
    if (sel) sel.textContent = S.SKUS[state.sku].name + ' in ' + S.FINISHES[state.finish].name;
  }

  /* ---------- Misc ---------- */
  function wireNav() {
    var btn = document.querySelector('.menu-btn'), nav = document.querySelector('.mobile-nav');
    if (btn && nav) btn.addEventListener('click', function () { var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); });
    var here = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav a, .mobile-nav a').forEach(function (a) { if (a.getAttribute('href') === here) a.setAttribute('aria-current', 'page'); });
  }
  function wireReveal() {
    var els = document.querySelectorAll('.reveal'); if (!els.length) return;
    if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (e) { io.observe(e); });
    /* safety net: nothing stays hidden, whatever the browser does with observers */
    setTimeout(function () { els.forEach(function (e) { e.classList.add('in'); }); }, 1800);
  }
  function wireGallery() {
    var g = document.querySelector('.gallery'); if (!g) return;
    var main = g.querySelector('.main img');
    g.querySelectorAll('.thumbs button').forEach(function (b) {
      b.addEventListener('click', function () {
        g.querySelectorAll('.thumbs button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        var src = b.getAttribute('data-full');
        if (b.hasAttribute('data-finish-img')) { src = src.replace(/\{finish\}/g, state.finish); main.closest('picture') && main.closest('picture').setAttribute('data-src-tpl', b.getAttribute('data-full')); }
        var pic = main.closest('picture'); if (pic) pic.querySelectorAll('source').forEach(function (s) { s.remove(); });
        main.removeAttribute('srcset'); main.src = src;
        main.alt = b.querySelector('img').alt;
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyBrand(); initPixel(); wireNav(); wireHero(); wireSwatches(); wireSkus(); wireGallery(); wireSticky(); wireDepositLinks(); wireWaitlist(); wireThanks(); wireReveal(); updateSticky();
    if (document.body.getAttribute('data-page') === 'product') track('ViewContent', { content_name: S.SKUS[state.sku].name, value: price(), currency: 'USD' });
  });
})();
