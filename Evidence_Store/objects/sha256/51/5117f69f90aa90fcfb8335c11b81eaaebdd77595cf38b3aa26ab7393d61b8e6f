# Codex Task — Cubic Role-Branch Census (first loaded survey)

**Track:** Lloyd Workbench / DBP theorem verification (NOT the V4 typed-substrate eval layer — see §11).
**Status of this object:** the first application run of the calibrated branch-monodromy tracker on a surface whose monodromy was not known in advance. It does three jobs: (a) it produces a per-role branch census of the cubic surface, suitable for generator-closure testing; (b) it puts the safeguards that went in unstressed during calibration — the motion-ratio step gate and the `π_track == π_prox` cross-check — under real load, because three sheets now crowd pairwise at each branch point; (c) it is the first rung where the discriminant oracle partially withdraws and oracle-free machinery (common-frame continuation, cross-check, Hurwitz factorization) carries structural weight. The coalescence oracle plus exact-algebraic arithmetic restore a full-permutation net for this surface while it is still available.
**Author:** Claude (drafted + reference-verified — every frozen prediction in §4 is backed by a run). **Executor:** Codex. **Reviewer:** Will.
**Builds on:** the calibrated tracker and certificate layer from `codex_branch_monodromy_calibration_v2.md`. That layer is carried forward unchanged except where this task extends it (common-frame lassos, exact-algebraic oracle, Hurwitz gate).

---

## 1. Purpose

Calibration proved the tracker returns the known answer on degree-1 and degree-2 role-solves. This task points it at a surface where the answer is genuine output. Degree-2 kept the sheets well separated all the way around, so the step-safety gate and the cross-check were exercised trivially-true. A cubic role-solve has three sheets that coalesce pairwise at each branch point — so those safeguards finally take load here, by design.

The deliverable is a role-branch census: per role, the branch structure of the role-solve, the monodromy at each stratum, and the typed classification of each stratum (branch vs role-denominator pole). This is the singular-structure data that generator-closure work consumes.

---

## 2. Surface and role structure

$$F = x_1^3 + x_1 x_2 + x_3^2 - 3.$$

| Role solved | Degree in role | Structure | Stratum |
|---|---|---|---|
| `x₁` | 3 | primary loaded branch tracker, 3 sheets | branch points = roots of the `x₁`-discriminant |
| `x₂` | 1 | identity monodromy, single sheet | role-denominator **pole** at `x₁=0` (not a branch point) |
| `x₃` | 2 | square-root anchor, 2 sheets | branch point on a fixed slice |

For the `x₁`-solve fix `x₃ = 2`, giving `x₁³ + x₂x₁ + 1 = 0` (depressed cubic, `p=x₂`, `q=1`).

---

## 3. Exact-algebraic layer (sympy)

This layer is exact. It governs branch-point locations, enclosure decisions, the cycle-type prediction, and the coalescence oracle. The numerical tracker (§5–6) consumes its outputs but never relaxes them to floating-point comparisons.

**Import category check.** This is Workbench/theorem-verification code. `sympy` for exact algebraic arithmetic is the correct tool here. The Axiom-11 import bans (`sympy`, `scipy`, math-named constants, etc.) govern the **V4 typed substrate only** and do **not** apply on this track. Do not smuggle V4 substrate discipline into Workbench numerics.

### 3.1 Branch points (exact)

`Δ_{x₁}(x₂) = −4x₂³ − 27`. Branch points are the exact roots of `−4x₂³ − 27 = 0`, i.e. `x₂³ = −27/4`:

```
b₀ = −3·∛2/2                     (real)
b₁ = 3·∛2/4 − 3·∛2·√3·i/4
b₂ = 3·∛2/4 + 3·∛2·√3·i/4        (= conj b₁)
```

Carry these as sympy algebraic numbers (`Poly(-4*x2**3 - 27, x2).all_roots()`), not floats. For the numerical tracker, evaluate them to a fixed high precision (mpmath, ≥50 digits) so loop centers are reproducible.

### 3.2 Exact enclosure

All three pairwise separations are exactly equal: `|bᵢ − bⱼ|² = 27·2^(2/3)/4 ≈ 10.715`, so `|bᵢ − bⱼ| ≈ 3.2734` for every pair (the branch points form an equilateral triangle). Any rational loop radius `ρ` with `ρ² < 27·2^(2/3)/4` encloses exactly one branch point when centered on it. Verify enclosure **exactly**: for a loop centered on `bᵢ` with rational radius `ρ`, confirm `|bᵢ − bⱼ|² > ρ²` for `j ≠ i` by exact sympy comparison (not float). Loops in this task center on the exact branch points; radii are rational.

