# Cella Pathfinder Kernel Architecture — v1.2 Upgrade Specification

**Delta against `CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1_1.md`.**
Status: proposed. Every block below is written as normative spec text
with an explicit anchor into v1.1. Law and section numbering is
provisional pending integration. Nothing here is canonical until merged
by Will's hand.

Provenance tags trace each item to its origin in the design review:
U1–U6 (architecture review), L1–L7 (April codebase lifts), S1–S4
(theorem-spine lifts), K1–K4 (unification keys), C-OP (centrifuge
operators).

---

## 0. Changelog summary

| # | Item | Anchor in v1.1 | Action | Tag |
|---|------|----------------|--------|-----|
| A1 | Functorial evaluation law | L0 | new law | L1 |
| A2 | Warrant-strength lattice | certificate envelope, §6.5 | new field + column | S1 |
| A3 | Identification law | Laws | new law | S2 |
| A4 | Salvage-manifest refusal law | §22 refusal envelope | amend | L7 |
| A5 | Object-channel law | Laws | new law | L6b |
| A6 | Spine-correspondence remark | §7 preamble | non-normative note | S4 |
| B1 | Margin law | scout output schema, §7 | new field + rule | L3a |
| B2 | Per-sample consistency law | scout plane | new law | L6a |
| B3 | Mutual-nullity guard | §22 events | new rule + event | L3c |
| B4 | Scout calibration ledger | §21 | new telemetry object | L3b |
| B5 | Structure-driven scheduling | §10.1 step 7 | strengthen to law | — |
| B6 | Centrifuge scout engine | scout plane | new section | C-OP |
| C1 | Checker-makes-no-choices law | L3 / checker | new law | U4 |
| C2 | Mod-p certificate prescreen | L3 | new step | U4 |
| C3 | Parser-diverse N-version | checker | amend | U4 |
| C4 | Functoriality column + transport | §6.5, planner moves | new column + move | U5, L6c |
| C5 | Negative-claim witness rows | §6.5, §16, §22.3 | two new rows | U6 |
| C6 | Warrant propagation rule | certificate composition | new rule | S1 |
| D1 | Route-B sourcing rule | §11.7, §11.9, cost model | new rule | U2 |
| D2 | Floor doctrine | cost model, §16 | new route-ordering law | L5 |
| D3 | Exact local classifier | §17 | new primitive | L4 |
| D4 | Interpolation reconstruction lane | L6 | new lane | L2 |
| E1 | Stratification descent law | Law 5, §22 | replace termination story | U1 |
| E2 | Gauge-fibre valuation | §14, §15, §18 | new unifying section | U1/S3 |
| E3 | Scope composition + nonvacuity | result envelope, §22.3 | new rule + outcome | U3 |
| F1 | Total-accounting completeness | §4 / Law 12 | restate | — |
| G | Unification appendix (the keys) | new appendix | new | K1–K4 |
| H | Integration map + open items | new appendix | new | — |

---

# Part A — Constitutional layer

## A1. LAW — Functorial evaluation (anchor: L0) [L1]

Every claim, fixture, and expression in the kernel is represented once,
in the canonical IR. Every evaluation backend — exact QQ, GF(p) per
prime, interval, float scout, jet/tower — is a **functor over that one
IR, selected at the leaves**. No backend re-parses, re-normalizes, or
maintains a private representation of any object.

Rationale (normative): the scout and the certifier must provably
evaluate the *same object*, differing only in leaf semantics. Any
architecture in which a scout builds its own representation admits the
bug class "scout computed a different object than the certifier
checked," which is undetectable from outcomes alone. This law removes
the class, not the instances.

Admission gate for the IR (companion rule): the expression language is
bounded from both sides by a complementary **allowlist + denylist**
pair, and inputs pass a **cost-ordered validation cascade** (length →
token → AST depth), failing at the cheapest violated gate.

## A2. Certificate field — warrant strength (anchor: certificate envelope; §6.5) [S1]

