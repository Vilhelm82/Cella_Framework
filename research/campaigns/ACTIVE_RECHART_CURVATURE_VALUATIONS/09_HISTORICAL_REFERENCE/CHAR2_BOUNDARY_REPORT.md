# CHARACTERISTIC-2 BOUNDARY — Campaign H (CL-H8, CL-H9)

Additive to the over-Q proof (CL-H4/CL-H5, unchanged). All facts here are verified exactly from our own gauge algebra (no external mathematics), recomputed from the H3 channel formulas, not cached.

## CL-H8 — the sharp ceiling is char ≠ 2, by an explicit single minor

The `r=1` channel coefficient matrix (6×3 over `O = (O12,O13,O23)`) has twenty 3×3 minors. The minor on the three **coupling** rows is

```
det(rows 0,2,4) = 32 / (g1 g2 g3),     numerator = 32 = 2^5.
```

The numerator is a **unit** (constant), so this single minor is nonzero on the *entire* regular locus `g1 g2 g3 ≠ 0` over **any field where 2 is invertible** — i.e. every characteristic-0 field (ℚ, ℝ, ℂ, …) *and* every positive characteristic `≠ 2`. Hence the `r=1` linear recovery is full rank, and RoleChSpec injectivity holds, on the regular locus over **char ≠ 2** — sharper than the conservative "over Q" headline.

**On the two-Gröbner saturation.** Because this minor's numerator is already the unit `32`, the control ideal `⟨minor numerators⟩` is `⟨1⟩`, so the Rabinowitsch saturation `⟨minor numerators, 1 − t·g1 g2 g3⟩ = ⟨1⟩` is *vacuous* (it does no work). The honest certificate is the explicit minor, not the saturation. (The non-constant minors *alone* do share the zero `g = 0`, as a saturation protocol would expect — it is the coupling minor that collapses to a constant.)

## CL-H9 — char ≠ 2 is a derived structural wall, not a margin

The exclusion of char 2 is **caused**, and the cause is in our own gauge algebra.

**The gauge is diagonal-blind in char 2.** `G_g(a)_ii = 2 g_i a_i`, which is `0` in characteristic 2 — the gauge cannot move the diagonal at all.

**The off-diagonal gauge map collapses.** Writing the off-diagonal of `G_g(a)` in `(O12, O13, O23)` as a map of `a`:

```
[ O12 ]   [ g2  g1   0 ] [ a1 ]
[ O13 ] = [ g3   0  g1 ] [ a2 ],     det = -2 g1 g2 g3.
[ O23 ]   [  0  g3  g2 ] [ a3 ]
```

`det = −2 g1 g2 g3 = 0` in char 2, so the rank drops **3 → 2** (a surviving 2×2 minor `−g1 g3 ≠ 0` pins it at exactly 2 on the regular locus).

**Consequence — the carrier `O` does not exist in char 2.**

| | `Im(G_g)` | quotient `Sym_3 / Im(G_g)` |
|---|---|---|
| char ≠ 2 | 3-dimensional | `k³` — the carrier `O` |
| char = 2 | 2-dimensional | **`k⁴`** |

The faithfulness theorem (CL-H4) is *phrased in the carrier `O`*, which is the 3-dimensional quotient. In char 2 the quotient is 4-dimensional, so the theorem's very coordinates collapse. This is why char ≠ 2 is **necessary, not conservative**.

**New char-2 invariants.** Since the gauge fixes the diagonal, `H11, H22, H33` become gauge-invariant, and the off-diagonal contributes one cokernel functional

```
ell = g3 O12 + g2 O13 + g1 O23,      ell(G_g(a)) = 2(g2 g3 a1 + g1 g3 a2 + g1 g2 a3) = 0 in char 2.
```

So the char-2 quotient is `{ H11, H22, H33, ell }` (4-dimensional).

## OPEN ANALOG — ~~flagged, not closed~~ NOW RESOLVED (CL-H10)

The genuine characteristic-2 question is a **different theorem**: is RoleChSpec faithful on the 4-dimensional char-2 quotient `{ H11, H22, H33, ell }`?

It **cannot be evaluated from the H3 formulas.** Those are written in `O`-coordinates, and

```
O_ij = H_ij − g_i H_jj/(2 g_j) − g_j H_ii/(2 g_i)
```

is undefined in char 2 (the `1/(2 g)`). The blocking input is the **raw chart-level RoleChSpec definition** (the channel carriers of the full Hessian `H`, *before* the gauge-normal substitution).

**That object is now built** (`raw_chart_rolechspec.py`, `RAW_CHART_ROLECHSPEC_REPORT.md`), and it resolves the analog:

- the raw channels *are* char-2-defined and *do* see `H_ii` and `ell` (e.g. `r2(2,0) = (g_i g_j)² H_kk² + g_k² ell²`);
- but the raw RoleChSpec carries an **extra** invariance — the rank-one **phantom** `g gᵀ` (= `G_g(g/2)` over ℚ, *not* in the diagonal-blind char-2 gauge image, yet still invisible);
- the blind spot is **exactly** `⟨g gᵀ⟩` (1-dimensional).

So the **naive 4-dim analog FAILS** by one dimension, and RoleChSpec is **FAITHFUL on the corrected 3-dim quotient** `Sym₃/(Im G_g ⊕ ⟨g gᵀ⟩)` — the same dimension (3) as the char ≠ 2 carrier `O`. See **CL-H10** and `RAW_CHART_ROLECHSPEC_REPORT.md`. (Recorded **PENDING Will's sign-off**.)

## Status

`CL-H8: PASS`, `CL-H9: PASS`, `CL-H10: PASS` (char-2 faithfulness resolved); `K-H7`, `K-H8`, `K-H9` armed and silent. The over-Q headline (CL-H4/CL-H5) and the symbolic theorem (CL-H1…H3, H6, H7) are untouched. Nothing canonical until Will signs off.
