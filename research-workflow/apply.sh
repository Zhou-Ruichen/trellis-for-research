#!/bin/bash
# Apply the research workflow overlay to a Trellis project.
#
# Usage:
#   ./apply.sh <project-dir>            # apply (with per-file backups, idempotent)
#   ./apply.sh <project-dir> --dry-run  # show what would change
#   ./apply.sh <project-dir> --verify   # read-only check that the overlay is in place
#
# Idempotent: files already identical to the master copies are left untouched
# and produce no backup. Backups use a timestamp suffix and are never cleaned
# by this script.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MASTER_WORKFLOW="$SCRIPT_DIR/workflow.md"
MASTER_IMPLEMENT="$SCRIPT_DIR/agents/implement.md"
MASTER_SKILL="$SCRIPT_DIR/skills/trellis-research-check/SKILL.md"

MODE="${2:-apply}"
MODE="${MODE#--}"
PROJ="${1:?usage: apply.sh <project-dir> [--dry-run|--verify]}"
T="$PROJ/.trellis"

[ -d "$T" ] || { echo "FATAL: $T not found (not a Trellis project?)"; exit 1; }

ts() { date +%Y-%m-%dT%H-%M-%S; }

# install <dest> <src>: backup then copy if different; skip silently if identical
install_file() {
  local dest="$1" src="$2"
  if [ ! -f "$dest" ]; then
    echo "  INSTALL (new)  ${dest#$PROJ/}"
    if [ "$MODE" = apply ]; then
      mkdir -p "$(dirname "$dest")"
      cp "$src" "$dest"
    fi
    return 0
  fi
  if cmp -s "$dest" "$src"; then
    echo "  OK (same)      ${dest#$PROJ/}"
    return 0
  fi
  echo "  REPLACE        ${dest#$PROJ/}"
  if [ "$MODE" = apply ]; then
    cp "$dest" "${dest}.backup-$(ts)"
    cp "$src" "$dest"
  fi
  return 0
}

# The official trellis-check skill is NOT patched. Routing lives entirely in
# workflow.md (state blocks, Phase 2.2, Active Task Routing) and in the
# trellis-research-check skill's own description.

verify_state_blocks() {
  local n o
  n=$(grep -c "^\[workflow-state:" "$T/workflow.md" || true)
  o=$(grep -c "^\[/workflow-state:" "$T/workflow.md" || true)
  if [ "$n" = "$o" ] && [ "$n" -ge 6 ]; then
    echo "  OK             workflow-state blocks parseable ($n blocks)"
  else
    echo "  FAIL           workflow-state blocks: $n open / $o close"
    return 1
  fi
}

echo "== research-workflow overlay: $PROJ ($MODE)"

if [ "$MODE" = verify ]; then
  ok=0
  cmp -s "$T/workflow.md" "$MASTER_WORKFLOW" && echo "  OK             workflow.md matches master" || { echo "  FAIL           workflow.md differs from master"; ok=1; }
  grep -q "Final check per mode" "$T/agents/implement.md" 2>/dev/null && echo "  OK             implement agent patched" || { echo "  FAIL           implement agent not patched"; ok=1; }
  [ -f "$PROJ/.claude/skills/trellis-research-check/SKILL.md" ] && echo "  OK             research-check skill installed" || { echo "  FAIL           research-check skill missing"; ok=1; }
  verify_state_blocks || ok=1
  [ $ok = 0 ] && echo "== verify: PASS" || echo "== verify: FAIL"
  exit $ok
fi

install_file "$T/workflow.md" "$MASTER_WORKFLOW"
install_file "$T/agents/implement.md" "$MASTER_IMPLEMENT"
install_file "$PROJ/.claude/skills/trellis-research-check/SKILL.md" "$MASTER_SKILL"
if [ "$MODE" = apply ]; then
  verify_state_blocks
  echo "== applied. Restart AI sessions in this project to pick up the new workflow."
fi
