// Name conflict checker: USPTO TM search (UI), Instagram + TikTok handle pages.
const { chromium } = require('/Users/artemis/.npm/_npx/e41f203b7505f1fb/node_modules/playwright');
const fs = require('fs');
const names = ['deadwax', 'side a', 'spindle', 'runout', 'lead-in', 'flipside', 'thirty three', 'revolve lighting'];
const handles = ['sidea','sideastudio','sidea.lighting','deadwax','deadwaxlighting','deadwax.studio','spindle','spindlelighting','runout','runoutstudio','leadin','flipside','thirtythree','revolvelighting','zq9x_definitely_not_taken_7731'];
const out = { uspto: {}, instagram: {}, tiktok: {} };
(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/Users/artemis/Library/Caches/ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' });
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36', viewport: { width: 1400, height: 1000 } });
  const page = await ctx.newPage();
  for (const n of names) {
    try {
      await page.goto('https://tmsearch.uspto.gov/search/search-information', { waitUntil: 'networkidle', timeout: 60000 });
      const box = page.getByRole('combobox', { name: 'Search trademarks' });
      await box.fill(n);
      await box.press('Enter');
      await page.waitForFunction(() => /results for/i.test(document.body.innerText), null, { timeout: 60000 });
      await page.waitForTimeout(2500);
      const txt = await page.evaluate(() => document.body.innerText);
      const total = (txt.match(/([\d,]+) results? for/i) || [])[1];
      // parse cards
      const cards = [];
      const re = /Wordmark\n(?:wordmark\n)?([^\n]+)\nStatus\n\n([A-Z]+)\n\nGoods & services\n([^\n]+)\n(?:outbound\n)?Class\n([^\n]+)\nSerial\n(\d+)\nOwners\n([^\n]+)/g;
      let m; while ((m = re.exec(txt))) cards.push({ mark: m[1], status: m[2], goods: m[3], cls: m[4], serial: m[5], owner: m[6] });
      out.uspto[n] = { total, shown: cards.length, cards };
      console.log('USPTO', n, total, cards.length);
    } catch (e) { out.uspto[n] = { error: String(e).slice(0, 200) }; console.log('USPTO fail', n, String(e).slice(0, 120)); }
  }
  for (const h of handles) {
    try {
      const r = await page.goto('https://www.instagram.com/' + h + '/', { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForTimeout(3500);
      const t = await page.evaluate(() => ({ title: document.title, og: (document.querySelector('meta[property="og:title"]') || {}).content || null, desc: (document.querySelector('meta[name="description"]') || {}).content || null, body: document.body.innerText.slice(0, 400) }));
      out.instagram[h] = { http: r && r.status(), ...t, url: page.url() };
      console.log('IG', h, r && r.status(), t.title, '|', (t.og || '').slice(0, 60));
    } catch (e) { out.instagram[h] = { error: String(e).slice(0, 200) }; console.log('IG fail', h); }
  }
  for (const h of handles) {
    try {
      const r = await page.goto('https://www.tiktok.com/@' + h, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForTimeout(3500);
      const t = await page.evaluate(() => ({ title: document.title, og: (document.querySelector('meta[property="og:title"]') || {}).content || null, notfound: /couldn.t find this account/i.test(document.body.innerText), body: document.body.innerText.slice(0, 300) }));
      out.tiktok[h] = { http: r && r.status(), ...t, url: page.url() };
      console.log('TT', h, r && r.status(), t.title, 'notfound=', t.notfound);
    } catch (e) { out.tiktok[h] = { error: String(e).slice(0, 200) }; console.log('TT fail', h); }
  }
  fs.writeFileSync(__dirname + '/namecheck.json', JSON.stringify(out, null, 2));
  await browser.close();
})();
