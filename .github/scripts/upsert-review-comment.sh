#!/usr/bin/env bash
# Create or update the Claude review's summary comment on a pull request, found by its marker
# (not by recency, so an @claude reply posted in between is never overwritten).
# Usage: upsert-review-comment.sh PR_NUMBER BODY. Needs GH_TOKEN and GH_REPO.
set -euo pipefail
number=$1
body=$2
[[ "$number" =~ ^[0-9]+$ ]] || { echo "not a pull request number: $number" >&2; exit 2; }
marker='<!-- claude-review-summary -->'
id=$(gh api "repos/$GH_REPO/issues/$number/comments" --paginate \
  --jq "map(select(.body | startswith(\"$marker\"))) | last | .id // empty" | tail -n 1)
if [ -n "$id" ]; then
  gh api -X PATCH "repos/$GH_REPO/issues/comments/$id" -f body="$marker
$body" > /dev/null
else
  gh pr comment "$number" --body "$marker
$body" > /dev/null
fi
