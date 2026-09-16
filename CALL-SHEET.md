# Call sheet: getting David unblocked (about 45 minutes)

Goal of the call: leave with every input his Claude is waiting on, so TEST runs can start the same day. Do these in order; each one unblocks the next. At the end of each item, David pastes the result into his Claude Code session.

Have open before the call: Slack (WFS Group), a terminal on David's laptop, OnceHub admin, Callix, Pipedrive, Google Drive.

---

## 1. The six identity values (5 minutes)

His Claude has asked three times. Get them on the call, read them back, done.

| Value | Where David finds it | Paste to Claude as |
|---|---|---|
| Slack handle | Slack profile; the part after the @, e.g. `david.leonty` (not the display name "David Leonty") | `SLACK_HANDLE: david.leonty` |
| Self-DM channel id | In Slack, open the DM with himself (his own name in the sidebar). In the desktop app: click the channel name at the top, scroll to the bottom of the popup, "Channel ID: D…". Or in the browser the URL ends in `/D…`. | `SLACK_SELF_DM_ID: D…` |
| @thewfsgroup.com Google account | whichever he signs into Google with for WFS | `WFS_EMAIL: …` |
| @ttwhizprogram.com Google account | if he has one; otherwise say "same" | `TTW_EMAIL: …` or `same` |
| Asana board | exact board name, or "none" (recommended unless he already runs one) | `ASANA_BOARD_NAME: none` |
| Supabase | "none" (recommended; it is paused and nothing live needs it) | `SUPABASE_PROJECT_ID: none` |

Already captured by his Claude: full name, first name, Slack member id `U0BUZ6C0C91`, Pipedrive `27299998`.

**Done when:** his Claude reports `personalize.py` at 0 identity residue.

## 2. Join the three Slack channels (2 minutes)

David's own Slack user must be a member because every send goes out as him. There is no bot to invite.

- `#wfs-ttw-sales-reps-dm-external` (reps, includes external members)
- `#wfs-ttw-sales-mgmt-client` (client-facing management)
- `#payments` (read only)

Have a WFS Slack admin add him if any are private. **Done when:** he can open all three.

## 3. Slack: one test message (2 minutes)

David already has the claude.ai Slack connector connected to WFS. Nothing to create. Have his Claude send one short message to his own DM and look at it together in the WFS workspace: is there a "via Claude" attribution, and how does it render? David decides whether that is acceptable in the reps channel. **The client channel `#wfs-ttw-sales-mgmt-client` is off limits regardless**: the five tasks that used to post there (lead flow, midday and EOD show rate, webinar report, PIF buyer report) now deliver to David's DM and he forwards to the client by hand if needed. Everything stays in TEST (his DM) until he says so.

**Done when:** the message lands in his DM and he has seen the attribution.

## 4. OnceHub API smoke test (5 minutes)

His Claude cannot run this because its cloud sandbox blocks `api.oncehub.com`. David runs it on his laptop.

Prereq: a OnceHub API key from a OnceHub admin (OnceHub, Settings, API and Webhooks, generate key). If David is not admin, get the admin on the call or have the key sent ahead.

```bash
echo 'export ONCEHUB_API_KEY=…' >> ~/.zshrc && source ~/.zshrc
curl -s -H "API-Key: $ONCEHUB_API_KEY" \
  "https://api.oncehub.com/v2/bookings?starting_time.gt=2026-09-15T04:00:00Z&starting_time.lt=2026-09-16T04:00:00Z&limit=100" | head -c 3000
```

(That window is yesterday in Eastern time, the day boundary the reports use. Adjust the dates to yesterday when you run it.)

What to look for:
- Rows come back. On 401, retry with `-H "Authorization: Bearer $ONCEHUB_API_KEY"`.
- Each row has a `status` and a booking-calendar field. Note the exact field name.
- Some rows have no shared calendar (booked on a rep's personal page). That is expected.

**Paste to Claude:** the first row's field names (not the whole payload; it has lead emails). His Claude finishes the "master page" rename against the real names. **Done when:** his Claude reports the nine OnceHub prompts rewritten and the lead-flow report producing a count in TEST.

## 5. Callix first call (10 minutes)

Prereq: David's Callix API key (Callix, API Keys tab).

Local MCP (for on-demand skills and this test):
```bash
claude mcp add callix -e CALLIX_API_KEY=callix_… -- npx -y @callixorg/mcp-server
```
Then in a Claude Code session: "call `get_current_time`, then `list_calls` for yesterday with no filters, and show me the raw first row."

What his Claude checks off, per REPLY-2 section 3: for each call can it get id, rep, lead email, start time, duration, whether it is a consultation, transcript with timestamps. The one to watch is **"is it a consultation"**: the old prompts key on the Zoom title containing "TikTok Wiz Consultation". If Callix has no title field, his Claude falls back to matching the call to its OnceHub booking by lead email and start time, which is what the old connector did.

For cloud routines: set `CALLIX_API_KEY` as an environment variable on the claude.ai Code environment (claude.ai, Code, Environments, the one the routines use). His Claude then uses `curl` against the Callix REST API there. If that environment has no place for variables, tell his Claude; the fallback is in REPLY-2 section 4.

**Done when:** his Claude reports all seven fields resolved, or names exactly which one is missing.

## 6. The WFS admin question (1 minute, may need a follow-up)

Ask verbatim, ideally with the admin on the call or by message during it:

> "Is the Callix workspace being cancelled, and on what date? Are the Zoom consultation calls booked through OnceHub being recorded in Callix today?"

**Paste to Claude:** the answer with the date. It decides whether the Callix comparison runs are possible and how urgent the Callix cutover is.

## 7. Google Drive access (2 minutes, your action)

Share the files in TROUBLESHOOTING-REPLY.md section I with David's work Google account while you are on the call: the Salesboard (viewer), the roster sheet (editor), the objection matrix (viewer), the SIP template (viewer), the six per-rep SIP docs (editor), the webinar doc and QA Failure Log (editor). Confirm the SIP-doc transfer is OK with WFS leadership if you have not.

**Done when:** David can open the Salesboard and one SIP doc.

---

## After the call: the first TEST run

Once 1 through 7 are in, his Claude can recreate the first task. Suggest the order:
1. `eow-report-reminder` (one DM, no data sources; proves Slack TEST path)
2. `ttw-daily-lead-flow-report-cloud` (OnceHub only; proves the denominator)
3. `daily-ttw-leaderboard-v4` (Pipedrive plus Salesboard; proves Drive and Pipedrive)
4. `daily-call-report-publisher-v27` (Callix or Callix; proves the call layer)
5. the two show-rate reports (OnceHub plus calls together)

Everything to David's DM. Two clean days per task, message matches its template line for line, then LIVE one task at a time. The only LIVE channel is the reps channel; the client channel is never a destination.

## What you can answer on the call that his Claude cannot

- Why a rule exists (the 9:00 AM payments cutoff, the 80% failsafe, the 15-minute floor, why S2C is bucketed separately, why the Salesboard is read-only).
- What a normal day looks like: roughly how many closer bookings per day, typical show rate range, what a good leaderboard post reads like. Give David two or three real examples from your Slack history so he can judge the first TEST outputs.
- Which reps are current. Walk the roster sheet with him.
