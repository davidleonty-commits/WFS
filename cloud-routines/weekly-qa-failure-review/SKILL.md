---
name: weekly-qa-failure-review
routine_name: "Weekly QA Failure Review"
routine_id: trig_016t8b38bgykAB1mvYoae1Ss
cron_utc: "0 21 * * 5"
enabled_at_handoff: False
model: claude-opus-4-8
created: 2026-07-24
connectors_required: Slack, Google_Drive
---

# SCHEDULED TASK: Weekly QA Failure Review

Runs as a Claude Cowork scheduled task. Reads the QA Failure Log, ranks what is breaking most, runs a fable-review against the worst offender using the logged failures as evidence, and delivers a patch proposal to the owner's DM.

Schedule: Fridays, 3:00 PM America/Denver.

=====================================================
CONFIG (OPERATOR NOTE: edit only the values in this block; never edit the rules below.)
=====================================================
DELIVERY_MODE: TEST
  (TEST or LIVE. TEST sends only to TEST_TARGET, the owner's DM. Keep TEST until officially out of test mode.)
DIRECTOR_SLACK_ID: <fill in: your own Slack member ID, for example U01234567>
TEST_TARGET: DIRECTOR_SLACK_ID
SLACK ACCESS: the WFS Group workspace bot token on the Slack Web API, reached either through the Slack MCP connector or a direct POST to https://slack.com/api/<method> with header Authorization: Bearer $SLACK_BOT_TOKEN. One sender only: never a personal user token, never a second sender.
LIVE_TARGET: @cayden
  (This task has no channel destination by design. Its output is owner-only in both modes.)
LOOKBACK_DAYS: 14
QA_FAILURE_LOG: Google Sheet named "QA Failure Log" in the owner's Drive
  (Includes a "Known Issues" tab. If the sheet does not exist, create it per the qa-failure-loop skill and report the creation.)
WFS_BROWSER_DEVICE_ID: 2fac653e-7302-41bb-839a-a7b4b18cab1b
REQUIRED_GOOGLE_ACCOUNT: cayden.johnson@thewfsgroup.com

=====================================================
STARTUP
=====================================================
Try to attach to the WFS browser (WFS_BROWSER_DEVICE_ID) and verify it is signed into REQUIRED_GOOGLE_ACCOUNT on the first Google surface opened. If that deviceId is not connected or is signed into the wrong account, search all currently connected browsers and attach to the first one found signed into REQUIRED_GOOGLE_ACCOUNT, noting the substitution in the summary. Only if no connected browser is signed into that account should the task stop and report. Never proceed with an unverified account.

This task never needs and never asks for browser clipboard permission. If a clipboard permission prompt appears, proceed without it (type instead of paste) and never pause or ask the owner.

=====================================================
AUTONOMY
=====================================================
Runs fully autonomous with no approval or confirmation prompts. It is pre-authorized to complete every step and deliver without asking. Safety comes from DELIVERY_MODE and from the write restrictions below, not from an approval gate. A "stop and report" applies only to the specific error conditions named in this prompt.

=====================================================
WORK
=====================================================
Read the qa-failure-loop skill and follow its weekly failure review exactly. In order:

1. Open the QA Failure Log and read all rows from the trailing LOOKBACK_DAYS. Read the Known Issues tab in full.

2. Aggregate the failures two ways: by task_or_skill, and by class (source_gap, source_shape, derivation, format_drift, tool_fail, rule_breach).

3. Rank offenders by frequency times severity. Any rule_breach, and any row whose outcome was "delivered wrong," outranks any volume of retried-and-recovered blips. Break ties toward the task that runs most often.

4. Check the patched column against this window. If a failure type that was previously patched has fired again, it becomes the top offender automatically regardless of raw counts, and the report says the prior patch did not hold.

5. Run fable-review against the top offender, passing its failure rows as the evidence input. Target the actual failure mechanism, not the task in general. If four of five failures are source_shape on one Avoma endpoint, the patch is pagination hardening, not a rewrite.

6. Produce the patch, matched to the offender type:
   - Scheduled task: the exact revised task prompt, complete and paste-ready, plus the create-verify-delete update plan (create or edit the replacement first, verify it exists and is scheduled correctly, only then remove the old one).
   - Skill: an updated .skill package delivered as a file.
   - Recurring issue with no single owner task: the new or corrected Known Issues row, plus the list of tasks that embed the stale workaround and need the fix propagated.

7. Update the Known Issues tab with anything new this window taught, and fill the patched column on the rows this run's patch addresses.

ZERO-FAILURE WEEKS: If the log has no rows in the window, deliver a one-line report stating the clean week and the current streak count. If the streak reaches three consecutive weeks while daily tasks are known to be running, do not celebrate it. Spot-check whether the logging step is still present in the QA gates of the daily tasks and report the finding, because silence can mean health or a dead sensor and the review has to know which.

=====================================================
WRITE TARGETS
=====================================================
The QA Failure Log, including its Known Issues tab, is the ONLY write target for this task. Never edit the salesboard or any other resource document. Never modify, create, or delete any scheduled task during this run; patches are delivered as proposals for the owner to apply.

=====================================================
QA GATE
=====================================================
Before delivering, run an independent pass that:
- Re-derives the offender ranking and every count directly from the log rows, not from working notes.
- Confirms the output matches the qa-failure-loop delivery format exactly.
- Confirms the task rules were followed: write restrictions respected, no scheduled task touched, correct delivery target, one send only.

On a fixable failure, correct and re-check, retrying up to 3 times. If it still fails, or the failure is a source or data problem, do NOT deliver; send the specific QA failures to TEST_TARGET instead.

This task logs its own QA failures and retries to the QA Failure Log, same as any other task.

=====================================================
DELIVERY
=====================================================
Send with `chat.postMessage` on the bot token above to TEST_TARGET while DELIVERY_MODE is TEST. One sender, one send only. Delivery is proven by the return value: ok = true, a non-empty ts, and a returned channel matching the destination.

Message contents:
- Two-line summary: worst offender, root cause, patch shipped or proposed.
- The patch itself (or the file, for skill patches).
- Week totals: failures by class, recoveries after retry, new Known Issues rows added, and whether any previously patched failure type recurred.

No em dashes anywhere. No emojis directly after rep names.
