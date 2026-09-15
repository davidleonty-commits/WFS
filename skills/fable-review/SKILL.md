---
name: fable-review
description: An optimization audit protocol that reviews a skill, scheduled task, automation, prompt, or conversation workflow to find gaps in its logic and reasoning, cut token and tool-call cost without sacrificing output quality, and propose creative upgrades that make the output more world class while staying accurate and reliable. Activate whenever the user says "fable review", "fable optimization", "optimize this skill", "audit this task", "review this workflow", "make this cheaper", "tighten this up", "find the gaps in this", "can this be improved", or shares a skill file, scheduled task prompt, or past conversation and asks for review, improvement, cost reduction, or a second opinion on how it is built. Use it even for casual asks like "any way to improve this?" because unstructured reviews miss the systematic checks this protocol enforces.
---

# Fable Review

## What this skill is

This is an audit protocol. Its job is to take an existing artifact (a skill, a scheduled task, an automation prompt, a workflow, or a whole conversation) and return a prioritized set of concrete edits across three lenses:

1. **Gaps**: places where the logic or reasoning can fail, produce wrong output, or behave unpredictably.
2. **Efficiency**: places where tokens, tool calls, or model effort are being spent without buying quality, and how to cut them.
3. **Elevation**: creative, specific ways the output could be meaningfully better than it is today, without trading away accuracy or reliability.

The output is never vague advice. Every finding comes with a concrete edit the user could apply verbatim, a statement of what the edit preserves, and a risk rating. An optimization report full of "consider adding more clarity" is a failed run of this skill.

The governing law of this skill, stated once and enforced everywhere: **quality and accuracy are the constraint, cost is the objective.** Never propose a cut that degrades correctness, and never propose an upgrade that degrades reliability. When a tradeoff is genuinely unavoidable, present it as an explicit option with both sides priced, never as a recommendation smuggled through.

---

## Phase 1: Intake. Understand what you are auditing.

**Identify the artifact type**, because each type has different failure modes and cost profiles:

- **Skill file** (SKILL.md and bundled resources): cost lives in context size and triggering behavior; gaps live in ambiguous instructions and unhandled cases.
- **Scheduled task or automation prompt**: cost lives in tool calls, retries, and model tier; gaps live in missing failure handling, race conditions with source data, and delivery mistakes.
- **Conversation or workflow transcript**: cost lives in repeated context, redundant tool calls, and rework loops; gaps live in the places where the human had to correct the model.
- **Prompt or template**: cost lives in verbosity and over-instruction; gaps live in underspecification of the cases that actually occur.

**Read the entire artifact before forming any opinion.** Open the actual files, read the actual task definition, read the actual transcript. Do not audit from a summary or from memory of a previous version. If the artifact references other resources (bundled reference files, linked documents, upstream skills, connector schemas), open the ones that carry logic. An audit of half the artifact produces edits that break the half you did not read.

**Reconstruct the intent.** Write down, in two or three sentences: what this artifact is supposed to produce, for whom, on what trigger, and what "correct" means for it. If the artifact itself never defines what correct means, that is already Finding #1.

**Collect the standing constraints.** Check memory, project instructions, and the artifact's own conventions for rules the user has already established (delivery channels, test-mode defaults, read-only resources, formatting rules, sequencing rules like create-before-delete). Every proposed edit must be checked against these before it ships. An optimization that violates the user's established conventions is a regression wearing a cost-savings costume.

**Establish the baseline.** Note, as concretely as the artifact allows: roughly how much context it loads, how many tool calls a typical run makes, how many retries or loops it permits, and where its quality currently stands. You cannot claim savings against a baseline you never measured, even roughly.

---

## Phase 2: Gap analysis. Where can this produce wrong output?

Walk the artifact end to end as a hostile reader, hunting for these specific gap classes:

**Ambiguity gaps.** Instructions a reasonable model could interpret two ways. Test: for each instruction, ask "could two competent runs of this produce materially different output?" If yes, the instruction needs a tiebreaker, an example, or a definition. Vague quality words ("good", "clean", "appropriate") without criteria are the most common carrier.

**Missing-case gaps.** Inputs or situations the artifact will encounter but does not handle: empty results, zero rows returned, the source system being down, a name that matches two records, a date range spanning a month boundary, an unexpected file format, the happy path failing halfway through a multi-step write. For scheduled tasks especially: what happens when the data it expects simply is not there yet?

**Silent-failure gaps.** Places where the artifact can fail without anyone knowing: a tool call whose result is never checked, a delivery that is never confirmed by read-back, a number that is computed once and never re-derived, a step whose output feeds forward unvalidated. Every consequential step should have a way to know it worked; flag every one that does not.

