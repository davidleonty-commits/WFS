---
name: ttw-avoma-clip-finder
description: Finds sales coaching clips from TikTok Wiz consultation calls by scoring how reps run the Decision Leadership Objection Matrix, then giving David exact clip-in and clip-out anchors so the snippet is one click. Pulls call data from Avoma (list_meetings, get_meeting_transcript, get_meeting_notes) and ranks the candidates itself. Use when David wants weekly clips, objection-handling clips, Great Demo or Missed Opportunity clips, or says "find this week's clips", "find clips", "run the clip finder", "find me 3 clips", or "who handled objections well this week", and when the weekly scheduled task fires. Always use it even when the request sounds simple, because rep identification, close vs no-close detection, the strict eligibility gate, and the verbatim anchor rule carry accuracy rules the output depends on.
---

# TTW Clip Finder (Avoma)

Finds teachable clips from TikTok Wiz consultation calls by scoring how a rep ran the Decision Leadership Objection Matrix, then delivers exact verbatim clip boundaries so David can create the snippet in one highlight.

Data source: **Avoma**, through the Avoma MCP connector (`list_meetings`, `get_meeting`, `get_meeting_transcript`, `get_meeting_notes`), or the REST API at `https://api.avoma.com/v1/...` with header `Authorization: Bearer $AVOMA_API_KEY` when the MCP is unavailable.

This skill owns the candidate ranking. The old connector returned calls pre-ranked and pre-scored; Avoma returns neither, so the ranking below is run here, and every score comes from the transcript.

**CANDIDATE RANKING (run after `list_meetings`, this replaces the old ranked feed):**
1. Keep only real recorded closer consultations: subject contains "TikTok Wiz Consultation" (or the closer-consultation equivalent for the brand asked for), recorded duration strictly over 15 minutes, a transcript available.
2. Drop setter introductions, S2C intros, team syncs, 1:1s, no-connects, voicemails and reschedules.
3. Rank what survives by, in order: whether the call closed (a close and a clear no-close are both wanted, and the mix is set by the clip types below), the size of the deal discussed, how far the rep's handling fell short of the matrix on a no-close, and recency. Most recent first inside a tier.
4. Cap the sweep at 50 candidates for a weekly run and pull transcripts only for the ones you will score.

Target: 3 clips per week by default (David may ask for a different count or mix, for example "3 good examples and 2 improvement points"). Two clip types, and the type controls which calls are even eligible:

1. **GREAT DEMO** comes ONLY from a call that CLOSED, where the rep executed a named matrix step well. The "watch how it is done" clip.
2. **MISSED OPPORTUNITY** comes ONLY from a call that did NOT close, where a clear objection trigger fired and the rep failed to run the step the moment called for. The "here is where we lost it" clip.

A clean close with no objection is correctly NOT clipped. A no-close where the rep ran the flow well is a talking point, not an auto-clip. Never manufacture a clip to hit the number. Three real clips beats five forced ones, and a forced clip teaches the team the wrong lesson.

Score STRICTLY. A step counts as executed only if the rep ran the PRESCRIBED move with the right talk track for that SPECIFIC objection (permission-ask before a reframe, root-relabel on acknowledge, motive-tied consequence and future pace, a clean self-close that produces the decision). Discounting, guarantees, social proof, urgency, and feature dumps do NOT count as matrix moves, even when the call closes.

The closers are Vidush Rana, Tom Judson, Crue Lindgren, Turok Tarango, Paul Rasoumoff, and Ky Newton. The setters are Petros Foustanellas, Antonio Vespa, Aidan Stammers, Saray Cortes, and Brittany Acton.

The full scoring rubric, the 16 objections, the per-step 0-1-2 markers, and the card format live in `references/decision-leadership-rubric.md`. Read that file before scoring. This SKILL.md is the workflow and the accuracy rules that protect the output.

---

## Step 1: Establish the window

The window is a `from_date` / `to_date` pair on `list_meetings`, computed in Mountain Time.
- Default weekly run: the last 7 days.
- "today and yesterday": 2 days. "this week": 7 days. "last two weeks": 14 days (keep 30 as the practical ceiling).
- The director works in Mountain Time (America/Denver). If he names calendar dates, use those dates directly and drop anything outside the range after you pull.
- If David asks for one brand or one rep, filter by meeting subject (brand) and organizer email (rep) after the meetings come back.

