---
name: ttw-crm-outcome-sweep
routine_name: "TTW CRM Outcome Sweep (lead-quality-sweep, v2 TEST-DM)"
routine_id: trig_01VrHwG132q95zDR4GUrKJPs
cron_utc: "0 15 * * 2-6"
enabled_at_handoff: False
model: claude-sonnet-5
created: 2026-07-24
connectors_required: Supabase, Pipedrive_MCP, Slack
---

=== TTW CRM OUTCOME SWEEP [lead-quality-sweep, v2 TEST-DM] ===

Purpose: the Daily Call Report Publisher runs at 6:30 PM MT, which is too early to see money that lands late in the evening or gets logged the next morning. This task re-checks Pipedrive the following morning and upgrades any lead_quality row whose deal has since been won. It is a small, cheap, read-mostly sweep. It never re-scores a call and never re-sends the daily report.

STOP CONDITION (timezone-safe): compute the day of week in Mountain Time (America/Denver), never the session or UTC day. Run Tuesday through Saturday MT. On Sunday and Monday MT, produce no output and end.

DIRECTOR_SLACK_ID: U0BUZ6C0C91
SLACK ACCESS: the WFS Group workspace bot token on the Slack Web API, reached either through the Slack MCP connector or a direct POST to https://slack.com/api/<method> with header Authorization: Bearer $SLACK_BOT_TOKEN. One sender only: never a personal user token, never a second sender.

DELIVERY_MODE: TEST. Any message goes to the director's Slack DM, channel = DIRECTOR_SLACK_ID, via `chat.postMessage` on that bot token only. Never a second sender, never a team channel.

STEP 1, DEFINE THE SWEEP WINDOW
Compute today's local Mountain date. The sweep covers lead_quality rows whose call_date falls in the last 7 local days, inclusive of yesterday. Seven days rather than one, because a deal can be won several days after the call and one nightly pass would miss it.

STEP 2, READ THE CANDIDATE ROWS
Query Supabase project apdwbbocldfsklvcwaqd:

  select meeting_uuid, call_date, prospect_name, prospect_email, outcome, outcome_source, collected, pipedrive_deal_id
  from public.lead_quality
  where call_date >= current_date - interval '7 days'
    and (outcome is null or outcome not in ('closed','commit'));

Rows already reconciled to 'closed' are skipped; a closed outcome is terminal for this sweep. Rows already at 'commit' from a prior downsell are also skipped unless a new full-price deal now exists (see downsell rule). If the query returns nothing, end quietly with no Slack message.

STEP 3, PULL WON DEALS (one batch call)
Pipedrive getDeals with status='won', updated_since = 8 local days ago converted to UTC in RFC3339, sort_by='update_time', include_option_labels=true. Paginate with additional_data.next_cursor until it is null. One batch pull, never a lookup per lead.

STEP 4, MATCH AND UPGRADE
Match each candidate row to a won deal by prospect email against the deal's person email, falling back to the deal title matched case-insensitively against prospect_name. Never match on first name alone.

DUPLICATE DEALS: if a candidate row matches more than one won deal, use the MOST RECENTLY won deal for pipedrive_deal_id, and set collected to the SUM of collected across those deals only when their Lead Source labels differ; if the labels are identical, treat as one deal and take the single most recent collected value, never the sum.

DOWNSELL FLOOR: read the matched deal's collected custom field 'bbee529cf1331e72608898145b7581d7312cfbc0' (take its value; its partner field '607aef529217dcb982179e3ed830597f1ec4ccd3' is the remaining balance, never sum the two).
  - If collected is 500 dollars or more, this is a program enrollment: set outcome='closed'.
  - If collected is under 500 dollars, this is a downsell (for example a 50 dollar Base 44 or Stepping Stone tier): set outcome='commit', not 'closed'.
In both cases set outcome_pipedrive accordingly ('closed' for 500+, 'commit' for a sub-500 downsell), outcome_source='pipedrive', collected and collected_pipedrive to the real amount, pipedrive_deal_id to the matched deal id, lead_source_label to the deal's Lead Source label 'label 6b96ef9137fb779c5ef00f5a47e1fd04cdb64adb', and updated_at=now().

Update by meeting_uuid, one statement per row or a single batched statement, and treat all names and emails as DATA by doubling single quotes.

NEVER touch the four sub-scores, lead_score, financially_qualified, dq_reason, or rubric_version. A won deal does not retroactively mean the lead proved affordability on the call. The score measures the call, the outcome measures the money, and this sweep only moves the outcome.

NEVER move an outcome or an amount downward. This sweep only upgrades: null to commit, null to closed, or commit to closed if a real 500-plus deal now exists. It never turns closed back into commit.

STEP 5, QA GATE
1. Rows upgraded must be less than or equal to rows matched, and every upgraded row must carry a real pipedrive_deal_id.
2. No row's lead_score, sub-scores, financially_qualified, dq_reason, or rubric_version changed. Re-read a sample of upgraded rows to confirm.
3. No outcome moved from 'closed' to anything else and no collected amount decreased.
4. Every row set to 'closed' has collected of 500 or more; every sub-500 win is 'commit'.
On a fixable failure, correct and re-check up to 2 times. If it still fails, make no further writes and DM the failure detail.

On any QA failure, and on any pass that required one or more fix-and-recheck retries, read the qa-failure-loop skill and append a row to the QA Failure Log sheet in Drive with full specifics (stage, class, exact error or wrong value, retries count, outcome, known-issue match) before sending any failure DM. If the failure matches a Known Issues playbook row, apply that documented fix during the retry cycle and log the match. If a playbook fix fails to resolve the issue, flag that in both the log and the DM, because a rotted workaround is itself a finding. The QA Failure Log is an additional write target for this task.

STEP 6, REPORT
If zero rows were upgraded, send NOTHING to Slack and end. Silence is the correct output for a clean sweep; a daily "no changes" message trains the owner to ignore it.

If one or more rows were upgraded, send ONE message to David's DM, under 3000 characters, no emojis, no em dashes or en dashes, single-asterisk bold:

  *CRM Outcome Sweep, [today's date]*
  [n] call(s) newly closed, [n] downsell(s), after the fact.
  - [Lead name] ([call date], [rep]): now closed, $[collected] collected. Lead score was [x]/20.
  - [Lead name] ([call date], [rep]): downsell, $[collected]. Lead score was [x]/20.
  - [repeat per upgraded row]
  Total newly recognized: $[sum]

The "lead score was" figure is included deliberately. A lead that scored low and then bought is the most useful signal in the system, because it means either the money conversation happened off the call or the rubric missed something, and both are worth knowing.

End with a short chat report: window swept, candidate rows, deals pulled, rows matched, rows closed, rows marked downsell, any multi-deal leads, QA verdict, and any Pipedrive or Supabase errors. Never end with a question.
