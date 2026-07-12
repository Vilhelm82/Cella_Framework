# Cella Pathfinder Kernel Architecture — v1.2r1 Upgrade Specification

**Second revision after audit round 2. Supersedes
`CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1_2r_DELTA.md` in full.**
This is the proposed normative v1.2 architecture delta. Anchors
reference v1.1 section numbers. Nothing canonical until merged by
Will's hand.

Tags: U/L/S/K/C-OP (design origins), R1–R10 (audit round 1),
Q1–Q9 (audit round 2, adjudicated below).

---

## 0a. Corrections ledger — round 2

| Q# | Finding | Disposition | Effect |
|----|---------|-------------|--------|
| Q1 | Termination measure μ does not contain the order used to prove termination: SPLIT descends in the Noetherian closed-set order, but μ's first component was *dimension*, which does **not** strictly decrease on a zero-divisor split | **Accepted — real hole in my proof** | E1 measure rebuilt with V(√I) under strict inclusion as primary; dimension demoted to derived coarsening |
| Q2 | `PINNED_UNVERIFIED` incompatible with unqualified `CERTIFIED`: warrant vector records the trust gap, final state conceals it | **Accepted, both fixes** | New `CERTIFIED_RELATIVE` state + rule that any unverified dependency must appear in `scope.assumptions` |
| Q3 | C6 invokes "meet" on proof_grade / relation_grade, which are not lattices (construction labels, not strength orders) | **Accepted** | C6 rewritten with explicit composition tables; checker verifies composed relation meets the claim's transport_variance |
| Q4 | F1 termination statement broader than E1 proves: E1 covers stratification descent, not GB fallback / factorization / radical membership / CAD / interpolation / certificate discovery | **Accepted — overclaim** | F1 restated as a constitutional rule (every routine: own measure or metered budget); E1 becomes one instance; global meter covers all search loops |
| Q5 | N2 underspecified: "λ(I) = 0 on a spanning set" states no object and no containment proof; a finite sample is insufficient | **Accepted** | N2 rewritten with certified finite-dimensional quotient/truncation + containment certificate |
| Q6 | W3 downgrade requires a rational point universally; a nonempty stratum with nonzero coefficient may have no rational point | **Accepted — named recurring trap** | W3 (and the N1 statement) corrected to "separating exact evaluation or ring-map witness, possibly into a certified algebraic extension" |
| Q7 | proof_grade composition may silently discard mixed provenance | **Accepted** | Composition preserves the full proof DAG; summary grade is derived, DAG retained |
| Q8 | Scope meets need incompatibility handling (contradictory characteristics / incompatible localizations) | **Accepted** | E3 scope-meet gains a compatibility axis with typed outcomes |
| Q9 | `HIGHER_JET_REQUIRED` too coarse: quadratic nullity does not prevent reporting exact inertia, only completing a classification needing the null directions | **Accepted** | D3 split into `INERTIA_CERTIFIED_WITH_NULLITY` + `HIGHER_JET_REQUIRED_FOR_CLASSIFICATION` |

**Named recurring trap (flagged so it stops happening):** the
**rational-point assumption** — treating "a rational witness point" as
a theorem when it is only the preferred route *when one exists*. Caught
in round 1 (scope nonvacuity: rational point sufficient, not necessary)
and re-committed in the round-1 W3 amendment. Standing rule: any
"evaluate at a point" or "witness point" route is stated as
*"exact/rational point when available, else a certified algebraic
extension point or a ring-map/dimension witness."* No point-existence
is assumed over QQ.

**Pushbacks this round:** none. All findings accepted.

Round-1 ledger (R1–R10) and changelog carried forward from v1.2r;
only the entries below change.

---

## 0b. Changelog — entries changed since v1.2r

| # | Item | Change |
|---|------|--------|
| C5 | Negative-claim certificates | N2 fully specified (Q5); N1 point-route generalized to algebraic-extension/ring-map (Q6) |
| C6 | Warrant composition | "meets" replaced by explicit composition tables; DAG preserved (Q3, Q7) |
| D3 | Inertia classifier | outcome split into certified-with-nullity vs classification-blocked (Q9) |
| E1 | Descent law | termination measure rebuilt around V(√I) strict-inclusion order (Q1) |
| E3 | Scope composition | scope-meet gains compatibility axis + typed outcomes (Q8) |
| F1 | Termination | restated as constitutional per-routine rule; E1 an instance; global meter (Q4) |
| H2 | Identifiers | new state `CERTIFIED_RELATIVE`; new outcomes/labels from Q8/Q9 (Q2) |
| — | KN spec | W3 discharge route generalized (Q6) — one-line amendment restated in H1 |

