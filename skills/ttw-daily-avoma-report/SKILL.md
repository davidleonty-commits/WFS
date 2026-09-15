---
name: ttw-daily-avoma-report
description: Automated daily TikTok Wiz call report delivered to Caydo's own Slack DM. Use this whenever the daily call report needs to run on its own, or whenever Caydo says "run the daily call report", "send me today's call report", "run today's calls", "daily DM report", "run the call report", or any request to pull, score, and DM today's sales consultation calls. ALSO trigger this when a scheduled task fires to produce the 6 PM daily report. This skill pulls every Avoma call from the current day that has a recording over 15 minutes, scores each one on the strict evidence-based rubric, formats the summary report, and sends it straight to Caydo's Slack DM with no draft step. Use this skill even when the request sounds simple, because the pull window, the 15-minute floor, the strict scoring, and the DM delivery all have specific rules that protect the report's accuracy.
---

# TTW Daily Avoma Report (auto-DM)

This skill runs the full daily TikTok Wiz call review without any manual transcript upload. It pulls the day's calls from Avoma over the MCP, keeps only real consultations over 15 minutes, scores each on the strict rubric using the transcript, builds the summary report, and sends it to Caydo's own Slack DM.

This is the automated counterpart to the manual `ttw-daily-call-review` skill. Use this one for scheduled and on-demand daily runs. Use the manual skill only when Caydo uploads a transcript file by hand.

The closers are Vidush Rana, Tom Judson, Crue Lindgren, Turok Tarango, and Paul Rasoumoff. The setters are Petros Foustanellas, Antonio Vespa, Aidan Stammers, and Saray Cortes.

---

## Step 1: Establish the day window

1. Call `get_current_datetime` to anchor the run.
2. Caydo is in Lehi, Utah (Mountain Time). Build the local-day window in UTC: from the target date at 06:00:00Z through the next date at 05:59:59Z. That covers 00:00 to 23:59 local. Adjust by one hour across daylight-saving boundaries.

## Step 2: List the day's meetings

1. Call `list_meetings` with `meeting_state=completed`, `page_size=100`, and the day window.
2. Paginate (`page=2`, `page=3`, ...) until `next` is null. Do not stop at page 1, a normal day has 20 to 30 meetings across multiple pages.

## Step 3: Filter to reportable calls (STRICT)

Keep a meeting only if ALL of these are true:
- `transcript_ready=true`. No transcript means nothing to score.
- `duration` is over 15 minutes (over 900 seconds). Anything 15 minutes or under is excluded from the report. These are no-connects, reschedules, and scheduling-only calls, and they are noise.
- `is_internal=false` and the subject is not a team or internal meeting (drop "TTW - Team Sync" and similar).

Then dedupe: if two meetings share the same lead and near-identical content, keep the one with the real recording and drop the other.

Keep a short operator list of what got dropped and why (under 15 min, no recording, internal, duplicate). That list does not go in the report.

## Step 4: Pull the FULL TRANSCRIPT for every reportable call

For each reportable call, call `get_meeting_transcript` with the meeting `uuid`. Always score from the transcript, not the notes. The structured notes summarize outcomes and flatten the exact things this report grades on: hesitation, tone, whether the closer asked for the close or folded, and the precise affordability and timeline language. Notes may be used only as a cross-check.

Because these calls run 25 to 95 minutes, pull and score them one at a time. Do not try to hold the whole day's transcripts at once.

**Duration is not enough on its own.** A call can show a long duration but contain only a one-minute reschedule (the recording ran while waiting). After pulling the transcript, confirm a real consultation actually happened. If the transcript is only a reschedule, a no-connect, or an audio-failure handoff to phone, drop it from the report the same way a sub-15-minute call is dropped, and note it in the operator list.

## Step 5: Reliability and the incomplete-day rule

The Avoma MCP times out and throws execution errors intermittently. For every pull:
- Retry a failed or timed-out pull at least twice before giving up. The same `uuid` often succeeds on a retry. If the `avoma:` prefixed tool keeps failing, try the `Avoma MCP:` prefixed tool, and vice versa.
- If a transcript still cannot be pulled after retries, the day is INCOMPLETE for that call.

Never silently drop a reportable call. If any reportable call's transcript could not be pulled, still send the report on time, but prepend the incomplete-day header (see Delivery).

## Step 6: Identify the closer correctly

