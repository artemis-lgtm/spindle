# Record player wall sconces (Austin, started 2026-11-09)

## What he wants
- Wall sconces made from vinyl records ("record player wall sconces"). Website + Facebook/Meta ads, launch Tue 2026-11-10.
- Demand-test first: run ads to a waitlist, build to at least 100 people, THEN order parts. "That way we know we're profitable from the get-go."
- 10:00 AM ET 11/10 reminder is set (scheduled-tasks id record-player-sconces-remind-1110).

## Decisions / positions so far (11/9)
- NO printed band logos/album art (e.g. Led Zeppelin sticker) = trademark + copyright infringement. Legal path: real original pressings, factual description ("made from an original pressing of Led Zeppelin IV"), our own design, no "official"/"limited edition <band>" framing. IP lawyer hour before it becomes a line.
- Austin wanted the ad to say "sold out, join the backorder waitlist". I pushed back (false claim in ads, Meta/FTC risk, zero extra sales vs honest version). He said "Ok sounds good". Use: "first batch of 100, made to order, join the waitlist".
- My recommendation: refundable deposit / real pre-order with ship date instead of free email waitlist (free signups convert ~1 in 10). Not yet confirmed by Austin; build both options, default to deposit pre-order if he agrees.

## Tomorrow (Tue 11/10) — what I need to do
1. Read the Fable scoping report (projects/record-sconces/scope-report.md) and turn it into a plan.
2. Ask Austin: brand name, the look (photo of a sconce he likes), price point, deposit vs free waitlist.
3. Build the landing page + waitlist/pre-order checkout (GitHub Pages pattern or Vercel), pixel on it.
4. Meta ad: honest "first batch" copy, small test budget (Ghost Audio precedent: $8/day audition, pixel first).
5. Parts list + per-unit cost from the scope report; order nothing until the 100.