## Step 2: List the calls to review

1. Call `list_meetings` over the window and PAGINATE to the end (the response carries a next page link; keep going until it is null). Avoma pages are small, so a week is several pages.
2. Apply the CANDIDATE RANKING above. Each surviving meeting carries a `meeting_uuid` used in the next step.
3. If David asked for a specific rep, keep only that rep's meetings (match the organizer email, never the display name, since Avoma mislabels speakers and duplicate names exist).

## Step 3: Filter to scoreable consultations (STRICT)

The ranking surfaces review candidates, but still confirm each is a real closer consultation before scoring:
- It is a closer **Consultation**, not a setter Introduction / intro call. The matrix does not apply to setter intros.
- It has a usable speaker transcript from `get_meeting_transcript`. No transcript means nothing to score.
- It is a real, full-length pitch call, not a no-connect, voicemail, or reschedule. A long call is not proof of a real consultation, confirm from the transcript end-state.

Keep a short operator list of what got dropped and why. It does not go in the output.

## Step 4: Reliability and the incomplete-run rule

Avoma can time out or error intermittently. For every call:
- Retry a failed or timed-out `list_meetings` or `get_meeting_transcript` at least twice before giving up. The same `meeting_uuid` often succeeds on a retry.
- If Avoma throws an auth error, tell David the Avoma connector needs re-approving (or that `AVOMA_API_KEY` needs refreshing if you are on the REST path), then continue once it is back.

Never silently drop a scoreable call. If an analysis cannot be pulled after retries, note it in the output as not yet scored rather than omitting it.

## Step 4b: Large transcripts (context safety)

`get_meeting_transcript` returns the full speaker transcript inline, and for a long consultation that payload can exceed the inline token limit and be saved to a file instead. When that happens, do NOT read the whole file into the main context. Hand the saved file path to a subagent and have it score the call against the rubric and return only the findings: rep by behavior, close status with the end-state quote, the per-step scores with verbatim evidence, and the candidate clip with verbatim CLIP IN / CLIP OUT anchors plus the timestamp of each anchor if the transcript carries timestamps. This keeps the full transcript out of the main context while preserving verbatim accuracy.

## Step 5: Pull and read each analysis

1. For each kept candidate, call `get_meeting_transcript` with its `meeting_uuid` (and `get_meeting_notes` for the AI notes).
2. Score the matrix from the SPEAKER TRANSCRIPT, never from the notes alone. The transcript is where the permission ask, the relabel, the future pace, and whether the rep folded actually live. There is no pre-computed scorecard any more: the 25-point score, close attempts, downsell and lead bucket are all derived here, from the transcript, against `references/decision-leadership-rubric.md`.
3. Use the AI notes as a cross-check only, never as the score: they help confirm close-vs-no-close and point at where the friction was, but the matrix score and the clip come from the transcript.
4. Work through candidates one at a time or in batches of no more than 5, summarizing each batch before loading more so the run does not blow past context.

## Step 6: Identify the rep by behavior, NEVER by the label

Speaker labels are not reliable, the rep's lines are sometimes tagged with the lead's name. If you score by the label you will attribute the rep's skill to the lead and the whole card is wrong.

Identify the rep as the person who:
- shares their screen and runs the program walkthrough,
- delivers the pitch and the proof-of-concept scroll,
- drops the Clarity Pay or Affirm financing link,
- runs onboarding and access at the end.

Cross-checks: a speaker whose name matches a known closer is the rep. Style cues help confirm. Once identified, every score and every clip attaches to the rep found this way, not the label.

## Step 7: Classify close vs no-close from the end-state

Read the end of the transcript, and cross-check against the analysis `close attempts` and `downsell` fields.

- **CLOSED** signals: a deposit was taken, a Clarity Pay or Affirm funding or deposit confirmation appears, the rep says "you're in" or "congrats", an onboarding call is scheduled, or course or Discord access is granted.
- **NO-CLOSE** signals: deposit declined or never attempted, "I need to think about it", "talk to my spouse", "I'll get back to you", a follow-up booked instead of a sale, or the call ends with no payment. A declined deposit of any amount is a no-close.

