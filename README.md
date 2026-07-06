# Cella Framework

Exact residue accounting engine — the diagnostic engine rebuilt clean on Cella foundations.

**Author:** William Lloyd · **Started:** 2026-07-06 · **Status:** Layer 0 in progress; Gate 0 CLOSED (the cell is real); G0.1–G0.4 open.

## What this is

A standalone build. It shares no code, no history, and no dependencies with any previous
engine or repository. Every capability it eventually has will exist because it was built
here, certified here, and admitted here.

The engine's job: take a dataset of related sensor channels, fit the constraint surface
they live on, compute invariant coupling diagnostics on it, and emit a **certified
verdict** — computed exactly, refused with a typed reason, or detected with a stated
confidence — never a bare number.

## The two standing rules

1. **Standalone / zero import.** Nothing is imported or copied wholesale from previous
   work. No exceptions for convenience.
2. **The admission rule.** Before anything from previous work is introduced — a design,
   a formula, a document, a test corpus — its record in `ADMISSIONS.md` must close the
   case: **why the engine needs it, why nothing we hold now or could derive with bounded
   additional work beats it, and what would displace it.** Records self-ratify when the
   case is closed — the answer must be obvious from the record; nothing waits on
   sign-off. A case that cannot close is a named work item, and displacement is by
   evidence: present the dominating alternative and the old record falls.

## Layer map

- **Layer 0 — the harness (current).** The cell type `(value, residue)`, observation
  maps and their typed defects, the residue algebra (two species: measurement defect and
  representation defect), the exact number tower (ℚ and ℚ(√q)), stratum-typed refusals,
  and the two-register certificate. Nothing uncertified can exist above this layer.
- **Layer 1 — the geometric substrate.** Jets, the gauge-normal carrier, the invariant
  tower, channel accounts, isotypic moments, localization channels.
- **Layer 2 — the time-series bridge.** Windowed surface fits as observation maps with
  typed fit defects.
- **Layer 3 — the diagnostic surface.** The full capability contract (point diagnostics,
  n-var, scanning, fingerprints, compare), graded by the Validation Programme.

See `ROADMAP.md` for the gates, `CERTIFICATE_SCHEMA.md` for the certificate design,
`ADMISSIONS.md` for what has been admitted and why.
