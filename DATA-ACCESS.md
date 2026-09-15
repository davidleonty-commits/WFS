# Data access contract (replaces the Lovable WFS connector)

Every scheduled prompt and skill in this package used to reach Slack, OnceHub, Avoma and
Pipedrive through one custom MCP server (`Lovable_WFS_Slack`, hosted at
`commandcenter.aiautomating.com`) that belonged to the outgoing director. That server is gone.

This file is the canonical replacement map. Section 1A of `README.md` ordered the swap; this
file is what the swap was done against, so every prompt says the same thing about the same
call. The prompts themselves are self-contained (a cloud routine cannot read this file at run
time), so the contracts below are inlined into each prompt that needs them. Edit here first,
then propagate, so the copies never drift.

Policies did not change. Thresholds, rosters, templates, QA gates, delivery modes, day
boundaries and status filters are all exactly as the outgoing director left them. Only the
data-access method changed.

---

## 1. Slack

One sender, always: the WFS Group workspace **bot token**. Never a personal user token, never a
second sender. (The old rule said "never the native Slack connector" only because the Lovable app
held the bot token. It no longer does, so the native Slack API IS the sender now. The
single-sender discipline is unchanged.)

Reach the Slack Web API either through the Slack MCP connector in claude.ai, or with a direct
HTTPS call: `POST https://slack.com/api/<method>` with `Authorization: Bearer $SLACK_BOT_TOKEN`
and `Content-Type: application/json`.

| Old call | New call |
|---|---|
| `slack_schedule_message(text, channel)` | `chat.postMessage(channel, text)` |
| `slack_schedule_message(..., thread_ts)` | `chat.postMessage(channel, text, thread_ts)` |
| `slack_schedule_message(..., send_at_mt)` | `chat.scheduleMessage(channel, text, post_at)` where `post_at` is that Mountain time as Unix epoch seconds |
| `slack_schedule_message(..., jitter_minutes = 0)` | `chat.postMessage`, sent immediately |
| `slack_schedule_message(..., jitter_minutes = N > 0)` | pick a random whole number of minutes `j` in `[0, N]`; `j = 0` sends immediately with `chat.postMessage`, otherwise `chat.scheduleMessage` with `post_at = now + j minutes` |
| `slack_schedule_message(..., agent = "...")` | no equivalent, drop the field (it was an internal label in the Lovable app) |
| `slack_schedule_message(..., mentions = [...])` | no equivalent and none needed: mentions are inline `<@USERID>` tokens in `text`, each rep tagged exactly once |
| `slack_send_sos(target, text)` | no second sender exists. Retry `chat.postMessage` ONCE after a short pause; if the retry also fails, report the failure in the run summary and send nothing else |
| `slack_list_pending()` | `chat.scheduledMessages.list`. Only meaningful for messages scheduled with `chat.scheduleMessage`; an immediate `chat.postMessage` never enters a queue, so a "wait for it to clear pending" loop has nothing to wait for and is dropped |
| `slack_cancel_message(id)` | `chat.deleteScheduledMessage(channel, scheduled_message_id)`, and only while the message is still scheduled and unposted |
| `slack_read_channel(channel_id, limit, oldest, latest)` | `conversations.history(channel, limit, oldest, latest)` |
| `slack_read_thread(channel_id, message_ts)` | `conversations.replies(channel, ts)` |
| `slack_send_message(channel_id, text)` | `chat.postMessage(channel, text)` (same single sender as everything else) |
| `slack_search_users(query)` | `users.list`, or `users.lookupByEmail(email)` |

**Delivery verification.** The prompts' DELIVERY VERIFICATION steps used to check the Lovable
queue row. The direct-API equivalent, and it is still the RETURN VALUE of the send, never a
follow-up read:

1. `ok: true` in the response body, and
2. a non-empty `ts` (`chat.postMessage`) or `scheduled_message_id` (`chat.scheduleMessage`), and
3. the returned `channel` id equals the destination the DELIVERY_MODE resolved to.

Any of the three missing means the send is NOT verified: report the failure, do not re-send
blindly (a blind re-send is how a report gets posted twice).

**Errors.** `invalid_auth` / `not_authed` means the bot token is missing or rotated: report that
`SLACK_BOT_TOKEN` needs refreshing, and send nothing else. `channel_not_found` or
`not_in_channel` means the bot is not in that conversation: report it and never improvise a
different destination. `msg_too_long` means the 3000-character body cap was missed upstream.

**Scopes** the token needs: `chat:write`, `chat:write.public`, `channels:read`,
`channels:history`, `groups:history`, `im:write`, `im:history`, `users:read`.

---

## 2. OnceHub

Two ways in, same credential.

**MCP (configured in this repo).** `.mcp.json` registers a project-scoped server:

