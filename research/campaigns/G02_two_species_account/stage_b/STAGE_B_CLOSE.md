# STAGE B CLOSE — the defective base point

**Graded against** frozen `PREREG.md` (pin `984b967d3205123e`, commit `0c5b9da`,
pre-battery). **Battery:** `battery_stage_b.py`, 36/36 PASS, byte-stable ×2
(stdout sha16 `7b155a2b46e13a5a`). **Kills:** K-B1..B4 armed, none fired — in
particular K-B3 silent: every cross-term stayed in ℚ. **Defects:** none.

## Results (all staked pre-battery, all held exactly)

**1. The cross-term has a closed form — exact total, not perturbative:**

```
O_{g+e,ij}(H) − O_{g,ij}(H) = (w_ij/2) · [ H_jj/(g_j g'_j) − H_ii/(g_i g'_i) ],
w_ij = g_i e_j − g_j e_i
```

**2. The radial/wedge decomposition [STRUCTURAL].** The carrier depends only on the
RAY of g (`O(H; λg) = O(H; g)`). A base-point defect therefore splits into an
invisible radial part and a visible wedge part — the two-species pattern recurses
into the parameter slot. The wedge `g ∧ e` controls everything.

**3. The cross-term reads diag(H) only.** Off-diagonal data never contaminates a
carrier reading through a defective base — base-point damage enters exclusively
through self-data.

**4. Gauge executed at a defective base is genuine damage.** `G_{g'}(a) = G_g(a) +
G_e(a)`, and `O_g(G_e(a)) ≠ 0` generically — so by RC-2 (`ker O = Im G_g`) the
execution defect is provably NOT representation motion. Witness in ℚ:
`O_g(G_e(a₁)) = (1/12, −5/3, −5/12)`.

**5. The attribution theorem (the Stage-B claim) — DEMONSTRATED.** Fold the
cross-terms into M: `rho_M* = Σ E + G_e(Σ a)`, keep `rho_R = Σ a` (intended
parameters). Then `O_g(H_final − rho_M*) = O_g(H_0)` — symbolically at n = 3, 4, 5
and exact-ℚ on the chain. **Every contamination is M-attributed in closed form; the
R-ledger stays pure.** Membership by criterion, not pedigree, exactly as the brief
demanded.

## Mutants

First-order approximation caught at finite e; R-contamination refuted by the
`O_g(G_e(a)) ≠ 0` witness; dropped correction breaks reconstruction. Battery bites.

## Status

The conjecture's derivation core is closed: Stage A (exact parameters) + Stage B
(defective base) both DEMONSTRATED at the symbolic tier. `residue.py`'s design is now
settled mathematics on this class: two ledgers, R = group parameter, cross-terms
computed by F1/F3 and folded into M by criterion. **Remaining before implementation:
Stage C — the adversarial battery (multiplicative-escape, quotient-carrier,
holonomy adversarials, interleaving sweeps with defective parameters).**
