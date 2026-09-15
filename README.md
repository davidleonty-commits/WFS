# WFS / TTW Sales Director: Claude Automation Handoff

Prepared by Cayden Johnson, September 2026, for the incoming Sales Director.

> **Status: the Section 1A connector swap has been done.** Every prompt and skill in this
> repository now reaches Slack, OnceHub, Avoma and Pipedrive directly. Nothing calls the
> retired Lovable WFS MCP. The swap is a clean diff against the original export, which is the
> first commit in this repository's history.
>
> - `DATA-ACCESS.md` is the canonical old-tool to new-call map, and the contract the prompts
>   were rewritten against. Edit it first if you change how a source is read, then propagate.
> - `RETARGETING.md` tracks the director identity. Slack id, Pipedrive id and the name are
>   filled in for David Leonty; four values (work Google account, Avoma account email, Team
>   Sync organizer, browser deviceId) are still outstanding. Start there.
>
> The rest of this README is the outgoing director's handoff, kept as written except where the
> swap changed the facts.

Everything in this folder is the AI operating layer I ran the WFS / TikTok Wiz sales org on. It is two things:

1. **`scheduled-prompts/`**: 13 Claude Cowork scheduled tasks that ran on my laptop. Each folder holds one `SKILL.md`, which is the complete prompt that runs on a schedule with no human in the loop. Paste it into a new scheduled task in your own Claude Cowork and it runs as-is once the connectors are wired.
2. **`cloud-routines/`**: 21 scheduled tasks that ran as claude.ai cloud routines. Same format. **These are the versions that were actually firing at handoff.** Most of the daily reports were migrated from the laptop to the cloud in July 2026; where a task exists in both folders, the cloud copy is newer and is the one to recreate. The local copy is kept for reference only.
3. **`skills/`**: 17 Claude skills. These are the on-demand playbooks (call reviews, KPI formulas, clip finder, EOW report, and so on). Upload each folder as a skill in your Claude account and they trigger by name or by intent.

Nothing here contains API keys or passwords. Auth lives in the connectors, which you will connect under your own account.

**Why Section 1A existed.** Every prompt in this package used to send Slack, read OnceHub, and pull call data through a private connector called the "Lovable WFS Slack" or "WFS Sales Director" MCP, which was a custom app I built and hosted. The new director does NOT have it. Section 1A told Claude Code how to swap each of its tools for direct API access. That work is done: Section 1A below now records what the swap changed and what it could not carry over.

---

## 1. What you need connected before any of this works

