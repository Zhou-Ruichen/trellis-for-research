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

# patch the official trellis-check skill description (one line, idempotent)
patch_check_description() {
  local f="$PROJ/.claude/skills/trellis-check/SKILL.md"
  [ -f "$f" ] || { echo "  SKIP           .claude/skills/trellis-check/SKILL.md (not installed)"; return; }
  if grep -q "exploratory experiments use trellis-research-check" "$f"; then
    echo "  OK (patched)   .claude/skills/trellis-check/SKILL.md"
    return
  fi
  echo "  PATCH          .claude/skills/trellis-check/SKILL.md (description)"
  [ "$MODE" = apply ] || return 0
  cp "$f" "$f.backup-$(ts)"
  python3 - "$f" <<'PYEOF'
import sys, re
p = sys.argv[1]
s = open(p).read()
s = s.replace(
    "before committing changes, or to catch context drift during long sessions.\"",
    "before committing changes, or to catch context drift during long sessions. "
    "For durable engineering changes; exploratory experiments use trellis-research-check instead.\"",
    1,
)
open(p, "w").write(s)
PYEOF
}

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
  grep -q "Closing pass per mode" "$T/agents/implement.md" 2>/dev/null && echo "  OK             implement agent patched" || { echo "  FAIL           implement agent not patched"; ok=1; }
  [ -f "$PROJ/.claude/skills/trellis-research-check/SKILL.md" ] && echo "  OK             research-check skill installed" || { echo "  FAIL           research-check skill missing"; ok=1; }
  grep -q "exploratory experiments use trellis-research-check" "$PROJ/.claude/skills/trellis-check/SKILL.md" 2>/dev/null && echo "  OK             check skill routing patch present" || { echo "  FAIL           check skill routing patch missing"; ok=1; }
  verify_state_blocks || ok=1
  [ $ok = 0 ] && echo "== verify: PASS" || echo "== verify: FAIL"
  exit $ok
fi

install_file "$T/workflow.md" "$MASTER_WORKFLOW"
install_file "$T/agents/implement.md" "$MASTER_IMPLEMENT"
install_file "$PROJ/.claude/skills/trellis-research-check/SKILL.md" "$MASTER_SKILL"
patch_check_description
if [ "$MODE" = apply ]; then
  verify_state_blocks
  echo "== applied. Restart AI sessions in this project to pick up the new workflow."
fi
