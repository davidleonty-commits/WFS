# START HERE: instructions for the new director's Claude Code

You are setting up the WFS / TikTok Wiz sales automation package for a new Sales Director. The package was built by the previous director, Cayden Johnson, and every file in it still carries his name, his Slack identity, his Google accounts, and his private connector. **Nothing in this package may be recreated, run, or scheduled until his identity has been fully removed and the new director's has been written in.** This file is the procedure. Follow it in order and do not skip the checks.

Rule for the whole procedure: **never guess or invent a value.** Every replacement comes from the director's own answer. If an answer is missing, stop and ask again.

---

## Step 0. What replaces the WFS connector: two API keys and one connector

The old "Lovable WFS" connector was one plug doing three jobs. It is replaced by three plugs, all of which Claude Code already knows how to use. No app, no proxy, no hosting.

| Job the connector did | Replacement | How to plug it in |
|---|---|---|
| Call data (`calls_list`, `calls_get_analysis`, `calls_find_review_candidates`) | **Callix MCP** | `claude mcp add callix -e CALLIX_API_KEY=<key> -- npx -y @callixorg/mcp-server` (local). Cloud routines: `curl` against the Callix REST API with `CALLIX_API_KEY` set on the cloud environment. See REPLY-2-CALLIX.md. While Callix is still live, the Callix claude.ai connector also works as the comparison baseline. |
| Bookings (`oncehub_booking_counts`, `oncehub_list_bookings`, `oncehub_get_master_page`) | **OnceHub REST API v2** via `curl` | `export ONCEHUB_API_KEY=<key>` in the shell (local) or on the cloud environment. The OnceHub MCP is NOT this; it only books meetings. See TROUBLESHOOTING-REPLY.md section D for the exact endpoints. |
| Slack (`slack_schedule_message`, `slack_read_channel`) | **claude.ai Slack connector** (already connected) | Reads and every send, TEST and LIVE, as the director. Send one test to the director's DM first to see how the "via Claude" attribution renders; the director signs off before anything goes LIVE. See TROUBLESHOOTING-REPLY.md section E. |

Two things the connector did that are now sentences in the prompts, not a service: matching a call to its OnceHub booking to decide whether it is a consultation, and mapping reps to a stable identifier. The replies spell both out.

Keys go in environment variables or connector settings, never in a prompt file.

## Step 1. Ask the director for these values, in these words

Ask all of them in one message so the director can answer once. Copy this block into the chat:

> Before I can set up any of the automations, I need to replace the previous director's identity everywhere in the package. Please give me:
>
> 1. **Your full name** as it should appear in reports (for example "David Smith").
> 2. **Your first name or what the team calls you.** This goes into every message that has to sound like you wrote it.
> 3. **Your Slack handle** in the WFS Group workspace (the part after the @).
> 4. **Your Slack member ID.** In Slack, click your profile picture, then "Profile", then the three-dot menu, then "Copy member ID". It starts with U.
> 5. **Your self-DM channel ID.** Open your own DM in Slack (the one with your own name), then the URL in the browser ends with /D followed by letters and numbers. That D value is the ID. Several tasks use your self-DM as their memory and as the safe TEST destination.
> 6. **Your @thewfsgroup.com Google account** email.
> 7. **Your @ttwhizprogram.com Google account** email, if you have one separate from the WFS account. The Salesboard spreadsheet must be read under a TTW work identity. If you only have one account, say so.
> 8. **Your Pipedrive user ID.** In Pipedrive, go to Settings, then Users, click your name, and the number at the end of the URL is the ID. Eight digits. The Thursday audit task clears your own To-do activities, so this must be yours.
> 9. **Are you using an Asana board** for your own work? If yes, its exact name. If no, say "none" and I will skip the board-orchestrator skill.
> 10. **Do you want lead-quality history in Supabase?** The previous setup is paused and nothing live depends on it. If no, say "none" and I will remove the Supabase steps. If yes, give me the new Supabase project ID once it exists.
>
> Separately, and NOT in this chat if you would rather not paste keys here: I will also need you to connect, under your own account, the Slack, Callix, Pipedrive, and Google Drive connectors in claude.ai, and to obtain an OnceHub API key from a OnceHub admin. Those are credentials and they never go into a prompt file.

