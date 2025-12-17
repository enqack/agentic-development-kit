#!/usr/bin/env bash
set -euo pipefail

# Determine changed files in PR or push.
# For pull_request events, GITHUB_BASE_REF is set.
# For pushes, compare against previous commit.
if [[ -n "${GITHUB_BASE_REF:-}" ]]; then
  git fetch origin "${GITHUB_BASE_REF}" --depth=1
  BASE="origin/${GITHUB_BASE_REF}"
  HEAD="HEAD"
else
  BASE="HEAD~1"
  HEAD="HEAD"
fi

CHANGED="$(git diff --name-only "${BASE}" "${HEAD}" || true)"

# Define "code change" as anything that is not:
# - markdown/docs/rules/workflows
# - artifacts/*
# - tools/*
# - .github/*
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
  echo "gate: no code changes detected; plan/walkthrough not required"
  exit 0
fi

echo "gate: code changes detected; requiring implementation_plan.json and walkthrough.md"

if [[ ! -f "implementation_plan.json" ]]; then
  echo "gate: ERROR: implementation_plan.json is required when code changes are present" >&2
  exit 1
fi

if [[ ! -f "walkthrough.md" ]]; then
  echo "gate: ERROR: walkthrough.md is required when code changes are present" >&2
  exit 1
fi

echo "gate: OK"