All other v1.2r entries (A1, A2, A3, A4, A5, A6, B1–B6, C1–C4, D1, D2,
D4, E2, Part G) stand unchanged and are the normative text.

---

# Part C — Certifier plane (changed entries)

## C5. Negative-claim certificates, typed — revised (anchor: §6.5; §16; §22.3) [U6, R3, R7, Q5, Q6]

**Negative membership — route ladder (cheapest first):**

    N1  separating ring-map witness:
        φ : R → S with φ(I) = 0 (checked on generators) and φ(f) ≠ 0.
        S is any target admitting an exact check: k itself (rational
        evaluation) WHEN a suitable rational point exists, else a
        CERTIFIED ALGEBRAIC EXTENSION of k, or a structured quotient.
        Verification: evaluate the generators and f under φ.
        (Point existence over QQ is NOT assumed — see the recurring-
        trap rule. A rational evaluation is the preferred instance,
        not the theorem.)

    N2  separating functional on a certified finite-dimensional
        quotient:
            π : R → Q,  Q a certified finite-dimensional quotient or
                         truncation (with its finiteness certificate),
            π(I) ⊆ W    (W a certified subspace; containment proved on
                         a generating set AND closed under the quotient
                         relations — not a finite sample of ideal
                         elements),
            λ : Q → k   linear with λ(W) = 0 and λ(π(f)) ≠ 0.
        The certificate must include the proof that vanishing on W
        implies vanishing on π(I) — i.e. that W ⊇ π(I), not merely
        W ⊇ π(generators of a sampled subset).

    N3  certified Gröbner basis + nonzero normal form with full
        reduction trace — the complete generic fallback, inheriting
        the basis certificate's grade and cost.

**Real emptiness — typed certificate forms** (unchanged from v1.2r):
`REAL_EMPTY_STURM`, `REAL_EMPTY_PREORDERING` (Krivine–Stengle:
−1 = Σ hᵢfᵢ + Σ_α σ_α ∏ gⱼ^{αⱼ}, hᵢ arbitrary, σ_α SOS),
`REAL_EMPTY_ARCHIMEDEAN_MODULE` (Archimedean hypothesis recorded),
`REAL_EMPTY_CAD_CELL`; strict inequalities/inequations via typed
encodings.

**KN spec consequence (Q6-corrected):** W3 (extremal noncancellation)
is nonmembership-shaped and discharges at **N1 grade by a separating
exact evaluation or ring-map witness** — a rational stratum point where
the coefficient is nonzero *when one exists*, otherwise a point in a
certified algebraic extension of the stratum's function field, or a
ring-map/dimension witness. Not "a rational point" unconditionally.

## C6. Warrant-vector composition — revised (anchor: certificate composition) [S1, R2, Q3, Q7]

Composition is defined **per axis by explicit rule**, not by an
unqualified "meet". The full proof DAG is retained after composition;
the summary grades are *derived from* it, never a substitute that
discards provenance (Q7).

**proof_grade** — by provenance:

    SELF_CONTAINED ∘ SELF_CONTAINED              → SELF_CONTAINED
    any edge using a verified theorem            → THEOREM_REDUCTION
    any edge depending on an external certificate
        envelope                                 → RELATIVE_CERTIFICATE

    (a self-contained identity resting on a theorem-reduced structural
    fact is THEOREM_REDUCTION overall — mixed provenance is preserved,
    not rounded away.)

**relation_grade** — by composition table (IDENTITY is the unit,
COMPARISON_ONLY is absorbing):

    IDENTITY ∘ r                 = r
    ISOMORPHISM ∘ ISOMORPHISM    = ISOMORPHISM
    INTERTWINER ∘ INTERTWINER    = INTERTWINER
    ISOMORPHISM ∘ INTERTWINER    = INTERTWINER
    COMPARISON_ONLY ∘ anything   = INADMISSIBLE (not a proof edge)

    After composing, the checker verifies the resulting relation
    satisfies the consuming claim's transport_variance (C4); a
    mismatch raises TRANSPORT_UNSUPPORTED.

