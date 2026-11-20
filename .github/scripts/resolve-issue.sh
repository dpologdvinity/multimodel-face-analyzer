#!/usr/bin/env bash
# Close the open issue a scheduled check filed (report-issue.sh) once the check passes again.
# Usage: resolve-issue.sh TITLE BODY. Needs GH_TOKEN with issues: write and GH_REPO.
set -euo pipefail
title=$1
body=$2
number=$(gh issue list --state open --search "\"$title\" in:title" --json number,title \
  --jq "map(select(.title == \"$title\"))[0].number // empty")
if [ -n "$number" ]; then
  gh issue close "$number" --reason completed --comment "$body"
fi
