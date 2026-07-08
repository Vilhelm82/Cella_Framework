# Three-Channel Gaussian Curvature `K_G`

**Strengthened canonical specification, derivation, and native-build gate**  
**Date:** 2026-06-18  
**Status:** Reference specification for an eval-tier native build first; substrate promotion remains fenced until the exact gates below pass and Will signs off.

---

## 0. Executive verdict

This document supplies the missing object for the geometry-side fence:

```text
K_G = κ_c + κ_s + κ_int
```

where:

- `κ_c` is the pure coupling channel: curvature carried only by off-diagonal Hessian structure.
- `κ_s` is the pure self/nonlinearity channel: curvature carried only by diagonal Hessian structure.
- `κ_int` is the interaction channel: curvature that exists only because self and coupling structure are simultaneously present.

The current non-negative fallback scalar is not this object. Any formula of the form `n²/g³`, `n²/(4g³)`, `κ²`, or `H²` cannot represent the signed object because it has erased the sign and the channel decomposition before the calculation begins.

The keystone discriminator is:

```text
F = x₁² + x₁x₂ + x₃² − 3,     p = (1,1,1)

κ_c   = −1/49
κ_s   = +1/49
κ_int = −3/49
K_G   = −3/49
```

Here `κ_c` and `κ_s` cancel exactly. The surviving curvature is interaction curvature. A scalar that reports only non-negative curvature, or only a single undifferentiated curvature, is blind to the regime this project actually needs.

---

## 1. Scope discipline

This specification is a **target object**, not a named-equation import. In V4/Cella terms:

```text
V4 as-built          = existing typed/stratified substrate
Cella ratified       = exact account law in the eval tier
cella-as-trunk       = proposed/fenced substrate re-founding
three-channel K_G    = missing geometry-side native object
```

The build must satisfy three separable demands:

1. **Mathematical correctness:** compute the signed Gaussian curvature and its exact three-channel partition.
2. **Cella/V4 correctness:** derive gradient, Hessian, determinant, channel terms, and final result from typed primitives with provenance, not from a naked imported formula.
3. **Promotion discipline:** pass the exact-ℚ retrodiction gate before the geometry arm is read as full-scope evidence.

Until then, HR138-style holonomy evidence should be described as `κ_c`-scope evidence, not full `K_G` evidence.

---

## 2. Setup

Let:

```text
F : ℝ³ → ℝ
S = {x ∈ ℝ³ : F(x) = 0}
p ∈ S
```

Assume `F` is twice differentiable at `p` and the point is regular:

```text
g = ∇F(p) ≠ 0
H = Hess F(p)
q = g·g = |g|²
```

Write:

```text
g = (g₁,g₂,g₃)

H = [ H₁₁ H₁₂ H₁₃
      H₁₂ H₂₂ H₂₃
      H₁₃ H₂₃ H₃₃ ]
```

Split the Hessian into diagonal/self and off-diagonal/coupling parts:

```text
H_s = diag(H₁₁,H₂₂,H₃₃)
H_c = H − H_s
```

So:

```text
tr(H_c) = 0
tr(H_c H_s) = 0
```

This split is **basis-relative**. That is not a defect here; it is the point. The physical sensor/channel basis is the diagnostic basis. Only the sum `K_G` is intrinsic. The channels are explanatory coordinates, not coordinate-free curvature invariants.

---

## 3. Signed scalar reference

Define the bordered Hessian:

```text
H_b = [ 0   g₁   g₂   g₃
        g₁  H₁₁ H₁₂ H₁₃
        g₂  H₁₂ H₂₂ H₂₃
        g₃  H₁₃ H₂₃ H₃₃ ]
```

For a regular implicit surface in `ℝ³`, the signed Gaussian curvature is:

```text
K_G = − det(H_b) / q²
```

Equivalently, because:

```text
det(H_b) = − gᵀ adj(H) g
```

we have:

```text
K_G = gᵀ adj(H) g / q²
```

The bordered-Hessian form is the better implementation cross-check because it naturally exposes the determinant expansion that yields the channels.

---

## 4. Canonical channel definition: determinant partition

Expand `det(H_b)` and partition the monomials by whether they contain only coupling Hessian entries, only self Hessian entries, or both.

The expansion decomposes exactly as:

```text
det(H_b) = Δ_c + Δ_s + Δ_m
```

where:

