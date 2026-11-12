# Spindle: creator seeding program (v2)

Rewritten 2026-11-11 after the audit (CHANGELOG.md). Nobody has been contacted. The creator list below is the v1 research pass of 2026-11-09 (48 accounts read from their live profile pages that night; follower counts will have moved). The v1 per-video rate column has been deleted: it priced creators at $10 to $25 per 1,000 followers, which put a 100K TikTok account at $1,000 to $2,500 a video and contradicted both the v1 budget and our own sponsorship research (see "What creators cost" below).

## What changed from v1 and why

- v1 shipped ten Kits to creators on 11/12. There are no Kits. Seeding starts at Gate 2 (strategy.md section 3): real units that passed the heat test, and a ship week on the page so a viewer who wants one can reserve it.
- v1 costed a gifted Kit at about $45. From ../build/cost-model.csv as rewritten by the product audit, a Kit costs $242.64 to build and ship at 20-unit prices (parts $211.33, labour $16.67, shipping $14.65) and $106.02 at 100-unit prices, with the chrome cap still an unquoted placeholder. Twenty gifts would be $2,100 to $4,800, not $900.
- v1 expected "most will post". Vendor sources put the post rate for unpaid gifting at 20 to 40% (Skeepers: "Gifted collaborations average a 20% to 40% post rate", https://www.skeepers.io/us/blog/product-seeding/, opened 2026-11-11; a vendor blog, no method shown). Our own research found no measured reply rate for cold creator outreach at all and used 3 to 6% from generic cold email as a floor (creator-sponsorship-norms-2026-08-31.md section 4a). Plan on a handful of yeses from 30 asks and one or two videos from five gifts.
- v1 offered @plastic.disc a TikTok Shop affiliate link. There is no TikTok Shop, no affiliate system and no discount codes. Removed.
- v1's disclosure line allowed "#ad or #gifted" in the caption. That is not enough (next section).

## Program design

Stage 1, at Gate 2: three units, gift only (it was five before the cost model was corrected). Pick the three whose own videos already look like ours (a lit room, a wall, hands on records), who are in the US, and whose recent videos get steady views. Choose on average views of their last ten videos, not on follower count (the first mistake on our research's list of common ones). Candidates from the list: @vintage_hifi_plants, @tyler.fortherecord, @spinningwithjackson, @her.vinyl, @zachs.space, with @kevin.vinyl and Too Many Records (YouTube) as alternates. Austin approves the three. Check each one's last ten videos by hand the week of outreach; none of that was done in this audit.

Stage 2, only if stage 1 produced at least one video and any reservations through creator links: three more units, weighted to apartment and decor accounts. No paid deal until the product clears a margin that can pay for one.

Stage 3, after Gate 3: paid videos with usage rights from whichever creator's gifted video brought reservations.

Rules:
- A gift is a material connection and must be disclosed. The FTC: a material connection includes "the brand ... giving you free or discounted products", and "the disclosure should be in the video and not just in the description"; it warns that disclosures get missed "at the end of posts or videos" and says not to use "vague or confusing terms like 'sp,' 'spon,' or 'collab'" (Disclosures 101 for Social Media Influencers, https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers, fetched 2026-11-11). TikTok's own policy lists "a product or service that has been gifted to you by (or on behalf of) a brand" as branded content and says "you must enable the commercial content disclosure toggle" (https://www.tiktok.com/legal/page/global/bc-policy/en, opened 2026-11-11). So the ask is: say or show "Spindle sent me this free" in the first seconds of the video, and switch the toggle on. A hashtag alone does not do it.
- We are responsible too. The endorsement guides put liability on the advertiser and expect it to give guidance and monitor (16 CFR 255.1(d), https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255). Watch every posted video the day it goes up; if the disclosure is missing, ask once in writing for it to be added, and keep the message.
- Never tie the gift to a good opinion, in words or by implication. 16 CFR 465.4 bars incentives "conditioned expressly or by implication" on a particular sentiment (https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465). The line to use: "Yours to keep. Say whatever you think of it, including the bad parts."
- No scripts and no approval rights on a gift. We send a one-page fact sheet: what it is, the measured numbers (heat reading, swap time), the ship week, what we do not claim (it is not UL listed as a fixture; we do not say "made in"), and three shots that tend to work (the light coming on, the swap, where they hung it).
- Band names and labels: the creator's own post is theirs. We do not ask them to hide their records and we do not ask them to show them. We include two plain-label records in the box so it is easy to film without a logo. A video goes into our own ad account only if no artist name, label or cover is visible or spoken, and only after the IP lawyer has answered that question (strategy.md section 9).
- Usage rights: a gift buys none. After a creator posts, we may ask to reshare with credit. Running their video as an ad (a Partnership Ad) is a paid deal, in writing, for a fixed term.
- Tracking: a personal link per creator (utm_source=creator, utm_content=handle). No codes.
- Nothing is sent to anyone outside the US until shipping and returns for that country are worked out.

## What creators cost (from our own research, not from a follower formula)

Source: creator-sponsorship-norms-2026-08-31.md in the workspace research folder, which was written for Ghost Audio and says plainly where its evidence is thin.

- Price on average views, not followers. At sponsorship rates of $25 to $60 per 1,000 views, a creator who averages 4,000 views is worth $100 to $240 a video.
- Revealed pricing on Collabstr: about $150 for a one-minute product video and $250 for a video made as an ad; range $50 to $1,000 and up.
- Realistic ask from a 10k to 100k TikTok creator for one video: $100 to $400 without usage rights; add 25 to 50% for paid usage (that uplift is an agency-blog figure and is flagged as low confidence in the research).
- YouTube costs more: the research's best-sourced figure is a median of $700 for a dedicated video from a small channel, and 50 to 60% of that for an integration.
- None of this was measured for home decor or for vinyl. Treat the first paid deal as price discovery and write down what was asked.

Against our margins: at $12.77 contribution a $250 video has to bring 20 orders of the $129 Sconce to pay for itself, before the cost of the unit. Paid creator deals are off until prices are re-set (strategy.md section 4).

## Budget

| Stage | Units | Product cost | Cash fees | When |
|---|---|---|---|---|
| 1 | 3 | about $730 at 20-unit cost, about $320 at 100-unit cost | $0 | Gate 2 |
| 2 | 3 | about $320 to $730 | $0 | only if stage 1 produced a video and tracked reservations |
| 3 | 0 to 2 | up to $210 | $250 to $500 per video with 90 days of paid usage | after Gate 3, only once the hero SKU clears $45 or more, and only for a creator whose gifted video brought reservations |

v1's month-two line of "$1,000 to $2,500" for 3 to 5 paid videos is replaced by the table.

## v1 shortlists (kept for reference; nothing ships before Gate 2)

Wave 1 as v1 listed it: @tyler.fortherecord (100.8K), @plastic.disc (81.3K), @vinylmaybe (89.3K), @vintage_hifi_plants (17.1K), @decibelvibe (106.2K), @zachs.space (28.5K), @kevin.vinyl (23.9K), @spinningwithjackson (7.2K), @her.vinyl (4.4K), Too Many Records on YouTube (55.4K).

Wave 2 as v1 listed it: @bohofrisco (94.5K), @444leafhome (11.8K), @lizathome_ (55.3K), @vinylgoneviral (11.2K), @anna_banana_vinyl (25.0K), @shayvinyls (17.4K), @vinyl.echoes_ (6.1K), @mattandjuanvinyl (9.2K), Melinda Murphy on YouTube (38.1K), Channel 33 RPM on YouTube (91.4K). @mattandjuanvinyl (UK) and Channel 33 RPM (Canada) are outside the US, as is @elie.vinyl (France) in the table below; all three are out until international shipping exists.

## Vinyl and record collecting (TikTok)

| # | Handle | URL | Followers | Niche | Why they fit | v1 approach (see program design; all gifting waits for Gate 2) | Verified |
|---|---|---|---|---|---|---|---|
| 1 | @tyler.fortherecord | https://www.tiktok.com/@tyler.fortherecord | 100.8K | Hi-fi and vinyl, "Welcome to my Listening Room" | Best fit: room shots, listening-room content | Gift, then paid | 200, profile data matches |
| 2 | @plastic.disc | https://www.tiktok.com/@plastic.disc | 81.3K | Vinyl recommendations, TikTok Shop | Already earns commission; affiliate link suits him | Gift + affiliate | 200 |
| 3 | @vinylmaybe | https://www.tiktok.com/@vinylmaybe | 89.3K | Collector, 10.9M likes | High engagement, public business email | Gift, then paid | 200 |
| 4 | @vinylplayground | https://www.tiktok.com/@vinylplayground | 194.5K | Vinyl, music, tech | Vinyl plus tech matches a lit-vinyl gadget | Paid | 200 |
| 5 | @lockedgroove | https://www.tiktok.com/@lockedgroove | 116.3K | Music appreciation | Large music-fan audience | Gift, then paid | 200 |
| 6 | @riquelmejosh | https://www.tiktok.com/@riquelmejosh | 142.9K | Turntables and setups for beginners | Setup content; has a manager | Paid | 200 |
| 7 | @elie.vinyl | https://www.tiktok.com/@elie.vinyl | 39.2K | French vinyl and concerts | EU test later | Gift | 200 |
| 8 | @vintage_hifi_plants | https://www.tiktok.com/@vintage_hifi_plants | 17.1K | Warm vintage hi-fi space | Mood-lit room look; 1.5M likes on 32 videos | Gift | 200 |
| 9 | @anna_banana_vinyl | https://www.tiktok.com/@anna_banana_vinyl | 25.0K | MTV-era nostalgia | Fits the $129 sconce with a vintage record | Gift | 200 |
| 10 | @kevin.vinyl | https://www.tiktok.com/@kevin.vinyl | 23.9K | Unboxing, 7.3M likes | Pure unboxing format | Gift | 200 |
| 11 | @shayvinyls | https://www.tiktok.com/@shayvinyls | 17.4K | "I buy records so you don't have to" | Posts constantly (1,338 videos) | Gift | 200 |
| 12 | @briancrowley | https://www.tiktok.com/@briancrowley | 16.4K | Spins records | Steady micro | Gift | 200 |
| 13 | @vinylgoneviral | https://www.tiktok.com/@vinylgoneviral | 11.2K | Millennial collector | Matches the Set buyer | Gift | 200 |
| 14 | @mattandjuanvinyl | https://www.tiktok.com/@mattandjuanvinyl | 9.2K | UK music content, invites collabs | Open to collabs | Gift | 200 |
| 15 | @spinningwithjackson | https://www.tiktok.com/@spinningwithjackson | 7.2K | Daily 1-minute spins, 3.4M likes | Spin format suits the mounted, lit record | Gift | 200 |
| 16 | @vinyl.echoes_ | https://www.tiktok.com/@vinyl.echoes_ | 6.1K | Physical media, hi-fi | Micro, aesthetic | Gift | 200 |
| 17 | @atribecalledval | https://www.tiktok.com/@atribecalledval | 5.2K | LA hip hop, collecting | Different audience slice | Gift | 200 |
| 18 | @her.vinyl | https://www.tiktok.com/@her.vinyl | 4.4K | Founder of a female collectors' community | Reaches a community, not just followers | Gift | 200 |

## Home decor, listening room, bar, lighting, gadgets (TikTok)

| # | Handle | URL | Followers | Niche | Why they fit | v1 approach (see program design; all gifting waits for Gate 2) | Verified |
|---|---|---|---|---|---|---|---|
| 19 | @zachs.space | https://www.tiktok.com/@zachs.space | 28.5K (bio: 117K across platforms) | Cozy desk and room setups; sells UGC | Made an IKEA vinyl setup video | Paid UGC | 200 |
| 20 | @444leafhome | https://www.tiktok.com/@444leafhome | 11.8K | Intentional interiors, Long Beach | Found under ambient-lighting and record-player-setup | Gift | 200 |
| 21 | @bohofrisco | https://www.tiktok.com/@bohofrisco | 94.5K | Colourful SF renter (Amanda Poe) | Renter-friendly wall decor | Gift, then paid | 200 |
| 22 | @lizathome_ | https://www.tiktok.com/@lizathome_ | 55.3K | Home decor and DIY, Atlanta | Public email | Gift | 200 |
| 23 | @vividcorners | https://www.tiktok.com/@vividcorners | 5.9K | Small-space design | Micro | Gift | 200 |
| 24 | @hansloreidesign | https://www.tiktok.com/@hansloreidesign | 236.1K | Interior designer | Design credibility | Paid | 200 |
| 25 | @sincerelyvalory | https://www.tiktok.com/@sincerelyvalory | 174.9K | Ambient room decor, Amazon storefront | Top result for "ambient lighting room" | Paid | 200 |
| 26 | @upgradeyour.home | https://www.tiktok.com/@upgradeyour.home | 192.7K | Home upgrades, finds | Finds format | Paid | 200 |
| 27 | @philfinds_ | https://www.tiktok.com/@philfinds_ | 122.5K | "Testing stuff so you don't have to" | Gadget-tester format | Paid | 200 |
| 28 | @decibelvibe | https://www.tiktok.com/@decibelvibe | 106.2K | VU-meter and spectrum displays | Audio gear that glows, same appeal | Gift, then paid | 200 |
| 29 | @thespritzeffect | https://www.tiktok.com/@thespritzeffect | 192.5K | Bar-cart styling | Home-bar angle, the Set | Paid | 200 |

## Large accounts for context (TikTok; not in any plan or budget)

| # | Handle | URL | Followers | Niche | Note | Verified |
|---|---|---|---|---|---|---|
| 30 | @want.zamora | https://www.tiktok.com/@want.zamora | 1.5M | Interior design, renter tips | Renter reach | 200 |
| 31 | @beingtheblooms | https://www.tiktok.com/@beingtheblooms | 2.1M | Cheap DIY wall decor (agency-managed) | Wall-decor reach | 200 |
| 32 | @hattiekolp | https://www.tiktok.com/@hattiekolp | 340K | Prewar NYC apartment | Apartment decor | 200 |
| 33 | @chelseyibrown | https://www.tiktok.com/@chelseyibrown | 341K | Rental style, NYC | Bio now says "Ex-influencer"; likely no | 200 |
| 34 | @nadismit | https://www.tiktok.com/@nadismit | 531.5K | Home, ASMR | Appears in vinyl-setup searches | 200 |
| 35 | @thethriftwitch | https://www.tiktok.com/@thethriftwitch | 489.1K | Cozy thrift vlogs | Thrifted-record angle | 200 |
| 36 | @mrrlittle | https://www.tiktok.com/@mrrlittle | 844.1K | LA home and lifestyle | Appears in vinyl-setup searches | 200 |

## YouTube

| # | Channel | URL | Subscribers | Niche | Why they fit | v1 approach (see program design; all gifting waits for Gate 2) | Verified |
|---|---|---|---|---|---|---|---|
| 37 | Noble Records (Dillon) | https://www.youtube.com/@noblerecords | 136K | Record buyer and store owner, NC | Collector audience; possible store stockist | Paid | 200, title and handle match |
| 38 | Too Many Records | https://www.youtube.com/@TooManyRecords | 55.4K | Vinyl nerd-out | Core collectors | Gift, then paid | 200 |
| 39 | Melinda Murphy | https://www.youtube.com/@MelindaMurphy | 38.1K | Which pressings are worth it | Trusted reviewer | Gift | 200 |
| 40 | Channel 33 RPM | https://www.youtube.com/@Channel33RPM | 91.4K | Vinyl and gear, Canada | Covers gear | Gift, then paid | 200 |
| 41 | Vinyl Rewind | https://www.youtube.com/@VinylRewind | 269K | Music-history essays, reviews | Large vinyl audience | Paid | 200 (host not confirmed) |
| 42 | The Vinyl Guide (Nate Goyer) | https://www.youtube.com/@TheVinylGuide | 13.2K | Vinyl podcast | Host-read spot | Gift | 200 |
| 43 | Music for Miles (was Vinyl for Miles) | https://www.youtube.com/@Music-for-Miles | 26.6K | Vinyl and music | Collector audience | Gift | 200 |
| 44 | Kristine Summer | https://www.youtube.com/@KristineSummer | 10.7K | Collector | Micro | Gift | 200 |
| 45 | Vinyl Richie | https://www.youtube.com/@vinylrichie007 | 8.9K | Collector | Micro | Gift | 200 |
| 46 | Rachael's Records | https://www.youtube.com/@RachaelsRecords | 4.9K | Collector | Micro | Gift | 200 |
| 47 | TheSorryGirls | https://www.youtube.com/@TheSorryGirls | 182K | DIY and thrifted spaces | Decor / DIY | Paid | 200 |
| 48 | Vinyl Eyezz | https://www.youtube.com/@vinyleyezz | 3.09M (as shown) | "Your home for vinyl records and music" | Context only | Paid | 200 |

## Instagram (not verified)

Instagram returns a login wall to logged-out requests, so no IG row above is verified. Before any outreach at Gate 2, check the Instagram accounts of the shortlisted creators in a logged-in browser. Until then Instagram is a reshare channel, not an outreach channel.

## How the list was verified

TikTok: GET of tiktok.com/@handle and a read of the page's embedded profile data (handle, display name, follower count, video count, bio). A HEAD request returns 403 even for real accounts, so status codes alone were not used. YouTube: GET of the channel page, reading og:title, the channel's @handle and the "N subscribers" text. Counts are from the platform pages, not Socialblade. Discovery sources: TikTok discover pages (vinyl-room, record-collection-room, vinyl-setup, listening-room, record-player-setup, ambient-lighting-room, apartment-decor-ideas, vinyl-unboxing), https://videos.feedspot.com/vinyl_record_youtube_channels/, https://www.yahoo.com/lifestyle/vinyl-tiktok-helped-record-collecting-135005080.html, https://sunset.com/home-garden/design/renter-friendly-design-tips, https://www.apartmenttherapy.com/rental-friendly-tiktok-decorating-hacks-37022677, https://www.tiktok.com/discover/vinyl-room.

Unverified or rejected: Darren's Vinyl Nation and Cosmic Chasm (404 at the guessed YouTube handles); @thomascsawyer (no profile); @vinylbymars, @stayininwithjulia, @heatherrobinsondesigns (no profile data returned); not checked for budget reasons: Jaden's Vinyl, 45 RPM Records, Spin Me Round, @oscarlyonscreates, @drewscott, @lightingbykris; Feedspot's "Infectious Groove Vinyl" channel ID now points at an unrelated food channel; poor fit: @johns_paul, @drew.hallgrimson. @vinylmeplease skipped as a brand.

## Outreach drafts (files only, nothing sent; for use at Gate 2)

Our research's advice on the message: say what the offer is in the first lines, keep it under about 120 words, refer to one specific video of theirs, one follow-up after 5 to 7 days and one at 14, then stop. Email first where a business address is public; TikTok direct messages are the weakest channel.

Gift email (subject: your [SPECIFIC VIDEO] and a wall light for records):

Hi [NAME],

I'm Austin. I make Spindle, a wall light built around a real 12 inch record: a warm ring of light behind it, a chrome dome that screws it on, nothing glued, so you can change the record. Your [SPECIFIC VIDEO] is the kind of room I built it for.

I'd like to send you one, free, yours to keep. No script, no obligation to post, and say whatever you think of it, including the bad parts. If you do post, please say on screen that I sent it to you free and switch on TikTok's disclosure setting; that part is the law, not my preference.

It's a new product from a one-person shop. Test numbers and real photos are here: [LINK].

If you're in, reply with a US shipping address.

Austin
Spindle
[POSTAL ADDRESS]

Short version for a direct message (under 300 characters):

Hi [NAME], Austin here. I make a wall light that back-lights a real record and lets you swap it, nothing glued. I'd like to send you one free, no script, no obligation, say what you like. If you post, just say on screen it was a gift. Interested?

Paid brief (stage 2 and 3, one page): one vertical video of 15 to 30 seconds and one still; the fact sheet; the disclosure line and the toggle; the fee, paid on delivery; 90 days of paid usage and Partnership Ad access, in writing; one round of notes limited to factual errors and legal lines, never taste. No real labels or artist names visible or spoken in a video we pay to run.
