# THEOREM CANDIDATES — Campaign F

## Candidate Theorem F — CONFIRMED_WITHIN_BOUND (0 exceptions)

> For regular same-gradient n=3 classes in the frozen A/D/E atlas, RoleChSpec survival holds **iff** the gauge-obstruction space `O(Span_Q{H_r − H_0}; g)` is nonzero (≥ 2 gauge-inequivalent active-role sections); collapse holds **iff** it is zero (one same-gradient gauge fibre). The empirical feature `diag_support_set_size` is a support-level proxy for this obstruction space.

**Status: CONFIRMED_WITHIN_BOUND.** Mechanism verdict PASS_STRONG; 0 exceptions over 5298 classes (`obstruction_rank = 0` ⟺ collapse, `> 0` ⟺ survive).

### What kind of fact this is

This is a **measured finite-bound theorem candidate**, exact over the frozen atlas (g ∈ {(1,1,1),(1,2,3),(2,-1,1)}, entries {-2..2}). It is **not** a proof for all n=3 jets, and explicitly **not** an n ≥ 4 claim.

### Proven exact facts (independent of the labels)

- The obstruction formula `O(ΔH;g)` characterises `Im(a ↦ g a^T + a g^T)` exactly: `O = 0 ⟺ ΔH` is a same-gradient gauge image (unit-tested by construction; CL-F3).
- `obstruction_rank = 0 ⟺` all representatives share one gauge fibre (gauge-equivalence at fixed `g` is an equivalence relation).
- RoleChSpec is gauge-invariant (Campaign D, CL-D1), so one gauge fibre ⟹ one RoleChSpec ⟹ collapse. This direction is **proven**, not merely measured.

### Measured finite-bound facts (the converse)

- Over the bound, `obstruction_rank > 0 ⟹ survive` with 0 exceptions — i.e. gauge-inequivalent representatives always carry **distinct** RoleChSpec here. This is the empirically-confirmed converse; a general proof is a successor target.

### Unresolved / scope

- Whether `obstruction_rank > 0 ⟹` distinct RoleChSpec holds beyond the frozen bound (and for n ≥ 4) is **open**.
- The proxy `diag_support_set_size` is imperfect (size-6 counterexample to the `≥ 5` threshold); the exact quantity is the obstruction rank, not the support-diversity count.

## Closeout wording (earned)

> A found the channel-carrier separations. D proved which survive same-gradient gauge quotienting. E found a non-tautological structural grammar for survival/collapse. **F identified the mechanism: within the frozen bound, survival holds exactly iff the Hessian-gauge obstruction space is nonzero, and structural diversity is its support-level proxy; collapse is concentrated in structurally uniform, g-specific low-diversity normal forms.**