The MCP returns clean participant metadata with org tags, so identify the closer from the participant list first. Use these as backup and as a tie-breaker:
- **Name match:** any speaker whose name matches a known closer (Vidush, Tom, Crue, Turok, Paul) is the closer. No lead has ever shared a name with a closer.
- **Speaker-label scrambling:** Avoma sometimes swaps the labels, putting the closer's name on the lead's lines and vice versa. If the person sharing the screen and running the pitch is labeled as the lead, the labels are swapped. Read it with the labels corrected and note it.
- **Voice and style cues:** UK phrasing ("no worries at all", "fair enough") is Tom. "I gotcha", "fantastic", Austin or Texas references are Vidush. "Hey man", "wonderful", Pacific time are Turok. Repeated "right" and "for sure" are Crue.

## Step 7: S2C versus webinar (controls setter callouts)

Check the meeting title:
- **Title contains "S2C":** a setter pre-qualified and routed this lead. Setter callouts in the takeaway are fair when the lead was clearly unqualified, unprepared, or wrongly routed.
- **Title does NOT contain "S2C":** the lead booked directly from the webinar with no setter involved. Do NOT make setter callouts on these calls. Blaming a setter for a lead they never touched creates unfair coaching tension.

---

## Scoring rubric (strict, evidence-based)

Score every reportable call out of 20, four categories each out of 5.

### EVIDENCE RULE (applies to every category)

Score only what the lead explicitly says in the transcript. No stated evidence means no score above 2 in that category. Do not infer affordability from a nice house, a job title, real estate, or "successful business owner" language. Do not infer a solo decision from a confident tone. If the number or the fact was never said on the call, it does not exist for scoring, and the justification line must say it was not disclosed. Asset signals without a stated number are not affordability.

### Affordability (1-5), must be backed by stated numbers

A lead who cannot afford the monthly financing payment, OR who had any deposit or payment decline on the call, is automatically a 1 or 2 and is financially unqualified. A lead who never states a real financial figure cannot score above 2, no matter how wealthy they appear.

- **5:** Paid in full live, OR stated clear high income AND confirmed funds available with numbers
- **4:** Approved on financing live AND stated income or discretionary numbers that comfortably cover the payment
- **3:** Stated real numbers showing they can cover the monthly with some stretch, financed, one decline at most then approved
- **2:** Tight, OR declined on a financing partner, OR asked for smaller plans, OR never disclosed any real number (unverified). Financially unqualified.
- **1:** Deposit or payment declined on the call, cannot cover the monthly, unemployed, fixed income that will not cover the payment, or explicitly says they cannot afford it. Financially unqualified.

### Decision Maker (1-5), spouse status must be explicit

- **5:** Lead EXPLICITLY stated they have no spouse and no business partner and decide fully alone. Only an explicit statement earns a 5.
- **4:** No spouse or partner disclosed either way (unknown). Default here when marital or partner status never came up, even if they sound solo.
- **3:** A spouse or partner exists or is mentioned but is not described as blocking. A disclosed spouse caps the score at 3.
- **2:** Needs spouse or partner approval before committing.
- **1:** Cannot decide without an external party, or a 3-way call with the spouse is being scheduled.

### Timeline (1-5), when will they actually commit, stated explicitly

- **5:** Committing now, on this call.
- **4:** Today or tomorrow.
- **3:** Three to six days out.
- **2:** About a week out.
- **1:** Beyond a week, no date, open-ended, "no rush", or shopping other programs.

A same-day logistics reschedule is not urgency to commit. If the lead voiced no urgency or gave a delay with no hard date, score 1.

### Intent (1-5), explicit "I am doing this now" language, tied to timeline

Intent is how clearly the lead states they are 100% doing this now, not merely interested or looking around. It tracks closely with Timeline.

- **5:** Explicitly committed now ("I'm in", "let's do it", "sign me up", "send me the link, I'll pay now") AND moved on it live
- **4:** Strong commit language with a today or tomorrow action, said yes to multiple closes
- **3:** Leaning, asked good buying questions, but hedged or deferred ("I'll look into it", "let me check tomorrow")
- **2:** Curious but reserved, "interested", "sounds good", no commit, mostly listening
- **1:** Skeptical or objection-focused, openly comparing or shopping other options, no buying signals

"Interested", "this sounds great", and "I'm looking around" are NOT intent. An established business owner who is measured with no commit language scores low here regardless of how good a fit they look.

### Financially unqualified

Any lead scoring 1 or 2 on Affordability is financially unqualified or unverified. Distinguish the reason in the takeaway: confirmed broke (deposit or payment declined, no income), declined at price (capable on paper but will not pay), or unverified (never disclosed a real number). A declined deposit of any amount, and a Base 44 or scholarship route taken because Inner Circle was out of reach, both mean financially unqualified.

