# REALFIBER THEOREM — connectivity of the rank-2 zero-diagonal isospectral family
**Date:** 2026-07-02 · **Status:** PROPOSED (grounding gate pending) · **Certificate:** `realfiber_fullfiber_cert.py`, ALL_PASS ×2, records sha `dfde6fbde06ee160` · **Ancestry:** wave-1 row 2 (sweep `4d2539a1`; Probe-1 `7b3b4305`; Probe-2 `848b8d8e`; pair-path `99fd1859`). Prior-art posture: **SWEEP EXECUTED S-2026-07-02** (`REALFIBER_CROWN_SWEEP.md`) — structure law (i) RECLASSIFIED KNOWN-adjacent (mr₀ literature, Grood et al.; cite, never claim); (ii)–(iv) apparently unrecorded, elementary-once-seen; claim language bound to the sweep's crown verdict. Ladder: L8-adjacent (field-positioned, boundaries known).

## Frozen statement
```
THEOREM. Fix a > 0, m ≥ 2, and let
   F(m,a) = { W ∈ Sym_m(ℝ) : spec(W) = (a, 0^{m−2}, −a), diag(W) = 0 }.
(Note: by trace, EVERY rank-2 zero-diagonal real symmetric matrix has spectrum of this form,
so F(m,a) sweeps the entire rank-2 zero-diagonal isospectral landscape.)

(i)   STRUCTURE LAW. Every W ∈ F(m,a) is W = a(uuᵀ − vvᵀ) with u ⊥ v unit vectors and
      |u_i| = |v_i| =: c_i for all i. Writing u_i = ε_i c_i, v_i = δ_i c_i, s = εδ on the
      active set A = {c_i > 0}: W_ij = a c_i c_j (ε_iε_j − δ_iδ_j), which vanishes iff
      s_i s_j = +1. Hence supp(W) is BIPARTITE between the s-classes, both classes are
      nonempty, and each carries weight exactly 1/2: Σ_{A₊} c² = Σ_{A₋} c² = 1/2.
(ii)  m = 2: F(2,a) = { ±a·(e₁e₂ᵀ + e₂e₁ᵀ) } — exactly two points; DISCONNECTED.
(iii) m ≥ 3: F(m,a) is PATH-CONNECTED. Canonical form: every point connects to the
      single-edge matrix a(e₁e₂ᵀ + e₂e₁ᵀ).
(iv)  LOCKING. For active i, j the product s_i s_j = sign(u_i v_i u_j v_j) is gauge-invariant,
      continuous, and nonvanishing, hence locally constant along fiber paths: relative class
      membership cannot change while both vertices remain active. Any partition change
      crosses {c_i = 0}.
```

## Proof obligations and their discharge
**O1 (structure law).** The eigenvalues a and −a are simple, so unit eigenvectors u, v are unique up to sign, mutually orthogonal (symmetric matrix, distinct eigenvalues), and the spectral decomposition is `W = a·uuᵀ + 0·(kernel part) − a·vvᵀ`. `diag(W)_i = a(u_i² − v_i²) = 0 ⟺ |u_i| = |v_i|`. The entry formula and the same-class vanishing are the certified identities [sha `dfde6fbd`, O1a–O1e]. Both classes nonempty: if s ≡ +1 on A then `u·v = Σ s_i c_i² = Σ c_i² = 1 ≠ 0`, contradiction; the balanced weights follow from `u·v = 0` and `‖u‖ = 1`. **PROVEN (+CERTIFIED identities).**

**O2 (m = 2).** `charpoly([[0,w],[w,0]]) = λ² − w² = λ² − a² ⟺ w = ±a` [CERTIFIED]. A two-point space has two path components. **PROVEN/CERTIFIED.**

**O3 (cell connectivity).** Fix a node `N = (A, s, ε)`. Its cell is `{c ∈ ℝ^A_{>0} : Σ_{A₊}c² = Σ_{A₋}c² = 1/2}`. In `q = c²` coordinates this is an open convex set (positivity + two linear equations), hence path-connected; `c = √q` and `(u,v) ↦ W` are continuous. The same holds for the closed cell. **PROVEN.**

