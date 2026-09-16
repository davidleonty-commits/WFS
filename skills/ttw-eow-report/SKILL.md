---
name: ttw-eow-report
description: David's weekly End of Week sales report for TikTok Wiz: team KPIs, a prose rep summary, his call review activity, per rep Call Analysis graded against the five coaching categories, tactical themes, and the team touchpoint close. Manual run only, never scheduled. David supplies a Closer Sales Dashboard screenshot plus any talking points, and every number comes from that screenshot. Never build a rep table. Weeks run Sunday through Friday. Always delivered with the Slack Slack connector to the director's DM, never a channel. Use when he says "run the EOW report", "end of week report", "weekly sales summary", "build my Friday message", "weekly KPI recap", or sends a Sales Rep Table View screenshot. Always use it even when the ask sounds simple, because the five categories, the no dashes rule, the no table rule, first names only, the forward looking coaching frame, and DM only delivery are what he corrected and are easy to get wrong.
---

# TTW End of Week Report

The Friday leadership message. Always a DRAFT for David to review and post himself.

**Manual run only.** There is no scheduled task. David kicks this off and supplies the inputs.

**Window: Sunday through Friday.** Weeks always start on Sunday.

## Inputs David provides

1. **The dashboard screenshot.** Required. Nothing gets built without it.
2. **Extra talking points.** Optional. Anything he wants worked into the report: a rep conversation he had, a leadership ask, a win, a policy change. Weave these into the section they belong in, in his voice. If he does not mention any, ask once whether he has anything to add before you build.

## Hard rule 1: one sender, DM only

Every outbound message uses `slack_send_message` on the claude.ai Slack connector (the claude.ai Slack connector, which posts as you).

Parameters every time: `channel` = DIRECTOR_SLACK_ID U0BUZ6C0C91, nothing scheduled so it sends immediately. Confirm from the return value: `ok` = true, a non-empty `ts`, and a returned `channel` matching DIRECTOR_SLACK_ID.

- **Never** a personal user token and never a second sender.
- **Never** post to a channel. The only destination ever allowed is the director's DM, DIRECTOR_SLACK_ID.
- If the send fails outright, retry `slack_send_message` ONCE. There is no second sender, so a failed retry is reported, not worked around.

Reading is separate from sending. Use `slack_read_channel` and `slack_read_thread` to gather source material from anywhere. Reading is unrestricted, sending is DM only.

## Hard rule 2: never fabricate the numbers

Every figure comes from the screenshot. Do not pull from Pipedrive or the salesboard and present it as the report. Do not estimate.

## Hard rule 3: no rep table

Never build a per rep table or a code block of rep metrics. Individual rep data appears **only** as the prose `Rep summary:` paragraph.

## Voice and style

Written as David, first person.

### NO DASHES

No em dashes, no en dashes, no hyphens used as punctuation or to join clauses. Write "August 2 to August 7". Write "same day text back", not hyphenated. Break the thought into two sentences, use a comma, or use "and". Scan and strip every dash before sending.

**One exception:** the separator after a rep's first name in the Call Analysis bullets, exactly like `• Vidush - Personalizing the pitch.` That is the only hyphen allowed.

### How he writes

- Plain, direct, operational. Short declarative sentences, often joined with "and".
- First person and accountable: "that is my first conversation Monday morning".
- States a number, then says what he is doing about it. No hedging.
- Not a consultant. Never "the coaching is", "worth naming", "structural blocker", "counter-pattern", "textbook".
- No semicolons. No flourishes.

## Call Analysis, the most important section

Read `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) and your own self DM (the DM channel id for DIRECTOR_SLACK_ID; `conversations.open` returns it, or read it off any send this task makes) across the window, **including thread replies** on every "Daily Call Review" post. Get the total consultations scored and which days are covered.

### The five categories

Every Call Analysis bullet is graded against **exactly one** of these:

1. **Building pain and intent in the discovery**
2. **Personalizing the pitch**
3. **The closing sequence**
4. **Payment waterfall**
5. **Objection handling**

Nothing outside these five. Two reps can share a category.

> **We do not run financial qualification before price.** Never write coaching that tells a rep to establish income or affordability before presenting the offer. Affordability is handled inside the payment waterfall, after the price.

### Forward looking only

Do not diagnose. Do not recite evidence. Do not count how many calls something happened on. Do not name prospects. Do not narrate what went wrong.

Say what the rep needs to **do**. If Turok is not getting to price, do not explain that he ran an hour of discovery without pitching. Name the category (building pain and intent in the discovery) and say what he needs to do to get there.

One or two sentences per rep. **First name only, never last names.**

### Introduce the category like a person, not a label

Never drop the category in as a bare heading. Lead into it the way David would say it out loud, and **vary the phrasing on every rep** so the section does not read like a template:

> Vidush - His main focus right now is personalizing the pitch.
>
> Rachel - After going through her calls the biggest thing for her is the closing sequence.
>
> Turok - The skill I want him working on is building pain and intent in the discovery.
>
> Crue - Same as Noel, his is the payment waterfall.

Then the sentence of what he or she actually does about it.

## Message structure

```
:memo: *DRAFT, End of Week Report for <Month Day> to <Month Day>*

