# Reply to the new director's Claude: answers to the READINESS.md audit

From Cayden (the previous director) and his Claude, September 15, 2026. This is written for the new director's Claude Code to act on. Every item below maps to a finding in your READINESS.md. Where an item needs the new director or Cayden to do something a model cannot, it says so.

The short version: your audit is correct on every point. Here is the authoritative resolution for each, plus the state that lived in Cayden's task list and did not travel with the files.

---

## A. Twinned tasks: recreate ONLY the cloud edition, never both

You are right that the disabled state lived in Cayden's Cowork, not in the files. Here is the rule that was in force at handoff. **For every pair, the `cloud-routines/` copy was the live publisher and the `scheduled-prompts/` copy was disabled.** Do not recreate the `scheduled-prompts/` side of any pair. Treat those files as archived history.

| Pair | Recreate this one | Ignore this one |
|---|---|---|
| Pipeline accountability | `cloud-routines/pipeline-accountability-report-v2-cloud` | `scheduled-prompts/pipeline-mgmt-accountability-report` |
| Midday check-in | `cloud-routines/daily-midday-checkin-v2-cloud` | `scheduled-prompts/daily-midday-checkin` |
| Midday show rate | `cloud-routines/show-rate-update-midday-cloud` | `scheduled-prompts/midday-show-rate-update` |
| EOD show rate | `cloud-routines/show-rate-report-eod-v12-cloud` | `scheduled-prompts/eod-show-rate-update` |
| Lead flow | `cloud-routines/ttw-daily-lead-flow-report-cloud` | `scheduled-prompts/ttw-daily-lead-flow-report` |
| Daily call report | `cloud-routines/daily-call-report-publisher-v27` | `scheduled-prompts/mgmt-call-reports` |
| Weekly clip finder | `cloud-routines/weekly-clip-finder-cloud` | `scheduled-prompts/weekly-ttw-clip-finder` |
| Pipedrive audit | `cloud-routines/pipedrive-activity-clearing-cloud` | `scheduled-prompts/pipedrive-director-audit-labeling` |

The only `scheduled-prompts/` tasks that were genuinely live and have no cloud twin are the five SIP engines (Vidush, Crue, Garrett, Noel, Scott). Those were local because they drove a browser to edit a Google Doc. See section F for how to run them without a browser.

So the full set to recreate is: the 21 folders in `cloud-routines/` plus the 5 SIP engines. Nothing else from `scheduled-prompts/`.

**Delivery mode on day one:** regardless of what the file says, set every recreated task to TEST (owner DM) for its first two or three runs. Cayden's LIVE flags were earned over weeks of TEST runs under his data access; yours is new. The two client-facing channels (`#wfs-ttw-sales-mgmt-client` for lead flow and EOD show rate) should be the last to go LIVE.

## B. Pipedrive EXECUTE tasks: one task, DRY_RUN first

Correct diagnosis. Only `pipedrive-activity-clearing-cloud` (Thursday 7 AM MT) should exist. Set `PROCESS_MODE: DRY_RUN` and read two run reports before flipping to EXECUTE.

Facts you need:
- Pipedrive label id **63** is the "Director Audit" label in the WFS Group Pipedrive account. The new director is in the same Pipedrive account, so that id is still valid. Verify with `getDeals` on any deal that already carries it before writing.
- The task filters activities by owner id. Cayden's was replaced by the new director's (27299998 per your audit). That is correct: the task exists to clear the director's own To-dos.
- You are right that the connector's proposal queue was a second gate. It no longer exists. `PROCESS_MODE` is the only gate. Keep the scoped allow-list in the prompt exactly as written (label add plus mark-done, nothing else).

## C. Call data: the source is Avoma, and it is a standard claude.ai connector

**Superseded by `REPLY-2-CALLIX.md`.** WFS is moving from Avoma to Callix; Avoma was still recording on September 14, so this section stays valid only for as long as Avoma runs, as the comparison baseline. Build against Callix per REPLY-2.

The Lovable connector's `calls_list`, `calls_get_analysis`, `calls_find_review_candidates`, and `avoma_api` were all thin wrappers over **Avoma**. Avoma has an official MCP at `https://mcp.avoma.com/mcp` that is available as a claude.ai connector with no custom key. Cayden's cloud routines had it attached as `Avoma_MCP` alongside the Lovable connector; the Lovable tools were only preferred because they pre-filtered by rep.

