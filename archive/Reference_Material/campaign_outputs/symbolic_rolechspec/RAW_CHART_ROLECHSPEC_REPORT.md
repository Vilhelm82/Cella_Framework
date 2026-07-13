# RAW CHART-LEVEL RoleChSpec — and the characteristic-2 faithfulness resolution (CL-H10)

Additive to Campaign H. The over-Q proof (CL-H1…H7) and the char-boundary claims
(CL-H8/CL-H9) are unchanged. CL-H9 had flagged the char-2 faithfulness analog
**OPEN**, *blocked on the raw chart-level RoleChSpec definition*. This report
supplies that object and resolves the analog. All facts are verified exactly from
our own channel engine (no external mathematics); GF(2) facts are reduced with an
explicit generator list and independently cross-checked numerically at odd-`g`
points where the `g`-monomial denominators are units mod 2.

Module: `raw_chart_rolechspec.py`. Tests: `tests/test_campaign_h_raw_chart_rolechspec.py` (16, all pass).

---

## 1. The object

The Campaign-H proof lives in the **obstruction coordinates**

```
O_ij = H_ij − g_i H_jj/(2 g_j) − g_j H_ii/(2 g_i),
```

which carry a `1/(2 g)` and are therefore **undefined in characteristic 2**. The
*raw chart-level RoleChSpec* is the **same channel engine applied to the full
Hessian `H`** instead of to the gauge-normal representative `H_perp`:

```
raw_channel_vector(g, H, k, r) := channel_vector(g, H, k, r).
```

Its channel denominators are pure powers of the chart pivot `g[k]` — **no factor
of 2** — so it is **defined in characteristic 2** (`defined_in_char2 = True`). By
contrast the obstruction map's denominator `2 g_i g_j` is even (the contrast is
pinned in the tests). Over **char ≠ 2** the raw object **equals** the gauge-normal
object (Campaign H, CL-H2): `channel_vector(g, H) = channel_vector(g, H_perp)` as
exact rationals over ℚ (`agrees_with_gauge_normal_over_Q = True`). So the raw
RoleChSpec is the correct characteristic-free extension of the Campaign-H object.

## 2. The explicit char-2 atlas

Reduced mod 2 (all roles, both radii; `i, j` denote the two indices ≠ `k`):

| channel | char-2 value |
|---|---|
| `r1 (1,0)` (off-diagonal density) | `0` |
| `r1 (0,1)` (diagonal density) | `g_k² · S`,  `S = H11(g2²+g3²) + H22(g1²+g3²) + H33(g1²+g2²)` |
| `r2 (1,1)` | `0` |
| `r2 (0,2)` | the pairwise products of `P = g2²H11+g1²H22`, `Q = g3²H11+g1²H33`, `R = g3²H22+g2²H33` |
| `r2 (2,0)` | `(g_i g_j)² · H_kk² + g_k² · ell²` |

with the single off-diagonal char-2 invariant

```
ell = g3 H12 + g2 H13 + g1 H23,     ell(H + offdiag G_g(b)) = ell(H) + 2(…) ≡ ell(H)   (char 2).
```

Every entry is a function of `{H11, H22, H33, ell}`, so the raw RoleChSpec is
invariant under the diagonal-blind char-2 gauge (`char2_gauge_invariant = True`)
and factors through the 4-dimensional char-2 quotient `{H11, H22, H33, ell}`.

## 3. The phantom direction `g gᵀ` (keystone)

The rank-one **gradient-squared** matrix `g gᵀ` (diagonal `g_i²`, off-diagonals
`g_i g_j`) is **invisible** to the raw RoleChSpec in char 2
(`grad_outer_invisible_char2 = True`, certified at four odd-`g` points × all
channels × several `t`). Yet:

- over **ℚ**, `g gᵀ = G_g(g/2)` — an honest defining-function gauge — so its
  invisibility there is expected;
- in **char 2**, `g gᵀ` has nonzero diagonal `g_i²`, which the **diagonal-blind**
  gauge `G_g(a)_ii = 2 g_i a_i = 0` cannot produce — so `g gᵀ` is **not in the
  char-2 gauge image**, yet RoleChSpec stays blind to it.

`g gᵀ` is the gauge generator that, when `1/2` dies, escapes the gauge image but
**persists as a RoleChSpec invariant** — a "phantom" gauge.

## 4. The blind spot is exactly `⟨g gᵀ⟩` — faithfulness resolved

A finite enumeration of the 4-dim char-2 quotient (basis `E11, E22, E33,
E12+E21`) at each regular GF(2) point returns **exactly one** nonzero invisible
vector, equal to the `g gᵀ` representative `(g1², g2², g3², g1 g2)`
(`char2_blind_spot`). The control directions `E11` (pure diagonal) and `E12` (the
`ell`-carrier) are **visible**, so "invisible" is not vacuous. Hence:

| quotient | dimension | RoleChSpec |
|---|---|---|
| naive char-2 analog `{H11,H22,H33,ell}` | 4 | **NOT faithful** (1-dim blind spot `⟨g gᵀ⟩`) |
| corrected `Sym₃ / (Im G_g ⊕ ⟨g gᵀ⟩)` | **3** | **FAITHFUL** |

The blind spot is geometrically `ΔH = t · g gᵀ`, i.e. `H_ii ↦ H_ii + t g_i²` and
`Δell = t(g3·g1g2 + g2·g1g3 + g1·g2g3) = 3 t g1g2g3 = t g1g2g3` in char 2.

**Dimension count is characteristic-independent.** Over char ≠ 2 the faithful
quotient is `Sym₃/Im(G_g)`, 3-dim (the carrier `O`). In char 2 the gauge collapses
`3 → 2`, but the phantom `⟨g gᵀ⟩` restores the third invariant direction, so the
faithful quotient is **3-dimensional in every characteristic**. What changes at
char 2 is only that one of the three "gauge" directions (`g gᵀ`) ceases to be a
literal defining-function gauge and survives as a RoleChSpec-only invariance.

## 5. Status

`CL-H10: PASS`; `K-H9` armed and silent (mutation-checked: replacing the phantom
with a genuinely visible direction fires K-H9 and flips the campaign to FAIL).
Byte-stable (two runs identical; `verify() = True`). CL-H1…H9 untouched.

> The char-2 faithfulness analog, flagged OPEN by Will in CL-H9, is now
> **resolved** as above. Per standing discipline this is recorded **PENDING
> Will's sign-off** — nothing canonical until then.
