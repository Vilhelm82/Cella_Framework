# Cella Pathfinder Kernel Architecture — v1.2r Upgrade Specification

**Revision of the v1.2 delta after external audit. Supersedes
`CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1_2_DELTA.md` in full.**
Status: proposed. Anchors reference v1.1 section numbers. Numbering
provisional. Nothing canonical until merged by Will's hand.

Provenance tags: U1–U6 (design review), L1–L7 (April lifts), S1–S4
(spine lifts), K1–K4 (unification keys), C-OP (centrifuge operators),
R1–R10 (audit corrections, adjudicated below).

---

## 0a. Corrections ledger

| R# | Audit correction | Disposition | Effect |
|----|------------------|-------------|--------|
| R1 | A1 over-restrictive: backends need private lowered representations; leaf-semantics framing conflates unlike interpretations | **Accepted** | A1 rewritten: hash-bound certified lowering + typed interpretation table |
| R2 | Warrant "lattice" malformed: four labels mix orthogonal axes | **Accepted** | A2/C6 replaced by four-axis warrant vector with per-axis composition; COMPARISON_ONLY inadmissible in proof DAG |
| R3 | C5 Positivstellensatz formula wrong: equality multipliers are arbitrary polynomials; general form is Krivine–Stengle preordering; module form needs Archimedean hypotheses | **Accepted — my formula was wrong, not loose** | C5 rewritten with typed real-emptiness certificate forms + recorded hypotheses |
| R4 | E1 lets holonomy certify termination: identity holonomy ≠ terminal (flat families); nonidentity w/o dim defect ≠ swallowed component; h ∈ √I is a certified empty-open, not an illegal query | **Accepted — the central catch** | E1 replaced: holonomy scouts, ideal certificates decide; well-founded measure proves termination. Amendment: cheap zero-divisor SPLIT route added (below) |
| R5 | F1 conflates semantic totality with operational termination | **Accepted** | F1 rewritten; taxonomy completeness kept as *necessary* (typed-halting + aperture spec), termination carried by the measure |
| R6 | Functoriality is claim-specific, not binary; symmetry gate underspecified (σ(F)−F ∈ I insufficient; inverse action needed) | **Accepted with amendment** | transport_variance enum adopted. Amendment: in Noetherian carriers the inverse containment is derivable (chain argument); certificate = automorphism + generator-wise containment + chain citation; explicit inverse containment required only off-Noetherian |
| R7 | "No cheaper witness than GB" for negative membership is false (separating ring-map witness) | **Accepted** | Negative-membership route ladder N1/N2/N3 adopted. Consequence: KN spec W3 drops from GB-grade to evaluation-grade (separate one-line amendment to `KN_CLOSURE_SPEC.md`) |
| R8 | Numeric margin not meaningful for structural scout outputs; low margin should price, not block; B2 conflicts with D4 and generic-with-exceptional-fibres objects | **Accepted** | stability_readout enum adopted; B2 rewritten as the fitting-admissibility law (which D4 already satisfied locally) |
| R9 | E2 declares one operator across domains on an unexhibited intertwiner — violates A3 as written | **Accepted — my own law biting me** | E2 split: per-domain content normative; cross-domain unification demoted to shared transport interface at comparison grade; cor:gauge scoped to the gauge system only |
| R10 | Scope nonvacuity needs outcome trichotomy; rational witness sufficient not necessary | **Accepted with amendment** | Trichotomy adopted. Amendment: geometric-vs-real scope semantics must be declared (saturation route certifies over the algebraic closure only) |
| — | Smaller corrections (C1 replay realism, drop complexity-class claim, C2 deterministic primes + homomorphic scoping, C3 assurance profile, D3 2×2 pivots + HIGHER_JET_REQUIRED, D4 degree bounds, B4 provenance pins, A5 adequacy, A3 weaker morphisms) | **All accepted** | Folded into the respective entries |

**Pushbacks (two, held):**

1. **Budget refusal.** REFUSED_BUDGET is a valid typed terminal —
   conceded. But a budget halt on an edge that *failed strict descent*
   (a cycle the measure should have rejected before resources were
   spent) remains a **DEFECT**, and the audit's own state machine
   carries the state for it. Both outcomes exist; the distinction is
   checkable from the edge log (was a certified decrease recorded for
   every recursive edge preceding the halt?).
