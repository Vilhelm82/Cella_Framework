# SN-1 HARD GATE — SPEC DIFF: Three_Channel_KG_Strong_Spec vs the step system
**Date:** 2026-07-02 · **Status:** PROPOSED — gate verdict routed to Will (SN-1 requires this check before any weld code) · **Substrate:** [CONTAINER] spec read at repo HEAD; one symbolic check (sympy, below); no battery.

## What was diffed
**Left:** `Build_Docs/reference/DBP_Curvature_Role_Reduction/Three_Channel_KG_Strong_Spec.md` (+ `..._New_Math_Extension.md` §1/§4, the κ tower at source). Repo copy byte-identical to the project mirror.
**Right:** the step system as frozen in `campaigns/flip_cartography/reports/STAGE0_step_ideal.md` DF-2 (torus embedding, tangent-projected momenta, h-cleared generators).

## Verdict: **GATE FAILS AS-WRITTEN.** The κ_{r;p,q} tower does not cover F_h without an extension or a reduction. Three concrete routes below; route choice is Will's.

## The diff, itemized

### D1 — Codimension mismatch [PROVEN, by inspection of both texts]
Every object in the spec chain is built on ONE scalar `F : ℝⁿ → ℝ` with ONE gradient border:
`H_b` (Strong Spec §3), the channel partition (§4), the n>3 mixed-discriminant tower `D_(p,q)` (§12, explicitly "for a hypersurface"), `𝓔_r(t,u)` and `𝒦(t,u)` (Extension §1, §4), and the obstruction tensor `O_ij` (dashboard I.3 — single g). Codim 1 everywhere.
F_h is a SYSTEM: on state×state the graph is cut by 8 generators in ℝ¹² (2 DEL + 2 momentum updates + 4 circle constraints) — codim 8 ambient, codim 4 intrinsic. Under no formulation is the step relation a hypersurface. No prior codim>1 channel work exists in the corpus (Stage −1 grep: clean; the only "codim" rows are CALC-28's unrelated rank-drop result).

### D2 — The step correspondence is SMOOTH; the strata live in the projections [PROVEN]
Each momentum generator is **linear in exactly one πᵢ with constant coefficient h** (verified symbolically in-container from the DF-2 Lagrangian; sympy check: deg 1, coeff h, no cross-π terms). Hence π and π′ solve out uniquely and the graph
```
Γ = { (q₀, π(q₀,q₁), q₁, π′(q₀,q₁)) : (q₀,q₁) ∈ T²×T² }
```
is an embedded smooth compact 4-manifold (injective immersion of a compact manifold). Consequence for SN-1's core claim as phrased: **Γ itself has no singular strata to find.** Fold points, the 30-branch structure, real-thinning walls, branch-12 — all are singularities/strata of the projection π_fwd : Γ → (q₀,π), not of Γ. Ghost corners are complex ideal points of the compactification, also not real points of Γ. A weld instrument must therefore be **relative** (blocked / fibered / projection-aware), not the intrinsic hypersurface machinery pointed at a variety.

### D3 — Regular-real-point assumption vs the four banked point classes
Spec requires a regular real point (`g ≠ 0`, real). Executability of SN-1's four-point test, per class:
| point class | status under as-written machinery |
|---|---|
| generic | evaluable (rational/algebraic points, exact-ℚ path exists) |
| fold (40-digit banked) | evaluable as points; but the fold CONDITION is projection-relative — as-written channels have no term that must see it (D2) |
| ghost corners (t=±i) | NOT evaluable as-written: complex, at chart infinity; needs a chart/limit convention |
| branch-12 fiber | evaluable as points; multiplicity structure again lives in the projection |

### D4 — Gauge mismatch [flagged, not resolved]
Static channel gauge = scalar rescale `F → λF` (Extension §9: channels defining-function-relative; σ_r invariant). A system has gauge `F → A(x)·F`, `A ∈ GL_c` pointwise — mixing generators. The obstruction/channel invariance analysis has never been done for this group. This is a hole AND a candidate novelty axis.

## Routes (Will's choice; can be sequenced)

**Route B — eliminant slice (as-written machinery, days-scale, recommended first).**
Stage A/B already produce genuine ONE-equation objects: the exact eliminants (k=1: `U = (T²+1)·U₃₀`) and their k-step successors on the release slice. `{E = 0}` is a plane curve/hypersurface — spec applies VERBATIM. And the slice hosts versions of all four point classes: folds = double roots (the banked 40-digit edges), ghosts = the global `(t²+1)` factor, branch-12 = real-root multiplicity structure, generic = everything else. The SN-1 four-point test becomes executable now, with the object relabeled "the eliminant surface." Scope caveat carried loudly: this probes the branched-cover projection of F_h, not F_h itself — a corollary of the unity claim, not the claim.

**Route A — multi-normal extension (the real weld; campaign spine).**
Extend the channel partition to codim c: borders = all c gradients, `q` → Gram matrix `(∇Fᵢ·∇Fⱼ)`, vector-valued second fundamental form, intrinsic invariants via the Gauss equation / normal-frame trace; channel split still monomial-definable in the physical basis. Requires: a WELD_SPEC with its own keystone-style worked example + exact-ℚ gate, and the D4 gauge analysis (GL_c). This is where the transfer-principle novelty would live if it lives anywhere.

**Route C — relative/block instrument on Γ (structurally matched to D2).**
Channel-decompose the projection-degeneracy objects: the now|next block structure of TΓ, i.e. the Jacobian `D_{q₁}(DEL)` whose determinant vanishing IS the fold condition (IFT — KNOWN BACKGROUND at that coarse level). Novelty candidate is one level finer: the self/coupling partition of that determinant in the physical basis, and which channel dies at folds vs ghosts vs branch-12. First-order (Jacobian) theory — a sibling of the Hessian tower, not an instance. Natural home of SN-1's proof obligation (fold condition ⟺ channel/discriminant vanishing).

## Recommendation (ROI order)
B → A, with C folded into A's proof-obligation. B is cheap, uses the certified strata as test masses unchanged, and either outcome pays: channel structure at fold points = first bridge evidence; flat nothing = loud cheap warning before A's spend. A is the campaign; it should get a brief (Movement 1) + Stage −1 audit at design time per the covenant, not a bolt-on.

## What freezes next (after Will's route call)
WELD_PREDECL: per-stratum degeneracy predictions committed before any battery (SN-1 requirement), object named explicitly (eliminant surface vs extended-spec F_h), point classes pinned to their banked shas, kill conditions typed, primes/precision pinned.

*Gate report ends. Nothing here is canonical; no weld code has been written.*
