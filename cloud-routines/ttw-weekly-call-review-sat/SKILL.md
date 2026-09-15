---
name: ttw-weekly-call-review-sat
routine_name: "TikTok Wiz Weekly Call Review (Sat 4pm MT)"
routine_id: trig_014zmBLB8ju9wE6FFBuG1VfU
cron_utc: "0 22 * * 6"
enabled_at_handoff: True
model: claude-opus-5
created: 2026-08-19
connectors_attached: Alpha_Vantage_MCP_Server, Asana, Avoma_MCP, Canva, Claude_Code_Remote, ClickUp, Excalidraw, Google_Calendar, Google_Drive, HyperFrames_by_HeyGen, Just_Call, Lovable, Lovable_WFS_Slack, Pipedrive_MCP, RobinHood, Slack, Supabase
---

Run the weekly TikTok Wiz sales call review report.

Invoke the `ttw-weekly-call-review` skill and follow it end to end. This is an unattended scheduled run: do not stop to ask clarifying questions or wait for confirmation at the skill's normal checkpoints. Make the reasonable call, state the assumption in your final summary, and keep going.

Reporting window
- This fires Saturday at 4:00 PM Mountain Time. The window is Monday 00:00 of the current week through the moment of this run (a partial week ending Saturday afternoon). Use `scripts/week_window.py` in the skill to compute it. Do not extend into Sunday and do not roll back to the prior full week.
- Timezone for all call timestamps is America/Denver.

Standing constraints (these are non-negotiable and carry over from prior runs)
- Exclude Cayden Johnson's own calls entirely. He is the Sales Director, not a rep under review. Filter them out before any counts, averages, or bucket percentages.
- Accuracy over speed. Nothing ships on a single grading pass. Single-pass grading on this report has been wrong roughly 30% of the time. Run the full multi-agent review workflow in `references/review-workflow.md`: blind independent reviewers, neutral adjudication, adversarial challenge, then neutral adjudication of the knockdowns. Then run `scripts/qa_gates.py` and do not deliver until all ten gates pass.
- Verify transcript completeness before grading any call. Many cached transcripts truncate at Avoma chunk 1, before the pricing segment. Follow `references/transcript-integrity.md`: check the chars-per-minute heuristic, paginate on `next_cursor` until `has_more` is false, and never write transcripts to a shared scratch path since parallel agents overwrite each other and silently grade the wrong call.
- Bucket grading follows `references/bucket-definitions.md` exactly. RED requires an affirmative financial reference in the lead's own words. An unrun application is not evidence of inability. GREY means funding, credit, affordability, and income were never established at all. Watch the Michelle Wilbur failure mode: a constraint on credit access is not the same as a lack of money.

Data sources
- Use the WFS connector (`mcp__Lovable_WFS_Slack__*`) as the primary source: `calls_list` for the window, `calls_get_analysis` per call. When `transcript` comes back null, fall back to `mcp__Avoma_MCP__get_meeting_transcript` with the `avoma_meeting_id`, and if that is 403-blocked use the WFS `avoma_api` passthrough on `/v1/transcriptions/` (the `meeting` filter is silently ignored there, so page through and match `meeting_uuid` manually).

Deliverables
1. The two-tab workbook (Data + Report) built per `references/report-spec.md`, with full-row bucket color coding, the Bucket Mix by Rep block showing RED % (not GREY %), and the FDQ opportunity-cost model at $6,400 net per deal. Recalculate formulas before shipping.
2. Send the workbook to Cayden with SendUserFile. Also upload the Report tab to Google Drive as a Sheet if it fits under the connector's size ceiling; if the full data tab is too large, upload the Report tab only and say so.
3. A DRAFT Slack message summarizing the week for the management team. Write it as plain text with no markdown or asterisks, because Slack's composer does not render pasted markdown. Lead with the FDQ opportunity cost framing, keep it short, and include the report link.

DO NOT SEND THE MANAGEMENT-TEAM SLACK MESSAGE. Cayden sends that one himself. Draft it only and put it in your final response as plain text he can copy.

Also: keep any compliance findings out of the Slack draft. Report those separately in your response to Cayden.

Final step, required: DM Cayden on Slack when the run is complete
- After the report is finished and delivered, send Cayden a Slack DM using `mcp__Lovable_WFS_Slack__slack_schedule_message` with `channel` set to "@cayden" (his Slack user ID is U092C85GA4D if the handle does not resolve), `jitter_minutes` set to 0, and `send_at_mt` omitted so it goes out immediately.
- This DM is separate from the management-team draft above and IS meant to be sent. It is a completion notice to Cayden only. Do not post it to a channel.
- Keep it to a few lines: the report is ready, the date window covered, call count and gradeable count, close count and close rate, average rep score, FDQ percentage, the estimated FDQ opportunity cost, the Google Sheet link, and a note that the management-team Slack draft is waiting in the session for him to review and send. Flag any QA gate failure or compliance finding in one line so he knows to open the session.
- Send this DM even if the run had problems. If the report could not be completed, DM him saying what halted it and how far it got. If `slack_schedule_message` itself fails, fall back to `mcp__Lovable_WFS_Slack__slack_send_sos` with target U092C85GA4D.
- Confirm the DM was queued (check the returned queue row id, or `slack_list_pending`) and say so in your final summary.

Finish with a short summary: call count, gradeable count, close count and rate, average rep score, bucket counts with percentages, FDQ percentage, whether the completion DM went out, and anything that failed a QA gate or needed a judgment call.
