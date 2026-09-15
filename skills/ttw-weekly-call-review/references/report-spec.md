# Report specification

## Workbook: two tabs

Build with `openpyxl`, then recalculate with the xlsx skill's `scripts/recalc.py` so cached formula values exist. Use live formulas against the data tab, not hardcoded numbers, so the report updates if a row is edited.

### Tab 1 — Call Data

One row per call, sorted by date, shaded across the whole row by bucket.

| # | Column | Notes |
|---|---|---|
| A | Lead Name | prospect, never the rep |
| B | Rep Name | from the roster, verbatim |
| C | Income Qualification | job, income, credit, savings, debts. Terse. `"Not stated"` only after a full read |
| D | Motivation | why they want it, one clause |
| E | Unqualified | financing attempted and outcome, by provider |
| F | Rep Performance | 1 to 10, blank if unscoreable |
| G | Closing Notes | 1 to 2 sentences, what happened plus follow-up day and time |
| H | Date | |
| I | Call Type | |
| J | Duration (min) | |
| K | Outcome | closed_full / closed_base44 / follow_up / no_close / not_a_sales_call |
| L | Bucket | RED / GREEN / GREY / BLUE / ORANGE / NA |
| M | Disqualifying Evidence | the lead's verbatim words with timestamp. Mandatory for RED and ORANGE |
| N | Evidence Type | see list below |
| O | Verification | how this row was verified |
| P | Data Quality | truncation, swapped labels, missing transcript |

Bucket fills: RED `F8D7D5`, GREEN `DDEEDA`, ORANGE `FCE3CC`, BLUE `D6E6F5`, GREY `E4E4E4`, NA `F3F3F3`. Freeze the header, add an autofilter.

Evidence types: `stated_inability`, `financial_figure`, `low_credit_or_debt`, `lender_decline`, `no_or_insufficient_income`, `third_party_funding`, `cannot_afford_monthly`, `capacity_confirmed`, `closed_funded`, `none`.

### Tab 2 — Report

Blocks, in order:

1. **Title and window**, plus a one-line note on exclusions and how rows were verified.
2. **Team summary**: total calls, gradeable calls, closes, close rate, average rep score.
3. **Lead buckets**: count, % of gradeable, % of all calls, with a plain-language meaning per bucket.
4. **FDQ economics** (see below). This is the block management reads.
5. **Closes by quality**: BLUE vs ORANGE, with ORANGE as a share of closes.
6. **Per rep**: calls, gradeable, closed, close rate, average score.
7. **Bucket mix by rep**: RED / GREY / GREEN / BLUE / ORANGE / gradeable / **RED %**. Sort by RED % descending. Use RED %, not GREY %.
8. **Review history**: counts by verification method.

Charts: average rep score by rep, bucket distribution pie, calls vs closes by rep, close rate by rep, RED % by rep.

Percentages use **gradeable calls** (everything except NA) as the denominator, so the real buckets sum to 100%. Say so on the tab.

## FDQ economics

FDQ = RED + ORANGE. Both were financially disqualified; ORANGE just bought anyway.

**Net revenue per Clarity Pay close is $6,400** (the $8,000 financed price less the finance company's cut). Use this unless told otherwise. Base 44 downsells count at $50 for the first month, not annualised.

Compute:

```
qualified_close_rate = closes among (GREEN + BLUE) / count(GREEN + BLUE)
fdq_actual_revenue   = fdq_full_closes * 6400 + fdq_base44_closes * 50
value_per_qualified  = qualified_closes * 6400 / count(GREEN + BLUE)
value_per_fdq        = fdq_actual_revenue / count(FDQ)
gap_per_consultation = value_per_qualified - value_per_fdq
opportunity_cost     = (qualified_close_rate * count(FDQ) * 6400) - fdq_actual_revenue
```

Report the opportunity cost for the window, and extrapolated to a 30-day month. Also give a sensitivity table showing modeled monthly revenue at several FDQ rates, so the value of moving the number is explicit.

**Do not lead with the theoretical ceiling** (every FDQ lead buying at $6,400). It assumes a 100% close rate. Mention it only as a bound if asked.

Always label these as modeled from actual close rates by segment, not booked revenue. State the two assumptions: replacement leads convert like the qualified leads already observed, and consultation volume is held constant.

## Deliverables

1. **The .xlsx**, both tabs, delivered with SendUserFile.
2. **A Google Sheet of the Report tab** via `mcp__Google_Drive__create_file` with `contentMimeType: "text/csv"` and conversion left on.
3. **A summary message** if asked.

**Drive limitation.** The connector accepts file content only as a parameter inside a single tool call, and there is no update-in-place tool. Anything much over about 85KB of CSV fails, so the full data tab will not upload. Post the Report tab and hand over the .xlsx for the full data. Uploading the .xlsx as base64 also fails at this size.

## Summary message

Ask where it is going. For Slack, note that the newer composer does not convert pasted markdown, so **deliver plain text with no asterisks or markup** unless the person says mrkdwn renders for them.

Keep it to the FDQ rate, what it costs, the per-rep spread, and where to look. Structure:

> [Window]
>
> [X]% of our consultations were with leads who couldn't afford the program. That's [n] of [total] calls.
>
> Those calls close at [x]%. Financially qualified leads close at [y]%.
>
> At $6,400 net per Clarity Pay deal, that gap cost us roughly $[X]K over [n] days, or about $[Y]K a month.
>
> Every FDQ call is worth about $[gap] less than a qualified one. Moving our FDQ rate from [current]% to [target]% is worth around $[Z]K a month.
>
> FDQ rate by rep, same lead source: [list].
>
> That spread points at lead routing and booking criteria before closing skill.
>
> Report: [link]
>
> Revenue is modeled from actual close rates by segment, not booked revenue.

Keep compliance findings out of channel messages. Note that they exist and hand the detail over directly.