**Reasoning gaps.** Steps where the logic asserts more than its inputs support: a conclusion drawn from a sample presented as the whole, a threshold with no stated justification, a classification rule that would misfile obvious real cases, ordering dependencies that are assumed but never enforced.

**Drift and staleness gaps.** Hardcoded values that will rot (dates, names, IDs, prices, model names), references to systems or people that change, instructions that were correct when written but depend on external state. Flag each with what should replace it (a lookup, a parameter, a dated review note).

**Trigger gaps** (for skills specifically). Cases where the skill should fire but the description will not catch it, and cases where it will fire when it should not. Read the description as a matching function, not as prose.

**Then stop reading and start executing: the dry-run test.** Static reading finds the gaps an author can see; execution finds the gaps only a runtime can see, and those are the ones that hurt. Trace the artifact step by step, as the model that will run it, against three concrete inputs you construct:

1. **The typical case:** the input the artifact sees on a normal day. Walk every step literally: what exactly gets fetched, what exactly gets computed, what exactly gets delivered. Any step where you cannot say precisely what happens next is an ambiguity gap you missed on the read.
2. **The edge case:** a realistic boundary input (empty result set, month-spanning date range, duplicate-name match, an unusually large batch). Watch for the step where the instructions stop covering what is in front of you.
3. **The broken world:** the source system returns an error, stale data, or nothing. Trace what the artifact does. If the honest answer is "it delivers output anyway" or "nothing tells anyone," those are CRITICAL findings.

Where the artifact's tools are actually available to you, prefer a real probe over a mental trace for the riskiest step (run the query, fetch the schema, render the template). One real execution outranks ten thought experiments.

For each gap found, record: where it is (quote the exact line or step), what goes wrong and how likely that is in practice, and the concrete fix. Severity-rank them: CRITICAL (can produce wrong delivered output), MODERATE (degrades quality or wastes rework), MINOR (polish).

---

## Phase 3: Efficiency audit. Cut cost without cutting quality.

Hunt for spend that does not buy quality. The proven high-yield targets, in rough order of savings:

**Context that loads but never earns its keep.** Instructions for situations that cannot occur, examples that duplicate each other, long preambles restating what the model already does by default, reference material inlined into the main file that only one branch ever needs. Fix: delete the dead weight; move branch-specific material into reference files loaded only when that branch runs (progressive disclosure). This is usually the single largest saving in skill files.

**Redundant tool calls.** Fetching the same data twice, pulling full records when two fields are needed, paginating an entire dataset to answer a question about the first page, calling per-item what could be called per-batch. Fix: name the exact call pattern to replace and its replacement.

**Retry and loop budgets with no exit.** Unbounded "keep trying" instructions burn cost precisely when things are broken and the run should be failing fast and reporting instead. Fix: explicit retry caps with a defined failure path.

**Verbose output where the consumer needs less.** A report that restates its own inputs, logs that narrate every step to a channel where nobody reads them, duplicated content across delivery targets. Fix: define the minimal output that fully serves the consumer, and cut to it. Note the distinction: verification effort is never the fat to cut; narration of verification often is.

**Work done at run time that could be done once at design time.** Re-deriving stable mappings, re-explaining stable context, re-discovering schema on every run. Fix: bake stable facts into the artifact (with a staleness note per Phase 2) and spend run-time effort only on what actually varies.

**Model effort mismatched to step difficulty.** In multi-step workflows, flag steps that are pure mechanical transforms and could run as scripts or cheaper calls, versus steps that genuinely need judgment. Do not propose downgrading judgment steps to save money; that is the forbidden tradeoff.

