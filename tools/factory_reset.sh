#!/usr/bin/env bash
set -euo pipefail

# factory_reset.sh - Destructively resets the repository history and artifacts.
# USE WITH CAUTION.

FORCE=false
INCLUDE_INTENT=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --force)
      FORCE=true
      shift
      ;;
    --include-intent)
      INCLUDE_INTENT=true
      shift
      ;;
    *)
      # Unknown options are ignored or could be handled
      ;;
  esac
done

if [ "$FORCE" != "true" ]; then
  echo "ERROR: This tool is destructive. You must pass --force to run it."
  echo "Usage: ./tools/factory_reset.sh --force [--include-intent]"
  echo "  --include-intent: Also delete artifacts/intent/project_intent.md"
  exit 1
fi

echo "WARNING: initiating FACTORY RESET. All history will be lost."

# 1. Clear history
echo "Cleaning artifacts/history..."
if [ -d "artifacts/history" ]; then
  # Delete all files in history root (history.md, history.ndjson, etc.)
  find artifacts/history -maxdepth 1 -type f -delete
  # Delete runs content
  if [ -d "artifacts/history/runs" ]; then
     find artifacts/history/runs -mindepth 1 -delete
     touch artifacts/history/runs/.gitkeep
  fi
  # Re-touch .gitkeep in history if needed (though we only deleted files)
fi

# 2. Clear journals
echo "Cleaning artifacts/journal..."
if [ -d "artifacts/journal" ]; then
  find artifacts/journal -mindepth 1 -delete
  touch artifacts/journal/.gitkeep
fi

# 3. Clear logs (preserve context_manifest.md? Plan said regenerate. Let's wipe all.)
echo "Cleaning artifacts/logs..."
if [ -d "artifacts/logs" ]; then
  find artifacts/logs -mindepth 1 -delete
  touch artifacts/logs/.gitkeep
fi
rm -f artifacts/logs/agent_mode.json

# 4. Clear diffs
echo "Cleaning artifacts/diffs..."
if [ -d "artifacts/diffs" ]; then
  find artifacts/diffs -mindepth 1 -delete
  touch artifacts/diffs/.gitkeep
fi

# 5. Clear test_results
echo "Cleaning artifacts/test_results..."
if [ -d "artifacts/test_results" ]; then
  find artifacts/test_results -mindepth 1 -delete
  touch artifacts/test_results/.gitkeep
fi

# 6. Truncate agent activity ledger
echo "Resetting agent_activity.jsonl..."
if [ -f "artifacts/agent_activity.jsonl" ]; then
  : > artifacts/agent_activity.jsonl
fi
# Also reset agent_mode.json (already handled in step 3, but being certain)
rm -f artifacts/logs/agent_mode.json

# 7. Intent
if [ "$INCLUDE_INTENT" = "true" ]; then
  echo "Deleting artifacts/intent/project_intent.md..."
  rm -f artifacts/intent/project_intent.md
else
  echo "Preserving artifacts/intent/project_intent.md (use --include-intent to wipe)."
fi

# 8. Reset AGENDA.md
echo "Resetting AGENDA.md..."
cat > AGENDA.md <<EOF
# Agenda

**Status**: Active

## Active Hypotheses

- None.

## Blockers

- None.

## Deferred Risks

- None.
EOF

echo "Factory reset complete. Artifacts are clean."
