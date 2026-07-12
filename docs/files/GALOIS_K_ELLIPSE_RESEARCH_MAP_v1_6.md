# Galois–k-Ellipse Horizon Program — Research Map

**Version:** v1.6
**Current as of:** 2026-07-10 (clean consolidation — changelog stack folded into git; present-tense state)
**Purpose:** Index and dashboard for the program. States what is true now and where the live fronts are. Proof detail lives in the log entries this map points to; provenance history lives in git, not here.

**Central physical family:**

```text
4M = sum_{i=1}^k sqrt(m^2 + N_i^2),      N_i = 4Q_i,      u = m^2.
```

---

## 1. The bridge in one statement

With `P = (m,0)`, `F_i = (0,N_i)`, `d(P,F_i) = sqrt(m^2 + N_i^2)`, the mass relation is the intersection of the planar `k`-ellipse `E_k(4M) = { sum_i sqrt(x^2+(y-N_i)^2) = 4M }` with the physical half-axis `y=0, x=m>=0`. The signed-radical mass norm is the axial restriction of the `k`-ellipse polynomial:

```text
p_k(x,y) = product_{eps in {+1,-1}^k} [4M - sum_i eps_i sqrt(x^2+(y-N_i)^2)],
p_k(m,0) = N_k(m^2).
```

This identification links black-hole thermodynamics to multifocal geometry, convex algebraic geometry, symmetric determinantal representations, hyperbolic polynomials, invariant theory, Galois theory, wall arrangements, and exact certified computation. The descent pathway and the convex/LMI pathway are both established end-to-end (see the register and the log entries).

---

## 2. What is established (current state)

**Degree law.** The axial mass norm has `deg_u N_k = 2^{k-1}` (odd `k`) or `2^{k-1} - (1/2)binom(k,k/2)` (even `k`). Generic irreducibility holds for every `k` with distinct nonzero `N_i^2`; specialized charge vectors still require per-instance witnesses.

**Four-charge Galois core.** `K = F(u)` has `[K:F] = 5` with `Gal(K^gal/F) = S_5`. The seed mass `u = m^2` is not radical over the observables `F`; the static entropy sum generates the same quintic field; individual horizon entropies are not radical functions of `F`.

**Reflection quotient / descent (R6, R7).** The signed-distance incidence curve `C` is the affine normalization of the axial curve `X`; the signed radicals descend, `w_i in K`, via the reflection-fixed field `F(m)^tau = F(m^2) = K`. The horizon deck transformation is the axial reflection `m -> -m`. Established under the standing hypotheses `N_i != 0`, `N_i^2 != N_j^2`.

**Field tower.** `K(m)` deg 10, `K(y)` deg 10, `K(m,y)` deg 20 with `Gal(K(m,y)/K) = V_4` — the ordered-horizon field. Either normalized horizon entropy alone generates it, pivoting on the universal area product `Ŝ_+ Ŝ_- = P`. The degree-20 crown is generic-transfer conditional on one certificate gate (see live fronts).

**Deck ramification (R18).** The horizon swap's finite fixed divisor is the signed axial-contact divisor `u = 0`; its all-plus physical-chamber component is the static BPS/extremal contact locus. (Finite part; infinite places unswept.)

**Total reality and spectral selection (R5).** On the strict physical chamber `4M > sum|N_i|`, which is exactly the definiteness region of the axial pencil: every mass-square root is real and strictly positive; the parity involution gives the singular-value factorization `N_k(u) = det(L_0) prod_j (1 - u σ_j(T)^2)`; each positive-imbalance sheet crosses once and transversely (saturation); the physical root is the unique least root with exact selection formula

```text
u_phys = λ_max(S)^{-2} = ||T||^{-2}      (first spectrahedral exit along the mass ray),
```

with strict coefficient-sign alternation, `k=4` global simplicity under `N_i^2 != N_j^2` alone, and closed-form sensitivity/condition numbers. The reality/positivity/selection mechanism is spectral (absorbable by definite-pencil theory); the horizon/BPS/thermodynamic meaning of the selection is the program's own content.

---

## 3. Live fronts (open, ripe)

