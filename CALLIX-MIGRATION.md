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

## 5. What I need before writing any of it

1. **Does the Callix webhook payload carry the transcript?** This is the one that decides
   everything. 44 call sites need transcript text. If the payload is only "call ended" with an
   id, then transcripts have to be retrievable some other way, and with no API key that may not
   be possible at all. A sample payload (redacted) answers this in one look.
2. **Which events does Callix emit, and what are the field names?** `call.completed`,
   `transcript.ready`, something else. The schema above is a guess at shapes, not names.
3. **Where should the receiver live?** A Supabase Edge Function is the natural answer since
   Supabase is already here: it gives an HTTPS endpoint and writes straight to the tables, with
   no new host. The alternative is wherever you want to run it. (The retired
   `commandcenter.aiautomating.com` app was exactly this sort of thing, which is why it went
   when the previous director did.)
4. **Can Callix replay or export past calls?** Decides whether the look-back reports resume
   immediately or after their window fills.

Worth confirming too: is Supabase staying? The README treats it as optional if the
`lead_quality` pipeline is dropped. Under this design it stops being optional, because it
becomes the only record of a call ever happening.
