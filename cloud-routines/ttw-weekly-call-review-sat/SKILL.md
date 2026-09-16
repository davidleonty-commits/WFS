---
name: ttw-weekly-call-review-sat
routine_name: "TikTok Wiz Weekly Call Review (Sat 4pm MT)"
routine_id: trig_014zmBLB8ju9wE6FFBuG1VfU
cron_utc: "0 22 * * 6"
enabled_at_handoff: True
model: claude-opus-5
created: 2026-08-19
connectors_required: Callix, Slack, Google_Drive
---

Run the weekly TikTok Wiz sales call review report.

CONFIG
DIRECTOR_SLACK_ID: U0BUZ6C0C91 (The completion DM goes here and nowhere else.)
SLACK ACCESS: the claude.ai Slack connector, which posts as YOU (the connected user), never as a bot. One sender only: never a second sender.

Invoke the `ttw-weekly-call-review` skill and follow it end to end. This is an unattended scheduled run: do not stop to ask clarifying questions or wait for confirmation at the skill's normal checkpoints. Make the reasonable call, state the assumption in your final summary, and keep going.

Reporting window
- This fires Saturday at 4:00 PM Mountain Time. The window is Monday 00:00 of the current week through the moment of this run (a partial week ending Saturday afternoon). Use `scripts/week_window.py` in the skill to compute it. Do not extend into Sunday and do not roll back to the prior full week.
- Timezone for all call timestamps is America/Denver.

Standing constraints (these are non-negotiable and carry over from prior runs)
- Exclude David Leonty's own calls entirely. He is the Sales Director, not a rep under review. Filter them out before any counts, averages, or bucket percentages.
- Accuracy over speed. Nothing ships on a single grading pass. Single-pass grading on this report has been wrong roughly 30% of the time. Run the full multi-agent review workflow in `references/review-workflow.md`: blind independent reviewers, neutral adjudication, adversarial challenge, then neutral adjudication of the knockdowns. Then run `scripts/qa_gates.py` and do not deliver until all ten gates pass.
- Verify transcript completeness before grading any call. Many cached transcripts truncate at Callix chunk 1, before the pricing segment. Follow `references/transcript-integrity.md`: check the chars-per-minute heuristic, paginate on `next_cursor` until `has_more` is false, and never write transcripts to a shared scratch path since parallel agents overwrite each other and silently grade the wrong call.
- Bucket grading follows `references/bucket-definitions.md` exactly. RED requires an affirmative financial reference in the lead's own words. An unrun application is not evidence of inability. GREY means funding, credit, affordability, and income were never established at all. Watch the Michelle Wilbur failure mode: a constraint on credit access is not the same as a lack of money.

Data sources
- Callix is the source for all call data. List the window with `mcp__Callix__list_calls`, then pull each call with `mcp__Callix__get_call` (plus `get_deal_analysis` for context). If a native Callix tool is 403-blocked or unreachable, call the Callix REST API directly with the same date window: `GET $CALLIX_API_BASE/calls` with `{from_date, to_date, page, page_size}` and `GET /v1/transcriptions/` with `from_date` and `to_date`, header `Authorization: Bearer $CALLIX_API_KEY` (the `meeting` filter is silently ignored on transcriptions, so page through and match `call_id` manually).
- There is no pre-scored call object any more: the old connector returned a scorecard alongside the transcript, and Callix does not. Grade every call from the transcript itself using the skill's own rubric and `references/bucket-definitions.md`. The grading rules are unchanged, only who runs them is.

Deliverables
1. The two-tab workbook (Data + Report) built per `references/report-spec.md`, with full-row bucket color coding, the Bucket Mix by Rep block showing RED % (not GREY %), and the FDQ opportunity-cost model at $6,400 net per deal. Recalculate formulas before shipping.
2. Send the workbook to David with SendUserFile. Also upload the Report tab to Google Drive as a Sheet if it fits under the connector's size ceiling; if the full data tab is too large, upload the Report tab only and say so.
3. A DRAFT Slack message summarizing the week for the management team. Write it as plain text with no markdown or asterisks, because Slack's composer does not render pasted markdown. Lead with the FDQ opportunity cost framing, keep it short, and include the report link.

DO NOT SEND THE MANAGEMENT-TEAM SLACK MESSAGE. David sends that one himself. Draft it only and put it in your final response as plain text he can copy.

Also: keep any compliance findings out of the Slack draft. Report those separately in your response to David.

Final step, required: DM David on Slack when the run is complete
- After the report is finished and delivered, send the director a Slack DM with `slack_send_message`, `channel` = DIRECTOR_SLACK_ID, nothing scheduled so it goes out immediately.
- This DM is separate from the management-team draft above and IS meant to be sent. It is a completion notice to David only. Do not post it to a channel.
- Keep it to a few lines: the report is ready, the date window covered, call count and gradeable count, close count and close rate, average rep score, FDQ percentage, the estimated FDQ opportunity cost, the Google Sheet link, and a note that the management-team Slack draft is waiting in the session for him to review and send. Flag any QA gate failure or compliance finding in one line so he knows to open the session.
- Send this DM even if the run had problems. If the report could not be completed, DM him saying what halted it and how far it got. If `slack_send_message` fails outright, retry it ONCE after a short pause; there is no second sender.
- Confirm the DM from the return value only (ok = true, a non-empty ts, and a returned channel matching DIRECTOR_SLACK_ID) and say so in your final summary.

Finish with a short summary: call count, gradeable count, close count and rate, average rep score, bucket counts with percentages, FDQ percentage, whether the completion DM went out, and anything that failed a QA gate or needed a judgment call.


CALLIX REST PATHS ARE UNVERIFIED. `$CALLIX_API_BASE` and every path under it above are placeholders: Callix's MCP tool names are documented (REPLY-2-CALLIX.md section 3) but its REST base URL, paths, query parameter names and response field names are NOT, and this environment cannot reach `callix.io` to check (the network policy answers 403). Use the Callix MCP tools as the primary and only path. If they are unavailable, STOP and report that — do NOT call a guessed URL. A guessed path does not fail loudly; it 404s or returns a differently-shaped body, and the report is then silently wrong. Fill these in only after a live call confirms them, then delete this paragraph.
