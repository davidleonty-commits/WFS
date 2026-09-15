# Moving call data from Avoma to Callix

Status: **design only, nothing rewritten yet.** Four answers are needed first (section 5).

## 1. Why this is not a find-and-replace

Avoma was a **pull** source: a task woke at 6:30 PM and asked "what calls happened today?"
A webhook is a **push**: Callix tells a URL that something happened, at the moment it happens.
A scheduled prompt cannot call a webhook, and a webhook cannot answer a question asked hours
later. So there is no line-for-line substitution. What replaces Avoma is not the webhook, it is
the **store the webhook writes into**:

```
Callix  --webhook-->  receiver endpoint  -->  Supabase (calls, call_transcripts)  -->  prompts read SQL
```

The prompts keep their current shape. `list_meetings over the window` becomes `SELECT ... FROM
calls WHERE call_date = ...`, and `get_meeting_transcript(uuid)` becomes `SELECT transcript
FROM call_transcripts WHERE call_id = ...`. Every rubric, gate and threshold is untouched.

Supabase is already in this stack (project `apdwbbocldfsklvcwaqd`, the `lead_quality` table),
several routines already hold the Supabase connector, and `mcp__Supabase__execute_sql` is
already how they read it. That makes it the cheap landing zone rather than a new dependency.

## 2. What actually has to be replaced

25 files make real call-platform calls (the other 28 that mention Avoma are incidental: SIP
documents that mention clip links, roster notes, and so on).

| Avoma operation | Uses | What the prompt actually needs | Becomes |
|---|---|---|---|
| `list_meetings` | 52 | the window's calls with title, duration, start time, organizer/attendee email, whether a transcript exists | `SELECT` over `calls` for the date window |
| `get_meeting_transcript` | 44 | full speaker-labelled transcript, ideally timestamped | `SELECT` over `call_transcripts` |
| `get_meeting_notes` | 22 | AI summary, used as a triage lead and never as evidence | `notes` column, nullable |
| `get_current_datetime` | 15 | a reliable clock, nothing more | **already removed**, now the system clock in `TZ=America/Denver` |
| `list_team_usage_metrics` | 1 | the director's own call-review activity for the EOW report | no known Callix equivalent, see section 5 |

Fields the prompts read off a call, in rough order of how much depends on them: `title` /
`subject` (qualification: "TikTok Wiz Consultation", excluding intros and syncs), `duration`
(the over-15-minutes and over-1800-seconds gates), `starting_time`, `organizer_email` (the rep
key after the connector swap), `transcript_ready`, `meeting_state`.

## 3. The store

Minimal schema that satisfies every consumer above:

```sql
create table calls (
  call_id            text primary key,          -- Callix's own id
  title              text,                      -- qualification gates read this
  started_at         timestamptz not null,       -- windowing; store UTC, slice in MT/ET
  duration_seconds   integer,                    -- the 900s / 1800s gates
  organizer_email    text,                       -- the rep key
  attendee_emails    text[],                     -- PIF buyer join
  state              text,                       -- completed / no-show / cancelled
  transcript_ready   boolean default false,
  raw                jsonb not null,             -- the untouched webhook payload
  received_at        timestamptz default now()
);

create table call_transcripts (
  call_id     text primary key references calls(call_id),
  transcript  text,                              -- speaker-labelled
  segments    jsonb,                             -- per-segment speaker + text + offset, if Callix sends it
  notes       text,
  updated_at  timestamptz default now()
);

create index on calls (started_at);
create index on calls (organizer_email);
```

Two properties the prompts depend on, so the receiver must guarantee them:

- **Idempotent upsert on `call_id`.** Callix will redeliver. A duplicate row becomes a
  double-counted call in the show rate denominator.
- **`raw` is kept verbatim.** When a report disagrees with Callix, the payload is the evidence,
  and the existing QA gates are written around having evidence to re-check.

## 4. What this changes about the reports

- **History starts empty.** A webhook only captures calls from the moment it is wired. Until
  the store fills, the weekly review (7 days), the PIF buyer report (30 days) and the SIP
  engines (three-week cycles, minimum 5 verified calls per rep per run) have nothing to read.
  Either Callix can export or replay history, or those reports stay paused for their window
  length.
- **`ttw-lead-quality-backfill-guardian` gets more useful, not less.** It exists to prove one
  scored row per qualifying call per weekday. Pointed at the Callix store it also catches
  dropped webhook deliveries, which is the new failure mode.
- **A missed delivery is silent by nature.** Avoma could be re-queried; a webhook that never
  arrived leaves no trace. The guardian's daily reconciliation becomes the only thing standing
  between a dropped call and a wrong published number, so it should be enabled before anything
  else goes LIVE.

## 5. Finding, 2026-09-15: the webhook screen points the wrong way