**dependency_state** — by strict floor:

    the composed state is the weakest present; any PINNED_UNVERIFIED
    edge makes the composition PINNED_UNVERIFIED (and forces
    CERTIFIED_RELATIVE at the final state — F1/Q2).

**scope** — union of assumptions; meet of opens with the compatibility
handling of E3 (Q8).

---

# Part D — Planner (changed entry)

## D3. Exact inertia classifier — revised outcomes (anchor: §17) [L4, R-small, Q9]

Machinery unchanged (hierarchical vanishing cascade; 1×1 and 2×2
congruence pivots; Sylvester on the block-diagonal result; post-hoc
labels). The **outcome is split** so a certified order-2 result is
never masked as a refusal:

    INERTIA_CERTIFIED_WITH_NULLITY:
        (rank, signature, nullity) are certified exactly. Reported
        whenever the congruence reduction completes — including when
        nullity > 0. This is a positive certified result.

    HIGHER_JET_REQUIRED_FOR_CLASSIFICATION:
        raised only for the *further* classification that depends on
        behaviour along the null directions (which the quadratic jet
        cannot see). The certified inertia above still stands and is
        returned alongside.

Consistent with A5: the quadratic observation family is *adequate* for
inertia and *inadequate* only for the null-direction classification;
the split records exactly that boundary.

---

# Part E — Stratification and scope (changed entries)

## E1. Descent law — revised termination measure (anchor: Law 5; §22) [U1, R4, Q1]

Layers 1 (holonomy scouts) and 2 (ideal certificates decide: STOP /
DESCEND / SPLIT, with the zero-divisor SPLIT route) are **unchanged
from v1.2r**. Only the termination measure changes.

**Layer 3 — termination (corrected).** The well-founded measure is

    μ(node) = ( V(√I),  remaining_obligation_rank,  remaining_budget )

with the **first component ordered by strict closed inclusion**:

    V(√J) ≺ V(√I)   iff   V(√J) ⊊ V(√I).

This order is well-founded by Noetherianity (a strictly descending
chain of closed subsets of a Noetherian scheme is finite). The
displayed measure now *contains* the order the proof uses — the
round-1 measure's first component (dimension) is **withdrawn as
primary**, because dimension does not strictly decrease on a
zero-divisor split (two lines through a point split into two lines, all
of dimension 1). Dimension survives only as a derived coarsening for
cost heuristics, never as the termination component.

Strict decrease on every recursive edge, now genuinely carried by μ:

    DESCEND:  V(I + ⟨h⟩) ⊊ V(I)          (certified proper + dim drop)
    SPLIT:    V(I + ⟨g⟩) ⊊ V(I)  and
              V(I + ⟨h⟩) ⊊ V(I)          (certified by g,h ∉ √I —
                                          each child a strictly
                                          smaller closed set)

`remaining_obligation_rank` handles recursive work that preserves the
carrier (no closed-set change); `remaining_budget` handles bounded
implementation limits. STOP terminates the branch (empty inverted
open). Budget terminal semantics unchanged: `REFUSED_BUDGET` when every
preceding edge carried its certified decrease; `DEFECT` otherwise
(round-1 pushback 1, retained).

## E3. Scope composition — revised with compatibility axis (anchor: result envelope; §22.3) [U3, R10, Q8]

Nonvacuity trichotomy (`CERTIFIED_SCOPE_NONEMPTY` /
`CERTIFIED_SCOPE_EMPTY` / `SCOPE_NONVACUITY_NOT_CERTIFIED`), the
nonvacuity routes, the geometric-vs-real semantics fork, and the
assumption ledger are **unchanged from v1.2r**. The scope **meet** now
carries an explicit **compatibility** determination before nonvacuity
is even asked:

    scope meet(scope_a, scope_b):
        compatible                     → composed scope; then evaluate
                                         the nonvacuity trichotomy on
                                         the meet of opens
        certified empty                → CERTIFIED_SCOPE_EMPTY
        compatibility unknown          → SCOPE_NONVACUITY_NOT_CERTIFIED
        contradictory characteristics
          or incompatible localizations→ typed SCOPE_INCOMPATIBLE error
                                         (or CERTIFIED_SCOPE_EMPTY when
                                         the contradiction certifies
                                         emptiness)

This matters where two results are certified in different
characteristics, or under mutually incompatible localizations — cases
the round-1 rule (nonvacuity axis only) did not type.

---

# Part F — Totality and termination (replaced)

