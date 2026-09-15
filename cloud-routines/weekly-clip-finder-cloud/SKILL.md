---
name: weekly-clip-finder-cloud
routine_name: "Weekly Clip Finder (cloud)"
routine_id: trig_013HTsU8JosZcxcwtbbomuc7
cron_utc: "15 14 * * 1"
enabled_at_handoff: False
model: claude-opus-4-8
created: 2026-07-13
connectors_attached: Avoma_MCP, Canva, Claude_Code_Remote, ClickUp, Excalidraw, Google_Calendar, Google_Drive, Lovable, Lovable_WFS_Slack, Pipedrive_MCP, Slack, Supabase
---

SCHEDULED TASK: Weekly Clip Finder
PURPOSE: Source this week's world-class sales coaching clips from TikTok Wiz consultation calls and deliver the clip list to Cayden's Slack DM.
Runs as a remote cloud task, fully connector-based, no browser, autonomous — never ask the user questions; the user is not present.

Invoke the `anthropic-skills:ttw-avoma-clip-finder` skill and follow its full workflow: score how reps executed the Decision Leadership Objection Matrix across the week's calls, identify the best teachable moments (Great Demo / objection handling / Missed Opportunity), apply the strict clip eligibility gate and verbatim clip-anchor rule, and hand Caydo exact clip-in and clip-out anchors so each snippet is one click to create.

Use the Lovable WFS connector as the PRIMARY source for all call data (the skill pulls via calls_find_review_candidates and calls_get_analysis). Cover the past week of calls (the most recent 7 days); all dates/windows in Mountain Time (America/Denver).

EFFICIENCY: The skill lists ranked candidates via calls_find_review_candidates (days_back=7, limit=50, no manual pagination) and pulls full analysis only for candidate calls; cap full-analysis reads at 25 calls for the week, most recent first, and note in the delivery if the cap was hit.

DATA SOURCE FALLBACK: the Lovable WFS connector is PRIMARY. If its call tools (calls_find_review_candidates or calls_get_analysis) fail after 2 retries (connection error, 4xx or 5xx, auth error, or they return no calls for the week), do NOT abandon the run: pull the week's consultation calls directly from the Avoma MCP instead (list_meetings over the last 7 days, get_meeting_transcript for candidates, get_meeting_notes when a transcript is unavailable) and apply the skill's same scoring rubric, eligibility gate, and verbatim clip-anchor rules to those transcripts. Note in the delivered DM which source was used (Lovable primary or Avoma fallback).

QA FAILURE LOGGING
On any QA failure, and on any pass that required one or more fix-and-recheck retries, read the qa-failure-loop skill and append a row to the QA Failure Log sheet in Drive with full specifics (stage, class, exact error or wrong value, retries count, outcome, known-issue match) before sending any failure DM. If the failure matches a Known Issues playbook row, apply that documented fix during the retry cycle and log the match. If a playbook fix fails to resolve the issue, flag that in both the log and the DM, because a rotted workaround is itself a finding. The QA Failure Log is an additional write target for this task.

DELIVERY: Deliver the finished clip list to Cayden's Slack DM via the Lovable WFS Slack connector (slack_schedule_message, channel @cayden.johnson; if that handle errors, use Slack user ID U092C85GA4D), jitter_minutes 0. Send exactly once; on delivery failure retry once, then try the fallback user ID. Never use the native Slack connector.

SCHEDULE: Runs Mondays per the schedule itself — no day-of-week gate needed in the prompt.

Repeats: Every Monday at ~8:15 AM Mountain Time.

TEST MARKER (cloud-migration testing only): begin the delivered DM with the emoji 🙌🏽 and a space, before all other content, so the owner can tell this CLOUD task run apart from the local task. Remove this rule once the local copy of this task is disabled.
