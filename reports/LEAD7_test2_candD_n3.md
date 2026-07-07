# LEAD-7 Test 2 — Candidate D (output-channel norm inverse) at n=3, Kerr-Newman

**Date:** 2026-07-07. Certificate: `verification/lead7_test2_candD_n3.py`. Construction
origin: `Reference_Material/LEAD7_Candidate_D_Output_Channel_Norm_Inverse_Metric.md`
(claims, re-derived in-repo). Prereq: Test 1 (`verification/lead7_test1_candD_n2.py`,
6/6 ×2 — D reduces exactly to the paper metric A at n=2).

## Construction (re-derived)

Kerr-Newman fundamental relation (re-derived, not cited):
`M² = S/(4π) + πJ²/S + Q²/2 + πQ⁴/(4S)`, charges `(S,J,Q)`, graph value `M`. Each output
chart `E_i = f_i(M, E_j, E_k)` is a 3-input graph; its three off-diagonal Hessian entries
are the couplings — two **mass-charge** pairs `{M,j},{M,k}` and one **charge-charge** pair
`{j,k}`. Candidate D:

```
C_i(t) = [ Λ²_{M,j} + Λ²_{M,k} + t·Λ²_{j,k} ] / q_i² ,   q_i = 1+|∇f_i|²,
g_D(t)_{ii} = 1/C_i(t)   (diagonal on charge-space (S,J,Q)).   t=1 = D_Frob.
```

The three output charts were solved explicitly (outer-horizon branch) and each verified to
satisfy the KN relation.

## Curvature machinery — VALIDATED

The 3D Ricci scalar `R` and Kretschmann `K = 4 R_ab R^ab − R²` (Weyl≡0 in 3D) are computed
from **exact lambdified partials** (not finite differences — the banked LEAD-7 guard: near
a boundary the metric collapses and FD is unreliable). The Ricci code was validated on two
closed-form metrics:

| test metric | computed | expected |
|---|---|---|
| flat ℝ³, `g=diag(1,r²,r²sin²θ)` | `1.5e−41` | `0` |
| round 3-sphere radius `a=2.3`, `g=diag(a²,a²sin²χ,a²sin²χ sin²θ)` | `1.13422` | `6/a² = 1.13422` |

Independent cross-check on the KN metric itself: the interior value
`R(20,3,1) = −0.70379688` is reproduced **identically** by finite-difference and by
exact-partial evaluation.

## Results

| tier | check | result |
|---|---|---|
| **T2-1** reduction | `C_S(t),C_J(t)` at `Q→0` | **= n=2 Kerr channels, exactly, t-independent** (forced by Q-parity of the KN relation; the charge-charge coupling is odd in Q). Constraint (1) at n=3. ✓ (symbolic) |
| **T2-2** definiteness | `C_i > 0` on the wedge | positive-definite at all samples ✓ |
| **T2-3** valuation | `g_SS` vs `F=√disc` on extremal | `g_SS ~ F²` — the paper's inverse-channel collapse, preserved ✓ |
| **T2-4** curvature | `R, K` on the three role boundaries | **split verdict** — see below |

### The curvature verdict (T2-4) — the decisive tier

Exact-partial `R` and `K`, approaching each physical role boundary:

| boundary | `R` | Kretschmann `K` | verdict |
|---|---|---|---|
| **extremal `T=0`** (`√disc→0`) | → ∞ (`~F⁻³`) | → ∞ (1.3 → 172 → 1.4e5 → …) | **DIVERGES** ✓ |
| **`Ω=0` (`J→0`, Q=1)** | −12.383 (stable 6 dig) | 65.248 (stable) | **FINITE** ✗ |
| **`Φ_e=0` (`Q→0`, J=1)** | −194.47 (stable) | 37839 (stable) | **FINITE** ✗ |

`K` finite ⟹ *every* sectional curvature finite (K is the sum of squared Riemann
components in an orthonormal frame), so the finiteness on `J=0`, `Q=0` is **not** a
scalar-trace cancellation — the whole intrinsic curvature is bounded there. On those faces
the metric *component* still collapses (`g_JJ, g_QQ → 0`), but the curvature does not
diverge. This is exactly the Candidate-B lesson in a new guise: **metric collapse is
necessary but not sufficient; the curvature is the diagnostic.**

### t-scan (is the miss repairable by the free weight?)

Kretschmann at deep boundary points (`F, J, Q = 1e-6`), over the one-parameter family:

| `t` | extremal `K` | `Ω=0` `K` | `Φ_e=0` `K` |
|---|---|---|---|
| 0   | 1.3012e5 | 54.398 | 37756 |
| 1/2 | 1.3466e5 | 59.582 | 37797 |
| 1 (Frob) | 1.3929e5 | 65.248 | 37839 |
| 2   | 1.4878e5 | 78.137 | 37922 |
| 5   | 1.7921e5 | 131.54 | 38172 |

The two reflection-fixed faces stay **finite and bounded for every `t`** (they vary
smoothly, never diverging); only the extremal divergence survives. **The one free weight
`t` cannot restore the `Ω=0`/`Φ_e=0` curvature divergence** — the miss is structural to
the diagonal `D(t)` ansatz, not a tuning problem.

## Verdict

**Candidate D_Frob (and the whole diagonal `D(t)` family) is a *correct n=2 lift* but an
*incomplete* n=3 complementarity metric.** It earns four of the six canonicity
constraints outright — (1) exact reduction, (2) S₃-equivariance by construction, (3)
factors through the channels, (4) definiteness — plus the role-boundary valuation and the
**extremal** curvature divergence. It **fails** the full constraint (6): its intrinsic
curvature is finite on the two reflection-fixed role boundaries `Ω=0`, `Φ_e=0`, and the
`t` freedom does not fix it.

This is a clean, anticipated branch point, not a dead end:

- It **confirms the paper's own suspicion** (the handoff doc, §"Candidate E"): *"If
  Candidate D is too diagonal or fails the D3 test, the next stronger construction is a
  pair-channel tensor."* The diagonal ansatz is too weak — the missing divergences live in
  the off-diagonal/interaction structure the diagonal `g_D` discards.
- Mapped to the BRIEF kill-list: this is **K-2-adjacent** — the failure of the canonical
  *diagonal* S₃-equivariant lift is itself a result (the complementarity does not descend
  to a diagonal channel-inverse metric at n=3), and it selects the next construction
  (Candidate E) rather than ending the campaign.

## Next (per the handoff Test ladder)

- **Candidate E — pair-channel tensor** (doc §"Candidate E"): build the metric from pair
  incidences `θ_{i,{a,b}}` with the charge-charge pair carrying an incidence form in
  `dE_j − dE_k`, restoring off-diagonal structure. This is the construction the doc flags
  for exactly this failure mode.
- Also open: does the induced 2D curvature on each face reproduce the paper's order law
  even though the 3D scalar does not? (a weaker, possibly still-true statement worth
  pinning) — and locate the KN Davies surface D3 to complete the finite-locus side.