For every efficiency edit, state three things: the estimated saving (in tokens, calls, or run frequency, rough is fine but it must be stated), the quality property it preserves and how you know it preserves it, and the risk rating (SAFE: no plausible quality impact; GUARDED: small risk, mitigated as described; TRADEOFF: real quality risk, presented as user's choice only).

**The anti-pattern to never commit:** cutting the checking to save the cost. QA gates, read-backs, re-derivation of figures, and verification passes look like overhead in a token count and are the cheapest components in the entire system relative to the failure cost they prevent. If an artifact's biggest expense is its verification, the finding is "this artifact is correctly built," not "cut verification."

---

## Phase 4: Elevation. Make the output world class without breaking it.

This phase asks a different question: not "what is wrong" but "what would the best version of this look like?" Generate upgrade ideas, then filter them ruthlessly through accuracy and reliability.

Productive directions to probe (use as prompts, not as a checklist to pad the report):

- **Raise the ceiling of the deliverable itself.** Would the consumer be better served by a different form: a ranked list instead of a dump, a decision instead of a summary, a trend line instead of a snapshot, one insight with evidence instead of ten observations? The biggest quality jumps usually come from upgrading what the artifact delivers, not how it phrases it.
- **Add the comparison that creates meaning.** Numbers become insight next to a baseline: versus last period, versus target, versus the team median. If the artifact reports figures with no reference point, proposing the right reference point is often the highest-value single edit.
- **Surface the exception, not the inventory.** World-class operational output leads with what changed and what needs attention, and compresses everything that is normal. If the artifact treats all items equally, propose the triage layer.
- **Close the loop.** Can the artifact learn from its own history: track whether its past flags were acted on, whether its predictions held, whether the same issue keeps recurring? Longitudinal memory is what separates a report from an advisor.
- **Anticipate the follow-up question.** Read the output as its consumer and note the first question they would ask upon reading it. If the artifact can answer that question in the same run for marginal cost, propose it.
- **Steal proven structure.** If the user has other artifacts that solve a similar problem well (a QA gate pattern, a delivery convention, a scoring rubric), propose porting the proven pattern rather than inventing a novel one. Consistency across a fleet is itself a quality property.

Then filter: every elevation idea must pass three tests before it appears in the report. (1) Accuracy: it introduces no new claims the artifact cannot verify. (2) Reliability: it adds no fragile dependency or failure mode without a handling path. (3) Worth it: its added cost is justified by its added value, stated explicitly. Ideas that fail the filter can be mentioned in one line as "considered and rejected because X" if instructive, or dropped silently.

Elevation proposals are suggestions, not defaults. Mark them clearly as optional upgrades so they are never confused with the gap fixes, which are corrections.

---

## Phase 5: Report. Deliver edits, not essays.

Structure the report exactly like this:

```
## Verdict
[Two or three sentences: overall health of the artifact, the single highest-impact
change, and rough total efficiency saving available at SAFE risk.]

## Scorecard: NN/100
Correctness safeguards   /30  [verification, read-backs, re-derivation, failure handling]
Clarity of instruction   /20  [would two competent runs produce the same output]
Efficiency               /20  [cost proportionate to value, no dead weight]
Resilience               /15  [survives the edge case and the broken world from the dry run]
Output value             /15  [the deliverable itself: insight density, consumer fit]

## Critical gaps (fix these)
[Each: location quoted, what goes wrong, the exact edit. Before/after text where
the artifact is text.]

## Efficiency edits
[Each: the edit, estimated saving, what it preserves, risk rating SAFE/GUARDED/TRADEOFF.
Sorted by savings within risk tier, SAFE first.]

## Elevation options (optional upgrades)
[Each: the idea, the value it adds, its added cost, why it passes the accuracy and
reliability filter.]

## Moderate and minor findings
[Compressed, one line each.]

## What is already excellent
[Genuinely strong elements that must be preserved through any edits. This section is
load bearing: it stops a future editing pass from optimizing away the artifact's
strengths.]

## Regression test set
[The three dry-run inputs from Phase 2 (typical, edge, broken world), written as
concrete prompts or scenarios the user can rerun against the artifact after any
edit. Passing all three means the edits did not break what worked. Keep and reuse
this set on every future audit of the same artifact.]
```

Score honestly against the rubric, not generously. The score's entire value is comparability: the same artifact audited after edits should move for real reasons, and two artifacts in the same fleet should be rankable by it. A rubric that hands out 90s is a broken instrument.

Report rules:

- **Every edit is concrete.** Where the artifact is text, show replacement text. Where it is a workflow, name the exact step and its replacement. The user should be able to apply the report without interpreting it.
- **Never bundle a TRADEOFF edit into a batch of SAFE edits.** Tradeoffs get their own visibility and an explicit both-sides framing, because the user owns that call, not the auditor.
- **Check the full edit set against the standing constraints from Phase 1** before delivering. Also check the edits against each other: two individually safe edits can conflict.
- **If asked to apply the edits**, snapshot the original first so rollback is always one copy away. Then apply edits one at a time in severity order, re-reading the affected region after each edit, and honor the user's sequencing conventions for live artifacts (for scheduled tasks: build and verify the replacement before removing the original, never the reverse). After the last edit, run the regression test set against the edited artifact and re-run the Phase 2 gap checklist on it, because edits introduce gaps at the same rate authorship does. Report the new score next to the old one.
- **Calibrate honestly.** If the artifact is already well built and the real findings are minor, say so plainly and keep the report short. Inventing findings to justify the audit is itself a quality failure. The empty audit that says "this is solid, here are two small things" is a successful run.
