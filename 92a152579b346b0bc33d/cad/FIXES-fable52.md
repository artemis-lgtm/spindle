# Fixes applied from the Fable 5.2 pessimist review

> **Update 2026-11-11, later the same day:** item M11 i (renders show the LED ring on the back face, CAD had it on the rim) is now CLOSED by `FIXES-heat-layout.md`: the strip moved to the back face on an aluminium ring over a cork ring, RS-BP-12-MDF went to rev C, and the build now ends with more gates than the 105 quoted below. Everything else in this file stands as written.

Answers `cad/REVIEW-fable52.md` item by item. Applied 2026-11-11 by claude-fable-5-2. Nothing was sent, ordered or published.

**New revisions:** RS-CAP-12 **rev D**, RS-CAP-7 **rev C**, RS-CAP-12L and its hub module **rev B**, RS-BP-12-MDF / RS-BP-7-MDF **rev B**, RS-HUB-01 **rev B**. RS-WP-01 and the aluminum plates are unchanged (rev A, sheets re-issued).
**Superseded, never quote:** RS-CAP-12 rev A/B/C, RS-CAP-7 rev A/B, RS-CAP-12L rev A/A.1, backplate rev A, hub rev A. Old zips are in `cad/rfq/SUPERSEDED-do-not-quote/`; `cad/rfq/README.md` is the index; every SPEC.txt opens with a REVISION STATUS block and every title block has a SUPERSEDES line.

**Build result:** `cad/.venv/bin/python build_all.py` ends with `gates: 105 pass, 0 FAIL`. The gates live in `cad/gates.py` and are printed at the top of `cad/checks.md`; the build exits non-zero if one fails. File:line references below are to the files as committed.

## Where I did not follow the review to the letter (read this first)

1. **M6, the "5 mm stroke Mill-Max pin" does not exist.** Mill-Max's own page calls the 3.0 mm 0919 family its longest travel, and a search of Harwin, Preci-Dip, PTR and Same Sky found nothing compact above 3.5. The stack needs 4.2 mm. So the centre contact is now a custom gold plunger on a catalogue compression spring, running inside the carrier's spigot, which doubles as the PEEK guard tube the review asked for. It has 4.9 mm of travel. This is a new mechanism that has never been built, and the spring is calculated, not a picked part number.
2. **M8, the pin head is at the tip end, not on the sleeve top.** The spring pushes the pin into the cap. A head on top of the sleeve stops it falling out, not walking in, and a D 2.4 head cannot sit in the D 2.2 bore the review specified above the sleeve. The head now seats in a counterbore in the sleeve's tip end, which is a real stop in the direction of the load. The sleeve becomes a turned PEEK part instead of cut tubing.
3. **M4, I deleted the lit cap's felt and recess instead of thickening the flange.** Thickening to 1.8 (tried first) lifted the light slot 0.5 mm and the ray trace showed the dark collar next to the cap growing from about 3 mm to about 8 mm. With no recess the flange is solid 1.3, sits flat on the PET washer, and the optics are unchanged (max/min 3.96 against 3.73 before).
4. **M3, the lip went up 0.20; the louver did not come down.** Same reason: the louver is the optic. The gap is 0.25 either way.
5. **M1, the centre ring has no 0.5 pocket.** With the review's own compression figure (1.6 free, 1.1 loaded) a 0.5 pocket would leave the clamped centre 0.5 lower than the unloaded pads: a new dish. The ring sits on the face inside a scored witness circle, so its loaded top is coplanar with the pads. One parameter (`CENTER_RING_SET`) carries the assumption; measure it and the pocket depth follows.
6. **M11c, the separate-stud option is deleted, not corrected to 18.7.** The new D 7.10 shoulder cannot be tapped 1/4-20 (0.37 wall).
7. **Found on the way, not in the review:** the felt pads sit in 0.5 targets, so the record is 1.1 off the backplate, not the 1.6 every stack assumed. All stacks now use 1.1. The 7 in sconce had the same unsupported-centre problem as the 12 in (its 38 mm hole is wider than the 12 in ring); it gets a 47 x 39 backing ring. Durofelt does not stock the 1-1/4 x 3/8 x 1/16 cap felt (page read 2026-11-11): it is a die-cut part. The dome-cap RFQ drafts in `sourcing/rfq-drafts/` describe a 1 in stud; they are now bannered as superseded.

## MUST-FIX

