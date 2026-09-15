# Decision Leadership Objection Matrix: Clip Scoring Rubric (v3)

Powers the ttw-avoma-clip-finder. Surfaces two clip types from real consultation calls.

1. GREAT DEMO clips come ONLY from calls that CLOSED where the rep actually executed a matrix step well. Teaching clips.
2. MISSED OPPORTUNITY clips come ONLY from calls that did NOT close where a clear trigger fired and the rep failed to run the step the moment called for. Coaching clips.

Built to be read off the Avoma call transcript (from `get_meeting_transcript`). Tone still needs a human gut check on the final shortlist, but every marker below is detectable from words.

---

## Part 0: Three things the runs proved (read first)

1. Speaker labels are NOT reliable. On real calls Avoma labeled the rep's lines with the lead's name. Identify the rep by behavior (shares screen, runs the pitch, drops the Clarity Pay or Affirm link, onboards), never by the transcript name label. Every score attaches to the rep identified this way.

2. Most calls that close cleanly contain no matrix objection at all, because the lead self-qualifies and is already a 10 before price. Do not manufacture a clip where there is no moment. The richest objection material lives in calls with friction, which is why Missed Opportunity is gated to no-close calls. Closes that contain a cleanly executed matrix move are rarer than no-closes, so finding Great Demos usually means scoring more calls.

3. Reps run SEQUENCES, not single steps. A good rep stacks acknowledge, then reframe, then self-close, and a missed clip is often a rep who started the sequence right (a clean Step 1) and then dropped it. Always map every step in the run, not just the headline one. The teaching value is in showing the whole sequence, or in showing exactly where a started sequence was abandoned.

---

## Part 1: Timestamps and how the clip boundary is defined

The Avoma transcript pull returns speaker-labeled text with per-word timestamp arrays on each segment. The 100% accurate clip boundary is verbatim anchor text:
- CLIP IN: the exact words where the highlight starts.
- CLIP OUT: the exact words where the highlight ends.

In Avoma you create a snippet by highlighting transcript text, and Avoma maps that highlight to the exact recording frame automatically. The anchor text is therefore the source of truth, tighter than any number.

Each clip ALSO carries a numeric Timestamp range (MM:SS to MM:SS), read from the first-word timestamp of the CLIP IN segment and the CLIP OUT segment. Never guess a timestamp. The anchors stay the primary boundary, the numbers are the convenience.

---

## Part 2: When to evaluate (trigger detection)

An evaluable moment starts the instant the prospect voices resistance, hesitation, a stall, or a price or risk concern. Surface triggers mapped to the 16 objections:

- Stall or certainty: think about it, not sure, get back to you, sit with it, don't make decisions on the spot, need 24 hours, need a few days
- Authority: talk to my spouse, talk to my partner, run it by, ask my husband or wife
- Price or money: too expensive, can't afford, don't have the money, go into debt, put it on credit, cheaper with, found it cheaper
- Risk or proof: success rate, what if it doesn't work, saw bad reviews, is this legit
- Time: don't have time, timing isn't right, too busy, not the right time
- Logistics: can't schedule, can't do a follow up

Also treat any objection-shaped pushback as a trigger even if it does not match a named objection. The trigger marks the START of a clip. The END is the prospect stating a decision or the rep abandoning the thread.

---

## Part 3: Close vs no-close detection (eligibility gate)

Avoma outcomes are untagged on these calls, so read the transcript end-state.

CLOSED signals: deposit taken, Clarity Pay or Affirm funding or deposit confirmation, "you're in", onboarding call scheduled, course or Discord access granted.

NO-CLOSE signals: declined or no deposit, "I need to think about it", "talk to my spouse", "I'll get back to you", a follow-up booked instead of a sale, or no payment attempt at all. A declined deposit of any amount is a no-close.

---

## Part 4: The scoring rubric

Score the Foundation once per call. Score Steps 1 through 4 per objection handled. Each item is 0, 1, or 2. Record EVERY step the rep runs in the sequence, not only the headline step.

### Foundation: Discovery / Identity Anchor (scored once per call)
Good looks like: earlier in the call the rep asked a future-pacing identity question (one of the three 2.0 versions) and captured a specific, reusable future identity, ideally with the Identity Anchor follow up ("if that version of you was in this chair, what advice would they give you").
- 2 = future identity question asked AND a specific reusable answer captured
- 1 = a vision question asked but shallow, no concrete identity captured
- 0 = no identity discovery
Detect: "a year from today", "12 months from now", "who would you have to become", "what had to change for that to be true", "what advice would that version of you give you", then check for a concrete answer.

