#!/usr/bin/env bash
# Post the QA test payload at a Callix custom webhook endpoint and show what comes back.
#
#   ./scripts/callix/post-test.sh https://app.callix.io/api/webhooks/<your-endpoint-id>
#
# The response BODY is the thing to read, not just the status code. It decides whether
# Callix can hand call data back to a caller, which is the open question in CALLIX-MIGRATION.md.

set -euo pipefail
URL="${1:?Pass the endpoint URL Callix generated for you}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "POST $URL"
echo "---------- response ----------"
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  --data @"$DIR/sample-payload.json" \
  -D /tmp/callix-headers.txt \
  -w '\n---------- status: %{http_code}  time: %{time_total}s ----------\n' \
  | tee /tmp/callix-response.json

echo
echo "Response headers:"; cat /tmp/callix-headers.txt

echo
echo "Verdict:"
if grep -qi 'transcript\|speaker\|segments' /tmp/callix-response.json 2>/dev/null; then
  echo "  The response carries transcript content. A per-call read path EXISTS."
  echo "  Remaining gap is enumeration: ask Callix how to list calls for a date."
else
  echo "  The response is an acknowledgement only, with no call content returned."
  echo "  No read path here. Callix ingests; it does not hand data back to a caller."
fi
