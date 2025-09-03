#!/usr/bin/env bash
set -euo pipefail

export GIT_PAGER=cat
export GH_PAGER=cat
export PAGER=cat
export LESS=FRSX

echo "=== Terminal Diagnostics ==="
echo "Date: $(date -Is)"
echo "User: $(id -un) ($(id -u))  Group: $(id -gn) ($(id -g))"
echo "Host: $(hostname)"
echo "Shell: ${SHELL:-unknown}  ($0)"
echo "TTY: $(tty 2>/dev/null || echo 'not a tty')"
echo "CWD: $(pwd)"

echo
echo "-- Versions --"
for cmd in bash git gh jq python3 node; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "%-8s: " "$cmd"; "$cmd" --version 2>&1 | head -n1
  else
    printf "%-8s: not installed\n" "$cmd"
  fi
done

echo
echo "-- Git config (core.pager, advice.detachedHead) --"
git config --get core.pager 2>/dev/null || echo "(unset)"
git config --get advice.detachedHead 2>/dev/null || echo "(unset)"

echo
echo "-- gh config (prompt, pager) --"
if command -v gh >/dev/null 2>&1; then
  gh config get prompt 2>/dev/null || echo "prompt: (unset)"
  gh config get pager 2>/dev/null || echo "pager: (unset)"
  echo "gh auth status:"; gh auth status || true
fi

echo
echo "-- Locale & Size --"
echo "LANG=${LANG:-}  LC_ALL=${LC_ALL:-}"
cols=$(tput cols 2>/dev/null || echo "?")
rows=$(tput lines 2>/dev/null || echo "?")
echo "Terminal size: ${cols}x${rows}"

echo
echo "-- Limits & misc --"
ulimit -a || true
stty -a 2>/dev/null || true

echo
echo "-- Environment flags that affect non-interactive runs --"
echo "CI=${CI:-}  GITHUB_ACTIONS=${GITHUB_ACTIONS:-}  NO_COLOR=${NO_COLOR:-}"
echo "PYTHONWARNINGS=${PYTHONWARNINGS:-}  NODE_NO_WARNINGS=${NODE_NO_WARNINGS:-}"

echo
echo "Tips:"
echo "- Disable pagers/prompts: export GIT_PAGER=cat GH_PAGER=cat PAGER=cat LESS=FRSX; gh config set prompt disabled; git config --global core.pager cat"
echo "- CI env: set at job-level: GIT_PAGER: cat, GH_PAGER: cat, PAGER: cat, LESS: FRSX"