### Missed close (highest evidentiary bar)

Only flag a missed close when ALL are true: the lead confirmed money was available on the call (a stated number or a live approval), used hard commit language, had no stated need for time, research, or a spouse, and the closer still failed to ask for or process the close. If any of those is missing, it is not a missed close. A missed-close flag names a closer, so never flag one on thin evidence.

---

## Output format

Build the report in this exact structure. Put `&nbsp;` on its own line between sections so Slack renders real spacing.

```
**Daily Call Review, [Month Day, Year]**

**Day Summary**
- [call count] scored. [outcomes: closes, commits, deferred, lost, unqualified, with lead names and the closer]
- [any held calls and why]
- Qualified follow-ups booked meeting the bar (confirmed money plus commit-now intent): [count]
- Financially unqualified or unverified: [count] of [scored]. [who, and the one-line reason]
- Missed closes: [count]
- Open pipeline from today: [closes and live qualified leads]. Watch list, not yet qualified: [deferred or low-confidence]
- Upcoming follow ups: [name (date), ...]

&nbsp;

**Lead Quality Trends**
- [5 to 7 lead-side headlines: affordability evidence quality, unqualified count, financing patterns, decision-maker gaps, urgency, price objections, recording or funnel visibility]

&nbsp;

**1. [Lead Name] ([Closer]), [OUTCOME], [score]/20**
- Affordability [n]/5: [what they actually said, with numbers or "not disclosed"]
- Decision Maker [n]/5: [spouse status as stated, or "not disclosed"]
- Timeline [n]/5: [stated commit timing]
- Intent [n]/5: [commit language or lack of it]
- Takeaway: [1 to 2 sentences in Caydo's voice, tough but fair, what to do next]

&nbsp;

[repeat for each call, strongest to weakest]
```

## Tone and voice

- Write the takeaways in Caydo's voice: direct, first person where natural, tough but fair on closers, focused on the next action.
- Be hard on the closer when they folded or skipped a step, fair when the lead was never going to buy.
- Never use em dashes anywhere. Use commas, periods, or parentheses.
- Do not put emojis after rep names. Avoid emojis in general.
- No tables. Bold headers and hyphen bullets only.
- Ground every score in stated evidence. If something was not disclosed, say so rather than giving credit.

---

## Delivery to Slack DM

Send the finished report to the director's own Slack DM with `chat.postMessage` on the WFS Group workspace bot token. Set `channel` to the director's Slack member ID (DIRECTOR_SLACK_ID). The report is private to him and goes to no team or exec channel, so naming a closer in a missed-close line is fine here.

**Send, do not draft.** The run pulls, scores, builds, and sends with no approval step. This is the scheduled daily behavior.

**Send as exactly two separate Slack messages, in this order:**

- **Message 1:** the `**Daily Call Review, [date]**` header, the full **Day Summary**, and the full **Lead Quality Trends**. Nothing else. If the day is incomplete, the incomplete-report header goes at the very top of this message.
- **Message 2:** every per-call breakdown, strongest to weakest, in one message. No summary, no trends, just the numbered calls.

This is the fixed structure. Message 1 is the at-a-glance read, message 2 is the detail.

**Overflow fallback only.** Slack rejects a single message over about 5000 characters. Message 1 is always well under that. Message 2 can exceed it on a heavy day (roughly 8-plus calls). Only if Message 2 would exceed the limit, continue the remaining calls into a third message split at a call boundary, never mid-call. Do not split when it fits. The default and the goal is two messages.

**Incomplete-day header.** If any reportable call could not be pulled after retries, still send on time and prepend this line to Part 1:

> **INCOMPLETE REPORT.** The following calls over 15 minutes could not be pulled and are not scored: [lead names]. Re-run or pull manually.

This guarantees an on-time report that shows exactly what is missing rather than a silent gap or a held send.

---

## Scheduled run (daily 6:00 PM Mountain)

When the scheduled task fires, run Steps 1 through 7, score on the strict rubric, build the report, and deliver per the Delivery rules above, all unattended.

**6 PM timing caveat:** only calls that have finished and finished processing in Avoma by 6 PM will have a ready transcript. A late-afternoon call may still be processing and will show `transcript_ready=false`. If a call clearly happened but is not yet processed, list it under the incomplete-day header rather than omitting it.

**Connector access:** the scheduled run needs the Avoma and Slack connectors authorized in the task's context. If a run returns no meetings or cannot send, surface that as the failure rather than sending an empty report.
