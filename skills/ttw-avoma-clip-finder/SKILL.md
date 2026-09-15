---
name: ttw-avoma-clip-finder
description: Finds sales coaching clips from TikTok Wiz consultation calls by scoring how reps run the Decision Leadership Objection Matrix, then giving Caydo exact clip-in and clip-out anchors so the snippet is one click. Pulls call data from the Lovable WFS connector (calls_find_review_candidates, calls_get_analysis). Use when Caydo wants weekly clips, objection-handling clips, Great Demo or Missed Opportunity clips, or says "find this week's clips", "find clips", "run the clip finder", "find me 3 clips", or "who handled objections well this week", and when the weekly scheduled task fires. Always use it even when the request sounds simple, because rep identification, close vs no-close detection, the strict eligibility gate, and the verbatim anchor rule carry accuracy rules the output depends on.
---

# TTW Clip Finder (Lovable WFS)

Finds teachable clips from TikTok Wiz consultation calls by scoring how a rep ran the Decision Leadership Objection Matrix, then delivers exact verbatim clip boundaries so Caydo can create the snippet in one highlight.

Data source: the **Lovable WFS connector**. Two tools do the work:
- `calls_find_review_candidates` returns the ranked calls to review (params: `brand` optional, `days_back` default 7 max 30, `limit` default 10 max 50). It already ranks by deal value, lead-score gaps, low rep score, and recency, so there is no manual pagination.
- `calls_get_analysis` (param: `call_id`) returns, for one call, a 25-point scorecard, financial signals, close attempts, downsell, lead bucket, and the speaker transcript.

Target: 3 clips per week by default (Caydo may ask for a different count or mix, for example "3 good examples and 2 improvement points"). Two clip types, and the type controls which calls are even eligible:

1. **GREAT DEMO** comes ONLY from a call that CLOSED, where the rep executed a named matrix step well. The "watch how it is done" clip.
2. **MISSED OPPORTUNITY** comes ONLY from a call that did NOT close, where a clear objection trigger fired and the rep failed to run the step the moment called for. The "here is where we lost it" clip.

A clean close with no objection is correctly NOT clipped. A no-close where the rep ran the flow well is a talking point, not an auto-clip. Never manufacture a clip to hit the number. Three real clips beats five forced ones, and a forced clip teaches the team the wrong lesson.

Score STRICTLY. A step counts as executed only if the rep ran the PRESCRIBED move with the right talk track for that SPECIFIC objection (permission-ask before a reframe, root-relabel on acknowledge, motive-tied consequence and future pace, a clean self-close that produces the decision). Discounting, guarantees, social proof, urgency, and feature dumps do NOT count as matrix moves, even when the call closes.

The closers are Vidush Rana, Tom Judson, Crue Lindgren, Turok Tarango, Paul Rasoumoff, and Ky Newton. The setters are Petros Foustanellas, Antonio Vespa, Aidan Stammers, Saray Cortes, and Brittany Acton.

The full scoring rubric, the 16 objections, the per-step 0-1-2 markers, and the card format live in `references/decision-leadership-rubric.md`. Read that file before scoring. This SKILL.md is the workflow and the accuracy rules that protect the output.

---

## Step 1: Establish the window

The window is expressed as `days_back` on `calls_find_review_candidates`.
- Default weekly run: `days_back=7`.
- "today and yesterday": `days_back=2`. "this week": `days_back=7`. "last two weeks": `days_back=14` (max 30).
- Caydo is in Lehi, Utah (Mountain Time). If he names calendar dates, translate them to the smallest `days_back` that covers them and then drop anything outside the range after you pull.
- If Caydo asks for one brand or one rep, pass `brand` and filter to that rep after the candidates come back.

## Step 2: List the calls to review

1. Call `calls_find_review_candidates` with the chosen `days_back` and `limit` (use `limit=50` for a full weekly sweep, smaller for a tight window). Pass `brand` if Caydo named one.
2. The response is already ranked and each candidate carries a `call_id` (uuid) used in the next step. There is no pagination to manage.
3. If Caydo asked for a specific rep, keep only candidates for that rep.

## Step 3: Filter to scoreable consultations (STRICT)

