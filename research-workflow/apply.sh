#!/bin/bash
# Deprecated overlay installer. This script is intentionally read-only.
#
# Usage:
#   ./apply.sh <project-dir>             # refuse legacy mutation and print migration command
#   ./apply.sh <project-dir> --dry-run   # compare the project workflow with this release
#   ./apply.sh <project-dir> --verify    # verify an official marketplace installation

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MASTER_WORKFLOW="$SCRIPT_DIR/workflow.md"
EXPECTED_TRELLIS_VERSION="0.6.16"
WORKFLOW_ID="research"
MARKETPLACE_SOURCE='gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0'

MODE="${2:-apply}"
MODE="${MODE#--}"
case "$MODE" in
  apply|dry-run|verify) ;;
  *) echo "FATAL: unknown mode: $MODE (use apply, --dry-run, or --verify)"; exit 2 ;;
esac

PROJ="${1:?usage: apply.sh <project-dir> [--dry-run|--verify]}"
T="$PROJ/.trellis"

[ -d "$T" ] || { echo "FATAL: $T not found (not a Trellis project?)"; exit 1; }

print_migration() {
  echo "Use the Trellis marketplace workflow command with a published release tag:"
  echo "  trellis workflow --template $WORKFLOW_ID --marketplace $MARKETPLACE_SOURCE --create-new"
  echo "Review .trellis/workflow.md.new, then rerun without --create-new and add --force only when replacement is intended."
}

if [ "$MODE" = apply ]; then
  echo "FATAL: apply mode is deprecated and performs no writes."
  echo "The old overlay could replace Trellis-managed runtime files with older copies."
  print_migration
  exit 2
fi

command -v trellis >/dev/null 2>&1 || { echo "FATAL: trellis CLI not found"; exit 1; }
ACTUAL_TRELLIS_VERSION="$(trellis --version)"
if [ "$ACTUAL_TRELLIS_VERSION" != "$EXPECTED_TRELLIS_VERSION" ]; then
  echo "FATAL: this workflow targets Trellis $EXPECTED_TRELLIS_VERSION; found $ACTUAL_TRELLIS_VERSION."
  echo "Obtain a workflow release compatible with the installed CLI before replacing workflow.md."
  exit 1
fi

if [ ! -f "$T/workflow.md" ]; then
  echo "FATAL: $T/workflow.md not found"
  exit 1
fi

if cmp -s "$T/workflow.md" "$MASTER_WORKFLOW"; then
  echo "OK: .trellis/workflow.md matches the research workflow source."
else
  if [ "$MODE" = dry-run ]; then
    echo "WOULD REPLACE: .trellis/workflow.md differs from the research workflow source."
    print_migration
    exit 0
  fi
  echo "FAIL: .trellis/workflow.md differs from the research workflow source."
  exit 1
fi

open_blocks=$(grep -c '^\[workflow-state:' "$T/workflow.md" || true)
close_blocks=$(grep -c '^\[/workflow-state:' "$T/workflow.md" || true)
if [ "$open_blocks" != "$close_blocks" ] || [ "$open_blocks" -lt 7 ]; then
  echo "FAIL: workflow-state blocks are not balanced ($open_blocks open / $close_blocks close)."
  exit 1
fi

if [ -f "$T/.template-hashes.json" ] && grep -q '"\.trellis/workflow\.md"' "$T/.template-hashes.json"; then
  echo "FAIL: .trellis/workflow.md remains Trellis hash-managed; reinstall through 'trellis workflow'."
  exit 1
fi

echo "PASS: workflow matches, state blocks are balanced, Trellis is $EXPECTED_TRELLIS_VERSION, and workflow.md is user-managed."