What the new director must do: get an Avoma seat in the WFS Group Avoma workspace (an admin adds them), then connect the Avoma connector in claude.ai. The recordings are workspace-wide, so once they have a seat they see every rep's calls.

Tool mapping, exact:

| Lovable tool | Avoma MCP equivalent |
|---|---|
| `calls_list(rep_id, from, to)` | `list_meetings` with a date range; filter by organizer or attendee email = the rep's `@ttwhizprogram.com` address. Call `get_current_datetime` first for relative dates. |
| `calls_get_analysis(call_id)` | `get_meeting(uuid)` for metadata, `get_meeting_transcript(uuid)` for the transcript, `get_meeting_notes(uuid)` for AI notes. |
| `calls_find_review_candidates(days_back, limit)` | `list_meetings` over the window, then apply the ranking that is written in the `ttw-avoma-clip-finder` skill (title contains "TikTok Wiz Consultation", exclude "S2C" titles where the prompt says so, duration over 15 minutes, close vs no-close). The ranking never lived in the connector. |
| `avoma_api(path)` | The Avoma REST API directly, or the MCP tool that covers that endpoint. |

Rep identity: replace every `REP_WFS_ID` (the UUIDs in the SIP engine CONFIG blocks) with the rep's email. The emails are already in the same CONFIG blocks. Jayden's is `jayden.coulter@ttwhizprogram.com`.

The "minimum 5 calls verified by transcript" gate in the SIP engines is satisfiable once Avoma is connected. Do not relax it.

## D. OnceHub: use the REST API, not the MCP (corrected September 16)

Your read is right. The OnceHub MCP (`https://mcp.oncehub.com/sse`) is a scheduling server with exactly two tools, `get_booking_time_slots` (read availability) and `schedule_meeting` (write). Confirmed from OnceHub's own docs. It cannot list bookings, and four prompts forbid OnceHub writes. **Connecting it was not wrong, it is just the wrong door.** Do not attach it to any task. The previous director's connector never used it; it called the REST API below.

The Lovable `oncehub_*` tools were wrappers over the OnceHub REST API v2. Replace them with direct calls (`curl` inside the cloud routine, key in an environment variable, no proxy; see REPLY-2 section 4 for the same pattern with Callix):

- Base: `https://api.oncehub.com/v2`
- Auth: the API key in a request header. OnceHub's header name has historically been `API-Key`; confirm on the first call against the "Try it" panel in the API reference (https://help.oncehub.com/developers/api/). The key comes from a OnceHub admin (Settings, API and Webhooks).
- **Naming change to know about:** the current v2 API calls what the prompts call "booking pages" and "master pages" **booking calendars**. There is no `/booking_pages` or `/master_pages` path in the current reference. The connector's `oncehub_get_master_page` and `oncehub_list_master_pages` were wrapping the older naming. Map them to `/booking-calendars`.

| Lovable tool | REST v2 call |
|---|---|
| `oncehub_list_bookings` | `GET /bookings?starting_time.gt=<iso>&starting_time.lt=<iso>&status=<scheduled|rescheduled|canceled>&limit=100`, page with `after` |
| `oncehub_booking_counts(master_page, status, day)` | the same `GET /bookings` call for the ET day window, then group rows by `booking_calendar` yourself. Keep the "unattributed booking rescue" rule: bookings on a rep's personal calendar come back without a shared calendar id and must be bucketed by the calendar name (for example "Vidush Rana | DLF | Closer"). |
| `oncehub_get_booking` | `GET /bookings/{id}` |
| `oncehub_find_bookings_by_attendee` | `GET /bookings?contact=<email>` (confirm the `contact` filter accepts an email; otherwise list the window and filter locally) |
| `oncehub_get_master_page`, `oncehub_get_booking_page` | `GET /booking-calendars/{id}` |
| `oncehub_list_master_pages` | `GET /booking-calendars` (filter `host`) |
| `oncehub_api` | the raw endpoint it names |

With the call source (Avoma while it lasts, then Callix; see REPLY-2) as the numerator and OnceHub REST as the denominator, the two show-rate reports produce a number again.

## E. Slack: the claude.ai Slack connector, for everything

