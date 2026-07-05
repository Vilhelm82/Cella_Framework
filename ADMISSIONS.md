# ADMISSIONS — the introduction ledger

**The rule (standing, Will, 2026-07-06):** nothing gets introduced or copied wholesale
from previous work until we have explained **why we are using it** and **how it is in its
best shape/format possible**. This file is where that explanation lives. An artifact
enters the repo only after its record here reads ADMITTED, and it enters in the improved
form the record describes — never the original form.

**Record template**

```
ID:           A-###
Artifact:     what is being admitted
Origin:       where it came from (repo/doc/paper — reference only, never a dependency)
Why:          the reason this engine needs it
Best shape:   the form it should take HERE, and what must change from the origin form
Status:       PROPOSED → ADMITTED (Will) → SUPERSEDED
```

Statuses move only on Will's word. PROPOSED artifacts may be discussed but not committed
as content.

---

## A-001 — The Cella primitives (cell, observation map, composable residue)

- **Origin:** Cella Foundational Design Document v0.1-draft (2026-06-13). Reference only.
- **Why:** they are the foundation itself — the typed-residue account is what makes every
  downstream verdict exact-or-refused instead of approximately-trusted.
- **Best shape:** re-authored as executable interface contracts in `src/cella/`
  (not prose): `Cell`, `ObservationMap`, `Residue`. The origin doc's honesty grading
  carries over — the two claims it marks as INFERENCE (the sum-typed token form and
  general residue composability) are implemented as **contracts the harness must
  certify**, not as assumed facts. The origin document itself is not copied in; this
  record plus the code contracts replace it.
- **Status:** PROPOSED

## A-002 — The second residue species (representation defect / gauge residue)

- **Origin:** the post-pivot geometry results (transport law; gauge-normal form). Cited
  as mathematics — theorems stand independent of any prior engine.
- **Why:** it is the new primitive the geometry work delivered: representation choice is
  an observation map whose defect is exactly typed and composable (zero-sum residue
  against an invariant total). Cells carrying both species can distinguish *data
  changed* / *representation changed* / *computation lost something* — the false-positive
  taxonomy the Validation Programme's interference stage exists to untangle.
- **Best shape:** a second `Residue` species in the same algebra, with its declared
  invisible subspace, plus a Layer-0 certification target: both species compose under one
  account. The composition claim is a design conjecture until the harness certifies it.
- **Status:** PROPOSED

## A-003 — The exact number tower ℚ ∪ ℚ(√q)

- **Origin:** the parity law (even-order invariants rational; odd-order carry exactly one
  √q). Cited as mathematics.
- **Why:** it lets the entire invariant tower — including the odd, bending-sensitive
  sector — live in exact arithmetic with no floats in any verdict path.
- **Best shape:** a two-rung exact numeric type (`Fraction`, and `a + b·√q` pairs with
  exact arithmetic), implemented fresh in `src/cella/qsqrt.py`.
- **Status:** PROPOSED

## A-004 — Stratum-typed refusals

- **Origin:** the refuse-not-lie discipline and the singular-strata typing leads;
  origin engines' Morse/degeneracy classification. Cited as design precedent.
- **Why:** degeneracy is a stratum, not a failure. A refusal that names its stratum
  (zero gradient, vanishing normal coordinate, rank-deficient fit, umbilic) is a
  diagnostic output; a NaN is a liability.
- **Best shape:** a closed token vocabulary in `src/cella/refusal.py`, each token
  carrying the stratum classification and the plain-language reason used by the
  certificate. Vocabulary grows only by admission record.
- **Status:** PROPOSED

## A-005 — The Validation Programme ("Sniff Test Architecture", Kessler v1.0, 2026-04-07)

- **Origin:** `Validation Programme.md` (uploaded 2026-07-06). Reference only.
- **Why:** it is the acceptance harness — nine staged, hard-gated questions from
  mathematical ground truth to operational robustness, with benchmark corpus, blind
  protocol, and adversarial stage already designed.
- **Best shape:** re-authored (not copied) when Layer 3 opens: sensor references updated
  to the corrected invariant set (numerator tower, carrier, shape moment, localization
  channels); the exactness/statistics separation made explicit per stage (Cella certifies
  computation; statistics judge detection); metamorphic relations MR-3/MR-4 rewritten as
  identity checks since they are now theorems. Stage structure and gates unchanged.
- **Status:** PROPOSED

## A-006 — The OG method portfolio as capability contract

- **Origin:** `Lloyd_Method_Portfolio.xlsx` (uploaded 2026-07-06). Reference only.
- **Why:** the clean rebuild must not silently lose capabilities. The 37-method
  inventory is the checklist this engine is graded against at Layer 3.
- **Best shape:** a `CAPABILITY_CONTRACT.md` table (method → planned equivalent → status)
  authored fresh at Layer 3 opening; includes the origin sheet's own gap list (entity
  segmentation, cross-file compare, streaming mode, per-variable sweep profiles). No
  origin code enters.
- **Status:** PROPOSED

## A-007 — The corrected invariant sensor set

- **Origin:** post-pivot mathematics: numerator coupling tower (self-fault-blind,
  scale-invariant), gauge-normal carrier O (complete order-2 invariant), shape moment
  (mandatory at n ≥ 5 by the dimension threshold), triangle localization channels
  (faulted-edge recovery), branch-typed inversion (monodromy). Cited as mathematics.
- **Why:** these replace the origin engines' sensors where the mathematics proved them
  wrong (the ratio law) or incomplete (scalar spectra at n ≥ 5), and add localization,
  which no prior engine had.
- **Best shape:** fresh Layer-1 derivation notes with exact reference values on the
  analytical test surfaces, then implementations certified against those references.
  Each sensor enters with its blindness statement (what it provably cannot see) alongside
  its sensitivity statement.
- **Status:** PROPOSED

---

*Ledger discipline: append-only. A superseded record stays visible with its successor
named. If an artifact is used anywhere without a record here, that is a defect.*