| # | What changed (old -> new) | Where | Gate that proves it |
|---|---|---|---|
| M1 | Centre backing ring added: 31.75 x 9.5 x 1.6 felt on the backplate front face, concentric with the insert, same blank as the cap felt. None -> ring + scored witness circle D 32.4 (D 47.65 on the 7 in). Record seat 1.6 (assumed) -> 1.1 (real). Outer pads R 127 -> R 120. | `cad/sconce_cad.py:52`, `cad/sconce_cad.py:48`, backplate cut `cad/sconce_cad.py:281`, solid `cad/sconce_cad.py:534`, assembly `cad/assembly.py:68`, drawing `cad/drawings.py:204`, BOM line 6a | `centre_ring_loaded_top_minus_pad_top` = 0.0 (abs <= 0.05); `backplate_*_centre_ring_seat_found_in_the_solid` = 1; `record_back_face_above_backplate_front_face` = 1.1; interference 0 |
| M2 | D-key height 0.9 -> 0.55 (under the 0.72 thinnest PCB). Boss mouth: none -> counterbore D 8.3 x 0.4 + 0.2 chamfer. Spigot: run-out groove D 7.3 x 0.5 added. LED PCB: return ring bottom only -> both faces, stitched. Dome bore now modelled at its tap-drill D 7.46 and the assembly spigot at minor diameter, so the interference check can see a clash inside the thread. | `cad/sconce_lit.py:70`, `cad/sconce_lit.py:109`, `cad/sconce_lit.py:72`, `cad/sconce_lit.py:198`, `cad/sconce_lit.py:250`, `cad/label-light/pcb.py:64`, `cad/label-light/PCB-SPEC.md` | `pcb_min_top_minus_key_top` = 0.17 (>= 0.1); `boss_counterbore_dia_minus_key_dia` = 0.3; `core_key_top_measured_below_min_pcb_top` = 1; `dome_boss_counterbore_found` = 1; negative control (0.9 key fails) = 1 |
| M3 | Lip-to-louver and lip-to-window gap 0.05 -> 0.25 (lip face z 4.80 -> 5.00, cap 14.8 -> 15.0 tall). Datums toleranced on the sheets: column top 4.80 +/-0.02, boss face above lip face 0.60 +/-0.02, PCB 0.80 +/-0.08; both sheets say the boss is the stop. | `cad/sconce_lit.py:92`, `cad/sconce_lit.py:102`, `cad/sconce_lit.py:125`, `cad/drawings_lit.py:30`, `cad/drawings_lit.py:64` | `louver_top_to_dome_lip_gap` = 0.25; `lip_gap_minus_tolerance_stack` = 0.13 (>= 0.1); `lip_gap_measured_on_the_solids` = 0.25 |
| M4 | Flange web over the felt recess 0.3 -> no recess at all: solid 1.3 flange, flat underside on the PET washer. Lit cap felt deleted. | `cad/sconce_lit.py:61`, profile `cad/sconce_lit.py:213`, `cad/drawings_lit.py:62` | `flange_solid_thickness_under_the_cavity` = 1.3 (>= 0.8); `core_underside_has_no_felt_recess` = 1 |
| M5 | PET label washer added under every cap: 37.5 x 7.5 x 0.25 (7 in: 47.5 x 38.6). Plain stud 11.70 -> 11.95; lit stud 11.70 -> 11.65 (no felt, so its face is 0.3 lower: same tip depth, asserted). Plain recess 1.0 (+/-0.3) -> 1.00 +/-0.05. Felt specified by loaded height. | `cad/sconce_cad.py:168`, `cad/sconce_cad.py:180`, `cad/sconce_lit.py:29`, `cad/sconce_lit.py:56`, `cad/assembly.py:71`, BOM line 6b | `pet_washer_od_minus_flange_od` = 0.9 (>= 0.5); `pet_washer_od_minus_cap12_band_od` = -0.6 (hidden); `cap12_stud_tip_z_measured` = -11.95; `lit_tip_minus_plain_cap12_tip` = 0.0 |
| M6 | Centre contact: Mill-Max 0919, 2.24 usable, 0.09 margin -> gold plunger, 4.9 travel, inside a PEEK guard tube whose top (z 2.1) is a hard stop below any correct stud. Hub relief 4.5 -> 9.1. Return contact 0906 -> 0919 at 7.5 working height. Tolerance stack (low 0.94, high 1.29) printed in checks.md. Birch deleted from the backplate RFQ; thickness 12.70 +/-0.15 measured. | `cad/sconce_lit.py:141`, `cad/sconce_lit.py:150`, `cad/sconce_lit.py:172`, `cad/sconce_lit.py:340`, `cad/sconce_lit.py:359`, `cad/sconce_cad.py:107`, `cad/build_all.py:240` | worst-case thick record compression = 0.56 (>= 0.5); worst-case thin record tip above guard = 0.56 (>= 0.2); spring margin with a stud on the guard = 0.7 (>= 0.3); return pin 6.79..8.01 inside 6.63..8.87 |
| M7 | RS-CAP-7 stud 15.875 -> 12.6, with an assert on tip position against RS-CAP-12. Bonded cap on a 1 in bolt superseded in the BOM. Any other screw stops on the guard tube. | `cad/sconce_cad.py:191`, `cad/sconce_cad.py:203`, `build/BOM.md` line 4 | `cap_7in_tip_minus_cap_12in_tip` = 0.018 (abs <= 0.05); plain cap and 7 in cap tips above the guard, worst case = 0.26 / 0.21 (>= 0.2) |
| M8 | Bore plain D 3.15 x 13.5 -> stepped: D 3.15 x 10.00 then D 2.2 (sleeve seats on the shoulder). Pin plain D 1.588 -> headed D 2.4 x 0.5, head in a D 2.5 x 0.55 counterbore in the sleeve tip. Loctite 609 and staking deleted. Pin recess 0.05 +0.05/-0. | `cad/sconce_lit.py:38`, `cad/sconce_lit.py:41`, `cad/sconce_lit.py:308`, `cad/drawings_lit.py:148` | `core_bore_shoulder_found` = 1; `sleeve_top_z_minus_bore_shoulder_z_measured` = 0.0; `pin_head_minus_sleeve_bore` = 0.8; `plunger_to_brass_margin_worst` = 0.42 (>= 0.3) |
| M9 | Dog point "4.8" (+/-0.3, so 5.1 against a 4.98 insert) -> 4.80 +0/-0.10. Stud +/-0.1 -> +/-0.05. Recess, column top, boss step, bore step, sleeve, pin all toleranced on the sheet. Core dimensioned with dimension lines. `sheet()` now sizes the title block to its text and raises if notes or title block would cross the border (the tolerance line used to be below it). EN 5 um max, thread to accept a 2B GO gauge after plating. DATE 2026-11-09 -> 2026-11-11. | `cad/sconce_cad.py:183`, `cad/drawings.py:105`, `cad/drawings.py:113`, `cad/drawings.py:361`, `cad/drawings_lit.py:52` | `insert_minor_min_minus_dog_point_max` = 0.18 (>= 0.1); lowest note line y = 0.029 and lowest title-block line y = 0.0216 (border 0.010); tolerance line on 19 of 19 sheets |
| M10 | Panel jack (D 8.0 hole, mouth 7.5 mm off the wall) -> 150 mm 18 AWG pigtail with an inline female 5.5 x 2.1 jack, P-clipped in the rear pocket (pilot D 2.4 at (-9.5, 4)). Cable hole D 6.5. Rear pocket 16.5 deep, to y 28.5 -> 12.0 deep, to y 22. In-wall hole 1-1/4 in offset -> 1 in on the plate centre. | `cad/sconce_cad.py:95`, `cad/sconce_cad.py:100`, `cad/sconce_cad.py:572`, `cad/sconce_cad.py:601`, hub cut `cad/sconce_cad.py:360`, `mounting-report.md`, `site/install.html`, BOM line 11 | everything stays 1.55 mm in front of the wall plane (>= 0.5); mated plug ends 9.85 mm inside the backplate edge; jack passes a centred 1 in hole with 13.9; `hub_has_no_panel_jack_hole` = 1; `hub_p_clip_pilot_found` = 1 |
| M11 | See the table below. | | document gates in checks.md, all 0 stale / 1 required |

