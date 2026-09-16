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

One sender, always: **the claude.ai Slack connector**, which posts as YOU (the connected user),
never as a bot. This is the exact equivalent of what the retired app did: its
`slack_auth_whoami` returned `user cayden.johnson, bot_id null`, i.e. it posted as the director
himself, not as an application.

That matters beyond plumbing. These messages are written to sound like the director wrote them
("in David's voice", "as if David is personally recapping the call"). A bot-authored message
with the director's voice reads wrong, and rep mentions behave differently. **No bot token is
needed, and none should be created.**

The old rule "never the native Slack connector" existed only so two senders could not race each
other. The native connector IS the single sender now. Delete the lock, keep the discipline.

| Old call | New call |
|---|---|
| `slack_schedule_message(text, channel)` | `slack_send_message(channel, text)` |
| `slack_schedule_message(..., thread_ts)` | `slack_send_message(channel, text, thread_ts)` |
| `slack_schedule_message(..., send_at_mt)` | `slack_schedule_message` with the send time |
| `slack_schedule_message(..., jitter_minutes)` | no equivalent, and none needed: it was always 0 |
| `slack_schedule_message(..., agent = "...")` | no equivalent, drop the field |
| `slack_schedule_message(..., mentions = [...])` | no equivalent and none needed: mentions are inline `<@USERID>` tokens in `text`, each rep tagged exactly once |
| `slack_send_sos(target, text)` | no second sender exists. Retry `slack_send_message` ONCE, then report the failure |
| `slack_list_pending()` | drop it. The prompts already say it was never a delivery test |
| `slack_cancel_message(id)` | `slack_cancel_message`, and only for a message scheduled and not yet posted |
| `slack_read_channel(...)` | `slack_read_channel` (same name on the connector) |
| `slack_read_thread(...)` | `slack_read_thread` (same name) |
| `slack_send_message(...)` | `slack_send_message` (same name) |
| `slack_search_users(query)` | `slack_search_users` |

**Delivery verification.** The RETURN VALUE of the send, never a follow-up read: `ok` plus a
non-empty `ts`, and a returned channel matching the DELIVERY_MODE destination. Any of those
missing means the send is NOT verified: report it, do not re-send blindly.

**Channel membership.** Because the connector posts as you, YOU must be a member of every
destination channel. There is no bot to invite.

- `#wfs-ttw-sales-reps-dm-external` (C09ADJS1V6H), reps channel, includes external members
- `#wfs-ttw-sales-mgmt-client` (C098J2VG41E), client-facing
- `#payments` (C07PVHXGD38), read only

**Errors.** Not authorized means the Slack connector needs reconnecting under your own account.
`channel_not_found` or `not_in_channel` means you are not a member of that conversation: report
it, never improvise a different destination.

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
