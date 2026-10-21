#!/usr/bin/env bash
# Commit and push any workspace changes. Silent when nothing changed.
set -euo pipefail
cd "$(dirname "$0")/.."
git add -A
if git diff --cached --quiet; then
  echo "no changes"
  exit 0
fi
git commit -q -m "Workspace backup $(date -u +%Y-%m-%dT%H:%MZ)"
git push -q origin main
echo "pushed"