### M11 contradictions

| | Was | Now | Where |
|---|---|---|---|
| a | BOM and README: cap felt 1 x 3/8 x 1/8 (SAW1GY) | 1-1/4 x 3/8 x 1/16, die-cut (not a Durofelt stock size, checked) | `build/BOM.md` line 5, `cad/README.md`, `cad/sconce_cad.py:162` |
| b | RFQ said 6 felt pockets, STEP had 3 | 6 in the STEP (probed), outer pads at R 120; the guard now raises instead of skipping | `cad/sconce_cad.py:44`, `cad/sconce_cad.py:271` |
| c | Alt stud "cut to 17.7" (really 10.7 exposed) | Option deleted; one-piece only | `cad/build_all.py:323` |
| d | Install sheet says clockwise, J-slots locked anticlockwise | J-slot entries mirrored (stud angle +20 -> -20): locks clockwise, and cap tightening seats the bayonet | `cad/sconce_cad.py:85` |
| e | BOM: shoulder screws, M3 x 6, 1 in hole, jack at 6 o'clock | PEM FH-832-10 + lock nuts, M3 x 12, 30 x 37 slot, pigtail hole at (0, +15) | `build/BOM.md` lines 2, 12, 13, 14 |
| f | Site: 4 to 10 W | about 4 W, up to 6 W | `site/faq.html`, `site/product.html`, `site/index.html`, `site/_gen/pages.py` |
| g | Site and renders: record lifts off a post | Copy fixed (the stud is part of the cap). Renders flagged, not redone | site files above, `renders-final/README.md`, `NOTES.md` |
| h | checks.md prose hard-coded (5/8 stud, 1.3..2.4 records) | Every sentence printed from parameters | `cad/build_all.py:154` |
| i | Renders: LED ring on the back face. CAD: rim | CAD, drawings, BOM, site and DESIGN.md all say RIM. Render discrepancy recorded as an open decision | `NOTES.md` (2026-11-11), `START-HERE.html`, `build/BOM.md` line 8 |
| j | Z1 12 V bidirectional on both boards | Cap: 12 V unidirectional. Hub: 15 V standoff | `cad/label-light/PCB-SPEC.md`, `cad/label-light/pcb.py:60` |

