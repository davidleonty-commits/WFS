---
name: webinar-lead-quality-report
description: On-demand webinar lead quality report for David, Sales Director. Takes just a webinar date, pulls that webinar's cohort from Pipedrive using the Lead Source custom field, and joins the leads by email to already-graded scores in the Supabase lead_quality table. Reads existing scores instead of re-scoring transcripts, so runs are cheap and always agree with the daily report. Use whenever David asks for a webinar lead quality report, webinar lead scores, lead quality by webinar, "how good were the leads from the [date] webinar", "score the webinar leads", "run the webinar report", "which webinar sent better leads", or "compare lead quality across webinars". Manual trigger only. Always use this skill for webinar-level lead grading even when the request sounds simple, because the Lead Source attribution, the email join, the cache write-back, and the QA gate carry exact rules that keep webinar-to-webinar comparisons honest.
---

# Webinar Lead Quality Report (on-demand)

Grades the leads a webinar produced, not the closers who took the calls.

**Division of labor.** The Daily Call Report Publisher (mgmt-call-reports) grades every call once per day and persists it to Supabase. This skill never re-grades. It resolves which leads came from a given webinar, joins them to their existing scores, rolls them up, and writes the attribution back so the next run of the same webinar is nearly free.

**All David needs to give: a webinar date** ("run it for the July 15 webinar") or several ("compare the last three webinars"). If no date is given, ask one question to pin it.

## Data sources

- **Supabase** project_id `apdwbbocldfsklvcwaqd`, table `public.lead_quality`. One row per graded call, keyed on `meeting_uuid`. Columns used: `call_date`, `prospect_name`, `prospect_email`, `affordability`, `decision_maker`, `timeline`, `intent`, `lead_score`, `financially_qualified`, `dq_reason`, `rubric_version`, `webinar_date`, `source_master_page_id`. The table also holds `rep`, `outcome`, and `collected`, which this report does not use.
- **Pipedrive** via `searchDeals`. Every deal carries a Lead Source custom field holding the OnceHub booking page label, so a single search returns the whole cohort. OnceHub is no longer needed for attribution.

Never pull an Avoma transcript in this skill, and never score a call. This skill reads grades and writes attribution, nothing else.

---

## Step 1: Check the cache first

Query Supabase for rows already attributed to the requested webinar:

```sql
select * from public.lead_quality
where webinar_date = 'YYYY-MM-DD'
order by lead_score desc;
```

If rows come back and David has not asked for a refresh, the cohort is already attributed. Skip to Step 5 and roll up. Say in the header that attribution came from cache. This is what makes a repeat run of the same webinar cost almost nothing.

If zero rows, continue to Step 2.

## Step 2: Pull the cohort from Pipedrive

Every deal carries its Lead Source as a custom field, holding the exact OnceHub booking page label. One search returns the cohort.

Call `searchDeals` with `exact_match=true`, `fields=custom_fields`, `limit=100`, and the term set to the webinar's page label:

`Webinar MM DD YY | Paid | Closer | 45min`

Build the label from the date David gave, zero-padded, two-digit year. For July 8 2026 that is `Webinar 07 08 26 | Paid | Closer | 45min`. Paginate with the cursor until `next_cursor` is null.