Every certificate carries a mandatory `warrant` field on the four-level
lattice:

- **ESTABLISHED** — self-contained proof, or reduction to a precise
  classical theorem with hypotheses checked and certified.
- **REALIZATION** — certified relative to a declared structural
  hypothesis (a named family, a triangularity witness, a declared
  chart). The hypothesis travels *as data inside the certificate*; the
  claim must not be cited without it.
- **BRIDGE** — an exact structural comparison or shared architecture;
  no equivalence asserted, no certifying weight across the bridge.
- **CONDITIONAL** — depends on a banked artifact (certificate, run,
  companion proof) that must be re-verified before the claim bears
  load; the dependency is pinned by hash.

The §6.5 certificate matrix gains a warrant column recording the
*maximum achievable* warrant per certificate family and route.

## A3. LAW — Identification requires an isomorphism certificate (anchor: Laws) [S2]

Two objects, claims, or structures may be **merged, identified, or
substituted for one another only on a produced isomorphism/intertwiner
certificate** (an explicit map, its equivariance where a group acts,
and its inverse or a canonical-form equality). Structural resemblance,
shared symmetry pattern, or matching invariants license at most a
BRIDGE-grade comparison. Resemblance is not a map.

Corollary (transport): a result proved on object X applies to object Y
only through an exhibited intertwiner (see C4); absent one, Y is
computed independently.

## A4. LAW — Salvage manifest (anchor: §22 refusal envelope) [L7]

Every refusal of a **composite** claim must enumerate, inside the
refusal envelope, the sub-obligations that were individually
discharged, each with its standing certificate and warrant. A composite
refusal without a salvage manifest is malformed. (Generalizes the §11.6
decomposition-grade behaviour to every composite claim in the system.)

## A5. LAW — Object channel (anchor: Laws) [L6b]

The evidence set for any claim must include at least one channel that
observes the **whole object**, not only derived or quotient shadows of
it. Derived channels (jets, parities, valuations, images under
projection) support; an object-level channel decides. Canonical
instances: homogeneity requires the function channel, not only
derivative channels; Kummer rank requires the generator-level upper
bound, not only parity rows.

## A6. Non-normative remark — spine correspondence (anchor: §7 preamble) [S4]

The route ladder's control flow (IR → cheapest structural theorem →
obligation fibre → certified selection → stratified children → germ
normal form) instantiates the theorem spine's proof order (carrier →
orbit quotient → account fibre → admissible selection → typed strata →
local normal form). The ladder is not an engineering convenience; it is
the proof architecture of the research program the kernel certifies.

---

# Part B — Scout plane

## B1. RULE — Margin is a mandatory scout output (anchor: scout output schema; §7 planner) [L3a]

Every scout verdict carries a `margin`: the distance from the reported
value or classification to the **nearest decision boundary** relevant
to the claim (examples: proximity of a rational reconstruction to its
bound; a sign or rank decision near zero at working precision; an
isolation interval containing a classification threshold). A verdict
whose margin falls below its declared floor triggers **escalation
before certification is attempted** — refine primes, precision, or
isolation first; do not spend exact-verification budget on a candidate
that can flip. Planner event: `LOW_MARGIN_ESCALATION` (retryable,
pre-certification).

## B2. LAW — Per-sample consistency over aggregate fitting (anchor: scout plane) [L6a]

A scout that demands **per-sample agreement** (the same structure or
parameter recovered independently at each specialization) is
structurally stronger than one that **fits across samples**; aggregate
fits can alias onto a plausible answer for an object that has no such
structure. Regression/fitting is admitted only as a *pre-scout* (to
propose candidates), never as the consensus mechanism. Cross-prime
structure clustering already conforms; every future scout must.

## B3. RULE — Mutual-nullity guard (anchor: §22 events) [L3c]