## SHOULD-FIX

| # | Status | What |
|---|---|---|
| S1 | Done | Smooth D 7.10 +0/-0.05 x 2.0 shoulder under RS-CAP-12 and the lit core: the record centres on it with 0.14 to 0.27 slop instead of 0.9 on thread crests. `cad/sconce_cad.py:172`. No fixed pilot bushing was added (it would collide with the shoulder). |
| S2 | Not done | Low-set urethane instead of felt for the backing ring and cap washer. Needs a bench comparison; noted in DESIGN.md failure modes. |
| S3 | Part | Flangeless anchors are now in the BOM. The 0.6 mm bayonet play is unchanged. |
| S4 | Part | Rabbet is now painted (drawing + RFQ). Copy and BOM say about 4 W, 6 W max. No aluminium flat under the strip; no thermal test exists yet. |
| S5 | Part | F1 100 mA PTC on the label tap and "12 V DC ONLY" marking note added. The rail PTC + TVS against a 24 V adapter is specified in PCB-SPEC.md but is not a designed board. |
| S6 | Part | Spigot lead-in 0.3 -> 0.6 (capture 0.69 against a 0.5 float); insert minor range 4.98..5.26 carried. The insert's real back-end land is still unmeasured. |
| S7, S8 | Done | Core finish note rewritten (nickel everywhere, mask from paint only; activator for Loctite 270). Cross-hole note corrected: it breaks out at the edge of the column top. |
| S9 | Not done | Louver locating step. Channel tolerance relaxed to +/-0.05 with a first-article check. |
| S10 | Done | Label fading disclosed in DESIGN.md failure modes. Not on the public site (the lit cap is not sold there yet). |
| S11 | Done | Rack on the stud only, mask do-not-chase, R 0.2 at the relief root, drawing date, README cap mass (54.8 g). |
| S12 | Done | UL sentence on the site reworded. |

## Could not fix, and why

- **The centre contact is unproven.** It replaces a catalogue part with a custom plunger and an unpicked spring. The geometry checks out and is gated; whether it makes reliable contact for years is a bench question.
- **Unverified purchased parts:** the contact spring, the inline-jack pigtail (envelope assumed D 11.5 x 28), the die-cut felt and PET vendors, the TVS part numbers, the flat land on the back of the E-Z Lok insert, the Mill-Max 0919 barrel diameter.
- **Felt compression (0.5 mm assumed)** sets record flatness at the centre. It needs one measurement on a first article.
- **Prices were not re-quoted.** `build/cost-model.py`, `BOM.csv`, `assembly-SOP.md` and `sample-kit-shopping-list.md` still price and describe the bonded cap and panel jack; they carry banners. BOM lines 6a and 6b are not in the totals.
- **Renders not redone.** The phantom post and the back-face halo remain in the product images; the lit-cap renders show the rev A cap (0.2 mm shorter, and with a different contact that is not visible).
- **Force and stress figures in the review** (dish under clamp load, flange stress, preload decay, strip temperature) are hand calculations there and here. No FEA or thermal run was done.
- **HTML copies:** the `.md` to `.html` mirror was regenerated with `_publish/md2html.py`; the published GitHub Pages copy was not touched.
