#!/usr/bin/env python3
"""
Compute the reporting window for the TTW weekly call review.

Default rule: Monday 00:00 through Sunday 23:59 of the current week.
If run mid-week, the window ends at the moment of the run.
Explicit dates always override.

Usage:
    python3 scripts/week_window.py                          # current week
    python3 scripts/week_window.py --now 2026-08-21T14:30   # pin "now" for testing
    python3 scripts/week_window.py --from 2026-08-01 --to 2026-08-17
    python3 scripts/week_window.py --weeks-ago 1            # last full week
"""
import argparse
from datetime import datetime, timedelta, timezone


def week_window(now: datetime, weeks_ago: int = 0):
    """Monday 00:00 -> min(now, Sunday 23:59:59) for the target week."""
    monday = (now - timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    monday -= timedelta(weeks=weeks_ago)
    sunday_end = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
    end = min(now, sunday_end) if weeks_ago == 0 else sunday_end
    return monday, end


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="frm")
    p.add_argument("--to", dest="to")
    p.add_argument("--now")
    p.add_argument("--weeks-ago", type=int, default=0)
    a = p.parse_args()

    if a.frm and a.to:
        start = datetime.fromisoformat(a.frm)
        end = datetime.fromisoformat(a.to)
        if end.hour == 0 and end.minute == 0:
            end = end.replace(hour=23, minute=59, second=59)
        label = "explicit range (overrides the weekly default)"
    else:
        now = datetime.fromisoformat(a.now) if a.now else datetime.now()
        start, end = week_window(now, a.weeks_ago)
        partial = a.weeks_ago == 0 and end < start + timedelta(days=6, hours=23)
        label = "current week, partial (Monday through now)" if partial else "full week (Monday through Sunday)"

    print(f"window     : {label}")
    print(f"human      : {start:%a %d %b %Y %H:%M}  ->  {end:%a %d %b %Y %H:%M}")
    print(f"days       : {(end - start).days + 1}")
    print(f"from (ISO) : {start.astimezone(timezone.utc):%Y-%m-%dT%H:%M:%SZ}")
    print(f"to   (ISO) : {end.astimezone(timezone.utc):%Y-%m-%dT%H:%M:%SZ}")
    print()
    print("State this window back to the requester before pulling.")


if __name__ == "__main__":
    main()
