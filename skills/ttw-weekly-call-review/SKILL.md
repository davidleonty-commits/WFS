---
name: ttw-weekly-call-review
description: Build the TikTok Wiz weekly sales call review from Avoma transcripts, grading every consultation into lead-quality buckets (RED, GREEN, GREY, BLUE, ORANGE) backed by the lead's own verbatim financial statement, and producing a two-tab workbook, a Google Sheet, and a management summary with FDQ opportunity-cost economics. Use this whenever Caydo or anyone at WFS asks for the weekly or monthly call review, a call report, a lead quality report, an FDQ report, a bucket breakdown, a rep scorecard from calls, "how many of our leads could not afford it", or wants calls over 30 minutes pulled and graded. Also use it to re-grade, audit, verify, or extend an existing call review to a new date range. Trigger even if the person does not say "skill" or name the buckets.
---

# TTW Weekly Call Review

Produce a defensible lead-quality and rep-performance report from Avoma sales call transcripts.

The entire value of this report is that **every RED is backed by something the lead actually said.** An untraceable number is worse than no number, because it gets carried into a coaching conversation and lands on a rep who did nothing wrong. Grade conservatively, cite verbatim, and prefer "we do not know" over a confident guess.

## Two non-negotiables

### 1. The reporting week is Monday to Sunday

Unless the requester names explicit dates, the window is **the current week: Monday 00:00 through Sunday 23:59**. If the skill runs mid-week, the window is **Monday 00:00 through the moment of the run**.

Compute it, then state it back before pulling: "Pulling calls for Mon 18 Aug through Sun 24 Aug" or "Mon 18 Aug through now (Thu 21 Aug)". Any explicit dates the requester gives override this entirely, including multi-week and month-to-date ranges.

Times are UTC in the connector. The team works US hours, so build the window from the user's local Monday and convert.

### 2. Nothing ships on a single pass

Single-pass grading on this report has been wrong roughly **30% of the time**, every time it has been checked. Accuracy matters more than turnaround here. The multi-agent review in `references/review-workflow.md` is mandatory, not optional, and its QA gates must pass before you report any number.

Never present figures without saying how many rows were independently verified and where the residual uncertainty sits.

## Workflow

### Step 1 — Scope and pull

Confirm the window per the rule above, then:

```
mcp__Avoma_MCP__list_meetings
  from_date: <ISO start>   to_date: <ISO end>
  page_size: 100
```

Paginate to the end (follow the `next` link until it is null), then keep only recorded consultations over 1800 seconds, since consultations run over 30 minutes. If the Avoma MCP is unavailable, the same sweep is `GET https://api.avoma.com/v1/meetings/` with `{from_date, to_date, page, page_size}` and header `Authorization: Bearer $AVOMA_API_KEY`.

The result usually exceeds the inline token cap and is written to a file. Parse it with python. Never read a whole persisted tool result into context.

Reps are identified by the meeting's **organizer email**, not by a connector rep id. Resolve an email to a name through the WFS Active Sales Team Roster sheet. Never join on a display name: the roster carries duplicate full names, and Avoma mislabels speakers.

**Exclusions.** Drop internal team syncs and any calls run by the sales director themselves. They are not consultations and they distort every rate. State what you excluded.

### Step 2 — Get complete transcripts

Read `references/transcript-integrity.md` before pulling. Truncated caches are the single largest source of wrong numbers on this report: many stop at exactly the first Avoma chunk, before the price is ever stated, so a call reads as "money never discussed" when the lead actually declined a lender two minutes later.

Every transcript must pass a completeness check before it is graded.

### Step 3 — Grade

Read `references/bucket-definitions.md` in full. It carries the buckets, the core RED test, the ten failure modes that have produced real misgrades, and the evidence-weighting rules.

The habit that matters most: **find where the price is first stated, read the next five minutes word by word, then read to the end of the call.** Capacity statements routinely land ten minutes after the lead's first reaction, and reviewers who stop at the reaction get it wrong.

### Step 4 — Multi-agent review and QA

Follow `references/review-workflow.md`. Two independent blind reviewers per call, a neutral third on every disagreement, then the automated QA gates. Do not skip the gates because the numbers look plausible.

### Step 5 — Build the deliverables

Follow `references/report-spec.md` for the column layout, the Report tab, the economics, and the summary templates.

### Step 6 — Report honestly

State the window, the exclusions, the verification coverage, and anything unscored. If a call has no transcript in either system, mark it NA and unscored rather than guessing.

## Flagging compliance and lead safety

While grading, record verbatim and without softening:

- card numbers, CVVs, expiry dates, bank routing or account numbers, or SSNs spoken aloud
- a rep coaching a lead to overstate income on a credit application
- financing pushed on a lead on disability, with no income, or who said they cannot afford it
- income or earnings guarantees, or "everyone gets approved" claims
- a lead's stated inability overridden rather than qualified

Keep these out of any broad channel message. Summarise that they exist and hand the detail over directly. Naming reps in a searchable channel before they can respond is unfair to them and unhelpful to the business.

## Tone for the written cells

Closing notes lean slightly in the rep's favour: lead with what they did well, state the gap once, plainly, without piling on, and keep every number, date and follow-up commitment intact. Do not invent a positive. Compliance and lead-safety findings are the exception and stay stated plainly.

Rep scores get the benefit of the doubt. A reasonably handled call that did not close is a 6 or 7. Below 5 is for a clear breakdown of fundamentals. Honest disqualification of someone who cannot afford the program is good work and scores well.

## Reference files

- `references/bucket-definitions.md` — buckets, the RED test, ten failure modes, evidence weighting. Read before grading.
- `references/transcript-integrity.md` — completeness checks, pagination, speaker labels, mangled figures, tooling. Read before pulling.
- `references/review-workflow.md` — the multi-agent review process, agent prompts, and QA gates. Mandatory.
- `references/report-spec.md` — columns, Report tab, FDQ economics, Slack and workbook templates.