```text
Δ_c =  g₁²H₂₃² + g₂²H₁₃² + g₃²H₁₂²
       − 2g₁g₂H₁₃H₂₃ − 2g₁g₃H₁₂H₂₃ − 2g₂g₃H₁₂H₁₃

Δ_s = −(g₁²H₂₂H₃₃ + g₂²H₁₁H₃₃ + g₃²H₁₁H₂₂)

Δ_m =  2(g₁g₂H₁₂H₃₃ + g₁g₃H₁₃H₂₂ + g₂g₃H₁₁H₂₃)
```

The three curvature channels are then:

```text
κ_c   = −Δ_c / q²
κ_s   = −Δ_s / q²
κ_int = −Δ_m / q²
```

and therefore:

```text
K_G = κ_c + κ_s + κ_int
```

This monomial partition is the **canonical implementation form** for `n = 3`. It is exact, signed, rational in `(g,H)`, and it contains no square root. That last point matters: exact-ℚ computation should use `q = g·g`, never `|g|`, unless a later typed layer explicitly needs a normalized normal vector.

---

## 5. Derivation I: bordered-Hessian expansion

Expanding the determinant gives:

```text
det(H_b)
= −H₁₁H₂₂g₃² + 2H₁₁H₂₃g₂g₃ − H₁₁H₃₃g₂²
  + H₁₂²g₃² − 2H₁₂H₁₃g₂g₃ − 2H₁₂H₂₃g₁g₃
  + 2H₁₂H₃₃g₁g₂
  + H₁₃²g₂² + 2H₁₃H₂₂g₁g₃ − 2H₁₃H₂₃g₁g₂
  − H₂₂H₃₃g₁² + H₂₃²g₁²
```

Group the terms by Hessian monomial support:

### Pure coupling terms

Terms using only off-diagonal Hessian entries `H₁₂,H₁₃,H₂₃`:

```text
H₂₃²g₁² + H₁₃²g₂² + H₁₂²g₃²
− 2H₁₃H₂₃g₁g₂ − 2H₁₂H₂₃g₁g₃ − 2H₁₂H₁₃g₂g₃
```

This is `Δ_c`.

### Pure self terms

Terms using only diagonal Hessian entries `H₁₁,H₂₂,H₃₃`:

```text
−H₂₂H₃₃g₁² − H₁₁H₃₃g₂² − H₁₁H₂₂g₃²
```

This is `Δ_s`.

### Mixed interaction terms

Terms using one coupling Hessian entry and one self Hessian entry:

```text
2H₁₂H₃₃g₁g₂ + 2H₁₃H₂₂g₁g₃ + 2H₁₁H₂₃g₂g₃
```

This is `Δ_m`.

The partition is exhaustive and disjoint. No term is omitted and no term is counted twice.

Because `K_G = −det(H_b)/q²`, the sign of each channel is the negative of the sign of its determinant component.

---

## 6. Derivation II: shape-operator equivalence

Let:

```text
n = g/|g|
P = I − nnᵀ = I − ggᵀ/q
```

`P` projects onto the tangent plane. The implicit-surface shape operator, restricted to the tangent plane, is:

```text
Ŝ = −(1/|g|) P H P
```

Split it by the same Hessian split:

```text
Ŝ_c = −(1/|g|) P H_c P
Ŝ_s = −(1/|g|) P H_s P
Ŝ   = Ŝ_c + Ŝ_s
```

On a two-dimensional tangent plane, use:

```text
det₂(M) = 1/2( tr(M)² − tr(M²) )
```

where `det₂` means the product of the two nonzero tangent-plane eigenvalues. Then:

```text
det₂(A+B) = det₂(A) + det₂(B) + tr(A)tr(B) − tr(AB)
```

Applying this to `Ŝ = Ŝ_c + Ŝ_s` gives:

```text
κ_c   = det₂(Ŝ_c)
κ_s   = det₂(Ŝ_s)
κ_int = tr(Ŝ_c)tr(Ŝ_s) − tr(Ŝ_cŜ_s)
```

A direct trace reduction gives the closed forms:

```text
κ_c = (2gᵀH_c²g − q tr(H_c²)) / (2q²)

κ_s = (q(tr(H_s)² − tr(H_s²))
       + 2gᵀH_s²g
       − 2tr(H_s)(gᵀH_sg)) / (2q²)

κ_int = (2gᵀH_cH_sg − tr(H_s)(gᵀH_cg)) / q²
```

These are algebraically equivalent to the determinant partition above.

### The `κ_s` trap

