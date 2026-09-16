# Creating the scheduled tasks

Tested and written 2026-09-16.

## Why these are not already created

`create_trigger` from a Claude Code session cannot attach connectors on this
organization — the parameter is rejected outright, and a routine created without it
fires sessions that have no `mcp__*` tools at all. A routine built that way would wake
every weekday, find no Slack and no Pipedrive, and fail. One was created to confirm this,
got exactly that warning back, and was deleted.

**Create these from the claude.ai routines UI instead** (claude.ai/code/routines), which is
where the originals lived and where connectors can be attached. For each task below: new
routine, paste the cron, paste the prompt, attach the listed connectors, save.

Every prompt below sets DELIVERY_MODE: TEST, so the task DMs David and posts to no channel.
That is the handoff's own rule — two clean TEST runs before anything goes LIVE.

---

## Preflight: what actually works from this environment

| Source | State |
|---|---|
| Slack (as David Leonty) | works; member of all three channels the tasks touch |
| Pipedrive | works; `getDeals` and `getActivities` both return |
| Google Drive | works; the Salesboard reads (580 KB) |
| Fathom | works, authenticated as david.leonty@thewfsgroup.com |
| **OnceHub** | **blocked** — `api.oncehub.com` and `mcp.oncehub.com` both get 403 at the environment network policy |
| **Avoma** | **not connected** — 8 `mcp__Avoma_MCP__*` calls in the prompts have no server behind them |
| Supabase / Asana | not connected (deliberately ignored) |
| Callix | readable via `#callix-call-updates` only; no API key |

---

## The seven that can run today

### `pipeline-accountability-report-v2-cloud`

- **Cron (UTC):** `6 18 * * 1-5`  — 12:06 PM MT, weekdays
- **Connectors to attach:** Slack, Google Drive, Pipedrive
- **Writes:** read-only

```
Run the WFS scheduled task `pipeline-accountability-report-v2-cloud`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/pipeline-accountability-report-v2-cloud/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. Read-only. Beyond the single Slack message in STEP 2, create, update or delete nothing — not in Pipedrive, not in Drive, not in Slack.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. Reads Pipedrive and the roster sheet, posts one message. LIVE target is #wfs-ttw-sales-reps-dm-external.
```

### `daily-midday-checkin-v2-cloud`

- **Cron (UTC):** `0 19 * * 1-5`  — 1:00 PM MT, weekdays
- **Connectors to attach:** Slack, Google Drive
- **Writes:** read-only

```
Run the WFS scheduled task `daily-midday-checkin-v2-cloud`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/daily-midday-checkin-v2-cloud/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. Read-only. Beyond the single Slack message in STEP 2, create, update or delete nothing — not in Pipedrive, not in Drive, not in Slack.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. Reads #payments after 9:00 AM and today's sets from the reps channel; reads its own last two DM posts as memory.
```

### `daily-sales-hype-v3`

- **Cron (UTC):** `30 14 * * 1-5`  — 8:30 AM MT, weekdays
- **Connectors to attach:** Slack, Google Drive, Pipedrive
- **Writes:** read-only

```
Run the WFS scheduled task `daily-sales-hype-v3`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/daily-sales-hype-v3/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. Read-only. Beyond the single Slack message in STEP 2, create, update or delete nothing — not in Pipedrive, not in Drive, not in Slack.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. Drive reads must run under david.leonty@thewfsgroup.com. No gviz CSV fallback, no browser.
```

### `daily-ttw-leaderboard-v4`

- **Cron (UTC):** `0 16 * * 1-5`  — 10:00 AM MT, weekdays
- **Connectors to attach:** Slack, Google Drive, Pipedrive
- **Writes:** read-only

```
Run the WFS scheduled task `daily-ttw-leaderboard-v4`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/daily-ttw-leaderboard-v4/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. Read-only. Beyond the single Slack message in STEP 2, create, update or delete nothing — not in Pipedrive, not in Drive, not in Slack.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. Salesboard read runs under david.leonty@ttwhizprogram.com. Has an 80% failsafe and a strict roster.
```

### `midday-hype-mwf`

- **Cron (UTC):** `0 21 * * 1,3,5`  — 3:00 PM MT, Mon/Wed/Fri
- **Connectors to attach:** Slack, Google Drive, Pipedrive
- **Writes:** read-only

```
Run the WFS scheduled task `midday-hype-mwf`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/midday-hype-mwf/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. Read-only. Beyond the single Slack message in STEP 2, create, update or delete nothing — not in Pipedrive, not in Drive, not in Slack.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. Bottom-2 vs leader on a 7-day rolling window. The only runnable task with no browser step at all.
```

### `eow-report-reminder`

- **Cron (UTC):** `0 22 * * 5`  — 4:00 PM MT, Friday
- **Connectors to attach:** Slack
- **Writes:** read-only

