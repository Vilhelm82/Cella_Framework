# ADMISSIONS — the introduction ledger

**The standard (Will, 2026-07-06, superseding the sign-off form):** nothing is introduced
from previous work until its record proves it is the correct addition — **why the engine
needs it, and why nothing we hold now, or could derive with bounded additional work,
beats it.** If that cannot be answered, there is more work to do, and the record names
that work. Records **self-ratify when the case is closed** — the answer must be obvious
from the record itself. No sign-off queue exists.

**THE RE-VERIFICATION RULE (Will, 2026-07-06).** No prior result enters on documentary
status. "ACCEPTED", "RATIFIED", "PROVEN", "CERTIFIED" in an origin document are
**claims, never evidence** — statuses hinge on humans, and humans are mistake-prone.
Before any prior mathematical result bears load here, it is **re-proven inside this
repo**: computational claims re-run from fresh code (never copied) against the stated
values, byte-stable ×2; symbolic identities re-derived; analytic theorems re-derived in
fresh notes. Once re-proven, the result carries its own certificate *here*, and future
sessions trust the re-runnable certificate — not the origin label, not memory, not
anyone's acceptance. Re-verification artifacts live in `verification/` and are named in
the consuming record. A result cited anywhere without an in-repo certificate is a
defect. (Case law: the WARP citation of 2026-07-06 — internally ratified, externally
stale; caught by Will, not by process. This rule makes that catch structural.)

**Statuses.**
- **OPEN** — case not yet closed; the missing work is named. A work item, not a request.
- **ESTABLISHED** — case closed; the artifact may be built. Scope stated exactly.
  *Mathematical inputs cited by the record additionally require in-repo
  re-certification before first load-bearing use (re-verification rule above).*
- **DISPLACED** — a better artifact won under the same standard. The record stays
  visible, successor named. Displacement is by evidence only: present the dominating
  alternative and the old record falls. This replaces authority with challenge.

**Record template**

```
ID / Artifact / Origin (reference only, never a dependency)
Need:          why the engine requires this capability at all
Criterion:     the properties that decide what "best" means here
Alternatives:  every live option — held now or derivable with bounded work — and
               why each loses on the criterion
Displacement:  the evidence that would displace this record
Obligations:   what the harness must still certify, and at which gate
Status:        OPEN | ESTABLISHED | DISPLACED
```

---

## A-001 — The cell, the observation map, composable residue

**Origin:** Cella Foundational Design Document v0.1 (2026-06-13). Reference only.
**Need:** the engine's defining output is exact-or-typed-refusal with a reconstructive
account. That requires a result object that carries its own account.
**Criterion:** simultaneously — (1) exact reconstruction of the true object where
possible, (2) typed non-recovery where not, (3) defects compose across chained
operations so a whole pipeline has one derivable account.
**Alternatives and why each loses:**
- *Floats + tolerances* — fails all three; it is the failure mode this engine exists
  against.
- *Interval/ball arithmetic* — enclosure, not reconstruction (fails 1); no typed
  non-recovery semantics (fails 2); widens under dependency where exact residues
  compose without widening on the covered class.
- *Higher precision (arbitrary-precision floats)* — relocates the defect, never
  types or recovers it (fails 1, 2).
- *Fully symbolic computation* — cannot represent the defect of a lossy observation at
  all (measured data has no symbolic truth to hold), unbounded cost (fails 3 in
  practice).
- *Derivable-with-work* — any object satisfying (1)–(3) **is** a cell under another
  name; the criterion forces the definition.
**Displacement:** an account object meeting (1)–(3) with a strictly larger covered class
or strictly lower cost.
**Obligations:** G0.1 — composition certified on the rational-op class. Sum-typed token
form certified or split (G0.4). These are certification targets, not assumptions —
the design doc itself graded them INFERENCE and this record preserves that.
**Status: ESTABLISHED.**

## A-002 — The second residue species (representation defect, R)

