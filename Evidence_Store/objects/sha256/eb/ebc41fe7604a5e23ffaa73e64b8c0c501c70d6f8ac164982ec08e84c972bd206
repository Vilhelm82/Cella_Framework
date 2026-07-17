# Report — DBP 2-Primary Involution Campaign

**Benches:** PAIR-SPLIT · Sym/Wedge Boundary · The Alternating Half Hunt
**Workstream:** `evals/dbp_involution/` → `results/dbp_involution/`
**Records:** 102 graded claims, **all `COMPUTER_VERIFIED`**, two runs content-byte-stable.
**Arithmetic:** exact throughout (sympy `Rational`/`ZZ` SNF, explicit mod-p Gaussian
elimination, integer permutation groups). No float reaches any graded verdict.

---

## 1. Executive verdict

> **`THESIS_CONFIRMED_LOCAL_ONLY`.**

The second-order DBP role-coupling carrier **is** the symmetric half of `std⊗std`
(`Im(L) ≅ Sym²(std) = triv⊕std⊕S^(n-2,2)`, proved n=3..8 by two independent routes). Every
prime-2 phenomenon the thesis names is reproduced and is exactly 2-primary:

- the integral `Sym²/∧²` split fails only at 2, with cokernel `(ℤ/2)^{C(n,2)}` and **no odd
  torsion** (n=3..8); the canonical integral carrier is `Sym²(ℤⁿ)/Im(gauge) = ℤ^{C(n,2)} ⊕ ℤ/2`,
  a **single, uniform** phantom `ℤ/2` (no n=4 spike);
- the char-2 phantom `g gᵀ` generalizes: `ker(channel mod 2) = gauge_mod2 ⊕ ⟨g gᵀ⟩` for n=3..7
  (linear channel core), the phantom restoring the dimension the diagonal-blind gauge loses;
- Campaign H's `O`-parity is a **compatible** 2-primary parity (density degree-parity), **not**
  the tensor-swap involution `τ` (which acts as `+I` on the symmetric carrier).

The one criterion for **strong** confirmation that fails is item 5: the alternating half
`∧²(std)` is **not** carried by the current monodromy construction via any *canonical*
comparison map. Alternating/sign structure exists on the monodromy side, but the bridge to it
is not a projection of existing data — it needs a new, role-canonical object. Hence the
local thesis is confirmed; the local↔global half remains open, exactly as the thesis sentence
itself describes it.

---

## 2. Stage-by-stage table

| Stage | Bench question | Verdict | Records |
|---|---|---|---|
| **0** | reproduce banked role-pair theorem, loss law, faithfulness margin | **ALL GATES PASS** | 22 ✓ |
| **A** | does the local carrier equal the symmetric half? | **carrier_is_symmetric_half** | 19 ✓ |
| **B** | is `O`-parity the tensor-swap parity? | **O_parity_not_tau** | 4 ✓ |
| **C** | is integral torsion exactly 2-primary, and where? | **integral_split_confirmed** | 19 ✓ |
| **D** | does the char-2 phantom generalize to all n? | **char2_phantom_generalizes** | 29 ✓ |
| **E** | does monodromy carry the alternating half? | **no_canonical_comparison_map** | 9 ✓ |

No stage produced a REFUTED or a forced pass. Stages B and E (the high-risk, non-assumed
tests) returned the weaker-but-clean outcomes, recorded exactly.

---

## 3. Exact reproduction of the banked gates (Stage 0)

Each character was computed three independent ways and required to agree: the **engine**
(trace of explicit conjugation matrices on `Sym²(ℝⁿ)` minus the kernel), the **elementary**
count `C(fix,2)+#2cycles`, and the **referee** `½(χ_std² + χ_std∘sq)` from Murnaghan–Nakayama.

- **P0.1** `rank L = C(n,2)` and `χ_Im(L) = χ_pair`, **n=3..8** — engine = elementary = referee,
  `Im(L)` decomposing as `triv ⊕ std ⊕ S^(n-2,2)`. (STOP gate; passed.)