| Front | What's open | Notes |
|---|---|---|
| **Closure monodromy** | The Galois group of the *closure* of the ordered-horizon field `K(m,y)` over `F` — the full symmetry of the whole tower. Floors are known (`S_5` base, `V_4` top); the glued group is not. | The program's headline open question. Run over the generic tower. Inputs: complex sub-balance loci (braid generators) + critical-sheet strata. |
| **Degree-20 crown certificate** | Record the good-specialization statement at point B and independently re-verify the square-class certificate (or supply one specialized degree-20 eliminant certificate). | Closing this releases the generic degree-20 crown and the ordered-horizon-field degree corollary. Small, self-contained. |
| **Total reality: implementation** | The selection *rule* is proved; the *certified* interval implementation (extremal generalized eigenvalue `Z v = λ L_0 v`, return `u_phys = λ^{-2}` with rational enclosure) is not built. Interlacing under parameter variation also open. | Named Cella consumer. |
| **Rotation** | Extend the entropy cover with angular momentum `J`. The definite-pencil machinery is cut for definite base points; rotation is indefinite — no off-the-shelf tool. | Where native re-derivation stops being optional. |
| **Higher-charge census** | `k=5` degree-16 norm: generic irreducibility established; the Galois group and one irreducible physical specialization are open. | Program-forming if the group is pinned. |
| **Discriminant strata** | Factor/stratify `Disc_u N_4` by mechanism. On the strict axial chamber only collision strata occur; critical-sheet strata are off-chamber/complex targets. | Feeds closure monodromy. |

---

## 4. Register (all research directions, current status)

| ID | Direction | Status |
|---|---|---|
| R1 | Axial `k`-ellipse identification | Established |
| R2 | Mass-norm degree formula | Established (imported + independently re-derived from the pencil) |
| R3 | Generic `S_5` at four charges | Established |
| R4 | BPS wall norm (16 signed factors at `m=0`) | Established |
| R5 | Total reality + spectral selection in the strict chamber | Established (package: chamber=definiteness, strict positivity, parity-block SVD, saturation, least-root selection formula, alternation, `k=4` global simplicity, sensitivity) |
| R6 | Incidence normalization (`C` = affine normalization of `X`) | Established |
| R7 | Generic radical descent `w_i in K` | Established |
| R8 | Degree-20 ordered-horizon field | Established at B; generic crown conditional on the certificate gate |
| R16 | Leading-coefficient law | Established |
| R17 | Physical-sheet isolation + collision classification | Established (physical sheet free of both discriminant mechanisms; saturation extends tangency-freeness to every crossing sheet on the strict axial chamber) |
| R18 | Deck ramification = signed axial-contact divisor | Established (finite part) |
| R19 | Ordered-horizon field generated by either horizon alone | Established; degree corollary conditional on the gate |
| R20 | Physical-root selection formula + sensitivity | Established |
| R9 | **Full closure monodromy group** | **Open — live front** |
| R10 | Five-charge degree-16 irreducibility | Generic half established; specialized instances open |
| R11 | Generic higher-`k` Galois groups | Open (generic fields established) |
| R12 | Wall/discriminant ramification | Open (two-mechanism decomposition recorded) |
| R13 | Rotating entropy obstruction | Open — live front |
| R14 | Weighted multifocal families | Exploratory |
| R15 | DBP curvature of cover divisors | Exploratory |

---

## 5. Guardrails (errors to not make)

```text
1. Temperature is not Galois-odd. Under the horizon swap tau(T_+) = T_- (mixed);
   the pure odd covariant is Theta = S*T.
2. The closure monodromy group is NOT known — degree 20 and V_4-over-K are
   certified; the glued group over F is open (R9).
3. Generic irreducibility/S_5 does NOT transfer to every specialization.
   Hilbert irreducibility is almost-all, not all; rational instances need
   per-point certification. Only "five positive real roots with multiplicity"
   is automatic on the strict chamber.
4. Not every algebraic signed wall is a physical decay wall.
5. Only the all-plus component of u = 0 is the physical extremal locus; the
   rest is shadow-sector axial contact.
6. Signed sub-balance varieties give only the sheet-collision components of
   Disc_u N_k; critical-sheet components are a separate mechanism, void on the
   strict axial chamber but live off-chamber/complex.
7. Total reality/positivity/selection are STRICT-CHAMBER, AXIAL statements —
   not for arbitrary planar line restrictions, off the closed chamber, or at
   the degenerate origin.
8. The sector first laws / Smarr pair / negative inner temperatures are
   imported (CGLP 2018); the derivation-from-grading is the contribution.
9. Rotation/gauging/extra moduli do NOT preserve the k-ellipse form without
   derivation.
```

