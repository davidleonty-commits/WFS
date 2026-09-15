---
name: weekly-clip-finder-cloud
routine_name: "Weekly Clip Finder (cloud)"
routine_id: trig_013HTsU8JosZcxcwtbbomuc7
cron_utc: "15 14 * * 1"
enabled_at_handoff: False
model: claude-opus-4-8
created: 2026-07-13
connectors_required: Avoma_MCP, Slack, Google_Drive
---

SCHEDULED TASK: Weekly Clip Finder
PURPOSE: Source this week's world-class sales coaching clips from TikTok Wiz consultation calls and deliver the clip list to Cayden's Slack DM.

CONFIG
DIRECTOR_SLACK_ID: <fill in: your own Slack member ID, for example U01234567. The only delivery destination for this task.>
SLACK ACCESS: the WFS Group workspace bot token on the Slack Web API, reached either through the Slack MCP connector or a direct POST to https://slack.com/api/<method> with header Authorization: Bearer $SLACK_BOT_TOKEN. One sender only: never a personal user token, never a second sender.
Runs as a remote cloud task, fully connector-based, no browser, autonomous — never ask the user questions; the user is not present.

Invoke the `anthropic-skills:ttw-avoma-clip-finder` skill and follow its full workflow: score how reps executed the Decision Leadership Objection Matrix across the week's calls, identify the best teachable moments (Great Demo / objection handling / Missed Opportunity), apply the strict clip eligibility gate and verbatim clip-anchor rule, and hand Caydo exact clip-in and clip-out anchors so each snippet is one click to create.

Avoma is the source for all call data (the skill pulls via the Avoma MCP: `list_meetings` over the window, `get_meeting_transcript` per candidate, `get_meeting_notes` when a transcript is unavailable). Cover the past week of calls (the most recent 7 days); all dates/windows in Mountain Time (America/Denver).

RANKING: there is no pre-ranked candidate list any more. List the week's meetings, then apply the skill's own candidate rules to rank them (a real recorded consultation over 15 minutes, a TikTok Wiz consultation title, a usable speaker transcript, closes weighed against no-closes). The ranking rules live in the skill and are unchanged.

EFFICIENCY: rank the week's meetings first and pull full transcripts only for candidates; cap transcript reads at 25 calls for the week, most recent first, and note in the delivery if the cap was hit.

DATA SOURCE FALLBACK: the Avoma MCP is PRIMARY. If a native Avoma tool fails after 2 retries (connection error, 4xx or 5xx, auth error, or it returns no calls for the week), do NOT abandon the run: call the Avoma REST API directly for the same window (`GET https://api.avoma.com/v1/meetings/` with `{from_date, to_date, page, page_size}`, then `GET /v1/transcriptions/?meeting_uuid=`, header `Authorization: Bearer $AVOMA_API_KEY`) and apply the skill's same scoring rubric, eligibility gate, and verbatim clip-anchor rules to those transcripts. Note in the delivered DM which path was used (Avoma MCP or the REST fallback).

QA FAILURE LOGGING
On any QA failure, and on any pass that required one or more fix-and-recheck retries, read the qa-failure-loop skill and append a row to the QA Failure Log sheet in Drive with full specifics (stage, class, exact error or wrong value, retries count, outcome, known-issue match) before sending any failure DM. If the failure matches a Known Issues playbook row, apply that documented fix during the retry cycle and log the match. If a playbook fix fails to resolve the issue, flag that in both the log and the DM, because a rotted workaround is itself a finding. The QA Failure Log is an additional write target for this task.

DELIVERY: Deliver the finished clip list to the director's Slack DM with `chat.postMessage` on the bot token above, channel = DIRECTOR_SLACK_ID, sent immediately. Send exactly once; on delivery failure retry `chat.postMessage` once, then stop, since there is no second sender. Delivery is proven by the return value only: ok = true, a non-empty ts, and a returned channel matching DIRECTOR_SLACK_ID.

SCHEDULE: Runs Mondays per the schedule itself — no day-of-week gate needed in the prompt.

Repeats: Every Monday at ~8:15 AM Mountain Time.

TEST MARKER (cloud-migration testing only): begin the delivered DM with the emoji 🙌🏽 and a space, before all other content, so the owner can tell this CLOUD task run apart from the local task. Remove this rule once the local copy of this task is disabled.
