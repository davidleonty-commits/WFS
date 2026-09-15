# Readiness review: what would stop these tasks executing

Audit of all 34 scheduled prompts and 17 skills, 2026-09-15, after the connector swap and the
retarget to David Leonty. Ordered by what it costs you to miss it.

---

## P0. Two things that cause visible damage on day one

### 1. Recreating both copies of a twinned task double-posts, to client-facing channels

Five tasks exist as a local/cloud pair. The README says the local twin was disabled so they
would not double-post, but that state lived in the outgoing director's task list, NOT in these
files. Every file carries the mode it had when it was exported, so recreating a folder pair
as-is gives you two tasks on the same schedule posting the same report.

| Local | mode | Cloud | mode | LIVE target |
|---|---|---|---|---|
| `pipeline-mgmt-accountability-report` | **LIVE** | `pipeline-accountability-report-v2-cloud` | **LIVE** | `#wfs-ttw-sales-reps-dm-external` |
| `ttw-daily-lead-flow-report` | **LIVE** | `ttw-daily-lead-flow-report-cloud` | TEST | `#wfs-ttw-sales-mgmt-client` |
| `eod-show-rate-update` | **LIVE** | `show-rate-report-eod-v12-cloud` | TEST | `#wfs-ttw-sales-mgmt-client` |
| `daily-midday-checkin` | **LIVE** | `daily-midday-checkin-v2-cloud` | TEST | `#wfs-ttw-sales-reps-dm-external` |
| `midday-show-rate-update` | TEST | `show-rate-update-midday-cloud` | **LIVE** | `#wfs-ttw-sales-mgmt-client` |
| `mgmt-call-reports` | (no mode) | `daily-call-report-publisher-v27` | TEST | owner DM |
| `weekly-ttw-clip-finder` | (no mode) | `weekly-clip-finder-cloud` | (no mode) | owner DM |

The accountability report is the sharp one: **both sides are LIVE**, and the target channel
includes external members. Two identical reports land in front of the client.

**Fix:** recreate the CLOUD copy only, per the README's own guidance that the cloud edition is
newer. Keep the local twin in the repo for reference and do not schedule it. Or set every local
twin to TEST before creating anything.

### 2. Both Pipedrive audit tasks write to the live CRM, with no dry run, on your activities

`pipedrive-director-audit-labeling` (local) and `pipedrive-activity-clearing-cloud` both carry
`PROCESS_MODE: EXECUTE`. Both now carry `OWNER_USER_ID: 27299998`, which is yours. Recreate both
and you get two tasks labelling deals and marking activities done in the live CRM, on your own
activities, racing each other on overlapping sets.

This is also where the old safety net is gone: the retired connector's write tools only created
proposals for approval. `PROCESS_MODE` is now the only gate.

**Fix:** set `PROCESS_MODE: DRY_RUN` in both before first run, run once, read the report, and
only then flip ONE of them to EXECUTE.

---

## P1. Blockers: these tasks cannot run until something is supplied

### 3. Call data has no source (25 files)

Avoma is retired and Callix has no read path yet. Detail in `CALLIX-MIGRATION.md`. Effect by
task family:

- **Both show-rate reports cannot produce a number at all.** OnceHub still supplies the
  scheduled denominator, but the live-call numerator came from Avoma. A show rate with no
  numerator is not degraded, it is absent.
- The daily call publisher, the clip finder sweep, review sourcing, and the PIF buyer report
  have no window to read.
- The six SIP engines cannot satisfy their own gate: "validate a MINIMUM of 5 of the rep's
  recorded calls this run by transcript."

### 4. The OnceHub MCP server is the wrong shape, and one of its tools breaks a hard rule

Now that it is registered, it exposes exactly two tools: `get_booking_time_slots` and
`schedule_meeting`. It is a **scheduling** server. There is no list-bookings and no
master-pages, so it cannot serve any report here; the REST API in `DATA-ACCESS.md` remains the
path.

Worse, `schedule_meeting` is a WRITE. Four prompts carry a hard rule reading "All reads are
READ-ONLY; never create, edit, cancel, reschedule, or delete any OnceHub object." Attaching
this connector to those tasks puts a booking-creation tool inside a task whose own rules forbid
it.

**Fix:** do not attach the OnceHub MCP to the reporting tasks. Keep it only if you want
Claude to book meetings interactively, and keep those tasks on the REST key.

It also still needs authorizing. That cannot be done from this session; use `/mcp` in an
interactive Claude Code, or the connector settings on claude.ai.

### 5. Four identity values are still unfilled

| Value | Files | Effect if not set |
|---|---|---|
| Work Google account | 8 | Six SIP engines STOP at the browser account check; the leaderboard refuses the Salesboard read |
| Avoma/Callix account email | 2 | EOW report cannot read your own call-review activity |
| `TEAM_SYNC_ORGANIZER` | 1 | Lead flow report's Team Sync recap finds the wrong meeting or none |
| Browser `deviceId` | 7 | Falls back to scanning connected browsers; works, but the fallback needs the work account set first |

`RETARGETING.md` tracks these. Your Fathom identity suggests `david.leonty@thewfsgroup.com`
for the first one, matching your predecessor's pattern, but I have not assumed it.

### 6. Credentials are not in place yet

`SLACK_BOT_TOKEN` gates every single task. `ONCEHUB_API_KEY` is now in
`.claude/settings.local.json` (gitignored) for local use, and still needs rotating since it came
through chat. Pipedrive and Google OAuth are per-connector.

