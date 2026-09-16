#!/usr/bin/env python3
"""Scrub the previous director's identity out of every prompt and skill and write the new director's in.

Usage:
  python3 personalize.py --check                 # list every remaining trace of the previous director, change nothing
  python3 personalize.py replacements.json       # apply the replacements in place, then run the check
  python3 personalize.py replacements.json --dry-run   # show what would change, write nothing

replacements.json must have every key from replacements.template.json filled in.
Secrets (API keys, tokens) are NOT replacements and must never go into a prompt; they live in connector settings.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
TARGET_DIRS = ["scheduled-prompts", "cloud-routines", "skills"]

# Previous director's identity. Order matters: longest, most specific strings first.
PREVIOUS = [
    ("cayden.johnson@thewfsgroup.com",   "WFS_EMAIL"),
    ("cayden.johnson@ttwhizprogram.com", "TTW_EMAIL"),
    ("@cayden.johnson",                  "SLACK_HANDLE"),
    ("@cayden",                          "SLACK_HANDLE"),
    ("Work Board - Cayden",              "ASANA_BOARD_NAME"),
    ("Cayden Johnson's",                 "FULL_NAME_POSSESSIVE"),
    ("Cayden Johnson",                   "FULL_NAME"),
    ("CAYDO'S",                          "FIRST_NAME_POSSESSIVE_UPPER"),
    ("CAYDEN'S",                         "FIRST_NAME_POSSESSIVE_UPPER"),
    ("CAYDO",                            "FIRST_NAME_UPPER"),
    ("Caydo's",                          "FIRST_NAME_POSSESSIVE"),
    ("Cayden's",                         "FIRST_NAME_POSSESSIVE"),
    ("Caydo",                            "FIRST_NAME"),
    ("Cayden",                           "FIRST_NAME"),
    ("cayden",                           "FIRST_NAME_LOWER"),
    ("U092C85GA4D",                      "SLACK_USER_ID"),
    ("D092C868SPP",                      "SLACK_SELF_DM_ID"),
    ("23815275",                         "PIPEDRIVE_USER_ID"),
    ("apdwbbocldfsklvcwaqd",             "SUPABASE_PROJECT_ID"),
    ("2fac653e-7302-41bb-839a-a7b4b18cab1b", "BROWSER_DEVICE_ID"),
    # The client-facing channel is OFF LIMITS as a send destination under the new director. Every LIVE_TARGET that
    # pointed at it becomes the director's own DM; the director forwards by hand if the client needs it.
    ("LIVE_TARGET: #wfs-ttw-sales-mgmt-client", "CLIENT_LIVE_TARGET_REPLACEMENT"),
]
OPTIONAL = {"SUPABASE_PROJECT_ID", "ASANA_BOARD_NAME", "BROWSER_DEVICE_ID"}

# Anything matching these after the scrub means the previous director is still in the files.
RESIDUE = re.compile(r"cayden|caydo|U092C85GA4D|D092C868SPP|23815275|2fac653e-7302-41bb-839a-a7b4b18cab1b", re.I)

# Previous director's Supabase project. Either replaced with the new project id or the Supabase steps are deleted (TROUBLESHOOTING-REPLY.md section J).
SUPABASE_RESIDUE = re.compile(r"apdwbbocldfsklvcwaqd")

# Any remaining mention of the client channel must be a READ (e.g. the EOW skill reads it), never a send destination.
CLIENT_CHANNEL = re.compile(r"wfs-ttw-sales-mgmt-client|C098J2VG41E")

# Not identity, but must be gone before the tasks can run (see README Section 1A and TROUBLESHOOTING-REPLY.md).
CONNECTOR_RESIDUE = re.compile(r"Lovable[ _]WFS|WFS_MCP_TOKEN|REP_WFS_ID|commandcenter\.aiautomating\.com|mcp__scheduled-tasks__update_scheduled_task", re.I)


def files():
    for d in TARGET_DIRS:
        yield from sorted((ROOT / d).rglob("*.md"))


def derive(answers):
    """Fill the derived keys from the answers the director actually gives."""
    first = answers["FIRST_NAME"].strip()
    full = answers["FULL_NAME"].strip()
    handle = answers["SLACK_HANDLE"].strip()
    if not handle.startswith("@"):
        handle = "@" + handle
    out = dict(answers)
    out["SLACK_HANDLE"] = handle
    out["FULL_NAME_POSSESSIVE"] = full + "'s"
    out["FIRST_NAME_POSSESSIVE"] = first + "'s"
    out["FIRST_NAME_UPPER"] = first.upper()
    out["FIRST_NAME_POSSESSIVE_UPPER"] = first.upper() + "'S"
    out["FIRST_NAME_LOWER"] = first.lower()
    out["CLIENT_LIVE_TARGET_REPLACEMENT"] = f"LIVE_TARGET: {handle} (the director's own DM. The client channel #wfs-ttw-sales-mgmt-client is OFF LIMITS as a destination; never post there.)"
    if not out.get("TTW_EMAIL", "").strip():
        out["TTW_EMAIL"] = out["WFS_EMAIL"]
    return out


def check(verbose=True):
    hits = 0
    conn = 0
    supa = 0
    client = []
    for f in files():
        t = f.read_text(encoding="utf-8")
        for n, line in enumerate(t.splitlines(), 1):
            if RESIDUE.search(line):
                hits += 1
                if verbose:
                    print(f"IDENTITY  {f.relative_to(ROOT)}:{n}: {line.strip()[:140]}")
            if SUPABASE_RESIDUE.search(line):
                supa += 1
            if CLIENT_CHANNEL.search(line) and re.search(r"LIVE_TARGET|deliver|send|post", line, re.I) and not re.search(r"OFF LIMITS|never post|read", line, re.I):
                client.append(f"{f.relative_to(ROOT)}:{n}: {line.strip()[:140]}")
            if CONNECTOR_RESIDUE.search(line):
                conn += 1
    print(f"\n{hits} identity residue line(s), {supa} Supabase residue line(s), {conn} connector residue line(s) across {sum(1 for _ in files())} files.")
    if client:
        print(f"\nCLIENT CHANNEL: {len(client)} line(s) still look like a SEND to #wfs-ttw-sales-mgmt-client. Reads are fine; sends are forbidden. Confirm each is a read or rewrite it:")
        for c in client: print("  ", c)
    if supa:
        print(f"Supabase decision pending on {supa} line(s): either set SUPABASE_PROJECT_ID to the new project or delete those Supabase steps (TROUBLESHOOTING-REPLY.md section J).")
    if hits:
        print("NOT DONE: the previous director is still referenced. Fix the lines above (add a rule to PREVIOUS if it is a new pattern) and re-run.")
    else:
        print("Identity scrub complete: no trace of the previous director remains.")
    if conn:
        print(f"Connector swap still pending on {conn} line(s): run the Section 1A rewrite (Lovable WFS tools, REP_WFS_ID, WFS_MCP_TOKEN, update_scheduled_task). Use --check-connector to list them.")
    return hits == 0 and not client


def check_connector():
    for f in files():
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if CONNECTOR_RESIDUE.search(line):
                print(f"CONNECTOR {f.relative_to(ROOT)}:{n}: {line.strip()[:140]}")


def apply(answers, dry_run):
    a = derive(answers)
    missing = [k for _, k in PREVIOUS if not a.get(k, "").strip() and k not in OPTIONAL]
    if missing:
        sys.exit(f"replacements.json is incomplete. Fill in: {sorted(set(missing))}. Ask the director; do not guess.")
    for k, v in a.items():
        if v.strip().startswith("<") or v.strip().upper().startswith("REPLACE"):
            sys.exit(f"{k} still holds a placeholder ({v!r}). Ask the director for the real value.")
    total = 0
    for f in files():
        t = f.read_text(encoding="utf-8")
        new = t
        for old, key in PREVIOUS:
            val = a.get(key, "").strip()
            if not val:
                continue  # optional key left blank: leave the token for the residue check to flag
            new = new.replace(old, val)
        if new != t:
            n = sum(1 for x, y in zip(t.splitlines(), new.splitlines()) if x != y)
            total += n
            print(f"{'would change' if dry_run else 'changed'} {n:4d} line(s): {f.relative_to(ROOT)}")
            if not dry_run:
                f.write_text(new, encoding="utf-8")
    print(f"\n{total} line(s) {'would be ' if dry_run else ''}rewritten.")
    if not dry_run:
        print("\nRunning residue check...\n")
        check()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--check":
        sys.exit(0 if check() else 1)
    if args[0] == "--check-connector":
        check_connector(); sys.exit(0)
    answers = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    apply(answers, dry_run="--dry-run" in args)