If the end-state is genuinely ambiguous, mark it UNCERTAIN and do not draw a clip from it. A clip on a misclassified call is worse than no clip.

## Step 8: Score the FULL step sequence, strictly, and select

Read `references/decision-leadership-rubric.md`, then for each call:
1. Run the Foundation (identity anchor) check once.
2. Find each objection trigger and score Steps 1 to 4 (0, 1, or 2) with the green and red markers in the rubric. Be conservative: a 2 requires the prescribed move with the right talk track for that specific objection. Discounting, guarantees, social proof, and urgency are explicitly NOT matrix moves.
3. Map the WHOLE sequence the rep runs around the objection, not just the single headline step. Reps usually stack multiple steps (acknowledge, then reframe, then self-close). Record every step that appears with its score, including steps run earlier in the call and steps skipped.
4. Apply the eligibility gate:
   - From CLOSED calls, a step executed at a genuine 2 is a GREAT DEMO candidate.
   - From NO-CLOSE calls, a fired trigger where the matching step scored 0 is a MISSED OPPORTUNITY candidate.
5. Rank candidates and select the requested number (default 3), aiming for a spread across different steps and reps. If David asks for a specific mix (for example good examples plus improvement points), honor it. If real candidates are thin, deliver fewer and say why. Do not pad. If the calls that closed did so by breaking the matrix (discount, guarantee, urgency), say that plainly rather than dressing one up as a Great Demo.

---

## The verbatim anchor rule (accuracy-critical)

The clip boundary is verbatim anchor text, not a timestamp.

- CLIP IN and CLIP OUT must be copied word for word, character for character, from the pulled transcript. They are highlight handles. If a single word is paraphrased, dropped, or reordered, the highlight will not match and the clip fails.
- CLIP IN must appear earlier in the transcript than CLIP OUT, and the span between them is the clip.
- If the transcript carries timestamps, add a numeric Timestamp range (MM:SS to MM:SS) from the first-word time of the CLIP IN and CLIP OUT lines. Never guess a timestamp. If the transcript has no times, write the anchors only and say the times were not available.
- Keep clips tight: open on the objection or the first move in the sequence, close on the resolution or the decision. A teaching clip is usually 30 seconds to about 3.5 minutes. When the rep stacks several steps, the clip may run to the longer end so the whole sequence is captured, but cut any dead tangent by choosing the tightest continuous span that still shows the sequence.

---

## Step-sequence and titling rules (accuracy-critical)

- Score and label the FULL step sequence the rep runs in or around the clip (Foundation, Step 1 through Step 4), not only the single headline step. If the rep stacks multiple steps, the clip and the SAY THIS FIRST must showcase the whole run and name each step.
- Every clip gets a **Clip title** (the snippet name) and, when available, a **Timestamp** range. The title format is: `[type] · [steps shown] — [teachable beat] (rep, objection)`, for example `GREAT DEMO · Reframe -> Self-Close — "what number would you sign up at?" (Vidush, price)`.
- The **SAY THIS FIRST** is two sentences David reads aloud before playing the clip. If the rep ran multiple steps, name the sequence and celebrate it. If the rep nailed only one step, or it is a MISSED OPPORTUNITY where the rep started right, explicitly say they started it right and name the exact step to EXPAND on next time.

---

## Accuracy gate (run before delivering anything)

Before producing the final cards, verify every card against the transcript and drop any card that fails:

1. **Anchor fidelity:** locate CLIP IN and CLIP OUT in the actual transcript text. Both must be exact verbatim matches, and CLIP IN must come before CLIP OUT. If either fails, fix the anchor or drop the card.
2. **Rep attribution:** confirm the rep was identified by behavior, and that the lines in the clip are actually the rep's lines. If the clip's key line is the lead's, fix or drop.
3. **Eligibility match:** GREAT DEMO must be on a CLOSED call with the named step at a genuine 2. MISSED OPPORTUNITY must be on a NO-CLOSE call with the named step at a 0. If the call is UNCERTAIN on close status, drop the card.
4. **Strictness:** the "2" must be the prescribed matrix move for that specific objection, not discounting, a guarantee, social proof, or urgency. If it is not, it is not a Great Demo.
5. **Step match:** the steps named in the title and in "Steps in this clip" must be the steps actually demonstrated or missed in the clipped span. The WHY line must quote or paraphrase the actual rep language in the span.
6. **No manufacturing:** if a candidate only half-fits, cut it. State that fewer than the requested number were found rather than stretching the bar.

