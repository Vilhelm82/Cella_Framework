# Audit Report — R5 Total Reality and Mathematical-Object Emergence Ledger v0.2

**Audit date:** 2026-07-10  
**Primary draft audited:** `LOG_ENTRY_DRAFT_R5_total_reality.md`  
**Context baseline:** `MATHEMATICAL_OBJECT_EMERGENCE_LEDGER_v0_2.md`  
**Dependency inspected:** `LOG_ENTRY_DRAFT_R6_R7_generic_descent.md`  
**Audit mode:** mathematical proof review, literature cross-check, exact counterexample/sanity check, and ledger-impact review  
**Status of this report:** revision guide; it does not enact ledger changes

---

## 1. Executive verdict

The central mathematical result of R5 is sound:

> Throughout the strict physical chamber, the axial mass polynomial is real-rooted in `m`; after the even quotient `u = m^2`, every mass-square root is strictly positive; and the physical root is simple without genericity hypotheses.

The proof of Theorem R5(i)–(iv) passes. Clause (v) also passes in substance, conditional on the banked generic irreducibility and leading-coefficient inputs, but its discriminant bookkeeping and generic-versus-specialized wording should be repaired.

The draft as a whole is **not yet ready for unqualified promotion**, because four surrounding claims require correction:

1. The NPS pencil is a sign-conjugate version of the displayed NPS pencil, not literally the same sign convention.
2. Remark D incorrectly promotes a generic `S_5` result to every chamber specialization.
3. The proposed equal-charge verification witness does not have five simple roots.
4. The absorption section understates how much definite-pencil and spectrahedral theory already distinguishes, including the first positive boundary root.

The audit also found results stronger than the current R5 statement:

1. An exact parity-block/singular-value factorization of `N_k(u)`.
2. A sheet-saturation theorem: every positive-imbalance signed sheet crosses exactly once and simply; no other signed sheet crosses in the strict chamber.
3. The physical root is the **unique least** mass-square root.
4. The physical root has an exact generalized-eigenvalue/Rayleigh-quotient characterization.
5. For `k = 4`, (H2) gives simplicity of all five roots at **every** strict-chamber point, not merely generically.
6. The coefficients of `N_k`, in its determinant normalization, alternate strictly in sign throughout the strict chamber.

### Promotion ruling

```text
Core theorem R5(i)–(iv):       PASS
Generic-simplicity clause (v): PASS AFTER WORDING REPAIR
Draft as written:              REVISE
E-012 enactment:               GO AFTER REQUIRED REVISIONS
PRED-003:                      CONFIRM, strengthened to strict positivity
OBJ-004:                       COMPLETE after revision
THM-005 native-theorem count:  DO NOT RATIFY FROM R5 ALONE
CAND-001 stage:                HOLD AT S2
```

---

## 2. Context baseline adopted from the ledger

For subsequent work, the authoritative baseline is ledger **v0.2**, with the following state.

| Item | Current authoritative state |
|---|---|
| Candidate | `CAND-001`: cover–chamber descent system |
| Stage | `S2` — recurring structure / candidate object under test |
| Critical blockers | `NS-002` native morphisms is EMPTY; `G3-05` third independent realization is BLOCKED |
| Strongest banked evidence | E-008 through E-011: two discriminant mechanisms, physical-sheet isolation, ordered-horizon reconstruction, and ramification parity/signed-wall distinction |
| Candidate-native theorem state | THM-002 proved in founding realizations but native form remains a lead; THM-005 was only PROOF-READY |
| Current queue | OBJ-004, then OBJ-002/PRED-006, then OBJ-001 |
| Current decision | DEC-002: hold CAND-001 at S2 and use R5 as an absorption test |

The proposed §10 changes in the R5 draft are **pending candidates**, not part of the v0.2 baseline. This distinction should be maintained until the corrected R5 text passes the remaining audit/sign-off protocol.

