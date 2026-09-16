---
name: sip-watch-loop
description: Closed-loop coaching outcome tracker for David's closer and setter fleet. Turns one-directional call reviews into an improvement engine by logging every SIP-relevant behavior flagged in a review to a durable SIP Watch Ledger, then auto-checking that rep's next calls for that specific behavior and reporting per-rep status (new, watching, clearing, persistent) until it clears or escalates with an evidence bundle. Use whenever a call review flags a coachable behavior, whenever David says "SIP watch", "SIP status", "is [rep] still doing X", "did the coaching stick", "who is clearing and who is persisting", or "check his last calls for [behavior]", and in any daily or weekly call report, which should carry a SIP Watch section. Also use when David wants escalation evidence for a rep whose flagged behavior is not changing. Composes with closer-call-review, setter-call-review, ttw-daily-call-review, and ttw-daily-avoma-report; it adds the memory layer those reviews lack.
---

# SIP Watch Loop

Call reviews without follow-through are content, not coaching. This loop closes the gap: every behavior a review flags gets logged, tracked across that rep's next calls, and resolved to one of two endings: cleared with evidence, or escalated with evidence. Nothing flagged is allowed to just evaporate.

## Non-negotiables

1. **Never use em dashes.** Anywhere, including ledger entries and Slack output.
2. **Evidence or nothing.** A behavior is only "present" in a call if it can be quoted or timestamped from the transcript. A behavior is only "absent" if the situation where it would occur actually arose and the rep handled it differently. A call with no objections proves nothing about objection handling.
3. **The ledger is the single source of truth.** Never reconstruct watch status from memory of past conversations. Read the ledger, then write to it.
4. **Delivery rules apply.** Any Slack output goes out with `slack_send_message` on the claude.ai Slack connector, one sender, routed to the director's DM while in test mode. The ledger is this skill's only write target; never touch the salesboard or any other resource doc.
5. **This tracks coaching follow-through, not gotchas.** The tone in any output is a coach checking that reps are getting better, not building a case by default. The case builds itself only when the behavior persists.

## The ledger

A Google Sheet named **SIP Watch Ledger** in David's Drive. On first run, search Drive for it; if missing, create it and report the new file. Columns:

| Column | Content |
|---|---|
| entry_id | date + rep + short slug, e.g. 2026-07-19-vidush-price-drop |
| date_flagged | date of the review that opened the watch |
| rep | closer or setter name |
| behavior | the specific behavior, stated as the observable action, not a vibe. "Drops price before pinning the budget question" not "weak on money talk" |
| sip_link | whether this maps to an item on the rep's current SIP, and which |
| source_call | call ID or Avoma link plus timestamp of the flagged moment |
| evidence_quote | verbatim line from the source call |
| status | new / watching / clearing / cleared / persistent / escalated |
| calls_checked | running count of subsequent calls checked |
| calls_present | count of checked calls where the behavior appeared, with call IDs |
| calls_absent | count of checked calls where the situation arose and the rep handled it right, with call IDs |
| last_checked | date of most recent check |
| notes | short free text, including the coaching given |

## The loop

### Write side: opening a watch

When any call review (closer or setter, script or Slack variant, or the daily batch) flags a behavior worth coaching:

1. Read the ledger first. If an open watch already exists for this rep and behavior, do not open a duplicate; update the existing entry (increment calls_present, add the new call as evidence, refresh last_checked).
2. Otherwise append a new row with status **new**, the verbatim quote, and the source call link.
3. Keep watches specific and few. One rep should rarely carry more than three open watches; if a review surfaces five issues, log the one or two highest-leverage behaviors and note the rest in the review itself. A watch list nobody can hold in their head protects nobody.

### Check side: watching the next calls

Whenever this rep's subsequent calls get processed (daily report, a new single-call review, or an explicit "check his calls" ask):

1. Read the ledger for the rep's open watches before analyzing the calls, so the check is targeted.
2. For each open watch, examine each new call: did the situation where the behavior lives arise? If yes, was the behavior present or handled correctly? Quote or timestamp either way. If the situation never arose, the call counts toward neither column; note it as checked.
3. Update the row: counts, call IDs, last_checked, and status per the state rules below.

### State rules

- **new to watching:** first subsequent call checked.
- **watching to clearing:** the last 3 consecutive situation-relevant calls show correct handling.
- **clearing to cleared:** 5 consecutive situation-relevant calls clean. Log the clear date. Cleared watches stay in the ledger as history; they are the receipts that coaching works.
- **watching to persistent:** behavior present in 3 or more of the last 5 situation-relevant calls, or still present in any call more than 14 days after date_flagged with at least 4 calls checked.
- **persistent to escalated:** only when David says to escalate, or when a persistent watch crosses 21 days. Escalation produces the evidence bundle below; it never fires silently.

A cleared behavior that reappears within 30 days reopens as a new row marked "relapse of [entry_id]" and starts at watching, not new. Relapses are worth calling out plainly.

### Read side: the SIP Watch section

Any daily or weekly report that covers reps with open watches carries a **SIP Watch** section, one line per open watch:

```
SIP WATCH
Vidush: price-before-budget | watching | clean 2 of last 3 (trending right)
Tom: skips decision-maker check | persistent | present 4 of last 5, day 16
Crue: no open watches
```

One line per watch, status plain, trajectory named. Reps with no open watches get one line saying so, because a clean sheet is information too.

### Escalation bundle

When a watch escalates, produce a tight packet to David's DM:

- Rep, behavior, date flagged, days open, coaching given (from notes).
- The evidence table: every checked call, date, present or absent, quote or timestamp.
- The cost: one or two lines on what this behavior is plausibly costing (a specific lost deal from the checked calls if one exists, otherwise the mechanism).
- Recommended next step, stated as a recommendation, not an action taken.

The bundle exists so a SIP conversation runs on receipts instead of recollection. David decides what happens with it.

## Weekly hygiene pass

Once a week (or when asked), sweep the ledger: close out anything cleared, flag watches with stale last_checked older than 7 days as needing calls pulled, and give David a two-line fleet summary: how many watches opened, cleared, and persisting this week. The cleared-to-opened ratio over time is the honest measure of whether the coaching system works.