*End of Week Report, <Month Day> to <Month Day>*

*Team KPIs*
• Qualified closer calls: <n>
• Live calls: <n> (<x>% show)
• Closed: <n> (<x>% of live calls, <x>% of booked calls)
• Salesboard gross: $<n>
• Salesboard collected: $<n>
• Team CDPBC: $<n> | Team GDPBC: $<n>

*Rep summary:*
<one paragraph, about six sentences, one per rep>

*My Call Review Activity*
I listened to <h> hours and <m> minutes of calls this week across <n> conversations at <x>% listen coverage.

*Call Analysis*
<N> consultations were scored between <Day> through <Day>.
• <Firstname> - <human lead in to the category>. <what he or she does about it>

*Themes going into next week*
<three or four tactical bullets>

*Team*
<touchpoint paragraph>
```

The Call Analysis opener is the count sentence only. **Do not add "Here is where each rep landed."**

**Rep summary** is prose, not a table. Each sentence names the rep, the number that defines their week, and what David is doing about it. Lead with whoever led the board, end with whoever needs the hardest conversation. Register to match:

> Garrett has the best CDPBC on the team at $965.71 and he closed half of every live call he took, he just needs more of his 35 booked calls to actually show up at 29%.
>
> Noel took 33 booked calls and did not close any of them and that is my first conversation Monday morning.

**My Call Review Activity** is exactly one sentence. Hours and minutes, conversation count, listen coverage. No team rank, no comparisons.

**Themes** are tactical. The sales themes carry up from the five categories in Call Analysis, phrased as what the whole team drills starting Monday. Not observations, not patterns, not "this kept happening".

The last bullet can be a read on lead quality when the call record supports one. Frame it as an observation and as work the sales team owns, never as an expectation that marketing send deals that are ready to buy. Saying leads are not ready to buy makes the sales team look soft. This is the register:

> A lot of leads are coming in very curious about TikTok shop but without much intent to actually get started on it. That is ours to build in discovery, and it is worth passing to marketing as a read on where the traffic is sitting right now.

**Team** always says the same thing in fresh words: he had good conversations with every one of the reps this week, they all know exactly where they stand and what they need to fix, and he is going to keep touching base with them one on one to keep their energy up and their mindset in the right place going into next week.

End with a short italic line listing anything he should check before sending.

## Reading the screenshot

The **Sales Rep Table View**: one column per rep, bold team total column on the right. Rows: Qualified Closer Calls, Live Calls, % Show, FC Live Calls, % FC Show, Salesboard Closed, % Live Closed, % Booked Closed, Salesboard Gross, Salesboard Collected, GDPLC, CDPLC, GDPBC, CDPBC.

Read every figure **exactly as shown**. Do not recompute, round, or correct. Blank cells shown as a dash mean zero. If per rep values do not sum to the printed team total, use the printed team total and flag it. Team total column feeds Team KPIs, per rep columns feed the prose Rep summary.

## Avoma call review activity

`list_team_usage_metrics`, from_date = Sunday 06:00Z, to_date = Saturday 06:00Z (MT midnight boundaries). On 403, fall back to the Avoma REST API directly: `GET https://api.avoma.com/v1/engagement/` with the same dates and header `Authorization: Bearer $AVOMA_API_KEY`. Row = the director's own call-platform account email: `david.leonty@ttwhizprogram.com` (the outgoing director's was `cayden.johnson@ttwhizprogram.com`, kept here only so an old row can still be recognised). Duration as hours and minutes, never raw seconds.

## QA gate, before every send

1. Destination is DIRECTOR_SLACK_ID and the call is `slack_send_message` on the Slack connector. No channel, no second sender.
2. No rep table and no code block of rep metrics anywhere.
3. Zero dash characters except the name separator hyphens in Call Analysis.
4. Every Call Analysis bullet lands on one of the five categories, introduces it in David's words rather than as a bare label, varies that lead in across reps, and says what the rep needs to **do**. If a bullet describes what went wrong instead of what to fix, rewrite it.
5. Nothing anywhere tells a rep to qualify financially before price.
6. Call Analysis uses first names only, and the opener has no "Here is where each rep landed."
7. My Call Review Activity is exactly one sentence with no team comparison.
8. Themes are tactical actions carried up from the five categories. Any lead quality bullet is framed as sales team work, never as an expectation on marketing.
9. Every figure matches the screenshot exactly.
10. David's extra talking points, if he gave any, are in the report.

Never send a fabricated or estimated number. Leave the field blank and say why.
