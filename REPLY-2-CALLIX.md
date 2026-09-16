# Reply 2: call data and bookings, the API way. Supersedes section C of the first reply.

From Cayden, September 16, 2026. For the new director's Claude Code. Everything in TROUBLESHOOTING-REPLY.md still holds except section C (Avoma), which this file replaces. Section D (OnceHub) was corrected in place; the corrected version is what is in the package now.

**Changes since your last report (so you do not need to re-audit):** prompts and skills are still byte-identical to the first package. Section E of TROUBLESHOOTING-REPLY.md now states plainly that the claude.ai Slack connector is the sender for everything, TEST and LIVE, which matches what you already rewrote; it adds one check (send a test to the director's DM and look at how the "via Claude" attribution renders before anything goes LIVE). `CALL-SHEET.md` is new and is for the humans: it walks Cayden and the director through collecting every input you are waiting on in one sitting. Section 8 below is updated. **New in this version:** the client channel is off limits (section 0), and capability 3 (is it a consultation) is now a concrete rule, not a verify-and-see (section 3).

## 0. The client channel is off limits

Nothing automated may post to `#wfs-ttw-sales-mgmt-client` under the new director. The client reads that channel. The five tasks that used it as LIVE_TARGET (lead flow, midday show rate, EOD show rate, webinar report, PIF buyer report) now deliver to the director's own DM; the director forwards to the client by hand if and when they choose. `personalize.py` rewrites those `LIVE_TARGET` lines and flags any remaining sentence that still reads like a send to that channel; rewrite each one (the PIF report's inline mode text, the two task descriptions, the local `mgmt-call-reports` twin). Reading the channel is fine; the EOW skill does.

## 1. Your open question: Avoma or Callix

Both, for now. WFS is moving from Avoma to Callix, but on September 16 I confirmed Avoma was still recording TikTok Wiz consultation calls as of **September 14** (full timestamped transcripts, four closers). So the cutover is in progress, not done.

Do this, in order:
1. Ask a WFS admin: "Is the Avoma workspace being cancelled, and on what date? Are the Zoom consultation calls booked through OnceHub being recorded in Callix today?" Put the answer, with the date, in your summary.
2. Build the Callix layer per section 3 below. It is the destination either way.
3. If Avoma is still live on the day you go to TEST, run the daily call report and the midday show rate against both sources for two real days and compare consultation counts. Cut over to Callix on the admin's date, or when the counts match, whichever is later.
4. The Avoma layer you already built is not wasted; it is the comparison baseline. The original section C tool map stands for as long as Avoma runs.

Historical scoring lived only in the paused Supabase project and does not carry forward. Lead-quality history, if kept at all, starts fresh.

## 2. What replaces the WFS connector: two API keys and one connector

The old connector was one plug doing three jobs. It is replaced by three plugs Claude Code already knows how to use. No app, no proxy, no hosting. The previous director's Lovable app was not a proxy; it did joins, classification, scoring, and a proposal queue. Those now live in the prompts as sentences or are dropped. Do not rebuild it.

| Job the connector did | Replacement | Plug it in |
|---|---|---|
| Call data: `calls_list`, `calls_get_analysis`, `calls_find_review_candidates`, `avoma_api` | **Callix** | Local: `claude mcp add callix -e CALLIX_API_KEY=<key> -- npx -y @callixorg/mcp-server`. Cloud routines: `curl` against the Callix REST API with `CALLIX_API_KEY` set as an environment variable on the claude.ai Code environment (see section 4). |
| Bookings: `oncehub_booking_counts`, `oncehub_list_bookings`, `oncehub_get_master_page`, `oncehub_api` | **OnceHub REST API v2** via `curl` | `export ONCEHUB_API_KEY=<key>` locally, or set it on the cloud environment. You already did this; section 5 has the smoke test. The OnceHub MCP you connected first is NOT this; it only books meetings. |
| Slack: `slack_schedule_message`, `slack_read_channel`, `slack_read_thread` | **claude.ai Slack connector** | Already done per your last report. |

Keys go in environment variables or connector settings, never in a prompt file.

## 3. Callix tool map

Callix is `callix.io` (prospects, payments, deal analyses), not the `callix.ai` dialer. The MCP is `@callixorg/mcp-server`. Tool names and one-line descriptions below are from Callix's own MCP page. **Parameter and response field names are not yet verified.** On your first call to each tool, read the schema and the response and correct this map where it differs.

### The six capabilities every call-dependent prompt needs