```json
{ "mcpServers": { "oncehub": {
  "type": "sse",
  "url": "https://mcp.oncehub.com/sse",
  "headers": { "API-Key": "${ONCEHUB_API_KEY}" }
} } }
```

The key is read from the environment, never committed. Put it in
`.claude/settings.local.json` (gitignored; copy `.claude/settings.local.json.example`).
Claude Code asks you to approve a project MCP server the first time it loads it.

Two notes on the vendor's own docs, which contradict themselves: the prose says the header is
`API-Key: <key>` while their sample config shows `authorization: Bearer <key>`. This repo uses
`API-Key`, matching the prose and the REST convention below. If the server rejects it, swap to
`"Authorization": "Bearer ${ONCEHUB_API_KEY}"`. Likewise their sample says `"type": "http"` for
a `/sse` URL; if `sse` fails to connect, try `http`.

**Direct REST (what the prompts use).** `GET https://api.oncehub.com/v2/<resource>` with header
`API-Key: $ONCEHUB_API_KEY`.
Every list endpoint is cursor-paginated: follow `next` until it is null. A partial sweep is
never a publishable number.

| Old call | New call |
|---|---|
| `oncehub_booking_counts(master_page, status, date_field, date_from, date_to)` | `GET /v2/bookings` with the same window on the same date field, `status` filter applied, paginated to the end; then group by `booking_page.master_page` yourself and count |
| `oncehub_list_bookings(...)` | `GET /v2/bookings` |
| `oncehub_get_booking(id)` | `GET /v2/bookings/{id}` |
| `oncehub_find_bookings_by_attendee(email, name, window)` | `GET /v2/bookings` over the window, then match `attendee.email` / `attendee.name` client-side |
| `oncehub_list_master_pages()` | `GET /v2/master_pages`, paginated to the end |
| `oncehub_get_master_page(id)` | `GET /v2/master_pages/{id}` |
| `oncehub_get_booking_page(id)` | `GET /v2/booking_pages/{id}` |
| `oncehub_api(path, query)` | call the named endpoint directly, it was a raw passthrough |

What the wrapper used to do for you, and now has to be done in the prompt:

- **Counting and grouping.** `booking_counts` returned `rows` (one per master page, with a
  label), `total_all` and `total_attributed`. Build the same shape yourself: one row per
  `master_page` id with its count, `total_all` = every booking in the window, `total_attributed`
  = the bookings that carry a master page.
- **Unattributed booking rescue** (this is a policy, keep it): a booking made on a rep's personal
  booking page has no master page, so it never lands in a row and used to deflate the
  denominator. `total_all - total_attributed` is the unattributed set; bucket those by their
  booking-page name (`GET /v2/booking_pages/{id}` when the name is not inline) and fold them into
  the right scope before computing any rate.
- **Truncation.** The wrapper silently capped at roughly the newest 100 bookings on some
  windows, which is why several prompts say a creation-time slice from `booking_counts` is
  unreliable and must be cross-checked. Direct pagination removes the cap, but the rule behind it
  stands: paginate to the end, record how many pages you read, and never publish a count you did
  not sweep completely.
- **Rejected parameters.** The wrapper rejected `starting_time_from` / `starting_time_to` /
  `in_trash` on some paths, so several prompts filter dates client-side. Client-side filtering on
  a fully paginated sweep stays correct either way, so those instructions were kept.
- **In-trash bookings** were excluded by the wrapper by default. Exclude them yourself: drop any
  booking whose `in_trash` is true.
- Day boundaries and status filters are unchanged and stated per prompt (the day slices are
  Eastern-time boundaries on `starting_time`).

---

## 3. Avoma

Avoma MCP (`list_meetings`, `get_meeting`, `get_meeting_transcript`, `get_meeting_notes`,
`get_current_datetime`) is the primary path and needs no key. The direct REST API is the
fallback: `https://api.avoma.com/v1/...` with header `Authorization: Bearer $AVOMA_API_KEY`.

| Old call | New call |
|---|---|
| `calls_list(rep_id, from, to)` | `list_meetings` (or `GET /v1/meetings/` with `from_date`, `to_date`, `page`, `page_size`) filtered to the rep by organizer / attendee **email**, not by a Lovable UUID |
| `calls_get_analysis(call_id)` | `get_meeting` + `get_meeting_transcript` + `get_meeting_notes` (or `GET /v1/meetings/{uuid}`, `GET /v1/transcriptions/?meeting_uuid=`, `GET /v1/notes/?meeting_uuid=`) |
| `calls_find_review_candidates(days_back, limit)` | `list_meetings` over the window, then rank with the rules in the `ttw-avoma-clip-finder` skill |
| `avoma_api(path, query)` | call the named Avoma endpoint directly |

Two gaps the swap has to fill, because they were the Lovable app's own work and not Avoma's:

