#!/usr/bin/env python3
"""
QA gates for the TTW weekly call review. Every gate must pass before reporting numbers.

Usage:
    python3 scripts/qa_gates.py rows.json [--expected-calls N] [--from YYYY-MM-DD --to YYYY-MM-DD]

Expects a JSON array of row objects with at least:
    call_id, lead_name, rep_name, bucket, outcome, dq_evidence,
    evidence_type, verification, rep_performance, _started, _dur
"""
import argparse
import collections
import json
import re
import sys

BUCKETS = {"RED", "GREEN", "GREY", "BLUE", "ORANGE", "NA"}
OUTCOMES = {"closed_full", "closed_base44", "follow_up", "no_close", "not_a_sales_call", "no_data"}
CLOSED = {"closed_full", "closed_base44"}
EVIDENCE_REQUIRED = {"RED", "ORANGE"}
GREY_TEXT = "No financial reference on the call"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("rows")
    p.add_argument("--expected-calls", type=int)
    p.add_argument("--from", dest="frm")
    p.add_argument("--to", dest="to")
    a = p.parse_args()

    rows = json.load(open(a.rows))
    fails, warns = [], []

    def fail(gate, msg):
        fails.append(f"[{gate}] {msg}")

    def warn(gate, msg):
        warns.append(f"[{gate}] {msg}")

    # 1 row count and duplicates
    ids = [r.get("call_id") for r in rows]
    dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dupes:
        fail("1 rows", f"duplicate call_ids: {dupes[:5]}")
    if any(not i for i in ids):
        fail("1 rows", "rows with a missing call_id")
    if a.expected_calls and len(rows) != a.expected_calls:
        warn("1 rows", f"{len(rows)} rows vs {a.expected_calls} expected (check exclusions)")

    # 2 evidence on RED and ORANGE
    missing = [r["lead_name"] for r in rows
               if r.get("bucket") in EVIDENCE_REQUIRED and not (r.get("dq_evidence") or "").strip()]
    if missing:
        fail("2 evidence", f"{len(missing)} RED/ORANGE rows with no evidence: {missing[:5]}")

    # 3 GREY hygiene
    bad_grey = [r["lead_name"] for r in rows if r.get("bucket") == "GREY"
                and ((r.get("dq_evidence") or "").strip() != GREY_TEXT
                     or (r.get("evidence_type") or "none") != "none")]
    if bad_grey:
        fail("3 grey", f"{len(bad_grey)} GREY rows carrying real evidence: {bad_grey[:5]}")

    # 4 bucket totals
    bc = collections.Counter(r.get("bucket") for r in rows)
    unknown = set(bc) - BUCKETS
    if unknown:
        fail("4 buckets", f"unknown bucket values: {unknown}")
    if sum(bc.values()) != len(rows):
        fail("4 buckets", "bucket counts do not sum to row count")

    # 5 closes reconcile
    closes = sum(1 for r in rows if r.get("outcome") in CLOSED)
    blue_orange = bc["BLUE"] + bc["ORANGE"]
    if closes != blue_orange:
        mism = [(r["lead_name"], r.get("outcome"), r.get("bucket")) for r in rows
                if (r.get("outcome") in CLOSED) != (r.get("bucket") in {"BLUE", "ORANGE"})]
        fail("5 closes", f"{closes} closes vs {blue_orange} BLUE+ORANGE; mismatched: {mism[:5]}")

    # 6 rep names
    bad_reps = [r.get("call_id") for r in rows
                if not r.get("rep_name") or r["rep_name"].upper() == "UNKNOWN"]
    if bad_reps:
        fail("6 reps", f"{len(bad_reps)} rows with unresolved rep names")

    # 7 dates in window
    if a.frm and a.to:
        out = [r["lead_name"] for r in rows
               if not (a.frm <= str(r.get("_started", ""))[:10] <= a.to)]
        if out:
            fail("7 dates", f"{len(out)} rows outside {a.frm}..{a.to}: {out[:5]}")

    # 8 rep scores
    bad_scores = []
    for r in rows:
        v = r.get("rep_performance")
        if v in (None, ""):
            continue
        if not isinstance(v, (int, float)) or not (1 <= v <= 10):
            bad_scores.append((r["lead_name"], v))
    if bad_scores:
        fail("8 scores", f"scores outside 1-10 or zero-as-missing: {bad_scores[:5]}")

    # 9 evidence timestamps inside call duration
    ts = re.compile(r"\[(\d+):(\d{2})(?::(\d{2}))?\]")
    bad_ts = []
    for r in rows:
        dur = r.get("_dur")
        if not dur:
            continue
        for m in ts.finditer(r.get("dq_evidence") or ""):
            g = [int(x) if x else 0 for x in m.groups()]
            mins = g[0] * 60 + g[1] if g[2] else g[0]
            if mins > dur + 2:
                bad_ts.append((r["lead_name"], m.group(0), f"{dur}min call"))
    if bad_ts:
        fail("9 timestamps", f"evidence timestamps past end of call (quote may be from another call): {bad_ts[:5]}")

    # 10 verification coverage
    novf = sum(1 for r in rows if not (r.get("verification") or "").strip())
    if novf:
        fail("10 verification", f"{novf} rows with no verification recorded")

    # summary
    grade = sum(v for k, v in bc.items() if k != "NA")
    fdq = bc["RED"] + bc["ORANGE"]
    print("=" * 60)
    print(f"rows {len(rows)} | gradeable {grade} | closes {closes}")
    print("buckets:", dict(bc))
    if grade:
        print(f"FDQ (RED+ORANGE): {fdq} = {fdq/grade*100:.1f}% of gradeable")
    print("verification:", dict(collections.Counter(r.get("verification") for r in rows)))
    print("=" * 60)
    for w in warns:
        print("WARN ", w)
    for f in fails:
        print("FAIL ", f)
    if fails:
        print(f"\n{len(fails)} gate(s) FAILED. Do not report these numbers until fixed.")
        sys.exit(1)
    print("\nAll QA gates passed.")


if __name__ == "__main__":
    main()
