# DAG Auto-Commit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically create a scoped local Git commit after every successfully applied DAG submission.

**Architecture:** `apply_bundle` remains the authoritative atomic DAG mutation. After its receipt is written, a focused Git helper derives repository-relative paths from artifact file declarations plus the three DAG transaction records, creates a path-limited commit, and returns either `committed` or the recoverable `git_publication_pending` state.

**Tech Stack:** Python 3.10+ standard library, Git CLI, standalone gate scripts.

## Global Constraints

- Never commit unrelated worktree or index changes.
- Never roll back an applied DAG transaction because Git publication failed.
- Never push automatically.
- Never permit configured paths to escape the repository root.

---

### Task 1: Prove the missing scoped auto-commit behaviour

**Files:**
- Create: `engine/tests/gate_dag_autocommit.py`
- Test: `engine/tests/gate_dag_autocommit.py`

**Interfaces:**
- Consumes: `submit_bundle(submission, dry_run=False)` and `apply_bundle(submission_id, confirm=True)`.
- Produces: a failing assertion requiring `result["git_commit"]["status"] == "committed"`.

- [x] **Step 1: Write the failing gate**

Create a temporary repository, copy the schema registry and canonical graph, make a baseline commit, stage a valid submission with one declared source file, apply it, and assert that the result exposes a Git commit containing exactly the source, graph, applied submission and receipt while an unrelated scratch file remains uncommitted.

- [x] **Step 2: Run the gate and verify RED**

Run: `PYTHONPATH=engine/src python3 engine/tests/gate_dag_autocommit.py`

Expected: failure because `apply_bundle` does not yet return `git_commit` and HEAD does not advance.

### Task 2: Add the minimal scoped Git publication boundary

**Files:**
- Modify: `engine/src/cella/dag_service.py`
- Test: `engine/tests/gate_dag_autocommit.py`

**Interfaces:**
- Produces: `_git_commit_applied_submission(submission, applied_path, receipt_path) -> dict`.
- Return success: `{"ok": true, "status": "committed", "commit": <sha>, "paths": [...]}`.
- Return failure: `{"ok": false, "status": "git_publication_pending", "error": <text>, "paths": [...]}`.

- [x] **Step 1: Resolve and validate commit paths**

Collect every `artifact.files[].path`, the canonical graph, applied submission and receipt. Resolve each beneath `repository_root()` and reject any external path.

- [x] **Step 2: Commit only owned paths**

Invoke Git with argument arrays: targeted `git add -- <paths>`, followed by `git commit --only -m "dag: apply <safe-id>" -- <paths>`, then read `git rev-parse HEAD`.

- [x] **Step 3: Preserve applied state on Git failure**

Catch Git/process/path errors and return `git_publication_pending`; do not raise after the DAG receipt has been written.

- [x] **Step 4: Integrate after receipt creation**

Attach the helper result as `git_commit` in the successful `apply_bundle` response.

- [x] **Step 5: Run the gate and verify GREEN**

Run: `PYTHONPATH=engine/src python3 engine/tests/gate_dag_autocommit.py`

Expected: all assertions pass, with the temporary repository HEAD advanced exactly once.

### Task 3: Document, regress and publish

**Files:**
- Modify: `engine/src/cella/dag_mcp_server.py`
- Modify: `engine/tests/gate_dag_service.py`

**Interfaces:**
- MCP apply documentation promises local scoped commit and explicit pending status.
- Existing service gate accepts the added result without weakening DAG validation.

- [x] **Step 1: Update the MCP apply contract text**

State that successful apply attempts a scoped local commit, never pushes, and reports `git_publication_pending` on Git failure.

- [x] **Step 2: Run focused regression gates**

Run the auto-commit gate, DAG service gate and DAG MCP gate in an environment with project dependencies available.

- [x] **Step 3: Run compile and graph validation gates**

Run `python3 -m compileall -q engine/src/cella` and live DAG file verification.

- [ ] **Step 4: Commit and publish**

Commit the implementation and plan, push `main`, fetch `origin`, and require `git rev-list --left-right --count HEAD...origin/main` to print `0 0`.
