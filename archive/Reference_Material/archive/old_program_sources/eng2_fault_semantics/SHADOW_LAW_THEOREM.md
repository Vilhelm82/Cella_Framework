# THE TRIANGLE DECOMPOSITION AND SHADOW LAW OF THE COUPLING FORM
**Status: PROVEN (derivation below) + CERTIFIED (machine verification
`shadow_law_verify.py`, ×2 byte-stable — see records). GROUNDED — Will,
S-2026-07-05b: "file the HR-row-equivalent deltas" (dashboard row I.3b).
Authorized: "next fork: (a) General-n derivation". Scope: n ≥ 3; g ∈ ℚⁿ with all g_k ≠ 0; W-prod normalization
ν_ij = (∏_{k∉{i,j}} g_k)·H_ij; pair order lexicographic.**

## Setup
q = g·g, P = I − ggᵀ/q, M = H_c (symmetric, zero diagonal), pair module
coordinates h = (h_e)_{e={i,j}} with M_ij = h_e. The coupling form (PREREG_v2
DF-B2, certified successor of Strong-Spec §4 Δ_c):
```
Δ_c^(n)(h) := −q · e_2(P M P) ,   e_2(A) = (tr(A)² − tr(A²))/2
```

## Lemma 1 (channel form in closed form)
For symmetric M with tr(M) = 0 and P = I − ggᵀ/q idempotent:
```
tr(PMP)  = tr(MP)   = −gᵀMg/q
tr((PMP)²) = tr(MPMP) = tr(M²) − 2·gᵀM²g/q + (gᵀMg)²/q²
⟹  e_2(PMP) = gᵀM²g/q − tr(M²)/2
⟹  Δ_c^(n)(h) = q·Σ_e h_e² − |Mg|²
```
*Proof.* P² = P gives tr((PMP)²) = tr(MPMP); expand MP = M − (Mg)gᵀ/q and
take traces; tr(M²) = 2Σ_e h_e². The (gᵀMg)² terms cancel in e_2. ∎
*(Keystone check: q=14, h=(1,0,0), Mg=(1,3,0): 14·1 − 10 = 4 = Δ_c. ✓)*

## Lemma 2 (Gram form / entry table)
Let u_e := g_j·δ_i + g_i·δ_j ∈ ℚⁿ for e = {i,j}. Then Mg = Σ_e h_e·u_e, so
```
Δ_c^(n)(h) = q·|h|² − |Σ_e h_e u_e|²  ,   Q_raw = q·I − Gram(u_e)
Q_raw[e][e] = q − (g_i²+g_j²) = Σ_{k∉e} g_k²
Q_raw[e][f] = −⟨u_e,u_f⟩ = −g_j·g_k   if e={i,j}, f={i,k} share vertex i
Q_raw[e][f] = 0                        if e ∩ f = ∅
```
*Proof.* (Mg)_i = Σ_{j≠i} h_{ij} g_j is linear in h with coefficient
vectors u_e; the Gram entries are immediate. Disjoint pairs: u_e ⊥ u_f. ∎

## Lemma 3 (triangle decomposition — the master identity)
In ν-coordinates (Q_ν = D_W⁻¹ Q_raw D_W⁻¹, W_e = ∏_{k∉e} g_k), with
T_S := 1/∏_{m∉S} g_m² for each 3-subset S ⊆ [n]:
```
Q_ν[e][e] = Σ_{S ⊇ e, |S|=3} T_S
Q_ν[e][f] = −T_{e∪f}     if |e∪f| = 3   (sharing)
Q_ν[e][f] = 0            if e ∩ f = ∅
⟹   Q_ν = Σ_{|S|=3} T_S · (2I−J)_S
```
where (2I−J)_S is the matrix with 1 on the diagonal at the three pairs
inside S, −1 between distinct pairs inside S, and 0 elsewhere — i.e. the
n=3 keystone form planted on the triangle S.
*Proof.* Diagonal: Σ_{k∉e} g_k²/W_e² = Σ_{k∉e} 1/∏_{m∉e∪{k}} g_m² =
Σ_{S⊇e} T_S. Sharing (e={i,j}, f={i,k}, S=e∪f={i,j,k}): W_e·W_f =
g_j·g_k·(∏_{m∉S} g_m)², so −g_j g_k/(W_e W_f) = −T_S. Disjoint: 0 stays 0.
Summing T_S·(2I−J)_S reproduces exactly these entries. ∎
*(Sanity n=3: one S, T_S = empty product = 1, Q_ν = 2I−J = I.3a. ✓)*

