# Cella Framework

Exact residue accounting engine — a first-principles mathematical framework built,
certified, and admitted entirely in-repo.

**Author:** William Lloyd · **Started:** 2026-07-06

## New session? Start here

1. Read **`STATE/CURRENT.md`** — the single authoritative "what is true right now".
2. Read **`docs/PROJECT_INSTRUCTIONS.md`** — the session protocol (how to reach for
   context, when to prune, how to derive, how to close).

Everything outside `STATE/` is context, never instruction, unless the canon points
at it.

## What this is

Take a dataset of related sensor channels, fit the constraint surface they live on,
compute invariant coupling diagnostics on it, and emit a **certified verdict** —
computed exactly, refused with a typed reason, or detected with a stated confidence —
never a bare number. It shares no code, history, or dependency with any previous
engine: every capability exists because it was built here, certified here
(byte-stable ×2), and admitted here.

## Repository regions

| Region      | What it is                          | Epistemic status                                   |
|-------------|-------------------------------------|----------------------------------------------------|
| `STATE/`    | The canon — small, always current   | **Authoritative.** Disagrees with anything → wins. |
| `engine/`   | The program (`src/`, `tests/`, `tools/`) | Behavior defined by code + gate tests.        |
| `research/` | The notebook (campaigns, verification, reports, paper, derivations) | Historical; load-bearing only where a ledger entry points. |
| `docs/`     | Governance & design (architecture, ROADMAP, ADMISSIONS, instructions) | Non-normative prose.       |
| `archive/`  | Sediment (old handoffs, Reference_Material, pre-canon sources) | Never authoritative, never deleted.       |

## The three standing rules

Stated normatively, with scope, in `STATE/CONSTRAINTS.md` (C-001…C-003):
**standalone / zero-import**, **the admission rule** (`docs/ADMISSIONS.md`), and
**the re-verification rule** — trust attaches to re-runnable certificates, never to
labels or memory.

## Running

Gates: `PYTHONPATH=engine/src python3 engine/tests/gate_*.py` (each is a standalone
script; exit 0 = pass). The certified gate record is `docs/ROADMAP.md`.