The connector surfaces review candidates, but still confirm each is a real closer consultation before scoring:
- It is a closer **Consultation**, not a setter Introduction / intro call. The matrix does not apply to setter intros.
- It has a usable speaker transcript in `calls_get_analysis`. No transcript means nothing to score.
- It is a real, full-length pitch call, not a no-connect, voicemail, or reschedule. A long call is not proof of a real consultation, confirm from the transcript end-state.

Keep a short operator list of what got dropped and why. It does not go in the output.

## Step 4: Reliability and the incomplete-run rule

The connector can time out or error intermittently. For every call:
- Retry a failed or timed-out `calls_find_review_candidates` or `calls_get_analysis` at least twice before giving up. The same `call_id` often succeeds on a retry.
- If the connector throws an auth error, tell Caydo his Lovable WFS connector needs re-approving, then continue once it is back.

Never silently drop a scoreable call. If an analysis cannot be pulled after retries, note it in the output as not yet scored rather than omitting it.

## Step 4b: Large transcripts (context safety)

`calls_get_analysis` returns the full speaker transcript inline, and for a long consultation that payload can exceed the inline token limit and be saved to a file instead. When that happens, do NOT read the whole file into the main context. Hand the saved file path to a subagent and have it score the call against the rubric and return only the findings: rep by behavior, close status with the end-state quote, the per-step scores with verbatim evidence, and the candidate clip with verbatim CLIP IN / CLIP OUT anchors plus the timestamp of each anchor if the transcript carries timestamps. This keeps the full transcript out of the main context while preserving verbatim accuracy.

## Step 5: Pull and read each analysis

1. For each kept candidate, call `calls_get_analysis` with its `call_id`.
2. Score the matrix from the SPEAKER TRANSCRIPT, never from the scorecard summary alone. The transcript is where the permission ask, the relabel, the future pace, and whether the rep folded actually live.
3. Use the analysis extras as cross-checks, not as the score: the 25-point scorecard, the `close attempts`, the `downsell` signal, and the `lead bucket` all help confirm close-vs-no-close and where the friction was, but the matrix score and the clip come from the transcript.
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
5. Rank candidates and select the requested number (default 3), aiming for a spread across different steps and reps. If Caydo asks for a specific mix (for example good examples plus improvement points), honor it. If real candidates are thin, deliver fewer and say why. Do not pad. If the calls that closed did so by breaking the matrix (discount, guarantee, urgency), say that plainly rather than dressing one up as a Great Demo.

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
- The **SAY THIS FIRST** is two sentences Caydo reads aloud before playing the clip. If the rep ran multiple steps, name the sequence and celebrate it. If the rep nailed only one step, or it is a MISSED OPPORTUNITY where the rep started right, explicitly say they started it right and name the exact step to EXPAND on next time.

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

SAY THIS FIRST: [two sentences Caydo reads before the clip. Celebrate the full sequence if the
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

Default (scheduled or "send it"): send to Caydo's own Slack DM with `slack_send_message`, `channel_id` set to his user ID `U092C85GA4D`. Send the run summary as message one and the cards as message two. Split at a card boundary, never mid-card, only if a message would exceed about 5000 characters.

On-demand in a chat ("find me clips" while working together): show the cards inline in the conversation instead of the DM, unless Caydo asks for the DM.

Optional: to log a clip as a formal call-review note for the Director to approve, use the Lovable WFS `calls_propose_review_note` tool (needs `call_id`, `rep_id`, a `summary`, and a `rationale`). This does not replace the Slack delivery, it is for when Caydo wants the note written to the review tracker.

The snippet itself is still created by hand where the recording lives: open the call, highlight from CLIP IN to CLIP OUT, create the snippet, and name it with the Clip title. The skill's job is to make that highlight unambiguous and correct.

---

## Scheduled run (weekly)

When the scheduled task fires, call `calls_find_review_candidates` with `days_back=7` and `limit=50`, pull each candidate with `calls_get_analysis`, score the full step sequence strictly against the rubric, pass every card through the accuracy gate, and deliver to the Slack DM unattended. The Lovable WFS and Slack connectors must be authorized in the task context. If a run returns no calls or cannot send, surface that as the failure rather than delivering an empty or padded report.
