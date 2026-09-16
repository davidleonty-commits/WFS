#!/usr/bin/env python3
"""Preflight the OnceHub assumptions the rewritten prompts depend on.

Read-only. Prints structure and counts only, never booking contents, so it is safe
to paste the output into a chat or a ticket.

Usage:
    export ONCEHUB_API_KEY=...        # never hardcode it, never commit it
    python3 scripts/verify-oncehub.py

What it checks, and why each one matters to a prompt:

1. Auth works at all.
2. The pagination cursor's real field name. Every list sweep in the lead flow,
   show rate and webinar prompts says "follow `next` until it is null"; if this
   account calls it something else, those prompts need the real name.
3. Whether `starting_time.gt` / `.lt` are accepted and `starting_time_from` /
   `_to` are rejected. Both show rate reports and the webinar report are written
   around exactly that split (documented by the outgoing director on 2026-07-27).
4. Whether a booking carries `booking_page.master_page` and `in_trash`. The
   per-master-page grouping and the unattributed-booking rescue both depend on
   those two fields existing on the booking object.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

KEY = os.environ.get("ONCEHUB_API_KEY")
if not KEY:
    sys.exit("ONCEHUB_API_KEY is not set. Export it first; do not edit it into this file.")

BASE = "https://api.oncehub.com/v2"


def get(path, params=None):
    """Return (status, parsed_body_or_text). Never raises on an HTTP error status."""
    url = BASE + path
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers={"API-Key": KEY, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass
        return e.code, body
    except Exception as e:  # network, DNS, proxy
        return None, f"{type(e).__name__}: {e}"


def envelope(body):
    """Describe a list response's shape without printing any row contents."""
    if not isinstance(body, dict):
        return "not a JSON object"
    rows = body.get("data")
    parts = [f"top-level keys: {sorted(body)}"]
    if isinstance(rows, list):
        parts.append(f"rows: {len(rows)}")
        if rows and isinstance(rows[0], dict):
            parts.append(f"row fields: {sorted(rows[0])}")
    cursors = {k: ("<present>" if v else v) for k, v in body.items() if k != "data"}
    parts.append(f"non-data fields: {cursors}")
    return "\n   ".join(parts)


print("0. REACHABILITY  (is the host allowed out of this environment at all?)")
status, body = get("/booking-calendars", {"limit": "1"})
if status is None:
    print(f"   {body}")
    sys.exit(
        "   The request never reached OnceHub. If this says 'CONNECT tunnel failed, response 403',\n"
        "   api.oncehub.com is not on this environment's network policy allowlist. That is a settings\n"
        "   change at claude.ai -> Code -> Environments, not something a key or this script can fix.\n"
        "   Add api.oncehub.com (and app.callix.io, which is blocked the same way), then re-run."
    )
print(f"   reached OnceHub, HTTP {status}")

print("\n1. AUTH and BOOKING CALENDARS  (GET /v2/booking-calendars)")
print(f"   HTTP {status}")
if status == 404:
    sys.exit("   404 here means the resource name is wrong for this account; v1 called it /master_pages.")
if status in (401, 403):
    sys.exit("   Auth rejected. Check the key, and that it has not been rotated.")
if status != 200:
    print(f"   {body}")
    sys.exit("   Stop here: fix this before checking anything else.")
print("   " + envelope(body))
print("   -> the prompts say 'paginate to the end'. Confirm which field above carries the cursor.")

print("\n2. BOOKINGS with the documented time operators  (starting_time.gt / .lt)")
now = datetime.now(timezone.utc)
lo = (now - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
hi = now.strftime("%Y-%m-%dT%H:%M:%SZ")
status, body = get("/bookings", {"starting_time.gt": lo, "starting_time.lt": hi, "limit": "5"})
print(f"   HTTP {status}  (expect 200: the prompts rely on these operators)")
if status == 200:
    print("   " + envelope(body))
    rows = body.get("data") or []
    if rows:
        row = rows[0]
        bp = row.get("booking_page")
        print(f"   in_trash present: {'in_trash' in row}")
        print(f"   booking_page type: {type(bp).__name__}")
        if isinstance(bp, dict):
            print(f"   booking_page fields: {sorted(bp)}")
            print(f"   master_page present on booking_page: {'master_page' in bp}")
        else:
            print("   NOTE: booking_page is not an object here. The grouping step in the show rate")
            print("         and lead flow prompts assumes booking_page.master_page; if it is a bare")
            print("         id, those prompts need a /v2/booking_pages/{id} lookup to group.")
    else:
        print("   No bookings in the last 2 days, so the field check is inconclusive.")
        print("   Re-run with a wider window before trusting the grouping assumptions.")
else:
    print(f"   {body}")
    print("   -> If this is a 400, the operator names differ on this account and five prompts")
    print("      need their sweep parameters corrected.")

print("\n3. BOOKINGS with the parameters the prompts say are REJECTED  (starting_time_from / _to)")
status, body = get("/bookings", {"starting_time_from": lo, "starting_time_to": hi, "limit": "5"})
print(f"   HTTP {status}  (expect 400 'Received unknown parameter')")
if status == 200:
    print("   These now WORK. That is a simplification, not a break: the prompts filter")
    print("   client-side after a full sweep, which stays correct either way.")
else:
    print(f"   {body if isinstance(body, str) else json.dumps(body)[:200]}")

print("\n4. CALLIX  (same network policy; see CALLIX-MIGRATION.md section 0a)")
ck = os.environ.get("CALLIX_API_KEY")
if not ck:
    print("   CALLIX_API_KEY not set, skipping.")
else:
    for base in ("https://app.callix.io/api/v1", "https://api.callix.io/v1"):
        req = urllib.request.Request(
            base + "/calls?limit=1",
            headers={"Authorization": f"Bearer {ck}", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                b = json.loads(r.read().decode())
            print(f"   {base} -> HTTP {r.status}")
            print("   " + envelope(b))
            print("   -> paste the row fields above into every CALLIX FIELD NAMES UNVERIFIED gate,")
            print("      map transcript_ready / meeting_state / organizer_email / start_at /")
            print("      is_internal / attendees to their real names, then delete the gates.")
            break
        except urllib.error.HTTPError as e:
            print(f"   {base} -> HTTP {e.code} {e.read().decode()[:120]}")
        except Exception as e:
            print(f"   {base} -> {type(e).__name__}: {e}")

print("\nDone. Nothing above contains a booking\'s contents or a customer\'s details.")