Do not mirror the `κ_c` formula naively. This tempting expression is wrong in general:

```text
(2gᵀH_s²g − q tr(H_s²)) / (2q²)
```

It omits the `tr(H_s)²` and `tr(H_s)(gᵀH_sg)` structure. The asymmetry is real: `H_c` is traceless, while `H_s` is not. A test suite must include a mutation that swaps in this false mirror and proves the gate catches it.

---

## 7. Keystone calculation, fully worked

Take:

```text
F = x₁² + x₁x₂ + x₃² − 3
p = (1,1,1)
```

Then:

```text
g = ∇F(p) = (2x₁+x₂, x₁, 2x₃)|(1,1,1) = (3,1,2)
q = g·g = 3² + 1² + 2² = 14
q² = 196
```

and:

```text
H = [ 2 1 0
      1 0 0
      0 0 2 ]
```

So:

```text
H₁₁ = 2,  H₂₂ = 0,  H₃₃ = 2
H₁₂ = 1,  H₁₃ = 0,  H₂₃ = 0
```

### Coupling channel

```text
Δ_c = g₃²H₁₂² = 2² · 1² = 4
κ_c = −Δ_c/q² = −4/196 = −1/49
```

### Self channel

```text
Δ_s = −(g₂²H₁₁H₃₃)
    = −(1² · 2 · 2)
    = −4

κ_s = −Δ_s/q² = +4/196 = +1/49
```

### Interaction channel

```text
Δ_m = 2(g₁g₂H₁₂H₃₃)
    = 2(3 · 1 · 1 · 2)
    = 12

κ_int = −Δ_m/q² = −12/196 = −3/49
```

### Total

```text
K_G = κ_c + κ_s + κ_int
    = −1/49 + 1/49 − 3/49
    = −3/49
```

The cancellation is the whole theorem-dragon in miniature. A single-channel or non-negative scalar cannot see it.

---

## 8. Exact-ℚ retrodiction gate

A native build is not promotable until every row below passes with exact rational equality. No tolerances. No float comparisons. No sign erasure.

| Surface | Point | Expected `K_G` | `κ_c` | `κ_s` | `κ_int` | Why it is in the gate |
|---|---:|---:|---:|---:|---:|---|
| `x₁+x₂+x₃−3` | `(1,1,1)` | `0` | `0` | `0` | `0` | Flat zero-Hessian sanity check. |
| `x₁x₂+x₂x₃−2` | `(1,1,1)` | `0` | `0` | `0` | `0` | Open-chain coupling can still be developable/flat. |
| `x₁x₂+x₂x₃+x₃x₁−3` | `(1,1,1)` | `1/12` | `1/12` | `0` | `0` | Pure coupling positive curvature. |
| `x₁x₂x₃−1` | `(1,1,1)` | `1/3` | `1/3` | `0` | `0` | Multilinear pure-coupling case. |
| `x₃−x₁²−x₂²` | `(1,1,2)` | `4/81` | `0` | `4/81` | `0` | Pure self positive curvature. |
| `x₁²+x₂²+x₃²−1` | `(3/5,4/5,0)` | `1` | `0` | `1` | `0` | Sphere at rational point; avoids irrational coordinates. |
| `x₃−x₁x₂` | `(1,1,1)` | `−1/9` | `−1/9` | `0` | `0` | Pure coupling negative curvature. |
| `x₁²+x₁x₂+x₃²−3` | `(1,1,1)` | `−3/49` | `−1/49` | `1/49` | `−3/49` | Keystone cancellation; interaction carries the result. |
| `x₁²+x₂²−x₃²` | `(3,4,5)` | `0` | `0` | `0` | `0` | Full-rank indefinite Hessian but developable cone; kills rank heuristics. |

### Gate semantics

A passing implementation must prove all of these:

```text
1. got.K_G == expected.K_G
2. got.κ_c == expected.κ_c
3. got.κ_s == expected.κ_s
4. got.κ_int == expected.κ_int
5. got.K_G == got.κ_c + got.κ_s + got.κ_int
6. got.K_G == −det(H_b)/q²
7. det(H_b) == Δ_c + Δ_s + Δ_m
```

Any mismatch is a hard failure. A warning is too soft. If this gate fails, the geometry-side spine remains fenced.

---

## 9. Negative tests: what must fail

A useful implementation does not merely pass good examples. It must reject bad surrogates.

The test suite should include mutations proving that these fail:

```text
M1. Replace signed K_G with a non-negative square/proxy.
M2. Return K_G without returning κ_c, κ_s, κ_int.
M3. Use the naive mirrored κ_s formula.
M4. Drop Δ_m.
M5. Flip the bordered-Hessian sign.
M6. Treat rank(H_s) > 0 as implying κ_s ≠ 0.
M7. Treat H_c = 0 / H_s = 0 cases as generic rather than pure-case reductions.
M8. Allow float tolerance to mask a rational mismatch.
M9. Compute g,H by hand in the real path rather than through typed differentiation primitives.
M10. Promote eval-tier success directly to substrate without provenance review.
```

The keystone row should kill M1, M2, M4, and M5. The cone row should kill M6. A deliberately chosen self-curved surface should kill M3.

---

## 10. Recommended V4/Cella implementation shape

### Eval-tier first

Create an eval-tier module before substrate promotion:

```text
src/lloyd_v4/evals/three_channel_kg/
  __init__.py
  channels.py
  bordered.py
  primitives.py
  retrodiction_gate.py
  README.md

tests/
  test_three_channel_kg_exact.py
  test_three_channel_kg_retrodiction.py
  test_three_channel_kg_mutants.py
  test_three_channel_kg_provenance.py
```

### Core functions

```python
def split_hessian(H):
    """Return (H_c, H_s) with H_s diagonal and H_c off-diagonal."""


def bordered_hessian_det(g, H):
    """Exact determinant of the 4x4 bordered Hessian."""


def kg_three_channel_from_gH(g, H):
    """Exact n=3 channel computation from already-derived rational g,H."""


def derive_gH_from_surface(surface, point):
    """Use V4 typed differentiation primitives to produce exact g,H with provenance."""


def kg_three_channel(surface, point):
    """Full native eval path: derive g,H, compute channels, attach provenance."""
```

### Result carrier

Use a typed result payload shaped roughly like:

```python
@dataclass(frozen=True)
class KGThreeChannelPayload:
    surface_id: str
    point: tuple
    gradient: tuple
    hessian: tuple
    q: Fraction
    bordered_det: Fraction
    delta_c: Fraction
    delta_s: Fraction
    delta_m: Fraction
    kappa_c: Fraction
    kappa_s: Fraction
    kappa_int: Fraction
    K_G: Fraction
    checks: dict
    scope: str
    provenance: object
```

The substrate-facing result must make the status explicit:

```text
REGULAR_EXACT_Q        g ≠ 0, all values exact fractions
SINGULAR_STRATUM       g = 0, curvature undefined at this point
OUT_OF_SCOPE           non-rational input outside exact-ℚ gate
REFUSED                required typed primitive unavailable or non-provenanced
```

The important behavior is **refuse, do not lie**. At a singular point such as the cone apex, there is no curvature value to return; the correct result is a stratum/refusal, not `0`, `NaN`, or a placeholder.

---

## 11. Provenance obligations

The reference snippet may hand-supply `g` and `H` only to show the arithmetic. The native path must not.

A native V4/Cella computation must record:

```text
surface expression/source
point
V4 primitive used for gradient
V4 primitive used for Hessian
Hessian split operation
bordered determinant operation
channel determinant components
final additivity check
exact-ℚ equality checks
trace/provenance id
```

The result is `substrate_derived` only if the observable can be traced through these primitives. A mathematically correct formula pasted into the repo is still merely a named-equation fallback if the provenance chain is absent. That sounds pedantic; it is exactly the sort of pedantry that keeps this beast from eating its own tail.

---

## 12. Generalization to `n > 3`

For a hypersurface in `ℝⁿ`, the tangent shape operator has dimension `(n−1)×(n−1)`:

```text
Ŝ = Ŝ_c + Ŝ_s
```

By multilinearity of determinant in the columns:

```text
K = det(Ŝ_c + Ŝ_s)
  = Σ_{k=0}^{n−1} D_k
```

where `D_k` is the sum of determinants obtained by choosing `k` columns from `Ŝ_c` and the remaining `n−1−k` columns from `Ŝ_s`.

Thus:

```text
D_{n−1} = κ_c       pure coupling
D_0     = κ_s       pure self
0<k<n−1 = interaction channels
```

For `n=4`, there are four terms:

```text
(3,0) κ_c
(2,1) interaction
(1,2) interaction
(0,3) κ_s
```

The general mixed-discriminant form is:

```text
D_(p,q) = C(n−1,p) · Δ(Ŝ_c repeated p times, Ŝ_s repeated q times)
p + q = n−1
```

where `Δ` is the symmetric mixed discriminant normalized by `Δ(M,…,M)=det(M)`.

### Generalization discipline

For `n=3`, there is one interaction channel, so `κ_int` is unambiguous.

For `n>3`, there are multiple interaction orders. Do not collapse them prematurely. The honest generalization is:

```text
K = κ_c + κ_s + Σ interaction_(p,q)
```

Only after the separated interaction orders pass exact gates may a convenience aggregate be exposed.

---

## 13. Documentation updates this spec enables

Once the eval-tier gate passes, records can be updated with this sharper language:

```text
The geometry arm HR138 is validated as a κ_c / holonomy special case.
The full signed K_G object is the three-channel exact-ℚ decomposition:
K_G = κ_c + κ_s + κ_int.
The keystone surface proves the interaction channel is not optional:
κ_c = −1/49, κ_s = +1/49, κ_int = −3/49, K_G = −3/49.
The old non-negative scalar cannot represent the object and remains a retired/confessed fallback.
```

Avoid:

```text
"holonomy is the curvature"
"the scalar curvature bridge is the full three-channel K_G"
"the geometry-side spine is unfenced"
"the channel split is intrinsic"
```

Prefer:

```text
"holonomy validates the κ_c channel"
"the three-channel gate validates the full signed object"
"the channel split is basis-relative and diagnostically intentional"
"promotion remains fenced until exact-ℚ retrodiction and provenance pass"
```

---

## 14. Minimal exact-ℚ reference implementation

```python
from fractions import Fraction as Q


def kg_three_channel_from_gH(g, H):
    """Exact three-channel signed Gaussian curvature for n=3.

    Parameters
    ----------
    g:
        Length-3 iterable of Fractions, the gradient ∇F(p).
    H:
        3x3 symmetric matrix of Fractions, the Hessian Hess F(p).

    Returns
    -------
    dict with exact Fraction fields:
        K_G, kappa_c, kappa_s, kappa_int,
        delta_c, delta_s, delta_m, bordered_det, q.
    """
    g1, g2, g3 = map(Q, g)

    H11 = Q(H[0][0]); H22 = Q(H[1][1]); H33 = Q(H[2][2])
    H12 = Q(H[0][1]); H13 = Q(H[0][2]); H23 = Q(H[1][2])

    q = g1*g1 + g2*g2 + g3*g3
    if q == 0:
        raise ValueError("singular stratum: gradient is zero, K_G undefined")

    den = q*q

    delta_c = (
        g1*g1*H23*H23 + g2*g2*H13*H13 + g3*g3*H12*H12
        - 2*g1*g2*H13*H23
        - 2*g1*g3*H12*H23
        - 2*g2*g3*H12*H13
    )

    delta_s = -(
        g1*g1*H22*H33
        + g2*g2*H11*H33
        + g3*g3*H11*H22
    )

    delta_m = 2*(
        g1*g2*H12*H33
        + g1*g3*H13*H22
        + g2*g3*H11*H23
    )

    kappa_c = -delta_c / den
    kappa_s = -delta_s / den
    kappa_int = -delta_m / den
    K_G = kappa_c + kappa_s + kappa_int

    bordered_det = delta_c + delta_s + delta_m
    assert K_G == -bordered_det / den

    return {
        "K_G": K_G,
        "kappa_c": kappa_c,
        "kappa_s": kappa_s,
        "kappa_int": kappa_int,
        "delta_c": delta_c,
        "delta_s": delta_s,
        "delta_m": delta_m,
        "bordered_det": bordered_det,
        "q": q,
    }
```

---

## 15. Exact retrodiction probe