1. **The scorecard.** `calls_get_analysis` returned a scored object (lead_score, rep_score,
   primary_objection, financially_qualified, close_attempts, downsell_offered, lead_bucket,
   payment_type and so on) alongside the transcript. Avoma returns no such fields. Every prompt
   that read them now SCORES THE TRANSCRIPT ITSELF against the rubric it already carries: the
   `ttw-daily-call-review` scorecard, the Decision Leadership Objection Matrix, and the
   `ttw-dashboard-metrics` definitions. The scoring rules did not change; only who runs them did.
   A score is never guessed from AI notes, it is read off the transcript, as before.
2. **The ranking.** `calls_find_review_candidates` returned calls pre-ranked for coaching. The
   ranking rules live in the `ttw-avoma-clip-finder` skill and are applied after `list_meetings`:
   keep real recorded consultations (duration over 15 minutes, title contains "TikTok Wiz
   Consultation" or the closer-consultation equivalent, a usable speaker transcript), then rank
   closes against no-closes and the objection-handling quality of each.

Identity: the rep key is the **Avoma user email**. Prompt CONFIG blocks that carried a
`REP_WFS_ID` UUID now carry `REP_AVOMA_EMAIL`.

---

## 4. Pipedrive

Pipedrive MCP, or `https://api.pipedrive.com/v1/...` with `api_token=$PIPEDRIVE_API_TOKEN`.
Closer pipeline is pipeline 3, as before.

| Old call | New call |
|---|---|
| `pipeline_smart_view(view="expected_close_past_due", limit)` | `getDeals` on pipeline 3, `status=open`, keep deals whose `expected_close_date` is before today (Mountain) |
| `pipeline_smart_view(view="hot_list_7d", limit)` | `getDeals` on pipeline 3, keep open deals labeled Hot List with activity in the last 7 days |
| `pipeline_smart_view(view="deals_won_last_7d", limit)` | `getDeals` on pipeline 3, `status=won`, keep deals whose `won_time` is within the last 7 days |
| `reps_scoreboard(window_days)` | compute per-rep KPIs from Pipedrive plus the Salesboard workbook using the `ttw-dashboard-metrics` formulas, which is what the connector did internally |
| `reps_scoreboard` used only to map an id to a name | resolve through the WFS Active Sales Team Roster sheet instead (Pipedrive owner id and Avoma email columns) |

**Identity, and the reason the old prompts say "map by rep_id, NEVER by name string":** the
roster carries duplicate full names across different people, so a name match silently merges two
reps. That hazard is unchanged. The stable keys are now the **Pipedrive owner id** (numeric, for
deal and activity data) and the **Avoma organizer email** (for call data). Join on those, never
on a name.

---

## 5. Director Console tools, removed

`calls_propose_review_note`, `tracker_propose_entry`, `pipeline_propose_reopen`,
`reps_propose_coaching_action`, `proposals_list`, `director_daily_brief` and `compliance_scan`
were UI features of the Lovable app's Director Console. There is nothing to swap them for. The
calls are removed. Where a prompt said "propose", it now writes the note directly to its target
(a Pipedrive note, or a Slack DM to the director).

Note that the old non-negotiable "write tools in the WFS connector never mutate live data, they
create proposals you approve in the Director Console" no longer has a mechanism behind it. Two
tasks now write for real: `pipedrive-director-audit-labeling` and
`pipedrive-activity-clearing-cloud`. Their own `PROCESS_MODE: DRY_RUN` gate is what stands
between a run and a live Pipedrive edit. Run them in DRY_RUN first.

---

## 6. Credentials

Nothing in this repository holds a secret, and no key belongs in a prompt body. Store these the
way your environment stores secrets (claude.ai connector settings, environment variables, or a
`.env` the tasks read):

| Variable | Service | Needed by |
|---|---|---|
| `SLACK_BOT_TOKEN` | Slack, WFS Group workspace | every task |
| `ONCEHUB_API_KEY` | OnceHub, Settings, API and Webhooks | lead flow report, both show-rate reports, EOD booking health, webinar report |
| `AVOMA_API_KEY` | Avoma, Settings, API (optional if the Avoma MCP connector is attached) | call reports, SIP engines, clip finder, review sourcing, weekly call review, all review skills |
| `PIPEDRIVE_API_TOKEN` | Pipedrive (optional if the Pipedrive MCP connector is attached) | accountability report, leaderboard, director audit, KPI formulas, webinar report |
| Google OAuth | Drive / Docs / Sheets, under the director's WORK Google account | SIP engines, leaderboard, sales hype, EOW, roster sheet |
| `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` | Supabase project `apdwbbocldfsklvcwaqd` | only if the `lead_quality` pipeline is kept |

Connect only what a given prompt needs. Each prompt's frontmatter lists its own required
connectors under `connectors_required`.