## F1. Totality, per-routine termination, and the final states (anchor: §4 / Law 12) [R5, Q2, Q4]

Three separate guarantees.

**Semantic totality.** Every terminal state has a typed meaning. The
final state machine (with the Q2 addition):

    CERTIFIED           — claim discharged; dependency_state is NOT
                          PINNED_UNVERIFIED on any axis (proof DAG
                          closes under the checker)
    CERTIFIED_RELATIVE  — claim discharged conditional on explicitly
                          named unverified dependencies; REQUIRES every
                          such dependency to appear in
                          scope.assumptions and dependency_state to be
                          PINNED_UNVERIFIED. The trust gap is visible in
                          the state, not only the warrant vector.
    SCOUTED_RETAINED    — scouting work returned explicitly as retained,
                          uncertified evidence (delegation is internal;
                          it terminates only by becoming CERTIFIED /
                          CERTIFIED_RELATIVE / SCOUTED_RETAINED)
    REFUSED_SCOPE       — typed refusal: outside the declared aperture,
                          named
    REFUSED_BUDGET      — typed refusal: certified descent throughout,
                          resources exhausted
    DEFECT              — a kernel invariant was violated (including a
                          budget halt without certified descent)

Enforcement: `CERTIFIED` requires `dependency_state != PINNED_UNVERIFIED`;
`CERTIFIED_RELATIVE` requires every unverified dependency present in the
assumption ledger. A certificate may not silently occupy `CERTIFIED`
while carrying an unverified dependency.

**Operational termination — constitutional rule (Q4).** Termination is
not proved once for the kernel by E1. It is required **per routine**:

    Every recursive or iterative kernel routine must provide either
      (1) a routine-specific well-founded descent measure, or
      (2) a monotonically consumed resource budget,
    and a global metered budget covers all search loops
    (Gröbner fallback, factorization, radical membership, CAD,
     interpolation search, certificate discovery, and any future
     search routine), not only stratification edges.

E1's descent measure is **one instance** of rule (1). No routine is
exempt; a routine presenting neither a measure nor a metered budget is
rejected at design review. This replaces the v1.2r sentence "every run
halts by the measure of E1 or budget," which overclaimed E1's scope.

Refusal-taxonomy completeness remains **necessary** (aperture spec +
typed-halting guarantee), not sufficient for termination. Meaning is
carried by the taxonomy; termination by the per-routine measures and
budgets. Distinct artifacts, distinct jobs.

---

# Part H — Integration map and open items (updated)

## H1. Integration order (proposed)

Unchanged from v1.2r except:

- Step 2 (trust root) now also lands `CERTIFIED_RELATIVE` and the
  `CERTIFIED` dependency-state guard (Q2) with C5/C6.
- Step 5 (E1 + F1 together) now lands the **constitutional per-routine
  termination rule** (Q4), and every other routine in the kernel must
  be annotated at merge with its measure or budget — a merge checklist
  item, not just a section edit.
- Step 9 (KN spec amendment): W3 discharges at **N1 by a separating
  exact evaluation or ring-map witness (algebraic extension permitted)**
  — not "a rational point" (Q6).

## H2. Typed identifiers introduced or changed since v1.2r

    New final state:     CERTIFIED_RELATIVE
    New scope outcome:    SCOPE_INCOMPATIBLE
    Split D3 outcomes:    INERTIA_CERTIFIED_WITH_NULLITY,
                          HIGHER_JET_REQUIRED_FOR_CLASSIFICATION
                          (replaces the single HIGHER_JET_REQUIRED)
    E1 measure:           first component now V(√I) under strict
                          inclusion (dimension demoted to heuristic)

All v1.2r identifiers otherwise stand.

## H3. Remains open after v1.2r1

Unchanged from v1.2r, plus one process item:

- **Per-routine termination annotations (Q4).** The constitutional
  rule is in force from merge; the actual measure/budget for each
  existing search routine (GB fallback, factorization, radical
  membership, CAD, interpolation, certificate discovery) must be
  written and attached as those routines are specified. The rule
  ships now; the per-routine instances accumulate.
- General closure lemma (Part G) beyond per-family discharge.
- Certificate compression (§28).
- Square-class relation witnesses when valuation rank is inconclusive.
- Formal-proof export (unblocked in shape by C1's replay form).
- Adequacy-certificate library (A5), seeded with the two canonical
  instances.

**END**
