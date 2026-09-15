# Retargeting checklist for the new director

The Section 1A connector swap is done: no prompt or skill in this package calls the retired
Lovable WFS MCP any more. What is left is IDENTITY. Every task was written with Cayden Johnson
as the owner, and the values below still point at him or at his machine. Work down this list
before you enable anything.

Nothing here is a code change. Each item is one value to fill in or confirm.

---

## 1. Blocking: fill these in or the task cannot run

### `DIRECTOR_SLACK_ID` (39 files)

Every Slack destination that used to be the outgoing director's DM is now the token
`DIRECTOR_SLACK_ID`, defined at the top of each prompt as `<fill in: your own Slack member ID,
for example U01234567>`. Replace that placeholder with your own Slack member ID in every file
you enable. Find your ID in Slack: click your avatar, View profile, the three-dot menu, Copy
member ID.

Find every one of them with:

```bash
grep -rn "fill in: your own Slack member ID" --include='*.md' .
```

Use the member ID, not a handle. Handle resolution was a feature of the retired app; the Slack
API resolves ids.

### `OWNER_USER_ID`, the Pipedrive audit tasks (2 files)

`scheduled-prompts/pipedrive-director-audit-labeling` and
`cloud-routines/pipedrive-activity-clearing-cloud` clear the OWNER'S due and overdue Pipedrive
activities. Their `OWNER_USER_ID` is a fill-in value now, because running either task against
the outgoing director's id (23815275) would clear a departed user's activities. Put your own
Pipedrive user id there, and run with `PROCESS_MODE: DRY_RUN` first.

### Secrets (never in a prompt body)

Store these where your environment stores secrets, per `DATA-ACCESS.md` section 6:
`SLACK_BOT_TOKEN`, `ONCEHUB_API_KEY`, `AVOMA_API_KEY`, `PIPEDRIVE_API_TOKEN`, Google OAuth, and
(only if you keep the `lead_quality` pipeline) `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`.

---

## 2. Confirm before enabling

### The work Google account (8 files)

`cayden.johnson@thewfsgroup.com` is the WORK Google identity the Salesboard and the SIP docs are
read and written under. The five local SIP engines verify the attached browser is signed into
it before touching anything, and the leaderboard requires the work account for the Salesboard
read. Replace it with your own work Google account, and keep the verification step: it is what
stops a run editing a personnel record from the wrong identity.

```bash
grep -rn "cayden.johnson@thewfsgroup.com" --include='*.md' .
```

### The director's Avoma account (1 file)

`skills/ttw-eow-report` reads your own call-review activity from Avoma by account email. The
outgoing director's was `cayden.johnson@ttwhizprogram.com`. Put yours in.

### The browser deviceId (the six SIP engines, plus the QA failure review)

Each SIP engine, and `cloud-routines/weekly-qa-failure-review`, tries to attach to a specific
Chrome instance (`deviceId 2fac653e-7302-41bb-839a-a7b4b18cab1b`), which was the outgoing
director's machine. Replace it with your own, or delete the id and let the task fall back to its
existing "list connected browsers and pick the one signed into the work account" path, which
already handles a wrong or missing deviceId.

### The roster

As handed off: Closers Vidush Rana, Crue Lindgren, Turok Tarango, Tom Judson, Garrett McKenna,
Noel Soto, Scott Jose. Setters Antonio Vespa, Petros Foustanellas. The cloud tasks read the WFS
Active Sales Team Roster sheet (Drive fileId `1qynTKt3Z8JhJK_CkdmwMcfiR5XbD1L0NKkZ4xcImDKo`) at
step 0 and only rows with `Status = Active` may appear, so that sheet is where you add or remove
a rep. Two notes after the swap:

- The roster's `Pipedrive Owner ID` column is now the join key for every deal and activity
  figure, and its `Slack User ID` column is what renders rep mentions. Both must be populated
  for a rep to appear correctly.
- The roster's old WFS rep UUID column is dead. Nothing reads it.

The older local prompts (`scheduled-prompts/`) still carry hardcoded rosters. Confirm those
against the sheet before enabling one, or prefer its cloud twin, which reads the sheet.

---

## 3. Voice and name, cosmetic but visible

`Cayden` and `Caydo` appear in 46 files, mostly in the voice instructions, mostly as "write this
the way Caydo would say it". The voice RULES (first names only, no consultant-speak, no hype,
no em dashes) are what the team is used to and should stay. Swap the NAME where the text is
about identity, such as the signature of a hype message or "Cayden sends that one himself". The
heaviest users are the call-review skills and `skills/board-orchestrator`.

`skills/board-orchestrator` is his personal Asana board runner. It is only useful if you adopt
the same board; otherwise leave it uploaded and unused, or drop it.

---

## 4. Test order

1. Fill in `DIRECTOR_SLACK_ID` everywhere and connect Slack, Avoma, Pipedrive and Drive.
2. Leave every `DELIVERY_MODE` on TEST. In TEST every task DMs you and nothing reaches a
   channel, a rep, or the client.
3. Run each task once and compare its Slack output to the message template in its own prompt,
   line for line. The templates did not change in the swap, so a drift is a real finding.
4. Flip to LIVE one task at a time. Hold the two client-facing reports
   (`ttw-daily-lead-flow-report`, `eod-show-rate-update`) in TEST until you trust the numbers:
   the client reads those.
5. The SIP engines go LIVE only when you are ready for the rep to receive the message directly.
   In TEST they message only you.
