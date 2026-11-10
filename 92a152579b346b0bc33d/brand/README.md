# brand: identity, naming and packaging for the record sconce

Built overnight 2026-11-09 by the brand agent. Nothing registered, nothing ordered, nobody contacted. Every claim with a number or a vendor carries a URL in the file where it is made; estimates are marked.

## Recommendation
**Brand and product: Spindle.** Deadwax is the alternate; Side A drops to third because a live SIDE A registration (class 009/021, protective sleeves for vinyl records) sits on the same shelf as us. Reasons, the eight-name table and the method are in `naming-report.md`. Austin's working name was Side A; all three names are built out so the switch is one line (see "Regenerating").

## What is here
| Path | What | Open |
|---|---|---|
| `brand-guide.html` | One page: name table, mark, lockups, colour, type, photography rules, voice and taglines, packaging previews, references, file index. Google Fonts loaded from the CDN; renders standalone from disk. | Add real photography when the first units are shot. |
| `naming-report.md` | 8 names x USPTO (011/020/035 + 009/021) x .com/.co x Instagram x TikTok, with the recommendation and the lawyer questions. | IP lawyer hour before filing; confirm @spindle on Instagram in the app. |
| `tokens.json`, `tokens.css` | Palette (9 colours, hex), fonts (Google + licensed alternatives), type scale, spacing, radii, rules. | None. |
| `logo/` | Monogram (on light, on dark, one-colour black and white, 512 icon). Wordmarks (caps + editorial italic) and horizontal + stacked lockups for Spindle, Deadwax, Side A. `palette.svg` sheet. All text outlined, no font dependency. | None. |
| `packaging/mailer-13x13x3-outside.svg`, `-inside.svg` | RETT mailer dieline artwork, 25 x 33.5 in flat, kraft B-flute, K + Ember outside, Soot flood + Halo radial on the lid interior. Cut magenta, crease cyan, 0.125 in bleed, 0.25 in safe, legend on sheet. | Re-flow onto the vendor's production dieline PDF (Packlane gives it after choosing options). Drawdown of Ember and Soot on kraft. |
| `packaging/insert-tray.svg` | Two-layer black EPE foam (pulp at volume) tray: dome pocket dead centre, cord and hardware pockets, backplate pocket below, record sleeve under everything. Plan views + centre section with dimensions. | Confirm final hub Ø and backplate Ø with the mounting agent before cutting foam. |
| `packaging/insert-card-front.svg`, `-back.svg` | 5 x 7 uncoated card. Front: mark, wordmark, "Change the record. Change the room." Back: four install steps, QR, the swap ritual, safety paragraph. | QR points at spindlelighting.com/install, a free but unregistered domain. Regenerate after the domain is bought. |
| `packaging/warranty-card.svg` | 3.5 x 5 Soot card, two-year warranty text, serial/finish/date lines. | Warranty terms are a draft; Austin to approve the exclusions. |
| `packaging/sticker-2in-round.svg`, `sticker-finish-labels.svg` | Round seal sticker; 3 x 0.55 in finish labels (Chrome, Brass, Black) so one box SKU serves three finishes. | None. |
| `packaging/spec-sheet.md` | Vendor-ready spec: style, size, board, inks, files, dieline note, quantities, lead times, tray material, card stocks, sticker vendor, unboxing order. Packlane numbers from their live product page; Arka rate-limited the scraper, quote by form. | Instant quote on packlane.com for 100 and 250 units. |
| `preview/` | PNG of every SVG (headless Chrome via `tools/render_previews.sh`). `_check/` holds downscaled copies and two brand-guide screenshots. | None. |
| `tools/` | `svgtext.py` (fontTools text-to-path with GPOS kerning), `gen_brand.py`, `gen_packaging.py`, `render_previews.sh`, `fonts/` (Inter Tight, Instrument Serif, JetBrains Mono TTFs, OFL), `namecheck-results/` (raw USPTO/IG/TikTok JSON + domain RDAP notes + the Playwright script). | None. |

## Regenerating (for a name change or copy edit)
```
cd projects/record-sconces/brand/tools
# edit RECOMMENDED = "spindle" | "deadwax" | "sidea" in gen_brand.py
python3 gen_brand.py && python3 gen_packaging.py && ./render_previews.sh
```
Headless Chrome is at /Applications/Google Chrome.app. No Inkscape or ImageMagick on this box; everything is pure Python + fontTools + Chrome.

## Design decisions in one breath
Lane: premium physical product, warm. References cited in the guide: Schoolhouse (plain object names, stamped wordmark), Rejuvenation (finish-first), Gantri (pulp tray, sconce price band), Tom Dixon Press (one polished part on a matte body), Teenage Engineering (mono spec type, exploded diagrams), Audio-Technica (record culture without album art), Poplight (brand equals product). Token discipline cross-checked against the Apple entry in the local brand library: one accent, near-black ink not pure black, negative tracking at display sizes, then warmed. Palette comes from the reference photo: Vinyl #16130F, Plaster #E9DFCF, Halo #F0A43B, Chrome #C7CBD0. Fonts: Inter Tight, Instrument Serif italic, JetBrains Mono, all Google Fonts.

## House rules honoured
No band names, logos or album art anywhere; labels in renders and artwork are plain or fictional. Written only inside brand/. No sends, no orders, no accounts, no payments. No em-dashes.

## Open items, in priority order
1. Austin picks the name (Spindle recommended). Then register spindlelighting.com, spindle.lighting, @spindlelighting on Instagram and TikTok, same morning.
2. IP lawyer hour: SPINDLE vs the class 020 mattress registration; whether to file SPINDLE or SPINDLE LIGHTING.
3. Packlane instant quote for the custom 13 x 13 x 3 kraft B-flute RETT at 100 and 250, both sides printed; download their dieline and re-flow the panel art.
4. Foam converter quote for the two-layer tray (or Packlane's insert partner); confirm pocket diameters against the final hub and backplate.
5. Shoot the three photographs per finish per the guide, replace the Blender renders in the guide.
