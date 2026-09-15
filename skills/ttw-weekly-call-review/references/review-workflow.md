# Multi-agent review workflow and QA gates

Accuracy is the point of this report. This process exists because every shortcut has been tried and measured, and each one produced wrong numbers.

## What the measurements showed

| Approach | Result when checked |
|---|---|
| Single-pass grading | ~30% of rows wrong |
| One reviewer, then an audit | audit itself 30% wrong |
| Adversarial-only pass ("knock these down") | knocked down 42%, a neutral judge then rejected half |
| Two blind reviewers + neutral adjudication | 86% agreement, disagreements resolved on evidence |

The last row is the process. Use it.

**The key insight:** two reviewers given the same rules can agree with each other and both be wrong, because they share the rule's blind spot. That is why the challenge pass exists, and why the challenge pass must itself be adjudicated by someone neutral.

## The process

### Pass 1 — Blind independent grading

Split the calls into batches of about 10 and run one agent per batch, in parallel. Each agent gets **only** the call_id, lead name hint, rep name, date, duration and call type. **Do not give them any prior classification, prior evidence, or another reviewer's notes.** Blindness is what makes the agreement rate meaningful.

Each agent: verifies transcript completeness, reads the full call, reads the five minutes after the price word by word, and returns bucket, verbatim lead evidence with timestamp, evidence type, confidence, transcript source, character count, and flags.

Run this twice, with different agents, to get two independent verdicts per call. Alternatively, on a re-grade, use the existing classification as reviewer A and run one blind pass as reviewer B.

### Pass 2 — Neutral adjudication of disagreements

Every call where the two reviewers differ goes to a third agent that sees **both** verdicts and both pieces of evidence, with explicit instruction that neither reviewer gets deference and both have been wrong before.

The adjudicator must also check that each side's quote actually exists and means what it claims. On the last run, adjudicators found 12 cases where one reviewer misquoted and 5 where the other did: cropped quotes that reversed meaning, timestamps past the end of the call, and the rep's line attributed to the lead.

### Pass 3 — Adversarial challenge on RED and ORANGE

Run every RED and ORANGE past a challenger whose job is to knock it down, hunting the ten failure modes in `bucket-definitions.md`.

**Never apply challenge results directly.** The challenger knocks down about 42%; a neutral judge upheld only half of those. Route every proposed knockdown through a neutral adjudicator that sees both readings and is explicitly warned about both traps: the mechanical read that treats any money-adjacent sentence as poverty, and the over-correction that treats any capacity-adjacent sentence as solvency.

### Pass 4 — QA gates

Run these programmatically before reporting anything. Each must pass.

1. **Row count** matches the pull, minus stated exclusions. No duplicates by call_id.
2. **Every RED and ORANGE has non-empty evidence.** Zero exceptions.
3. **Every GREY has exactly** `"No financial reference on the call"` and evidence_type `none`. A GREY carrying real evidence text is a contradiction.
4. **Bucket totals sum to the row count.**
5. **Closes reconcile**: the count of `closed_full` + `closed_base44` equals BLUE + ORANGE. A mismatch means a row's outcome and bucket disagree; fix it before publishing. This caught a real error where a lead was counted as a close although nothing was funded.
6. **Rep names** resolve for every row; none left as UNKNOWN.
7. **Dates** all fall inside the stated window.
8. **Rep scores** are blank or 1 to 10; no zeros standing in for missing.
9. **Evidence timestamps** fall within the call duration. A timestamp past the end means the quote came from a different call.
10. **Verification coverage** is recorded per row and reported in aggregate.

### Pass 5 — Spot-check against the requester

Surface the two or three rows the reviewers marked lowest confidence, with their evidence, and ask directly. The director has caught real errors this way three separate times. Their instinct on a specific lead is worth more than another automated pass.

## Agent prompt skeletons

**Blind reviewer:**
> You are one of two independent reviewers. You are deliberately not being told how this call was classified before. Verify the transcript is complete, read it in full, then read the five minutes after the price word by word. Classify per the bucket rules and return your verbatim lead evidence with timestamp. Accuracy matters more than speed. Do not inflate anything.

**Neutral adjudicator:**
> Two reviewers classified the same call differently. You are the tiebreaker and you have no thumb on the scale. Neither gets deference; both have been wrong before. Check that each side's quote actually exists and means what it claims. Rule from the transcript.

**Adversarial challenger:**
> Every row you have is currently RED or ORANGE. Your job is to try to knock it down, hunting the listed failure modes. Do not knock one down without a verbatim lead quote that proves capacity or proves the constraint was administrative. Upholding is a good outcome.

## Practical notes

- Batch about 10 calls per agent. More than 15 risks context pressure and skimming.
- Launch batches in parallel in a single message.
- If the API returns 529 overload, retry in smaller waves. Do not fall back to grading them yourself in one pass and call it verified; say plainly what got the full treatment and what did not.
- Record per row how it was verified: `two reviewers agreed`, `adjudicated by third reviewer`, `survived adversarial challenge`, `challenged then neutrally adjudicated`. Put it in a Verification column so anyone reading knows which rows are solid.