Only cards that pass all six ship.

---

## Output format (one card per clip)

```
Clip title:     [type] · [steps shown] — [teachable beat] (rep, objection)
                e.g. GREAT DEMO · Reframe -> Self-Close — "what number would you sign up at?" (Vidush, price)

[CLIP TYPE] — [STEP SEQUENCE shown] (executed | missed)

Rep:            [identified by behavior, not the transcript label]
Call:           [lead name / call subject]
Close status:   [CLOSED | NO CLOSE]
Maps to:        [one of the 16 objections, or general]
Timestamp:      [MM:SS to MM:SS, or "not available"]
Steps in this clip:  [every matrix step the rep runs in or around the clip with its score,
                      plus steps run earlier in the call and steps skipped]

CLIP IN  (highlight starts here): "[verbatim words]"
CLIP OUT (highlight ends here):   "[verbatim words]"

SAY THIS FIRST: [two sentences David reads before the clip. Celebrate the full sequence if the
                 rep ran multiple steps. If only one step landed, or a missed clip where the rep
                 started right, say they started it right and name the step to EXPAND on next.]

WHY: [one line tied to the steps shown: what the rep did, or failed to do]
```

Title examples:
- GREAT DEMO · Acknowledge -> Reframe — moving the price 6 months forward (Tom, price shock)
- GREAT DEMO · Self-Close through a spouse stall — "Shall we get you started?" (Tom)
- COACH · Stopped at Step 1 — clarified the money objection, then capitulated (Vidush)
- COACH · Got the 11-out-of-10 buying signal, skipped the close (Tom)

Open the run with a one-line summary: how many consultations were scanned, how many closed vs no-close, and how many clips made the bar. Then the cards, Great Demos first. Then a one-line operator note of anything that could not be pulled.

## Tone and standards

- Never use em dashes anywhere. Use commas, periods, or parentheses.
- No emojis. Do not put emojis after rep names.
- No tables. Bold headers and hyphen bullets only.
- Ground every WHY and every SAY THIS FIRST in what was actually said in the clipped span.

---

## Delivery

Default (scheduled or "send it"): send to the director's own Slack DM with `chat.postMessage` on the WFS Group workspace bot token (Slack MCP connector, or a direct POST to https://slack.com/api/chat.postMessage with header `Authorization: Bearer $SLACK_BOT_TOKEN`), `channel` set to the director's Slack member ID (DIRECTOR_SLACK_ID U0BUZ6C0C91). Send the run summary as message one and the cards as message two. Split at a card boundary, never mid-card, only if a message would exceed about 5000 characters.

On-demand in a chat ("find me clips" while working together): show the cards inline in the conversation instead of the DM, unless David asks for the DM.

Optional: to log a clip as a formal call-review note, write it straight to the review tracker yourself (a Pipedrive note on the matching deal, or the coaching ledger the `sip-watch-loop` skill maintains) with the call, the rep, a summary and a rationale. The old proposal queue lived inside the retired Director Console, so there is nothing to approve any more: the write is the record. This does not replace the Slack delivery.

The snippet itself is still created by hand where the recording lives: open the call, highlight from CLIP IN to CLIP OUT, create the snippet, and name it with the Clip title. The skill's job is to make that highlight unambiguous and correct.

---

## Scheduled run (weekly)

When the scheduled task fires, call `list_meetings` over the last 7 days, rank the candidates per CANDIDATE RANKING (cap 50), pull each kept candidate with `get_meeting_transcript`, score the full step sequence strictly against the rubric, pass every card through the accuracy gate, and deliver to the Slack DM unattended. The Avoma and Slack connectors must be authorized in the task context. If a run returns no calls or cannot send, surface that as the failure rather than delivering an empty or padded report.