**O4 (move realization).** PARK i (legal iff `|class(i)| ≥ 2`): the segment `q_i(t) = (1−t)q_i`, with the released weight moved linearly onto another member of the same class, satisfies every constraint identically in t; by O1's identities each point lies in F, including the endpoint `c_i = 0`. REVIVE is the reverse segment, with `(s_i, ε_i)` freely chosen at revival: since `u_i(t) = ε_i c_i(t)` passes through 0, the path `(u(t), v(t))` — hence `W(t)` — is continuous across the sign redefinition. **PROVEN.**

**O5 (move-graph connectivity, m ≥ 3).** Nodes `(A, s, ε)` with `|A| ≥ 2`, both classes nonempty; edges = PARK/REVIVE as above. *Canonicalization algorithm:* target `N* = ({1,2}, s=(+,−), ε=(+,+))`. From any node: (1) *Unlock:* whenever a needed PARK is blocked by a singleton class, note `|A| = 2 < m` or a spare exists, and REVIVE an inactive vertex into that class — reviving is always legal, and m ≥ 3 guarantees a spare when both classes are singletons. (2) *Place:* revive 1 and 2 if inactive; migrate 1 into class + and 2 into class − by park-and-revive-with-new-class, using (1) to unlock; set `ε₁ = ε₂ = +` by park-and-revive-with-flipped-ε, again via (1). (3) *Strip:* park every other active vertex, class by class, each park legal because its class still holds 1 or 2 (final sizes 1|1 are reached by parking the *other* members). Every step is an edge, so every node connects to `N*`. **PROVEN for all m ≥ 3**; independently **CERTIFIED** by exhaustive components count = 1 at m = 3, 4, 5 (72 / 464 / 2640 nodes) [sha `dfde6fbd`].

**O6 (lift and composition).** Given `W, W' ∈ F`, choose spectral preimages; each lies in the closed cell of some node (assign inactive vertices no data; any gauge representative works since `Φ(−u,v) = Φ(u,−v) = Φ(u,v)`). Connect: within-closed-cell to an interior point (O3), along the O5 edge sequence realized by O4 segments, then within-cell to the target preimage. Push forward through the continuous Φ. **PROVEN.**

**O7 (locking).** As stated in (iv): `s_i s_j` is a continuous, nonvanishing, gauge-invariant function wherever both vertices are active, hence locally constant along paths. **PROVEN.** (This is the precise mechanism behind Probe-2's empirical floor: the flows lived in one closed cell family and measured its separation from the target orbit.)

∎

## Grading
| clause | level | support |
|---|---|---|
| (i) structure law | **PROVEN**, identities CERTIFIED ×2 | Level 6–7 |
| (ii) m=2 boundary | **PROVEN/CERTIFIED** | Level 7 |
| (iii) connectivity m≥3 | **PROVEN** (Level 6); combinatorial core CERTIFIED m=3,4,5 | Level 6, 7-adjacent |
| (iv) locking | **PROVEN** | Level 6 |

## Boundaries (scoped closeout — what this theorem is NOT)
Covers the **rank-2 spectral family only** — exactly the spectra `(a, 0^{m−2}, −a)`. It says nothing about general-spectrum real fibers, which remain **OPEN** (and rank ≥ 3 breaks the parametrization outright: `diag = 0` no longer reduces to a coordinate-wise modulus condition). The m=2 disconnection is kept in the statement deliberately: the family is not trivially connected, and the theorem knows its own edge. Instance: m=5, a=2 closes wave-1 row 2 **in full** — the whole fiber containing the cospectral pair is path-connected, and the pair-path of `99fd1859` is one explicit realization.

## Corollary worth a line
Every rank-2 zero-diagonal real symmetric matrix of norm-scale a connects, within its isospectral zero-diagonal fiber, to the single weighted edge `a(e₁e₂ᵀ + e₂e₁ᵀ)` (m ≥ 3): a normal form under fiber homotopy.

## Successor obligations
(1) EXECUTED — see `REALFIBER_CROWN_SWEEP.md`; re-sweep re-owed at any manuscript boundary. (2) Optional: exact algebraic value of the Probe-2 floor (the cell-separation infimum). (3) The general-spectrum question stays on the wave-1 board, now with a proven base case.
