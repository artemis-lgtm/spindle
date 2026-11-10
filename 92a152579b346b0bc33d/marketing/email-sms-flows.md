# Spindle: email and SMS flows (ready to paste)

Prepared 2026-11-09. Nothing here has been sent. Brand and product are both "Spindle" (brand/naming-report.md, 11/9: "Side A" conflicts with a live trademark on record sleeves). Handles @spindlelighting, domain spindlelighting.com (free, not bought).

House rules baked in: plain paragraphs, no bold, no bullet lists inside emails (Austin's email rule, tools/email_format_gate.py). No band names, album titles or logos. "Sold out" only as "first batch of 20 sold out". No ship date, countdown, or batch-size number that is not real. Every deposit email carries the FTC Mail Order Rule language from scope-report.md section 4: refundable any time, the ship week we commit to, and the right to cancel for a full refund if we miss it. Reply-to is a human inbox. Sender: "Austin at Spindle". Unsubscribe in every email; SMS only with express written consent at the form (TCPA), STOP/HELP language on the first text.

Placeholders in square brackets must be filled with real values before a flow is switched on. [SHIP WEEK] is the batch-two ship week Austin sets with a two-week buffer. [FIRST NAME] falls back to "there". [LINK] is the page or Stripe link. Do not launch flow 3 (batch-two countdown) until [SHIP WEEK] exists.

Tooling: Klaviyo or Mailchimp for flows; Stripe webhook (checkout.session.completed) tags the contact "deposit"; Stripe Payment Link success redirect to /thanks-deposit fires the Purchase pixel. Abandoned deposit uses Stripe's abandoned-checkout recovery email or Klaviyo "Started Checkout" via the Stripe integration.

---

## Flow 1: Free waitlist welcome (3 emails + 1 optional SMS)

Trigger: free-list form submit (no deposit). Goal: move them to the $25 deposit.

Email 1.1, immediately. Subject: You're on the list for The Spindle
Preview: Here is what you actually signed up for.

Hi [FIRST NAME],

You're on the waitlist for The Spindle, the wall light built around a real record. A warm ring of light sits behind a 12" LP and throws a halo on the wall, and a polished chrome dome screws the record on through the spindle hole. Nothing is glued. Unscrew the dome and swap the record whenever you like.

The first batch of 20 sold out. The next batch is made to order, and deposit holders get first pick of finish (chrome, brass or black) and the first ship slots. A $25 deposit holds a spot and comes off the price; it is refundable any time, no questions.

Hold a spot: [LINK]

If you'd rather wait and watch, that's fine too. I'll send one email when the batch opens and one when it ships, and nothing else.

Austin
Spindle, Fort Lauderdale

Email 1.2, day 2. Subject: Why nothing is glued to your record
Preview: The part everyone asks about.

Hi [FIRST NAME],

The first question I get is whether the light damages the record. It doesn't. The record rests on three felt pads and a felt washer sits under the chrome dome, which finger-tightens on a quarter-inch post through the spindle hole. No adhesive, no clips on the edge, no heat near the vinyl. The light is a 12 volt ring on the rim of the backplate, so the record never touches anything warm.

That is also why you can change it. Ten seconds, one hand, and a different record is on the wall. People who have the first batch are already swapping with the season.

If you want one of the next batch, a $25 refundable deposit holds it and picks your finish: [LINK]

Austin

Email 1.3, day 5. Subject: Three ways people are hanging it
Preview: Wiring in the wall, down the wall, or into a box.

Hi [FIRST NAME],

Quick one. Three ways the first twenty went up. Most ran the low-voltage cable inside the wall down to a small plate by the outlet, which takes about 45 minutes and no electrician because nothing above 12 volts goes in the wall. Renters ran the braided cord straight down to the outlet in a paintable channel, about 15 minutes. A few had an electrician wire it to a switch.

All three use the same steel mounting plate and the same twist-lock, so you can start with the cord and go in-wall later.

Deposits for the next batch are open, refundable any time: [LINK]

Austin

SMS 1.1 (only if they ticked SMS consent), day 3, 11am local:
Spindle: Hi [FIRST NAME], Austin here. Deposits for the next batch of The Spindle are open. $25 holds your spot and finish, refundable any time: [LINK]. Reply STOP to opt out, HELP for help.

---

## Flow 2: Deposit confirmation (immediate + day 1 + day 7)

Trigger: Stripe checkout.session.completed for the $25 deposit product. Goal: confirm, reassure, collect finish and record preference, start the referral loop.

Email 2.1, immediately. Subject: Your Spindle spot is held (deposit #[DEPOSIT NUMBER])
Preview: Here is what happens next and how refunds work.

Hi [FIRST NAME],

Thank you. Your $25 deposit is received and your spot in the next batch of The Spindle is held. It comes off the balance when your light ships.

Two plain facts first. The deposit is fully refundable at any time; reply to this email and it goes back to your card. The next batch ships the week of [SHIP WEEK]. If we cannot ship by then you will hear from me before that date with a new date, and you can cancel for a full refund.

What I need from you, when you have a minute: your finish (chrome, brass or black), whether you want the light only for your own record or one of ours with a vintage pressing from your decade, and in-wall or surface wiring. Tell me here: [PREFERENCE FORM LINK]

Your receipt is attached from Stripe. Your deposit number is [DEPOSIT NUMBER]; balance due before ship is [BALANCE] for the [SKU].

Austin
Spindle, Fort Lauderdale

Email 2.2, day 1. Subject: Pick the record before it gets here
Preview: What goes on the wall first.

Hi [FIRST NAME],

Most people know exactly which record goes up first. Some don't, and that's the fun part. The label is what you see, so look at labels, not covers. Solid colours and simple type read best behind the chrome dome; busy labels look great in brass. Coloured vinyl glows at the edge where the halo catches it.

If you chose one of ours, tell me your decade and a mood (quiet, loud, Sunday morning) and I'll pick a clean pressing with a label worth looking at.

Preferences, if you haven't sent them: [PREFERENCE FORM LINK]

Austin

Email 2.3, day 7. Subject: Know someone with a crate they never look at?
Preview: One link, no codes.

Hi [FIRST NAME],

Deposit holders get first pick of ship slots, and the batch fills in order. If a friend wants one in the same batch, this link puts them straight into the deposit page: [REFERRAL LINK]. No codes, no points; I'd just rather the batch go to people you know.

A photo of a first-batch unit on a dark green wall is attached, for scale and because it looks good.

Austin

Printable certificate (attached to 2.1 when the buyer ticks "this is a gift"): one page, cream, the brand mark, "A Spindle is on its way to [RECIPIENT]. Finish: [FINISH]. From: [GIVER]." plus the line "Made to order in Fort Lauderdale; ships the week of [SHIP WEEK]." No ship week set, no certificate.

SMS 2.1, immediately (consented only):
Spindle: Deposit received, [FIRST NAME]. Your Spindle spot is held and refundable any time. Pick your finish here: [PREFERENCE FORM LINK]. Reply STOP to opt out.

---

## Flow 3: Batch-two countdown (ONLY with real dates)

Trigger: Austin sets [SHIP WEEK] and [BATCH CAP]. Three emails to the free list and the deposit list, no countdown timers, no "almost gone" unless the count is wired to Stripe.

Email 3.1, when the date is set. Subject: Batch two ships the week of [SHIP WEEK]
Preview: Real date, real number.

Hi [FIRST NAME],

The next batch of The Spindle has a ship week: [SHIP WEEK]. The batch is capped at [BATCH CAP] units because that is what we can build well in that window; deposit number [BATCH CAP + 1] goes to the batch after.

Deposits are $25, refundable any time, and come off the price. Kit for your own record $89. With a vintage pressing from your decade $129. The three-piece set, one 12" and two 7", from $249.

Hold a spot: [LINK]

Austin

Email 3.2, 7 days before the batch closes. Subject: [REAL NUMBER] spots left in batch two
Preview: Closes [CLOSE DATE] or when full.

Hi [FIRST NAME],

As of this morning [REAL NUMBER] of the [BATCH CAP] spots in batch two are open. Deposits close on [CLOSE DATE] or when the batch is full, whichever is first, so parts can be ordered and the ship week of [SHIP WEEK] holds.

Hold a spot: [LINK]

Austin

(Send 3.2 only if [REAL NUMBER] is pulled from Stripe that morning. If the count isn't automated, send without the number: "spots are still open in batch two; deposits close [CLOSE DATE].")

Email 3.3, day of close. Subject: Batch two closes tonight
Preview: After midnight ET new deposits roll to batch three.

Hi [FIRST NAME],

Deposits for batch two close tonight at 11:59 pm ET. Anything after that goes to batch three with its own ship date. Same $25, same refund policy.

[LINK]

Austin

SMS 3.1 (consented), morning of close:
Spindle: Batch two of The Spindle closes tonight 11:59pm ET. $25 refundable deposit holds a spot: [LINK]. Reply STOP to opt out.

---

## Flow 4: Shipping (balance due, shipped, delivered)

Email 4.1, 10 days before ship. Subject: Your Spindle ships the week of [SHIP WEEK]; balance due
Preview: Final step before it goes in the box.

Hi [FIRST NAME],

Your Spindle is in the build queue for the week of [SHIP WEEK]. The balance is [BALANCE] for the [SKU] in [FINISH], with your $25 deposit already taken off. Pay here: [BALANCE LINK]

Shipping is included in the US. Confirm the address in that link; it ships in a double-wall box with a foam tray, and the record (if you chose one) travels in its own sleeve under the plate.

If anything has changed and you'd rather not, reply and the deposit is refunded in full.

Austin

Email 4.2, on ship. Subject: It's on the way
Preview: Tracking inside, plus the two-minute install.

Hi [FIRST NAME],

Your Spindle shipped today. Tracking: [TRACKING LINK]

While it travels, the install card is attached. Surface cord is about 15 minutes. In-wall is about 45 and the card walks through the one-inch hole, the cable drop and the plate by the outlet. Only the 12 volt side goes in the wall; the adapter stays at the outlet.

When it's up, send me a photo. I mean that.

Austin

Email 4.3, 2 days after delivery scan. Subject: Did it arrive in one piece?
Preview: Reply with one word if so.

Hi [FIRST NAME],

Tracking says your Spindle was delivered. Records in flat boxes make me nervous, so reply with one word if everything is intact, or send a photo if it isn't and a replacement goes out the same day.

Austin

SMS 4.1 (consented), on ship:
Spindle: Your Spindle shipped. Track it: [TRACKING LINK]. Reply STOP to opt out.

---

## Flow 5: Review request (day 10 and day 24 after delivery)

Email 5.1, day 10. Subject: Which record went up first?
Preview: Genuinely curious.

Hi [FIRST NAME],

Ten days in. What's on the wall? If you have 60 seconds, a photo and two sentences here help the next batch more than any ad I could run: [REVIEW LINK]. If you post it, tag @spindlelighting and I'll share it.

If anything isn't right, reply to this instead and I'll fix it first.

Austin

Email 5.2, day 24 (only if no review and no complaint). Subject: One more ask, then I'll stop
Preview: Two sentences.

Hi [FIRST NAME],

Last ask from me on this. A short review here [REVIEW LINK] is the thing that lets a stranger trust a small shop in Fort Lauderdale with their favourite record. Two sentences is plenty.

Thank you for being in the early batch.

Austin

---

## Flow 6: Abandoned deposit (started checkout, no payment)

Trigger: Stripe Checkout started, no completion in 1 hour (email captured at Checkout). Two emails, one SMS if consented.

Email 6.1, 1 hour. Subject: Your spot is still open
Preview: Refundable any time, so no pressure.

Hi [FIRST NAME],

You started a deposit for The Spindle and didn't finish, which usually means a question. The common ones: the $25 is fully refundable any time; it comes off the price; nothing is glued to your record; it plugs in and needs no electrician; shipping in the US is included.

Finish the deposit: [LINK]

Or just reply with the question.

Austin

Email 6.2, day 2. Subject: The ten-second swap
Preview: A short clip.

Hi [FIRST NAME],

Here is the thing people like most, in ten seconds: unscrew the chrome dome, lift the record, drop another one on, screw it back. [CLIP LINK]

Your spot in the next batch is still open: [LINK]

Austin

SMS 6.1 (consented), 3 hours:
Spindle: Your Spindle deposit didn't go through. It's $25, refundable any time: [LINK]. Reply STOP to opt out.

---

## Flow 7: Delay notice (keep ready, hope to never send)

Required by the FTC Mail Order Rule if we miss [SHIP WEEK] (scope-report.md section 4). Send before the promised date.

Subject: Your Spindle ship date has moved; your options
Preview: New date, or a full refund, your call.

Hi [FIRST NAME],

I promised the week of [SHIP WEEK] and we will miss it. [ONE HONEST SENTENCE ON WHY]. The new ship week is [NEW SHIP WEEK].

You have two options and both are fine. Keep your spot and nothing more is needed. Or cancel for a full refund of everything paid, which goes back to your card within one billing cycle; reply "refund" and it's done.

I'm sorry for the wait.

Austin

---

## Flow 8: The first 20 buyers (one-off, 11/10)

Subject: You're the first twenty
Preview: What's next for your Spindle, and a favour.

Hi [FIRST NAME],

You bought one of the first twenty Spindles before most people knew it existed, and I want you to hear the plan from me. Your unit is in the first build run and ships the week of [SHIP WEEK]; you'll get tracking and the install card by email.

A favour. The next batch opens tomorrow, and the honest line on the page is that the first twenty sold out, because they did, to you. If you know someone who should have one, this link puts them at the front of the next batch: [REFERRAL LINK]

Thank you for trusting a new thing.

Austin
Spindle, Fort Lauderdale