A dual-lane disagreement is a genuine conflict **only if both lanes are
certified able to resolve the quantity** at their operating parameters.
Two lanes reporting values below their own resolution floors, or a
lane at a degenerate parameter (e.g. a bad prime), produce the
degeneracy event `DUAL_LANE_UNRESOLVABLE`, not a consensus failure.
Prime-event instances (bad-prime disagreement) are subsumed as special
cases of this rule.

## B4. Telemetry object — scout calibration ledger (anchor: §21) [L3b]

After every certified outcome, the kernel scores each scout route that
proposed a candidate against the certified truth (the "winner audit")
and appends the result to a **calibration ledger**. The planner's
expected-cost/confidence model reads this ledger to reorder routes over
time. The ledger lives strictly in the telemetry lane: it may reorder
*attempts*; it may never touch a *verdict*.

## B5. LAW — Structure-driven scheduling (anchor: §10.1 step 7) [—]

Scout iteration scheduling (next prime, next pair, next specialization)
must be driven by the full structure computed in prior iterations
(clusters, pair histories, learned reduction schedules), never by a
scalar success/failure residual alone. An iterator that computes rich
structure and steers on a scalar is architecturally wasteful and is
rejected at design review. (Promotes the existing step-7 gesture to a
law; the deprecation reason of the legacy Halley loop, stated
positively.)

## B6. Section — the centrifuge as the unified scout engine (anchor: scout plane, new section) [C-OP]

The kernel's scout plane is organized around one primitive with four
typed readouts, inherited from the framework's original centrifuge:

1. **Round-trip residual** — solve forward, reconstruct backward,
   measure what fails to close. Kernel role: the cheap pre-check of
   every two-way containment (ideal equality, basis correctness)
   before exact replay; the continuous precursor of the holonomy
   readout (E1/E2).
2. **Recursive drift** — iterate the loop; classify by whether the
   residual settles, vanishes, or runs. Kernel role: the stability
   signature feeding the stop/descend/split classifier (E1).
3. **Permutation/role transport** — cycle the object through a declared
   symmetry; compare what survives. Kernel roles: (a) triangularity
   detection — an ordering under which the round trip closes with
   vanishing residual is a triangular-solvability witness, the
   structural source Route B requires (D1); (b) empirical
   functoriality scouting — content invariant under transport is
   candidate identity-shaped (transportable) content; content that
   shifts is quantified-shaped (C4).
4. **Parameter sweep + phase-transition detection** — move through the
   base; find where structure breaks. Kernel roles: nonvacuity witness
   scouting (a point where all inverted elements are nonzero — E3) and
   boundary-locus finding for Law 5 stratification.

The four readouts are scouts without exception: each proposes; the
corresponding exact certificate (replay, triangular witness, invariance
certificate, witness point) decides.

---

# Part C — Certifier plane

## C1. LAW — The checker makes no choices (anchor: L3, checker spec) [U4]

Every certificate is a **straight-line replay**: the prover serializes
every reduction step, multiplier, ordering decision, and branch into
the witness, and the checker is a finite fold over the certificate —
multiply, add, compare under a declared order. The checker performs no
search and contains no choice points; its complexity class is strictly
below the prover's. Checkers that currently re-derive (Hilbert-series
validation, regular-sequence checking) must be brought into replay form:
the prover emits the full combinatorial trace; the checker replays it.

Consequence (recorded, not required now): replay-form certificates are
the shape that makes later formal-proof export (§28) near-free.

## C2. STEP — Mod-p certificate prescreen (anchor: L3 verification pipeline) [U4]

Every certificate identity is pre-screened by replay **modulo one or
more fresh random primes** avoiding all denominators, before the exact
QQ replay. For a good prime, failure mod p is a *sound rejection* of
the QQ identity; only survivors receive the exact replay. Event:
`CERTIFICATE_PRESCREEN_REJECT` (kills the candidate, returns to scout).
The mod-p replay is reconnaissance; the QQ replay is the warrant.

## C3. RULE — Parser-diverse N-version verification (anchor: checker spec) [U4]

