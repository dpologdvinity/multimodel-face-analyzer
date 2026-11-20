#!/usr/bin/env bash
# Keep one open issue per scheduled check: comment on it when the check fails again, open it
# (with the given labels) the first time. Usage: report-issue.sh TITLE BODY [LABEL...]
# Needs GH_TOKEN with issues: write and GH_REPO.
set -euo pipefail
title=$1
body=$2
shift 2
number=$(gh issue list --state open --search "\"$title\" in:title" --json number,title \
  --jq "map(select(.title == \"$title\"))[0].number // empty")
if [ -n "$number" ]; then
  gh issue comment "$number" --body "$body"
else
  label_args=()
  for label in "$@"; do label_args+=(--label "$label"); done
  gh issue create --title "$title" --body "$body" "${label_args[@]}"
fi