| Capability | Old Lovable tool and field | Callix tool | Verify on first call |
|---|---|---|---|
| 1. List calls in a date window | `calls_list(from, to)` | `list_calls`; call `get_current_time` first for relative windows, as the prompts already do | Date range parameter? Timezone of timestamps? Pagination and page cap? |
| 2. Filter to one rep | `calls_list(rep_id=...)` | `list_calls` rep filter | What identifies a rep: email, Callix user id, or name? Build a roster map and put it in each SIP engine CONFIG where `REP_WFS_ID` was. |
| 3. Identify a TTW consultation | title contains "TikTok Wiz Consultation"; `is_consultation`; `call_type` | **Do not use the Callix call title for this.** Classify by joining each call to its OnceHub booking; the rule is spelled out under "Consultation classification" below. It is deterministic, needs no Callix field beyond lead email and start time, and is exactly how the old connector computed `is_consultation` and `call_type`. | Only that `list_calls` returns a lead email (or phone) and a start time per call. |
| 4. Duration for the 15-minute floor | `duration_seconds`, null when no recording | whatever `get_call` returns for length | Unit, and how "no recording" is represented (null, 0, absent). The floor treats no recording as not live. |
| 5. Transcript with speakers and timestamps | `calls_get_analysis(id).transcript` as `[mm:ss] Speaker: line` | `get_call` ("including its full transcript") or `list_calls` with transcripts on | Timestamps and speaker names per line? The clip finder's clip-in/clip-out anchors need timestamps; without them that skill quotes lines without times and the prompt must say so. |
| 6. Stable call id | `id` (uuid) | the id `list_calls` returns and `get_call` accepts | Rename any `meeting_uuid` you create to `call_id`. |

For reference, the exact record shape the prompts were written against, from a live row of the old connector:

```
id, title ("Sara M Jamison - TikTok Wiz Consultation"), source (the OnceHub booking calendar name, e.g. "Webinar 09 13 26 | Paid | Closer | 45min"),
call_type (webinar_closer | s2c_closer | setter_intro | consultation | sync | other), is_consultation, started_at, ended_at,
duration_seconds (null = no recording), rep_id, lead_email, state (completed | canceled | not_recorded), transcript ("[mm:ss] Speaker: line")
```

### Consultation classification: the fix for the numerator

The show-rate reports, the daily call report, the clip finder, and the SIP engines all need to know which calls are TTW consultations and of which kind. The old prompts keyed on the Zoom meeting title. Callix may not carry that title, and guessing a Callix field would be the failure mode where the report still prints a plausible number. So the source of truth for "what kind of call was this" becomes the **OnceHub booking**, which every consultation was scheduled through. This is what the old connector did internally: its `source` field was the OnceHub booking calendar name and `call_type` was derived from it.

Put this block into every call-dependent prompt in place of the title rule:

