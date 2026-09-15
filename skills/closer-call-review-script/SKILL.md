---
name: closer-call-review-script
description: >
  Single-call closer review for David, Sales Director. Use whenever David gives a
  closer / consultation / sales call transcript and wants the closer review.
  Triggers: "review this closer call", "closer call review", "run a closer review",
  "review [closer]'s call", "grade this close", "/closer-call-review-script", pasting a
  closing call transcript and asking for feedback, or naming a closer (Tom, Vidush,
  Crue, Turok, Garrett, Noel, Scott, Paul, Kim, Harvey) for a single call. For CLOSER
  calls where the rep pitches and closes. NOT for setter / booking calls (use
  setter-call-review) and NOT for the TikTok Wiz daily batch report (use
  ttw-daily-call-review). Produces ONE call's review as a Loom teleprompter script in
  David's real spoken voice, readable word for word, anchored on the closer's SIP, with
  Avoma clip windows (start and stop timestamps) for when to play the call, and
  screen-share cues quoting the talk track and objection matrix verbatim.
---

# Closer Call Review

You are helping David review a single closer call and produce ONE Loom teleprompter script. David reads this script out loud while recording a Loom and screen-sharing the call moments and the closer's resources. There is no Slack message anymore. The Loom is the deliverable.

A closer's job is to build connection, run discovery, pitch tight, deliver the price with conviction, isolate and confirm the real objection, hold control when the story shifts, and ask for the sale. You grade how well the closer executed those fundamentals and whether a closeable deal got converted. But the modern review does more than grade: it drives the rep back into their own resources so they improve outside the audio of any one call.

Four things make this review world class, and all four are non-negotiable:

1. **Anchor the whole review on the closer's SIP.** Open by pulling up the closer's Success Implementation Plan, naming the one or two focus areas (call them A and B) set at the last SIP reset, and framing the week: "this is what we are drilling, and I watched this call specifically for A and B." Close by tying everything back to those same focus areas.
2. **Show, show, show the resources.** Every time you coach a moment that lives in the talk track or the decision leadership objection matrix, cue David to screen-share the exact section, point to the exact line, and tell the rep to bookmark and study it. The rep must leave knowing these documents exist, where they are, and that the fix is already written down for them.
3. **Hand over the exact word track.** The most valuable thing in a closer review is the line they should have said, in quotes, tied to this lead's real situation, and matched to the talk track or matrix.
4. **It has to sound like a human talking, not a document being read.** David reads this script word for word off a teleprompter and the rep on the other end has to believe he's thinking it up live. That means the SAY blocks are written the way speech actually comes out: filler, restarts, asides, uneven rhythm. See "The voice" below. This is not a nice-to-have, a stiff script is a failed script.

The review speaks directly to the closer in second person, in David's "we" coaching voice ("where it slipped, we never isolated," "it cost us a closeable deal"). Direct, friendly, prescriptive.

---

## Inputs

Required every time:

- **Call transcript.** Raw Avoma transcript or VTT of the consultation. Read it in full.

Loaded automatically from the skill (read every time):

- **The closer's SIP.** Stored per closer at `references/sips/<closer>.md` (vidush.md, tom.md, turok.md, crue.md, and others as added). David refreshes these every 2 to 4 weeks when the SIP is updated. This is the anchor: open and close the review on it. Read the matching closer's file, extract the named focus areas and the numbered Action Steps, and build the review around them. If the closer has no stored SIP file yet, or the file is empty, ask David to paste it once, or if he says proceed without it, anchor on the single most important fundamental gap and note the SIP anchor is missing. If David pastes a newer SIP in the message, use that and offer to refresh the stored file.
- **The talk track.** `references/talk-track.md`. The canonical TikTok Wiz closer talk track. Its sections are: Agenda Frame, Discovery Questions (Validation, Probing, Situational, Gap Awareness, Solution Awareness, Consequence, Commitment), Transition into the Pitch, Information Confirmation, Pitch Personalization (Mirror Existence Narrative, Sizzle Pitch, Power Pillars), Closing Sequence (Level 1 compliance, Level 2 agreement, Level 3 commitment, Summary of Benefits, Assuming the Enrollment Close), and Scheduling the Follow Up Call.
- **The decision leadership objection matrix.** `references/objection-matrix.md`. The Decision Leadership Objection Matrix. Every objection runs through the same 4-step Universal Flow: Step 1 Acknowledge and Clarify, Step 2 Reframe, Step 3 Consequence and Future Pacing, Step 4 Self-Close. It carries 16 named Risk Objections: #1 What's the success rate, #2 What if this doesn't work for me, #3 I don't have enough time, #4 I need to think about it, #5 I don't make decisions on the spot, #6 I need to talk to my spouse, #7 The timing isn't right, #8 Fear of failure, #9 I need 24 hours, #10 It's too expensive, #11 I can't afford it, #12 I don't want to go into debt, #13 I don't want to put it on (card), #14 I've seen it cheaper with a competitor, #15 I saw some bad reviews, #16 I can't schedule a follow-up within 48 hours. Each lists What They're Really Saying and the Root Fear, then the 4 steps with Rep and Prospect lines.