| Connector | Used for | Notes |
|---|---|---|
| ~~**Lovable WFS MCP**~~ (the outgoing director's private app at `commandcenter.aiautomating.com`) | Was the backbone for Slack sends, OnceHub reads, call data and pre-filtered Pipedrive views. | **RETIRED, and nothing calls it any more.** Its tools were replaced with direct API access; see Section 1A and `DATA-ACCESS.md`. |
| **Slack Web API** (bot token, or the Slack MCP connector) | Every send, and the `#payments` and reps-channel reads | The single sender for every task. Scopes are listed in `DATA-ACCESS.md`. |
| **OnceHub API** (`api.oncehub.com/v2`, API key) | Bookings, master pages, booking pages | Lead flow report, both show-rate reports, EOD booking health, webinar report. |
| **Avoma MCP** (or the Avoma REST API as fallback) | Call transcripts, meeting lists, AI notes | Used by the show-rate and call-report tasks and all call-review skills. Note: Avoma has no scorecard. Scoring is done from the transcript by the task's own rubric. |
| **Pipedrive MCP** | Deals, activities, pipeline 3 (TTW closer pipeline), Lead Source field | Director audit labeling, accountability report, KPI formulas, webinar report. |
| **Google Drive / Docs / Sheets** | SIP docs (one per rep), TTW Salesboard 2026 sheet (read-only), SIP master template, Decision Leadership Objection Matrix | The SIP engines edit ONE Google Doc each, through the browser. |
| **Claude in Chrome** (browser) | Editing the SIP Google Docs | The five local SIP engines only. |
| **Supabase** (optional) | `lead_quality` table for the webinar lead quality report | Only if you keep that report. |

## 1A. What the connector swap changed (done)

The prompts in `scheduled-prompts/` and `cloud-routines/`, and several skills in `skills/`,
called tools on an MCP server named `Lovable_WFS_Slack` (also "the Lovable WFS connector", "the
WFS Sales Director MCP", or "the WFS connector"), a custom app hosted at
`commandcenter.aiautomating.com` under the previous director's account. It does not exist for
the new director.

Every one of those calls has been replaced with direct API access. The full old-to-new map,
including the parameter-level equivalences and the day-boundary and pagination rules that came
with them, is in **`DATA-ACCESS.md`**. Read that file before changing how any prompt reads a
source.

What the swap preserved: every rule, threshold, roster, template, QA gate, delivery mode and
day boundary. Only the data-access method changed, which is what the prompts' own
"SELF-HEAL GUARDRAILS" always allowed (methods may change, policies may not).

What the swap changed in substance, because the old behavior no longer exists:

- **The Slack sender lock.** The old rule said "the Lovable WFS connector, never the native
  Slack connector", because that app held the workspace bot token. It now reads: the Slack Web
  API with the bot token, never a personal user token, never a second sender. Same discipline,
  different name.
- **Delivery verification.** There is no send queue to poll. An accepted `chat.postMessage`
  has already posted, so the send's return value (`ok`, a `ts`, the resolved channel) is the
  proof, and a follow-up read is a content spot-check that can never trigger a resend. That
  rule is what stops a read hiccup double-posting to the client channel.
- **Mentions.** The old app resolved plain `@Name` text into pings server-side. The Slack API
  does not, so every rep mention is now an inline `<@MEMBERID>` token, read from the roster
  sheet's Slack User ID column (or resolved once via `users.lookupByEmail`).
- **The call scorecard.** `calls_get_analysis` returned the app's own scoring (lead_score,
  rep_score, primary_objection, financially_qualified, close_attempts, downsell_offered,
  lead_bucket) alongside the transcript. Avoma returns none of it. Every task that read those
  fields now scores the transcript itself against the rubric it already carried. In practice
  most of those fields were already null, and the prompts already said to derive from the
  transcript, so the graded output should not move.
- **Candidate ranking.** `calls_find_review_candidates` returned calls pre-ranked. The ranking
  rules now live explicitly in the `ttw-avoma-clip-finder` skill and run after `list_meetings`.
- **Rep identity.** The Lovable rep UUID is gone. Call data keys on the rep's **Avoma email**
  (`REP_AVOMA_EMAIL`, replacing `REP_WFS_ID` in the SIP engines); deal and activity data keys on
  the integer **Pipedrive owner id**. The old rule "map by id, NEVER by name string" still holds
  and for the same reason: the roster carries duplicate full names across different people.
- **The Director Console.** `calls_propose_review_note`, `tracker_propose_entry`,
  `pipeline_propose_reopen`, `reps_propose_coaching_action`, `proposals_list`,
  `director_daily_brief` and `compliance_scan` were UI features of the app. The calls are
  removed; where a prompt said "propose", it now writes the note directly to its target.

Two consequences worth knowing before you enable anything:

1. The old non-negotiable "write tools in the WFS connector never mutate live data, they create
   proposals you approve in the Director Console" no longer has a mechanism behind it. Two tasks
   write for real, `pipedrive-director-audit-labeling` and `pipedrive-activity-clearing-cloud`,
   and their `PROCESS_MODE: DRY_RUN` gate is now the only thing between a run and a live
   Pipedrive edit. Run them in DRY_RUN first.
2. Identity was never guessed. It is now set to David Leonty: `DIRECTOR_SLACK_ID` = U0BUZ6C0C91
   in all 39 sending prompts, `OWNER_USER_ID` = 27299998 in the two audit tasks, and the name
   swapped wherever the text is about the sitting director. Four values remain outstanding, all
   listed in `RETARGETING.md`.

### Credential checklist to collect from the new director

| Service | What to ask for | Used by |
|---|---|---|
| Slack (WFS Group workspace) | Bot token with `chat:write`, `chat:write.public`, `channels:read`, `channels:history`, `im:write`, `users:read`, plus the new director's own Slack user id (replaces `U092C85GA4D` everywhere) | every task |
| OnceHub | API key | lead flow report, both show-rate reports, EOD booking health |
| Avoma | API key, or connect the Avoma MCP in claude.ai | call reports, SIP engines, clip finder, review sourcing, weekly call review, all review skills |
| Pipedrive | API token, or connect the Pipedrive MCP in claude.ai | accountability report, leaderboard, director audit, KPI formulas, webinar report |
| Google Drive / Sheets / Docs | OAuth under the director's WORK Google account (the Salesboard reads must be logged under a work identity, per the leaderboard prompt) | SIP engines, leaderboard, sales hype, EOW, roster sheet |
| Supabase | Project URL and service key for project `apdwbbocldfsklvcwaqd`, only if the `lead_quality` pipeline is kept | daily call report v27, sweeps, guardian, webinar report |

### Verifying the swap

The original sanity check was to grep for the retired tool names. It still passes, and it is
worth re-running after any edit:

```bash
grep -rnE 'Lovable|WFS connector|WFS_MCP_TOKEN|slack_schedule_message|slack_send_sos|oncehub_[a-z]|calls_list|calls_get_analysis|calls_find_review_candidates|pipeline_smart_view|reps_scoreboard|REP_WFS_ID|avoma_api' --include='*.md' cloud-routines scheduled-prompts skills
```

That returns nothing today. Then run each task once in TEST and confirm the Slack message
matches the template in its own prompt line for line: the templates were not touched by the
swap, so any drift is a real finding.

One assumption is worth checking before the first TEST run, because five prompts are written
around it: that OnceHub accepts `starting_time.gt` / `.lt` and rejects `starting_time_from` /
`_to`, and that a booking carries `booking_page.master_page`. `scripts/verify-oncehub.py`
checks exactly that, read-only, printing structure and counts but never a booking's contents:

```bash
export ONCEHUB_API_KEY=...        # from your secret store, never committed
python3 scripts/verify-oncehub.py
```

It was written but NOT run: this environment's network policy blocks `api.oncehub.com`, so the
OnceHub behavior in those prompts is still carried over from the outgoing director's notes
rather than confirmed.

Key reference docs (links are inside the prompts):
- Decision Leadership Objection Matrix (Sales Rep Quick Reference): every coaching point must trace to it.
- SIP master template.
- TTW Salesboard 2026 Google Sheet, fileId `1_5YMQVATclX5gRRJfkqG-wfyWP23TYlDoLugu8Tz_W4` (read-only, revenue source of truth).
- WFS Sales MGMT Playbook ("Core Four": Call Analysis, Pipeline MGMT, Performance MGMT, Training). The retired connector was built around it, and the prompts still are.

---

## 2. The scheduled prompts (what runs, when, where it lands)

All times Mountain. "Cloud" means fully connector-based, runs remotely with your machine closed. "Local" means it needs the browser and runs on your laptop.

### Daily rhythm (weekdays)

| Order | Task folder | Fires | Delivers to | Mode as handed off | Runs |
|---|---|---|---|---|---|
| 1 | `pipeline-mgmt-accountability-report` | 11:00 AM | `#wfs-ttw-sales-reps-dm-external` | LIVE | Cloud (superseded by `cloud-routines/pipeline-accountability-report-v2-cloud`) |
| 2 | `daily-midday-checkin` | midday (after the 9:00 AM payments cutoff) | `#wfs-ttw-sales-reps-dm-external`, memory copy to owner DM | LIVE | Cloud |
| 3 | `midday-show-rate-update` | 1:30 PM | Owner DM (TEST). Below 40% show rate it is DM-only even in LIVE. | TEST | Cloud |
| 4 | `ttw-daily-lead-flow-report` | weekday, OnceHub day boundary in ET | `#wfs-ttw-sales-mgmt-client` (client reads this) | LIVE | Cloud |
| 5 | `mgmt-call-reports` | weekday, end of day | Owner self-DM, per-call reviews threaded | TEST | Cloud |
| 6 | `eod-show-rate-update` | 7:00 PM | `#wfs-ttw-sales-mgmt-client` (client reads this) | LIVE | Cloud |

What each one does:

- **pipeline-mgmt-accountability-report**: three sections from Pipedrive (Expected Close past due, Hot List, activities overdue plus due today), one message to the reps channel. No CRM writes.
- **daily-midday-checkin**: reads today's `#payments` posts (only those after 9:00 AM, because the payments automation reposts yesterday's deals in the morning) and today's sets from the reps channel, writes a short check-in that calls out payments and set counts, tags the five closers by Slack user id, and asks what the team has confirmed. Reads its own last two posts back from the memory DM so it never repeats itself.
- **midday-show-rate-update**: time-based show rate (calls due by now vs Avoma live calls over 15 min) for Webinar and S2C, plus a Call Recaps section in my voice, one bullet per live call. Has the unattributed-booking rescue (rep personal booking pages come back with `master_page = null` in OnceHub and used to deflate the denominator). A show rate over 100% is a hard QA failure.
- **ttw-daily-lead-flow-report**: OnceHub booking counts for the day, QA-gated, posted to the client channel. This is the source the show-rate tasks reconcile against; all three use the same day boundary and status filter.
- **mgmt-call-reports**: pulls today's TTW consultation transcripts from Avoma, scores each call, posts a Day Summary plus threaded per-call reviews. Every Slack message body must stay under 3000 characters or Slack silently splits it into a top-level message that escapes the thread. No compliance flags in Slack, ever; those go in the run report only.
- **eod-show-rate-update**: full-day scheduled counts (no halving), live calls, reschedules, cancellations, double bookings, closer Booking Health, to the client channel.

