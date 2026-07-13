# CAMPAIGN BRIEF — SHAPE READOUT (completing the σ-tower on the carrier)

**Status: DRAFT — not canonical until signed by Will's hand (covenant). Drafted 2026-07-02, chat-side + container audit. Sits behind: nothing (flagship unblocked by the shape_witness gate, Will: "confirmed"→"go ahead with the campaign work"). Does NOT jump: flip_cartography remains FROZEN/RUNNING; the weld stays gated on Will's route call.**
**Genre:** campaign brief / pre-registration scaffold. Everything here is *proposed*; freezes happen on-repo with pins.

---

## 0. Charter
**Meta-thesis (one sentence):** The information the σ-tower provably discards at n≥5 — the shape component `π_shape(O)` — can be read out by an explicit, low-degree, exact-ℚ-certifiable family of Sₙ-invariants that, relative to the σ-fibration, separates role-jet orbits (8.1′-complete on the tested strata).

**Strategic placement:** downstream of Part III (dimension threshold, PROVEN), I.3/I.3a (gauge-normal form; isotypic-form lemma), and the shape_witness gate (CLOSED PASS — the calibration pair exists with exact rationals attached). Upstream of: weld route A (inherits the tensor machinery), the transport-law generalization, and any applied coupling-fault diagnostic beyond n=4.

