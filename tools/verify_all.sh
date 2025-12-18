#!/usr/bin/env bash
set -euo pipefail

mkdir -p artifacts/logs artifacts/test_results docs/exec/runs docs/intent

ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

run_log() {
  local name="$1"
  shift
  local out="artifacts/logs/${name}.log"
  echo "==> ${name} @ ${ts}" | tee "${out}"
  echo "+ $*" | tee -a "${out}"
  ( "$@" ) >>"${out}" 2>&1
  echo "==> OK: ${name}" | tee -a "${out}"
}

# Baseline template presence
if [ -f tools/template_baseline_lint.py ]; then
  run_log "template_baseline_lint" python3 tools/template_baseline_lint.py
fi

# Mechanical enforcement: workflows must require intent (except establish-intent)
if [ -f tools/workflow_intent_lint.py ]; then
  run_log "workflow_intent_lint" python3 tools/workflow_intent_lint.py
fi

# Panic messaging style enforcement (no override prompts)
if [ -f tools/panic_style_lint.py ]; then
  run_log "panic_style_lint" python3 tools/panic_style_lint.py
fi

# Intent must exist for any real work. (Fail closed.)
if [ -f tools/intent_lint.py ]; then
  run_log "intent_lint" python3 tools/intent_lint.py
fi

# Lints
if [ -f tools/agenda_lint.py ]; then run_log "agenda_lint" python3 tools/agenda_lint.py; fi
if [ -f tools/context_manifest_lint.py ] && [ -f artifacts/logs/context_manifest.md ]; then
  run_log "context_manifest_lint" python3 tools/context_manifest_lint.py
fi
if [ -f tools/post_verify_lint.py ] && [ -f artifacts/logs/post_verify_report.md ]; then
  run_log "post_verify_lint" python3 tools/post_verify_lint.py
fi
if [ -f tools/lessons_lint.py ] && [ -f docs/exec/lessons-learned.md ]; then
  run_log "lessons_lint" python3 tools/lessons_lint.py
fi
if [ -f tools/walkthrough_lint.py ]; then
  run_log "walkthrough_lint" python3 tools/walkthrough_lint.py
fi
if [ -f tools/run_artifacts_lint.py ] && [ -d docs/exec/runs ]; then
  run_log "run_artifacts_lint" python3 tools/run_artifacts_lint.py
fi
if [ -f tools/evidence_location_lint.py ]; then
  run_log "evidence_location_lint" python3 tools/evidence_location_lint.py
fi

# Plan lint: validate run-dir plan if present, else root
if [ -f tools/plan_lint.py ]; then
  if ls docs/exec/runs/**/implementation_plan.json >/dev/null 2>&1; then
    run_log "plan_lint_run" python3 tools/plan_lint.py --run
  elif [ -f implementation_plan.json ]; then
    run_log "plan_lint_root" python3 tools/plan_lint.py
  fi
fi

# Project tests (language-agnostic hook)
if [ -x tools/test.sh ]; then
  run_log "project_tests" tools/test.sh
else
  echo "verify_all: tools/test.sh not present/executable; skipping project tests"
fi

echo "verify_all: OK"