2. **Symmetry inverse check.** Required in general; *derivable* in
   Noetherian carriers (σ(I) ⊆ I with σ an automorphism forces
   σ(I) = I via stabilization of I ⊆ σ⁻¹(I) ⊆ σ⁻²(I) ⊆ …). The gate
   demands the cheaper certificate where the theorem applies and the
   explicit inverse containment where it does not.

**Amendments contributed beyond the audit (three):**

1. **Zero-divisor SPLIT route (E1):** a certified nontrivial cover from
   three certificates — g·h ∈ √I, g ∉ √I, h ∉ √I — with no minimal-
   prime computation; full decomposition is the fallback, not the law.
2. **Scope semantics fork (E3):** geometric vs real nonvacuity are
   different claims; the scope object declares which it certifies.
3. **W3 downgrade (KN spec):** extremal noncancellation is
   nonmembership-shaped; one exact evaluation at a rational stratum
   point discharges it at N1 grade.

---

## 0b. Changelog summary

| # | Item | Anchor in v1.1 | Action | Tags |
|---|------|----------------|--------|------|
| A1 | Certified-lowering IR law | L0 | new law | L1, R1 |
| A2 | Warrant vector (four axes) | certificate envelope, §6.5 | new fields + columns | S1, R2 |
| A3 | Identification & transport morphisms | Laws | new law | S2, R6 |
| A4 | Salvage-manifest refusal law | §22 refusal envelope | amend | L7 |
| A5 | Observation-adequacy law | Laws | new law | L6b, R-small |
| A6 | Spine-correspondence remark | §7 preamble | non-normative | S4 |
| B1 | Stability readout | scout output schema, §7 | new field + pricing rule | L3a, R8 |
| B2 | Fitting-admissibility law | scout plane | new law | L6a, R8 |
| B3 | Mutual-nullity guard | §22 events | new rule + event | L3c |
| B4 | Scout calibration ledger | §21 | telemetry object + provenance pins | L3b, R-small |
| B5 | Structure-driven scheduling | §10.1 step 7 | strengthen to law | — |
| B6 | Centrifuge scout catalogue | scout plane | **non-normative** section | C-OP, audit |
| C1 | Deterministic bounded replay | L3 / checker | new law | U4, R-small |
| C2 | Homomorphic mod-p prescreen | L3 | new step | U4, R-small |
| C3 | Parser-diverse verification | checker | amend + assurance profile | U4, R-small |
| C4 | transport_variance + symmetry gate | §6.5, planner moves | new column + move | U5, L6c, R6 |
| C5 | Negative-claim certificates (typed) | §6.5, §16, §22.3 | new rows/routes | U6, R3, R7 |
| C6 | Warrant-vector composition | certificate composition | new rule | S1, R2 |
| D1 | Route-B sourcing + the IX certificate | §11.7, §11.9, cost model | new rule | U2, audit |
| D2 | Floor doctrine | cost model, §16 | route-ordering law | L5 |
| D3 | Exact inertia classifier (2×2 pivots) | §17 | new primitive | L4, R-small |
| D4 | Evaluate–interpolate lane (bounded) | L6 | new lane | L2, R-small |
| E1 | Descent: scout-propose / certificate-decide + measure | Law 5, §22 | **replaces** v1.2 E1 | U1, R4 |
| E2 | Fibre transport: per-domain normative, interface cross-domain | §14, §15, §18 | **replaces** v1.2 E2 | S3, R9 |
| E3 | Scope composition, trichotomy, semantics fork | result envelope, §22.3 | rule + outcomes | U3, R10 |
| F1 | Totality vs termination + final states | §4 / Law 12 | **replaces** v1.2 F1 | R5 |
| G | Unification appendix | new appendix | non-normative | K1–K4 |
| H | Integration map + open items | new appendix | new | — |

---

# Part A — Constitutional layer

## A1. LAW — Certified lowering of one semantic IR (anchor: L0) [L1, R1]

There is exactly **one canonical semantic IR** per claim, fixture, and
expression — the single source of meaning. Backends do not consume it
directly; each consumes a **hash-bound lowering**:

    CanonicalIR --certified lowering--> BackendIR
    BackendIR   --execution-->          BackendResult
    BackendResult --typed decoding-->   Candidate

The lowering and decoding maps are typed, versioned, and independently
checkable; the lowering artifact is pinned by hash to the IR it lowers.
Backends may maintain private optimized representations (bit-packed F2,
packed monomials, interval boxes) — what is forbidden is a backend
*re-parsing or re-deriving semantics* from anything but a certified
lowering.

**Typed interpretation table** (normative — each backend declares its
relation to the semantics; this scopes which downstream rules apply):