The independent verifiers (compiled checker; pure-Python reference)
must **share no serialization or parsing code**. Most real-world
verifier defects live in the parser; N-version verification with a
shared parser is one bug wide.

## C4. Matrix column + planner move — certificate functoriality (anchor: §6.5; planner moves) [U5, L6c]

The certificate matrix gains a **functoriality column**:

- **Identity-shaped** certificates (membership f = Σqᵢgᵢ, containment,
  factor-product, any finite polynomial identity) are **functorial**:
  they push forward along any ring map or declared group action by
  applying the map to the witness. Transport is a first-class planner
  move, priced near zero.
- **Quantified-shaped** certificates (Gröbner-basis property,
  irreducibility, primality, dimension, any order-dependent claim) are
  **not functorial** and must be re-established after transport.
  Attempting to transport one raises `TRANSPORT_ILLEGAL`.
- **Conditional** rows state their transport hypothesis explicitly.

**Symmetry admission gate** [L6c]: a symmetry or group action may be
used for orbit transport only after a one-time exact **invariance
certificate** (e.g. σ(F) − F ∈ I, checked by replay) admits it to the
declared-symmetry registry. Detectors (B6 operator 3) scout candidate
symmetries; the admission certificate decides. Unadmitted symmetry in a
transport request raises `SYMMETRY_UNADMITTED`.

This generalizes the §19 wall practice (one substitution proof plus
sign-orbit transport) from an ad-hoc trick to kernel law: one proof per
orbit, transported by right.

## C5. Two witness rows (anchor: §6.5; §16; §22.3) [U6]

- **ELEMENT_NOT_IN_IDEAL** — certificate: a certified Gröbner basis of
  the ideal (with its own certificate and warrant) plus a recorded
  **nonzero normal form with full reduction trace**. Negative
  membership *inherits the basis certificate's grade and cost*; there
  is no cheaper witness, and the matrix must say so.
- **REAL_LOCUS_EMPTY** — certificate: a Positivstellensatz/SOS witness
  (−1 = σ₀ + Σσᵢfᵢ with each σ a recorded sum of squares over the
  ideal-plus-inequality system), replay-checkable as a polynomial
  identity with listed squares; univariate/slice cases may substitute
  Sturm-chain data with the slice schedule declared. Slots directly
  under C1's replay law.

## C6. RULE — Warrant propagation (anchor: certificate composition) [S1]

A certificate composed from constituents carries the **meet** of their
warrant strengths on the lattice
ESTABLISHED > REALIZATION > BRIDGE/CONDITIONAL. In particular, any
chain containing a REALIZATION link is REALIZATION-grade overall and
carries the union of declared structural hypotheses; a BRIDGE link
never transmits certifying weight at all.

---

# Part D — Planner and route ladder

## D1. RULE — Route-B sourcing (anchor: §11.7, §11.9, cost model) [U2]

Route B (the complete-intersection theorem route) is **Gröbner-free if
and only if its hypotheses — height and regular-sequence certificates —
are sourced from Route A/C structural witnesses** (triangular towers,
generators monic in fresh variables, linear elimination). Absent a
structural source, the generic witness for height/regularity is
dimension data, i.e. a Gröbner computation, and the planner **must
price Route B as one GB plus a theorem**. The cost model may never
present Route B as free while its hypotheses are unpaid. (The corpus
fixture IX qualifies structurally: four monic quadrics plus one linear
form — a triangular height witness by inspection; the spec must state
this is *why* the §12.2 costs are legitimate.)

## D2. LAW — Floor doctrine (anchor: cost model; §16) [L5]

Every claim is discharged at the **lowest invariant floor that
suffices**. Coefficient-level invariants — traces, elementary symmetric
functions e_k, determinants, characteristic-polynomial coefficients —
are polynomial in the input, exact, and replay-certifiable without root
isolation. Spectrum-level access (real root isolation, root ordering or
selection; the §16 real layer) is an **escalation**, permitted only
when the claim genuinely concerns root order or selection. The planner
orders routes accordingly. (Pedigree: the floor hierarchy
e_k(κ₁…κ_{n−1}) and the typed σ_r tower with parity law A-003.)