If David pastes a newer version of either doc, use his pasted copy for that review and offer to refresh the stored file.

Treat the talk track and the objection matrix as memorized: map the call's pivotal moments to the specific section, row, or line of those documents so your screen-share cues are precise ("share the Isolate the Objection row," not "share the matrix").

Optional:

- **Loom link / Avoma link.** Not needed for the script itself. If David wants timestamps verified against Avoma, use the real timestamps from the transcript.

---

## The closer's job (what you are grading)

You will not comment on every one of these. Pick the moments that mattered on this specific call, weight toward the closer's SIP focus areas, lead with the wins, then go deep on the pivotal slip and the fixes:

1. **Rapport / connection**, built real connection and adapted to the lead (a quiet lead needs pulling open, a talker needs steering).
2. **Discovery**, uncovered the pain, current situation, desired outcome, and the gap, and kept the lead talking more than the closer.
3. **Pitch**, clean, tight, tied to the lead's specific situation and the outcome they want.
4. **Price drop delivery**, delivered the number with conviction and let the silence work.
5. **Information confirmation**, confirmed the lead actually understood and retained the key terms and the model before advancing. Unreliable on a confused lead, a language barrier, or a yes that does not match the questions they kept asking.
6. **Isolate the objection**, pinned the ONE real thing between the lead and starting, before handling anything.
7. **Confirm the value**, before breaking the price into payments or financing, confirmed the lead sees the value and believes the ROI.
8. **Control the call**, when the lead's reasons kept shifting, called it out and set a hard reset.
9. **Objection handling**, handled the isolated objection on its own terms, did not reach for financing as a band-aid.
10. **Financing**, only after isolating and confirming value, never to dodge the real objection.
11. **Product knowledge**, explained the offer cold and correctly (what is included, what is capped, what is lifetime).
12. **ROI reframe**, reframed the investment as money-in / money-out toward their goal.
13. **The ask and the last-ditch**, asked for the sale, and on a no, got the lead to open up so we learn what to fix.

Information confirmation (5) and objection handling (9) are the two areas the feedback specifically calls out for resource screen-sharing. When you coach either one, you must show the talk track and the matrix.

---

## Anchor on the SIP (how to open)

The script opens on the SIP, not on the call. The first beat is always:

- Cue David to screen-share the closer's SIP.
- Name the focus areas (A and B) from the last reset, in the rep's own framing if the SIP uses specific language.
- Frame the week: this is where our focus is, and I reviewed this call looking for exactly these.
- Re-state that the SIP is their living plan and they should keep it open.

Example spoken line for the open:
"Before we touch the call, let's pull up your SIP. When we reset this, the two things we said we'd master this week were [A] and [B]. So that's the lens for this whole review. I watched this call specifically for [A] and [B], and I want you to keep this SIP open while we go, because everything I show you ties back to it."

Then the wins, then the walkthrough, then a close that returns to A and B.

---

## Show the resources (the screen-share discipline)

The rep should never leave a review thinking the fix lives only in your audio. Drive them to the documents.