| Backend | Interpretation | Notes |
|---|---|---|
| GF(p) | **homomorphic image** (prime admissible: divides no pinned denominator/leading datum) | sound-rejection rules (C2) apply |
| interval | **enclosure** | soundness = containment, never equality |
| float | **lossy observation** | scout-only; never verdict-bearing |
| jet / tower | **algebra extension** | exact; carries its own typed arithmetic |
| exact QQ / ZZ | **identity** | the certifying semantics |

Admission gate for the IR (unchanged): allowlist + denylist pair;
cost-ordered validation cascade (length → token → AST depth).

## A2. Certificate fields — the warrant vector (anchor: certificate envelope; §6.5) [S1, R2]

The single ordered "warrant" label is replaced by **four orthogonal
axes**, all mandatory on every certificate:

    proof_grade:       SELF_CONTAINED | THEOREM_REDUCTION | RELATIVE_CERTIFICATE
    dependency_state:  INLINE_VERIFIED | PINNED_VERIFIED | PINNED_UNVERIFIED
    relation_grade:    IDENTITY | ISOMORPHISM | INTERTWINER | COMPARISON_ONLY
    scope:             {assumptions, family, localization, characteristic}

Semantics: `proof_grade` records how the claim is warranted;
`dependency_state` records whether banked inputs have been re-verified;
`relation_grade` records how the claim relates to the object it is
cited for; `scope` records the declared hypotheses as data. A rigorous
theorem about a declared family is *not* weaker for having hypotheses —
its hypotheses live in `scope`, not in a demoted grade.

