#!/usr/bin/env python3
"""Permission guard: refuses unless the streamer is marked `approved` in permissions.md.

Usage: guard.py STREAMER [--permissions FILE]   (exit 0 = approved, exit 1 = refuse)
Importable: from guard import is_approved
A streamer is approved only when their table row contains the exact cell `approved`.
`replied`, `contacted`, `candidate` and anything else all refuse.
"""
import os, sys

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "permissions.md")


def is_approved(streamer, path=DEFAULT):
    name = streamer.strip().lower()
    for line in open(path, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0].lower() == name and "approved" in [c.lower() for c in cells[1:]]:
            return True
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[sys.argv.index("--permissions") + 1] if "--permissions" in sys.argv else DEFAULT
    ok = is_approved(sys.argv[1], path)
    print(f"{sys.argv[1]}: {'APPROVED' if ok else 'NOT approved: refusing'}")
    sys.exit(0 if ok else 1)
