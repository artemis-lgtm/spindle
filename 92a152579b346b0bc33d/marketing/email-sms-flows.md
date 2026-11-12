# Spindle: email flows (v2), with SMS parked

Rewritten 2026-11-11 after the audit (CHANGELOG.md). Nothing here has been sent. Gates 0 to 3 are defined in strategy.md section 3; each flow says which gate must be passed before it is switched on.

## Rules for every email

- Plain paragraphs. No bold, no bullets, no headers inside an email.
- No band, artist, album or label names.
- Nothing is stated about a finished unit, a customer, a photo, a temperature, a swap time or an install time unless it exists and is on file. v1 had emails saying "people who have the first batch are already swapping with the season", "three ways the first twenty went up" and "a photo of a first-batch unit on a dark green wall is attached". None of those things exist. They are gone.
- "First batch of 20 sold out" is not used until the 20 have shipped (Gate 3). From Gate 2, and only if the ledger of the 20 exists: "the first 20 are spoken for".
- Origin wording: "designed and assembled in Fort Lauderdale from US and imported parts", never "made in".
- Every commercial email carries an unsubscribe link and a valid physical postal address in the footer. The law requires "a valid physical postal address of the sender" (15 USC 7704(a)(5)(A)(iii), read 2026-11-11 at https://www.law.cornell.edu/uscode/text/15/7704). "Spindle, Fort Lauderdale" is not an address. [POSTAL ADDRESS] below must be a real street address or a registered PO box; Austin supplies it.
- Sender: "Austin at Spindle", from a mailbox on the Spindle domain, in an email tool account that belongs to Spindle alone. Not the Higney International Mailchimp, not a Higney address, not anything Ghost Audio or Elbo Room uses. Klaviyo's free plan covers "250 active profiles and 500 emails per month" (https://www.klaviyo.com/pricing, opened 2026-11-11), which is enough to start.
- Reply-to is a mailbox a person reads.

## The deposit and the law (read before switching on flows 2, 3, 4, 6, 7)

A $25 deposit is a partial payment, and the mail order rule counts it. The rule's definition of a received order covers a buyer who "tenders full or partial payment", and it requires a "reasonable basis" to ship within the time stated or, "if no time is clearly and conspicuously stated, within thirty (30) days" (16 CFR 435.1(c), 435.2(a)(1); https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-435). Without "records or other documentary proof" of a system that ships on time, the rule presumes there was no reasonable basis (435.2(a)(4)).

So: no deposit is taken, and flows 2 to 4, 6 and 7 stay off, until [SHIP WEEK] exists and is backed by the sample run and written supplier lead times. If Austin already took money from the first 20, those are orders today and flow 8 goes first.

Placeholders in square brackets must be real before a flow is switched on. That includes [PRICE] and [KIT PRICE]: prices are being re-set from the product audit's cost model (strategy.md section 4). Only chrome is offered, so no email asks for a finish. [FIRST NAME] falls back to "there".

---

## Flow 1: Waitlist welcome (2 emails). Live from Gate 0.

Trigger: waitlist form submit. Goal before Gate 2: keep the promise made on the form and nothing more. v1 sent three sales emails and a text after telling the reader "I'll send one email when the batch opens and one when it ships, and nothing else". That contradiction is removed.

Email 1.1, immediately. Subject: You're on the Spindle list
Preview: What it is, where it stands, and what I'll send you.

Hi [FIRST NAME],

You're on the list for Spindle, a wall light built around a real record. A warm ring of light sits behind a 12 inch LP and throws a halo on the wall, and a chrome dome screws the record on through the spindle hole. Nothing is glued, so you can change the record whenever you like.

Here is where it honestly stands. The design is finished and the first units are being built and tested now. The pictures on the site are renders until the first real one is on a wall. I won't take anyone's money until the test units have passed, including a heat test with a probe on the record, and I have a ship date I can stand behind.

You will get three more emails from me at most: one with the first real photos and the test results, one when reservations open, and one when units ship. If you want to watch it get built in the meantime, it's at [TIKTOK OR INSTAGRAM LINK].

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

Email 1.2, at Gate 1 (one send to the whole list, not a timed drip). Subject: The first real one is on the wall
Preview: Photos, and the heat test numbers.

Hi [FIRST NAME],

The first Spindle is built and hanging. Real photos are here: [LINK].

The question I get most is whether the light is bad for the record, so I measured it. With a probe on the back edge of the record and the light on for two hours, the record read [Y] F in a room at [X] F. The full test is on the page.

The swap takes [N] seconds; there's a one-take video at [LINK].

Reservations aren't open yet. They open when I can give you a ship week I trust, and you'll hear first.

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

(Send 1.2 only with real photos, a real reading and a real time. If the heat reading is over the test limit, this email does not go; a plain "it ran warm, here is what I'm changing" note goes instead.)

---

## Flow 2: Reservation confirmation (immediate + day 2). Live from Gate 2.

Trigger: Stripe checkout.session.completed for the deposit or the full pre-order.

Email 2.1, immediately. Subject: Your Spindle is reserved (order [ORDER NUMBER])
Preview: Ship week, refunds, and one thing I need from you.

Hi [FIRST NAME],

Thank you. I have your [$25 deposit / payment of AMOUNT] and a Spindle in the next batch is yours. [For deposits: The $25 comes off the price; the balance of BALANCE is due before it ships.]

Two plain facts. Your order ships the week of [SHIP WEEK]. If I can't make that week I will tell you before it arrives, give you a new date, and you can take a full refund instead. And you can cancel for a full refund at any time before it ships, for any reason; reply to this email and it's done.

One thing I need: whether you want the light for your own record or with one of ours, and whether you'll run the cord down the wall or inside it. Tell me here: [PREFERENCE FORM LINK]

Stripe sends your receipt separately.

Austin
Spindle
[POSTAL ADDRESS]

Email 2.2, day 2. Subject: Pick the record before it gets here
Preview: What goes on the wall first.

Hi [FIRST NAME],

Most people know which record goes up first. If you don't, look at labels, not covers, because the label is what you see around the dome. Plain colours and simple type read best. Coloured vinyl catches the light at the edge.

If you chose one of ours, tell me a decade and a mood and I'll pick a clean pressing with a label worth looking at.

Preferences, if you haven't sent them: [PREFERENCE FORM LINK]

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

Removed from v1: email 2.3 (the referral ask with an attached photo that did not exist). A referral line can return after Gate 3 with a real photo.

Gift certificate: one page, the brand mark, "A Spindle is on its way to [RECIPIENT]. From [GIVER]. Designed and assembled in Fort Lauderdale. Ships the week of [SHIP WEEK]." Attached to 2.1 only when the buyer ticked "this is a gift". No ship week, no certificate.

---

## Flow 3: Batch announcement (real dates only). Live from Gate 2.

Trigger: Austin sets [SHIP WEEK], [BATCH CAP] and [CLOSE DATE].

Email 3.1, when the date is set. To the waitlist. Subject: Spindle reservations are open; ships the week of [SHIP WEEK]
Preview: The date, the number, the price.

Hi [FIRST NAME],

Reservations for Spindle are open. This batch is [BATCH CAP] units, because that is what I can build well in the time, and it ships the week of [SHIP WEEK]. Order number [BATCH CAP + 1] goes to the following batch with its own date, and you'll see that before you pay.

With one of our vintage records it's [PRICE]. For your own record it's [KIT PRICE]. [A $25 refundable deposit holds one, or you can pay in full.] Either way you can cancel for a full refund any time before it ships.

Reserve one: [LINK]

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

Email 3.2, the morning of [CLOSE DATE]. Subject: Spindle reservations close tonight
Preview: After 11:59 pm ET, new orders go to the next batch.

Hi [FIRST NAME],

Reservations for this batch close tonight at 11:59 pm Eastern so I can order parts and hold the ship week of [SHIP WEEK]. Orders after that go to the next batch with a later date.

[LINK]

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

Removed from v1: the "[REAL NUMBER] spots left" email. It is allowed only if the number is read from Stripe by a script that morning; with one person and no such script it is a mistake waiting to happen. 3.2 goes only if the close date is real and is enforced on the page.

---

## Flow 4: Shipping. Live from Gate 2.

Email 4.1, 10 days before ship (deposit orders only). Subject: Your Spindle ships the week of [SHIP WEEK]; balance due
Preview: Last step before it goes in the box.

Hi [FIRST NAME],

Your Spindle is in the build queue for the week of [SHIP WEEK]. The balance is [BALANCE] for the [SKU], with your $25 deposit already taken off. Pay here: [BALANCE LINK]

Shipping in the US is included. Please confirm your address at that link.

If anything has changed and you'd rather not, reply and your deposit is refunded in full.

Austin
Spindle
[POSTAL ADDRESS]

Email 4.2, on ship. Subject: It's on the way
Preview: Tracking, and the install card.

Hi [FIRST NAME],

Your Spindle shipped today. Tracking: [TRACKING LINK]

The install card is attached. It covers the cord-down-the-wall install and the in-wall one. Only the 12 volt cable goes inside a wall; the adapter stays at the outlet. In-wall low-voltage cable is allowed in most US homes under the National Electrical Code; check your local rules if you're unsure.

When it's up, send me a photo. I mean that.

Austin
Spindle
[POSTAL ADDRESS]

Email 4.3, 2 days after the delivery scan. Subject: Did it arrive in one piece?
Preview: One word is plenty.

Hi [FIRST NAME],

Tracking says your Spindle was delivered. Reply with one word if everything is intact. If anything is broken, send a photo and I'll replace the part or the unit as fast as I can build one, at no cost to you.

Austin
Spindle
[POSTAL ADDRESS]

(v1 promised "a replacement goes out the same day". A made-to-order shop of one cannot promise that.)

---

## Flow 5: Review request (day 10 and day 24 after delivery). Live from Gate 3.

Both emails go to every delivered customer. v1 sent the second one "only if no review and no complaint", which filters unhappy buyers out of the review ask; that filter is removed. Reviews are never edited, never hidden for being negative, and never rewarded (16 CFR 465.4 bars incentives "conditioned expressly or by implication" on a review's sentiment, and 465.7 covers suppression; https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465).

Email 5.1, day 10. Subject: Which record went up first?
Preview: Genuinely curious.

Hi [FIRST NAME],

Ten days in. What's on the wall? If you have a minute, a photo and two honest sentences here help the next person decide more than anything I could write: [REVIEW LINK]. Good or bad, I'll publish it as written.

If something isn't right, reply to this as well and I'll fix it.

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

Email 5.2, day 24 (only if no review yet). Subject: One more ask, then I'll stop
Preview: Two sentences.

Hi [FIRST NAME],

Last ask from me on this. A short, honest review here [REVIEW LINK] is what lets a stranger trust a one-person shop with their favourite record. Two sentences is plenty.

Thank you for being early.

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

---

## Flow 6: Unfinished checkout (1 email). Live from Gate 2.

Trigger: Stripe Checkout started with an email captured, no completion in 2 hours.

Email 6.1. Subject: Your Spindle reservation isn't finished
Preview: In case it was a question.

Hi [FIRST NAME],

You started reserving a Spindle and didn't finish, which usually means a question. The short answers: it ships the week of [SHIP WEEK]; you can cancel for a full refund any time before then; nothing is glued to your record; it plugs into a normal outlet.

Finish here: [LINK]

Or reply with the question.

Austin
Spindle
[POSTAL ADDRESS]
[UNSUBSCRIBE]

(v1's second abandoned-checkout email and its text are removed. One reminder is enough for a list this size.)

---

## Flow 7: Delay notice (two versions; send before the promised week, never after)

The rule sets what this notice must say, and v1's single version did not meet it. From 16 CFR 435.2(b)(1): the offer must be made "in no event later than" the promised time; where the new date is 30 days or less later, the notice must say that without a reply the buyer "will be deemed to have consented"; where it is more than 30 days later, or unknown, the notice must say the order "will automatically be deemed to have been cancelled" unless the buyer agrees to the delay. The FTC's business guide says the same in plain words (https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule, fetched 2026-11-11). A cancelled order is refunded within seven working days (435.1(b)(1)).

Version A, new date 30 days or less after the promised week.
Subject: Your Spindle is delayed to [NEW SHIP WEEK]; your options
Preview: Keep your place, or take a full refund.

Hi [FIRST NAME],

I promised to ship your Spindle the week of [SHIP WEEK] and I'm going to miss it. [ONE HONEST SENTENCE ON WHY.] The new ship date is [NEW SHIP DATE].

You have two choices. You can cancel now for a full refund of everything you've paid; reply "cancel" or use this link [CANCEL LINK] and the money goes back to your card within seven working days. Or you can wait. If I don't hear from you, I'll take that as your agreement to the new date and ship on or before [NEW SHIP DATE].

I'm sorry for the wait.

Austin
Spindle
[POSTAL ADDRESS]

Version B, new date more than 30 days later, or no date yet.
Subject: Your Spindle is delayed; please tell me what you want to do
Preview: I need a reply to keep your order.

Hi [FIRST NAME],

I promised to ship your Spindle the week of [SHIP WEEK] and I'm going to miss it. [ONE HONEST SENTENCE ON WHY.] [The new ship date is NEW SHIP DATE. / I can't give you a new date yet.]

Because the delay is long, I need to hear from you. If you want to keep your order, reply "keep" or use this link [KEEP LINK]. If I don't hear from you by [ORIGINAL SHIP WEEK END PLUS 30 DAYS] and it hasn't shipped, your order is cancelled automatically and everything you've paid goes back to your card. You can also cancel today for a full refund: [CANCEL LINK].

I'm sorry. This is on me.

Austin
Spindle
[POSTAL ADDRESS]

Keep a log of who was sent which version and when, and of every reply.

---

## Flow 8: The first 20 (one-off). Send as soon as the ledger exists.

This email depends on facts only Austin has: who the 20 are, whether they paid, and what they were told. Two versions.

If they paid something:
Subject: Your Spindle: where it stands
Preview: The honest timeline, and your options.

Hi [FIRST NAME],

You were one of the first twenty people to buy a Spindle, before one existed, and you should hear the plan from me. The design is finished. The first test units are being built now and have to pass a heat test and a drop test before I build yours. My honest estimate for shipping yours is the week of [SHIP WEEK].

If that's later than you expected, or you'd rather not wait, reply and I'll refund you in full, no questions. If you're happy to wait, you don't need to do anything, and I'll send photos as the first ones come together.

Thank you for trusting a new thing.

Austin
Spindle
[POSTAL ADDRESS]

If they said yes but have not paid:
Subject: Your Spindle: where it stands
Preview: The honest timeline.

Hi [FIRST NAME],

You told me you wanted one of the first twenty Spindles, and you should hear the plan from me. The design is finished and the first test units are being built now. Once they pass the heat and drop tests I'll have a firm ship week, and I'll send you a link to pay then, not before.

I'll send photos as the first ones come together.

Austin
Spindle
[POSTAL ADDRESS]

(v1's version asked the 20 to refer friends to a batch that "opens tomorrow". Nothing opens tomorrow.)

---

## SMS: parked

v1 had six text messages. They are removed from the launch, for these reasons.

- Marketing texts need "prior express written consent", and that consent cannot be "a condition of purchasing any property, goods, or services" (47 CFR 64.1200(a)(2) and (f)(9); https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200, read 2026-11-11). No texts before 8 a.m. or after 9 p.m. in the recipient's local time (64.1200(c)(1)). v1's "immediately" and "3 hours after an abandoned checkout" texts could land at 2 a.m.
- Opt-outs must be honoured through "any reasonable method", and the rule names "stop", "quit", "end", "revoke", "opt out", "cancel" and "unsubscribe" (64.1200(a)(10)).
- Florida has its own statute with its own written-consent rule for automated texts and a private right of action (Fla. Stat. 501.059, read 2026-11-11 at leg.state.fl.us). We are a Florida seller.
- The upside is tiny. The list will be dozens to low hundreds of people for months.

If SMS is ever added: an unticked box with the full disclosure next to it, a platform that enforces quiet hours by the recipient's area code and keeps the consent record, registration with the carriers, and a lawyer's read of the form. Florida quiet hours and message caps were not checked in this audit.