Callix's Settings, Developers, Custom Webhooks screen creates an **inbound** endpoint. Its own
description: "Each endpoint gets a unique URL. Point any external platform at it and choose what
to do with the incoming data." The five processing actions are all ingest actions (Log Only,
Store Payment, Store Event, Upsert Prospect, and "Analyze Call, extract transcript to AI deal
analysis").

That is Callix receiving. Every consumer in section 2 needs Callix emitting, or at least being
readable on a schedule. So this screen does not replace the Avoma reads, and wiring it up would
produce a working pipe that still leaves 25 files with nothing to query.

If an ingest endpoint is wanted anyway (for example, pointing a recorder at Callix so it
extracts the transcript), the fields are:

- NAME: `WFS TTW Call Ingest`
- DESCRIPTION: `Recorder posts finished TikTok Wiz consultation calls here; Callix extracts the transcript and runs deal analysis.`
- PROCESSING ACTION: `Analyze Call - extract transcript to AI deal analysis`

## 5b. Why "Analyze Call on every call that day" does not solve it

The proposal: set an endpoint's processing action to "Analyze Call, extract transcript to AI
deal analysis" and push each of the day's calls through it.

The blocker is enumeration, not transcription. Every report in section 2 opens by asking which
calls happened in a window; `list_meetings` is 52 of the call sites, more than any other
operation. A per-call analyze endpoint answers "tell me about this call" and cannot say which
calls to ask about. The 6:30 PM publisher would not know how many consultations happened, and
the show rate reports could not count live calls at all.

Behind that, three more:

- To POST the day's calls in, something must already hold them. If it does, that something is
  the real Avoma replacement and Callix is a detour. If it does not, because the calls are
  already inside Callix, there is nothing to send.
- The result lands inside Callix, attached to a prospect or deal. A scheduled task still has
  nothing to query.
- It is the wrong analysis. These reports score against their own rubric: the 25-point
  scorecard, the Decision Leadership matrix steps, the RED / GREEN / GREY / BLUE / ORANGE
  buckets, `financially_qualified` with `dq_reason`, the CDPBC inputs. Callix's deal analysis is
  its own product's opinion with its own schema. Substituting it would change every published
  number and break the QA gates that check a score against its bucket rule. The Avoma swap kept
  scoring inside the prompts deliberately; what is needed from Callix is the transcript, not an
  analysis. Running analysis per call and discarding it also pays for work nobody reads.

### The one test worth running

Create the endpoint with the Analyze Call action, POST a single payload referencing a known
call, and read the HTTP RESPONSE BODY, not only the Activity Log.

- Response carries transcript text: that is a read path, one call at a time. Enumeration is
  then the only gap, and the question for Callix narrows to "how do I list calls for a date".
- Response is an acknowledgement (`{"ok": true}` or an id): dead end for reporting, established
  in two minutes instead of a rebuild.

Checked 2026-09-15: the closers' consultations are not reachable through any other connected
source, so Callix is the only place they exist and this test decides the outcome.

## 6. The open question is now narrower

Everything depends on whether call data can leave Callix at all:

1. **Is there any read path?** An API key or token under Developers, a native or Zapier
   integration under Integrations, or an outbound event subscription. Any one of these makes
   this a straightforward rebuild against the schema in section 3.
2. **Failing that, can Callix export calls and transcripts** (CSV or JSON, scheduled or manual)?
   An export to a watched Drive folder is slower and lossier than an API, but it is enough to
   keep the scheduled reports alive, since the prompts can read Drive.
3. **Failing both**, the unattended call reports cannot be rebuilt. See section 7.

## 7. What survives if Callix stays closed

The call-review skills come in pairs, and only one half of each pair needs a live source:

| Needs a live source | Works from a supplied transcript |
|---|---|
| `ttw-daily-avoma-report` (the 6:30 PM self-serve report) | `ttw-daily-call-review` (grades an uploaded transcript file) |
| `daily-call-report-publisher-v27` | `closer-call-review`, `closer-call-review-script`, `closer-call-review-slack` |
| the show rate reports' live-call counts | `setter-call-review-slack`, `setter-call-review-script` |
| the SIP engines' five-verified-calls gate | `ttw-weekly-call-review` (grades from transcripts it is given) |
| `weekly-call-review-sourcing-v2`, the clip finder's sweep | the clip finder's scoring, once it has transcripts |

So even in the worst case the coaching layer survives as a manual workflow: export transcripts
from Callix, hand them to the review skills, and the rubrics, buckets and clip anchors all still
apply. What is lost is the unattended half: the daily publisher, the live-call side of both show
rate reports, and the SIP engines' automatic evidence gate.

The show rate reports are the sharpest loss, because the live-call numerator has no substitute.
Scheduled counts still come from OnceHub, so a show rate cannot be computed at all without a
count of calls that actually happened.
