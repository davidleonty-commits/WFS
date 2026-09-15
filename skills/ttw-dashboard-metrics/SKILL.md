---
name: ttw-dashboard-metrics
description: The verified, exact formulas for every TTW closer KPI that used to live on the Looker Studio "Closer Sales Dashboard", computed connector-only from Pipedrive and the TTW Salesboard 2026 Google Sheet. Use this skill whenever Caydo asks for TTW sales numbers, closer or rep metrics, show rate, live calls, qualified calls, close rate, collections, CDPBC/GDPLC/CDPLC/GDPBC, salesboard revenue (gross or collected), leaderboard or scorecard numbers, SIP KPI actuals, "how are the closers doing", month-to-date sales stats, or anything that used to come from Looker Studio or datastudio. Also use it when building or fixing any report, scheduled task, or automation that needs these KPIs, so the numbers match the verified definitions instead of being re-derived. Trigger even for simple-sounding metric requests, because the date basis, refund handling, and show/close definitions have exact rules that were verified against the live dashboard on 2026-07-02 and are easy to get subtly wrong.
---

# TTW Dashboard Metrics (verified formulas)

Formulas verified exactly against the Looker "Closer Sales Dashboard" (Sales Rep tab) on four periods (Jul 1, Jun 1–30, Jun 1–15, May 1–31, 2026). Compute everything from raw counts; round only for display.

## Call metrics — Pipedrive, pipeline 3

Stages: 11 Lead in → 12 First Call Completed → 13 Demo Completed → 14 Follow up → 15 Funding → 16 Enrolled.

Custom field hash keys (stable):

| Key | Field | Values |
|---|---|---|
| `1f670bc129bc774c0263568ce202fdd81060d5f7` | First Call Date | ISO date — THE date basis for all call counts (never add_time) |
| `9bbc316d2725b360e7c28af48c04899619e0b966` | First Call Show Up | YES (option 29) / NO (option 30) |
| `d7fb74d5136840a5757fe5e3e1477323309fd6a6` | Secondary yes/no (post-show) | YES (31) / NO (32) |
| `6f4a224eaf3834b9a3a32a716ec355b11b561814` | Lead Source / event label | e.g. "Youtube", "Webinar 06 28 26" |

Pull: `getDeals(pipeline_id=3, include_option_labels=true, sort_by=add_time, sort_direction=desc, custom_fields=<keys above>)`, paginate by cursor until add_time < range_start − 14 days (deals are created up to ~a week before their first call), then filter by First Call Date. Include open, won, AND lost deals. Read-only: never call Pipedrive write tools for reporting.

Over deals with First Call Date in range (per rep = deal owner; team = all):
- **Qualified Closer Calls** = count of those deals
- **Live Calls** = subset that ever moved past Lead in (stage_id > 11, or won)
- **FC Live Calls** = Live subset with First Call Show Up = YES
- **% Show** = Live / Qualified (the Show Rate; flag >100% as anomaly, don't print)
- **% FC Show** = FC Live / Qualified

Leaderboard-style reports exclude Lead Source labels S2C, DM S2C, Newsletter; SIP/scorecard pulls are unfiltered. Known ±1: archived deals count in old dashboard history but aren't returned by getDeals.

## Revenue metrics — TTW Salesboard 2026 (READ-ONLY, always)

Sheet id `1_5YMQVATclX5gRRJfkqG-wfyWP23TYlDoLugu8Tz_W4` (accounting-managed: never edit, sort, filter, comment, or script it — reads only). Deal rows live in monthly tabs "<Month> MC (Webinar) Detail" and "<Month> DLF (Non Webinar) Detail"; row 1 = totals, row 2 = headers, data from row 3. Columns: A Date, B Sales Rep, C SDR Rep, G Gross, H Collected, P Payment Status. Read every month tab the date range touches.

Over rows with Date in range (per rep = Sales Rep column; setters = SDR Rep):
- **Salesboard Closed** = count of rows with non-blank Gross (refund rows INCLUDED)
- **Salesboard Gross** = sum of Gross on those rows, refund rows INCLUDED (correctly exceeds the tab's row-1 total, which excludes refunds)
- **Salesboard Collected** = sum of Collected EXCLUDING rows with Payment Status "Refund" (matches row-1 totals: MC + DLF)
- Blank-Gross rows with Collected values are follow-up payments: Collected only, never Closed/Gross
- Validation: per-tab Collected (excl. refunds) must equal that tab's row-1 Collected total

## Derived ratios

- **% Live Closed** (the Close Rate) = Closed / Live — never Closed / Qualified
- **% Booked Closed** = Closed / Qualified (sanity only)
- **Collection Rate** = Collected / Gross
- **GDPLC** = Gross / Live; **CDPLC** = Collected / Live; **GDPBC** = Gross / Qualified; **CDPBC** = Collected / Qualified (ranks "Most Profitable Rep"; June check: $769,150/313 = $2,457.35 GDPLC exact)

## Freshness

The old Looker dashboard cached data ~twice daily; these connector pulls are live and FRESHER. Same-day differences vs. old dashboard screenshots are cache lag, not formula error. Reference totals for self-checks — Jun 2026: Qualified 671, Live 313, Closed 102, Gross $769,150, Collected $508,810; May 2026: 550 / 217 / 71 / $542,500 / $300,705.