- **P0.2** loss `= S^(n-2,2)`, `dim = n(n-3)/2 = 0, 2, 5, 9, 14, 20` for n=3..8. n=4 corroboration:
  the S₄ permutation rep on the three 2+2 partitions has character `(3,1,3,0,1) = triv ⊕ S^(2,2)`,
  confirming `S^(2,2)` is the standard rep of `S₄/V₄`.
- **P0.3** faithfulness margin `:= dim − max_{g≠e} χ_shape(g)`, **n=4..12**: kernel `V₄`
  (order 4) with **margin 0** at n=4; trivial kernel with **margin `2(n-3)`** = 4,6,8,10,…,18 for
  n≥5; least-faithful element a transposition for n≥7 (`χ_shape = (n-3)(n-4)/2`). (STOP gate; passed.)

The referee `rep_utils.py` is independently unit-tested: known S_3/S_4 Specht characters, hook-length
dimensions, and full character orthonormality for S_3..S_7.

---

## 4. Does the local carrier equal the symmetric half? — **YES** (Stage A)

`std⊗std = Sym²(std) ⊕ ∧²(std)` with `P_± = (1±τ)/2` (verified `P_±²=P_±`, `P_+P_-=0`,
`P_++P_-=I`, `τ²=I`; `rank P_+ = C(n,2)`, `rank P_- = C(n-1,2)`). Characters from projector
traces match the referee: `Sym²(std)=triv⊕std⊕S^(n-2,2)`, `∧²(std)=S^(n-2,1,1)`, and
`∧²(std_4)=S^(2,1,1)=std⊗sign`.

**P-A3** (the pillar): two independent confirmations, n=3..8.
- *Assumption-free (Schur):* multiplicity of `∧²(std)` in `Im(L)` is **0**; `Im(L)` is entirely
  `Sym²` content. Since `Im(L)` and `∧²(std)` share no irreducible constituent, every equivariant
  map `Im(L) → ∧²(std)` is zero.
- *Explicit projector:* the map `q⊗q : Sym²(ℝⁿ) → std⊗std` sends the **gauge to 0** (so it
  descends to a carrier `≅ Sym²(std)` iso), has rank `C(n,2)`, and is annihilated by `P_-` /
  fixed by `P_+`. The carrier inherits `τ=+1` from Hessian symmetry.

→ **Local DBP coupling lives in the symmetric half.** Thesis claim (1) confirmed.

---

## 5. Is Campaign H's `O`-parity the tensor-swap parity? — **NO** (Stage B)

Regression reproduced (Campaign H engine): `r=1` density **odd**, `r=2` density **even** under
`O ↦ −O`, all three roles. The O-space `Sym_3/Im(G_g) ≅ ℚ³` was lifted explicitly into
`std_3⊗std_3` (matrix `ι`, rank 3, landing in `im P_+ = Sym²(std_3)`).

The induced swap action is `**τ_O = +I**` (not `−I`): `τ` acts trivially on the symmetric
carrier where `O` lives. The densities therefore satisfy `D_r(τ_O·O)=D_r(O)` for all r, which does
**not** reproduce the `(−1)^r` density pattern that `O ↦ −O` produces. So:

> `B_VERDICT = O_parity_not_tau`.

The `O ↦ −O` parity is a **separate, compatible 2-primary parity** — the degree-parity of the
densities (odd r=1 / even r=2) — not the tensor-swap involution. The genuine `τ=−1` half is
`∧²(std_3)=sign`, which the carrier `O` (an `S_3`-module `triv⊕std`) never touches. This is the
weak form of the thesis: weakened, not killed, and it is the same distinction the parallel
campaign's T3 note flags — reached here independently.

---

## 6. Is integral torsion exactly 2-primary, and where does it localize? — **YES, 2-primary** (Stage C)

