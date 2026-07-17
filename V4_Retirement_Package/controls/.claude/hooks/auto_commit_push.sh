#!/usr/bin/env bash
# Auto-commit + push, invoked by the Claude Code "Stop" hook.
# Behaves as a DAILY SAFETY NET, not a per-turn committer:
#   - commits only if >= 24h since the LAST commit (manual or auto) AND the tree is dirty
#   - your own manual commits reset the 24h clock, so it stays quiet during active work
#   - skips detached HEAD and in-progress merge/rebase/cherry-pick/revert
#   - never fails the session (always exit 0; a rejected push is swallowed)
# Tune the window with CLAUDE_AUTOCOMMIT_WINDOW (seconds); default 86400 (24h).
# Usage: auto_commit_push.sh [dry]   ("dry" reports the decision without committing)
set +e
DRY="${1:-}"
WINDOW="${CLAUDE_AUTOCOMMIT_WINDOW:-86400}"   # 24h in seconds

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || { [ "$DRY" = dry ] && echo "[dry] skip: project dir unavailable"; exit 0; }

# Must be a git repo on a real branch (detached HEAD -> skip).
branch="$(git symbolic-ref -q --short HEAD)"
if [ -z "$branch" ]; then
  [ "$DRY" = dry ] && echo "[dry] skip: detached HEAD or not a git repo"
  exit 0
fi

# Skip if an in-progress git operation would be corrupted by an auto-commit.
for m in MERGE_HEAD CHERRY_PICK_HEAD REVERT_HEAD rebase-merge rebase-apply; do
  p="$(git rev-parse --git-path "$m" 2>/dev/null)"
  if [ -n "$p" ] && [ -e "$p" ]; then
    [ "$DRY" = dry ] && echo "[dry] skip: git operation in progress ($m)"
    exit 0
  fi
done

# Daily rate limit: skip if the branch had ANY commit within the window.
now="$(date -u +%s)"
last="$(git log -1 --format=%ct 2>/dev/null || echo 0)"
age=$(( now - last ))
if [ "$age" -lt "$WINDOW" ]; then
  [ "$DRY" = dry ] && echo "[dry] skip: last commit ${age}s ago (< ${WINDOW}s window)"
  exit 0
fi

# Only commit if there is actually something to commit (respects .gitignore).
if [ -z "$(git status --porcelain)" ]; then
  [ "$DRY" = dry ] && echo "[dry] skip: working tree clean (no repo change)"
  exit 0
fi

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
msg="auto: daily snapshot ${ts}"
trailer="Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"

if [ "$DRY" = dry ]; then
  echo "[dry] WOULD COMMIT on $branch (last commit ${age}s ago >= ${WINDOW}s, tree dirty):"
  echo "[dry]   git add -A && git commit -m \"$msg\" -m \"$trailer\" && git push origin $branch"
  git status --porcelain | head -20
  exit 0
fi

git add -A
git commit -q -m "$msg" -m "$trailer"
# A rejected push (remote moved ahead via another session) must not fail the hook;
# the work is committed locally and the user resolves the remote.
git push -q origin HEAD 2>/dev/null
exit 0
