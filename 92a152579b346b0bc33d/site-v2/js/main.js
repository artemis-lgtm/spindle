/* Spindle: site behaviour. No dependencies. */
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
    if (document.title.indexOf('Spindle |') !== -1 && S.BRAND !== 'Spindle') document.title = document.title.replace(/Spindle \|/g, S.BRAND + ' |');
    var y = document.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();
  }

  /* ---------- Meta pixel wrapper: the ONLY place events leave the page ----------
     Every event goes through track(). It logs to window.SpindlePixel.log (and the console)
     whether or not a real pixel id is set, so the funnel can be tested before the pixel exists.
     Spindle needs its OWN pixel: never paste Ghost Audio's id into config.js. */
  var PIX = window.SpindlePixel = { live: false, log: [] };
  function initPixel() {
    if (isPlaceholder(S.META_PIXEL_ID)) {
      window.fbq = function () {};
    } else {
      /* Standard Meta pixel bootstrap */
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init', S.META_PIXEL_ID);
      PIX.live = true;
    }
    track('PageView');
  }
  function track(name, params, eventID) {
    params = params || {};
    PIX.log.push({ event: name, params: params, eventID: eventID || null, live: PIX.live, t: Date.now() });
    try { if (window.console) console.log(PIX.live ? '[pixel]' : '[pixel placeholder]', name, JSON.stringify(params), eventID || ''); } catch (e) {}
    try { if (eventID) window.fbq('track', name, params, { eventID: eventID }); else window.fbq('track', name, params); } catch (e) {}
  }
  window.track = track;

  /* ---------- Ad attribution: UTM + click ids, first and last touch ---------- */
  var ATTR_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'fbclid', 'gclid', 'ttclid'];
  function readAttr() { try { return JSON.parse(localStorage.getItem('spindle-attr') || 'null') || {}; } catch (e) { return {}; } }
  function captureAttribution() {
    var q, hit = {}, any = false;
    try { q = new URLSearchParams(location.search); } catch (e) { return; }
    ATTR_KEYS.forEach(function (k) { var v = q.get(k); if (v) { hit[k] = v.slice(0, 200); any = true; } });
    var a = readAttr();
    var touch = function () { return Object.assign({ landing_page: location.pathname.split('/').pop() || 'index.html', referrer: (document.referrer || '').slice(0, 300), ts: new Date().toISOString() }, hit); };
    if (!a.first) a.first = touch();
    if (any || !a.last) a.last = touch();
    try { localStorage.setItem('spindle-attr', JSON.stringify(a)); } catch (e) {}
  }
  function cookie(n) { var m = document.cookie.match(new RegExp('(?:^|; )' + n + '=([^;]*)')); return m ? decodeURIComponent(m[1]) : ''; }
  function attributionFields() {
    var a = readAttr(), last = a.last || {}, first = a.first || {}, out = {};
    ATTR_KEYS.forEach(function (k) { out[k] = last[k] || first[k] || ''; });
    out.first_utm_source = first.utm_source || ''; out.first_utm_campaign = first.utm_campaign || '';
    out.landing_page = last.landing_page || first.landing_page || ''; out.referrer = last.referrer || first.referrer || '';
    out.first_seen = first.ts || ''; out.fbp = cookie('_fbp'); out.fbc = cookie('_fbc');
    return out;
  }
  function newEventId(prefix) { return prefix + '-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8); }

  /* ---------- Selection state (shared between home, product, reserve) ---------- */
  var state = { sku: 'sconce', finish: 'chrome', withRecords: false };
  try { var saved = JSON.parse(localStorage.getItem('spindle-sel') || 'null'); if (saved) state = Object.assign(state, saved); } catch (e) {}
  if (!S.SKUS[state.sku] || (state.sku === 'set' && !S.SET_OPEN)) state.sku = 'sconce';
  if (!S.FINISHES[state.finish] || !S.FINISHES_OPEN) state.finish = 'chrome';
  var hashSku = (location.hash || '').slice(1);
  if (S.SKUS[hashSku] && (hashSku !== 'set' || S.SET_OPEN)) state.sku = hashSku;
  var DEMO_PAY = isPlaceholder(S.STRIPE_PAYMENT_LINK);
  function saveState() { try { localStorage.setItem('spindle-sel', JSON.stringify(state)); } catch (e) {} }
  function price() {
    var sku = S.SKUS[state.sku]; if (!sku) return 0;
    return (state.sku === 'set' && state.withRecords) ? sku.priceWithRecords : sku.price;
  }
  function depositUrl() {
    var ref = state.sku + '-' + state.finish + (state.sku === 'set' && state.withRecords ? '-records' : '');
    var base = S.STRIPE_PAYMENT_LINK;
    if (isPlaceholder(base)) return 'thanks-deposit.html?demo=1&ref=' + encodeURIComponent(ref);
    var at = attributionFields(), extra = '';
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) { if (at[k]) extra += '&' + k + '=' + encodeURIComponent(at[k]); });
    return base + (base.indexOf('?') === -1 ? '?' : '&') + 'client_reference_id=' + encodeURIComponent(ref) + extra;
  }
  function wireDepositLinks() {
    document.querySelectorAll('[data-deposit-link]').forEach(function (a) {
      a.href = depositUrl();
      if (a.hasAttribute('data-wired')) return;   /* this runs on every SKU/finish change: one listener per link, one event per click */
      a.setAttribute('data-wired', '');
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
      document.querySelectorAll('[data-price]').forEach(function (p) { p.textContent = '$' + price(); });
      document.querySelectorAll('[data-sku-name]').forEach(function (n) { n.textContent = S.SKUS[state.sku].name; });
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

  /* ---------- Product configurator: size, cap finish, cap ----------
     Buttons carry data-open. An option that is not open yet (not engineered or not quoted) can be looked at,
     never held: picking one swaps the hold button for a waitlist link that says what they wanted. */
  function wireConfig() {
    var box = document.querySelector('[data-config]'); if (!box) return;
    var cfg = { size: '12', finish: 'chrome', cap: 'plain' };
    var groups = box.querySelectorAll('[data-opt-group]');
    var note = box.querySelector('[data-later-note]'), later = box.querySelector('[data-later-link]');
    function showImage(src, alt) {
      var main = document.querySelector('#pdp-main img'); if (!main) return;
      var pic = main.closest('picture'); if (pic) pic.querySelectorAll('source').forEach(function (x) { x.remove(); });
      main.removeAttribute('srcset'); main.removeAttribute('sizes'); main.src = src; if (alt) main.alt = alt;
      var wrap = document.getElementById('pdp-main'); if (wrap) wrap.classList.remove('contain');
      document.querySelectorAll('.thumbs button').forEach(function (b, i) { b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false'); });
    }
    function render(changed) {
      var notes = [], wants = [];
      groups.forEach(function (g) {
        var k = g.getAttribute('data-opt-group');
        g.querySelectorAll('[data-value]').forEach(function (b) {
          var on = b.getAttribute('data-value') === cfg[k];
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
          if (!on) return;
          var l = g.querySelector('[data-opt-label]'); if (l) l.textContent = b.getAttribute('data-label');
          if (b.getAttribute('data-open') !== 'true') { notes.push(b.getAttribute('data-note')); wants.push(k + '-' + cfg[k]); }
          else if (k === 'finish' && S.FINISHES[cfg[k]]) { state.finish = cfg[k]; saveState(); }
        });
      });
      var isLater = notes.length > 0;
      box.classList.toggle('is-later', isLater);
      document.body.classList.toggle('cfg-later', isLater);
      if (note) note.textContent = isLater ? notes.join(' ') + ' Join the free list and we will email you when it opens. Everything else on this page can be held today.' : '';
      if (later) later.href = 'reserve.html?wants=' + encodeURIComponent(wants.join(',')) + '#waitlist-form';
      if (changed === 'finish' || changed === 'cap') {
        if (cfg.cap === 'lit') showImage('img/litcap-sq-1080.webp', 'Rendering of the lit-label cap: a ring of light on the record label. Planned, not built.');
        else showImage('img/sq-' + cfg.finish + '-1080.webp', 'Rendering of the Spindle with a ' + cfg.finish + ' cap, lit, on a warm plaster wall');
        var t0 = document.querySelector('.thumbs button img'); if (t0) t0.src = 'img/sq-' + cfg.finish + '-640.webp';
      }
      wireDepositLinks(); updateSticky();
    }
    groups.forEach(function (g) {
      var k = g.getAttribute('data-opt-group');
      g.querySelectorAll('[data-value]').forEach(function (b) {
        b.addEventListener('click', function () { cfg[k] = b.getAttribute('data-value'); render(k); track('CustomizeProduct', { content_name: k + ': ' + b.getAttribute('data-label') }); });
      });
    });
    render();
  }

  /* ---------- Sticky buy bar (mobile) ---------- */
  function updateSticky() {
    var bar = document.querySelector('.sticky-bar'); if (!bar) return;
    var n = bar.querySelector('[data-sticky-name]'); if (n) n.textContent = S.SKUS[state.sku].name + (S.FINISHES_OPEN ? ', ' + S.FINISHES[state.finish].name : '');
    var p = bar.querySelector('[data-sticky-price]'); if (p) p.textContent = '$' + price() + ' when it ships. $' + S.DEPOSIT_AMOUNT + ' refundable hold today.';
  }
  function wireSticky() {
    var bar = document.querySelector('.sticky-bar'); if (!bar) return;
    document.body.classList.add('has-sticky');
    var anchor = document.querySelector('[data-sticky-anchor]');
    if (!anchor || !('IntersectionObserver' in window)) { bar.classList.add('show'); return; }
    /* the bar is there whenever the main reserve button is off screen, above or below */
    new IntersectionObserver(function (es) { es.forEach(function (e) { bar.classList.toggle('show', !e.isIntersecting); }); }, { threshold: 0 }).observe(anchor);
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
    /* the product is visible from the first frame (dim), then the room comes up. Never a black box. */
    setLevel(reduce ? 1 : 0.32);
    if (reduce) armed = true;
    /* turn on when the page is scrolled or the hero is tapped, or by itself after 0.7s */
    window.addEventListener('scroll', turnOn, { passive: true, once: true });
    hero.addEventListener('pointerdown', function (e) { if (e.target.closest('a,button,input,label')) return; if (armed) { setLevel(level > 0.5 ? 0.12 : 1); } else turnOn(); });
    setTimeout(turnOn, 700);
    if (range) {
      range.addEventListener('input', function () { armed = true; setLevel(range.value / 100, true); });
      range.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
    }
  }

  /* ---------- Waitlist form ----------
     Posts JSON to WAITLIST_FORM_ACTION (our /api/waitlist on Vercel, or any endpoint that accepts JSON,
     Formspree included). Placeholder = demo: nothing is sent, the payload is kept in sessionStorage
     ('spindle-wl-demo') so the funnel can be checked, and thanks.html shows the TEST MODE banner.
     Lead fires ONCE, on thanks.html, and only after a real submit from this browser. */
  var WANT_NAMES = { 'size-7': 'the 7 inch size', 'finish-brass': 'the brass cap', 'finish-black': 'the black cap', 'cap-lit': 'the lit-label cap' };
  function wantsParam() {
    var w = ''; try { w = new URLSearchParams(location.search).get('wants') || ''; } catch (e) {}
    return w.split(',').filter(function (k) { return WANT_NAMES[k]; }).join(',');
  }
  function wireWaitlist() {
    var f = document.getElementById('waitlist-form'); if (!f) return;
    var asked = wantsParam(), wn = document.querySelector('[data-wants-note]');
    if (asked && wn) { wn.textContent = 'You asked about ' + asked.split(',').map(function (k) { return WANT_NAMES[k]; }).join(' and ') + '. Join the list below and we will email you when it opens.'; wn.style.display = 'block'; }
    var demo = isPlaceholder(S.WAITLIST_FORM_ACTION), busy = false;
    f.addEventListener('submit', function (e) {
      e.preventDefault(); if (busy) return;
      var email = f.querySelector('input[type=email]'), consent = f.querySelector('input[name=consent]'), err = document.getElementById('wl-err'), fail = document.getElementById('wl-fail');
      var trap = f.querySelector('input[name=_gotcha]'), version = f.querySelector('[name=version]'), btn = f.querySelector('button[type=submit]');
      if (fail) fail.hidden = true;
      if (!email || !email.value || !email.validity.valid || (consent && !consent.checked)) {
        if (err) err.hidden = false; (email && (!email.value || !email.validity.valid) ? email : consent).focus(); return;
      }
      if (err) err.hidden = true;
      if (trap && trap.value) { location.href = 'thanks.html'; return; }   /* bot: look successful, record nothing */
      var id = newEventId('lead'), wants = wantsParam();
      var payload = Object.assign({ email: email.value.trim(), interest: (version ? version.value : '') + (wants ? ' | wants: ' + wants : ''), consent: true, page: location.pathname.split('/').pop() || 'index.html', event_id: id }, attributionFields());
      var done = function (q) { try { sessionStorage.setItem('spindle-lead-pending', id); } catch (x) {} location.href = 'thanks.html' + (q || ''); };
      if (demo) { try { sessionStorage.setItem('spindle-wl-demo', JSON.stringify(payload)); } catch (x) {} done('?demo=1'); return; }
      busy = true; if (btn) btn.disabled = true;
      fetch(S.WAITLIST_FORM_ACTION, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); done(''); })
        .catch(function () { busy = false; if (btn) btn.disabled = false; if (fail) fail.hidden = false; });
    });
  }

  /* ---------- Thanks pages fire the conversion events (once each) ---------- */
  function wireThanks() {
    var t = document.body.getAttribute('data-thanks'); if (!t) return;
    var qs = location.search, demo = /[?&]demo=1/.test(qs), sid = (qs.match(/[?&]session_id=([^&]+)/) || [])[1];
    if (t === 'lead') {
      var lid = null; try { lid = sessionStorage.getItem('spindle-lead-pending'); sessionStorage.removeItem('spindle-lead-pending'); } catch (e) {}
      if (lid) track('Lead', { content_name: 'waitlist', content_category: 'waitlist' }, lid);
    }
    if (demo) document.querySelectorAll('[data-demo-banner]').forEach(function (el) { el.hidden = false; });
    if (t === 'purchase' && !demo && !sid) {
      /* someone opened this page without paying: never tell them a deposit is in, never fire Purchase */
      document.querySelectorAll('[data-has-session]').forEach(function (el) { el.hidden = true; });
      document.querySelectorAll('[data-no-session]').forEach(function (el) { el.hidden = false; });
      return;
    }
    if (t === 'purchase' && sid) {
      var key = 'spindle-purchase-' + sid, seen = false;
      try { seen = !!localStorage.getItem(key); localStorage.setItem(key, '1'); } catch (e) {}
      if (!seen) track('Purchase', { value: S.DEPOSIT_AMOUNT, currency: 'USD', content_name: 'batch-two-deposit', content_type: 'product', contents: [{ id: state.sku + '-' + state.finish, quantity: 1 }] }, 'dep-' + sid);
    }
    var sel = document.querySelector('[data-thanks-selection]');
    if (sel) sel.textContent = S.SKUS[state.sku].name + (S.FINISHES_OPEN ? ' in ' + S.FINISHES[state.finish].name : '');
  }

  /* ---------- Misc ---------- */
  function wireNav() {
    var btn = document.querySelector('.menu-btn'), nav = document.querySelector('.mobile-nav');
    if (btn && nav) {
      var setOpen = function (o) { nav.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); };
      btn.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
      nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    }
    var here = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav a, .mobile-nav a, .policy-nav a').forEach(function (a) { if (a.getAttribute('href') === here) a.setAttribute('aria-current', 'page'); });
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
        main.removeAttribute('srcset'); main.removeAttribute('sizes'); main.src = src;
        g.querySelector('.main').classList.toggle('contain', b.hasAttribute('data-contain'));
        main.alt = b.querySelector('img').alt;
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyBrand(); captureAttribution(); initPixel(); wireNav(); wireHero(); wireSwatches(); wireSkus(); wireGallery(); wireConfig(); wireSticky(); wireDepositLinks(); wireWaitlist(); wireThanks(); wireReveal(); updateSticky();
    if (document.body.getAttribute('data-page') === 'product') track('ViewContent', { content_name: S.SKUS[state.sku].name, value: price(), currency: 'USD' });
  });
})();
