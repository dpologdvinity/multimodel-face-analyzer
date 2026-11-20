#!/usr/bin/env bash
# Add labels that already exist in the repository to an issue; the triage agent's only write
# action. Unknown labels are skipped rather than created. Usage: add-labels.sh NUMBER LABEL...
# Needs GH_TOKEN with issues: write and GH_REPO.
set -euo pipefail
number=$1
shift
[[ "$number" =~ ^[0-9]+$ ]] || { echo "not an issue number: $number" >&2; exit 2; }
known=$(gh label list --limit 200 --json name --jq '.[].name')
for label in "$@"; do
  if grep -qxF -- "$label" <<<"$known"; then
    gh issue edit "$number" --add-label "$label"
  else
    echo "skipped unknown label: $label" >&2
  fi
done