1. **Pull the day's bookings from OnceHub** (`GET /v2/bookings`, all statuses, the ET day window). Keep per booking: booking calendar name, lead email, start time, status.
2. **Pull the day's calls from Callix** (`list_calls`, same window). Keep per call: id, rep, lead email (or phone), start time, duration, transcript.
3. **Match** a call to a booking when the lead email matches (case-insensitive, trimmed) and the start times are within 30 minutes. If Callix has no lead email on a call, match on lead name plus rep plus start time within 30 minutes, and flag the match as name-based in the anomaly notes.
4. **Derive `call_type` from the booking calendar name**, case-insensitive: contains "Webinar" = `webinar_closer`; contains "S2C" = `s2c_closer`; contains "Setter" or "15min" or "Introduction" = `setter_intro`; contains "Closer" without Webinar or S2C (a rep's personal calendar such as "Vidush Rana | DLF | Closer") = `consultation`; anything else = `other`. `is_consultation` = call_type in {`webinar_closer`, `s2c_closer`, `consultation`}.
5. **Live** = matched AND duration at or above 900 seconds. Duration null or missing = not live.
6. **Unmatched Callix call** (no booking with that lead) = `other`; list it in the anomaly notes with its lead and rep, never count it as a consultation. **Unmatched OnceHub booking** (no Callix call) = scheduled, did not go live. That is the show-rate denominator working as designed, not an error.
7. **Reconcile once per run:** the count of matched consultations must not exceed the count of consultation bookings for the day. If it does, that is a QA FAIL (same rule as the existing "show rate above 100%" gate).

This removes the title dependency entirely, keeps the S2C versus Webinar split the reports need, preserves the unattributed-booking rescue (personal calendars classify as `consultation`), and works identically whether the call platform is Avoma, Callix, or anything else. The only thing Callix must supply is a lead email (or name) and a start time per call; verify those two on the first `list_calls`.

If Callix turns out not to have the Zoom consultation calls at all (it records phone calls, the consultations happen on Zoom), then no classification rule helps: the numerator is missing and Avoma must stay until Callix or another recorder captures them. That is what the WFS admin question in section 1 settles.

### Analysis and scoreboard tools

| Old tool | Callix tool | Note |
|---|---|---|
| `calls_get_analysis` (scorecard, financial signals, close attempts, transcript) | `get_deal_analysis`; `list_deal_analyses` to enumerate | Callix's scorecard is Callix's rubric. The prompts score against the WFS rubric written in them. Use Callix's scores as a cross-check in anomaly notes, never as the published score. The transcript is what the prompts consume. |
| `calls_find_review_candidates` | `list_deal_analyses` over the window, then the ranking rules in `ttw-avoma-clip-finder` | Ranking never lived in the connector. |
| `reps_scoreboard` | `get_rep_performance` | KPI definitions of record stay in `ttw-dashboard-metrics` (Pipedrive plus Salesboard). `get_rep_performance` and `get_metrics` are reconciliation inputs only. |
| none | `get_metrics`, `get_insights`, `get_ad_performance`, `list_payments` | New. Not needed by any existing task. `list_payments` must not become a third published revenue figure; Pipedrive is primary (August 7 decision in the EOD v12 prompt). |

### Hard rule: Callix writes are off limits

`create_prospect`, `update_prospect`, `log_event`, `record_payment`, `manage_webhooks` write straight to the account (the old connector's writes only created proposals). Add Callix to the READ-ONLY list in every prompt's HARD RULES block and name those five tools as forbidden. The only writes in this package remain the Pipedrive audit's label-and-mark-done and each SIP engine's one Google Doc.

## 4. Local versus cloud, and why no proxy

The Callix MCP is a local `npx` process. Cloud routines cannot start one; they only attach remote claude.ai connectors. So per task:

- **Local Cowork task on the director's laptop:** the MCP works as-is. Fine for on-demand skills (call reviews, clip finder). Laptop must be on.
- **Cloud routine:** `curl` the Callix REST API with `Authorization: Bearer $CALLIX_API_KEY`, the key set as an environment variable on the claude.ai Code environment the routine runs in. The MCP page says it "communicates with the Callix API using your key and inherits the same rate limits as direct API calls," so the endpoints exist and the key is the same. Read the endpoint paths out of the `@callixorg/mcp-server` package source or get the REST docs from Callix support. Recommended for every scheduled report.
- **Only if the cloud environment cannot hold an environment variable:** ask Callix for a hosted MCP endpoint, and failing that a roughly 50-line Cloudflare Worker that holds the key and forwards `list_calls` and `get_call`. That is the whole extent of any "proxy." Check the environment settings before building anything.

Same pattern for `ONCEHUB_API_KEY`.

## 5. OnceHub: you have the API plugged in. Prove it with one call.

```bash
curl -s -H "API-Key: $ONCEHUB_API_KEY" \
  "https://api.oncehub.com/v2/bookings?starting_time.gt=2026-09-15T04:00:00Z&starting_time.lt=2026-09-16T04:00:00Z&limit=100"
```

That is yesterday in ET, the day boundary every show-rate and lead-flow prompt uses. Check:
1. Rows come back. On 401, try `Authorization: Bearer` per the "Try it" panel at https://help.oncehub.com/developers/api/.
2. Each row has a booking-calendar field and a `status`. Those are what the denominator groups on. Note the exact names; the prompts say `master_page`, which no longer exists in v2 (booking pages and master pages are now **booking calendars**, `GET /booking-calendars`).
3. Some rows have no shared calendar (booked on a rep's personal calendar). That is the "unattributed booking rescue" case in the midday prompt; if you see them, the rule ports over.

The full endpoint table is in TROUBLESHOOTING-REPLY.md section D (corrected). With OnceHub as denominator and Callix (or Avoma while it lasts) as numerator, both show-rate reports produce a number again.

## 6. Order of work

1. Callix: connect locally, call `get_current_time`, then `list_calls` for yesterday with no filters. Read the raw response. Fill every "verify" cell in section 3.
2. Confirm you can produce, per call: id, rep, lead email, start, duration, is-consultation, transcript. If any is missing, stop and report which; each gates specific tasks.
3. OnceHub: run the section 5 smoke test.
4. Decide local or cloud per task (section 4) and record it in each CONFIG block.
5. Rewrite the prompts. Keep every rule, threshold, roster, template, and QA gate. Change only the access method. Then `python3 personalize.py --check-connector` must return zero.
6. TEST runs to the director's DM, two clean days per task, Avoma comparison where available, then LIVE one task at a time. Client-facing channels last.

## 7. Still owed by the director

The six identity values from your last report. "David Leonty" is a display name; the handle is the part after the @. Keep asking until all six are in; do not fill any from context. Keep running `personalize.py --check` after every edit pass; it already caught two misses a careful pass did not.

## 8. For Cayden, not for you

The previous director's ingest app was still receiving WFS transcripts on September 14 under its own Avoma key. His plan is to disable every scheduled task on his side on his last day, so nothing posts from his account after that. Whether the app's Avoma sync itself is switched off or the key revoked is his and WFS's decision; do not wait on it, and do not treat it as a blocker for anything in this package. If a WFS admin asks, that is the state of it.
