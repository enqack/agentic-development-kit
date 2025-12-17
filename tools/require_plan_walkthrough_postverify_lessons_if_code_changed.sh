#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${GITHUB_BASE_REF:-}" ]]; then
  git fetch origin "${GITHUB_BASE_REF}" --depth=1
  BASE="origin/${GITHUB_BASE_REF}"
  HEAD="HEAD"
else
  BASE="HEAD~1"
  HEAD="HEAD"
fi

CHANGED="$(git diff --name-only "${BASE}" "${HEAD}" || true)"
NON_CODE_RE='^(docs/|\\.agents/|artifacts/|tools/|\\.github/|.*\\.md$)'

CODE_CHANGED=0
while IFS= read -r f; do
  [[ -z "${f}" ]] && continue
  if [[ ! "${f}" =~ ${NON_CODE_RE} ]]; then
    CODE_CHANGED=1
    break
  fi
done <<< "${CHANGED}"

if [[ "${CODE_CHANGED}" -eq 0 ]]; then
  echo "gate: no code changes; no plan/walkthrough/post-verify/lessons required"
  exit 0
fi

echo "gate: code changes detected; requiring plan + walkthrough + post_verify_report + lessons-learned"

for req in \
  "implementation_plan.json" \
  "walkthrough.md" \
  "artifacts/logs/post_verify_report.md" \
  "lessons-learned.md"
do
  [[ -f "${req}" ]] || { echo "gate: ERROR: missing ${req}" >&2; exit 1; }
done

echo "gate: OK"