## D3. Primitive — exact local classifier (anchor: §17 germ layer) [L4]

The germ layer gains the **rank-ladder classifier**, exact by
construction:

- **Hierarchical vanishing cascade**: order-0 (on locus?) → order-1
  (gradient/linear part regular?) → order-2 (quadratic part), each gate
  strictly cheaper than the next, later stages computed only on earlier
  failure. This cascade is the canonical *shape* of every local
  recognizer in the kernel — the route ladder in miniature.
- **Signature without spectra**: (rank, signature, nullity) of a
  rational symmetric form computed by symmetric Gaussian elimination
  plus Sylvester's law of inertia — pure QQ arithmetic, no
  eigendecomposition, replay-certifiable. Consistent with D2.
- **Post-hoc labelling discipline**: the stored datum is the structural
  triple; names ("fold", "saddle-index-k") are derived labels
  downstream, never primary data.

Feeds: the tangent-cone/branch scout, and the E1 descent classifier's
local arm.

## D4. Lane — evaluation–interpolation reconstruction (anchor: L6) [L2]

L6 gains a third reconstruction lane beside CRT/rational-reconstruction
and Hensel lifting: **evaluate–interpolate**. A coefficient object
polynomial in a parameter t of known degree k is reconstructed by
evaluation at k+1 **integer nodes** followed by the exact Vandermonde
solve over QQ (exact by construction at integer nodes; deterministic;
no lifting). Canonical uses: pencil coefficient extraction
(e_k(A + tB) mixed-discriminant data), eliminant/resultant scouting by
parameter specialization, and D3-adjacent graded decompositions.
Scout/certify split: interpolated coefficients are candidates;
certification is the replay of the defining identity at the
reconstructed coefficients.

---

# Part E — Stratification, gauge fibre, scope

## E1. LAW — Stratification descent by holonomy readout (anchor: Law 5; §22) [U1]

The invariant on every stratification edge is the **residual holonomy
of claim transport around the cycle** — the centrifuge readout (B6),
promoted to the termination law. Its signature classifies the edge
three ways, and all three arms are mandatory:

- **STOP** — identity holonomy. The loop closes; the node is a fixed
  point; the correct outcome is terminal closure (e.g. the inverted
  open collapses to the unit ideal), not recursion.
- **DESCEND** — non-identity holonomy with a **dimension defect**: the
  residual is supported on a boundary strictly smaller than the node.
  Recurse on the strictly smaller child; Noetherian descent is read off
  the measurement rather than imposed.
- **SPLIT** — non-identity holonomy with **no dimension defect** (pure
  translation): the inverter vanishes identically on a whole component
  of the node. Do not recurse — **factor the node into components and
  return them to the planner**. Collapsing this arm into DESCEND is
  precisely how a component-swallowing loop defeats a termination
  argument that otherwise looks complete.

**Illegal inverter**: an inverter h with h ∈ √(node ideal) is illegal
for that node — planner event `ILLEGAL_INVERTER`, never a boundary
child. Budget exhaustion (`BOUNDARY_STRATIFICATION_BUDGET_EXCEEDED`) is
demoted from terminator to anomaly: a budget halt on a cycle the
holonomy readout should have classified is a defect, not a refusal.

Termination statement: the case tree is well-founded **by the holonomy
readout plus refusal-taxonomy completeness** (F1). Same artifact, two
jobs.

## E2. Section — gauge-fibre valuation of holonomy (anchor: unifies §14, §15, §18) [U1, S3]

Holonomy is valued in the **structure group of the declared gauge
fibre**, not in a magnitude. The scalar residual of B6 is the
continuous scout; the certified object is a group element.

- Each domain declares its structure group: **C₂^s** for the
  Kummer/cover arm (sign flips of the s adjoined square roots);
  **ker Σ_r** for the defining-function gauge arm (channel
  displacements at fixed σ_r), with the orientation flip μ < 0 acting
  as the C₂ discretization on odd σ_r; the **chart-permutation group**
  for role/chart transport.
