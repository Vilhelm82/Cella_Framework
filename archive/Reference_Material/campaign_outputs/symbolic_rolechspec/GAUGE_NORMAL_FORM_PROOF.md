# GAUGE-NORMAL FORM PROOF — Campaign H (Lemma H1, CL-H1)

## Statement

For regular `g` (`g1 g2 g3 ≠ 0`), every `H ∈ Sym_3(Q)` has a **unique** gauge-normal representative

```
H_perp = H − G_g(a),   a_i = H_ii/(2 g_i),   G_g(a) = g a^T + a g^T
```

with `diag(H_perp) = 0` and off-diagonals exactly the obstruction coordinates:

```
H_perp = [[0, O12, O13], [O12, 0, O23], [O13, O23, 0]],
O_ij = H_ij − g_i H_jj/(2 g_j) − g_j H_ii/(2 g_i).
```

Hence `Sym_3(Q)/Im(G_g) ≅ Q^3` via `[H] ↦ O_g(H)`.

## Proof (verified symbolically, exact SymPy)

- **Diagonal killed:** `H_perp_ii = H_ii − 2 g_i a_i = H_ii − 2 g_i · H_ii/(2 g_i) = 0` — verified `sp.simplify(H_perp[i,i]) = 0` for all i.
- **Off-diagonal = obstruction:** `H_perp_ij = H_ij − (g_i a_j + a_i g_j) = O_ij` — verified `sp.simplify(H_perp_ij − O_ij) = 0`.
- **Im(G_g) is 3-dimensional:** the symmetric 6-vectors of `G_g(e1), G_g(e2), G_g(e3)` have **rank 3** on the regular locus (`gauge_image_rank(g) = 3`).
- **The obstruction map is surjective onto Q^3:** the Jacobian of `(O_12, O_13, O_23)` w.r.t. `(H11,H22,H33,H12,H13,H23)` has **rank 3**, and `Im(G_g)` (rank 3) is exactly its kernel (the obstruction is gauge-invariant: `O(H + G_g(b)) = O(H)`, verified symbolically). So `Sym_3(Q) = Im(G_g) ⊕ {gauge-normal}` and the quotient is `Q^3`.

**CL-H1: PASS.** Uniqueness of `a` follows from `g_i ≠ 0` (the diagonal equations `2 g_i a_i = H_ii` have a unique solution). The gauge-normal carrier `O = O_g(H)` is the complete invariant of the same-gradient gauge class.