## 1. Stage −1 — prior-wins audit (EXECUTED 2026-07-02)
**Internal (clean):** repo-wide grep for separating-invariant / Molien / Hilbert-series work: empty. Glossary, LAYER_MANIFEST, HISTORICAL_RECORD: no hits (HR rows on "separating" are unrelated refinery/lattice work). Evals: `rep_utils.py` supplies Specht characters/projectors (reused, not re-derived); no moment-invariant or fiber-separation work exists. Nearest ancestors: OG `effective_curvature_rank`, V3 `coupling_det_signature` / `coupling_invariance_signature` (design steals, catalogued in session log addendum 19's steal map).
**External (design-time oracle — anchors, not verdicts):**
- Separating-invariant framework: Derksen–Kemper (2002→); Dufresne; Dufresne–Jeffries cardinality bounds; Reimers (non-linear actions). **KNOWN.**
- Permutation groups: minimal separating sets for multisymmetric polynomials incl. monomial/permutation groups (Kemper–Lopatin–Reimers line). **KNOWN.**
- **The edge module specifically:** ℚ[x_edges]^{Sₙ} decomposition via higher Specht polynomials, with separating families for graph orbits (Hopf-algebra-of-graph-invariants line; recent separating-sets↔graph-reconstruction work). **KNOWN — this kills any absolute claim of the form "invariants of the pair module separate."**
**Consequence (binding on all claim language):** novelty may attach ONLY at (i) separation *relative to the σ-fibration* (fiber-wise completeness — not located in the oracle pass), (ii) the curvature/gauge-normal interpretation (O = gauge-invariant Hessian quotient; moments as the completion of a curvature-scalar tower), (iii) the exact-ℚ certified, n-uniform package + conjugation mechanism. Full prior-art sweep re-runs at every claim boundary.

## 2. MATHEMATICAL OBJECTS + definition freezes owed to Stage 0
- **Orbit space (DF-S1, to freeze):** pairs `(g, O)`, g regular with distinct entries (degenerate-g locus fenced to a named stratum), O ∈ pair module ≅ gauge-invariant Hessian quotient (I.3). Invariance group = Sₙ acting simultaneously on coordinates of g and pair indices of O. σ-detector = the rational bordered sums `Ê_r` (gauge-invariant, session lemma).
- **Isotypic frame (DF-S2):** projectors P_triv/P_std/P_shape from `rep_utils` characters, gated (rank/idempotency/partition) as in `witness_battery.py`; inner product = standard ℓ² on pair coordinates (Sₙ-invariant; pinned to kill coordinate-artifact ambiguity).
- **Invariant families:** degree-2 = isotypic moments `m2_X`; degree-3 = the graded space computed at Stage 0 via exact Molien/character series (counts recorded per n BEFORE any degree-3 prediction freezes).
- **σ-fiber and the slack group:** σ_r are invariant under the full `O(n−1)_g` conjugation (witness mechanism); the campaign's group is smaller (Sₙ) — the slack between the two groups is exactly where the readout lives.

## 3. CLAIM LEDGER (all rows open at NOT_YET_PROBED)
- **CL-F1 (quadratic basis).** `{m2_triv, m2_std, m2_shape}` is a basis of the Sₙ-invariant quadratics on the pair module, n≥5 (mechanism: multiplicity-freeness of `triv⊕std⊕shape` ⟹ exactly 3). Target: PROVEN, cheap. Also fixes: degree-2 + σ cannot be complete by dimension count (≤7 functions vs orbit-space dimension) — the ladder must climb to degree 3.
- **CL-F2 (generic separation).** Over a preregistered sweep of conjugation pairs (random rational g distinct entries, random H1, random g-stabilizing Cayley A) at n=5,6,7: every pair with `δ_shape ≠ 0` is separated by `m2_shape`. Target: EMPIRICAL → STRUCTURAL (mechanism extraction if any tie appears — a tie is a lead, not just a fail).
- **CL-F3 (fiber completeness at n=5) — the summit, deliberately expected PARTIAL.** The invariant vector (σ-data; degree-≤3 isotypic invariants) separates Sₙ-orbits on σ-fibers over the tested strata at n=5. Method: orbit-separation certificates / Gröbner on the fiber ideal. Honest expectation: PARTIAL with the failure locus *named exactly* — the failure locus is itself a deliverable (it tells us the next invariant's degree/type).
- **CL-F4 (n-uniformity).** Closed-form, n-uniform expressions for all degree-≤3 invariants + exact Molien counts symbolic in n. Target: symbolic/PROVEN.
- **CL-F5 (transport bridge).** General-n isotypic-block expansion of the coupling form `Δ_c`, specializing to I.3a's `2·m2_std − m2_triv` at n=3. Target: symbolic; welds the channel language to the moment language at every n.

## 4. PREREGISTERED PREDICTIONS (to be frozen per-stage with pins; stated here as the brief's stakes)
- **P-F1:** quadratic invariant count = 3 at every n≥5 (Molien check ×3 values of n).
- **P-F2:** 100% m2_shape-separation on nonzero-δ conjugation pairs in the sweep (sharp; any tie triggers mechanism-extraction arm, not silent widening).
- **P-F3:** there EXIST σ-tied pairs tied in all three m2's (degree-2 insufficiency realized by witness, not just counted — the second-order sibling of the shape_witness result).
- **P-F4:** the CL-F5 bridge identity exists in closed form with g-rational coefficients.
- **Structural side-question banked (measure, don't kill):** orbit-dimension vs fiber-dimension at n=5 (dim O(4)=6 = fiber dim 6) — are conjugation orbits generically OPEN in σ-fibers? Either answer shapes CL-F3's scope.

## 5. TEST SURFACE
n = 5, 6, 7 (7 = wall-scout only); generic-g stratum primary; named side-strata: equal-entry g (Sₙ-symmetric locus), single-edge / path / cycle O-supports (transport-law §7 dictionary); sweep sizes, seeds, and primes frozen in stage preregs.

## 6. STAGES & GATES
- **Stage 0 — freeze + calibration.** DF-S1/S2 frozen; manifest + fixtures + schema pinned; `witness_battery.py` adopted as the standing calibration control (must reproduce sha `39bed555` verdicts); exact Molien/character series per n computed and RECORDED (degree-3 counts become frozen numbers). GATE: controls green, counts recorded, Will's Go.
- **Stage A — quadratic layer.** CL-F1 proof; CL-F2 sweep ×2 byte-stable; the P-F3 witness hunt (construct the all-m2-tied pair). GATE: verdicts + any tie routed to Will.
- **Stage B — degree-3 / fiber completeness at n=5.** CL-F3 battery: orbit-separation certificates on σ-fibers; failure locus characterized exactly. GATE: PARTIAL verdict with named locus, or full pass.
- **Stage C — uniformity + bridge.** CL-F4 symbolic-in-n; CL-F5 identity. GATE: closed forms certified; arm-close draft to Will's desk.

## 7. EXPECTED FAILURE MODES
1. **Prior-art collision at claim time** (edge-module separating sets) — pre-named; crown language restricted to σ-relative + curvature framing per §1.
2. **Coordinate artifact** — inner product / pair ordering pinned in DF-S2; every invariant checked under a random Sₙ relabeling as a runtime control.
3. **Conjugation pairs unrepresentative of σ-fibers** — the §4 side-question measures it; CL-F3 uses fiber-ideal methods, not only conjugation samples.
4. **Degenerate-g leakage** — distinct-entry gate enforced; equal-entry stratum quarantined as its own fixture class.
5. **Exact-arithmetic wall at n=7** — reported as "tool wall at (n, degree, RAM)", never "impossible"; n=7 is scout-tier.

## 8. CERTIFICATION STRATEGY
Exact-ℚ on every verdict path; clause embedding + predecl pin gates (as `witness_battery.py`); projector gates mandatory; byte-stable ×2 per banked run; kills typed and armed per stage; dashboard PROPOSED deltas by object; **nothing canonical until Will signs**.

## 9. FENCES (explicitly OUT)
The weld / F_h (SN-1, own gate & route call); DBP↔Cella bridge (standing gate); n≤4 completeness (already resolved, Part III); monodromy-S₃ (CALC-10 closed); arithmetic vein (parked); substrate promotion (covenant #8).

## 10. RESERVED RULINGS — CONVERTED per PA-2 (80_PROCESS_AMENDMENTS.md, Will S-2026-07-02)
No rulings remain. B1/B5 → conventions (home = this directory; in-session sweeps). B2 → **WALL_SCOUT** Stage-0 battery: measured cost (time, memory) of projector construction + Molien series + one bordered-Jacobian rank op at n = 6, 7; inclusion threshold = container session envelope with byte-stable ×2 — a measured wall, never a preference. B3 → **ADAPTIVE DEGREE LADDER**: start 3; climb iff insufficiency at current degree is CERTIFIED (locus named) and the wall permits. B4 → **STOP-RULE**: arm closes at completeness-CERTIFIED or insufficiency-CERTIFIED-at-wall. This brief is therefore UNBLOCKED: Stage 0 = DF freezes + fixtures + WALL_SCOUT + witness-battery calibration, ready on any session's Go.