**Admissibility rule:** a `COMPARISON_ONLY` edge is **inadmissible in a
proof DAG** — it carries no certifying weight at all and may appear
only in commentary/bridge registers. (Replaces "bridge lowers the
warrant.")

Continuity mapping to the spine's editorial labels (informative):
Established ≈ (SELF_CONTAINED|THEOREM_REDUCTION, INLINE/PINNED_VERIFIED);
Realization ≈ same proof grades with nonempty family `scope`;
Conditional ≈ PINNED_UNVERIFIED on any axis; Bridge ≈ COMPARISON_ONLY.

## A3. LAW — Identification and transport morphisms (anchor: Laws) [S2, R6]

**Identification** (merging two objects, substituting one for another
everywhere) requires an **isomorphism certificate**: the explicit map,
equivariance where a group acts, and the inverse (or canonical-form
equality). Structural resemblance licenses at most `COMPARISON_ONLY`.
Resemblance is not a map.

**Transport** (carrying one claim across, without identification) is
weaker and claim-specific: a claim may transport along a certified
morphism whose strength meets that claim's `transport_variance`
requirement (C4). Isomorphism is reserved for identification; transport
does not require it.

## A4. LAW — Salvage manifest (anchor: §22 refusal envelope) [L7]

Unchanged from v1.2: every refusal of a composite claim enumerates the
sub-obligations individually discharged, each with its standing
certificate and warrant vector. A composite refusal without a salvage
manifest is malformed.

## A5. LAW — Observation adequacy (anchor: Laws) [L6b, R-small]

For every claim, the selected observation family must carry a
**claim-specific adequacy certificate**: a stated and checked theorem
that the observed channels suffice to decide the claim. Derived/shadow
channels (jets, parities, valuations, projections) may dominate the
evidence *when their adequacy for the claim is certified*; when it is
not, an object-level channel is required. Canonical instances retained
as adequacy examples: homogeneity requires the function channel
(derivatives are blind to constants — the derivative family is
certified *inadequate* alone); Kummer rank requires the generator-level
upper bound (parity rows alone are certified inadequate — they bound
from one side only).

## A6. Non-normative remark — spine correspondence (anchor: §7 preamble) [S4]

Unchanged: the route ladder instantiates the spine's proof order
(carrier → orbit quotient → account fibre → admissible selection →
typed strata → local normal form). Motivational, no normative force.

---

# Part B — Scout plane

## B1. RULE — Stability readout (anchor: scout output schema; §7) [L3a, R8]

Every scout verdict carries a typed **stability readout**:

    NUMERIC_MARGIN(value, derived_floor)   — numeric decisions
    DISCRETE_AGREEMENT(count, exceptions)  — clusters, patterns, supports
    STRUCTURAL_GAP(witness)                — e.g. rank gap, degree gap
    NOT_APPLICABLE                          — declared, never defaulted

Low stability **prices** routes — it raises the expected cost of
certifying the candidate and may advise refinement first — but does not
categorically block exact checking: when the exact check is cheaper
than another refinement round, the planner may take it. (Replaces the
v1.2 hard escalation gate; `LOW_MARGIN_ESCALATION` event retired in
favour of cost-model input.)

## B2. LAW — Fitting admissibility (anchor: scout plane) [L6a, R8]

Aggregate fitting (regression, interpolation, cluster consensus) **may
propose a candidate**. Certification of a fitted object requires, in
full:

1. a **certified degree/complexity bound** for the object being fitted;
2. **admissible sample points** (typed per backend: good primes,
   distinct integer nodes, non-degenerate specializations);
3. **exact reconstruction** over the exact semantics;
4. **per-sample residual replay** (the reconstructed object re-checked
   at every sample);
5. a final **defining-identity certificate** for the reconstructed
   object.

Per-sample agreement remains the preferred *scout consensus* mechanism
where structure is expected constant across samples; objects with
legitimate exceptional fibres declare their exceptional loci instead of
failing consensus. (This is the general law D4 already satisfied
locally; the April homogeneity lesson survives exactly as: the polyfit
aliased *because* no degree bound was pinned — condition 1.)

## B3. RULE — Mutual-nullity guard (anchor: §22 events) [L3c]

Unchanged: a dual-lane disagreement is a conflict only if both lanes
are certified able to resolve the quantity; otherwise
`DUAL_LANE_UNRESOLVABLE`. Bad-prime disagreements are special cases.

## B4. Telemetry — scout calibration ledger (anchor: §21) [L3b, R-small]

Unchanged in substance: post-certification winner audits feed a
calibration ledger; the planner's cost model reads it; the ledger may
reorder attempts, never touch verdicts. **Addition (reproducibility):**
every route decision records the **calibration-ledger snapshot hash and
planner version** in its provenance, so adaptive planning replays
deterministically.

## B5. LAW — Structure-driven scheduling (anchor: §10.1 step 7) [—]

Unchanged: iteration scheduling is driven by the full structure of
prior iterations, never a scalar success/failure residual alone.

## B6. NON-NORMATIVE — the centrifuge scout catalogue (anchor: scout plane) [C-OP]

Re-marked non-normative per audit: the four centrifuge readouts —
round-trip residual, recursive drift, permutation/role transport,
parameter sweep + phase-transition — form the kernel's recommended
scout vocabulary, with the role assignments of v1.2 (triangularity
detection; functoriality scouting; nonvacuity-witness and boundary
scouting; two-way containment pre-check). All four **propose only**;
in every case the corresponding exact certificate decides. No normative
claim depends on this section.

---

# Part C — Certifier plane

## C1. LAW — Deterministic bounded replay (anchor: L3, checker spec) [U4, R-small]

Every certificate is verified by a **deterministic, bounded replay
checker**: the prover serializes every choice (reduction steps,
multipliers, orderings, branches) into the witness; the checker
executes a deterministic pass over the certificate DAG — loops over
recorded steps, sorting, and canonicalization are permitted — with **no
search and no choice points**. Verification cost is bounded by
certificate size. (The v1.2 "complexity class strictly below the
prover's" claim is withdrawn — no theorem was supplied; boundedness by
certificate size is the enforceable statement.) Hilbert-series and
regular-sequence checkers are brought into replay form: the prover
emits the full trace; the checker replays it.

## C2. STEP — Homomorphic mod-p prescreen (anchor: L3 verification pipeline) [U4, R-small]

Certificate identities are pre-screened by replay modulo prescreen
primes **derived deterministically from the certificate hash** (byte
stability across runs), each certified admissible (dividing no pinned
denominator or leading datum). Scope: **homomorphic polynomial
identities only**, per A1's interpretation table — for a good prime,
failure mod p is a sound rejection of the exact identity. Survivors
proceed to exact replay. Event: `CERTIFICATE_PRESCREEN_REJECT`.

## C3. RULE — Parser-diverse verification (anchor: checker spec) [U4, R-small]

The independent verifiers share no serialization or parsing code.
Dual verification runs as a **high-assurance profile** — mandatory for
trust-root certificates and final closures; optional per planner policy
where runtime cost is material.

## C4. Matrix column + planner move — transport variance (anchor: §6.5; planner moves) [U5, L6c, R6]

The binary functoriality column is replaced by **transport_variance**:

    COVARIANT_IDENTITY            — polynomial identities; push forward
                                    along any ring homomorphism by
                                    mapping the witness
    INVARIANT_UNDER_ISOMORPHISM   — primality, reducedness as such,
                                    dimension: transport across ring
                                    isomorphisms
    BASE_CHANGE_WITH_HYPOTHESES   — claims transporting under declared
                                    base change (e.g. dimension under
                                    suitable field extension;
                                    reducedness under separable
                                    extension) — hypotheses recorded
    ORDER_PRESERVING_ONLY         — Gröbner status: transports only
                                    under variable renamings preserving
                                    the declared order
    NONTRANSPORTABLE              — everything else; re-establish after
                                    any map

Transport is a first-class planner move; a transport request whose
certified morphism does not meet the claim's variance requirement
raises `TRANSPORT_UNSUPPORTED`.

**Symmetry admission gate (corrected):** a group action is admitted to
the declared-symmetry registry for orbit transport only on a
certificate comprising: (i) σ certified an **automorphism** of the
carrier (endomorphisms do not qualify); (ii) **generator-wise
containment** σ(fᵢ) ∈ I for every generator; (iii) closure of the
action: in Noetherian carriers, a citation of the chain argument
(σ(I) ⊆ I with σ invertible forces σ(I) = I); off Noetherian carriers,
the explicit inverse containment σ⁻¹(fᵢ) ∈ I. Detectors (B6) scout
candidates; the admission certificate decides. Event:
`SYMMETRY_UNADMITTED`.

## C5. Negative-claim certificates, typed (anchor: §6.5; §16; §22.3) [U6, R3, R7]

**Negative membership — route ladder (cheapest first):**

    N1  separating ring-map witness:
        φ : R → S with φ(I) = 0 (checked on generators) and φ(f) ≠ 0.
        Verification: m+1 evaluations. (Example: I = ⟨x⟩, f = 1,
        φ = evaluation at 0.)
    N2  separating linear functional on a finite quotient:
        λ with λ(I) = 0 on a spanning set and λ(f) ≠ 0.
    N3  certified Gröbner basis + nonzero normal form with full
        reduction trace — the complete generic fallback, inheriting
        the basis certificate's grade and cost.

The v1.2 claim "no cheaper witness than N3" is withdrawn.
(Consequence, recorded here and to be amended into
`KN_CLOSURE_SPEC.md`: W3 — extremal noncancellation — is
nonmembership-shaped and discharges at N1 grade by one exact evaluation
at a rational point of the stratum where the coefficient is nonzero.)

**Real emptiness — typed certificate forms**, each recording the exact
theorem and hypotheses it invokes:

    REAL_EMPTY_STURM              — univariate / slice-scheduled:
                                    Sturm-chain data, schedule declared
    REAL_EMPTY_PREORDERING        — Krivine–Stengle: for equalities
                                    fᵢ = 0 and inequalities gⱼ ≥ 0,
                                    −1 = Σᵢ hᵢ·fᵢ
                                        + Σ_{α∈{0,1}^m} σ_α·∏ⱼ gⱼ^{αⱼ}
                                    with hᵢ arbitrary polynomials and
                                    σ_α sums of squares (recorded as
                                    square lists); replay-checkable
    REAL_EMPTY_ARCHIMEDEAN_MODULE — quadratic-module form, admissible
                                    only with a certified Archimedean
                                    hypothesis (recorded)
    REAL_EMPTY_CAD_CELL           — cell-decomposition emptiness with
                                    the cell certificate attached

Strict inequalities and inequations enter via their typed encodings
(g ≠ 0 as g·t − 1 = 0 with fresh t; g > 0 as g·t² − 1 = 0), declared in
the certificate. The v1.2 formula (−1 = σ₀ + Σσᵢfᵢ, all multipliers
SOS) is withdrawn as the general form.

## C6. RULE — Warrant-vector composition (anchor: certificate composition) [S1, R2]

Composition acts **per axis**:

    proof_grade       = meet of constituent proof grades
    dependency_state  = meet of constituent dependency states
    relation_grade    = weakest relation on any edge; any
                        COMPARISON_ONLY edge renders the composition
                        inadmissible as proof
    scope             = union of assumptions; meet of opens (E3
                        supplies the nonvacuity obligation for the
                        meet of opens)

---

# Part D — Planner and route ladder

## D1. RULE — Route-B sourcing, with the structural certificate stated (anchor: §11.7, §11.9, cost model) [U2, audit]

Route B is Gröbner-free **iff** its height/regularity hypotheses are
sourced from structural witnesses; otherwise it is priced as one GB
plus a theorem. **The structural certificate form (normative):** a
sequence ordered so that each element is **monic in a fresh variable**
not occurring in earlier elements is a regular sequence — a monic
polynomial in a fresh variable is a non-zero-divisor over *any*
coefficient ring (leading coefficient 1), with no domain hypothesis on
intermediate quotients. The check is per-element and syntactic: (fresh
variable, leading coefficient 1); it is replayed, not searched.

Corpus instance (why §12.2's costs are legitimate):

    wᵢ² − u − Nᵢ²          monic in fresh wᵢ   (i = 1..4)
    w₁ + w₂ + w₃ + w₄ − 4M  linear (monic) in fresh M

— a height-5 regular-sequence certificate by inspection.

## D2. LAW — Floor doctrine (anchor: cost model; §16) [L5]

Unchanged: discharge every claim at the lowest sufficient invariant
floor (coefficient-level: traces, e_k, determinants, charpoly
coefficients — exact, replay-certifiable); spectrum access (root
isolation, ordering, selection) is an escalation permitted only when
the claim concerns roots as such.

## D3. Primitive — exact inertia classifier (anchor: §17) [L4, R-small]

As v1.2 — hierarchical vanishing cascade (order-0/1/2, cheapest-gate
first) as the canonical local-recognizer shape; (rank, signature,
nullity) as primary data with post-hoc labels — with two corrections:

- **Congruence reduction uses 1×1 and 2×2 pivots**: over QQ a symmetric
  form can present a zero diagonal against nonzero off-diagonal; the
  2×2 hyperbolic block [[0,b],[b,0]] contributes signature (+1, −1).
  Sylvester's law applies to the block-diagonal result. Pure QQ
  arithmetic, replayable, no eigendecomposition.
- **Typed outcome `HIGHER_JET_REQUIRED`**: when the quadratic part is
  degenerate (nullity > 0 after reduction), the classifier refuses at
  order 2 and names the escalation, rather than guessing from an
  inadequate jet (consistent with A5).

## D4. Lane — evaluate–interpolate reconstruction, bounded (anchor: L6) [L2, R-small]

As v1.2 — third reconstruction lane; integer-node exact Vandermonde —
with the admissibility conditions made explicit (they instantiate B2):
a **certified degree bound** on the parameter dependence; **distinct
admissible nodes** (typed); **pole/degree-drop checks** at each node
(a specialization that drops degree or hits a pole is inadmissible and
is replaced, with the exclusion recorded); per-node residual replay;
final defining-identity certificate for the reconstructed coefficients.

---

# Part E — Stratification, fibre transport, scope

## E1. LAW — Descent: scouts propose, certificates decide, a measure terminates (anchor: Law 5; §22) [U1, R4 — replaces v1.2 E1]

**Layer 1 — scout.** The holonomy/centrifuge readout (B6) proposes the
likely case for a stratification edge: closed loop → likely STOP;
residual with dimension defect → likely DESCEND; residual without
dimension defect → likely SPLIT. Proposals price routes; they decide
nothing.

**Layer 2 — certificate.** The edge is classified by ideal-theoretic
certificates alone:

    STOP:
        I : h^∞ = ⟨1⟩  (certified) — the inverted open is empty on
        this node. In particular h ∈ √I yields exactly this outcome:
        a legitimate CERTIFIED empty-open result, not an illegal
        query. (The v1.2 `ILLEGAL_INVERTER` event is retired.)

    DESCEND:
        I + ⟨h⟩ proper (certified), and
        dim(R/(I + ⟨h⟩)) < dim(R/I) (certified dimension drop).
        Recurse on the strictly smaller child.

    SPLIT — first route (zero-divisor witness, cheap):
        certificates g·h ∈ √I, g ∉ √I, h ∉ √I (the negative claims by
        C5's N-routes). This certifies the nontrivial cover
        V(I) = V(I + ⟨g⟩) ∪ V(I + ⟨h⟩) with both pieces proper —
        no component computation anywhere.
    SPLIT — fallback route:
        certified minimal components P₁,…,P_r with h ∈ Pᵢ for some i
        and h ∉ Pⱼ for some j; split along the certified components.

**Layer 3 — termination.** The well-founded measure

    μ(node) = (dimension,
               number of unresolved minimal supports,
               remaining obligation rank,
               declared budget)

with the rule: **every recursive edge strictly decreases a certified
algebraic component of μ.** DESCEND edges decrease dimension (certified
above). SPLIT edges decrease under the Noetherian closed-set order:
each child is a *strictly* smaller closed set, certified by the radical
non-membership witnesses (g ∉ √I means V(I+⟨g⟩) ⊊ V(I)); strictly
descending chains of closed sets in a Noetherian space are finite.
Budget is the declared final component.

**Terminal semantics of budget:** exhaustion is the valid typed refusal
`REFUSED_BUDGET` **when every preceding recursive edge carries its
certified decrease**. A budget halt on an edge lacking a certified
decrease is a `DEFECT` (pushback 1) — the measure was violated before
the budget was spent, and the edge log shows it.

## E2. Fibre transport — per-domain normative, cross-domain interface (anchor: §14, §15, §18) [S3, R9 — replaces v1.2 E2]

**Per-domain content (normative):**

- **Kummer/cover arm.** The parity matrix B records tame C₂
  monodromy/valuation parity **under its stated hypotheses** (tameness;
  odd/even valuation of the radicand along the divisor); rows are
  divisor loops, columns the adjoined square classes, entries the
  parity exponents (`ordAlongPrime` computes exactly these). Rank law
  as already disciplined in §15.2:
  rank(B) ≤ rank(square-class module), with **equality only when the
  parity lower bound meets the generator upper bound or explicit
  relation witnesses close the gap.** Nothing here cites the gauge
  theorem.
- **Defining-function gauge arm.** cor:gauge is the proved,
  ESTABLISHED content **for this system only**: σ_r fixed under gauge;
  channel displacement in ker Σ_r; orientation reversal flips odd σ_r.
- **Chart/role arm.** Permutation transport of framed jets per the
  orbit theorem, at its own warrant.

**Cross-domain claim (relation_grade = COMPARISON_ONLY):** the three
arms instantiate a **shared bundle/transport interface** — declared
structure group, transport operation, holonomy readout, base/fibre
separation (sweep and discriminant remain base-arm; transport and
holonomy fibre-arm). This interface is an engineering unification of
*shape*; it is inadmissible in any proof DAG (A2), and no theorem of
one arm underwrites another absent an exhibited intertwiner (A3). The
v1.2 sentence "three readouts of one operator" is withdrawn.

## E3. RULE — Scope composition, trichotomy, semantics fork (anchor: result envelope; §22.3) [U3, R10]

Scopes compose by meet; every composed result carries a scope-status
from the **trichotomy**:

    CERTIFIED_SCOPE_NONEMPTY
    CERTIFIED_SCOPE_EMPTY
    SCOPE_NONVACUITY_NOT_CERTIFIED

A composed result may be *emitted* at `SCOPE_NONVACUITY_NOT_CERTIFIED`
but may not be consumed as a fact about any point until upgraded.
`CERTIFIED_SCOPE_EMPTY` is the certified-nonexistence outcome (the
v1.2 name `COMPOSED_SCOPE_VACUOUS` is retired; emptiness must be
*proved*, not inferred from failure to find a point). Constituent
certificates of an empty-scope pipeline stand individually (A4).

**Nonvacuity routes (any one suffices):**

    I : h^∞ ≠ ⟨1⟩                      (geometric semantics)
    dim V(I + ⟨h⟩) < dim V(I)          (proper intersection)
    certified algebraic point           (exact coordinates in a
                                         certified extension)
    certified rational point            (sufficient, not necessary)

**Semantics fork (amendment 2):** every scope object declares whether
it certifies **geometric** nonvacuity (over the algebraic closure — the
saturation and dimension routes certify this) or **real** nonvacuity
(a real point or real-dimension certificate required). Consuming a
geometric scope certificate in a real-semantics pipeline is a typed
error.

Pipelines maintain the assumption ledger (running meet + its
scope-status), unchanged.

---

# Part F — Totality and termination

## F1. Totality vs termination (anchor: §4 / Law 12) [R5 — replaces v1.2 F1]

Two separate guarantees, never conflated:

**Semantic totality.** Every terminal state has a typed meaning. The
final state machine:

    CERTIFIED          — claim discharged with its warrant vector
    SCOUTED_RETAINED   — scouting work returned explicitly as retained,
                         uncertified evidence (delegation is an
                         internal state; it terminates only by
                         becoming CERTIFIED or SCOUTED_RETAINED)
    REFUSED_SCOPE      — typed refusal: outside the declared aperture
                         (phenomenon-by-subtraction, named)
    REFUSED_BUDGET     — typed refusal: certified descent throughout,
                         resources exhausted (E1 terminal semantics)
    DEFECT             — an invariant of the kernel itself was
                         violated (including a budget halt without
                         certified descent)

Refusal-taxonomy completeness remains **necessary**: it is the aperture
specification and the guarantee that every halt is meaningful. It is
not a termination proof.

**Operational termination.** Every run halts by the well-founded
measure of E1 (a certified strict decrease on every recursive edge) or
by an explicit declared budget. The measure carries the theorem; the
taxonomy carries the meaning. One artifact, two jobs — not three.

---

# Part G — Appendix: the unification (non-normative)

Unchanged from v1.2 in content, re-stated in v1.2r vocabulary: the
minimized datum 𝒮 = (C, G↷C, R ⊆ C/G, s : R → C) with derived quotient
and walls [K1]; the category of such systems with equivariant,
chamber-preserving, section-intertwining morphisms, in which the
non-identification guardrail is the theorem that the chart (S₃), cover
((C₂)^k), and gauge (continuous) systems are pairwise non-equivalent
objects [K2]; the gauge system as the third realization with property
(ii) carried by cor:gauge [K4]; closure as the stratification functor
landing in the category **up to typed refusal**, with the KN pilot
(`KN_CLOSURE_SPEC.md`) as its per-family discharge and the stabilizer ↦
valuation pattern (trivial ↦ 3; C₂ ↦ 4, −14/B; C₂×C₂ ↦ Newton wedge)
as the functor's output [K3].

Warrant vector of this appendix: relation_grade = COMPARISON_ONLY
except where a cited theorem carries its own grade; **inadmissible in
any proof DAG** (A2); the ordering constraint is permanent — the
appendix is built from the proved results and may never be used to
prove any of them. Key 3 stands at family scope for KN pending the
pilot; the general closure lemma remains the named obligation.

---

# Part H — Integration map and open items

## H1. Integration order (proposed)

1. A1–A5 (constitutional layer — everything cites these).
2. C1–C3, C5 (trust root: replay law, prescreen, diversity, typed
   negative claims).
3. A2 + C6 retrofit of the certificate envelope (warrant vector).
4. B1–B5, D1–D2 (planner behaviour and cost honesty).
5. E1 + F1 together (descent law and final-state machine are one
   change).
6. C4 (transport), E3 (scope), D3–D4 (primitives/lanes).
7. E2 (per-domain normative content into §14/§15/§18; interface
   paragraph marked COMPARISON_ONLY).
8. B6, A6, Part G (non-normative).
9. One-line amendment to `KN_CLOSURE_SPEC.md`: W3 discharges at N1
   (evaluation-grade) — see C5.

## H2. Typed identifiers introduced or changed

Events: `CERTIFICATE_PRESCREEN_REJECT`, `TRANSPORT_UNSUPPORTED`
(renames v1.2 `TRANSPORT_ILLEGAL`), `SYMMETRY_UNADMITTED`,
`DUAL_LANE_UNRESOLVABLE`, `HIGHER_JET_REQUIRED`.
Retired: `ILLEGAL_INVERTER` (now the STOP certificate outcome),
`LOW_MARGIN_ESCALATION` (now cost-model input),
`COMPOSED_SCOPE_VACUOUS` (now `CERTIFIED_SCOPE_EMPTY`).
Scope statuses: `CERTIFIED_SCOPE_NONEMPTY`, `CERTIFIED_SCOPE_EMPTY`,
`SCOPE_NONVACUITY_NOT_CERTIFIED`.
Final states: `CERTIFIED`, `SCOUTED_RETAINED`, `REFUSED_SCOPE`,
`REFUSED_BUDGET`, `DEFECT`.
Descent certificates: STOP / DESCEND / SPLIT (certificate outcomes;
holonomy signatures are scout hints only).
Certificate fields: warrant vector (proof_grade, dependency_state,
relation_grade, scope); transport_variance column; stability_readout.

## H3. Remains open after v1.2r

- The general closure lemma (Part G) beyond per-family discharge.
- Certificate compression (§28); C2's prescreen is implementable now.
- Square-class relation witnesses when valuation rank is inconclusive
  (§28): the witness w with w² = ∏aᵢ^{eᵢ} is its own search problem.
- Formal-proof export: unblocked in shape by C1's replay form; still
  unscheduled.
- Adequacy-certificate library (A5): the per-claim adequacy theorems
  accumulate as they are proved; the law is in force from merge, with
  the two canonical instances seeded.

**END**
