# Retargeting checklist for the new director

The Section 1A connector swap is done and the director identity is now David Leonty.
This file tracks what is filled in and what is still outstanding.

| Item | Value | Status |
|---|---|---|
| Slack member ID (`DIRECTOR_SLACK_ID`) | `U0BUZ6C0C91` | Filled, 39 files |
| Slack handle | `david.leonty` (display name "David Leonty") | Confirmed from the Slack connector |
| Pipedrive user id (`OWNER_USER_ID`) | `27299998` | Filled, the 2 audit tasks |
| Director name in voice and identity text | David / David Leonty | Swapped, 36 files |
| WFS work Google account | `david.leonty@thewfsgroup.com` | Filled, 9 files |
| TTW work Google account | `david.leonty@ttwhizprogram.com` | Filled, 2 files |
| Team Sync organizer | `david.leonty@thewfsgroup.com` | Filled as a lookup key, verify on first run |
| Slack channel membership | member of all 3 channels the tasks touch | Verified 2026-09-16 |
| Self-DM channel id | not supplied | Not needed — resolved at runtime |
| Browser deviceId (local SIP engines) | not supplied | **Outstanding** |
| Asana board name | not supplied | **Outstanding** |
| Supabase project id | not supplied | **Outstanding** |

The Slack handle and the WFS account were not guessed: `slack_read_user_profile` on
`U0BUZ6C0C91` returns username `david.leonty`, email `david.leonty@thewfsgroup.com`,
organization WFS Group, timezone America/New_York.

---

## 1. Still outstanding

### Browser deviceId (the six SIP engines, plus the QA failure review)

`deviceId 2fac653e-7302-41bb-839a-a7b4b18cab1b` was the outgoing director's machine. Replace it
with your own, or delete the id and let the task fall back to its existing "list connected
browsers and pick the one signed into the work account" path, which already handles a wrong or
missing deviceId. That fallback now checks for `david.leonty@thewfsgroup.com`.

### Asana board name and Supabase project id

Both are one value each, and both may legitimately be "none" — say so and the steps that use
them are deleted rather than filled. See TROUBLESHOOTING-REPLY.md section J for Supabase.

### Team Sync organizer — filled, but verify

`cloud-routines/ttw-daily-lead-flow-report-cloud` finds the "TTW - Team Sync" meeting by
subject and *prefers* one organized by `TEAM_SYNC_ORGANIZER`. It is set to David on the
assumption the sitting director inherited the meeting. Because the organizer breaks ties
rather than filtering, a wrong value degrades to subject matching instead of losing the
meeting — but if someone else hosts the sync, change it.

### Secrets (never in a prompt body)

Store these where your environment stores secrets, per `DATA-ACCESS.md` section 6:
`ONCEHUB_API_KEY`, `CALLIX_API_KEY`, `PIPEDRIVE_API_TOKEN`, Google OAuth, and (only if you keep
the `lead_quality` pipeline) `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`. There is no Slack bot
token: the claude.ai Slack connector posts as the connected user.

No API key has ever been written to this repository. The OnceHub key was supplied on
2026-09-15 and again on 2026-09-16; it lives only in gitignored `.claude/settings.local.json`.
Rotate it in OnceHub (Settings, API and Webhooks), because it has now been pasted into a chat
transcript twice.

**The Callix key supplied on 2026-09-16 was not stored. It is character-for-character the same
string as the OnceHub key, which two unrelated vendors cannot both have issued — it is a
copy-paste of the wrong value. Nothing was written rather than wire a key that will fail
authentication in a way that looks like a Callix outage.**

---

## 2. What the name swap did and did not touch

"Cayden" and "Caydo" now read "David" wherever the text is about the sitting director: voice
instructions, delivery targets, approval gates, and the rules that name the Sales Director
(including "exclude the Sales Director's own calls" in the weekly call review, which would
otherwise have excluded the wrong person's calls).

Five things deliberately still say Cayden, because changing them would falsify a record or
break a lookup:

- `Went LIVE on 2026-07-02 per Cayden's instruction` and similar dated ledger entries. History.
- `two "Cayden Johnson"` in the duplicate-name warning. That is a real data-quality fact about
  the roster, and it is the reason the reports join on ids rather than names.
- `Work Board - Cayden`, the literal Asana project title, and its GID row in the board map.
  Rename the board in Asana first if you adopt it, then change this.
- The `→ Cayden` whitespace example in `board-orchestrator/references/board-map.md`, which is a
  literal field-label sample.
- `Assigned to Cayden Johnson` in a board-map example row.

Also corrected while swapping: two skills asserted the director lives in Lehi, Utah. The
operative fact was the timezone, so they now say Mountain Time without claiming a location.

`skills/board-orchestrator` is still the outgoing director's personal Asana board runner. It is
only useful if you adopt the same board; otherwise leave it uploaded and unused, or drop it.

---

## 3. Test order

1. Connect Slack, Avoma, Pipedrive and Drive, and set the four outstanding values above.
2. Leave every `DELIVERY_MODE` on TEST. In TEST every task DMs you and nothing reaches a
   channel, a rep, or the client.
2a. **Look at how a sent message renders before anything goes LIVE.** Every send now goes out
   through the claude.ai Slack connector as YOU, and a message sent that way may carry a small
   "via Claude" attribution in Slack. Send one test message to your own DM and look at it in the
   WFS workspace. You decide whether that attribution is acceptable in the reps channel and,
   especially, in the client-facing channel. This is a judgment only you can make, and it is
   worth making before two weeks of TEST runs rather than after.
3. Run each task once and compare its Slack output to the message template in its own prompt,
   line for line. The templates did not change in the swap, so a drift is a real finding.
4. Flip to LIVE one task at a time. Hold the two client-facing reports
   (`ttw-daily-lead-flow-report`, `eod-show-rate-update`) in TEST until you trust the numbers:
   the client reads those.
5. The SIP engines go LIVE only when you are ready for the rep to receive the message directly.
   In TEST they message only you.