The Lovable connector's `slack_schedule_message` posted as Cayden himself (its `slack_auth_whoami` returned `bot_id null, user cayden.johnson`). The claude.ai Slack connector David already has connected to the WFS workspace also posts as the connected user. That is the replacement, for reads and for every send, TEST and LIVE. No Slack app to create, no token to store.

Tool mapping:

| Lovable tool | claude.ai Slack connector |
|---|---|
| `slack_schedule_message(text, channel, jitter_minutes, send_at_mt, thread_ts)` | `slack_send_message` for immediate sends (pass `thread_ts` to reply in a thread); `slack_schedule_message` when the prompt sets `send_at_mt`. Delivery proof = the returned `ts`. Drop `jitter_minutes` (it was always 0). |
| `slack_list_pending`, `slack_cancel_message` | Drop them. The prompts already say `slack_list_pending` is never a delivery test. |
| `slack_read_channel`, `slack_read_thread` | Same names on the connector. |
| `mentions` parameter | Does not exist. Mentions are inline `<@USERID>` tokens in the text, which every prompt already does. |

One thing to know: messages sent through the connector may carry a small "via Claude" attribution in Slack. Send one test message to the director's own DM first and look at how it renders in the WFS workspace. The director decides whether that is acceptable in the reps channel and the client channel before any task goes LIVE; until then everything stays in TEST (DM only), which is the plan anyway.

Channels the director's Slack user must be a member of (the connector posts as them, so membership is the whole requirement; there is no bot to invite):
- `#wfs-ttw-sales-reps-dm-external` (C09ADJS1V6H), reps channel with external members
- `#wfs-ttw-sales-mgmt-client` (C098J2VG41E), client-facing management channel
- `#payments` (C07PVHXGD38), read only

The "memory DM" pattern (the midday check-in reads its own last two posts back from the director's self-DM) works unchanged once `D092C868SPP` is replaced with the director's own self-DM channel id (section H).

## F. SIP engines without a browser

The five local SIP engines drove Claude in Chrome for one purpose: appending a tab to a Google Doc. Everything else in them is connector-only. In the cloud, replace that single browser step with the Google Drive connector's document write (the `update_file` tool on the claude.ai Google Drive connector, or the Docs API `documents.batchUpdate` via `curl` with the connected OAuth token). Once that is done all six SIP engines (five local plus Jayden's cloud one) can be cloud routines with no browser, and there is no reason to keep any local Cowork task at all.

The "Issue Date" three-week cycle logic reads the doc; that read already used the Drive connector, so it needs no change.

## G. The two broken references

**`fable-mode`** does exist; it was left out of the first package by mistake. It is now in `skills/fable-mode/`. It is a reasoning and verification protocol (plan, verify, QA rigor), and `board-orchestrator` routes high-stakes work through it. Upload it with the others. `fable-review` is a different skill (an audit of a prompt or workflow) and is not a substitute.

**`mcp__scheduled-tasks__update_scheduled_task`** is a Cowork desktop tool and does not exist in cloud routines, as you found. In both show-rate prompts, replace the self-rewrite step with: append the LESSON to the QA Failure Log sheet (the `qa-failure-loop` skill already defines that sheet) and DM the owner. The owner then edits the routine prompt by hand. That is what actually happened in practice; the self-rewrite never fired successfully in the cloud either. The phrase "the ONLY write of any kind it may make" should be updated to name the QA Failure Log sheet instead.

## H. Hardcoded identity glossary (check every id against its label, as you said)

You caught the `D092C868SPP` class of error correctly. Here is every hardcoded id in the package and what it actually is, so you can audit the rest the same way.

**Cayden's identities (replace all of these with the new director's):**

| Value | What it is | Occurrences |
|---|---|---|
| `U092C85GA4D` | Cayden's Slack user id, WFS Group workspace | 61 |
| `D092C868SPP` | Cayden's Slack self-DM channel (the "memory DM") | 4 |
| `@cayden`, `@cayden.johnson` | Cayden's Slack handle | many |
| `cayden.johnson@thewfsgroup.com` | Cayden's WFS Google account (calendar, Team Sync organizer match) | 28 |
| `cayden.johnson@ttwhizprogram.com` | Cayden's TTW work Google account (the one the Salesboard reads had to run under) | 3 |
| "Caydo", "Cayden" in voice rules | Author identity in the hype and recap voice blocks | many |