```
Run the WFS scheduled task `eow-report-reminder`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/eow-report-reminder/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. Read-only. Beyond the single Slack message in STEP 2, create, update or delete nothing — not in Pipedrive, not in Drive, not in Slack.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. A reminder only. It must NOT build the EOW report or invoke the ttw-eow-report skill.
```

### `pipedrive-activity-clearing-cloud`

- **Cron (UTC):** `0 13 * * 4`  — 7:00 AM MT, Thursday
- **Connectors to attach:** Slack, Pipedrive
- **Writes:** WRITES TO PIPEDRIVE

```
Run the WFS scheduled task `pipedrive-activity-clearing-cloud`.

STEP 1. The WFS repository is checked out in this session. Read `cloud-routines/pipedrive-activity-clearing-cloud/SKILL.md`. Everything after the YAML frontmatter is your prompt — follow it exactly, including its QA gates, templates, thresholds and roster rules. Do not summarise it and do not shortcut it.

STEP 2. DELIVERY_MODE: TEST. Deliver ONLY to the director's own Slack DM (David Leonty, Slack user `U0BUZ6C0C91`); open the DM against that user id rather than using a hard-coded channel id. Prefix the message with `[TEST]`. Do not post to any channel.

STEP 3. CHANNEL PROHIBITION (standing, not mode-dependent, not overridable): `#wfs-ttw-sales-mgmt-client` (C098J2VG41E) is NEVER a destination for this or any task — not in TEST, not in LIVE, not on a retry, not on a fallback, not in a QA failure notice. If a destination ever resolves to that channel, that is a QA FAILURE: do not send, and report it.

STEP 4. PROCESS_MODE: DRY_RUN — this OVERRIDES the EXECUTE value in the SKILL.md CONFIG block. Read and classify only. Make NO Pipedrive writes: no label changes, no `updateActivity`, no marking anything done. Report exactly what EXECUTE would have touched, activity by activity, with the pre-write snapshot for each.

STEP 5. If a required data source is unavailable or errors, do NOT improvise a substitute source and do NOT publish a partial report as if it were complete. Stop, and DM the director exactly what was missing and at which step.

NOTES. The Slack connector posts as the connected user, not as a bot — there is no bot token and nothing needs inviting to a channel. Ships with PROCESS_MODE: EXECUTE. The prompt below forces DRY_RUN. Do not remove that line until a dry run has been reviewed.
```

---

## The fourteen that cannot run yet, and why

### Blocked on OnceHub (5) — network policy, not credentials

`daily-call-report-publisher-v27`, `show-rate-report-eod-v12-cloud`,
`show-rate-update-midday-cloud`, `ttw-daily-lead-flow-report-cloud`, `webinar-report-v8`.

The key is valid as far as anyone knows — it has never been tested, because the request
never leaves the container. The proxy answers 403 to CONNECT for `api.oncehub.com`. This is
the environment's network policy, chosen when the environment was created ("Default —
trusted network access"), and it applies to scheduled runs exactly as it applies here.

**Fix:** allow `api.oncehub.com` on the environment's network policy, then re-run the
smoke test. Nothing in the prompts needs changing. This is the single highest-value
unblock in the package — it covers both show-rate reports, the lead flow report, the
webinar report and the call report publisher.

### Blocked on call transcripts (7)

`lead-quality-zero-row-guard`, `sip-engine-jayden-coulter`,
`ttw-lead-quality-backfill-guardian`, `ttw-weekly-call-review-sat`,
`weekly-call-review-sourcing-v2`, `weekly-clip-finder-cloud`, `weekly-pif-buyer-report`.

Avoma is retired and its MCP is not connected. Callix has the calls but this package has
no way to read a transcript from it: the API key supplied on 2026-09-16 was the OnceHub
key pasted twice, and `#callix-call-updates` carries summaries, not dialogue. Scoring a
call against the WFS rubric needs the dialogue.

**Fix:** a real Callix API key, then the rewrite described in CALLIX-MIGRATION.md. Until
then these stay uncreated rather than created and failing.

### Blocked on Supabase (2)

`ttw-crm-outcome-sweep`, and the `lead_quality` half of the two guardians above. Ignored
by direction; the steps should be deleted rather than left dangling.

### Needs one check (1)

`weekly-qa-failure-review` declares only Slack and Google Drive, but its body references
Avoma and a browser deviceId. Worth reading before creating.

---

## Order to bring things up

1. Create the seven above in TEST. Let them run one cycle and read the DMs.
2. Allow `api.oncehub.com` on the network policy. Re-test. Create the five OnceHub tasks.
3. Get a real Callix key. Then the call-data rewrite, then the remaining seven.
4. Flip a task to LIVE only after two clean TEST runs whose output matches its template.
