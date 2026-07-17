# DAG Auto-Commit Design

**Date:** 2026-07-17  
**Status:** Approved

## Objective

Make a successfully applied DAG submission durable in Git without absorbing
unrelated worktree changes. A DAG apply remains the mathematical transaction;
the Git commit is its immediate repository-publication step.

## Approved behaviour

After `apply_bundle` has validated and atomically written the canonical graph,
applied submission and receipt, it attempts one local Git commit containing only:

1. source files declared by the submission's artifact file records;
2. `DAG_Library/canonical/theorem-dag.json`;
3. the applied submission JSON; and
4. the apply receipt JSON.

The commit message is `dag: apply <submission-id>`. The operation does not push;
remote publication remains an explicit maintainer action.

## Safety boundary

- Paths are resolved against the configured Cella repository and must remain
  inside it.
- Target files are staged explicitly and committed with a path-limited commit,
  so unrelated modified, untracked or already-staged files are not absorbed.
- Git is invoked as an argument vector, never through a shell.
- An apply in a detached test DAG outside the configured repository is not
  allowed to commit the live checkout.

## Failure semantics

Git failure does not roll back a valid mathematical transaction. The apply result
still reports `applied: true` and returns a `git_commit` record with status
`git_publication_pending`, the exact intended paths and the Git error. This makes
the durability gap visible and recoverable without corrupting or replaying the DAG
transaction.

On success, `git_commit` reports status `committed`, the commit hash and committed
paths.

## Verification

A standalone gate creates a temporary Git repository and proves that a valid DAG
apply:

- creates a new commit;
- commits the declared source, canonical graph, applied submission and receipt;
- leaves an unrelated worktree file uncommitted; and
- exposes the commit hash in the apply result.

Existing DAG service and MCP gates must continue to pass in the configured project
environment. No automatic push, branch creation or whole-worktree commit is in
scope.
