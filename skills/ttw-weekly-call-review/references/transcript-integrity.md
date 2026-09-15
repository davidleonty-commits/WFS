# Transcript integrity

Truncated and mis-attributed transcripts are the largest single source of wrong numbers on this report. A call scored from a transcript that stops before the price reads as "money never discussed" when the lead actually declined a lender two minutes later. On one audit, three of four truncated caches would have been misclassified.

Treat this as a data-quality gate, not a nicety.

## Getting a transcript

Primary route, always try first:

```
mcp__Avoma_MCP__get_meeting_transcript  uuid: <meeting_uuid>
```

**Pagination is mandatory**: loop on `next_cursor`, passing it back unchanged, until `has_more` is false. A single call truncates by 20 to 25 percent, and the close is at the end.

The output is large and usually persists to a file. Extract with python rather than reading the whole thing:

```bash
mkdir -p <scratch>/<TAG>
python3 -c "
import json
raw=json.load(open('<PERSISTED_PATH>'))
d=json.loads(raw[0]['text']) if isinstance(raw,list) else raw
print('uuid', d.get('meeting_uuid') or d.get('uuid'))
open('<scratch>/<TAG>/<CALL_ID>.txt','w').write(d.get('transcript') or '')
print('tlen', len(d.get('transcript') or ''))
"
```

**Always confirm the returned meeting uuid matches the one you asked for** before scoring anything.

## When the MCP transcript is unavailable

The Avoma MCP is intermittently blocked (403) and some meetings return notes before the transcript finishes processing.

Fallback order:

1. Retry `get_meeting_transcript` once; a transcript that was still processing often lands on the second attempt.
2. If the tool is unavailable or returns 403, call the REST API directly:
   `GET https://api.avoma.com/v1/transcriptions/` with `from_date` and `to_date`, header `Authorization: Bearer $AVOMA_API_KEY`.
   **Its `meeting` filter is silently ignored.** Narrow the date window to the call, page through, and match on `meeting_uuid` yourself.

If neither route has it, mark the row NA with `data_quality: "no transcript in Avoma"` and exclude it from bucket rates. Say so in the report rather than guessing.

## The completeness check

Run this on every transcript before grading. A transcript is suspect if any of these hold:

- it ends mid-sentence
- it ends before any price is stated
- its last timestamp is well short of `duration_seconds`
- its density falls outside roughly **800 to 1,200 characters per minute** of call

Density is a screen, not a verdict. Low density can be legitimate: dead air while a lead fills in a loan application, a long rep monologue merged into one block, or a genuinely quiet call. Check the ending and the timestamp span before concluding truncation. Equally, a transcript that starts late (say at 58:41) may simply be where the recording begins.

**Known trap:** several caches on this project were saved from only the first Avoma chunk. They look complete, end cleanly, and contain no price. If a call of 60+ minutes has no price anywhere, assume truncation and re-pull with pagination before concluding GREY.

Also note that price is often spoken without a dollar sign, as "8 k" or "8 g's" or "we will bring it out to 8". Searching for `$8,000` will falsely suggest the price is missing.

## Speaker labels

Labels are frequently wrong. Identify the rep by behaviour, not by name: the rep runs discovery, pitches, quotes the price, and asks for the sale.

Common patterns seen:

- **Fully swapped**: the rep's lines carry the lead's name and vice versa. Confirm by finding a line where one speaker addresses the other by name.
- **Device names**: the lead appears as "iPhone", "Zoom user", "Samsung SM-S938U", or an email handle.
- **Merged blocks**: one timestamped block containing both speakers, sometimes covering twenty minutes including the whole pricing segment.
- **Third parties absorbed**: a spouse's or sibling's lines attributed to the named lead. Check whose words the decisive quote actually is.
- **Avoma display names**: a lead may appear under an unrelated stored contact name. That is not necessarily a swap.

Record any label problem in the row's `data_quality` so the next reader is not misled.

## Mangled figures

Avoma routinely mangles numbers. Read for meaning and resolve from the rep's restatement where possible:

| Transcript | Actual |
|---|---|
| `$4.26`, `$4.26 and 96¢` | $426 / $426.96 per month |
| `$8` | $8,000 |
| `$5.50 ish`, `$5.80` | a 550 / 580 credit score |
| `$1.45` | $145,000 income |
| `$13.33`, `333` | $1,333 per month |
| `1,001 week` | $1,000 per week |
| `25,001 year` | $25,000 per year |
| `$2` | $2,000 |

A mangled line proves nothing on its own. Never let a garbled figure decide a bucket.

## Caching for reuse

Save every verified transcript to a per-batch scratch directory named for the call_id. **Never write to a shared path like `/tmp/t.txt`** — parallel agents overwrite each other and silently grade the wrong call. This has happened and produced a whole batch of wrong rows.

When reusing a cache from an earlier run, re-verify completeness. Some cached files on this project were abridged by a previous reader, with elisions or summarised parentheticals replacing real dialogue.
