---
name: eow-report-reminder
routine_name: "EOW Report Reminder (Fri 4pm MT)"
routine_id: trig_012B8Zr2N96x1NUtWFxy7XM7
cron_utc: "0 22 * * 5"
enabled_at_handoff: True
model: claude-opus-5
created: 2026-08-21
connectors_required: Slack
---

SCHEDULED TASK: End of Week Report reminder for David.

CONFIG
DIRECTOR_SLACK_ID: U0BUZ6C0C91 (The only destination this task may ever use.)
SLACK ACCESS: the WFS Group workspace bot token on the Slack Web API, reached either through the Slack MCP connector or a direct POST to https://slack.com/api/<method> with header Authorization: Bearer $SLACK_BOT_TOKEN. One sender only: never a personal user token, never a second sender.

This is a reminder only. Do NOT build the End of Week report. Do NOT invoke the `ttw-eow-report` skill. Do NOT pull KPIs, read Slack history, or gather Avoma metrics. The only action this task takes is sending one Slack DM.

This is an unattended run. David is not present. Never ask questions, never wait for confirmation.

WHY: the `ttw-eow-report` skill is manual by design because every figure in the report must come from the Closer Sales Dashboard screenshot that David supplies. A scheduled run cannot obtain that screenshot, so this task exists purely to prompt him at the right moment.

STEP 1 - compute the window
The report week runs Sunday through Friday in America/Denver. This task fires Friday at 4:00 PM Mountain. The window is the Sunday of the current week through today (Friday). Compute both dates with bash and format them as "Month Day to Month Day", for example "August 16 to August 21". Do not hyphenate the range, use the word "to".

STEP 2 - send the DM
Send exactly one Slack DM with `chat.postMessage`:
- `channel` = DIRECTOR_SLACK_ID
- `text` = the message below
- no `thread_ts`, and nothing scheduled, so it goes out immediately

One sender only, the bot token above. Never post to a channel. The only destination ever allowed is DIRECTOR_SLACK_ID.

Message content, plain text, no markdown asterisks, no dash characters used as punctuation:

:memo: Time to run the End of Week report for <window>.

Send me the Closer Sales Dashboard screenshot (Sales Rep Table View) and any talking points you want worked in, a rep conversation, a leadership ask, a win, a policy change, and I will build the draft.

Reply in this session or start a new one and say "run the EOW report".

Substitute the real computed window. Keep it to those three short lines.

STEP 3 - confirm and retry
Confirm the send from the `chat.postMessage` RETURN VALUE and nothing else: `ok` = true, a non-empty `ts`, and a returned `channel` that resolves to DIRECTOR_SLACK_ID. Never confirm with a follow-up read.

If the send fails outright, retry `chat.postMessage` ONCE after a short pause. There is no second sender, so if the retry also fails, send nothing else and report the failure in STEP 4.

STEP 4 - final summary
Finish with two lines: the window you computed, and whether the DM was confirmed sent (ok true plus a ts) or failed after the one retry. Nothing else.