---

## P2. These will run and produce wrong or broken output

### 7. `fable-mode` does not exist

`board-orchestrator` routes all high-stakes work (money, compliance, numbers from source
systems) "inside `fable-mode`", and `references/routing.md` repeats it. There is no such skill.
The closest is `fable-review`, an audit protocol, which is not the same thing as a wrapper mode.
Every high-stakes board task hits an unresolvable instruction.

### 8. The self-heal write tool does not exist in cloud routines

Both show-rate prompts persist lessons by rewriting their own prompt via
`mcp__scheduled-tasks__update_scheduled_task`. That is a local Cowork scheduled-task API; a
claude.ai cloud routine has no such tool. Both prompts also declare that call "the ONLY write of
any kind it may make", so on the cloud the self-heal loop can diagnose but never persist, and
the LESSONS LEDGER stops accumulating silently.

**Fix:** decide per task. Keep the rule if you run these locally; otherwise replace persistence
with "report the lesson in the run output for the operator to paste in".

### 9. Fifteen Google Drive resources must be shared with your work account

Including six per-rep SIP documents (these are personnel records), the TTW Salesboard 2026
workbook, the Active Sales Team Roster, the Decision Leadership Objection Matrix, the SIP master
template, and the QA Failure Log sheet.

| Engine | SIP document |
|---|---|
| vidush-rana | `1K355E4r2Iti7G_g9_rE4VsFHrwTkoEtCBbkHTlzf-8Q` |
| crue-lindgren | `1heyBUvV1IT-hfG4TW5uCJrMfzsvghcEc2BWRSIIbPWc` |
| garrett-mckenna | `1vLZotZ1TjCokpFpF-JKStDP-jItDlzSon02ttfmpJcE` |
| noel-soto | `15ew_N7HuUWkC3lumddd5XkFU0JQVs0ipUxj1Ivsypj4` |
| scott-jose | `1mIyWP5V3bQjVVEjR9ncS0h-YBhH1jBj1Lmpipq-ADNQ` |
| jayden-coulter | `1bR4DhgAM5pa8Fe77GxfDWYELxgNX-3mxEMLC-34BmEE` |

Each engine has a DESTINATION LOCK: it may edit only its own doc and must stop rather than
create a replacement. So an unshared doc is a clean stop, not a wrong write. Worth confirming
access to all fifteen before enabling anything.

### 10. The Slack bot must be a member of three channels

`#payments` (C07PVHXGD38, read), `#wfs-ttw-sales-reps-dm-external` (C09ADJS1V6H, post),
`#wfs-ttw-sales-mgmt-client` (C098J2VG41E, post). `chat.postMessage` into a channel the bot has
not joined returns `not_in_channel`, and the prompts correctly refuse to improvise another
destination, so the report simply does not send. DMs need `im:write`.

### 11. Fixed during this review: a stale DM channel id in the EOW report

`ttw-eow-report` read call-review activity from "the self DM `D092C868SPP`". That id is the
OUTGOING director's DM channel, and the rename pass had relabelled it as yours, which would
have made the report read his DM and find nothing. It now resolves your own DM channel from
DIRECTOR_SLACK_ID instead. Flagging it because it is the kind of error a rename cannot catch:
the label changed, the id did not.

### 12. Pipedrive label option id 63 must still exist

Both audit tasks require a deal label option named exactly "Director Audit" (id 63) and STOP if
it is missing. Confirm it survived in your Pipedrive.

### 13. Supabase stops being optional

Six artifacts read or write `lead_quality`: the daily call publisher, the backfill guardian, the
zero-row guard, the CRM outcome sweep, the webinar report, and the webinar lead-quality skill.
The README calls Supabase optional. Under the Callix design it becomes the record of a call
having happened at all. Decide explicitly whether you are keeping that pipeline.

---

## P3. Operational notes

- **Skill names are load-bearing.** Prompts invoke skills by exact name, some with an
  `anthropic-skills:` prefix that is a workspace label and will differ in your account. Upload
  all 17 with folder names unchanged, then check the prefix the prompts use.
- **Six SIP engines need a browser and a bash subagent.** They edit a Google Doc through Claude
  in Chrome and parse the Salesboard xlsx in a sandbox. These cannot run as cloud routines;
  they are local tasks by nature.
- **Stagger the SIP engines.** Their own HARD RULE 12 warns that two browser tasks sharing one
  Chrome is an environment-interference stop. The handoff times are already staggered; keep it.
- **`SendUserFile` in the Saturday weekly review** delivers the workbook into the session. That
  is meaningful when you run it yourself and meaningless unattended; the Slack DM is the part
  that reaches you.
- **`ttw-crm-outcome-sweep` and `lead-quality-zero-row-guard` both run 9:00 AM Tue-Sat** and
  both read the same table. Harmless, but if you enable both, expect two Supabase reads at once.

---

## Suggested order

1. Set `PROCESS_MODE: DRY_RUN` on both Pipedrive audit tasks. Before anything else.
2. Decide local-vs-cloud per twinned pair; schedule one side only.
3. Supply the four identity values and the Slack bot token; invite the bot to the three channels.
4. Confirm Drive access to all fifteen resources and the Pipedrive label.
5. Resolve the Callix read path. Until then, hold every call-dependent task, and know that the
   two client-facing show-rate reports cannot run at all.
6. Then start the TEST runs described in `RETARGETING.md` section 3.