- The **parity matrix B is a holonomy matrix**: rows are loops (small
  circuits around divisors), columns are the C₂ gauge factors (adjoined
  square roots), entries are the holonomy exponents; the order-mod-2
  computation of `ordAlongPrime` *is* the holonomy exponent
  computation. Monodromy of the cover is the holonomy of its flat
  connection; the inertia generator at a divisor is the holonomy of a
  small loop around it; Kummer rank is the rank of the holonomy matrix.
  §14 (cover/branch), §15 (Kummer/inertia/monodromy), and the §18
  inertia handoff are hereby three readouts of one operator: run the
  gauge-fibre centrifuge, read holonomy, certify over F₂.
- **Scout→certifier bridge, cited not gestured**: the continuous-to-
  discrete reconstruction is the spine's gauge-transport corollary
  (`cor:gauge`) — shape operator and all σ_r fixed under gauge, channel
  displacement in ker Σ_r, odd-σ_r sign flip under orientation
  reversal. The bridge is a proved theorem; this section cites it as
  the formal connection under the gauge-fibre centrifuge.
- **Base/fibre separation (guardrail, per A3)**: the gauge-fibre
  conversion covers the *fibre-arm* operators (transport, holonomy).
  The *base-arm* (parameter sweep, discriminant/boundary finding, E3
  witness scouting) is motion in the base and remains distinct. A
  bundle is fibre and base; conflating the arms erases the
  discriminant.

## E3. RULE — Scope composition and certified nonvacuity (anchor: result envelope; §22.3) [U3]

Scopes of certified-on-open results **compose by meet**: a pipeline
consuming results on D(h₁) and D(h₂) holds on D(h₁h₂). Any composed
result must carry a **nonvacuity certificate** for the intersected open
on its ambient stratum: an exact witness point at which every inverted
element is nonzero, or a proper-intersection dimension argument
(V(h₁h₂) meets the stratum in strictly smaller dimension). A pipeline
of individually warranted generic results whose opens have empty
intersection is a set of true statements about nothing; the kernel
makes this outcome impossible to reach silently.

New certified-nonexistence outcome: `COMPOSED_SCOPE_VACUOUS` — the
intersection of accumulated scopes is empty; the pipeline is vacuous as
composed; the constituent certificates stand individually (A4 manifest
applies).

Pipelines maintain an **assumption ledger**: the running meet of all
scopes with its nonvacuity witness, updated per composition.

---

# Part F — Completeness and termination

## F1. Restatement — completeness as total accounting (anchor: §4 / Law 12) [—]

The kernel does not promise coverage-completeness (solving every ideal
unconditionally — the conventional-CAS promise, and the source of its
cost). It promises **total accounting over arbitrary inputs**: every
input resolves to exactly one of

  certificate | delegation to the declared search primitive |
  typed refusal (phenomenon-by-subtraction, named),

with nothing silently dropped and nothing erased. The refusal
taxonomy's completeness is simultaneously (i) the aperture
specification, (ii) the termination proof of the stratifying compiler
(with E1), and (iii) the kernel's answer to arbitrary-input
completeness. One artifact, three jobs; it is built and reviewed
first.

---

# Part G — Appendix: the unification, keys cut

Status discipline applies throughout (A2 vocabulary). The ordering
constraint is permanent: this appendix is constructed **from** the
proved results of the spine and kernel and may never be used to prove
any of them.

## G1. Minimized datum [K1] — ESTABLISHED

The orbit–quotient–selection structure is the four-tuple

  𝒮 = (C, G ↷ C, R ⊆ C/G, s : R → C),

a carrier with symmetry, a chamber in the quotient, and a section over
it. The quotient Q = C/G and the wall data (stratification of ∂R̄ by
stabilizer conjugacy class) are derived functors of 𝒮, not axioms.

