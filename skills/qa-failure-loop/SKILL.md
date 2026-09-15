---
name: qa-failure-loop
description: Self-healing infrastructure loop for Caydo's Cowork scheduled tasks and skill library. Every QA gate failure in any scheduled task gets logged to a durable QA Failure Log instead of dying in a DM, failures get classified against a known-issue playbook (Avoma pagination, format drift, source data gaps, tool errors), and a weekly pass runs fable-review against the worst-offending task or skill using the failure log as input, producing a concrete patch. Use whenever a Cowork task hits its QA gate and fails, whenever a scheduled task misdelivers or DMs a failure, whenever Caydo says "log this failure", "QA log", "what keeps breaking", "which task fails most", "run the failure review", "patch the worst offender", or "why did the report not send", and on any weekly infrastructure review. Also use when building or updating any Cowork task, so its QA gate includes the logging step. Always log before or alongside the failure DM, because a failure that is only a DM teaches the system nothing.
---

# QA Failure Loop

Every Cowork task already has a QA gate. Today a failure DMs Caydo and dies; next month the same Avoma pagination bug burns another hour. This loop gives failures a memory: log every one, classify it, and once a week aim fable-review at whichever task or skill is failing most, with the log as evidence. The infrastructure starts fixing itself instead of Caydo re-debugging the same issue.

## Non-negotiables

1. **Never use em dashes.** Anywhere.
2. **Log first, then DM.** The failure DM to Caydo still happens per his task rules; the log entry is written before or alongside it, never skipped because the DM "already covered it."
3. **The log is append-only fact.** Entries record what happened with specifics (the exact error, the exact wrong number, the exact format drift), never a vague "QA failed."
4. **Patches follow the update rule.** Any task update produced by this loop follows create-then-verify-then-delete: build the new task, verify it exists and is scheduled correctly, only then remove the old one. Prefer editing in place when tooling supports it. Skill patches get delivered as updated .skill packages for Caydo to install; this loop never silently swaps a skill.
5. **Delivery rules apply.** Slack output goes out with `chat.postMessage` on the WFS Group workspace bot token, one sender, to the director's DM while in test mode. The log is this skill's only write target.

## The log

A Google Sheet named **QA Failure Log** in Caydo's Drive. On first run, search Drive for it; if missing, create it and report the new file. Columns:

| Column | Content |
|---|---|
| date | when the failure occurred |
| task_or_skill | exact task or skill name |
| stage | where it failed: pull, derive, format, QA re-derive, delivery |
| class | one of the failure classes below |
| specifics | the exact error, wrong value, or drift, verbatim where possible |
| retries | how many fix-and-recheck cycles ran (0 to 3) |
| outcome | delivered after fix / not delivered, DMed failure / delivered wrong (worst case) |
| known_issue | matching playbook entry if any, else "new" |
| patched | blank until a patch ships; then the date and one line on the fix |

## Failure classes and the known-issue playbook

Classify every entry into one of these, so patterns aggregate instead of scattering:

- **source_gap:** the source system lacked or lagged the data (Avoma call not yet processed, Pipedrive field empty, sheet row missing).
- **source_shape:** the source changed shape (renamed column, new field format, API pagination behavior). Known issues here already include Avoma day-by-day pagination limits, retry-required endpoints, and the absent attendee_emails filter; new shape issues get added to this playbook as they appear.
- **derivation:** the task computed a figure wrong (date boundary, refund handling, definition drift from ttw-dashboard-metrics).
- **format_drift:** output stopped matching the template exactly (emoji placement, section order, an em dash sneaking in).
- **tool_fail:** a connector or tool errored or timed out.
- **rule_breach:** the task violated a standing rule (wrong delivery channel, touched a read-only doc, asked for clipboard). These are severity-one regardless of frequency.

The playbook lives as a **Known Issues** tab on the same sheet: one row per recurring issue, its class, the reliable workaround, and which tasks embed the fix. When a new failure matches a playbook row, the fix is already written; apply it and log the match. When a playbook fix fails, that is a finding: the workaround has rotted, flag it loudly.

## The loop

### Write side: inside every QA gate

Amend the QA gate protocol of every Cowork task (as tasks get built or updated) with one step: on any QA failure, before or alongside the failure DM, append a row to the QA Failure Log with full specifics. Fixable failures that pass after retries also get logged, with retries count and outcome "delivered after fix." Near-misses are the cheapest signal there is; a task that needs 2 retries every day is a task about to start failing outright.

### Read side: the weekly failure review

Once a week (scheduled or on "run the failure review"):

1. **Read the log** for the trailing 14 days. Aggregate by task_or_skill and by class.
2. **Rank the offenders.** Frequency times severity: any rule_breach or delivered-wrong outcome outranks a pile of retried-and-recovered blips.
3. **Run fable-review against the top offender**, with its failure rows as the evidence input. The review targets the actual failure mechanism, not the task in general: if 4 of 5 failures are source_shape on the same Avoma endpoint, the patch is pagination hardening, not a rewrite.
4. **Produce the patch.** For a scheduled task: the exact revised task prompt, plus the create-verify-delete update plan. For a skill: an updated .skill package. For a playbook-level issue: the new or corrected Known Issues row, plus the list of tasks that embed the stale workaround.
5. **Deliver to Caydo's DM:** two-line summary (worst offender, root cause, patch shipped or proposed), the patch itself, and the week's totals: failures by class, recoveries, anything new added to the playbook.
6. **Close the loop in the log.** When a patch ships, fill the patched column on the rows it addresses. Next week's review checks whether patched failure types actually stopped. A patch that did not stop its failure type reopens automatically as the top offender.

### Quiet weeks

A week with zero failures gets a one-line DM saying so, plus the streak count. If the log has been empty three straight weeks while tasks are running daily, treat that with suspicion, not celebration: spot-check that the logging step is still wired into the gates. Silence can mean health or a dead sensor, and the review has to know which.

## The honest metric

The number that matters over time: **repeat rate**, the share of failures matching an already-known issue. High repeat rate means the loop is not closing (known problems keep firing). The goal state is a log dominated by genuinely new failure modes, each occurring once, each ending with a playbook row and a patch. That is what self-healing looks like on paper.