### Context rule for later work

```text
Use ledger v0.2 as the last enacted state.
Treat R5/E-012/THM-005/OBJ-004 changes as pending until this report's
required revisions are applied and signed off.
Do not silently promote CAND-001 beyond S2.
```

---

## 3. Scope and verification basis

The audit separated four kinds of claims:

| Class | What was checked |
|---|---|
| Self-contained | Tensor-pencil spectrum, definiteness, real-rootedness, degree/rank, inertia, positivity, physical-root isolation, and the new spectral consequences |
| Imported literature | NPS degree/determinantal representation and the standard definite-pencil implication |
| Banked dependency | Generic irreducibility of `N_k` and the leading-coefficient law from the R6/R7 entry and its cited map |
| Specialization claim | Exact equal-charge `k=4` calculation and the distinction between generic and specialized Galois groups |

The relevant primary references are:

- Jiawang Nie, Pablo Parrilo, and Bernd Sturmfels, [Semidefinite Representation of the k-Ellipse](https://arxiv.org/abs/math/0702005).
- Daniel Plaumann and Cynthia Vinzant, [Determinantal Representations of Hyperbolic Plane Curves: An Elementary Approach](https://arxiv.org/abs/1207.7047), for the definite-representation/hyperbolicity direction and the Helton–Vinnikov converse distinction.
- Abel Castillo and Rainer Dietmann, [On Hilbert's Irreducibility Theorem](https://arxiv.org/abs/1602.00314), for the fact that preservation of a generic Galois group is an “almost all” specialization result, not an “every specialization” result.

This is a rigorous paper audit, not a proof-assistant formalization. Clause (v) remains conditional on the correctness and enacted status of the banked R6/R7 irreducibility and leading-coefficient results.

---

## 4. Theorem-by-theorem verification

### 4.1 Setup and physical root

**Verdict: PASS.**

For

```text
g(u) = sum_i sqrt(u + N_i^2),
Cham = {4M > sum_i |N_i|},
```

`g` is continuous and strictly increasing on `u >= 0`, with `g(0) < 4M` and `g(u) -> infinity`. Therefore there is exactly one `u_phys > 0` satisfying `g(u_phys) = 4M`. This remains valid with zero or repeated charges.

### 4.2 NPS tensor pencil

**Verdict: PASS, with citation/sign-convention repair.**

The draft's operators in different tensor slots commute, and each slot operator has eigenvalues

```text
±sqrt(x^2 + (y-N_i)^2).
```

Consequently the stated spectrum and determinant product follow directly. Along `y=0`,

```text
L(m,0) = L_0 - mZ,
L_0 = 4M I + sum_i N_i X_i,
Z = sum_i Z_i,
```

and `det(L_0-mZ)=Phi_k(m,M)=N_k(m^2)` with no normalization factor.

The only repair is bibliographic precision: the sign convention displayed by NPS is equivalent rather than character-for-character identical. Simultaneously changing the signs of the slot Pauli matrices is an orthogonal conjugation and leaves the determinant and positive-semidefinite region unchanged.

### 4.3 Lemma A — chamber equals definiteness locus

**Verdict: PASS exactly.**

The least eigenvalue of `L_0` is

```text
lambda_min(L_0) = 4M - sum_i |N_i|.
```

Hence

```text
L_0 > 0  iff  4M > sum_i |N_i|,
L_0 >= 0 iff  4M >= sum_i |N_i|.
```

This is a genuine exact bridge: the strict BPS chamber and the interior definiteness region coincide.

### 4.4 Lemma B — definite symmetric pencils

**Verdict: PASS exactly.**

With

```text
S = L_0^(-1/2) Z L_0^(-1/2),
```

one has

```text
det(L_0-mZ) = det(L_0) product_j (1-m mu_j),
```

where the `mu_j` are real. Rank, degree, reality, multiplicity, and inertia statements all follow. Congruence preserves both rank and inertia.

### 4.5 Theorem R5(i) and (ii)

**Verdict: PASS.**

The spectrum of `Z` is `sum_i eps_i`. Its zero eigenspace has dimension `binom(k,k/2)` for even `k` and dimension zero for odd `k`, giving exactly

```text
rank Z = D_k.
```

The deck/spin-flip conjugation proves evenness independently.

### 4.6 Theorem R5(iii) — strict positivity of every `u`-root

**Verdict: PASS.**

If `N_k(u_0)=0`, choose any complex `m_0` satisfying `m_0^2=u_0`. Then `q(m_0)=0`; real-rootedness of `q` forces `m_0` real and therefore `u_0 >= 0`. Since

```text
N_k(0)=det(L_0)>0,
```

zero is excluded. Thus every `u`-root is strictly positive.

The proof handles both square roots: once one chosen square root is a root of `q`, Lemma B forces that chosen value itself to be real.

### 4.7 Theorem R5(iv) — unconditional physical-root simplicity

**Verdict: PASS.**

At `u_phys`, every radical is strictly positive, including channels with `N_i=0`. Every shadow factor differs from the all-plus factor by a nonempty positive sum, so no shadow factor vanishes there. The derivative of the all-plus factor is

```text
-(1/2) sum_i 1/w_i(u_phys) < 0.
```

Therefore the physical root has multiplicity one without (H1) or (H2).

### 4.8 Theorem R5(v) — generic simplicity

**Verdict: PASS in substance; rewrite required.**

The banked generic irreducibility of `N_k` in characteristic zero implies generic separability and a nonzero generic resultant/discriminant. After clearing any parameter denominators, its zero locus is a proper real-algebraic subset. Off that set, all roots are simple.

Three wording repairs are needed:

1. For a degree-`n` polynomial `f`, write the exact identity

   ```text
   Disc(f) = (-1)^(n(n-1)/2) Res(f,f') / lc(f).
   ```

   The discriminant is itself polynomial in the coefficients; it need not be described as an unspecified rational function divided by `lc^(...)`.

2. The strict chamber alone implies `M>0`, because `4M > sum_i |N_i| >= 0`. H1 is not needed for this step.

3. Make explicit that generic irreducibility proves the **discriminant polynomial is nonzero**. It does not prove irreducibility, separability, or `S_5` at every real point satisfying H1/H2.

---

## 5. Required corrections before promotion

### R1. Repair the NPS attribution

Replace “the NPS construction specializes to” with language such as:

> We use the sign-conjugate NPS pencil. It is orthogonally equivalent to the sign convention displayed by NPS and therefore has the same determinant and spectrahedral region.

The draft's pencil itself is correct; only the exact attribution needs precision.

### R2. Replace Remark D's specialization claim

**Current claim:** every strict-chamber specialization of the generic `S_5` quintic is a totally real `S_5` field.

**Why it fails:** a generic function-field Galois group does not persist at every specialization. Specialization can become reducible, inseparable/repeated, or have a smaller Galois group.

**Suggested replacement:**

> Every strict-chamber specialization of `N_4` has five positive real roots counted with multiplicity. At any rational or algebraic chamber specialization for which `N_4` is additionally irreducible and retains Galois group `S_5`, the resulting quintic field is totally real. Generic `S_5` does not imply `S_5` at every chamber point; arithmetic specialization must be certified separately.

This distinction is required by Hilbert irreducibility, not merely stylistic caution.

### R3. Replace the equal-charge “five simple roots” witness

The optional witness

```text
(M,N_1,N_2,N_3,N_4) = (2,1,1,1,1)
```

lies in the strict chamber but violates H2. Exact grouping by the number of plus signs gives

```text
N_4(u) = 2^30 (3-u)(15-u)^4.
```

Therefore:

```text
u_phys = 3       simple,
u_shadow = 15    multiplicity four.
```

This is an excellent **degeneracy witness** and should be retained for that purpose. It cannot certify generic simplicity. For a distinct-charge test, use a chamber point such as `(M,N)=(3,1,2,3,4)` and certify its roots by an exact Sturm sequence or rational interval isolation. A floating-point check gives five separated positive roots, but that numerical observation is not an exact certificate.

### R4. Rewrite the absorption verdict

The sentence “hyperbolicity theory has no distinguished root” is too strong. Once a definite base point and an oriented ray are supplied, spectrahedral theory canonically distinguishes the first boundary exit:

```text
m_first = sup {m >= 0 : L_0-mZ >= 0}
        = 1/lambda_max(L_0^(-1/2) Z L_0^(-1/2)).
```

In this realization, `m_first=sqrt(u_phys)`. Thus the selection mechanism is visible in the pencil. What remains external is the **physical/BPS interpretation** of that ray, root, and wall, and its coupling to thermodynamic covariants and norm-wall semantics.

The honest absorption conclusion is therefore:

```text
Absorbed by equivariant definite-pencil theory:
  - bare total reality;
  - positivity after the even quotient;
  - multiplicity as spectral multiplicity;
  - first-exit / least-root selection.

Not supplied by that parent theory alone:
  - why this chamber and oriented ray are physically selected;
  - the horizon/thermodynamic meaning of the selected branch;
  - the BPS meaning of the relevant norm-wall component;
  - coupling to the wider cover/covariant/reconstruction package.
```

Do not count R5 by itself as a native theorem toward G4-02. It is a powerful bridge theorem and a strong realization theorem. A candidate-native theorem still needs an intrinsic formulation whose content survives after the full spectral mechanism is removed.

### R5. Qualify Remark B at zero-charge boundary strata

On `4M=sum_i|N_i|`, the physical root reaches `u=0`. If every `N_i` is nonzero, it is the only signed sheet doing so. If some `N_i=0`, flipping signs in those zero-charge channels creates shadow sheets at the same axial contact, so “only through the physical root” is false without a qualification.

Also exclude the degenerate origin `(M,N)=(0,0)` from any fixed-degree continuity statement; for even `k`, the determinant polynomial can collapse there because the leading coefficient vanishes.

Suggested replacement:

> On the nontrivial closed chamber (`M>0`), real-rootedness and nonnegativity pass to the boundary at fixed degree. The physical branch reaches `u=0`. If all charges are nonzero, it is the unique signed sheet at that contact; zero-charge channels permit additional shadow sheets to meet the same point.

### R6. Clarify Remark C's multiplicity language

“One per unbalanced sign-pair” should either say “counted with multiplicity” or be supported by the sheet-saturation theorem in §6.2 below. Equal charges show why the distinction matters: several sheets can produce the same `u`-value.

---

## 6. High-value additions proved by the audit

These are not speculative research suggestions. Each follows from the same pencil and signed-sheet structure already present in R5.

### 6.1 Parity-block and singular-value factorization

Let `X_all=sigma_x^(tensor k)`. Since

```text
X_all L_0 X_all = L_0,
X_all Z X_all   = -Z,
```

decompose the matrix space into the `+1` and `-1` eigenspaces of `X_all`. In compatible orthonormal bases,

```text
L_0 = [ A   0 ],       Z = [ 0    C  ],
      [ 0   B ]            [ C^T  0  ],
```

with `A>0` and `B>0`. Set

```text
T = A^(-1/2) C B^(-1/2).
```

Then

```text
rank C = D_k/2
```

and a block determinant gives

```text
N_k(u) = det(L_0) product_{j=1}^{D_k/2} (1-u sigma_j(T)^2),
```

where the product runs over the nonzero singular values of `T`, with multiplicity.

Consequences:

```text
Every root is u_j = sigma_j(T)^(-2).
Root multiplicity = singular-value multiplicity.
The degree D_k/2 is rank C.
Strict positivity is immediate.
```

This is the cleanest spectral form of R5 and should be added as a corollary after Remark A or Lemma B.

### 6.2 Sheet-saturation theorem

For a sign vector `eps`, define

```text
s_eps(u) = sum_i eps_i w_i(u),
a_eps    = sum_i eps_i.
```

At `u=0`, every sheet satisfies

```text
s_eps(0) <= sum_i |N_i| < 4M.
```

If `a_eps>0`, then

```text
s_eps(u) = a_eps sqrt(u) + O(u^(-1/2)) -> +infinity,
```

so that sheet has at least one positive crossing of `s_eps(u)=4M`.

The number of sign vectors with `a_eps>0` is exactly

```text
D_k/2 = deg_u N_k.
```

Each crossing contributes at least one to the total zero multiplicity of `N_k`. The positive-imbalance sheets already supply at least `D_k/2` crossings counted with multiplicity, which saturates the degree. Therefore:

> Every positive-imbalance signed sheet has exactly one positive crossing, that crossing is transverse, and sheets with zero or negative imbalance have no crossing in the strict chamber.

This has several strong consequences:

- The phrase “one per unbalanced sign-pair” becomes a theorem: choose the positive-imbalance representative of each pair.
- A single signed sheet cannot be tangent at its crossing.
- The critical-sheet condition `sum_i eps_i/w_i=0` cannot cause an axial discriminant point inside the strict chamber.
- Every multiple root inside the strict chamber is a collision of crossings from distinct positive-imbalance sheets.

This strengthens the R5 use of E-008/E-009: along the strict axial chamber, the critical-sheet mechanism is absent for **all** crossing sheets, not only for the physical sheet.

### 6.3 Physical root is the unique least root

Let `u` be the crossing of a shadow sheet and let `I_-={i:eps_i=-1}`. At that root,

```text
4M = s_eps(u)
    = g(u) - 2 sum_{i in I_-} w_i(u),
```

so

```text
g(u) = 4M + 2 sum_{i in I_-} w_i(u) > 4M = g(u_phys).
```

Since `g` is strictly increasing,

```text
u > u_phys.
```

Hence:

> `u_phys` is the unique least root of `N_k(u)` at every strict-chamber point.

This is substantially stronger than simplicity. It supplies an intrinsic selection rule within the axial realization and should be added to Theorem R5 or as its first corollary.

### 6.4 Exact generalized-eigenvalue and variational formula

Set

```text
S = L_0^(-1/2) Z L_0^(-1/2).
```

The positive `m`-roots are reciprocals of the positive eigenvalues of `S`. Since the physical root is the least positive root,

```text
m_phys = 1/lambda_max(S),
u_phys = 1/lambda_max(S)^2.
```

Equivalently,

```text
lambda_max(S)
  = max_{v != 0} (v^T Z v)/(v^T L_0 v),

u_phys
  = [max_{v != 0} (v^T Z v)/(v^T L_0 v)]^(-2).
```

This gives the exact certified-selection route requested in the R5 queue:

```text
Solve the largest positive generalized eigenvalue of Z v = lambda L_0 v;
then return u_phys = lambda^(-2).
```

What remains open is a formally certified implementation with rational interval bounds, not the mathematical selection rule.

### 6.5 Strict coefficient-sign alternation

From the singular-value factorization, if

```text
N_k(u) = c_0 + c_1 u + ... + c_n u^n,
n = D_k/2,
```

then throughout the strict chamber

```text
(-1)^r c_r > 0,   r=0,...,n.
```

In particular, the determinant normalization fixes a strict alternating coefficient pattern. This is a cheap exact falsification check for symbolic expansions and a new family of coefficient inequalities.

### 6.6 Strong `k=4` specialization theorem

For `k=4`, the five positive-imbalance sheets are

```text
(+,+,+,+)
```

and the four sheets with exactly one minus sign. By sheet saturation, each crosses exactly once and transversely.

Two one-minus sheets `i` and `j` cross at the same `u` only if

```text
w_i(u)=w_j(u),
```

equivalently

```text
N_i^2=N_j^2.
```

Therefore:

> For `k=4`, H2 alone implies that all five roots of `N_4` are simple at every strict-chamber point.

This is stronger than R5(v)'s generic simplicity. H1 is not needed for this `k=4` conclusion.

There is also a canonical ordering. If `|N_i|>|N_j|`, then `w_i(u)>w_j(u)` for every `u>=0`, so the `i`-minus sheet lies below the `j`-minus sheet and crosses later. Thus larger charge magnitude corresponds to the larger associated shadow root.

### 6.7 Physical-root sensitivity formulas

Implicit differentiation of

```text
sum_i sqrt(u_phys+N_i^2)=4M
```

gives

```text
partial u_phys / partial M
  = 8 / sum_i 1/w_i(u_phys) > 0,

partial u_phys / partial N_j
  = -2 N_j / [w_j(u_phys) sum_i 1/w_i(u_phys)].
```

Thus the selected mass-square root increases strictly with `M` and decreases as a fixed-sign charge magnitude increases. These formulas provide condition numbers for certified numerical continuation.

---

## 7. Recommended restructuring of the R5 paper

The strongest paper structure is now:

```text
Theorem R5a — Definite-pencil result
  chamber = definiteness;
  axial m-polynomial is real-rooted;
  degree and inertia.

Corollary R5b — Equivariant spectral quotient
  parity-block/singular-value factorization;
  all u-roots positive;
  alternating coefficient signs.

Theorem R5c — Signed-sheet saturation and physical selection
  one transverse crossing per positive-imbalance sheet;
  no other crossings;
  physical root is unique least root;
  generalized-eigenvalue/first-exit formula.

Corollary R5d — Four-channel global simplicity
  under H2, all five roots are simple everywhere in the strict chamber;
  charge magnitudes canonically order the four shadow roots.

Proposition R5e — Generic higher-k collision locus
  generic simplicity from the nonzero discriminant;
  every chamber multiple root is an inter-sheet collision;
  no critical-sheet tangency occurs on the strict axial slice.
```

This organization is mathematically clearer than placing the strongest consequences in remarks. It also makes the absorption boundary explicit: R5a and much of R5b are classical translated mathematics; R5c/R5d are the realization-specific synthesis and selection results.

### Required update to §9 (“What this entry does NOT prove”)

The draft currently says certified smallest-root/interlacing selection is still open. Replace that with:

> The entry proves the exact selection rule: `u_phys` is the unique least root and equals the inverse square of the largest generalized eigenvalue of `(Z,L_0)`. A formally certified numerical implementation and interval-error analysis remain open.

---

## 8. Audited ledger deltas

The following changes are recommended after the R5 revisions are applied and signed off.

| Ledger item | Recommended action | Audit reason |
|---|---|---|
| E-007 | Mark SUPERSEDED by E-012 | The proof route is complete |
| E-012 | Add as PROVED | Chamber/definiteness, total reality, positivity, spectral factorization, and physical-root selection are proved |
| E-013 | Add as PROVED | Sheet saturation: exactly one transverse crossing per positive-imbalance sheet; no critical-sheet tangency on the strict axial slice |
| PRED-003 | OPEN → CONFIRMED | Strengthen “nonnegative” to “strictly positive” |
| THM-005 | Split and downgrade native claim | Definite-pencil reality/positivity/first-exit are TRANSLATED; physical interpretation is a bridge and native generalization remains LEAD |
| NS-001 | Add founding-family realization note | The physical section is the first spectrahedral exit along the oriented mass ray in this family; do not assume this is intrinsic in all candidates |
| NS-007 / E-008 | Add chamber restriction | Critical-sheet mechanism exists generically in the broader discriminant geometry but is absent from strict-chamber axial crossings; chamber multiplicity is collision-only |
| OBJ-004 | Mark COMPLETE | Absorption verdict: stronger absorption than drafted |
| DEC-003 | Append a new decision | Enact corrected evidence; do not count R5 alone toward G4-02; hold CAND-001 at S2; proceed to OBJ-002/PRED-006 |

### Recommended THM-005 split

```text
THM-005a — Definite symmetric pencil over the strict chamber gives a
            real axial fiber; an anti-commuting parity involution gives a
            positive quotient fiber and a first-exit eigenvalue formula.
Status:     TRANSLATED / PROVED in the axial k-ellipse realization.
Native count: NO.

THM-005b — The physically selected branch is identified with the first
            spectrahedral exit and with the distinguished BPS wall
            component, compatibly with cover covariants and wall data.
Status:     CANDIDATE-NATIVE BRIDGE; PROVED in the founding realization,
            abstract candidate-language form remains LEAD.
Native count: NOT YET.
```

### Stage decision

R5 substantially strengthens the corpus, but it does not repair the two S2→S3 blockers:

```text
NS-002 native morphisms:              still EMPTY
G3-05 third independent realization: still BLOCKED
```

Therefore `CAND-001` remains at **S2**.

---

## 9. Revision checklist

### Must fix

- [ ] Label the displayed pencil as sign-conjugate/equivalent to the NPS convention.
- [ ] Replace Remark D's “every specialization is `S_5`” claim.
- [ ] Replace the equal-charge simplicity certificate with its exact degeneracy factorization.
- [ ] Rewrite §8 to recognize first-exit selection and equivariant spectral absorption.
- [ ] Correct the discriminant formula and generic-versus-specialized wording in clause (v).
- [ ] Qualify the closed-boundary claim when some charges vanish.

### High-value insertions

- [ ] Add the parity-block/singular-value factorization.
- [ ] Add the sheet-saturation theorem.
- [ ] Promote “physical root = unique least root” into a theorem/corollary.
- [ ] Add the generalized-eigenvalue/Rayleigh formula.
- [ ] Add strict coefficient-sign alternation.
- [ ] Add the `k=4` global-simplicity and shadow-ordering corollary.
- [ ] Add the physical-root sensitivity formulas.
- [ ] Update §9: only the certified numerical implementation remains open.

### Ledger enactment

- [ ] Add E-012 and E-013 only after paper revisions are signed off.
- [ ] Confirm PRED-003 with the strengthened positivity statement.
- [ ] Mark OBJ-004 complete with the stronger-absorption verdict.
- [ ] Do not count R5 alone toward G4-02.
- [ ] Append DEC-003; do not rewrite DEC-001 or DEC-002.
- [ ] Keep CAND-001 at S2 and move the active queue to OBJ-002/PRED-006.

---

## 10. Final audit statement

R5 is a successful theorem entry, but its most valuable form is not merely “all roots are real.” The stronger structure is:

```text
strict physical chamber
    = definite-pencil chamber
    -> parity-block singular-value spectrum
    -> one transverse crossing per positive-imbalance sheet
    -> every mass-square root strictly positive
    -> physical root is the unique least root
    -> exact first-exit / generalized-eigenvalue selection.
```

That is a real improvement to the mathematics and to the paper's practical root-selection program.

At the same time, the audit should be allowed to move the emergence ledger in the conservative direction: definite-pencil and spectrahedral theory absorb the reality, positivity, and first-exit mechanisms. The remaining candidate-specific content is the physical identification and its coupling to thermodynamic covariants, wall meaning, and reconstruction. That remainder is still important, but R5 alone does not yet establish an autonomous native theorem.

**Recommended disposition:** revise, promote the corrected mathematical package as E-012/E-013, complete OBJ-004 with a stronger-absorption verdict, confirm PRED-003, and retain CAND-001 at S2.