### 3.3 Coalescence oracle (exact, full-permutation net)

At each branch point `bᵢ` the cubic has a double root and a simple root, both exact:

```
double root   r(bᵢ) = −3 / (2 bᵢ)        (verified: P(r)=0 and P′(r)=0 exactly)
simple root   s(bᵢ) =  3 / bᵢ  = −2 r(bᵢ)
```

The two sheets that coalesce at `bᵢ` are the two whose values approach `r(bᵢ)`. Combined with the common-frame continuation (§5), this pins **which common-frame sheet pair** each branch point transposes — i.e. the full common-frame permutation, not just its cycle type. The oracle confirms the measured pairing at each branch point: the two sheets the tracker swaps must be the two whose values converge to the exact `r(bᵢ)` within the certified-closure margins.

---

## 4. Frozen predictions — verified, committed before execution

Every line below was reproduced by a reference run during spec authoring. Do not edit to match output.

**`x₁`-solve (3 sheets):**
- Three finite branch points at the exact cube roots of `−27/4` (§3.1).
- Each finite simple branch loop has **cycle type (2,1)** — a transposition.
- In a common frame the three finite transpositions are **distinct** (the three transpositions of S₃). *(Convention-robust: distinctness survives relabeling. The specific pair each branch point swaps is convention-dependent — measured, and oracle-confirmed, not frozen as a specific pair.)*
- **Infinity is ramified:** a large loop enclosing all three branch points has cycle type (2,1), a transposition — **not** identity.
- **Hurwitz factorization holds:** the large-loop monodromy equals the CCW-ordered product of the three lasso monodromies in a common frame.
- **Coalescence pairing:** at each branch point the swapped pair are the two sheets whose values → `−3/(2bᵢ)`.

**`x₂`-solve (1 sheet):** identity monodromy; `x₁=0` recorded as a **role-denominator pole stratum**, not branch monodromy.

**`x₃`-solve (2 sheets):** on the slice `x₁=1`, `x₃² + x₂ − 2 = 0`, loop `x₂` around `2` → **ℤ₂** swap.

---

## 5. Common-frame construction (the new capability)

This is the engineering this task adds over the calibrated tracker. Composing monodromies across loops requires them in **one** frame; per-loop labels are not comparable. The calibration harness has no such construction — build it here.

1. **Base point.** `β = 0` (rational, not a branch point; the fiber `x₁³ + 1 = 0` has three clean separated roots). Fix a sheet labeling at `β` by a deterministic ordering of the three roots (e.g. sort by `(Re, Im)`); this labeling **is** the common frame.
2. **Lassos.** For each branch point `bᵢ`, the lasso is: straight segment `β → Aᵢ` where `Aᵢ = bᵢ − ρ·(bᵢ−β)/|bᵢ−β|` (the point on the loop circle nearest `β`); a full CCW circle of radius `ρ` about `bᵢ` starting and ending at `Aᵢ`; the straight segment `Aᵢ → β` back. Continue the sheet labels along the **entire** lasso with the §6 certificate machinery. The resulting permutation, expressed in `β` labels, is `m(bᵢ)` in the common frame.
3. **Ordering.** Order the lassos by increasing argument of `(bᵢ − β)` (CCW). Document the orientation and ordering convention explicitly in the script.
4. **Large loop.** Segment `β → R`, a full CCW circle of radius `R` about `β` with `R` chosen so all three branch points are strictly inside (`R > 3.2734 + ρ`; use `R = 5`), segment `R → β` back. Continue labels → `m_big` in the common frame.
5. **Segments must stay clear.** A connecting segment that passes too close to another branch point crowds the roots; the §6 motion-ratio and fidelity gates catch this automatically and void the run. The radial segments from `β=0` to branch points at argument 60°/180°/300° are clear by construction.

---

## 6. Tracker and certificate layer (carried from calibration v2, now loaded)

Carry forward unchanged: greedy nearest-neighbour as the lowest-level primitive; the motion-ratio step-safety gate (`motion_ratio = max_motion / min_sep > 0.10 → halve step; underflow → UNCERTIFIED_STEP_MATCH`); the normalized root-fidelity residual (`R(z) = |p(z)| / Σ|a_k|·max(1,|z|)^k > 1e-9 → ROOT_FIDELITY_FAILURE`); and the certified closure gate with the **`π_track == π_prox` cross-check** (else `CONTINUATION_PROXIMITY_DISAGREEMENT`).

