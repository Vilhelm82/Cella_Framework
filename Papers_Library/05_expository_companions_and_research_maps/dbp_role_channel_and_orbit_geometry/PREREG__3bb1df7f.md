# PREREG — Campaign H: RoleChSpec Symbolic Proof Extraction

**Status:** pre-registration, recorded **before** any generated report.
**Tier:** eval-tier / proof-extraction only. No substrate promotion. Does not change Campaign A/D/E/F/G artifacts. **Campaign type: symbolic theorem extraction.**
**Discipline:** exact symbolic algebra (SymPy + `fractions`); no float / no tolerance / no NumPy in any verdict path; RoleChSpec recomputed (no cached Campaign G labels); deterministic, two-run byte-identical (same SymPy version — 1.14.0).

## Proof target (Theorem H)

For regular `g ∈ Q^3` (`g1 g2 g3 ≠ 0`) and `H1, H2 ∈ Sym_3(Q)`:

```
RoleChSpec_g(H1) = RoleChSpec_g(H2)   ⟺   O_g(H2 − H1) = 0
```

i.e. **RoleChSpec is a faithful invariant of `Sym_3(Q)/Im(G_g)`** on the regular active-role locus.

## Gauge-normal form (Lemma H1)

`a_i = H_ii/(2 g_i)` gives `H_perp = H − G_g(a)` with `diag(H_perp) = 0` and off-diagonals exactly the obstruction coordinates:

```
H_perp = [[0, O12, O13], [O12, 0, O23], [O13, O23, 0]],   O_ij = H_perp_ij.
```

`Sym_3(Q)/Im(G_g) ≅ Q^3` via `[H] ↦ O_g(H)`.

## The proof found (recorded as the registered expectation — best outcome)

A pre-derivation (SymPy, exact) over `H_perp(O)` established:

- **Lemma H2 (gauge-normal reduction):** `RoleChSpec_g(H) = RoleChSpec_g(H_perp)` — RoleChSpec depends only on `(g, O)`, not on the gauge diagonal.
- **Lemma H3 (closed formulas):** the active graph-chart channel vectors are closed rational functions of `g1,g2,g3,O12,O13,O23` for all three output roles (Product k=2, Directive k=0, Substrate k=1); the `r=2` density channels are **homogeneous quadratic** in `O` (even, `κ_int = 0`); the `r=1` density channels are **linear** in `O` (odd).
- **Lemma H4 (injectivity — the key):** the `r=1` channel vectors give 6 linear forms in `O` whose `6×3` coefficient matrix has **rank 3**; a `3×3` minor has determinant `16 g2⁴(g1²+g3²)/(g1³ g3⁶)`. Over **Q**, this is nonzero whenever `g1 g2 g3 ≠ 0` (since `g1²+g3² = 0 ⟹ g1=g3=0` over Q). Hence `O` is recovered as an **explicit linear function** of the RoleChSpec components → RoleChSpec is **injective in O** with **no exceptional stratum beyond regularity**.

**Expected outcome: BEST — a complete symbolic proof on the regular Q-locus.** The `r=1` even/`r=2` odd parity is what breaks the `O ↦ −O` sign symmetry that `r=2` alone leaves ambiguous.

## Claims

- **CL-H1** `Sym_3(Q)/Im(G_g) ≅ Q^3` via `H ↦ O_g(H)`.
- **CL-H2** `RoleChSpec_g(H) = RoleChSpec_g(H_perp)`.
- **CL-H3** closed RoleChSpec formulas in `g, O` for all active roles.
- **CL-H4** injectivity: the equality of RoleChSpec forces `O = O'` after saturating the regularity denominators (here: linear recovery, rank 3).
- **CL-H5** every denominator/singularity component typed (here: none beyond `g1 g2 g3 ≠ 0` over Q).
- **CL-H6** Campaign G retrodiction: recomputed exact-Q samples reproduce `0` faithfulness / `0` gauge-invariance counterexamples.
- **CL-H7** all symbolic/proof mutations caught.

## Kill conditions
K-H1 normal form fails · K-H2 RoleChSpec depends on gauge diagonal · K-H3 injectivity fails generically (regular `O≠O'` with equal RoleChSpec off the exceptional locus) · K-H4 exceptional locus untyped · K-H5 Campaign G retrodiction contradicted · K-H6 float/tolerance leakage.

## Non-goals
n ≥ 4; substrate promotion; another numeric search; cached Campaign G labels; claiming the proof over fields where `−1` is a square (the result is stated over Q, where sums of squares are definite).
