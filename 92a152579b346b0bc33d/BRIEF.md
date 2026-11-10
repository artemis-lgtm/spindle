# Record Sconces: master brief for the overnight build (2026-11-09 night)

## History (from the record, read the files)
- NOTES.md: every decision Austin made today, in order. READ IT FULLY FIRST.
- scope-report.md (market, costs, legal, ads math), engineering-report.md (mount, LED, heat, BOM),
  design-report.md (29 best-selling sconces, trends, finishes, naming, price ladder),
  mounting-report.md (steel wall plate + twist-lock hub + in-wall CL2 wiring).
- refs/austin-reference-1.jpg (THE look: records with warm amber halo, 12" + two 7"),
  refs/austin-reference-2-tomdixon-press.jpg (chrome dome cap reference, Tom Dixon Press $755).
- render/: sconce.py + sconce_v2.py (Blender, CYCLES), PNGs of chrome/brass/black heroes, exploded, cutaway, rear.

## The product (decided)
- Halo-backlit wall sconce built around a real 12" vinyl LP (7" single variant). Warm 2700K COB LED ring on the rim
  of a ~10.5" backplate throws a halo on the wall. 12V Class 2 from a UL-listed adapter. Nothing 120V inside.
- Customer's own record screws on with a mirror-CHROME DOME cap (brass and gloss black variants) on a 1/4-20 post
  through the spindle hole into a brass insert. Felt washer. Nothing glued to customer records.
- Wall: steel mounting plate (fits box or anchors), hub twist-locks on, set screw. Wiring BEHIND THE WALL is the
  default (CL2 cable inside the wall down to an outlet-height jack plate); surface cord + raceway is option B.
- SKUs: Kit (no record, customer's own) ~$89; Sconce with a vintage record $129; named title $179;
  3-piece Set (12" + two 7") ~$249 kit / $329 with records. 20 units already sold (first batch sold out, real).
- Legal: NO band names, logos, or album art in our marketing or renders. Use plain/fictional labels.
- Brand name not final. Candidates: "Spindle" product, brand "Deadwax" or "Side A". Check before using.

## House rules for every agent
- Write ONLY inside your own folder listed in your task. Do not edit other agents' folders or NOTES.md.
- Every claim about a product, vendor, price, or "best seller": cite a URL. Mark estimates as estimates.
  Use references from proven, best-selling, top-converting examples, as Austin demanded.
- Realistic and doable: real vendors that take small orders from a US small business, real prices, real lead times.
- Do NOT send emails/messages/Telegram, do NOT place orders, do NOT create accounts, do NOT pay anything.
  Draft outbound messages to files only.
- Blender: /Applications/Blender.app/Contents/MacOS/Blender -b -P script.py, CYCLES only (never EEVEE).
  Long renders run detached (nohup ... & disown, absolute PATH). Never /tmp.
- Plain prose, no em-dashes. Finish with a README.md in your folder: what you made, where, what's open.