### Weekly rhythm (Mondays)

| Task folder | Fires | Delivers to | Mode | Runs |
|---|---|---|---|---|
| `weekly-ttw-clip-finder` | Monday morning | Owner DM | LIVE | Cloud |
| `pipedrive-director-audit-labeling` | Monday | Owner DM run report | EXECUTE (writes to Pipedrive) | Cloud |
| `sip-engine-vidush-rana` | Mon 10:30 AM (cron `15 12 * * 1`) | Owner DM | TEST | Local |
| `sip-engine-crue-lindgren` | Mon 10:50 AM (cron `10 12 * * 1`) | Owner DM | TEST | Local |
| `sip-engine-garrett-mckenna` | Mon 11:50 AM (cron `5 12 * * 1`) | Owner DM | TEST | Local |
| `sip-engine---noel-soto` | Mon 3:00 PM | Owner DM | TEST | Local |
| `sip-engine---scott-jose` | Mon 4:00 PM | Owner DM | TEST | Local |

- **weekly-ttw-clip-finder**: runs the `ttw-avoma-clip-finder` skill over the last 7 days, scores objection handling against the Decision Leadership matrix, hands you exact clip-in and clip-out anchors so each Avoma snippet is one click.
- **pipedrive-director-audit-labeling**: labels and clears the director's due and overdue Pipedrive activities via API, then DMs a run report. Tightly scoped edit allow-list. Set `PROCESS_MODE: DRY_RUN` first to see what it would touch under your account.
- **SIP engines (five, one per rep)**: each Monday does exactly one thing based on the Issue Date on the rep's most recent SIP tab: create a new SIP (week 0), append check-in 1 (week 1), append check-in 2 (week 2), then create again. KPIs come connector-only from Pipedrive plus the Salesboard sheet using the `ttw-dashboard-metrics` definitions. Minimum 5 of the rep's calls verified by transcript per run. Slack update tags the rep exactly once as `<@REP_SLACK_ID>` inline, and nowhere else (a second mention double-tags the rep). The three original engines (Vidush, Crue, Garrett) were paused (`enabled: false`) on 9/8/26 when I began winding down; Noel and Scott were still enabled. All five are still in TEST, so they only ever messaged me, never the rep.