**Rep roster (keep, but verify against the WFS Active Sales Team Roster sheet, which is the source of truth):**

| Rep | Role | Slack id | Pipedrive owner id | Email |
|---|---|---|---|---|
| Vidush Rana | Closer | U09EYHTG6HK | 23934614 | vidush.rana@ttwhizprogram.com |
| Crue Lindgren | Closer | U09E6D2GZAN | 23830631 | crue.lindgren@ttwhizprogram.com |
| Turok Tarango | Closer | U0B26QM90GL | 25188625 | |
| Tom Judson | Closer | U0AQ4CQTS1G | 25007532 | |
| Garrett McKenna | Closer | U0B9V1D6SPR | 25718913 | garrett.mckenna@ttwhizprogram.com |
| Rachel Snee | Closer | U0BFFJW3B0S | 26092759 | |
| Noel Soto | Closer | U0BJM5J5DNW | 26356990 | noel.soto@ttwhizprogram.com |
| Scott Jose | Closer | U0BKNUNRH40 | 26376669 | scott.jose@ttwhizprogram.com |
| Jayden Coulter | Closer | U0BRPT6RLBU | 26969976 | jayden.coulter@ttwhizprogram.com |
| Antonio Vespa | Setter | U0ATUMU1M1A | 25092474 | |
| Petros Foustanellas | Setter | U0A9LAB8NTG | 24564067 | |
| Madden McGowan | (credited on payments) | U0B1B6S8PS4 | | |
| Santiago Espinoza | Setter (example in a skill) | U0AUDUD1599 | | |

**Channels:** C09ADJS1V6H = `#wfs-ttw-sales-reps-dm-external`; C098J2VG41E = `#wfs-ttw-sales-mgmt-client`; C07PVHXGD38 = `#payments`. `C0D38JNPM9` is NOT a Slack channel; it is an OnceHub booking page id (`BP-C0D38JNPM9`) used as an example.

**Pipedrive:** pipeline 3 = TTW closer pipeline; stages 11 Lead in, 12 First Call Completed, 13 Demo Completed, 14 Follow up, 15 Funding, 16 Enrolled; label 63 = Director Audit. Custom field hashes for First Call Date, First Call Show Up, and Lead Source are in the leaderboard prompt and are account-wide, so they still apply.

**REP_WFS_ID values** (UUIDs like `97246e2a-...`) were internal to the Lovable app. Delete them; use the rep's email per section C.

## I. Google Drive files that Cayden must share

These are all owned by Cayden or the WFS Group Drive. A model cannot fix access; **Cayden needs to share each one with the new director's work Google account**, editor on the SIP docs and the QA log, viewer on the rest. Cayden, this is your action list:

| File | fileId | Used by |
|---|---|---|
| TTW Salesboard 2026 (sheet, read-only, accounting-managed) | `1_5YMQVATclX5gRRJfkqG-wfyWP23TYlDoLugu8Tz_W4` | leaderboard, hype, EOD show rate, SIP engines |
| WFS Active Sales Team Roster (sheet) | `1qynTKt3Z8JhJK_CkdmwMcfiR5XbD1L0NKkZ4xcImDKo` | leaderboard, v2 check-in, v2 accountability, review sourcing |
| Decision Leadership Objection Matrix, Sales Rep Quick Reference (doc) | `16Xg8L1ouymErNyjA9WnYjxicF9f7EXoS7z4fwjoOUlE` | every SIP engine, every review skill |
| Objection Matrix link used in hype messages (doc) | `1wJqNR5JT6-m9IpcSsf4k1ICFgcaVOFT53sOY1iNORNc` | daily-sales-hype |
| SIP master template (doc, never edit) | `1X3new1x8VaDtQuA7WP7v2OZ7E5WXMXWyA-mnkR6JR7I` | SIP engines |
| SIP doc, Vidush Rana | `1K355E4r2Iti7G_g9_rE4VsFHrwTkoEtCBbkHTlzf-8Q` | sip-engine-vidush-rana |
| SIP doc, Crue Lindgren | `1heyBUvV1IT-hfG4TW5uCJrMfzsvghcEc2BWRSIIbPWc` | sip-engine-crue-lindgren |
| SIP doc, Garrett McKenna | `1vLZotZ1TjCokpFpF-JKStDP-jItDlzSon02ttfmpJcE` | sip-engine-garrett-mckenna |
| SIP doc, Noel Soto | `15ew_N7HuUWkC3lumddd5XkFU0JQVs0ipUxj1Ivsypj4` | sip-engine---noel-soto |
| SIP doc, Scott Jose | `1mIyWP5V3bQjVVEjR9ncS0h-YBhH1jBj1Lmpipq-ADNQ` | sip-engine---scott-jose |
| SIP doc, Jayden Coulter | `1bR4DhgAM5pa8Fe77GxfDWYELxgNX-3mxEMLC-34BmEE` | sip-engine-jayden-coulter |
| Leadflow Google Doc (retired source, read-only reference) | `16qeQ7C_jbAZ34Ewv8yGkquvtrPd0dzLBxJs0i0Db8aw` | older show-rate prompts only |
| Webinar Reports doc | `1fXO0j8AjaFhFZRGSYpN0-A0rS4TgmDXiPnzJPSc2CkU` | webinar-report-v8 |
| QA Failure Log (sheet) | referenced by name in `qa-failure-loop`; Cayden to locate and share, or the new director creates a fresh one with the columns the skill lists | qa-failure-loop, weekly QA review |

