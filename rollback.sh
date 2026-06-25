#!/usr/bin/env bash
#
# rollback.sh — revert the LIVE site to a previous version and re-render.
#
# Run this ON THE WEB SERVER (Hetzner), from inside the site repo:
#   ./rollback.sh <git-commit-sha>
#
# Find a commit to roll back to with:  git log --oneline
# (publish.sh also prints the previous commit each time it runs.)
#
set -euo pipefail
cd "$(dirname "$0")"

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  echo "Usage: ./rollback.sh <commit-sha>"
  echo "Recent commits:"
  git --no-pager log --oneline -10
  exit 1
fi

echo "==> Rolling the live site back to $TARGET"
git checkout "$TARGET"
# shellcheck disable=SC1091
source .venv/bin/activate
quarto render
echo ""
echo "==> Rolled back and re-rendered at $TARGET."
echo "    You are now in 'detached HEAD'. To return to the latest published"
echo "    version when you're ready:  git checkout main && ./publish.sh"
