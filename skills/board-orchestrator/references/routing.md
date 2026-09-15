# Skill routing

Match on **intent**. Read the task's description and custom fields, decide what the work
actually *is*, then find the skill whose stated capability covers it. Keyword collisions
are the main failure mode — "review" appears in a call review, a contract review, and a
funnel review, and they route three different places.

## Routing table

| The task actually requires… | Route to | Signals |
|---|---|---|
| Reviewing one **closer** call, producing the team Slack post | `closer-call-review-slack` | Transcript + Loom link, wants the written post |
| Reviewing one **closer** call, producing the Loom teleprompter | `closer-call-review-script` | "script to film", teleprompter, timestamps |
| Reviewing one **setter/booking** call → written post | `setter-call-review-slack` | Qualification, pre-call sell, show rate |
| Reviewing one **setter** call → film script | `setter-call-review-script` | Same, but "script"/"loom" |
| The **daily** batch of TTW calls, DM'd to Slack | `ttw-daily-avoma-report` | "today's calls", scheduled daily report |
| Daily batch from an **uploaded transcript file** | `ttw-daily-call-review` | Attachment on the card is an Avoma export |
| Weekly **coaching clips** with clip-in/out anchors | `ttw-avoma-clip-finder` | "find clips", objection handling |
| Any **TTW sales number** (show rate, close rate, collections, CDPBC…) | `ttw-dashboard-metrics` | Any KPI. Never re-derive these. |
| Lead quality for a **specific webinar date** | `webinar-lead-quality-report` | A webinar date + lead scoring |
| A flagged **compliance** issue, or "is this a pattern" | `compliance-trend-loop` | Income coaching, guarantee language |
| Tracking whether **coaching stuck** for a rep | `sip-watch-loop` | "did it stick", "is he still doing X" |
| A **VSL** script, from scratch or improved | `vsl-script-writer`, or `vsl-conversion-loop` if it must be ship-ready | Revenue funnel → use the loop |
| Grading or rebuilding an **offer** | `offer-validator` | "is this a good offer", pricing |
| Auditing a **funnel / landing page** URL | `funnel-review` | A URL + "why isn't this converting" |
| A **YouTube video** idea, hook, title, or script | `youtube-video-engine` | Channel content |
| Turning a long video into **platform posts** | `content-repurpose` | Personal brand, carousels, LinkedIn |
| **Clip farming** / Whop campaigns / content rewards | `clip-farming` | Monetized short-form |
| Weekly **AI news** sourcing or scripting | `ai-news-engine` | The news show |
| **Lead gen scraping** a site or finding creators | `web-crawler` | "find me leads", "crawl this" |
| Reviewing or optimizing **another skill or automation** | `fable-review` | "audit this task", "make this cheaper" |
| A **spreadsheet** is the deliverable | `xlsx` | .xlsx/.csv in or out |
| A **deck** is the deliverable | `pptx` | "slides", "deck", "presentation" |
| A **Word doc** is the deliverable | `docx` | "report", "memo", .docx |
| A **PDF** is the deliverable | `pdf` | .pdf in or out |
| Something in **Summit's brand style** | `summit-brand-design` | "Summit style/branding" |
| The **trading contest** account | `ai-trading-contest` | Robinhood, positions, stops |
| A **QA gate failed** anywhere in this pass | `qa-failure-loop` | Always, in addition to the primary skill |

## Tie-break rules

1. **More specific wins.** `closer-call-review-slack` beats `closer-call-review`.
   `ttw-dashboard-metrics` beats "go query Pipedrive".
2. **Deliverable format is a second axis, not a competitor.** "Build the Q3 closer report
   as a deck" = `ttw-dashboard-metrics` for the numbers, *then* `pptx` for the artifact.
   Research first, format skill second — never read a format skill before you have the
   facts.
3. **Account tag gates the TTW family.** `Account name` ≠ TikTok Wiz means the TTW skills
   almost certainly don't apply, however well the words match.
4. **High stakes → wrap in `fable-mode`.** Money, compliance, numbers from source systems,
   anything a third party will read.
5. **Ambiguous → don't pick.** Two plausible skills with no specificity gap, or a task
   whose real requirement you can't state in one sentence, is a flag to Caydo — not a
   coin flip.

## What "no match" looks like

Route to nothing and flag when the task is:

- Pure human judgment (a hiring call, a comp decision, a relationship conversation).
- An action inside a system with no connector for it.
- A physical-world or verbal task (attend a session, make a phone call, run a 1:1).
- Something the guardrails block outright (delete, permissions, purchase, external send).

`Work Board action ✨` is a strong tell here — `📅 Attend session`, `☎️ Call`,
`👫 Manage team`, `🧑🏽‍🏫 Train`, and `🛍️ Purchase` are all human-only actions. A card
carrying one of those is a flag, not a routing problem. Say so plainly in the flag rather
than reaching for the nearest skill.