## Lemma 4 (shadow of one triangle form)
The commutant of S_n on the pair module is the Johnson-scheme adjacency
algebra span{I, A₁, A₂}; the trace-orthogonal projection onto it (=
group-averaging) replaces entries by their orbit means. For any 3-subset S:
diagonal support 3 of N = C(n,2); sharing support 6 ordered of N·2(n−2);
disjoint support 0. Hence
```
shadow((2I−J)_S) = (3/N)·I − (3/(N(n−2)))·A₁ = (1/C(n,3))·[(n−2)I − A₁]
```
using 3/(N(n−2)) = 6/(n(n−1)(n−2)) = 1/C(n,3). ∎

## THEOREM (shadow law + scalar, all n ≥ 3)
```
shadow(Q_ν) = s(g)·[(n−2)·I − A₁] ,  s(g) = (Σ_{|S|=3} T_S)/C(n,3)
            = e_3(g²)/(C(n,3)·e_n(g²))
```
*Proof.* Linearity of shadow over Lemma 3, then Lemma 4; and
Σ_S T_S = Σ_S ∏_{m∈S} g_m²/e_n(g²) = e_3(g²)/e_n(g²). ∎
Spectrum of (n−2)I − A₁ on (triv, std, shape) = (−(n−2), 2, n) — the
direction certified at Stage B′; at n=3, s ≡ 1 and (n−2)I−A₁ = 2I−J: I.3a
is the n=3 member. The Stage-B′ certificates are instances of this theorem.

## Corollaries
1. **Residual structure (answers the "covariant completion"):**
   R = Q_ν − shadow(Q_ν) = Σ_S (T_S − T̄)·(2I−J)_S + [cross-orbit residue
   of the sharing/diagonal mismatch], concretely: the FULL form is the
   triangle sum; the shadow is its orbit mean; all g-anisotropy = the
   fluctuation of the triangle weights T_S about their mean. No further
   completion object is missing — the bridge is CLOSED by Lemma 3, not by
   an extra correction term.
2. **tt-block vanishing (measured 15/15 at B′):** shadow removal zeroes all
   three orbit means, hence 1ᵀR1 = 0 and diag-mean 0 ⟹ P_triv R P_triv = 0
   identically. PROVEN.
3. **n=4 block sparsity (measured):** at n=4 the weights T_S are indexed by
   3-subsets ↔ their complement vertices, a 4-dim permutation module
   (triv⊕std); fluctuations live in std of the label space — a selection
   rule consistent with the measured vanishing of shape-shape and
   triv↔shape blocks at n=4. [STRUCTURAL — stated as mechanism, exact
   selection-rule lemma not written out; at n≥5 the 3-subset module gains
   shape and all non-tt blocks activate, as measured.]
4. **CL-F5 in revised, stronger form:** the general-n bridge identity is
   `Δ_c^(n)(ν) = Σ_S T_S·Δ_c^(3)[S](ν|_S)` — the coupling channel is a
   g-weighted sum of keystone triangle channels; its isotypic (invariant)
   content is exactly s(g)·[(n−2)I − A₁]. The originally staked fixed-g
   three-moment expansion is false (Stage B, K-B1) BECAUSE the fluctuation
   term is generically nonzero — now proven, not just measured.

## Machine verification (CERTIFIED ×2)
`shadow_law_verify.py`: (V1) SYMBOLIC n=4: Q_ν == Σ_S T_S(2I−J)_S with
symbolic g (sympy, exact); (V2) exact-Fraction identity check at all 15
banked fixtures (n=4,5,6; Stage-B + B′ g's); (V3) shadow + scalar recomputed
from the decomposition and matched against the B′ certified values; (V4)
Lemma-1 closed form vs direct e_2 evaluation, symbolic n=4. Records ×2
byte-stable beside this file.

*Prior-art posture: Johnson-scheme algebra is classical (Delsarte/Bannai–
Ito). NOVELTY CANDIDATE (needs sweep before any external claim): the
triangle decomposition of the hypersurface coupling channel and the
resulting shadow law/scalar; nearest known territory = mixed discriminants
/ second elementary symmetric of projected operators. Nothing here is
canonical until Will signs.*
