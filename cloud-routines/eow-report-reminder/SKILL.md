---
name: eow-report-reminder
routine_name: "EOW Report Reminder (Fri 4pm MT)"
routine_id: trig_012B8Zr2N96x1NUtWFxy7XM7
cron_utc: "0 22 * * 5"
enabled_at_handoff: True
model: claude-opus-5
created: 2026-08-21
connectors_attached: Alpha_Vantage_MCP_Server, Asana, Avoma_MCP, Canva, Claude_Code_Remote, ClickUp, Excalidraw, Google_Calendar, Google_Drive, HyperFrames_by_HeyGen, Just_Call, Lovable, Lovable_WFS_Slack, Pipedrive_MCP, RobinHood, Slack, Supabase, Typeform
---

SCHEDULED TASK: End of Week Report reminder for Cayden.

This is a reminder only. Do NOT build the End of Week report. Do NOT invoke the `ttw-eow-report` skill. Do NOT pull KPIs, read Slack history, or gather Avoma metrics. The only action this task takes is sending one Slack DM.

This is an unattended run. Cayden is not present. Never ask questions, never wait for confirmation.

WHY: the `ttw-eow-report` skill is manual by design because every figure in the report must come from the Closer Sales Dashboard screenshot that Cayden supplies. A scheduled run cannot obtain that screenshot, so this task exists purely to prompt him at the right moment.

STEP 1 - compute the window
The report week runs Sunday through Friday in America/Denver. This task fires Friday at 4:00 PM Mountain. The window is the Sunday of the current week through today (Friday). Compute both dates with bash and format them as "Month Day to Month Day", for example "August 16 to August 21". Do not hyphenate the range, use the word "to".

STEP 2 - send the DM
Send exactly one Slack DM using `mcp__Lovable_WFS_Slack__slack_schedule_message` with:
- `channel` = "U092C85GA4D"
- `jitter_minutes` = 0
- `agent` = "claude-eow-reminder"
- `send_at_mt` omitted so it goes out immediately

Never use `mcp__Slack__slack_send_message` or any other Slack send tool. Never post to a channel. The only destination ever allowed is U092C85GA4D.

Message content, plain text, no markdown asterisks, no dash characters used as punctuation:

:memo: Time to run the End of Week report for <window>.

Send me the Closer Sales Dashboard screenshot (Sales Rep Table View) and any talking points you want worked in, a rep conversation, a leadership ask, a win, a policy change, and I will build the draft.

Reply in this session or start a new one and say "run the EOW report".

Substitute the real computed window. Keep it to those three short lines.

STEP 3 - confirm and fall back
Confirm the send was queued by checking the returned queue row id or `mcp__Lovable_WFS_Slack__slack_list_pending`.

If `slack_schedule_message` fails outright, fall back once to `mcp__Lovable_WFS_Slack__slack_send_sos` with target "U092C85GA4D" and the same text.

STEP 4 - final summary
Finish with two lines: the window you computed, and whether the DM was confirmed queued or fell back to SOS. Nothing else.