### Step 1: Acknowledge & Clarify
- 2 = acknowledged calmly AND asked a genuine clarifying question AND relabeled surface to root ("so it is not really about time, it is about certainty")
- 1 = acknowledged OR clarified but took the objection at face value
- 0 = got defensive, rebutted, justified price, or ignored it
Green: "totally fair", "that is a fair question", "help me understand", "tell me more", "what is behind that", "what specifically", "would it be fair to say the real concern is not X it is Y".
Red: instant "well actually", feature dump, defending price before asking anything.

### Step 2: Reframe
- 2 = asked permission AND delivered a real reframe AND the prospect agreed or shifted
- 1 = reframe with no permission, OR permission with a weak reframe
- 0 = no reframe, steamrolled or capitulated
Green: "can I offer another perspective", "would it be okay if I challenged that", "if you knew with certainty this would work would X still be your concern", "does certainty create action or does action create certainty".
Red: arguing without permission, conceding, changing the subject.

### Step 3: Consequence + Future Pace
- 2 = cost of inaction tied to their motive AND commitment bridge AND future pace tied to their captured identity
- 1 = some consequence framing but generic, or consequence with no future pace, or substituting a guarantee or proof stats for a true cost-of-inaction
- 0 = no consequence or future pace, jumped to a discount or to "when should we follow up"
Green: "if another year passes and you are still dealing with", "what does that cost you", "how does that affect your goal of", "is that a future you are willing to settle for", "are you sure, why not", "the version of you that already achieved the goal, what would they do".
Red: discount as the first move, "no worries let us circle back".

### Step 4: Self-Close
- 2 = clean self-close question AND the prospect states the decision
- 1 = closed but did it for them or led them to it
- 0 = no close, defaulted to a follow up
Green: "what do you want to do from here", "where do you want to go from here", "what number would you sign up at", "shall we get you started", then the prospect answers.
Red: assuming the close, hard pressure, or no close attempt.

---

## Part 5: Clip routing (eligibility is strict)

### GREAT DEMO clip
ALL of:
- Call CLOSED
- At least one named step was executed at a 2 (the rep ran the move and it landed)
- Clean arc from trigger to resolution
Showcase the full sequence the rep ran (for example acknowledge then reframe then self-close), not just the single peak step.

### MISSED OPPORTUNITY clip
ALL of:
- Call did NOT close
- A clear trigger fired
- The named step scored 0 (the rep failed to run the move the moment called for)
Often the rep started the sequence right (a clean Step 1) and then dropped it. Show where the sequence was abandoned.

Anything that closed with no objection is correctly NOT clipped. Anything that did not close but where the rep ran the flow well is a discussion point, not an auto-clip.

---

## Part 6: Output format (one card per clip)

Title the clip first, then name the clip type AND the step sequence shown, with executed or missed.

```
Clip title:     [type] · [steps shown] — [teachable beat] (rep, objection)

[CLIP TYPE] — [STEP SEQUENCE shown] (executed | missed)

Rep:            [identified by behavior, not the transcript label]
Call:           [meeting subject]
Avoma link:     [meeting url]
Close status:   [CLOSED | NO CLOSE]
Maps to:        [one of the 16 objections, or general]
Timestamp:      [MM:SS to MM:SS]
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
- GREAT DEMO · Reframe -> Self-Close — "what number would you sign up at?" (Vidush, price)
- GREAT DEMO · Acknowledge -> Reframe — moving the price 6 months forward (Tom, price shock)
- COACH · Stopped at Step 1 — clarified the money objection, then capitulated (Vidush)
- COACH · Got the 11-out-of-10 buying signal, skipped the close (Tom)

The only manual step left is opening the Avoma link, highlighting from CLIP IN to CLIP OUT, clicking Create Snippet, and naming it with the Clip title.

---

## Part 7: Honest limits

- Transcript catches words, not tone. The phrase markers are starting signals. Human gut check the final shortlist before posting.
- Reps who run the flow in their own words still count. Reward the move (acknowledge, clarify, relabel, permission, reframe, consequence, future pace, self-close) over exact phrasing.
- Foundation is scored once per call, and its absence caps Step 3, because you cannot future pace to an identity you never captured.
- Map the whole sequence. The most useful clips either show several steps stacked correctly, or show a rep who opened the sequence right and then stopped.
