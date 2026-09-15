---
name: compliance-trend-loop
description: Rolling compliance pattern tracker for Caydo's TTW sales fleet. Turns stateless per-call compliance flags (income coaching on financing applications, guarantee language, exclusive partnership claims) into per-rep rolling 30-day trends with hard escalation thresholds and auto-built evidence packets containing verbatim quotes and call links. Use whenever any call review or daily report flags a compliance issue, whenever Caydo says "compliance trend", "compliance ledger", "who keeps flagging", "how many times has [rep] done this", "build the compliance packet", "escalation evidence", or asks whether a compliance issue is a one-off or a pattern. Also use in every daily and weekly call report, which should carry a compliance trend line, and when preparing any escalation to WFS leadership about rep conduct. Composes with closer-call-review, setter-call-review, ttw-daily-call-review, and ttw-daily-avoma-report; every compliance flag those produce must land in this ledger.
---

# Compliance Trend Loop

A compliance flag on one call is an anecdote. The same violation three times in thirty days is a pattern with a paper trail, and patterns are what leadership acts on and what protects the program if a deal goes sideways. This loop makes every flag land in a durable ledger, computes rolling per-rep trends, and builds the escalation packet automatically when a threshold trips. Same detection work Caydo already does; the output becomes defensible instead of disposable.

## Non-negotiables

1. **Never use em dashes.** Anywhere, including ledger entries and packets.
2. **Verbatim or it did not happen.** Every ledger entry carries the exact quoted line from the transcript and the call link with timestamp. A compliance entry without a quote is invalid; paraphrase is not evidence when the stakes are conduct.
3. **Grade the line, not the rep.** An entry records what was said on a specific call. Trend math does the pattern reading; individual entries stay factual and neutral. No editorializing in the ledger.
4. **Borderline gets logged as borderline.** If a line is arguably compliant, log it with severity "borderline" and the reason it might cross, rather than either dropping it or inflating it. Borderline entries count toward watch awareness but never toward escalation thresholds on their own.
5. **Escalation packets go to Caydo only.** This loop never sends anything to leadership, the rep, or any channel on its own. It builds the packet, delivers it to Caydo's DM through the Lovable WFS Slack connector (test-mode routing rules apply), and he decides. The ledger is this skill's only write target.

## The ledger

A Google Sheet named **Compliance Ledger** in Caydo's Drive. On first run, search Drive for it; if missing, create it and report the new file. Columns:

| Column | Content |
|---|---|
| date | date of the call |
| rep | closer or setter name |
| violation_type | one of the standard types below |
| severity | clear / borderline |
| call_link | Avoma link or call ID with timestamp of the moment |
| quote | the verbatim line or exchange |
| context | one neutral line on the situation (what the prospect asked, where in the call) |
| flagged_in | which review or report surfaced it |
| coached | blank, or date and one line when the rep was addressed on it |
| escalated | blank, or date the packet went to Caydo |

## Violation types

The standard set, so trends aggregate cleanly:

- **income_coaching:** coaching a prospect on what income to state on a financing application, or suggesting numbers.
- **guarantee_language:** promising or implying guaranteed results, income, or outcomes without basis.
- **exclusive_partnership:** claiming exclusive partnerships, endorsements, or affiliations that do not exist as stated.
- **pressure_misrepresentation:** fake scarcity, invented deadlines, misstating refund or contract terms.
- **other:** anything else, with a one-line label; if the same "other" appears twice, promote it to a named type.

The type list lives on a **Types** tab of the same sheet so new categories get added once and used consistently.

## The loop

### Write side: every flag lands

When any call review or daily report detects a compliance issue:

1. Read the ledger first. If this exact call and line is already logged (the daily report and a single-call review can both catch the same moment), do not duplicate; enrich the existing row if the new review adds context.
2. Append the row with the verbatim quote, link, type, and severity.
3. The review or report that surfaced it still says whatever it says; the ledger entry is additional, never a replacement for the in-review flag.

### Trend side: rolling 30-day math

Whenever the ledger is written, and in every daily and weekly report, compute per rep:

- Count of clear-severity entries per violation_type in the trailing 30 days.
- Total clear entries across types in the trailing 30 days.
- Days since last entry.

Report format, one line per rep with any trailing-30 activity:

```
COMPLIANCE TREND (trailing 30 days)
Turok: guarantee_language x2 (Jul 3, Jul 15), threshold 2 hit, packet built
Paul: income_coaching x1 (Jul 11), coached Jul 12, clean since
Rest of fleet: clean
```

Reps with nothing in the window get covered by one collective clean line.

### Thresholds

Computed on clear-severity entries only, per rep:

- **1 in 30 days:** coaching note. The next review of that rep addresses it directly; log the coached date.
- **2 of the same type in 30 days:** formal flag. The rep's next written review carries a compliance section naming both instances with quotes, and the trend line marks the threshold hit. Packet gets built and sent to Caydo's DM.
- **3 total clear entries in 30 days, or 2 of the same type after a coached date:** escalation packet to Caydo's DM marked as leadership-ready, with the recommendation that this leaves the coaching lane. Repeat-after-coaching is the aggravator that matters most, because it converts "did not know" into "was told and continued."

Income_coaching on financing applications carries extra weight: a second clear instance is automatically leadership-ready regardless of the 30-day math, because the downstream risk is not a bad sale, it is fraud exposure.

### The packet

Built automatically at any threshold, delivered to Caydo's DM:

- Rep, violation_type(s), window covered, coached history.
- Evidence table: every entry, date, quote, call link, severity. Quotes exact, links live.
- The pattern in two lines: frequency, whether it survived coaching, trajectory.
- Risk statement: one or two lines on the specific exposure this pattern creates for the program (chargeback ammunition, financing fraud exposure, FTC-style claims risk), stated factually.
- Recommendation, clearly labeled as a recommendation.

The packet must stand on its own in front of someone who has never heard of the rep. That is the standard.

### Decay and hygiene

Entries never get deleted; the rolling window handles decay naturally. A rep whose last clear entry ages past 30 days drops off the trend line, and if they were previously at a threshold, the next weekly report notes the recovery in one line, because clean streaks after coaching are the success signal this loop exists to produce. Monthly, sweep for borderline entries piling up on one rep (3 or more borderlines in 30 days is itself worth a coaching note even though no threshold tripped) and confirm every clear entry has its quote and link intact.

## The honest metric

Over time, the number that matters is **repeat-after-coaching rate**: the share of coached reps who log another clear entry of the same type within 30 days of the coached date. Low means the coaching lane works and escalations stay rare. High means the coaching lane is theater and Caydo needs to know that plainly.