These are no longer trivial. Three sheets crowd pairwise near each branch point, so the step gate will actually fire and the cross-check actually has a hop to detect. `π_prox` is now a brute force over 3! = 6 permutations with the same uniqueness/separation margins (`best ≤ 0.05·min_sep`, `gap ≥ 0.25·min_sep`).

**Status vocabulary** (calibration set plus this task's additions):

```text
CERTIFIED_PERMUTATION
UNCERTIFIED_STEP_MATCH
UNCERTIFIED_CLOSURE_MATCH
NON_BIJECTIVE_CLOSURE
CONTINUATION_PROXIMITY_DISAGREEMENT
LOOP_HITS_DISCRIMINANT
ROOT_FIDELITY_FAILURE
DISCRIMINANT_ORACLE_MISMATCH          # cycle-type or branch-location disagreement
COALESCENCE_ORACLE_MISMATCH           # measured swapped pair != oracle pair (sheets not -> -3/(2b))
COMMON_FRAME_NOT_DISTINCT             # the three finite transpositions are not distinct in common frame
HURWITZ_FACTORIZATION_FAILURE         # m_big != CCW product of lassos under documented convention
```

Only `CERTIFIED_PERMUTATION` is a passing per-loop result.

---

## 7. Gate 4 — infinity / Hurwitz, in non-tautological form

Do **not** enforce `m(b1)·m(b2)·m(b3)·m(∞) = e` as the test. With `m(∞)` defined as the reversed large loop, that relation is automatic and checks nothing. Enforce the two checks that have content:

1. **Infinity ramified:** `m_big ≠ identity` (predicted: a transposition). A finite-product-is-identity assumption is wrong for this cubic.
2. **Hurwitz factorization:** `m_big == ` CCW-ordered product of the three common-frame lasso monodromies, under the documented orientation/ordering convention. This is the check that catches a hop in any single lasso, because a corrupted lasso permutation breaks the product.

`m(∞) = m_big⁻¹` follows by definition and the four-term `= e` relation is then satisfied for free — record it as a derived consistency line, not a gate.

---

## 8. Controls — wired as PASS/FAIL gates

Every gate voids the run on failure, loudly (nonzero exit + explicit `FAIL` in console and JSON).

1. **`x₁` finite branch loops certify transpositions.** Each of the three lassos returns `CERTIFIED_PERMUTATION` with cycle type (2,1).
2. **`x₁` common-frame distinctness.** The three finite transpositions are distinct in the `β` frame; else `COMMON_FRAME_NOT_DISTINCT`.
3. **`x₁` coalescence-oracle agreement.** At each branch point the swapped sheet pair are the two whose values converge to the exact `−3/(2bᵢ)`; else `COALESCENCE_ORACLE_MISMATCH`. (This is the full-permutation net.)
4. **`x₁` contractible loop.** A loop enclosing no branch point (e.g. `β`-centered, radius `1` < 1.89) returns identity.
5. **`x₁` strained non-enclosing loop.** A loop that forces substantial root motion while enclosing no branch point still returns identity. (Choose a center between branch points with radius provably below the nearest-branch distance, verified exactly.)
6. **`x₁` radius-independence.** Each lasso's monodromy is identical at `ρ ∈ {0.5, 1.0, 1.5}` (all `< 3.2734`, exact enclosure of exactly one confirmed).
7. **`x₁` infinity + Hurwitz (§7).** `m_big` is a non-identity transposition **and** equals the CCW product of the lassos; else `HURWITZ_FACTORIZATION_FAILURE`.
8. **`x₂` structural identity + pole typing.** The `x₂`-solve is degree 1, identity monodromy, and `x₁=0` is recorded as a **role-denominator pole stratum**, explicitly typed distinct from branch monodromy.
9. **`x₃` square-root swap.** On the slice `x₁=1`, looping `x₂` around `2` certifies a two-sheet ℤ₂ swap.
10. **Certificate gates.** Root-fidelity, motion-ratio safety, certified closure with `π_track == π_prox`, and byte-stability all pass on every loop.

---

## 9. Reference confirmation (reproduce these)

A reference implementation was run during spec authoring. The production run must reproduce:

```
EXACT LAYER (sympy)
  branch points: -3*2**(1/3)/2 , 3*2**(1/3)/4 -/+ 3*2**(1/3)*sqrt(3)*i/4         PASS
  pairwise |b_i-b_j|^2 = 27*2**(2/3)/4 (~10.715), equilateral                    PASS
  enclosure (center on b_i, rho in {0.5,1.0,1.5}): exactly one enclosed          PASS
  coalescence double roots r=-3/(2b): exact double roots (P=P'=0)                PASS

x1-SOLVE (common frame, beta=0)
  m(b) at each branch point: cycle type (2,1)                                    PASS
  three finite transpositions DISTINCT in common frame                          PASS
  large loop |x2|=5: cycle type (2,1) -> infinity ramified                       PASS
  Hurwitz: m_big == CCW product of the three lassos                             PASS
  coalescence pairing: swapped pair -> -3/(2b) at each branch point             PASS
  contractible loop (beta, radius 1): identity                                   PASS

x3-SOLVE
  slice x1=1, x3^2+x2-2=0, loop x2 around 2: cycle type (2) swap                 PASS

x2-SOLVE
  degree 1, identity, x1=0 typed as role-denominator pole (not branch)           PASS

CERTIFICATE
  every loop CERTIFIED_PERMUTATION; pi_track == pi_prox on every loop            PASS
  all failure-status counts zero                                                 PASS
```

If the production run diverges on these, the production code — not the reference — is suspect.

---

## 10. Scripting, JSON, byte-stability

Standing harness discipline (`TeeStream`, single JSON report with `console_log`, `RAW_OUTPUT_DIR` constant set to the Workbench raw-output convention; confirm the mount). Per-loop JSON carries the calibration schema plus: `frame` (`"common:beta=0"`), `branch_point` (exact sympy string + high-precision value), `lasso_order_index`, `pi_track`, `closure_certificate` (with `track_prox_agree`), and an `oracle` block:

```json
"oracle": {
  "cycle_type": [2, 1],
  "double_root_exact": "-3/(2*b)",
  "coalescence_pair_matches": true,
  "distinct_in_common_frame": true
}
```

Top-level: `hurwitz` block (`m_big`, `ccw_product`, `equal`, `infinity_ramified`), and `status_counts` over the full §6 vocabulary, all failure statuses zero on a pass.

**Determinism.** sympy exact arithmetic is deterministic; numerical centers come from evaluating the exact branch points at fixed precision; the tracker uses no RNG. Run twice into `/tmp/`, `diff` excluding only `timestamp`; any other difference is a leak to fix.

---

## 11. Deliverable layout and discipline

```
results/cubic_role_branch_census/
  census_script.py            # exact layer + common-frame tracker + oracle
  census_report.json          # generated, full console_log
  CENSUS.md                   # the role-branch census: per role, strata, monodromies, typing
```

- **Scope boundary.** This task ends at "census produced and certified." It does not build, parametrise, or solve for any generator. The census is the input to subsequent generator-closure work, which is out of scope here.
- **Import category.** sympy + numpy are correct on this track; the V4 Axiom-11 bans do not apply (see §3).
- **Oracle partial-withdrawal note.** The discriminant pins locations and cycle type; the coalescence oracle pins the pairing; but the same-frame assembly leans on lasso continuation and the `π_track == π_prox` cross-check. This is the first rung where oracle-free machinery carries structural weight — and the geometry finally loads it. Treat the census's correctness as resting on the certificate layer and Hurwitz consistency, with the oracle as confirmation, not sole authority.
- **Discrete output.** Every monodromy is a certified permutation read off independent cross-checks, never a magnitude against a tolerance. The pole stratum at `x₁=0` is a typed classification, not a small-magnitude reading.
- Pre-registration is the §4 frozen block, committed (with the spec) before the run; note it in the commit message. No standalone PREREG file required. Clean **task-scoped** git status; log any pre-existing dirty paths; record the commit hash. Nothing canonical until Will signs off.

---

## 12. Acceptance

Passes iff:

1. The exact layer reproduces §9 (branch points, equilateral separation, exact enclosure, exact double roots).
2. `x₁`: three finite transpositions, distinct in common frame, infinity ramified, Hurwitz factorization holds, coalescence pairing matches the oracle at every branch point.
3. `x₂`: degree-1 identity with `x₁=0` typed as a role-denominator pole.
4. `x₃`: ℤ₂ swap on the specified slice.
5. Every loop is `CERTIFIED_PERMUTATION` with `π_track == π_prox`; all controls in §8 pass; all failure-status counts zero.
6. Byte-stable across two runs (timestamp excluded); §4 committed before the run.

Only then is the census trusted, and only then do we take it to the next object.
```