| Object | Integral cokernel | n=3..8 |
|---|---|---|
| `std⊗std → Sym²(std)⊕∧²(std)` split (P-C1) | `(ℤ/2)^{C(n,2)}` (2-adic exp 3,6,10,15,21,28) | no odd torsion |
| pairwise `(s,a)` seam (P-C2) | exactly `ℤ/2` per unordered pair (`[[1,1],[1,-1]]→[1,2]`) | ✓ |
| **gauge** `Sym²(ℤⁿ)/Im(G_g)` (P-C3, canonical carrier) | `ℤ^{C(n,2)} ⊕ ℤ/2` — **single uniform phantom** | no n=4 spike |
| `ggᵀ` over ℤ | `ggᵀ ∉ Im`, but `2·ggᵀ = G_g(g) ∈ Im` | ✓ |
| coupling-numerator `L_flag` cokernel | **torsion-free** | ✓ |

**Answers to the four P-C3 questions.** (1) All torsion is 2-primary — no odd prime appears
anywhere. (2) It vanishes over `ℤ[1/2]` (every factor is a power of 2). (3) It localizes to the
splitting seam: the canonical carrier carries exactly the single phantom `ℤ/2 = [g gᵀ]`, and the
involution split itself carries one `ℤ/2` per pair. (4) **No** torsion generator projects to
`∧²(std)` — the role-pair carrier module contains no `S^(n-2,1,1)` constituent (multiplicity 0).

> `C_VERDICT = integral_split_confirmed`.

*Honesty note.* `L_flag` (the genuine integer coupling numerator) has a **torsion-free** cokernel;
the `(ℤ/2)^{C(n-1,2)}` cokernel of `L_int` is a presentation artifact of clearing the `½` in
`H_ij − ½H_ii − ½H_jj` and is reported as such, not as a fundamental finding. The canonical,
convention-independent statements are the gauge-quotient `ℤ/2` phantom and the split's
`(ℤ/2)^{C(n,2)}`. (These independently land on the same single-`ℤ/2` phantom the parallel
campaign's gauge GATE expects — computed by this workstream's own code, nothing lifted.)

---

## 7. Does the char-2 phantom generalize to all tested n? — **YES (linear core)** (Stage D)

- **P-D1** char ≠ 2 (`p=3,5,7`, n=3..7): `ker(channel mod p) = gauge` (dim n), `rank = C(n,2)`.
- **P-D2** char 2 (n=3..9): the gauge map `a ↦ G_g(a)` over `GF(2)` collapses to **rank n−1**,
  kernel `⟨g⟩`, and `g gᵀ ∉ gauge image` (its diagonal is unreachable by the diagonal-blind gauge).
- **P-D3** char 2 (n=3..7): `ker(channel mod 2) = gauge_mod2 ⊕ ⟨g gᵀ⟩` (dim n, `rank = C(n,2)`)
  — the phantom restores exactly the lost dimension. This is the all-n analog of CL-H10.
- **n=3 cross-check** against the Campaign H raw-RoleChSpec engine: the char-2 blind spot is
  exactly `grad_outer = g gᵀ`.

> `D_VERDICT = char2_phantom_generalizes`.

*Scope (flagged honestly).* The "channel map" here is the **linear** carrier (the r=1 channel
core whose linear recovery is the heart of RoleChSpec injectivity, Campaign H Lemma H4). The
**full nonlinear** RoleChSpec mod 2 is reproduced only at **n=3** (CL-H10). The all-n *nonlinear*
RoleChSpec faithfulness in char 2 remains **OPEN** (as CALC-16 already flagged). The phantom and
the `V₄` accident are distinct 2-phenomena here too: the phantom is the **uniform** lattice `ℤ/2`
(Stage C), present identically at every n including n=4, whereas `V₄` is the n=4-only representation
accident (Stage 0 margin dip).

---

## 8. Does the alternating half appear in monodromy/transport? — **structure yes, canonical bridge no** (Stage E)

Monodromy groups reconstructed exactly as permutation groups and verified against the banked
self-glue numbers:

| Cover | Group | order | abelianization | blocks |
|---|---|---|---|---|
| product `mP=2` | `Sym(2)≀Sym(2) = D4` | 8 | `(ℤ/2)²` | `{0,1},{2,3}` |
| directive `mD=2` | `D4` | 8 | `(ℤ/2)²` | — |
| directive `mD=3` | `Sym(3)≀Sym(3)` | 1296 | `(ℤ/2)²` | block kernel 216, block action `S3` |

