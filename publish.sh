#!/usr/bin/env bash
#
# publish.sh — safe, rollback-able deploy for diligentservices.io
#
# Run this ON THE WEB SERVER (Hetzner), from inside the site repo:
#   cd /var/www/diligentservices/diligentservices-quarto && ./publish.sh
#
# What it does, in order:
#   1. Backs up the current live _site to _site.bak.<timestamp>
#   2. Records the current git commit (so we can roll back to it)
#   3. Fast-forward pulls origin/main
#   4. Activates the Python venv (required, or computational blog posts fail)
#   5. Renders the site
# If ANY step fails, it automatically restores the previous commit AND the
# previous _site, so the live site is never left half-broken.
#
set -euo pipefail
cd "$(dirname "$0")"

STAMP="$(date +%Y%m%d-%H%M%S)"
PREV_COMMIT="$(git rev-parse HEAD)"
BACKUP="_site.bak.$STAMP"

echo "==> Current live commit: $PREV_COMMIT"
if [ -d _site ]; then
  echo "==> Backing up live _site -> $BACKUP"
  cp -a _site "$BACKUP"
fi

restore() {
  echo "!! Publish FAILED. Restoring the previous version."
  git reset --hard "$PREV_COMMIT" || true
  if [ -d "$BACKUP" ]; then rm -rf _site && mv "$BACKUP" _site; fi
  echo "!! Live site restored to $PREV_COMMIT. Nothing broken is live."
  exit 1
}
trap restore ERR

echo "==> Pulling origin/main (fast-forward only)"
git fetch origin
git merge --ff-only origin/main

echo "==> Activating venv"
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Rendering"
quarto render

trap - ERR
echo ""
echo "==> Published successfully."
echo "    Previous version was: $PREV_COMMIT"
echo "    Roll back any time with:  ./rollback.sh $PREV_COMMIT"
echo "    (A copy of the old site is also kept at: $BACKUP)"