Wait for the answers. Do not proceed on partial answers.

## Step 2. Write the answers into `replacements.json`

Copy `replacements.template.json` to `replacements.json` and fill in every field from the director's answers. Leave `SUPABASE_PROJECT_ID`, `ASANA_BOARD_NAME`, and `BROWSER_DEVICE_ID` blank unless the director gave you a value for them. Never put an API key, token, or password in this file.

Show the director the filled file and ask them to confirm each value is correct before you run it.

## Step 3. Run the scrub

```bash
python3 personalize.py replacements.json --dry-run
```

Read the output. It lists every file that will change. Then:

```bash
python3 personalize.py replacements.json
```

The script also rewrites every `LIVE_TARGET: #wfs-ttw-sales-mgmt-client` to the director's own DM, because nothing automated may post to the client channel, and flags any remaining send to it. It replaces every occurrence of the previous director's name (Cayden, Caydo, Cayden Johnson, all possessive and uppercase forms), Slack handle, Slack user ID, self-DM channel ID, both Google emails, Pipedrive user ID, Asana board name, and Supabase project ID across every prompt and skill. It then runs a residue check and refuses to report success while any trace remains.

Expected outcome after a correct run: `0 identity residue line(s)`, except for lines containing the previous director's browser `deviceId` in the six SIP engines, which are removed in Step 5.

If the residue check reports anything else, read the flagged lines. If it is a pattern the script does not know, add it to the `PREVIOUS` list in `personalize.py` with the right replacement key and re-run. Do not hand-edit around the script; the check has to end at zero.

## Step 4. Confirm the scrub by hand on three files

Open these and read them fully, looking for anything that still describes the previous director rather than the new one:

- `cloud-routines/daily-ttw-leaderboard-v4/SKILL.md` (CONFIG block: TEST_TARGET, work Google account)
- `cloud-routines/sip-engine-jayden-coulter/SKILL.md` (CONFIG block and the Slack delivery step)
- `skills/ttw-eow-report/SKILL.md` (reads the director's self-DM; the ID must be the new one)

This catches the class of error where a label was changed but the ID next to it was not, or the reverse. Also confirm that the voice rules ("must sound like [first name] wrote it", "in [first name]'s voice") now carry the new director's name; the team should read these messages as coming from them.

## Step 5. Remove the previous director's connector and browser

Follow README Section 1A and `TROUBLESHOOTING-REPLY.md` sections C, D, E, F, and G. In short:

- Replace every `Lovable WFS` / `Lovable_WFS_Slack` tool call with the mapped Callix, OnceHub REST, Slack connector, or Pipedrive call.
- Delete every `REP_WFS_ID` value; use the rep's email.
- Delete every `WFS_MCP_TOKEN` error-handling line.
- Delete the browser-attach block in all six SIP engines and replace the Google Doc edit with the Drive connector write.
- Replace the `update_scheduled_task` self-rewrite steps with a QA Failure Log write plus an owner DM.

Then run:

```bash
python3 personalize.py --check
python3 personalize.py --check-connector
```

Both must come back clean: `0 identity residue`, `0 connector residue`, and Supabase residue either 0 or resolved per the director's answer to question 10.

## Step 6. Only now: recreate the tasks

Follow `TROUBLESHOOTING-REPLY.md` sections A, B, and K. Recreate only the `cloud-routines/` editions plus the six SIP engines. Every task starts in TEST or DRY_RUN and delivers only to the new director's self-DM. Flip a task to LIVE only after two clean TEST runs that match its template.

## What the director still owes you after this

- Connecting Slack, Callix, Pipedrive, and Google Drive in claude.ai under their own account.
- An OnceHub API key from an admin, stored as a secret, never in a file.
- Membership in `#wfs-ttw-sales-reps-dm-external`, `#wfs-ttw-sales-mgmt-client`, and `#payments`.
- Confirmation that the previous director has shared the 14 Google Drive files listed in `TROUBLESHOOTING-REPLY.md` section I.
- Confirmation of the current rep roster against the WFS Active Sales Team Roster sheet.

Ask for each of these explicitly and record what is still outstanding in your final summary to the director.