Sheet-pair modules `Q[Ω]`, `Sym²(Q[Ω])`, `∧²(Q[Ω])` were built and their characters computed
exactly. Findings (every cover): **0** `G`-invariants in the alternating sheet-pairs, but the
**block-action sign character appears with multiplicity 1** in the alternating sheet-pairs — so
alternating/sign structure genuinely lives on the monodromy side (consistent with the `(ℤ/2)²`
abelianizations).

The role side: `∧²(std_3) = sign_{S₃}` (dim 1), **not** the standard rep — the campaign's warning
is heeded and verified by character projection. The candidate bridge is the block-action quotient
`G → S₃`, under which `sign` pulls back to a sign character of `G` that *is* present in the
alternating sheet-pairs. **But** the 3 blocks are root-sheets of the stage-2 trinomial, **not** the
3 roles: there is no role-canonical bijection roles ↔ sheets (CALC-10's standing conclusion).

> `E_VERDICT = no_canonical_comparison_map` — the alternating half is not absent, but the bridge to
> it requires a new (role-canonical) cover, not a projection of existing monodromy data.

---

## 9. Final classification and the strong-confirmation checklist

| # | Strong-confirmation criterion | Status |
|---|---|---|
| 1 | `Im(L)` is the symmetric half of `std⊗std` | **MET** (Stage A) |
| 2 | `O`-parity is `τ`-parity **or** a compatible 2-primary obstruction-sign parity | **MET** (compatible parity, Stage B) |
| 3 | integral torsion is 2-primary, localized to the `Sym/∧` split failure | **MET** (Stage C) |
| 4 | char-2 phantom generalizes: `ker = gauge ⊕ ⟨g gᵀ⟩` for all tested n | **MET for the linear core**; nonlinear all-n OPEN |
| 5 | a monodromy/transport carrier for `∧²(std)` with an equivariant comparison map | **NOT MET** (no canonical map) |

Item 5 fails (and item 4 is met only at the linear-core / n=3-nonlinear level), so per the
campaign rule the classification is:

> ## `THESIS_CONFIRMED_LOCAL_ONLY`

### The final sentence, adjudicated

> *"The second-order DBP role-coupling carrier is the symmetric half of `std⊗std`; the repeated
> prime-2 phenomena are the cost of separating this magnitude-like symmetric data from its
> alternating/oriented companion, and the unresolved local-global problem is whether monodromy
> carries that alternating half."*

- "carrier is the symmetric half" — **CONFIRMED** (Stage A).
- "prime-2 phenomena = cost of separating symmetric from alternating" — **CONFIRMED**: the integral
  split fails exactly at 2 (`(ℤ/2)^{C(n,2)}`, no odd torsion), the carrier quotient carries one
  phantom `ℤ/2`, the char-2 gauge goes diagonal-blind and is repaired by `g gᵀ`, and the `O`-parity
  is a compatible 2-primary parity.
- "unresolved local-global problem … whether monodromy carries the alternating half" — the sentence
  is **accurate**: monodromy carries alternating *structure* but no role-canonical identification of
  `∧²(std)`; the problem is genuinely **OPEN**.

The sentence is therefore confirmed in all its local assertions and correct in calling the
local↔global question unresolved.

---

## 10. Stop rule

Per the brief, work stops after Stage F. No new theorem campaign is opened, no papers are
rewritten, and no terminology is adopted permanently. Notable banked open threads for Will's
review (not pursued here):

1. **All-n nonlinear RoleChSpec faithfulness in char 2** (the full CL-H10 analog beyond the linear
   core; OPEN, = CALC-16).
2. **A role-canonical four-role branched cover** whose sheets *are* role-indexed — the candidate new
   object that could turn `no_canonical_comparison_map` into a genuine local↔global bridge for
   `∧²(std)`.

*Nothing here is canonical until Will signs off.*