## G2. Category [K2] — ESTABLISHED

A morphism 𝒮 → 𝒮′ is a pair (α : G → G′, f : C → C′) with f
α-equivariant, descending to f̄ : Q → Q′ with f̄(R) ⊆ R′, and
intertwining sections: f ∘ s = s′ ∘ f̄. Composition and identities
hold; equivalence is an invertible morphism. The non-identification
guardrail becomes an in-category theorem: the local chart system
(G = S₃), the global cover system (G = (C₂)^k), and the gauge system
(continuous gauge group) are pairwise non-equivalent objects — related,
never identified (A3).

## G3. Third realization [K4] — ESTABLISHED; independence BRIDGE

The **gauge system** is a realization: carrier = defining-function jets
F̃ = μF; symmetry = gauge (log-gradient shifts; orientation C₂);
quotient = the σ_r (fixed by `cor:gauge`); account fibre = ker Σ_r;
chamber = {μ > 0}; section = graph normalization. Property (ii) of the
former conjecture — invariants factor through the quotient — is
`cor:gauge` itself, already proved. Its symmetry flavour (gauge) is
distinct from chart-permutation and deck-sign, making it the
independent third. The Pathfinder compiler instantiates the same spine
(A6) as a corroborating fourth, cover-flavoured, not load-bearing for
independence.

## G4. Closure [K3] — REALIZATION per family; CONDITIONAL in general

Closure is the stratification functor Strat : 𝒮 ↦ {(C_τ, Stab(τ),
R_τ, s_τ)} landing back in the category **up to typed refusal**: every
boundary stratum is again an object, or a named section-less child.
Closure-up-to-typed-refusal is property (v) fused with the aperture
doctrine — the last unification condition and the kernel's founding law
are one statement.

Pilot discharge: the Kerr–Newman family, per `KN_CLOSURE_SPEC.md`
(W1–W7 + E1). The pilot's confirmed pattern is the **stabilizer ↦
valuation functor**: trivial stabilizer ↦ boundary pole order 3;
C₂ (reflection-fixed) ↦ order 4 with universal coefficient −14/B
(parity kills the odd order); C₂ × C₂ (corner) ↦ direction-dependent
Newton wedge. On the pilot's closure, Key 3 stands at REALIZATION for
KN and the general lemma remains the single named obligation of the
unification.

---

# Part H — Integration map and open items

## H1. Integration order (proposed)

1. A1–A5 (constitutional laws) — everything downstream cites them.
2. C1–C3, C5 (checker laws + witness rows) — the trust root.
3. A2 + C6 (warrant lattice + propagation) — retrofit the certificate
   envelope once, early.
4. B1–B5 (scout rules) and D1–D2 (cost-model rules) — planner behaviour.
5. B6 + E1 + E2 (centrifuge, descent law, gauge fibre) — the §14/§15/§18
   unification; largest textual change.
6. C4 (functoriality + transport move), E3 (scope composition), D3–D4
   (primitives/lanes).
7. F1 restatement; A6 remark; Part G appendix.

## H2. New event/outcome types introduced

`LOW_MARGIN_ESCALATION`, `DUAL_LANE_UNRESOLVABLE`,
`CERTIFICATE_PRESCREEN_REJECT`, `TRANSPORT_ILLEGAL`,
`SYMMETRY_UNADMITTED`, `ILLEGAL_INVERTER`, `COMPOSED_SCOPE_VACUOUS`;
holonomy signatures `STOP | DESCEND | SPLIT` on stratification edges.

## H3. Remains open after v1.2

- The general closure lemma (G4) beyond per-family discharge.
- Proof/certificate compression (§28) — C2's prescreen is implementable
  now; compression proper stays open.
- Square-class relation witnesses when valuation rank is inconclusive
  (§28) — the relation witness w with w² = ∏aᵢ^{eᵢ} is its own search
  problem; named, not scheduled.
- Formal-proof export — unblocked in shape by C1 (replay form), still
  unscheduled.

**END**
