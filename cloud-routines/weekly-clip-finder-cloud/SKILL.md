---
name: weekly-clip-finder-cloud
routine_name: "Weekly Clip Finder (cloud)"
routine_id: trig_013HTsU8JosZcxcwtbbomuc7
cron_utc: "15 14 * * 1"
enabled_at_handoff: False
model: claude-opus-4-8
created: 2026-07-13
connectors_required: Callix, Slack, Google_Drive
---

SCHEDULED TASK: Weekly Clip Finder
PURPOSE: Source this week's world-class sales coaching clips from TikTok Wiz consultation calls and deliver the clip list to David's Slack DM.

CONFIG
DIRECTOR_SLACK_ID: U0BUZ6C0C91 (The only delivery destination for this task.)
SLACK ACCESS: the claude.ai Slack connector, which posts as YOU (the connected user), never as a bot. One sender only: never a second sender.
Runs as a remote cloud task, fully connector-based, no browser, autonomous — never ask the user questions; the user is not present.

Invoke the `anthropic-skills:ttw-callix-clip-finder` skill and follow its full workflow: score how reps executed the Decision Leadership Objection Matrix across the week's calls, identify the best teachable moments (Great Demo / objection handling / Missed Opportunity), apply the strict clip eligibility gate and verbatim clip-anchor rule, and hand David exact clip-in and clip-out anchors so each snippet is one click to create.

Callix is the source for all call data (the skill pulls via the Callix MCP: `list_calls` over the window, `get_call` per candidate, `get_deal_analysis` when a transcript is unavailable). Cover the past week of calls (the most recent 7 days); all dates/windows in Mountain Time (America/Denver).

RANKING: there is no pre-ranked candidate list any more. List the week's meetings, then apply the skill's own candidate rules to rank them (a real recorded consultation over 15 minutes, a TikTok Wiz consultation title, a usable speaker transcript, closes weighed against no-closes). The ranking rules live in the skill and are unchanged.

EFFICIENCY: rank the week's meetings first and pull full transcripts only for candidates; cap transcript reads at 25 calls for the week, most recent first, and note in the delivery if the cap was hit.

DATA SOURCE FALLBACK: the Callix MCP is PRIMARY. If a native Callix tool fails after 2 retries (connection error, 4xx or 5xx, auth error, or it returns no calls for the week), do NOT abandon the run: call the Callix REST API directly for the same window (`GET $CALLIX_API_BASE/calls` with `{from_date, to_date, page, page_size}`, then `GET /v1/transcriptions/?call_id=`, header `Authorization: Bearer $CALLIX_API_KEY`) and apply the skill's same scoring rubric, eligibility gate, and verbatim clip-anchor rules to those transcripts. Note in the delivered DM which path was used (Callix MCP or the REST fallback).

QA FAILURE LOGGING
On any QA failure, and on any pass that required one or more fix-and-recheck retries, read the qa-failure-loop skill and append a row to the QA Failure Log sheet in Drive with full specifics (stage, class, exact error or wrong value, retries count, outcome, known-issue match) before sending any failure DM. If the failure matches a Known Issues playbook row, apply that documented fix during the retry cycle and log the match. If a playbook fix fails to resolve the issue, flag that in both the log and the DM, because a rotted workaround is itself a finding. The QA Failure Log is an additional write target for this task.

DELIVERY: Deliver the finished clip list to the director's Slack DM with `slack_send_message` on the connector above, channel = DIRECTOR_SLACK_ID, sent immediately. Send exactly once; on delivery failure retry `slack_send_message` once, then stop, since there is no second sender. Delivery is proven by the return value only: ok = true, a non-empty ts, and a returned channel matching DIRECTOR_SLACK_ID.

SCHEDULE: Runs Mondays per the schedule itself — no day-of-week gate needed in the prompt.

Repeats: Every Monday at ~8:15 AM Mountain Time.

TEST MARKER (cloud-migration testing only): begin the delivered DM with the emoji 🙌🏽 and a space, before all other content, so the owner can tell this CLOUD task run apart from the local task. Remove this rule once the local copy of this task is disabled.


CALLIX REST PATHS ARE UNVERIFIED. `$CALLIX_API_BASE` and every path under it above are placeholders: Callix's MCP tool names are documented (REPLY-2-CALLIX.md section 3) but its REST base URL, paths, query parameter names and response field names are NOT, and this environment cannot reach `callix.io` to check (the network policy answers 403). Use the Callix MCP tools as the primary and only path. If they are unavailable, STOP and report that — do NOT call a guessed URL. A guessed path does not fail loudly; it 404s or returns a differently-shaped body, and the report is then silently wrong. Fill these in only after a live call confirms them, then delete this paragraph.
