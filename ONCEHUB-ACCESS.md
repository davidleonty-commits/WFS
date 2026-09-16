# Getting OnceHub data into the tasks

Written 2026-09-16, after testing both routes.

## Short version

**I cannot fix this from inside the session, and neither can the API key.** OnceHub is blocked
by the environment's egress policy, which is a setting on your claude.ai environment. One
change unblocks it. Everything else is already in place and tested.

## What was tested

| Check | Result |
|---|---|
| `GET https://api.oncehub.com/v2/bookings` with the key | `CONNECT tunnel failed, response 403` |
| `GET https://api.github.com` (control, same proxy, same session) | `HTTP 200` |
| `mcp.oncehub.com` (the SSE MCP endpoint) | same 403 |
| `app.callix.io` / `api.callix.io` | same 403 |
| `Oncehub_MCP` connector, `get_booking_time_slots` | reached OnceHub, replied `API key not configured` |

The control matters: the proxy is healthy and the CA is trusted. GitHub goes through on the
same connection that OnceHub is refused on. So this is not a broken proxy, not a TLS problem,
and not a bad key — **the key has still never been sent to OnceHub.** `api.oncehub.com` is not
on this environment's allowlist.

The agent proxy's own documentation (`/root/.ccr/README.md`) is explicit about this failure
class: *"The destination host is not allowed by your organization's egress policy for this
session. Do not retry or route around it — report the blocked host."* Routing around an egress
policy is not something to do quietly on someone's behalf, so this is reported rather than
worked around.

## The two routes, and what each one can actually deliver

### Route A — the claude.ai OnceHub connector (`Oncehub_MCP`)

Already attached to this session, and it does **not** go through the environment's network
policy, so the 403 does not apply to it. It answered.

What it said: `Failed to get API key from context: Missing or invalid Authorization header`.

**Fix:** claude.ai -> Settings -> Connectors -> OnceHub -> add the API key.

**But this route cannot deliver the reports.** The connector exposes exactly two tools,
`get_booking_time_slots` and `schedule_meeting`. Neither lists or enumerates bookings, which is
what every show-rate, lead-flow and webinar report needs. And `schedule_meeting` *writes* — it
creates real bookings on real calendars, which four prompts explicitly forbid. Fixing the key
here is worth doing for completeness, but it does not unblock a single report.

### Route B — the OnceHub REST API (what the prompts actually use)

This is the one that matters. Every booking sweep in the package is
`GET https://api.oncehub.com/v2/bookings` with header `API-Key`, paginated.

**Fix:** allow `api.oncehub.com` on the environment's network policy — claude.ai -> Code ->
Environments -> the environment these run in (currently "Default - trusted network access").
See https://code.claude.com/docs/en/claude-code-on-the-web for how environments and their
network policies are configured.

**Add `app.callix.io` in the same change.** It is blocked identically, and it is what clears
the `CALLIX FIELD NAMES UNVERIFIED` and `CALLIX REST PATHS ARE UNVERIFIED` gates now sitting in
28 files.

## The moment it opens, run this

```bash
export ONCEHUB_API_KEY=...        # the key, from your secret store
export CALLIX_API_KEY=...
python3 scripts/verify-oncehub.py
```

It is read-only and prints **field names and counts only, never booking contents**, so the
output is safe to paste back here or into a ticket. It answers, in one run, every question the
prompts currently guess at:

1. Whether the host is reachable at all, and says so in those words if it is not.
2. Whether `/v2/booking-calendars` is the right resource name for this account (v1 called it
   `/master_pages`; five prompts were corrected on that already).
3. Whether `starting_time.gt` / `.lt` are accepted and `starting_time_from` / `_to` are
   rejected — both show-rate reports and the webinar report are built around exactly that split.
4. Whether a booking carries `booking_page.master_page` and `in_trash`. The per-master-page
   grouping and the unattributed-booking rescue both depend on those existing.
5. The real name of the pagination cursor, which every sweep follows "until it is null".
6. Callix's row field names, to replace the six carried-over ones in the gates.

Paste the output back and the gates come out of all 28 files in one pass.

## Why nothing was faked in the meantime

No prompt was given an invented endpoint, parameter or field name to paper over this. A guessed
name does not fail loudly — it 404s, or silently matches nothing, and the report then reads
zero calls and looks like a quiet day. That is the failure this package is least able to
notice, so the unverified spots are marked and made to stop a run instead.