**Origin:** the transport law and gauge-normal form. Cited as mathematics.
**Need:** the engine must distinguish *the data changed* from *the representation
changed* — the false-positive taxonomy (recalibration, units, chart choice) that
interference testing exists to untangle.
**Criterion:** type-level separation of information-bearing defect (M) from
zero-information motion (R), losing neither the invariant nor the explanation of what
moved.
**Alternatives and why each loses:**
- *Type gauge motion as measurement error (M)* — provably wrong typing: the transport
  law says invariants are untouched, so gauge motion carries zero information about the
  state; conflation makes every recalibration look like a fault.
- *Eager quotient (store only invariants, discard the representative)* — loses the
  account: "representation changed, not data" becomes unverifiable, and the
  representative carries the role semantics (the declared frame is the physical
  section, not junk).
- *No typing (incumbent practice)* — the taxonomy collapses; ad hoc normalization.
**Displacement:** none available at the substrate level — the transport law is proven.
If G0.2 refutes single-account composition of M and R, the account splits into two
ledgers *visibly*; the species survives, the algebra bends.
**Obligations: DISCHARGED 2026-07-06.** The composition conjecture was resolved by the
G0.2 campaign (`campaigns/G02_two_species_account/` — Stages 0/A/B/C, frozen preregs,
byte-stable ×2, conjecture DEMONSTRATED on the covered class: order-2 slot,
translations, rational data, fixed/drifting base crossed by F1), and the
implementation certified at gates G0.1/G0.2 (`tests/gate_01.py` 7/7, `tests/gate_02.py`
13/13, both ×2). Key laws now in code: attribution by criterion (`fold_into_m`),
two-epoch boundary guard, owned holonomy (`holonomy_gap`).
**Status: ESTABLISHED — composition resolved positive on the covered class;
outside-class maps remain fenced (T_token territory).**

## A-003 — The exact number tower ℚ ∪ ℚ(√q)

**Origin:** the parity law. Cited as mathematics.
**Need:** no float on any verdict path, across the *entire* invariant tower — including
the odd, bending-sensitive extrinsic sector.
**Criterion:** exact arithmetic covering every invariant the engine emits; minimal
machinery.
**Alternatives and why each loses:**
- *ℚ only* — provably insufficient: odd-order invariants carry √q, and that sector is
  the derived defence to the isometric-bending attack.
- *General algebraic number fields / symbolic radicals* — provably unnecessary: the
  parity law shows nothing beyond one √q ever occurs in the tower. Generality buys
  cost for zero covered objects.
- *Ball arithmetic over ℝ* — enclosure, not exactness (see A-001).
**The parity law is itself the optimality proof: two rungs are necessary (ℚ fails) and
sufficient (nothing above √q occurs).**
**Displacement:** an invariant entering the engine whose value provably leaves ℚ(√q) —
that would be a mathematical finding first and a tower extension second.
**Obligations:** G0.3 — exact arithmetic certified; no float constructor reachable from
verdict paths.
**Status: ESTABLISHED.**

## A-004 — Stratum-typed refusals

**Origin:** refuse-not-lie discipline; degeneracy-as-stratum leads. Design precedent.
**Need:** degenerate inputs are diagnostic findings (lockstep channels, vanishing
gradients), and the certificate must render every non-result in plain language.
**Criterion:** no silent garbage, no crash paths; every refusal classifiable and
renderable; strata carry their diagnostic content.
**Alternatives and why each loses:**
- *NaN / None / exceptions* — silent garbage or crash; both banned by the engine's
  definition.
- *Flat error codes* — discard the stratum content, which is exactly the diagnostic
  value of a degeneracy.
- *Confidence scores in place of refusal* — smuggles statistics into the computation
  layer; violates the layer separation.
**Displacement:** none — the criterion admits only this form. Vocabulary grows by
new records, each token with its plain rendering.
**Obligations:** G0.4 — refusal paths produce schema-conformant certificates; every
token renders.
**Status: ESTABLISHED.**

## A-005 — The Validation Programme (Kessler v1.0, 2026-04-07)