---

## 6. Standing process rules

Rules are a safety net, not a ladder: they constrain what may be **concluded**, never what to **investigate**. Sequencing follows the mathematics — what's ripe, what's blocked, where the proof energy is — never a promotion gate. A gate may veto a conclusion; it may never nominate the next target.

```text
Triage before strike     : no result is struck without a recorded salvage
                           attempt (narrow -> repair -> re-role). Demotion-
                           with-retention is not a strike.
Read before cite         : banked material is read from source, never
                           reconstructed from memory. External prior art is
                           quarantined OUT during native derivation; internal
                           banked corpus is mandatory-read IN.
Derive before sweep      : prior art enters as auditor, never architect.
                           Derive from program primitives first; sweep after,
                           grading convergence-as-validation vs divergence.
Scope ceilings           : every imported result carries a one-line ceiling
                           (what it licenses, where it stops). Native
                           re-derivation is mandatory when an import is load-
                           bearing for a novelty claim, ceiling-bound, or
                           defense-critical.
Two-register separation  : emergence-ledger verdicts strip novelty credit
                           only — never truth, establishment, or program use.
Spec-first containment   : freeze a full-facet spec (each facet consumer/gate/
                           falsifier-justified) before deriving; imports enter
                           as the realization of a facet, never as the frame
                           the spec is trimmed to fit.
Verification chain       : draft -> external audit -> counter-audit -> GO ->
                           promote. Nothing canonical without Will's GO.
Repo discipline          : nothing executes, commits, or deletes without GO;
                           path-scoped adds; one artifact, one commit; provenance
                           over purity (never erase, mark superseded).
```

---

## 7. Log entries (the proof archive this map points to)

Frozen, audited proof artifacts. The map states results; these prove them.

- **R5 — total reality, spectral factorization, physical-root selection** (`LOG_ENTRY_R5_total_reality_v2.md`) — promoted, audited + counter-audited.
- **R6/R7 — generic birationality and reflection descent** (`LOG_ENTRY_R6_R7_generic_descent_v2.md`) — promoted, audited + counter-audited.
- **RESEARCH_LOG Entry 4** — square-class run at point B; degree-20 `V_4` certification at B.

---

## 8. External anchors (with scope ceilings)

- Nie–Parrilo–Sturmfels, *Semidefinite Representation of the k-Ellipse* (arXiv:math/0702005). *Licenses:* planar degree law + definite symmetric determinantal representation. *Stops at:* indefinite/Lorentzian pencils (rotation); no thermodynamic semantics. Program pencil is the sign-conjugate (orthogonally equivalent) convention.
- Plaumann–Vinzant, *Determinantal Representations of Hyperbolic Plane Curves* (arXiv:1207.7047). *Licenses:* definite-representation ⇒ hyperbolicity direction. *Stops at:* selection semantics; the Helton–Vinnikov converse is nowhere used.
- Castillo–Dietmann, *On Hilbert's Irreducibility Theorem* (arXiv:1602.00314). *Licenses:* almost-all specialization transfer. *Stops at:* per-point certification (source for guardrail 3).
- Cvetič–Youm (hep-th/9603147) — seed family (mass relation, entropies).
- Cvetič–Gibbons–Lu–Pope (arXiv:1806.11134) — sector first laws, Smarr pair, negative inner temperatures (cite, don't claim).
- Cvetič–Gibbons–Pope (arXiv:1011.0008) — universal area product `Ŝ_+ Ŝ_- = P` (pivot of R19).
- Jiang–Han, *Singularities and Genus of the k-Ellipse* (arXiv:1908.01414) — contents unswept; sweep before load-bearing use.

---

## 9. Companion documents

- **Mathematical Object Emergence Ledger** (`MATHEMATICAL_OBJECT_EMERGENCE_LEDGER.md`) — tracks the one question "is the recurring cover–chamber–selection structure (CAND-001) a native mathematical object or absorbable into existing theory." Evidence, loss matrix, promotion gates, decision log. Currently: CAND-001 held at S2. This ledger records objecthood evidence only; it does not sequence program work.