The SIP docs are personnel records. Cayden should confirm with WFS leadership that transferring them is appropriate before sharing.

## J. Supabase: it is already off, and that is fine

The Supabase project `apdwbbocldfsklvcwaqd` ("TTW Sales Ops") is **paused (status INACTIVE)** in Cayden's Supabase org. Every task that depended on it was already paused at handoff: `daily-call-report-publisher-v27` (its Supabase write), `ttw-crm-outcome-sweep`, `ttw-lead-quality-backfill-guardian`, `lead-quality-zero-row-guard`, and `webinar-report-v8`. So Supabase is not a blocker for anything that was running.

Recommendation: run `daily-call-report-publisher-v27` with its Supabase step removed (the prompt already says that step is non-blocking and happens after Slack delivery, so deleting it changes nothing about the report). Skip the four Supabase-only tasks unless the new director wants lead-quality history, in which case create a new Supabase project and table `public.lead_quality` with these columns, taken from the v27 prompt's field mapping:

`meeting_uuid text primary key`, `call_date date`, `rep text`, `prospect_name text`, `prospect_email text`, `affordability int`, `decision_maker int`, `timeline int`, `intent int`, `lead_score int`, `outcome text`, `outcome_transcript text`, `outcome_pipedrive text`, `outcome_source text`, `pipedrive_deal_id bigint`, `lead_source_label text`, `collected numeric`, `collected_transcript numeric`, `collected_pipedrive numeric`, `financially_qualified boolean` (nullable, three-state), `dq_reason text`, `rubric_version text`, `webinar_cohort text`, `webinar_date date`, `source_master_page_id text`, `created_at timestamptz default now()`, `updated_at timestamptz default now()`.

Plus `public.report_run_log` (one row per checked day: `run_date`, `task`, `rows_found`, `rows_expected`, `outcome`, `notes`). Then point the five tasks at the new project id. If "the Callix design" in your audit refers to something on your side that makes Supabase mandatory, that is a new decision the new director is free to make; nothing in Cayden's setup required it to be live.

## K. Order of operations, so nothing double-fires

1. Do nothing in the cloud until sections C, D, E credentials and section I file access are in place.
2. Rewrite the 21 cloud routines plus the 5 SIP engines per Section 1A of the README and sections C to F above. Every task to TEST / DRY_RUN.
3. Recreate them as cloud routines one at a time, starting with the low-risk owner-DM ones (EOW reminder, clip finder, weekly call review), then the leaderboard and hype (reps channel), then the two client-facing reports last.
4. After each has two clean TEST runs whose message matches its template line for line, flip that one task to LIVE.
5. Never have a `scheduled-prompts/` task and its `cloud-routines/` twin both enabled.

## L. What only humans can do (summary)

**New director:** Avoma seat, OnceHub API key (admin), Slack connector under their own account, Google Drive connector under their work account, Pipedrive connector, decide on Supabase.

**Cayden:** share the 14 Drive files in section I, confirm the SIP-doc transfer with leadership, and answer any question about a rule's intent that the prompts do not explain.
