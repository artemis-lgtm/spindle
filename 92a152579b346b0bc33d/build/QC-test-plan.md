# QC and test plan (build/QC-test-plan.md)

> **SUPERSEDED IN PART, 2026-11-11 (heat-safe layout, `../cad/FIXES-heat-layout.md` and `../cad/THERMAL.md`):** on the 12 in unit the LED strip is now on the BACK of the backplate on an aluminium ring over a cork ring, not on the rim. Test 1 points T1 (strip face at 3 o'clock on the rim) and T2 (rim wood beside the strip) no longer exist as described. Measure instead: the strip face from behind (limit under 55 C), the aluminium ring, and the record's BACK face 114 mm from the centre, at the top edge and under the cap (limit: no more than 5 C above the room). The record-face limits in this plan are unchanged. This plan has not been rewritten.

Prepared 2026-11-10. Five tests. Tests 1 to 4 run on all three prototypes and on the first 10 production units; tests 2 to 4 run on every production unit as a 90-second check; test 5 runs on three packed boxes before the first shipment. Acceptance limits come from engineering-report.md section 3 (heat) and the mounting report (mount); shipping limits are an ISTA 3A-lite reading of the real ISTA 3A procedure for small parcels, scaled to one home-built drop rig.

Equipment: IR thermometer with emissivity set to 0.95, a room thermometer, a 1-gallon water jug (8.3 lb), a #8 screw-and-loop hook, a tape measure, a phone camera at 240 fps (slow-motion mode), a bathroom scale, a hard floor (concrete garage or tile), masking tape, the pass/fail sheet in section 6.

## 1. Heat soak, 2 hours

Why: vinyl softens around 55 to 60 C and creeps under load from about 30 to 38 C over long periods (engineering-report.md section 3). Our target, which we print on the product page once measured, is record face under 35 C in a 24 C room.

Setup: unit mounted on a plain painted drywall or plywood panel exactly as it ships (1" wall gap, record clamped on the pads), in a still room with no sun on it. Record the room temperature at the start. Adapter and dimmer at FULL brightness (worst case). Record a reading at 0, 15, 30, 60, 90 and 120 minutes at each of these points, IR from 4" away:

| Point | Where | Limit at 120 min |
|---|---|---|
| T1 Strip surface | The COB face at 3 o'clock on the rim | under 60 C (strip makers' substrate limit) |
| T2 Backplate rim, wood | 1/4" inboard of the strip, on the painted rim | under 45 C |
| T3 Record back face | Through the gap at the 6 o'clock edge, aimed at the vinyl at the 5" pad radius | under 35 C, and no more than 8 C over room |
| T4 Record label, front | Centre of the label beside the dome | under 35 C |
| T5 Dome cap | Top of the chrome dome | under 35 C (it is a touch point) |
| T6 Adapter body | The wall-wart case | under 50 C (typical Class 2 adapter case limit, UL 1310 class) |
| T7 Wall behind the hub | Through the gap, the wall surface at 12 o'clock | under 35 C |
| T8 Room | Thermometer 6 ft away | log only |

Pass: all limits met at 120 minutes AND the 90 to 120 minute readings differ by under 1 C (steady state reached). Fail: any limit exceeded, or still rising at 120 minutes (extend to 180 and re-judge; if still rising, fail). After the soak: unclamp the record, lay it on a flat table, sight the edge against a straightedge; any new dish or ripple = fail.

Repeat once at minimum dimmer (PWM at low duty cycles can run some drivers warmer) and log T6 only.

Then run one unit for 48 hours continuously at full brightness, repeat the straightedge check on the record. Log only; this is the "lives on a wall" confidence test.

## 2. Mount: pull, drop, bump

Why: a 12" lever arm on a 1.5 lb fixture; a sconce that lifts off when a door slams is a returned sconce and a cracked record.

Install per mounting-report.md: steel plate on two #8 screws into drywall anchors (worst case; no stud), hub twist-locked, set screw turned in.

| Test | Method | Pass |
|---|---|---|
| 2a Static pull, down | Hook J6 on the dome stud (record removed), hang the 8.3 lb jug for 60 seconds. That is 5x the fixture weight. | No movement of plate or hub; set screw still seated; anchors not loosened (check by hand). |
| 2b Static pull, out | Pull straight away from the wall on the hub rim with a luggage scale to 10 lb for 10 seconds. | Hub does not come off the studs; no visible gap opening between plate and wall. |
| 2c Twist | With the set screw IN, try to untwist the hub by hand, hard (about 10 lb-ft, two hands on the rim). Then back the set screw OUT and repeat. | Set screw in: no rotation. Set screw out: rotates and lifts off only with the 20 degree twist, never by a straight pull. |
| 2d Bump | Record clamped. Strike the record's edge at 3 o'clock with the heel of a hand, five times, hard enough to hear it (about a door slam). Repeat at 12 o'clock downward. | Record does not rotate on the pads more than 2 degrees (mark the edge with tape first); dome does not loosen; hub does not shift on the plate. |
| 2e Record swap x20 | Unscrew the dome, lift the record off, set it back, screw on. Twenty cycles. | The insert does not loosen in the MDF (check with a torque of finger-tight plus 1/4 turn, no spin); the dome stud does not turn in the epoxy; felt washer still attached. |
| 2f Drop (unit, not packaged) | Fixture face-up (record off) dropped 12" onto carpet over concrete, hub down, once. Simulates a slip while hanging. | Strip still fully lit; no hub-to-plate glue crack; jack still tight. |

Any fail on 2a to 2c is a design stop, not a unit reject: change the anchor spec or the slot geometry before the next unit.

## 3. 7" and the keyhole plate

The 7" uses the Hardwick keyhole (a third the weight). Run 2a with a 3 lb weight and 2d only. Pass: no lift-off, no rotation beyond 2 degrees.

## 4. Dimmer flicker

Why: PWM dimmers at low duty cycles can strobe on camera and on some eyes; the product sells on photos and video.

| Check | Method | Pass |
|---|---|---|
| 4a Eye | In a dark room, sweep the dimmer slowly from full to minimum and back, twice, looking at the halo on the wall and at the strip edge. | No visible flicker, stepping or colour shift at any point; smooth to about 5% before cut-off. |
| 4b Camera | Phone in 240 fps slow-motion, 10 seconds at full, at 50% and at the lowest visible setting; play back. Then a normal 30 fps video at each. | 30 fps: no rolling bands. 240 fps: banding is allowed (every PWM shows it) but the 30 fps hero video must be clean. If 30 fps shows bands, the PWM frequency is too low; swap to a higher-frequency dimmer (the Ecolocity LC-OL-8DIM spec sheet gives its frequency; log it). |
| 4c Minimum | Note the lowest dimmer position that keeps every COB segment lit. | Whole ring lit at minimum; no segment drops out earlier than the rest. |
| 4d Warm-up colour | IR not needed. Photograph the halo at 0 and 30 minutes, same exposure. | No visible colour drift (CRI 90+ 2700K should hold). Log only. |
| 4e Adapter hum | Ear 6" from the adapter and from the dimmer at 50%. | No audible whine in a quiet room. Hum = reject that adapter unit. |

## 5. Packaging drop test (ISTA 3A-lite)

Why: a 12" record in a flat box is a frisbee; the dome is the premium signal and a dented dome is a refund.

Based on ISTA 3A for parcels under 150 lb: drop sequence on corners, edges and faces from a height set by weight (for under 20 lb ISTA 3A uses 18"; we use 30" for the three test boxes because small-parcel carriers are rougher than the standard assumes, then 18" for any later re-test). Three packed boxes, each with a real record, dome, adapter and card. Hard floor.

Sequence per box (10 drops):
1. Corner: the bottom corner where the record edge sits closest to the box wall, 30".
2 to 4. The three edges radiating from that corner, 30".
5 to 10. All six faces, 30".
Then: a 10-second vibration stand-in: carry the box down a flight of stairs at a trot and back up (ISTA 3A's vibration table is not available; log that this was substituted).

Open and inspect:

| Item | Pass |
|---|---|
| Record | No crack, chip or new warp (straightedge). |
| Dome cap | No dent, no scratch through the polish, stud still rigid in the epoxy. |
| Backplate | No corner chip in the MDF, strip fully adhered, lights on first plug-in. |
| Hub | Not cracked at the jack pocket or the J-slots; still glued flat. |
| Box | Outer box may be scuffed; no puncture; foam corners intact; nothing migrated. |

Pass = 3 of 3 boxes pass every row. 2 of 3 = change the foam (add a die-cut pad over the record) and re-test. Record the box weight of each (cost-model.md needs the real 3 to 4 lb).

## 6. Pass/fail sheet (one per unit; print and keep in the build log)

```
Unit #: ______   Date: ______   Builder: ______   SKU: Kit / Sconce / 7" / Set   Cap: Chrome / Brass / Black
Room temp at start: ____ C

HEAT (prototypes + first 10 only)        0   15   30   60   90  120 min   Limit     P/F
T1 strip surface                        __  __   __   __   __   __       <60 C      __
T2 rim wood                             __  __   __   __   __   __       <45 C      __
T3 record back @5" radius               __  __   __   __   __   __       <35 C, <room+8   __
T4 record label                         __  __   __   __   __   __       <35 C      __
T5 dome                                 __  __   __   __   __   __       <35 C      __
T6 adapter case                         __  __   __   __   __   __       <50 C      __
T7 wall behind hub                      __  __   __   __   __   __       <35 C      __
Steady at 120 (90->120 delta <1 C)                                                  __
Record flat after soak (straightedge)                                               __

MOUNT (prototypes + first 10; 2d and 2e every unit)
2a 8.3 lb hang 60 s, no movement                                                    __
2b 10 lb pull-out 10 s                                                              __
2c twist: locked with set screw / releases only by twist                            __
2d bump x5 at 3 and 12 o'clock, rotation <2 deg                                     __
2e swap x20: insert tight, stud rigid, felt on                                      __
2f 12" drop onto carpet, still lit                                                  __

ELECTRICAL (every unit)
Polarity tester red = centre positive                                               __
Full brightness, all segments lit 60 s                                              __
4a eye sweep, no flicker                                                            __
4b 30 fps video clean at full / 50% / min                                           __
4c whole ring lit at minimum                                                        __
4e no adapter or dimmer whine                                                       __
Hot glue strain relief present at strip and in channel                              __

PACK (every unit)
Dome bagged, 45 adapter, adapter+dimmer, mount bag, card, shake test silent         __
Box weight: ____ lb

PACKAGING DROP (3 boxes before first ship)   Box A __  Box B __  Box C __

RESULT:  PASS / FAIL    Notes: ____________________________________________
```

## 7. What gets printed on the product page after the prototypes pass
"Tested: record surface stays within X C of room temperature after two hours at full brightness (measured with an IR thermometer on prototype units). Mount holds 5x the fixture's weight. Nothing in the fixture carries more than 12 volts." Fill X from T3. Do not publish until measured.