```python
from fractions import Fraction as Q

Z = [[Q(0),Q(0),Q(0)], [Q(0),Q(0),Q(0)], [Q(0),Q(0),Q(0)]]
TRI = [[Q(0),Q(1),Q(1)], [Q(1),Q(0),Q(1)], [Q(1),Q(1),Q(0)]]

KEYSTONES = {
    "plane": (
        [Q(1),Q(1),Q(1)], Z,
        (Q(0), Q(0), Q(0), Q(0)),
    ),
    "open_chain": (
        [Q(1),Q(2),Q(1)],
        [[Q(0),Q(1),Q(0)], [Q(1),Q(0),Q(1)], [Q(0),Q(1),Q(0)]],
        (Q(0), Q(0), Q(0), Q(0)),
    ),
    "closed_triangle": (
        [Q(2),Q(2),Q(2)], TRI,
        (Q(1,12), Q(1,12), Q(0), Q(0)),
    ),
    "multilinear": (
        [Q(1),Q(1),Q(1)], TRI,
        (Q(1,3), Q(1,3), Q(0), Q(0)),
    ),
    "paraboloid": (
        [Q(-2),Q(-2),Q(1)],
        [[Q(-2),Q(0),Q(0)], [Q(0),Q(-2),Q(0)], [Q(0),Q(0),Q(0)]],
        (Q(4,81), Q(0), Q(4,81), Q(0)),
    ),
    "sphere_rational_point": (
        [Q(6,5),Q(8,5),Q(0)],
        [[Q(2),Q(0),Q(0)], [Q(0),Q(2),Q(0)], [Q(0),Q(0),Q(2)]],
        (Q(1), Q(0), Q(1), Q(0)),
    ),
    "saddle": (
        [Q(-1),Q(-1),Q(1)],
        [[Q(0),Q(-1),Q(0)], [Q(-1),Q(0),Q(0)], [Q(0),Q(0),Q(0)]],
        (Q(-1,9), Q(-1,9), Q(0), Q(0)),
    ),
    "mixed_keystone": (
        [Q(3),Q(1),Q(2)],
        [[Q(2),Q(1),Q(0)], [Q(1),Q(0),Q(0)], [Q(0),Q(0),Q(2)]],
        (Q(-3,49), Q(-1,49), Q(1,49), Q(-3,49)),
    ),
    "cone_developable": (
        [Q(6),Q(8),Q(-10)],
        [[Q(2),Q(0),Q(0)], [Q(0),Q(2),Q(0)], [Q(0),Q(0),Q(-2)]],
        (Q(0), Q(0), Q(0), Q(0)),
    ),
}


def retrodiction_gate():
    failures = []
    for name, (g, H, expected) in KEYSTONES.items():
        out = kg_three_channel_from_gH(g, H)
        got = (out["K_G"], out["kappa_c"], out["kappa_s"], out["kappa_int"])
        if got != expected:
            failures.append((name, got, expected))
        if out["K_G"] != out["kappa_c"] + out["kappa_s"] + out["kappa_int"]:
            failures.append((name, "additivity failed", None))
        if out["K_G"] != -out["bordered_det"] / (out["q"] * out["q"]):
            failures.append((name, "bordered determinant failed", None))

    if failures:
        message = "three-channel K_G retrodiction gate failed:\n"
        message += "\n".join(f"{name}: got {got}, expected {expected}" for name, got, expected in failures)
        raise AssertionError(message)

    return True
```

---

## 16. Promotion checklist

The geometry-side fence can only be reconsidered after all are true:

```text
[ ] Exact monomial n=3 implementation exists in eval tier.
[ ] Gradient/Hessian are produced by typed primitives, not hand-supplied in the native path.
[ ] Retrodiction gate passes exactly in ℚ.
[ ] Independent bordered-Hessian determinant cross-check passes.
[ ] Shape-operator closed forms match monomial forms on randomized exact rational cases.
[ ] Negative tests fail the known bad substitutes.
[ ] Singular strata refuse loudly.
[ ] Basis-dependence caveat is present in docs.
[ ] HR138 is relabelled as κ_c-special-case evidence.
[ ] Theorem 8.1 is not frozen until the full three-channel gate passes.
[ ] Substrate promotion is separately signed off.
```

The shorter strategic sentence:

```text
The native geometry object is not a scalar upgrade; it is a provenance-bearing, signed, exact-ℚ, three-channel observable whose keystone proof is the −3/49 interaction regime.
```

---

## 17. Final concise claim

The strongest defensible claim after this spec is:

> The missing geometry-side native is now specified: signed Gaussian curvature decomposes exactly as `K_G = κ_c + κ_s + κ_int`, where the three channels are the exhaustive monomial partition of the bordered-Hessian determinant relative to the privileged variable basis. The keystone surface proves the interaction channel is essential: pure coupling and pure self cancel, leaving `κ_int = K_G = −3/49`. Therefore the former non-negative scalar is not merely incomplete; it is structurally incapable of representing the object. The path forward is an eval-tier exact-ℚ build with typed-gradient/Hessian provenance, hard retrodiction gates, and only then fenced substrate-promotion review.