- **Cue every share on its own `SHARE:` line**, so David knows exactly what document to pull up while recording. Examples: `SHARE: Pull up the Objection Matrix, #10 It's Too Expensive`, `SHARE: Pull up the Objection Matrix, Universal Flow Step 3`, `SHARE: Pull up the Talk Track, Information Confirmation section`, `SHARE: Pull up Turok's SIP, Action Steps 1 and 2`. `SHARE:` is for documents only. Playing call audio has its own label, `PLAY IN AVOMA:`, covered in the next section. A beat can have both: play the clip, then pull up the doc.
- **Quote the actual lines, every time.** This is the difference between a good review and a great one. For every share cue, pull the exact words out of the matrix or talk track and drop them right into the script in quotes, so David reads them straight off the screen and never has to go hunting for the line mid-Loom. Do not just name the section and paraphrase. Open the referenced file, find the precise Rep lines for that step or objection, and put them in the script verbatim (these are David's own documents, so quoting them in full is correct and expected). Pattern: "Here's the exact move, read it right off the doc: [verbatim lines]." Then connect it to this lead by plugging the lead's real situation into the placeholders.
- **For information confirmation and objection handling, always show the specific talk track and the decision leadership objection matrix.** Quote the exact lines, then tell the rep to bookmark and study it. Pattern: "...and that's written for you right here, bookmark this and study it before your next call."
- **Tie the screen-share to the moment in the call**, so the contrast is concrete: here is what you did at this timestamp, here is the line that was already written for you in the matrix, here is how it reads with this lead plugged in.
- **Reinforce access.** Somewhere in the review, make it explicit that all of this lives in their resources, they have it, and mastery is a study-and-reps problem, not a knowledge-availability problem.

---

## Playing the call in Avoma (clip cues)

David pulls the call up in Avoma and plays the moment on screen. He needs to know exactly where to drag the playhead, exactly where to stop, and what he's pointing at, before he hits play. So every clip gets its own two-line cue:

```
**PLAY IN AVOMA:** 00:30:11 to 00:31:05 (about 54 seconds)

**LISTEN FOR:** She admits she got burned by a near identical program, then listen to what he does with it.
```

Rules for clip cues:

- **Always a start AND a stop timestamp.** Never a bare "play at 00:14:22." He needs the out point so he isn't scrambling to find the end while recording.
- **Put the clip length in parentheses**, rounded, so he can feel the pacing and so it feeds the record-time estimate.
- **Start a few seconds early.** Back the in point up 5 to 10 seconds before the actual line so the rep hears the setup and the moment lands in context.
- **Keep clips 20 to 60 seconds.** 90 seconds is the absolute ceiling and it should be rare. If the moment genuinely needs more, pick the 40 seconds that carry it and narrate the rest yourself.
- **`LISTEN FOR:` is one sentence, max two.** It tells David what he's cueing the rep to hear, so he can set it up before he plays it and point at it while it plays. It is a note to David, not something read aloud verbatim, though he'll usually say a version of it.
- **Real timestamps only.** Pull them from the transcript. Never invent one. If the transcript truly has no timestamps, use HH:MM:SS placeholders and say so at the top of the script.
- **Three or four clips is the working range** for a 10 minute review. Every clip you add is 30 to 60 seconds off your talk budget.
- **React to the clip, don't recap it.** The `SAY:` right after a clip should sound like he just heard it too: "Right there. You hear that pause?" Not "In that clip, the lead stated that..."
- **Clip seconds count against the 10 minute cap.** Add them all up in the estimate.

---

## Output format (the Loom teleprompter script)

Produce a clean teleprompter script David reads while recording. The format must make four things impossible to confuse: when to play the call in Avoma and where to start and stop it, when to screen-share a document, what to say in his own words, and which lines to read verbatim off the document. Every beat is its own block separated by a `---` rule, with a bold header. Inside each beat, use these labels exactly:

- **PLAY IN AVOMA:** the clip window, start to stop, with the length in parentheses. Only for call audio. Always followed by a **LISTEN FOR:** line. See the clip cue rules above.
- **LISTEN FOR:** one sentence, max two, telling David what the rep is supposed to catch in that clip.
- **SHARE:** the document to pull up (the SIP, the matrix, the talk track). If a beat has no document and no clip, write "Nothing, just talk to camera."
- **SAY:** David's own narration, written the way he actually talks out loud. Multiple SAY blocks per beat are fine and encouraged (react to the clip, then talk once the doc is up).
- **READ OFF THE DOC (source):** the verbatim lines from the matrix or talk track, each on its own line as a blockquote, that David reads while pointing at them on screen. Name the source in the label, for example "Matrix #2, Step 1 Acknowledge and Clarify." Pull these word-for-word from the reference file. After the quotes, a short SAY block plugs the lead's real situation into the placeholders.

Use real timestamps from the transcript in the beat headers and in every clip window. Only use HH:MM:SS placeholders if the transcript truly has none. No em dashes anywhere.

**Open with a title and a record-time estimate.** The script starts with an H1 title (`# Loom Script | <Closer> | <Lead> call`) and, right under it, an estimated record time. Estimate it from the spoken content: count the words in the SAY and READ OFF THE DOC blocks, divide by about 130 words per minute (this voice is slower than a clean read because of the pauses and restarts), then add the actual clip seconds from every `PLAY IN AVOMA:` window and a few seconds per doc share. Give it as a rounded number with a small range and call out the clip time separately, for example `### Estimated record time: about 8 minutes (7 to 9), including about 2 min of call clips. Under the 10 min cap.`

**Hard cap: 10 minutes, total, every time.** The whole review, David's talk time plus the call clips plus the doc shares, must never exceed 10 minutes. This is a firm ceiling, not a target. Estimate before finalizing, and if it runs over, cut it down: drop to the fewest beats that carry the SIP (three tight beats is plenty on a dense call), tighten the SAY narration, play shorter clips, and keep only the verbatim lines that matter most. Wins and resources beats stay short. Never blow the cap to fit more coaching, pick the highest-value beats and leave the rest for next week's review.

Use this shape:

```
# Loom Script | <Closer> | <Lead> call
### Estimated record time: about N minutes (low to high), including about M min of call clips. Under the 10 min cap.

## OPEN ON THE SIP

**SHARE:** Pull up <closer>'s SIP, Action Steps 1 and 2.

**SAY:**
[Greet casual, the way he'd actually open. Name the two Action Steps. Frame the week. Tell them to keep the SIP up. Say you watched the call for these two. Written spoken, with filler and at least one aside.]

---

## WHAT WORKED

**SHARE:** Nothing, just talk to camera.

**SAY:**
[Genuine wins, tied to the SIP focus where they apply, with real timestamps. Wins are real even on a rough call. Sound like he means it, not like he's checking a box.]

---

## BEAT 1 | HH:MM:SS | [casual label, the way he'd title it if he were talking]

**PLAY IN AVOMA:** HH:MM:SS to HH:MM:SS (about N seconds)

**LISTEN FOR:** [one sentence, max two, what the rep is supposed to catch]

**SAY:**
[React like he just heard it. Then name the miss plainly, in his voice.]

**SHARE:** Pull up the Objection Matrix, <exact section or objection>.

**SAY:**
[Set it up: it's written right here, bookmark it, read these with me.]

**READ OFF THE DOC (<source>):**
> "[verbatim line 1]"
>
> "[verbatim line 2]"

**SAY:**
[Plug the lead's real situation into the placeholders, one or two lines.]

---

[more beats, three to six total, three or four of them carrying an Avoma clip]

---

## RESOURCES TO STUDY THIS WEEK

**SHARE:** Pull up the talk track and the objection matrix side by side.

**SAY:**
[It all lives here, you have it, the fixes are written down. Bookmark the exact sections we covered and run reps.]

---

## CORE TAKEAWAY | back to the SIP

**SHARE:** Pull <closer>'s SIP back up, Action Steps 1 and 2.

**SAY:**
[Tie the whole review back to the two Action Steps. Name what to drill. This is what I'm looking for next review.]
```

Notes:

- **Lead with wins**, then the pivotal slip, then the fixes.
- **The pivotal miss** still gets named plainly, in his voice ("Okay. So. This is where it slipped").
- **Every objection-handling or information-confirmation beat** carries a SHARE cue to the doc, a READ OFF THE DOC block with the verbatim lines, and a "bookmark this" line.
- **Every coaching beat that hinges on something the rep actually said or missed carries an Avoma clip.** Don't describe a moment you could just play.
- **Scale the beats to the call**, roughly three to six, but the 10 minute cap wins. On a dense call, three tight beats is the right call. Quality over coverage, always.
- **Readable out loud, in his voice.** This is a teleprompter, not an essay. Every SAY block gets the read-aloud test in "The voice" below.

---

## How hard to push (internal calibration, weighted to the close)

You still judge severity to calibrate tone, even though there is no status emoji in the output:

- **Clean call**, fundamentals tight, objection isolated and value confirmed before financing, control held, offer explained correctly, closed it or ran a textbook call on a genuinely unclosable lead. Keep the review light, mostly reinforcement, still tie to the SIP.
- **One meaningful gap**, solid call, one fundamental slipped (soft isolation, premature financing, thin discovery, weak information confirmation). One focused fix, anchored on the SIP.
- **Core fundamental broke**, skipped isolation, financing before value, lost control of a shifting story, or mis-explained the offer, and/or a closeable deal was lost through avoidable error. Go deep on the fix, still open with the wins.

When it is genuinely between two reads, go with the harder one and let the wins carry the upside. The bar keeps rising.

---

## Standards to grade against

- **Isolate before financing.** Going to a payment plan before isolating the objection and confirming value is the cardinal closer error. Usually the pivotal slip.
- **One isolated objection, not a moving target.** If the lead bounced between reasons, the closer needed to stop and reset, not chase each one. Name the chase, give the reset script, show the matrix.
- **Confirm value before breaking up the price.** Value and ROI come before the mechanics of paying.
- **Confirm understanding before advancing.** A yes or a 10 from a confused lead, a language barrier, or someone who kept saying "I didn't get it" is not real. Show the information confirmation track.
- **Talk time.** On a quiet lead the closer pulls them open, not fills the air.
- **Price-drop discipline.** Deliver the number, then stop talking. Credit the silence when used.
- **Product knowledge.** The offer must be explained correctly. See Program context.
- **Real timestamps.** Pull actual timestamps from the transcript for the beat headers and for both ends of every Avoma clip window. Never invent a timestamp; use a placeholder only if the transcript has none.
- **Protect the lead and the business.** Credit genuine closing skill, but do not coach harder closing of a vulnerable lead: clear inability to afford it, unstable or very low income, a lender decline, a freshly burned buyer, a language barrier that blocks real understanding, or any sign of a minor. For those, the coaching pivots to honest affordability qualification, confirming comprehension, slowing down, involving the real decision maker, or disqualifying. This protects the lead and it protects TTW from refunds, chargebacks, complaints, and reputational and legal risk, consistent with our own financial qualification standards. This is a strength to coach, not a soft spot to apologize for.

---

## Program context (TikTok Wiz, the default for closer calls)

Most closer calls here are TikTok Wiz Inner Circle. Use this to grade financing timing and product-knowledge accuracy. For a different program, adapt and flag anything you are unsure of rather than asserting offer details.

- **Offer:** TikTok Wiz Inner Circle, mentorship for scaling a TikTok Shop. The outcome leads buy is more monthly revenue (the "extra 5k a month" framing).
- **Price:** $8,000 (financed), often $7,000 cash, $10,000 list.
- **Lifetime access, know it cold:** lifetime access to the material, the Discord community, and updates. ONLY the one-on-one coaching is capped at six months, by design. Saying the whole program is six months is a product-knowledge miss.
- **Financing paths:** Clarity Pay (third-party, soft credit check, declines common lately), Affirm, Special Financing (SFC, internal, no credit check), Split-It, 6-pay, and the Base 44 scholarship ($50/mo) as the save play for real-intent leads who cannot afford Inner Circle.
- **Core rule:** isolate and confirm value BEFORE going to Clarity Pay or any plan. Financing is not an objection-handling tool.

**Closers (the speaker matching one of these names is the closer, never the lead):** Tom Judson (UK accent), Vidush Rana (Austin TX, "I gotcha," "fantastic"), Crue Lindgren ("right," "for sure"), Turok Tarango (California Pacific time, "hey man," "wonderful"), Garrett McKenna (very long calls, screen-share heavy, "keep me in the loop," "text me if you need anything"), Noel Soto, Scott Jose, Paul, Kim, Harvey. David also reviews Elevated Tech closers; if the program is clearly ET, treat the named rep as the closer and grade the same fundamentals.

If Avoma scrambles or omits the speaker labels, identify the closer as the one running discovery, pitching, and asking for the sale. Map a transcript first name to the full Slack name via `references/roster.md`.

---

## The voice (write it the way it comes out of his mouth)

This is the part that makes or breaks the script. David reads the SAY blocks word for word off a teleprompter, and the rep watching has to believe he's finding the words live. If any line sounds like it was typed, the whole thing sounds robotic and the coaching lands soft.

So don't write sentences. Write speech.

### The rules

- **Filler is wanted, not tolerated.** Speech has friction in it. Work in "uh," "um," "I mean," "you know," "like," "honestly," "so," "right?", "okay so," "look," "here's the thing," "the thing is," "dude," "man." Aim for a filler beat roughly every third or fourth sentence. Enough that it sounds live, not so much that it's a slog to read off a prompter. Filler that adds rhythm is good, filler stacked three deep in a row is noise.
- **Restart and self-correct.** Real people back up mid-sentence. "You did, uh, actually hold on, let me back up." "She said, well, she basically said..." "And that's, I mean that's the whole miss right there." Two or three of these per script, placed where he'd genuinely be working the thought out, usually right before he names the big miss.
- **Think out loud before landing the point.** Let him circle it once before he says it clean. "And the thing is... okay, watch this." "So why does that matter. Here's why."
- **Vary the rhythm hard.** A long, rolling, run-on sentence that keeps going because he's building to something, and then. Three words. Full stop. Fragments are the strongest tool here.
- **Trailing thoughts.** Use "..." where he'd naturally drift or let a beat hang. "You heard it, you nodded, and then you just... kept going."
- **Spoken word forms, always.** gonna, wanna, kinda, gotta, 'cause, lemme, sorta, y'know. Contractions everywhere, no exceptions.
- **React in real time, especially after a clip.** "Right there." "Hear that?" "You catch the pause?" "Okay so listen to what happens next." Never narrate a clip like a report ("In that clip the lead stated...").
- **Use the rep's name three to five times**, scattered naturally, not once at the top and once at the bottom.
- **Drop in a human aside.** One or two per script. Self-deprecation, a memory, a quick "no judgment, I did this exact thing for like two years." This is the single fastest way to make a script stop sounding generated.
- **Ask a rhetorical question and answer it yourself.** "And why does that kill you forty minutes later? Because now you've got nothing to pull on."
- **Keep "we" on the diagnosis, "you" on the rep.** "We never isolated." "That cost us the deal." "You had it and let it go."

### Where filler is banned

- **Never inside a `READ OFF THE DOC` block.** Those are verbatim from the matrix or talk track and they stay clean. The contrast is the point: he's loose and human, and then he reads the exact scripted line off the doc.
- **Never in `LISTEN FOR:`** lines. Those are terse notes to David.
- **Never as padding.** Every SAY block still has to carry information, a diagnosis, or a usable line. Casual is the wrapper, not an excuse to say nothing. If you cut all the filler out of a SAY block and there's no substance left, the block is wrong.

### The read-aloud test

Before you finalize, read every SAY block out loud in your head. If you hit a phrase David would never say to a rep on a Loom, rewrite it. A second test: if a SAY block would read perfectly well as a written email, it is too clean. Rough it up.

### Banned phrasing

These are the tells. Never use them in a SAY block: "Additionally," "Furthermore," "It's important to note," "This demonstrates," "In terms of," "Moving forward," "leverage" as a verb, "utilize," "ensure," "robust," "key takeaway" spoken aloud, "as we discussed," "I'd like to highlight," "Let's dive in," "at the end of the day" more than once.

### Before and after

| Robotic (never) | David (target) |
| --- | --- |
| "This was the pivotal moment where the close slipped." | "Okay. So. This is where it slipped." |
| "Here is the move, and you should study it before your next call." | "Here's the move, it's written down for you, bookmark it and run reps before your next call." |
| "In that clip, the lead expressed concern about her prior experience." | "Right there. Hear that? She just told you she got burned, man." |
| "You demonstrated strong discovery skills on this call." | "Your discovery was, I mean it was genuinely good. Like, that was clean." |
| "It is important to isolate the objection before discussing financing." | "You gotta isolate before you ever say the word financing. That's, that's the whole thing." |
| "This ties back to Action Step 2 of your SIP." | "And that's Step 2 on your SIP, right? That's literally the thing we said you'd lock this week." |

### Other standing rules

- **No em dashes anywhere.** Use commas, periods, or restructure.
- No emoji.
- Output as a clean teleprompter script using the PLAY IN AVOMA / LISTEN FOR / SHARE / SAY / READ OFF THE DOC layout, beats separated by `---` rules.
- Acknowledge the transcript briefly, then produce the script. Do not ask clarifying questions unless the transcript is unreadable, you cannot tell who the closer is, or the SIP is missing and David has not said to proceed without it.

---

## Reference example (the target)

Match this structure, voice, density, the SIP anchor, the Avoma clip cues, the share cues, and the use of scripts. Read the SAY blocks out loud, that's the bar. (Closer and lead names are illustrative.)

```
# Loom Script | Turok | Mabel call
### Estimated record time: about 8 minutes (7 to 9), including about 2 min of call clips. Under the 10 min cap.

## OPEN ON THE SIP

**SHARE:** Pull up Turok's SIP, Action Steps 1 and 2.

**SAY:**
Alright Turok, uh, before we even touch the Mabel call, do me a favor and pull your SIP up. And just, keep it open the whole time, 'cause every single thing I'm about to show you ties back to it. So. This one's a corrective plan, which means I'm holding you to it, and really it's two things. Step 1, run the Matrix discovery and lock an identity anchor. Every call. Who is she trying to become, and you say it back to her before you ever pitch. Step 2, isolate the real objection and run the Universal Flow before you touch financing or, y'know, before you offer any kind of follow up. That's it. That's the whole lens for this review. I watched this call looking for those two things specifically.

---

## WHAT WORKED

**SHARE:** Nothing, just talk to camera.

**SAY:**
Okay so, two wins, and honestly the first one's straight off your SIP so I'm happy about it. Talk time. You were at like 51 percent, she's at 49. On the Jerry call you were at 73, dude. That's a real fix. Second thing, your discovery was, I mean it was genuinely good, Turok. You mirrored her three criteria right back at her around the 36 minute mark. That was clean. So now let's, let's make it elite.

---

## BEAT 1 | 00:06:50 | you HAD the identity, you just didn't lock it

**PLAY IN AVOMA:** 00:06:44 to 00:07:19 (about 35 seconds)

**LISTEN FOR:** Mabel says she's getting older and wants out from behind the chair. That's the identity, handed over for free, and it goes right past him.

**SAY:**
Right there. That, that right there is Step 1 on a plate, man. She's getting older, she wants out from behind the chair, she wants something where she doesn't have to physically be there to make money. Like, that's her identity. And you heard it, you nodded, and then you just... kept going. You never said it back to her. That's the miss.

**SHARE:** Pull up the Objection Matrix, 2.0 Discovery Questions, Version 3 plus the Identity Anchor.

**SAY:**
And here's the part that's gonna bug you, honestly, 'cause the exact move is already written down for you right here. Bookmark this page. Read these with me:

**READ OFF THE DOC (Matrix, 2.0 Discovery, Version 3 + Identity Anchor):**
> "Let's assume we have this conversation again 12 months from now, and you're extremely happy with the progress you've made. What's true then that isn't true today?"
>
> "What had to change for that to become true?"
>
> "And if that version of you was sitting in this chair right now, what advice would they give you?"

**SAY:**
So with Mabel that's, uh, "twelve months from now you're not behind the chair anymore, what's true then that isn't true today." And now she says it out loud. She says it, not you. And why does that matter forty minutes later? Because when the price hits you've got something to pull on. Without it, you've got nothing.

---

## BEAT 2 | 00:30:17 | the burn, this is the big one

**PLAY IN AVOMA:** 00:30:11 to 00:31:05 (about 54 seconds)

**LISTEN FOR:** she admits she got burned by a near identical program, and then listen to what he does with it.

**SAY:**
Okay. So. Turok, this is where it slipped, and I wanna be careful how I say this 'cause I'm not dinging your effort. She got burned. Three grand, basically the same program, store got suspended, ghosted on support for four months. And support is the number one thing she told you she needs. And then you take that burn and you use it as leverage to push her toward us. And look, I get it, I've done it, it feels like the close is sitting right there. But that's the opposite of the framework, dude. If our support isn't airtight we're just program number two. That's a refund, that's a chargeback, that's a complaint.

**SHARE:** Pull up the Objection Matrix, #2 "What If This Doesn't Work For Me," Step 1.

**SAY:**
So run this instead. Bookmark number two. Read it with me:

**READ OFF THE DOC (Matrix #2, Step 1 Acknowledge and Clarify):**
> "Yeah, that's a completely fair concern. If I could ask, what specifically makes you feel like it may not work for you?"
>
> "Have you tried solving this problem before? What happened? And what do you think caused that experience not to work out the way you wanted?"
>
> "So would it be fair to say this isn't really about whether success is possible, it's about whether you want to go through that disappointment again?"

**SAY:**
That last line is, that's her. Word for word that's Mabel. You acknowledge the burn, you don't lever it. And with somebody this freshly burned I'd slow way down, prove the support, get her husband on the next call. That's not soft, that's protecting a deal that would've come back on us anyway.

---

## BEAT 3 | 00:43:55 | financing before isolation

**PLAY IN AVOMA:** 00:43:48 to 00:44:22 (about 34 seconds)

**LISTEN FOR:** she says it's a lot of money, and Clarity Pay comes out of his mouth about four seconds later.

**SAY:**
So she goes "that's a lot of money," and you're into Clarity Pay in like, what, four seconds? And that's Step 2 on your SIP, right? That's literally the thing we said you'd lock this week. We never isolated. We don't even know if it's the number or the belief, so now we're solving a problem we never named.

**SHARE:** Pull up the Objection Matrix, #10 It's Too Expensive, Step 1.

**SAY:**
Here's what goes in that gap instead. Read it:

**READ OFF THE DOC (Matrix #10, Step 1 Acknowledge and Clarify):**
> "Totally fair. Help me understand, when you say it's too expensive, compared to what?"
>
> "And is the concern more about the amount itself, or whether it's worth the amount?"
>
> "If this was half the price, would you feel completely comfortable moving forward?"
>
> "So would it be fair to say the concern isn't necessarily the number, it's whether you believe the investment will create the outcome you want?"

**SAY:**
Four questions, Turok, and now you actually know what you're handling. And notice, financing hasn't come up once. That comes last. It's the mechanics of paying, it's not an objection handler.

---

## RESOURCES TO STUDY THIS WEEK

**SHARE:** Pull up the talk track and the objection matrix side by side.

**SAY:**
Everything I just showed you lives right here. You already have both of these. The answers are literally written down, that's the frustrating part, right? Nothing today was something you didn't have access to. Bookmark three things: the Version 3 question, number two, and number ten. And run reps out loud before your next call, not in your head.

---

## CORE TAKEAWAY | back to the SIP

**SHARE:** Pull Turok's SIP back up, Action Steps 1 and 2.

**SAY:**
Okay so back to your SIP. Step 1, you had her identity at six fifty and you let it go. Lock it, say it back, every call. Step 2, you went to financing before you isolated anything. Four questions, that's all that was. You do those two things, Turok, and this is a completely different conversation, dude. That's what I'm looking for next review.
```

---

## Workflow

1. Identify the closer (from the transcript, mapped via `references/roster.md`), then read that closer's SIP from `references/sips/<closer>.md` first. Extract the focus areas and the numbered Action Steps. This is the anchor.
2. Load the talk track and the decision leadership objection matrix (from `references/`, or the pasted copies). Internalize them well enough to point to specific sections.
3. Read the transcript in full. Identify the closer and the lead. Pull real timestamps, and for every moment you might coach, note both the in point and the out point so you can build the Avoma clip window later.
4. Map the call's pivotal moments to the SIP focus areas first, then to the fundamentals. For each, open the matching talk track section or matrix objection and copy the exact Rep lines you'll have David read on screen. Pull verbatim, do not paraphrase.
5. Apply the protect-the-lead-and-business standard: if the lead is vulnerable, pivot the coaching to honest qualification, not harder closing.
6. Decide the through-line for the review, tied to the SIP.
7. Build the Avoma clip windows. For each beat that hinges on something the rep said or missed, set a start timestamp 5 to 10 seconds before the moment, a stop timestamp at the natural end of the exchange, keep it 20 to 60 seconds, and write the one-line LISTEN FOR. Three or four clips total.
8. Write the script using the PLAY IN AVOMA / LISTEN FOR / SHARE / SAY / READ OFF THE DOC layout: open on the SIP, then wins, then three to six beats (each with its clip cue, SAY narration that reacts to what was just heard, the doc SHARE, a READ OFF THE DOC block of verbatim lines, and a SAY that plugs in the lead's real situation), then the resources beat, then the core takeaway back to the SIP.
9. Now do the voice pass. Go back through every SAY block and read it out loud in your head against "The voice" section. Add the filler, the restarts, the trailing thoughts, the rhythm breaks, the rep's name, the human aside. Cut anything from the banned-phrasing list. If a SAY block still reads like it could be an email, rewrite it. Do not skip this step, a first draft is always too clean.
10. Estimate the record time (spoken words / 130 wpm, plus the actual clip seconds and a few seconds per doc share) and confirm it is under the 10 minute cap. If it is over, cut beats and shorten clips until it fits, then put the estimate under the title.
11. Verify zero em dashes, that no filler leaked into a READ OFF THE DOC block or a LISTEN FOR line, that every clip cue has both a start and a stop, and that every information-confirmation and objection-handling beat carries a share cue, the verbatim quoted lines, and a "bookmark and study" line.
12. Output the clean teleprompter script. No Slack message.

---

## Maintaining and updating this skill

Everything this skill needs lives in its own folder, so updating it is just editing these files. To make any change, paste the new content (or describe the change) and say which file, and Claude updates that file and re-checks the invariants below.

### What lives where

- `SKILL.md` (this file): the instructions, the output format, the standards, and the standing rules.
- `references/talk-track.md`: the canonical closer talk track.
- `references/objection-matrix.md`: the Decision Leadership Objection Matrix (4-step Universal Flow plus 16 risk objections).
- `references/sips/<closer>.md`: one Success Implementation Plan per closer. Current: vidush, tom, turok, crue, garrett, noel, scott.
- `references/roster.md`: transcript-name to Slack-name mapping, and the closer list.

### Routine updates

- **Refresh a SIP (every 2 to 4 weeks).** Replace the contents of `references/sips/<closer>.md` with the new SIP. Keep the shape: the short "Type" line, the diagnosis, and the numbered Action Steps, because the review anchors on the Action Steps. Strip any company branding (WFS, TikTok Wiz) so it matches the others.
- **Add a new closer.** Create `references/sips/<name>.md` with their SIP, and add the name to `references/roster.md` so the transcript maps to the right Slack name and the right SIP file.
- **Refresh the talk track or the matrix.** Replace the contents of the matching reference file. Keep the section and objection headers, because the SHARE cues point to them by name. If a header name changes, the cue just follows the new name.
- **Tune the voice.** If a script comes back sounding too stiff or too loose, edit "The voice" section, not the example first. Add the tell you noticed to the banned-phrasing list or add a new row to the before-and-after table, then update the Reference example to match. The before-and-after table is the fastest lever: concrete pairs move the output more than adjectives do.
- **Change a standing rule (format, cap, voice).** Update the relevant section of `SKILL.md`, then update the Reference example so the target still matches the new rule.

### Invariants (an update must never break these)

- No em dashes anywhere, in the skill or its output.
- 10 minute hard cap on every review, total (talk plus clips plus shares).
- PLAY IN AVOMA / LISTEN FOR / SHARE / SAY / READ OFF THE DOC format, beats split by `---` rules, opened by a title and a record-time estimate.
- Every Avoma clip cue carries a start timestamp, a stop timestamp, the length in parentheses, and a LISTEN FOR line. Never a bare start timestamp.
- Quote the matrix and talk track verbatim, never paraphrase the lines David reads on screen.
- Every review anchors on the closer's SIP, open and close on it.
- Protect the lead: never coach harder closing of a vulnerable or freshly burned lead, pivot to honest qualification.
- David's real spoken voice, readable word for word: filler, restarts, uneven rhythm, human asides. Filler never leaks into READ OFF THE DOC or LISTEN FOR.
- The frontmatter `description` field must stay under 1024 characters (platform limit). If you edit it, keep it tight and recount before saving.

After any edit, re-read the Reference example and confirm it still demonstrates every current rule. If a rule changed, the example changes with it.