## 2026-11-09 20:2x ET — Austin overruled: "we want to go the sold out version"
- His call stands on the look and urgency of "SOLD OUT, join the waitlist".
- My line: I won't write a flat false "sold out" for something never sold. Plan to make it TRUE: release a tiny real first drop (e.g. 10-20 units / deposits, friends + a soft post) on day one, let it actually sell out, THEN the ads run "First drop sold out. Join the waitlist for the next batch." Page shows the sold-out drop as real.
- 2026-11-09 20:2x ET UPDATE: Austin says they ALREADY SOLD 20. So "sold out" is true. Ad copy: "First batch of 20 sold out. Join the waitlist for the next one." Need from Austin tomorrow: who the 20 buyers are + what they paid (they're the first fulfillment list).
- 2026-11-09 Fable scope report landed: projects/record-sconces/scope-report.md (read it first at 10am). Its "make sold-out true with a tiny first drop" section is superseded by Austin's 20 already sold. Headline numbers: parts ~$28-35/unit at qty 1, $15-22 at 100; price $129 base / $179 named title, $25 refundable deposit; Stripe Payment Link + static page + pixel fastest; 100 deposits ~ $3.9k ad spend over 4-6 wks.

## 2026-11-09 ~15:3x ET — NEW SKU: light-only kit (Austin)
- Sell the light fixture separately so people mount THEIR OWN record. Austin's idea.
- My take: yes, strong. No record cost, no trademark exposure at all (their record, their choice), and it beats the $27-66 "Now Playing" display shelves on looks.
- Design consequence: NO epoxy/VHB on a customer's record. Needs a non-destructive mount (spindle-hole post + soft edge clips) so the record swaps in and out. Swappable = a selling point ("change the record, change the room").
- Price idea: ~$79 kit (parts ~$15-22 at qty 100, ship lighter/cheaper, no record, no labeling risk). Bundle with the full $129 sconce stays the hero; kit is the second ad set / upsell for collectors.
- Tomorrow: add the kit to the landing page as a second option + its own Stripe link; confirm price with Austin.
- Austin's mount (11/9): screw-on system. Brass-head thumbscrew through the record's center hole into the backplate. Spec: LP spindle hole is 0.286" (7.26mm), so a 1/4" (6.35mm) bolt into a threaded insert in the backplate, felt washer under the brass cap so it grips without scratching the label. Standoff sleeve behind the record keeps the halo gap. Same mount on the full sconce too.
- 11/9 Austin reference image: refs/austin-reference-1.jpg (12" center + two 7" singles, warm halo behind each, small brass base mounts on the 7"s). His spec: light behind the record like that, plus a BRASS or BLACK CONE on the front center that screws the customer's record on. Cone = the visible hero hardware.
- (done 11/9) engineering-report.md landed; design + best-sellers Fable agent SPAWNED -> design-report.md. Engineering flags kit at $79 is thin (~$34 contribution); suggests $89-99. BOM ~$27 @100.
- 11/9 cap reference: refs/austin-reference-2-tomdixon-press.jpg (Tom Dixon Press Surface Light, $755 at DWR). Cap = polished CHROME low dome / mirror half-sphere in the center, threaded, sits on the outside of the vinyl and screws it on. Chrome is now the lead finish (brass/black as variants). Also a price anchor: designer ringed-disc sconce at $755.
- 11/9 render progress (agent interim): chrome hero + brass dome rendered and self-QA'd; black variant + exploded view pending. Agent sends PNGs to Austin itself.
- 11/9 render progress: black dome w/ chrome rim done; exploded view pending.
- 11/9 design-report.md landed (29 best-sellers, 6 render variants). Recs: lead chrome, kit $89, set $249/$329, names Spindle / Deadwax / Side A, 7" caps as chromed 45 adapters. Summary pushed to Austin.

## 2026-11-09 19:0x ET — Austin: wall attachment + BEHIND-THE-WALL wiring is the default
- Austin: "wiring should be designed to go behind the wall, most people will want to; down-the-wall still an option."
- Parts check: stock parts verified live (curl 200): E-Z Lok 400-4 insert, Rockler brass knob, Hardwick keyhole plate, Diode LED in-wall CL2 wire, LED Updates UL 12V adapter, Durofelt washers. The CHROME DOME is NOT a stock part: custom turned/CNC brass, chrome-plated, on a 1/4-20 stud. Needs a machine-shop quote.
- Design direction: keyhole/mounting plate on the hub over a 1" hole in the drywall; low-voltage DC (Class 2) runs inside the wall in CL2 cable down to an outlet-height recessed power kit (PowerBridge-style) where the UL adapter plugs in. Legal DIY, no electrician (only low-voltage side in wall, NEC 725). Surface cord + raceway stays as option B. Premium option C: hardwired to a standard junction box with a Class 2 driver in the box (electrician install; UL questions).
- Agent spawned to design + render the mount and in-wall wiring, and quote the chrome dome.
- 11/9 ~19:30 ET mount agent progress: render/sconce_v2.py built (original sconce.py untouched). Mount = 4" steel plate (arc slots fit single-gang 83.3 mm / round box 88.9 mm / anchors or stud, levelable) + 3 bayonet studs; hub J-slots twist-lock + M3 set screw at 6 o'clock; CL2 cable through the plate centre into the hub's DC jack. Finals: render/sconce_v2_cutaway.png, render/sconce_v2_rear.png (Cycles 1920x1080). mounting-report.md drafted; BOM + dome-cap quotes pending from research agents.
- 11/9 19:3x: mounting agent interim: renders + report skeleton done (renders sent to Austin 00:29Z); BOM + dome-cap sections pending its sub-agents. When filled: send Austin the dome-cap pick + kit BOM total (owed).

## 2026-11-09 21:3x ET — OVERNIGHT FULL BUILD (Austin: "front to back, full designs when I wake up, organized")
- Everything committed to git (0f5a787). Master brief: BRIEF.md. brain-rotate hold set 10h (memory/.rotate-hold-until) so agents survive.
- 8 Fable agents, one folder each: cad/ (STEP/DXF/drawings + RFQ packets), sourcing/ (vendors, sample-run plan, RFQ drafts NOT sent), build/ (BOM, sample shopping list, SOP, QC, cost model), renders-final/ (full image set), brand/ (name check, logo, packaging, guide), site/ (complete website, NOT deployed), marketing/ (campaign, ads, creators, flows), ops/ (legal, safety, insurance, entity options, policies).
- MORNING (me): when all land -> build START-HERE.html index of everything, cross-check consistency (prices, names, dims), commit, send Austin one organized Telegram with the link + top 5 decisions he owes.
- 21:34 ops agent interim: 6 policy drafts done, waiting on its own sub-researchers.
- 21:38 marketing interim: strategy, email-sms-flows, ad-copy-bank, organic-plan drafted; waiting on its creators/ads/PR researchers.
- 21:43 build/ DONE: BOM 12" $38 @100; $89 Kit only clears $25 before ads (needs price/spec decision, Austin); first 100 needs ~$5.3k cash; ~$400 parts + $300-360 tools for 3 prototypes this week. Some prices (Amazon/HD) need browser eyeball.
- 21:47 sourcing/ DONE: 45 vendors; sample run 8 units + 5 in-wall kits $1.3-1.7k, ~3 wks (chrome caps long pole; brass knobs unblock photos day 10); 13 RFQ drafts UNSENT. Needs Austin: logins for gated quoters (SendCutSend/Xometry/PCBWay) -> check credentials.md first; Broward lathe shop open.
- 21:55 brand/ DONE: recommend SPINDLE (class 011 clear, spindlelighting.com + @spindlelighting free). Side A has a live mark on vinyl sleeves -> dropped to 3rd. Tagline: Change the record. Change the room. Told site+marketing agents to switch working name to Spindle.
- 21:55 site/ DONE (12 pages, 24 screenshots, not deployed). Resumed it to switch brand constant to Spindle.
- 22:01 site/ rebranded to Spindle (config.js BRAND). Check: footer says 'Side A, always.' -> given the SIDE A sleeve mark, consider cutting in integration pass.
- 22:07 cad/ DONE: 9 parts STEP/STL/DXF, 12 drawings, 4 assemblies, interference-clean; 5 RFQ packets. Open: confirm DC jack dims, PEM hole.
- 22:36 marketing/ DONE: 8 files, 14 ad concepts on 17 live Meta ads + 17 viral TikToks, 48 verified creators, Reddit rules. Kickstarter = no. Remaining agents: renders-final, ops.
- 23:08 renders-final/ DONE: 46 stills + 8s loop. ENGINEERING FLAG: tight halo needs LED ring on the BACK of backplate near rim facing wall (not rim-edge as engineering/CAD assumed) -> reconcile CAD hub/backplate + BOM in integration. Rerun site/_gen/import-finals.sh. Only ops/ still running.
