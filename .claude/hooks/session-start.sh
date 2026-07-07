#!/bin/bash
# SessionStart hook — install the Python deps that the ephemeral container drops on
# every reset, so verification/ and reports/ scripts (sympy/mpmath/numpy) run without
# manual reinstalls. Synchronous, idempotent, non-interactive. Web-only.
set -euo pipefail

# only run in the remote (Claude Code on the web) environment
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# core deps used across verification/ and reports/ (exact-arithmetic + numeric)
python3 -m pip install --quiet --disable-pip-version-check sympy mpmath numpy || {
  echo "session-start hook: core dep install failed" >&2; exit 1; }

# optional: pymupdf for reading the tracked reference PDFs (non-fatal if it fails)
python3 -m pip install --quiet --disable-pip-version-check pymupdf 2>/dev/null || \
  echo "session-start hook: pymupdf (optional) not installed" >&2

exit 0