**Origin:** `Validation Programme.md`. Reference only.
**Need:** an acceptance harness whose stages are cumulative hard gates, or the engine's
claims are self-graded.
**Criterion:** staged coverage of the forced question sequence — is the maths right →
how small a change is visible → what corrupts it → does it detect real faults → blind →
what breaks it → versus incumbents → self-consistent → deployable.
**Alternatives and why each loses:**
- *Derive a fresh programme* — the nine questions are near-forced by the claim
  structure; a fresh derivation reproduces them at the cost of losing the imported
  cross-domain discipline (interference protocol, LoD, blind protocol, adversarial
  stage) already encoded.
- *Ad hoc per-dataset testing* — no gates, no cumulative validity, no limitation
  disclosure; the incumbent failure mode.
**Best shape:** re-authored at Layer 3 with corrected sensors, exactness/statistics
separation per stage, and metamorphic relations MR-3/MR-4 as identity checks (now
theorems).
**Displacement:** stage *structure* — by a demonstrated gap the nine questions miss;
stage *parameters* (thresholds, corpora) — evidence-bound and expected to move.
**Status: ESTABLISHED (structure; parameters evidence-bound).**

## A-006 — The capability contract (origin method inventory)

**Origin:** `Lloyd_Method_Portfolio.xlsx`. Reference only.
**Need:** a clean rebuild's classic failure is silently shipping without capabilities
the old engine had.
**Criterion:** an enumerable checklist the rebuild is graded against; completeness of
inventory.
**Alternatives and why each loses:** *rebuild from memory* — the documented drift
failure mode; *no contract* — silent loss, discovered by users. The origin inventory is
the only complete method census that exists (37 methods + its own gap list).
**Displacement:** a demonstrated inventory error (method missing from the census).
**Obligations:** `CAPABILITY_CONTRACT.md` authored fresh at G3.0; no origin code enters.
**Status: ESTABLISHED.**

## A-007 — The corrected invariant sensor set

**Origin:** post-pivot mathematics (numerator tower; carrier; shape moment; triangle
localization; parity). Cited as mathematics.
**Need:** the engine's sensors, each shipping invariance group + blindness set +
completeness scope.
**Criterion:** recalibration-proof (invariant), complete at declared scope, exactly
computable, blindness derivable.
**Why nothing beats it — the dominance cases, one per sensor:**
- *Carrier O* — the normal-form theorem forces every invariant sensor to factor
  through O. The carrier is not one choice among alternatives; it is the
  coordinatization of **all** invariant sensors at order 2. Competitors are either
  functions of O or provably non-invariant.
- *Numerator tower* — strictly dominates the ratio sensor it corrects: same coupling
  sensitivity, exact (not approximate) self-fault blindness, scale invariance without
  the quotient. Proven.
- *Shape moment* — scalars are provably insufficient at n ≥ 5 (dimension threshold);
  the isotypic moment set captures exactly the invariant content at its degree. A
  better degree-2 sensor cannot exist; it could only be a different basis of the same
  content.
- *Localization channels* — proven support inclusion ({moved} = {S ⊇ e*}); the
  alternative (contribution-style attribution) has no support theorem.
**Scope stated exactly:** mathematical dominance on the regular locus at declared order/
degree. **Not claimed:** empirical dominance on real data — that question is routed to
armed kill conditions at G3.1 (A/B rerun) and G3.2 (shape-moment wager), and the global
completeness tier remains OPEN as successor work (portfolio priority #2).
**Displacement:** per sensor, by a certified counterexample inside its stated scope, or
by a completed global tier changing the completeness statement.
**Obligations:** G1.2 — each sensor enters with exact reference values + its blindness
statement.
**Status: ESTABLISHED (mathematical scope); empirical scope gated, kills armed.**

---

*Ledger discipline: append-only; displaced records stay visible with successors named.
An artifact used anywhere without a record here is a defect. A record that cannot close
its case stays OPEN with its missing work named — OPEN records are the R&D queue.*