Each SIP engine's CONFIG block holds the rep's Slack id, Pipedrive owner id, `REP_EMAIL` (which is now the call-data key, replacing the retired connector's rep UUID), and the URL of the ONE Google Doc it is allowed to edit. To add a rep, copy any engine and change only the CONFIG block.

### Cloud routines (`cloud-routines/`)

These ran as claude.ai cloud routines (claude.ai/code/routines), not from my laptop, so they were exported from the cloud rather than copied from disk. Same format: one folder, one `SKILL.md`, the prompt is the body. The frontmatter records the UTC cron, the enabled state at handoff, the model, and the connectors that were attached. Cron is in UTC there; Mountain time is in the tables.

Where a cloud routine has a local twin in `scheduled-prompts/`, the cloud one is the newer edition and was the live publisher; the local twin was disabled to avoid double-posting. Recreate the cloud version.

**Daily (weekdays)**

| Task folder | Fires (MT) | Delivers to | Mode | State | Replaces local |
|---|---|---|---|---|---|
| `daily-sales-hype-v3` | 8:30 AM (`30 14 * * 1-5`) | Owner DM (LIVE: reps channel) | TEST | Enabled | |
| `ttw-daily-lead-flow-report-cloud` | 9:45 AM (`45 15 * * 1-5`) | `#wfs-ttw-sales-mgmt-client` | TEST value in CONFIG, but the note says it went LIVE 7/13. Confirm before relying on it. | Enabled | `ttw-daily-lead-flow-report` |
| `daily-ttw-leaderboard-v4` | 10:00 AM (`0 16 * * 1-5`) | Owner DM (LIVE: reps channel) | TEST | Enabled | |
| `pipeline-accountability-report-v2-cloud` | 12:06 PM (`6 18 * * 1-5`) | `#wfs-ttw-sales-reps-dm-external` | LIVE | Enabled | `pipeline-mgmt-accountability-report` |
| `daily-midday-checkin-v2-cloud` | 1:00 PM (`0 19 * * 1-5`) | Owner DM (LIVE: reps channel) | TEST | Enabled | `daily-midday-checkin` |
| `show-rate-update-midday-cloud` | 1:30 PM (`30 19 * * 1-5`) | `#wfs-ttw-sales-mgmt-client` | LIVE | Paused | `midday-show-rate-update` |
| `midday-hype-mwf` | Mon/Wed/Fri 3:00 PM (`0 21 * * 1,3,5`) | Owner DM only (hard-locked to TEST in the prompt) | TEST | Enabled | |
| `show-rate-report-eod-v12-cloud` | 6:00 PM (`0 0 * * 2-6`) | `#wfs-ttw-sales-mgmt-client` | TEST | Enabled | `eod-show-rate-update` |
| `daily-call-report-publisher-v27` | 6:30 PM (`30 0 * * 2-6`) | Owner DM, then Supabase `lead_quality` | TEST-DM | Paused | `mgmt-call-reports` |
| `ttw-crm-outcome-sweep` | Tue to Sat 9:00 AM (`0 15 * * 2-6`) | Supabase only, DM on anomaly | TEST | Paused | |
| `lead-quality-zero-row-guard` | Tue to Sat 9:00 AM (`0 15 * * 2-6`) | DM on alert only | n/a | Paused | |
| `ttw-lead-quality-backfill-guardian` | Tue to Sat 8:30 PM (`30 2 * * 2-6`) | Supabase only, DM on shortfall | LIVE | Paused | |

**Weekly**

| Task folder | Fires (MT) | Delivers to | Mode | State | Replaces local |
|---|---|---|---|---|---|
| `weekly-call-review-sourcing-v2` | Sun 7:00 PM (`0 1 * * 1`) | Owner DM (Google Doc of Loom scripts) | TEST | Enabled | |
| `weekly-clip-finder-cloud` | Mon 8:15 AM (`15 14 * * 1`) | Owner DM | LIVE | Paused | `weekly-ttw-clip-finder` |
| `sip-engine-jayden-coulter` | Mon 1:30 PM (`30 19 * * 1`) | Owner DM (LIVE: Jayden's DM, Slack id `U0BRPT6RLBU`) | TEST | Paused | |
| `webinar-report-v8` | Mon and Thu 8:30 AM (`30 14 * * 1,4`) | Per its delivery block | see prompt | Paused | |
| `pipedrive-activity-clearing-cloud` | Thu 7:00 AM (`0 13 * * 4`) | Owner DM run report | EXECUTE (writes to Pipedrive) | Enabled | `pipedrive-director-audit-labeling` |
| `weekly-pif-buyer-report` | Fri 4:00 PM (`0 22 * * 5`) | Owner DM (LIVE: client channel) | TEST | Paused | |
| `eow-report-reminder` | Fri 4:00 PM (`0 22 * * 5`) | Owner DM | LIVE | Enabled | |
| `weekly-qa-failure-review` | Fri 3:00 PM (`0 21 * * 5`) | Owner DM | LIVE | Paused | |
| `ttw-weekly-call-review-sat` | Sat 4:00 PM (`0 22 * * 6`) | Owner DM | LIVE | Enabled | |

What the cloud-only ones do (the twins are described under the local tables above):

- **daily-ttw-leaderboard-v4**: the TTW Sales Leaderboard. Closer metrics from Pipedrive pipeline 3, revenue from the live Salesboard workbook. Three sections: Most Profitable Rep (MTD as of yesterday, ranked by CDPBC), Webinar Ranking (trailing 7 days, ranked by CDPBC), and MTD Setter standings by gross. Roster comes from the WFS Active Sales Team Roster sheet (Drive fileId `1qynTKt3Z8JhJK_CkdmwMcfiR5XbD1L0NKkZ4xcImDKo`): only rows with Status = Active and In_Leaderboard = yes may appear, anyone else is excluded and flagged, never published. A rep is added to the roster only once they have a Salesboard close. The 80% failsafe blanks any show, close, or collection rate above 80% because those are almost always cross-source denominator artifacts. Reads under the work Google account only.
- **daily-sales-hype-v3**: a morning hype message in my voice for the reps channel, built from real Salesboard facts. Rotation and voice rules are in the prompt.
- **midday-hype-mwf**: Mon = close rate, Wed = CDPBC, Fri = show rate, over a rolling 7 days, bottom two vs leader. Hard-locked to DM in the prompt until you remove the lock.
- **weekly-call-review-sourcing-v2**: picks 5 lost-deal or great-close calls across the closer team each week, runs `closer-call-review-script` on each, assembles the Loom scripts into one Google Doc.
- **weekly-pif-buyer-report**: profiles every paid-in-full buyer from the past week for marketing (who they were, what pain, what closed them). Accuracy over completeness; blank fields allowed, fabricated fields are a failure.
- **lead-quality-zero-row-guard**: cheap monitor that DMs you if a weekday has zero or under 5 `lead_quality` rows in Supabase when Avoma shows calls happened.
- **sip-engine-jayden-coulter**: the sixth SIP engine, same three-week cycle as the five in `scheduled-prompts/`, but cloud-hosted.
- **eow-report-reminder**: sends ONE Slack DM on Friday at 4 PM reminding you to run the `ttw-eow-report` skill with a fresh Closer Sales Dashboard screenshot. It deliberately does not build the report, because every number has to come from your screenshot.
- **ttw-weekly-call-review-sat**: runs the `ttw-weekly-call-review` skill unattended over the week and DMs the workbook and summary.
- **daily-call-report-publisher-v27**: the cloud version of `mgmt-call-reports`, and the newer one. v27 decoupled "financially unqualified" from the Affordability sub-score (a lead is unqualified only on an articulated disqualifier). It also writes one `lead_quality` row per call to Supabase, which the webinar report and the sweeps depend on.
- **ttw-crm-outcome-sweep**: next-morning Pipedrive re-check that upgrades any `lead_quality` row whose deal has since been won.
- **ttw-lead-quality-backfill-guardian**: verifies Supabase has one row per qualifying call per weekday and re-scores only the missing ones.
- **webinar-report-v8**: the scheduled form of the `webinar-lead-quality-report` skill. Only worth running if you keep the Supabase `lead_quality` pipeline.
- **weekly-qa-failure-review**: the scheduled half of `qa-failure-loop`. Ranks what is breaking most and proposes a patch.

Two things to know about the cloud editions:
- Several read the **WFS Active Sales Team Roster** Google Sheet (fileId above) instead of a hardcoded roster. That sheet is now the single place to add or remove a rep; the "v2 roster sheet" tasks and the leaderboard all read it at step 0.
- The **Show Rate EOD v12** task made Pipedrive the primary revenue source on 8/7/26 (collected-amount custom field populated on 139 of 139 enrolled deals). The Salesboard is a reconciliation check there, not the source. The leaderboard still reads the Salesboard for revenue.
- The routines each had my full connector list attached (including personal ones like RobinHood and Alpha Vantage). When you recreate them, attach only what the prompt needs. Each one's frontmatter now lists exactly that under `connectors_required`: typically Slack, Avoma, Pipedrive, Google Drive, and Supabase only where the `lead_quality` pipeline is involved.

### Not included on purpose

`clip-farm-scout`, `clip-farm-post`, `clip-farm-report` (my personal clip-farming side business, disabled since April) and `ghl-api-smoke-test` (my own funnel tooling). Nothing to do with WFS or TTW.

---

## 3. The skills (on-demand playbooks)

### Call review (the Core Four "Call Analysis" pillar)

| Skill | What it produces | Trigger phrase |
|---|---|---|
| `closer-call-review` | One closer call graded, as a Loom teleprompter script anchored on the closer's SIP | "review this closer call" |
| `closer-call-review-script` | Same, with Avoma clip windows (start and stop timestamps) and screen-share cues quoting the talk track and objection matrix verbatim | "closer loom script" |
| `closer-call-review-slack` | The team-facing written Slack post for a closer review (status emoji, coaching bullets with word tracks, "Where it slipped", "What to preserve", `@channel` takeaways) | "make the closer slack post" |
| `setter-call-review-slack` | Written Slack post for a setter / booking call | "review this setter call" |
| `setter-call-review-script` | Loom teleprompter script for a setter call (SHARE / READ / SAY beats) | "setter loom script" |
| `ttw-daily-call-review` | Daily batch report from an uploaded Avoma transcript file | "here are today's calls" |
| `ttw-daily-avoma-report` | Same daily report, but self-serve: pulls Avoma itself and DMs you. The 6 PM report. | "run the daily call report" |
| `ttw-weekly-call-review` | Weekly or monthly lead-quality grading into RED / GREEN / GREY / BLUE / ORANGE buckets, two-tab workbook, Google Sheet, FDQ opportunity-cost economics | "run the weekly call review" |
| `ttw-avoma-clip-finder` | Coaching clips with exact clip-in and clip-out anchors | "find this week's clips" |

The closer skills ship with `references/`: the talk track, the objection matrix, the roster, and a SIP file per closer (`sips/tom.md`, `crue.md`, `vidush.md`, `turok.md`). **Update those SIP files when a rep's SIP changes; the review grades against them.**

### Numbers and reporting

| Skill | What it produces |
|---|---|
| `ttw-dashboard-metrics` | The verified formulas for every closer KPI that used to be on the Looker Studio dashboard (show rate, live calls, qualified, close rate, collections, CDPBC / GDPLC / CDPLC / GDPBC, salesboard gross vs collected). Every task and report that needs a KPI reads this so numbers agree. Looker Studio is deprecated; do not reopen it. |
| `ttw-eow-report` | Friday End of Week message: team KPIs, prose rep summary, your call-review activity, per-rep Call Analysis against the five coaching categories. Manual run only. You supply a Closer Sales Dashboard screenshot and every number comes from it. Never a rep table, first names only, DM only. |
| `webinar-lead-quality-report` | Lead quality by webinar date, joined from Pipedrive Lead Source to already-graded scores in Supabase. Manual trigger. |

### Coaching loops (the "Performance MGMT" pillar)

| Skill | What it produces |
|---|---|
| `sip-watch-loop` | Durable SIP Watch Ledger: every behavior flagged in a review gets logged, then the rep's next calls are auto-checked for that behavior and reported as new / watching / clearing / persistent, with an evidence bundle when it escalates. Every daily and weekly report should carry a SIP Watch section. |
| `compliance-trend-loop` | Rolling 30-day per-rep compliance ledger (income coaching on financing applications, guarantee language, exclusive partnership claims) with hard escalation thresholds and verbatim evidence packets for WFS leadership. |

### Keeping the machine running

| Skill | What it produces |
|---|---|
| `qa-failure-loop` | Every scheduled-task QA failure is logged instead of dying in a DM, classified against the known-issue playbook (Avoma pagination, format drift, source gaps, tool errors), and a weekly pass patches the worst offender. Use this when a report does not send. |
| `fable-review` | The audit protocol for improving any skill or scheduled task: finds logic gaps, cuts token cost, proposes upgrades. `qa-failure-loop` calls it. |
| `board-orchestrator` | Runs my personal Asana "Work Board - Cayden" one task at a time. Optional; only useful if you adopt the same board structure. |

---

## 4. First-week setup for the new director

1. **The Section 1A connector swap is already done.** What is left is to collect the credentials in that checklist and connect the standard connectors (Slack, Avoma, Pipedrive, Google Drive, Supabase if kept) under your own Claude account. Each prompt's frontmatter lists what it needs under `connectors_required`; attach only those.
2. **Upload the 17 skill folders** to your Claude account (Settings, Capabilities, Skills, upload each folder). Names must stay the same because the scheduled prompts call them by name (for example `anthropic-skills:ttw-avoma-clip-finder`; the `anthropic-skills:` prefix is just the workspace label and may differ in yours).
3. **Retarget the prompts.** Done for the director identity: Slack `U0BUZ6C0C91`, Pipedrive `27299998`, and the name swapped to David Leonty wherever the text is about the sitting director. `RETARGETING.md` lists the four values still outstanding (work Google account, Avoma account email, Team Sync organizer, browser deviceId) and the five places that still say Cayden on purpose, because changing them would falsify a record or break a lookup. Still worth confirming yourself:
   - Roster tables: confirm the closers and setters are current. As handed off: Closers Vidush Rana, Crue Lindgren, Turok Tarango, Tom Judson, Garrett McKenna, Noel Soto, Scott Jose. Setters Antonio Vespa, Petros Foustanellas.
4. **Create the scheduled tasks** in Claude Cowork, one per folder, pasting the `SKILL.md` body as the prompt and using the fire times in Section 2. Set the model to Opus and permission mode to auto (the prompts are written to run with no approval gate; safety comes from DELIVERY_MODE).
5. **Run everything in TEST first.** Every task has a `DELIVERY_MODE` (or `PROCESS_MODE`) value at the top of its CONFIG block. Leave it on TEST so the output lands only in your DM, watch two or three runs, then flip the single value to LIVE. The two client-facing reports (`ttw-daily-lead-flow-report`, `eod-show-rate-update`) are read by the client; hold those in TEST until you trust the numbers.
6. **Flip the SIP engines to LIVE only when you are ready for the rep to receive the message directly.** In TEST they message only you.

---

## 5. Non-negotiables baked into every prompt

These are the rules the prompts enforce. Keep them when you edit.

- **One Slack sender only.** The Slack Web API with the workspace bot token, never a personal user token, never a second sender. (The prompts used to say "never the native Slack connector" because the retired app held the token. Same discipline, different name.)
- **Delivery is proven by the send's return value**, never by a follow-up read: `ok`, a `ts`, and the resolved channel. A read that disagrees is a read problem and never a reason to re-send.
- **Never enter credentials, never complete a CAPTCHA, never download files.** Keys live in the environment (`SLACK_BOT_TOKEN`, `ONCEHUB_API_KEY`, `AVOMA_API_KEY`, `PIPEDRIVE_API_TOKEN`) and are never printed or written into a message.
- **No emojis in report bodies, no em dashes, no en dashes.** Single asterisks for bold. Plain hyphens, commas, periods.
- **Slack message bodies under 3000 characters** or the block splits and escapes the thread.
- **Mentions are `<@USERID>` tokens, never plain names**, and each rep is tagged exactly once.
- **Every KPI comes from `ttw-dashboard-metrics` definitions**, never re-derived. Show rate is time-based and can never exceed 100%.
- **Every coaching point traces to the Decision Leadership Objection Matrix**, and every cited call moment is transcript-verified, not notes.
- **Compliance flags never appear in team-facing Slack.** They go in the run report and the compliance ledger only.
- **Playbook rules the connector honors:** minimum 9 contact attempts before a lead is marked lost; no-show gets double-dial plus text plus email; calls are never booked more than 72 hours out.
- **The proposal queue is gone.** The old `*_propose_*` tools never mutated live data because they wrote to the Director Console for your approval. That console was part of the retired app. Two tasks now write to Pipedrive for real (`pipedrive-director-audit-labeling`, `pipedrive-activity-clearing-cloud`), and their `PROCESS_MODE: DRY_RUN` gate plus their edit allow-list are what protect the CRM. Run them in DRY_RUN first.

---

## 6. Where the originals lived on my machine (for reference only)

- Scheduled prompts: `~/Documents/Claude/Scheduled/<task>/SKILL.md`
- Skills: the Claude desktop skills cache, synced from my claude.ai account

You do not need either path. This folder is a complete copy.