Capture per deal: deal id, title (the lead's full name), person name, status (open, won, lost), stage, deal value, owner, the collected custom field `bbee529cf1331e72608898145b7581d7312cfbc0`, the Lead Source label `6b96ef9137fb779c5ef00f5a47e1fd04cdb64adb`, and from the notes the lead's email, the OnceHub booking id, and the intake answers including their declared budget.

Never blend other funnels into a dated webinar's numbers. `Webinar S2C | Demo | Closer | 45min` is the setter-routed funnel, `Automated Webinar | Paid | Closer | 45min` is the evergreen funnel, and labels like `Youtube | Organic | Closer | 45min` are separate sources entirely. Each is its own cohort, run only when David names it.

If the search returns nothing, the label is probably wrong. Do not guess a nearby date. Read the exact label text from OnceHub (`GET https://api.oncehub.com/v2/booking-calendars` with header `API-Key: $ONCEHUB_API_KEY`, paginated to the end), since spacing in these labels is occasionally inconsistent, then retry once with the corrected string.

ONCEHUB v2 NAMING (verify on the first live call, corrected 2026-09-16): the current v2 API calls
what this prompt calls "booking pages" and "master pages" **booking calendars**. There is no
/booking_pages or /master_pages path any more; both map to `/v2/booking-calendars`. The grouping
this prompt does by master page is therefore a grouping by BOOKING CALENDAR, and the
unattributed-booking rescue is the case where a booking came in on a rep's PERSONAL calendar and
so carries no shared calendar id. The business rules below are unchanged: which calendars count
as Webinar Closer, which as S2C, which are Setter pages to ignore, and the ET day boundary.
Read the exact response field names off the first `GET /v2/bookings` call and correct the field
names in this prompt if they differ; do not assume them. Also confirm the auth header (`API-Key`
historically; the API reference "Try it" panel is authoritative).

## Step 3: Establish the call window

The booking window is the webinar date through 14 days after. State it in the report header. David can widen or narrow it.

## Step 4: Join deals to graded calls

Pull candidate rows in one query, using the call window widened by 2 days on each side to catch reschedules:

```sql
select * from public.lead_quality
where call_date between 'START' and 'END';
```

For each deal, find its row in this order:

1. **Email match** on `prospect_email`, exact and case-insensitive, using the email from the deal notes. This is the primary key.
2. **Name match:** deal title against `prospect_name`, case-insensitive, requiring both first and last name to appear. Never match on first name alone; the roster has repeated first names.
3. **No match:** that deal produced no graded call. It counts toward coverage and nothing else. Never estimate a score.

Two integrity rules:

- **One deal, one row.** If a single deal matches two rows, the lead had two calls. Count the lead once using the LATER call, and note it, since a rebooked lead double-counted skews the average.
- **Do not overwrite an existing attribution.** If a matched row already carries a different `webinar_date`, report the conflict rather than silently reassigning it.

### Write the attribution back (cache)

For matched rows only, update the attribution columns. This is the ONLY write this skill makes.

```sql
update public.lead_quality
set webinar_date = 'YYYY-MM-DD',
    lead_source_label = 'Webinar MM DD YY | Paid | Closer | 45min',
    pipedrive_deal_id = <deal id>,
    updated_at = now()
where meeting_uuid = '...'
  and webinar_date is null;
```

The `webinar_date is null` guard means a re-run can never rewrite an attribution that already exists. Never write scores, never write outcomes, never delete a row.

## Step 5: Roll up per webinar

Compute from the joined rows, and re-derive independently at the QA gate:

- **Average lead score** out of 20, and each category average out of 5.
- **Distribution:** High Quality 16-20, Medium Quality 11-15, Poor Quality 6-10, dead 5 or under. These bands come from the SCORE BANDS section of the shared TTW rubric, the same one the Publisher grades against, so sales and marketing bucket a lead identically. They only sort a `lead_score` the Publisher already assigned; never rescore to fit a band.
- **Qualified rate:** share of rows with `financially_qualified = true`. Read the boolean, never recompute it from `affordability`. The Publisher's rubric decides qualification, and recomputing here is how the two reports start disagreeing about the same lead.
- **Unqualified split** by `dq_reason`: confirmed_broke, declined_at_price, unverified.
- **Top disqualifying patterns:** the 3 to 5 most common low-score drivers, read from the category averages and the dq_reason split.
- **Enrollments and collected**, read from the deals pulled in Step 2 (status won, and the collected custom field). Apply a downsell floor: a won deal whose collected is 500 dollars or more is a program enrollment; a won deal under 500 dollars is a downsell (for example a 50 dollar Base 44 or Stepping Stone tier) and is counted and reported SEPARATELY, never blended into the enrollment count or its dollar total. Report enrollments as cohort context on one line, separate from the scores, with downsells on their own line when any exist. A cohort can score badly and still enroll buyers, and that gap is the single most useful thing this report surfaces, so never let a low average imply the webinar produced nothing.
- **Trend line:** when 2 or more webinars are in scope, compare averages, qualified rates, and won counts, and say plainly which direction lead quality is moving.

**Rubric version check.** If the joined rows carry more than one `rubric_version`, say so in the report. Comparing cohorts graded under different rubric versions is still useful, but it must be visible.

## Step 6: Reps are context, not the subject

This report grades LEADS. Report per-rep splits only when David asks. Never diagnose a rep, never flag missed closes, and never imply a low cohort average is a rep's fault. Closer coaching lives in the call review skills.

## Step 7: Coverage, never estimates

This report has no gaps section and never lists ungraded bookings by name. It does carry one coverage figure in the header, the count of graded calls over completed bookings, because an average built on half a cohort presented as a whole-cohort number is misleading. Keep it to that single clause.

If coverage falls below 80 percent of completed bookings, add one line under the header saying the averages rest on a partial cohort. One line, no list.

**This skill NEVER scores a call.** There is exactly one grader in this system, the Daily Call Report Publisher, and its rubric lives inside that scheduled task where this skill cannot read it. Grading here would mean grading from memory, which is how two reports start disagreeing about the same lead. If David asks to fill the missing calls, do not score. Tell him the two supported routes:

1. Re-run the Publisher for the specific call date, which regrades under the canonical rubric and upserts on `meeting_uuid` so nothing duplicates.
2. Check `public.report_run_log` for that date, since the backfill guardian may already have logged the shortfall and be able to heal it.

Then re-run this report, which will pick up the new rows from cache.

---

## Output format

Put `&nbsp;` on its own line between sections so Slack renders spacing.

```
**Webinar Lead Quality Report, [webinar date(s)], run [Month Day, Year]**
[Booking window: webinar date through +14 days. [n] of [n] completed bookings graded. Scores read from lead_quality, not re-graded.]

**Webinar: [MM DD YY]**
- Average lead score: [x.x]/20 (Affordability [x.x], Decision Maker [x.x], Timeline [x.x], Intent [x.x])
- Distribution: [n] High Quality (16-20), [n] Medium Quality (11-15), [n] Poor Quality (6-10), [n] dead (5 or under)
- Qualified rate: [n]%
- Unqualified: [n]% ([n] confirmed broke, [n] declined at price, [n] unverified)
- Enrolled from this cohort: [n] program enrollments (500+), $[n] collected
- Downsells: [n] under 500, $[n] collected (only show this line if any)
- Top disqualifying patterns:
  - [pattern, with the count of leads it hit]
  - [repeat, 3 to 5 total]

&nbsp;

[repeat webinar blocks when comparing multiple webinars]

**Webinar-to-webinar trend** (only when 2+ webinars in scope)
- [plain-language read: averages, qualified rates, what changed and the likely funnel cause]
```

## Tone and voice

- David's voice: direct, plain, focused on what marketing and the webinar funnel should do about it.
- Never use em dashes anywhere. Commas, periods, or parentheses.
- No emojis after names, avoid emojis in general. No tables, bold headers and hyphen bullets only.

---

## QA GATE (before delivery, mandatory)

1. Re-derive every average, rate, distribution count, and the coverage figure independently from the joined rows. Numbers must match.
2. Confirm every scored row traces to a deal carrying this webinar's exact Lead Source label, and that no S2C, automated-funnel, YouTube, or unmatched row entered a dated webinar's average.
3. Confirm no row was counted in two cohorts in this run, and no existing attribution was overwritten.
4. Confirm no score was estimated, recomputed, or derived from a transcript. Every score, and the qualified flag, came from lead_quality exactly as the Publisher wrote it. This skill grading anything is an automatic FAIL.
5. Confirm the only Supabase write performed was the attribution cache update, guarded by `webinar_date is null`.
6. Confirm the format matches the template, including `&nbsp;` separators and the no-em-dash rule.
7. On a fixable failure, correct and re-check, up to 3 attempts. If it still fails, or the failure is a source or data problem, do not deliver. Send the specific QA failures to David's DM instead.

## Delivery

TEST MODE until David explicitly declares this skill out of test mode: send output with **`slack_send_message`** on the claude.ai Slack connector (the claude.ai Slack connector, which posts as you), sent immediately, to the director's DM (channel = DIRECTOR_SLACK_ID U0BUZ6C0C91). One sender only: never a second sender, never a team channel while in test mode.

Split at webinar-block boundaries if a message would exceed the roughly 3000-character Slack block cap, never mid-lead.

If David triggered the run in a live chat, showing the report in the conversation is fine, and offer the Slack DM send as the follow-up.

**If lead_quality has no rows for the window,** say so plainly and name the likely cause (the window predates the table, which starts 2026-07-06, or the Publisher did not run that day). Check `public.report_run_log` for that date before concluding, since the backfill guardian logs shortfalls there. Do not silently fall back to scoring transcripts.
