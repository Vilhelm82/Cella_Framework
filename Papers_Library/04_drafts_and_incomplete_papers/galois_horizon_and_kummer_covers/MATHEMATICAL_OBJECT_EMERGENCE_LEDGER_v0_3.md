# Mathematical Object Emergence Ledger

**Version:** v0.3 (2026-07-10). v0.1 is the founding draft, v0.2 the first enacted revision, both of the same date — superseded, retained (provenance over purity).

### Changelog v0.2 → v0.3 (applied per §14 protocol; sources: LOG_ENTRY_R5_total_reality_v2.md, AUDIT_REPORT_R5_TOTAL_REALITY_AND_LEDGER_v0_2.md + counter-audit, map v1.4; GO 07-10, second of the day)

1. **E-007 PROOF-READY → SUPERSEDED** by **E-012** (new, PROVED): the R5 package — chamber = definiteness identity; total reality; **strict positivity**; parity-block singular-value factorization; **exact selection formula** `u_phys = λ_max(S)^{-2} = ||T||^{-2}` (least root / Rayleigh / first spectrahedral exit); coefficient alternation; sensitivity formulas.
2. New **E-013** (PROVED): sheet-saturation theorem — one transverse crossing per positive-imbalance sheet, no others; **chamber multiplicity is collision-only** (critical-sheet mechanism void on the strict axial chamber); `k = 4` global simplicity + canonical shadow ordering under (H2) alone; exact (1,4) degeneracy certificate `N_4 = 2^30(3-u)(15-u)^4` at `(2,1,1,1,1)`.
3. **PRED-003 OPEN → CONFIRMED**, strengthened from "real/nonnegative" to "real and strictly positive."
4. **THM-005 → SUPERSEDED, split** per the audit: **THM-005a** (definite-pencil reality/positivity/first-exit — TRANSLATED/PROVED in the realization; **native count: NO**) and **THM-005b** (physical branch = first spectrahedral exit = distinguished BPS wall component, compatibly with covariants and wall data — candidate-native **bridge**, PROVED in the founding realization, abstract form **LEAD**; native count: **not yet**). **R5 alone does not count toward G4-02.**
5. **Absorption test (OBJ-004) COMPLETE — verdict SPLIT, stronger absorption than drafted.** Equivariant definite-pencil / spectrahedral theory absorbs: bare reality, positivity-after-quotient, multiplicity-as-spectral-multiplicity, **and the first-exit selection mechanism itself**. Not supplied: why this chamber/ray is physically selected; horizon/thermodynamic meaning; BPS wall meaning; coupling to the cover/covariant/reconstruction package. Loss-matrix rows updated accordingly.
6. **REM-001 narrowed** (not dissolved): chamber + oriented ray DO select the root spectrally; the recurring lost datum contracts to the **physical interpretation and coupling** of the selection. Thesis-wording refinement registered for ratification: "the selection is spectral; the physics is the interpretation of the selection."
7. **NS-001** gains the founding-family realization note (physical section = first spectrahedral exit along the oriented mass ray in this family; do **not** assume this is intrinsic in all candidates). **NS-007/E-008** gain the chamber restriction (critical-sheet mechanism absent from strict-chamber axial crossings; alive off-chamber/complex).
8. **FAIL-005** recorded (equivariant definite-pencil absorption attempt — the most serious to date; FAIL-004 remains reserved by PRED-006's stop condition).
9. Queue: **OBJ-004 → COMPLETE**; active head advances to **OBJ-002 / PRED-006**. **DEC-003** appended. **CAND-001 HELD AT S2** (blockers NS-002, G3-05 unchanged).

---


**Project:** Cella / DBP / Galois–k-Ellipse Horizon Program  
**Purpose:** Track when a recurring bridge between existing mathematical theories warrants a new native mathematical object or theory.  
**Document mode:** Living, append-oriented research control document.  
**Naming rule:** Candidate names remain descriptive and provisional until the promotion gates are satisfied.

---

## 0. Why this format

Use one Markdown master ledger while there are at most three serious candidate objects.

The most practical structure is a hybrid:

| Data type | Best format | Reason |
|---|---|---|
| Candidate overview | Index table | Fast orientation |
| Parent-theory comparisons | Loss matrix | Repeated fields are easy to compare |
| Definitions and axioms | Structured candidate card | Mathematical nuance does not fit cleanly in cells |
| Evidence and counterevidence | Append-only table | Preserves provenance |
| Theorems and predictions | ID-indexed registers | Makes dependencies explicit |
| Promotion decisions | Gate table + decision log | Prevents premature naming |
| Failed reductions | Failure ledger | Stops repeated literature loops |
| Weekly changes | Dated log | Keeps the current state auditable |

Do not use a spreadsheet as the primary record. A spreadsheet is useful later for filtering dozens of candidates, but it handles equations, proof dependencies, and subtle equivalence claims rather badly. Markdown remains readable, searchable, versionable, and copy-friendly.

### Split rule

Split this file into an index plus separate candidate files only when one of the following becomes true:

```text
1. More than three candidates reach Stage S2.
2. Any candidate card exceeds roughly 300 lines.
3. Two candidates develop independent theorem and evidence registers.
4. Concurrent editing makes one file difficult to review.
```

Suggested later structure:

```text
MATHEMATICAL_OBJECT_EMERGENCE_INDEX.md
object_candidates/
    CAND-001__cover_chamber_descent.md
    CAND-002__provisional_name.md
evidence/
    EVIDENCE_REGISTER.md
decisions/
    PROMOTION_LOG.md
```

---

## 1. Status vocabulary

### 1.1 Candidate stages

| Stage | Label | Meaning |
|---:|---|---|
| S0 | Coincidence | A resemblance or isolated analogy |
| S1 | Bridge | A faithful translation between existing theories |
| S2 | Recurring structure | The same structural remainder appears in several translations |
| S3 | Candidate object | Native data, morphisms, equivalence, and invariants are defined |
| S4 | Native theory | The candidate supports its own theorems, operations, and predictions |
| S5 | Autonomous field | Nonrepresentable examples and an independent problem ecology exist |
| SX | Retired | Absorbed by an existing theory, refuted, or no longer productive |

### 1.2 Evidence status

| Status | Meaning |
|---|---|
| OBSERVED | Seen in an example or computation |
| REPRODUCED | Independently reproduced |
| CERTIFIED | Exact computational certificate exists |
| PROVED | Mathematical proof exists |
| IMPORTED | Established theorem imported from literature |
| PROOF-READY | Exact proof route known; one stated obligation remains |
| PREDICTED | Sharp, falsifiable consequence |
| OPEN | Not resolved |
| REFUTED | Demonstrably false |
| SUPERSEDED | Replaced by a stronger or corrected statement |

### 1.3 Gate status

| Gate status | Meaning |
|---|---|
| EMPTY | No usable formulation |
| LEAD | Plausible formulation, not demonstrated |
| EVIDENCE | Supported in examples |
| PROVED | Established generically or under explicit hypotheses |
| BLOCKED | A known obstruction prevents promotion |

---

## 2. Candidate index

| ID | Provisional description | Stage | Strongest evidence | Critical missing gate | Last reviewed |
|---|---|---:|---|---|---|
| CAND-001 | Finite algebraic cover with physical chamber, branch selection, parity, and norm-wall descent | S2 | Four-charge axial k-ellipse, generic reflection descent, S5 obstruction, isolation against both discriminant mechanisms (E-009), single-covariant reconstruction (E-010), chamber=definiteness identity + spectral selection formula (E-012), sheet saturation (E-013) | Native morphisms + third independent family | 2026-07-10 (v0.3) |

### Current program-level judgment

```text
CAND-001 is more than an isolated bridge.

It is not yet an autonomous mathematical object.

The correct current classification is:

    Stage S2 — recurring structure / candidate object under test.

[v0.3] The OBJ-004 absorption test moved the ledger in the CONSERVATIVE
direction: the strongest parent yet tested (equivariant definite-pencil /
spectrahedral theory) absorbs the reality, positivity, and even the
selection MECHANISM. The remainder — physical interpretation and its
coupling to covariants, walls, and reconstruction — is narrower than v0.2
believed, and is now the precise thing a native definition must carry.
```

---

## 3. Candidate card — CAND-001

### 3.1 Provisional descriptor

```text
Cover–chamber descent system
```

This is a descriptor, not a proposed permanent name.

### 3.2 Motivation

Several existing theories capture different projections of the same structure:

```text
finite algebraic cover
+
deck or monodromy action
+
distinguished real/hyperbolic chamber
+
distinguished physical branch
+
invariant/covariant thermodynamic data
+
norm-defined wall divisor
+
solvability obstruction for root data.
```

No single parent theory currently retains all of these simultaneously.

**[v0.3 sharpening, from OBJ-004.]** Equivariant definite-pencil theory
retains cover + parity + chamber + a canonical branch rule (first exit).
What it does not retain is the **meaning layer**: which chamber/ray is
physical, what the selected branch *is* thermodynamically, what the walls
*mean* (BPS), and how selection couples to the covariant/reconstruction
package. Any native axiomatization must make that meaning layer
first-class data, or the candidate is absorbed.

### 3.3 Provisional data tuple

A candidate system may have data

```text
T = (B, pi:X->B, G, C, s_phys, Omega, I, W)
```

with provisional meanings:

| Symbol | Provisional meaning | Status |
|---|---|---|
| `B` | Observable parameter space | EVIDENCE |
| `pi:X->B` | Finite algebraic cover of branch data | EVIDENCE |
| `G` | Deck, Galois, or monodromy action | EVIDENCE |
| `C` | Distinguished real or hyperbolic chamber | EVIDENCE [v0.3: in the founding family, C is REPRESENTABLE — identically the definiteness/hyperbolicity region of the pencil (E-012 Lemma A); as reality-datum it is not extra data] |
| `s_phys` | Physical branch or section-selection rule | LEAD [v0.3: in the founding family the RULE is spectral (first exit / least root, E-012); the datum that is not representable is the rule's physical MEANING] |
| `Omega` | Thermodynamic differential/covariant data | LEAD |
| `I` | Invariant and covariant observable algebra | EVIDENCE |
| `W` | Norm/discriminant wall structure | EVIDENCE |

### 3.4 Candidate native questions

```text
1. Which observables descend through X/G?
2. Which quantities are invariants, anti-invariants, or mixed covariants?
3. When does G obstruct reconstruction of physical branch data?
4. How is the physical real section selected among algebraic sheets?
   [v0.3: in the founding family, answered mechanically — first
   spectrahedral exit along the oriented mass ray; the native question
   becomes: what data DETERMINES the ray and its interpretation?]
5. When is the physical chamber a hyperbolicity or spectrahedral chamber?
   [v0.3: in the founding family, ALWAYS and EXACTLY — E-012 Lemma A.]
6. Which boundary divisors are norms, discriminants, or ramification loci?
7. How do wall intersections change inertia and monodromy?
8. What data reconstructs X from the descended observable algebra?
9. Which morphisms preserve physical branch selection and thermodynamic data?
10. Which systems satisfy the axioms without arising from black holes or k-ellipses?
```

### 3.5 Current non-goal

Do not currently claim a new field or permanent object name. The present task is to determine whether the recurring remainder has a stable native definition.

---

## 4. Parent-theory loss matrix

Update this table whenever a new parent theory is tested.

| Parent theory | Faithful content captured | Structure lost or externalized | Does the loss change theorems? | Evidence IDs | Current verdict |
|---|---|---|---|---|---|
| Algebraic k-ellipse theory | Distance sum, degree, signed norm, LMI, rigid convexity | Horizon meaning, entropy field, thermodynamic branch selection | Yes | E-002, E-006 | Strong realization, not complete owner |
| Galois theory | Field tower, solvability, monodromy, norms | Distinguished physical chamber and real branch | Yes | E-002, E-004 | Essential parent, incomplete alone |
| Invariant theory | Quotient, parity, invariants and covariants | Thermodynamic first-law meaning, physical positivity | Yes | E-001, E-003 | Essential language |
| Black-hole thermodynamics | Horizons, entropy, temperature, first laws | Algebraic-cover degree, Galois obstruction, norm geometry | Yes | E-001, E-002, E-004 | Physical realization |
| Hyperbolic-polynomial/LMI theory | Real-rootedness, rigid convexity, spectrahedral region; [v0.3] positivity via parity grading, spectral multiplicity, first-exit selection | [v0.3] Physical MEANING of sheet/ray/walls and thermodynamic observables | Yes — but less than v0.2 believed | E-007 → E-012, E-013 | **TESTED (OBJ-004): strongest mechanism parent** — absorbs reality, positivity, multiplicity, and the selection mechanism; loses the interpretation layer |
| Wall-arrangement theory | Signed hyperplanes, chamber intersections | Why walls are seed collapse or horizon degeneration | Probably | E-004 | Structural realization |
| Singularity/ramification theory | Branch divisors, inertia, collision strata | Distinguished physical component | Yes | E-008, E-011, E-013 | Campaign open; mechanism decomposition, ramification parity, and strict-axial-chamber saturation now PROVED |
| Real fibered morphisms / hyperbolicity (Helton–Vinnikov; Kummer–Shamovich; MTV total reality) [v0.2] | Total reality, chamber as hyperbolicity region, real-locus-preserving covers; [v0.3] + canonical first-exit branch rule given a base point and oriented ray | [v0.3] Deck-parity THERMODYNAMIC grading (the algebraic parity itself is captured), norm-wall BPS meaning, solvability obstruction, physical selection of chamber/ray | Yes | E-007 → E-012 | **TESTED (OBJ-004, GO 07-10): verdict SPLIT, absorption stronger than drafted.** Absorbs the reality clause completely (chamber = hyperbolicity region — exact identity) AND the selection mechanism (first exit = physical root). Does not supply the physical interpretation/coupling. Absorption threat RESOLVED; retained as mechanism parent, not owner |
| Enumerative monodromy (Harris; Sottile Schubert Galois groups) [v0.2] | Monodromy/Galois groups as obstructions to formulas | Chamber, physical branch, thermodynamic covariants, wall meaning | Yes | E-002 | Owns THM-003's obstruction language; loses everything physical |
| Category theory | Possible language for objects and morphisms | No candidate category defined yet | Unknown | — | Premature |

### Repeated remainder

Record a feature here only if at least three parent theories discard it.

| Remainder ID | Recurring lost datum | Parents that lose it | Consequence of loss | Status |
|---|---|---|---|---|
| REM-001 | Distinguished physical branch inside a finite algebraic cover [v0.3 NARROWED: chamber + oriented ray select the branch spectrally (first exit, E-012); the recurring lost datum is now precisely the PHYSICAL INTERPRETATION of that selection — which ray, why, and what the selected branch means] | Galois, k-ellipse, invariant theory; [v0.3] definite-pencil theory loses only the interpretation half | Cannot identify the physical root's MEANING from algebraic/spectral symmetry alone; the mechanism, however, is representable | EVIDENCE — narrowed, not dissolved |
| REM-002 | Joint interaction of chamber geometry and deck parity | Galois, thermodynamics, wall theory | Total reality and physical selection remain disconnected [v0.2: the isolation theorem E-009 is the first statement requiring C, s_phys, and W jointly] [v0.3: E-012 Lemma A IDENTIFIES chamber with definiteness in the founding family, and R5b runs parity and chamber jointly — the disconnection is repaired inside the realization; the native question is whether the identification is an axiom or a theorem] | EVIDENCE |
| REM-003 | Thermodynamic meaning of invariants and anti-invariants | Galois, k-ellipse, hyperbolic theory | Parity statements can be algebraically correct but physically misidentified | EVIDENCE |
| REM-004 | Norm-wall divisor with both algebraic and physical roles | Galois, wall theory, thermodynamics | Signed walls and physical BPS wall can be conflated [v0.2: the conflation is now provably an error — E-011, map guardrail 12] | EVIDENCE |

---

## 5. Native structure register

A candidate cannot advance to S3 until the first four rows are at least EVIDENCE and no row marked compulsory is EMPTY.

| Structure ID | Native component | Compulsory for S3? | Current formulation | Status | Next obligation |
|---|---|---:|---|---|---|
| NS-001 | Object | Yes | Tuple `(B,X->B,G,C,s_phys,Omega,I,W)` | LEAD | Remove redundant data; state axioms. [v0.2] Isolation-axiom candidate registered: `s_phys` extends over `int(C)` without meeting the branch locus; the four-charge isolation theorem (E-009) is the verification in the founding family. [v0.3, audit] Founding-family realization note: the physical section is the FIRST SPECTRAHEDRAL EXIT along the oriented mass ray in this family — do NOT assume this is intrinsic in all candidates; and for reality purposes `C` is representable inside the pencil (E-012 Lemma A), so the axioms must locate the non-representable content (interpretation/coupling) or concede absorption |
| NS-002 | Morphism | Yes | Must preserve cover, action, chamber, branch rule, and covariants | EMPTY | Define exact commutative diagrams |
| NS-003 | Equivalence | Yes | Isomorphism over base compatible with physical data | LEAD | Decide whether chamber/section preservation is strict or up to homotopy/conjugacy |
| NS-004 | Invariants | Yes | Descended observable algebra, norms, discriminants, parity grading | EVIDENCE | Define functorially |
| NS-005 | Covariants | No | Odd and mixed branch-oriented thermodynamic quantities | EVIDENCE | Define representation type |
| NS-006 | Operations | Yes for S4 | Quotient, pullback/base change, product, restriction to chamber | LEAD | Test closure |
| NS-007 | Subobject/degeneration | No | Wall restriction, branch collision (two mechanisms: sheet-collision sub-balances + critical-sheet `sum eps_i/w_i = 0` [v0.2, E-008]), channel shutoff. [v0.3, audit] Chamber restriction: the critical-sheet mechanism exists in the broader discriminant geometry but is ABSENT from strict-chamber axial crossings (E-013 saturation) — chamber multiplicity is collision-only | LEAD | Formalize; stratify critical-sheet components off-chamber/complex |
| NS-008 | Duality | No | Possible relation between cover action and charge/focus dualities | OPEN | Identify one exact operation |
| NS-009 | Reconstruction | Yes for S4 | Recover cover or physical branch from invariant/covariant data. [v0.2] Minimal reconstruction problem stated: which single covariants generate the total field over `B`? First instance PROVED (E-010: either normalized horizon entropy alone, pivot = area product) | EVIDENCE | Generalize the single-generator statement natively |
| NS-010 | Representation | Yes for S4 | Realizations as k-ellipses, horizon covers, or other systems | LEAD | Prove a representation theorem |

---

## 6. Evidence ledger

Append new rows. Never delete a refuted row; change its status and add a correction link.

| Evidence ID | Date | Result | Domain | Status | Supports | Source/ref | Notes |
|---|---|---|---|---|---|---|---|
| E-001 | 2026-07-10 | Kerr–Newman horizons form a quadratic cover with a horizon-swap involution | Thermodynamics/Galois | PROVED | REM-001, NS-004 | Horizon-cover draft | Temperature itself is mixed; `S*T` is odd |
| E-002 | 2026-07-10 | Four-charge mass fiber is the axial restriction of an algebraic 4-ellipse | Multifocal geometry | PROVED + IMPORTED | CAND-001 | NPS bridge + mass relation | Explains degree five after `u=m^2` quotient |
| E-003 | 2026-07-10 | Axial reflection `m->-m` realizes static horizon swap | Invariant theory/thermodynamics | PROVED | REM-002, NS-005 | R6/R7 descent work | Requires correct lift to entropy variables |
| E-004 | 2026-07-10 | Norm of `u` splits into sixteen signed BPS-type wall factors | Galois/wall geometry | PROVED | REM-004, NS-004 | Wall-factorization theorem | Physical BPS wall is one chamber component |
| E-005 | 2026-07-10 | Generic descent `w_i in K=F(u)` | Function fields | PROVED | NS-004, NS-010 | R6/R7 audit | Removes point-B descent caveat |
| E-006 | 2026-07-10 | Generic mass degree follows k-ellipse half-degree for all `k`; `k=5` gives 16 | Algebraic geometry | PROVED | THM-003, PRED-002 | R6/R7 Theorem 4 | Specialized Galois group remains open |
| E-007 | 2026-07-10 | LMI/rigid convexity may imply total reality in the physical chamber | Convex algebraic geometry | **SUPERSEDED [v0.3] → E-012** | PRED-003 | NPS representation | Proof route completed and strengthened; see E-012 |
| E-008 | 2026-07-10 | Discriminant has collision and critical-sheet mechanisms | Ramification geometry | PROVED [v0.2] | NS-007 | LOG_ENTRY_R6_R7_generic_descent_v2.md §9; map v1.3 Branch E | Decomposition promoted on GO; stratification of critical-sheet components remains OPEN. [v0.3] Chamber restriction: mechanism 2 is VOID on strict-chamber axial crossings (E-013) — alive off-chamber/complex |
| E-009 | 2026-07-10 | Physical (all-plus) sheet is free of BOTH discriminant mechanisms: collision-free and `sum_i 1/w_i > 0` strictly on the chamber | Ramification/chamber geometry | PROVED (prose) | REM-002, NS-001 (axiom candidate), NS-007 | Entry v2 §9 isolation upgrade; map v1.3 R17 | First statement requiring C, s_phys, and W jointly. [v0.3] Now subsumed on the strict axial chamber by E-013 (saturation extends tangency-freeness to EVERY crossing sheet) |
| E-010 | 2026-07-10 | Ordered-horizon field reconstruction: `F(Shat_+, Shat_-) = K(m,y)`; either normalized horizon entropy ALONE generates it, pivot `Shat_+ Shat_- = P` | Field theory/reconstruction | PROVED | NS-009, NS-004 | Entry v2 P6 (R19) | Degree-20 count conditional on Entry-4 gate; the field identity is unconditional |
| E-011 | 2026-07-10 | Ramification of `W/K` iff `ord_v(u)` odd; deck fixed divisor = signed axial-contact divisor; only the all-plus component is the physical BPS/extremal locus | Ramification geometry | PROVED (finite part; infinite places unswept) | REM-004, NS-004 | Entry v2 Thm 5 remark (R18); map guardrail 12 | Upgrades the signed-vs-physical wall distinction from caution to theorem |
| E-012 | 2026-07-10 [v0.3] | **R5 package**: strict chamber = definiteness region of the axial pencil (exact identity); every mass-square root real and STRICTLY POSITIVE; deck involution = parity grading, `N_k(u) = det(L_0)·prod_j(1 - u σ_j(T)^2)`; physical root = unique least root; exact selection `u_phys = λ_max(S)^{-2} = \|\|T\|\|^{-2}` (Rayleigh / first spectrahedral exit); strict coefficient alternation; sensitivity/condition-number formulas | Convex algebraic geometry / spectral theory / thermodynamics | PROVED | REM-001 (narrowing), REM-002, REM-003, NS-001, NS-004, THM-005a/b, PRED-003 | LOG_ENTRY_R5_total_reality_v2.md (R5a–R5c); audit + counter-audit 07-10 | Selection MECHANISM absorbed by the pencil parent; selection MEANING is the residue. Supersedes E-007 |
| E-013 | 2026-07-10 [v0.3] | **Sheet saturation**: every positive-imbalance sheet crosses exactly once, transversely; no other sheet crosses; every strict-chamber multiple root is an inter-sheet COLLISION (critical-sheet mechanism void on the strict axial chamber). `k = 4`: GLOBAL simplicity under (H2) alone + canonical shadow ordering by charge magnitude. Exact (1,4) degeneracy certificate `N_4 = 2^30(3-u)(15-u)^4` at `(2,1,1,1,1)` | Ramification/chamber geometry | PROVED | NS-007, NS-001, REM-002 | LOG_ENTRY_R5_total_reality_v2.md (R5c-0, R5d, §6); audit §6.2/6.6 + counter-audit | Corollary of total reality (budget argument); strengthens E-008/E-009 on the strict axial slice |

### Evidence entry template

| Evidence ID | Date | Result | Domain | Status | Supports | Source/ref | Notes |
|---|---|---|---|---|---|---|---|
| E-___ | YYYY-MM-DD |  |  | OBSERVED |  |  |  |

---

## 7. Native theorem register

A theorem belongs here only if it can be stated primarily in the candidate language, even if its proof imports older mathematics.

| Theorem ID | Provisional statement | Native or translated? | Status | Dependencies | Tested examples |
|---|---|---|---|---|---|
| THM-001 | Universal observables factor through the invariant quotient | Candidate-native | LEAD | NS-001, NS-004 | Kerr–Newman; four-charge static |
| THM-002 | Sheet-oriented thermodynamic data transforms as covariants under the deck action | Candidate-native | PROVED in both founding realizations [v0.2]: `tau(Shat_±)=Shat_∓`, `tau(T_+)=T_-` (mixed), `Theta=S*T` anti-invariant; native form LEAD | NS-005, E-003, E-010 | Kerr–Newman; four-charge static |
| THM-003 | The Galois/monodromy group obstructs radical reconstruction of physical branch data | Candidate-native | EVIDENCE | NS-001, NS-004 | Four-charge static |
| THM-004 | Collapse walls are detected by norms of distinguished cover coordinates | Candidate-native | EVIDENCE | NS-004, NS-007 | Four-charge static |
| THM-005 | Hyperbolicity plus a physical chamber forces total reality of the restricted cover | — | **SUPERSEDED [v0.3] — split into THM-005a / THM-005b per audit** | — | — |
| THM-005a [v0.3] | A definite symmetric pencil over the strict chamber gives a real axial fiber; an anti-commuting parity involution gives a positive quotient fiber and a first-exit eigenvalue selection formula | **TRANSLATED** (equivariant definite-pencil theory) | PROVED in the axial k-ellipse realization (E-012). **Native count: NO** | E-012 | Axial k-ellipse, all k |
| THM-005b [v0.3] | The physically selected branch is identified with the first spectrahedral exit AND with the distinguished BPS wall component, compatibly with cover covariants and wall data | Candidate-native **BRIDGE** | PROVED in the founding realization; abstract candidate-language form **LEAD**. **Native count: not yet** | E-012, E-013, E-011, NS-001 | Four-charge static |
| THM-006 | Reflection-fixed branch radicals descend to the quotient field | Currently realization-specific | PROVED | E-005 | General axial k-ellipse family |

### Promotion rule for native theorems

Do not count a theorem toward S4 if it is merely an existing theorem with symbols renamed. It must do at least one of:

```text
1. Relate structures imported from two or more parent theories.
2. Make a prediction in a realization not used to formulate it.
3. Explain an obstruction that no single parent formulation states.
4. Classify candidate objects or morphisms intrinsically.
```

**[v0.3 ruling, per audit + DEC-003:** R5 alone does not count toward
G4-02. THM-005a fails the rule (renamed pencil theory). THM-005b satisfies
rule 1 in its realization but has no abstract formulation yet — it counts
when, and only when, an intrinsic statement is drafted whose content
survives after the spectral mechanism is removed.**]**

---

## 8. Prediction register

A prediction must be written before the confirming computation or proof.

| Prediction ID | Date registered | Prediction | Falsifier | Target family | Status | Outcome/evidence |
|---|---|---|---|---|---|---|
| PRED-001 | 2026-07-10 | Four independent charges are the first generic nonsolvable mass inversion | Solvable generic four-charge group | Charge ladder | CONFIRMED | S5 quintic |
| PRED-002 | 2026-07-10 | Five-charge mass-square norm has degree 16 | Degree other than 16 | General `k=5` mass fiber | CONFIRMED GENERICALLY | E-006 |
| PRED-003 | 2026-07-10 | All generic mass-square roots are real/nonnegative in the strict physical chamber | One certified nonreal root in the chamber | Axial k-ellipse | **CONFIRMED [v0.3] — STRENGTHENED**: all roots (not just generic) real and STRICTLY POSITIVE; `N_k(0) = det L_0 > 0` | E-012 |
| PRED-004 | 2026-07-10 | Full static ordered-horizon field has degree 20 | Dependent square classes or lower field equality | Four-charge static | CONDITIONAL | [v0.2] Field identification PROVED (E-010); sole remaining condition = Entry-4 gate: good-specialization statement + independent re-verification (map Branch I item d). [v0.3] Unaffected by the R5 entry |
| PRED-005 | 2026-07-10 | The same cover/chamber/parity/norm structure occurs in a third independent family | Failure to define one candidate datum | Third-family search | OPEN | Required for S3/S4 |
| PRED-006 | 2026-07-10 [v0.2 — registered BEFORE any OBJ-002 attempt, per §14 step 4] | The precision-flow rounding structure defines a faithful CAND-001 tuple: `pi` = degree-2 dyadic/rounding cover; `C` = binade/representable chamber; `s_phys` = rounding rule (round-to-nearest as branch selection); `W ⊇` {ULP/binade walls, dyadic-death locus}; `Omega` = Refinement-Law flow; covariant = signed residual (sign flips under local reflection, magnitude descends). Structural thread: `ord_v(u)` parity governs horizon-cover ramification, `ord_2(b_0)` governs precision-flow periodicity — same valuation-parity instrument | Some datum (`Omega` or `G` most at risk) is only definable vacuously, or no banked theorem transfers | Precision flow (HR133 campaign — cite, do not re-derive) | OPEN — **[v0.3] ACTIVE HEAD of the queue** | If refuted: record FAIL-004 and stop; no forcing. [v0.3 note from OBJ-004: the faithfulness bar now includes the interpretation layer — a rounding cover whose `s_phys` is only the spectral/first-exit mechanism with no independent meaning datum does NOT count as a faithful tuple] |

### Prediction entry template

| Prediction ID | Date registered | Prediction | Falsifier | Target family | Status | Outcome/evidence |
|---|---|---|---|---|---|---|
| PRED-___ | YYYY-MM-DD |  |  |  | OPEN |  |

---

## 9. Nonrepresentable-example register

This is the strongest autonomy test.

A nonrepresentable example is a valid candidate object satisfying the native axioms that does not arise from any founding realization.

| Example ID | Candidate object | Why it satisfies the axioms | Why it is not a founding realization | Status |
|---|---|---|---|---|
| NR-001 | Not yet found | — | — | EMPTY |

### Required progression

```text
First:  third independent realization.
Then:   abstract examples generated by candidate operations.
Finally: prove at least one example cannot be represented as a black-hole
         horizon cover or axial k-ellipse.
```

No promotion to S5 without a genuine nonrepresentable example.

---

## 10. Failed-reduction ledger

Record serious attempts to absorb the candidate into an existing theory. This prevents endless rediscovery of the same near-match.

| Failure ID | Parent theory tested | Proposed reduction | Exact point of failure | Essential or repairable? | Decision | Date |
|---|---|---|---|---|---|---|
| FAIL-001 | Algebraic k-ellipses | Treat the complete structure as an axial k-ellipse | No thermodynamic covariants or physical horizon field | Essential so far | Retain as realization, not owner | 2026-07-10 |
| FAIL-002 | Galois theory | Treat physical system as only a field extension | Physical chamber and distinguished root are absent | Essential so far | Enrich rather than replace | 2026-07-10 |
| FAIL-003 | Invariant theory | Treat all observables as invariants/covariants | Does not encode thermodynamic differential structure | Possibly repairable | Test equivariant/contact enrichment | 2026-07-10 |
| FAIL-005 [v0.3] | Equivariant definite-pencil / spectrahedral theory (OBJ-004 test) | Absorb the full R5 package: chamber, reality, positivity, multiplicity, selection | The MECHANISM does not fail — it absorbs (reality, positivity, spectral multiplicity, first-exit selection all representable). Failure point is the INTERPRETATION layer: physical choice of chamber/ray, horizon/thermodynamic meaning of the selected branch, BPS wall semantics, coupling to covariants/reconstruction (E-010, THM-002) | Essential so far — and now precisely localized | Retain as the strongest mechanism parent; any native axiomatization must carry the interpretation layer as first-class data or concede absorption | 2026-07-10 |

*Numbering note [v0.3]: FAIL-004 remains reserved by PRED-006's stop
condition (a refuted precision-flow tuple); FAIL-005 is used here to keep
that reservation intact. IDs are labels, not a chronology.*

### Failed-reduction template

| Failure ID | Parent theory tested | Proposed reduction | Exact point of failure | Essential or repairable? | Decision | Date |
|---|---|---|---|---|---|---|
| FAIL-___ |  |  |  |  |  | YYYY-MM-DD |

---

## 11. Promotion gates

### 11.1 S2 -> S3: recurring structure to candidate object

| Gate | Requirement | Current status | Evidence or blocker |
|---|---|---|---|
| G3-01 | Minimal native data tuple | LEAD | NS-001 [v0.3: axioms must now locate the non-representable interpretation content — see FAIL-005] |
| G3-02 | Native morphisms | EMPTY | NS-002 |
| G3-03 | Native equivalence | LEAD | NS-003 |
| G3-04 | Intrinsic invariant/covariant algebra | EVIDENCE | NS-004, NS-005 |
| G3-05 | At least three independent realizations | BLOCKED | Only two closely related black-hole realizations |
| G3-06 | Same structural remainder in at least three parent theories | EVIDENCE | REM-001 to REM-004 [v0.3: REM-001 narrowed to the interpretation layer — still lost by ≥3 parents] |
| G3-07 | One theorem stated natively | LEAD | THM-001 to THM-005b [v0.3: THM-005b is the nearest candidate; abstract form owed] |

**Current decision:**

```text
Do not promote CAND-001 to S3 yet.   [Reaffirmed v0.3, DEC-003.]
```

### 11.2 S3 -> S4: candidate object to native theory

| Gate | Requirement | Current status |
|---|---|---|
| G4-01 | Closure under at least two natural operations | EMPTY |
| G4-02 | Three native theorems | LEAD [v0.3: R5 alone does NOT count (audit ruling, DEC-003); THM-005b counts only once an intrinsic abstract formulation is drafted] |
| G4-03 | One representation or realization theorem | LEAD |
| G4-04 | One obstruction or impossibility theorem | EVIDENCE |
| G4-05 | One successful preregistered prediction in a new family | EMPTY |
| G4-06 | Independent proof technology or classification problem | LEAD |

### 11.3 S4 -> S5: native theory to autonomous field

| Gate | Requirement | Current status |
|---|---|---|
| G5-01 | Nonrepresentable examples | EMPTY |
| G5-02 | Independent problem ecology | LEAD |
| G5-03 | Results useful outside founding applications | EMPTY |
| G5-04 | Stable terminology accepted by more than one worker/group | EMPTY |
| G5-05 | Multiple independent research directions | EVIDENCE |

---

## 12. Research queue

Rank only tasks that change a promotion gate or falsify the candidate.

**[v0.2 re-rank, 07-10 review; v0.3 status updates — revert via decision-log entry if disputed.]**

| Priority | Task ID | Task | Gate changed if successful | Stop condition | Status |
|---:|---|---|---|---|---|
| — | OBJ-004 | Prove total reality from chamber/LMI data. [v0.2] Doubles as the absorption test vs real fibered morphisms | G4-02; loss-matrix verdict for real fibered morphisms | Counterexample in strict physical chamber | **COMPLETE [v0.3, GO 07-10]** — theorem proved and strengthened (E-012/E-013); absorption verdict SPLIT, stronger than drafted; G4-02 NOT credited from R5 alone; loss matrix updated; DEC-002's revisit trigger fired |
| 1 | OBJ-002 | Find and formalize a third independent realization. [v0.2] First attempt = precision-flow tuple per PRED-006 (structurally independent: no black holes, no ellipses). Registered lead #2: Seiberg–Witten families (`B` = Coulomb branch, `W` = discriminant of massless BPS states, `Omega` = SW differential — a textbook realization of the `Omega` slot; literature-heavy, so second). [v0.3] Faithfulness bar raised per FAIL-005: the tuple must carry an interpretation datum for `s_phys`, not merely a selection mechanism | G3-05, G4-05 | Candidate data cannot be defined faithfully → FAIL-004 | OPEN — **ACTIVE HEAD** |
| 2 | OBJ-001 | Define native morphisms and equivalence for CAND-001. [v0.2] Deliberately sequenced AFTER the OBJ-002 attempt: with only two sibling black-hole realizations the definition over-fits ("charge specialization + base change" is circular); a rounding cover on the other side of the arrow forces honesty. [v0.3] Morphisms must preserve the interpretation layer, per FAIL-005 | G3-02, G3-03 | Definition collapses to a standard existing category without remainder | OPEN |
| 3 | OBJ-003 | State and prove one genuinely native descent theorem. [v0.3] Nearest concrete target: the abstract form of THM-005b (selection = first exit = distinguished wall component, stated intrinsically) | G3-07, G4-02 | The statement reduces verbatim to one parent theorem | OPEN |
| 4 | OBJ-005 | Test closure under base change and quotient | G4-01 | Physical-section data is not preserved | OPEN |
| 5 | OBJ-006 | Search for non-black-hole realizations. [v0.2] Partially subsumed by OBJ-002 leads (precision flow, SW families); keep open for the nonrepresentable-example runway | G4-05, G5-01 | No candidate object survives outside founding examples | OPEN |
| 6 | OBJ-007 | Attempt a representation theorem | G4-03 | Data tuple is too weak or redundant | OPEN |

### Queue rule

If a task does not change a gate, correct a false claim, or test a falsifier, it belongs in an ordinary campaign plan rather than this emergence ledger.

---

## 13. Decision log

Append decisions; never rewrite old entries.

| Decision ID | Date | Candidate | Decision | Evidence considered | Revisit trigger |
|---|---|---|---|---|---|
| DEC-001 | 2026-07-10 | CAND-001 | Hold at S2 | Two realizations, strong remainder, no native morphisms or third family | OBJ-001 and OBJ-002 complete |
| DEC-002 | 2026-07-10 | CAND-001 | Hold at S2; re-rank queue (OBJ-004 → OBJ-002 → OBJ-001); attach the real-fibered-morphisms absorption test to OBJ-004; register PRED-006 before any OBJ-002 attempt; add two absorber rows to the loss matrix | E-008 → PROVED; new E-009/E-010/E-011; THM-002 upgrade; NS-009 → EVIDENCE | OBJ-004 complete, or PRED-006 resolved either way |
| DEC-003 | 2026-07-10 | CAND-001 | Enact the audited R5 package (E-012, E-013; PRED-003 confirmed-strengthened; E-007 superseded). Split THM-005 into 005a (translated — native count NO) and 005b (bridge — native count not yet; abstract formulation owed, feeds OBJ-003). Do NOT count R5 alone toward G4-02. Record FAIL-005 (definite-pencil absorption attempt: mechanism absorbed, interpretation layer is the residue). Narrow REM-001 accordingly; raise the PRED-006 faithfulness bar to include the interpretation datum. **HOLD CAND-001 AT S2** (NS-002 EMPTY, G3-05 BLOCKED — unchanged by R5). Advance queue head to OBJ-002 / PRED-006. Thesis-wording refinement registered for ratification: "the selection is spectral; the physics is the interpretation of the selection" | AUDIT_REPORT_R5_TOTAL_REALITY_AND_LEDGER_v0_2.md; counter-audit in LOG_ENTRY_R5_total_reality_v2.md; map v1.4 | PRED-006 resolved either way; or an intrinsic THM-005b formulation drafted (OBJ-003); or a new absorber row is proposed |

### Decision entry template

| Decision ID | Date | Candidate | Decision | Evidence considered | Revisit trigger |
|---|---|---|---|---|---|
| DEC-___ | YYYY-MM-DD | CAND-___ |  |  |  |

---

## 14. Update protocol

Use this sequence whenever a result appears relevant to object emergence.

```text
Step 1 — Record the result in the evidence ledger.
Step 2 — Link it to one or more remainder, structure, theorem, or gate IDs.
Step 3 — Ask whether it changes a parent-theory loss claim.
Step 4 — Register any new prediction before testing it.
Step 5 — Update gate status only after proof/certificate review.
Step 6 — Add a decision-log row if the candidate stage changes or is held.
Step 7 — Mark superseded statements; never erase provenance.
```

**[v0.3 compliance note:** this revision followed all seven steps —
evidence recorded (E-012/E-013, step 1); linked (step 2); two loss-matrix
rows changed with the OBJ-004 verdict (step 3); no new predictions were
tested unregistered, and PRED-006's bar was tightened before its attempt
(step 4); gates updated only after the audit + counter-audit chain
(step 5); DEC-003 appended (step 6); E-007 and THM-005 marked SUPERSEDED,
nothing erased (step 7).**]**

### Weekly five-minute review

```text
[ ] Did a new parent theory absorb the candidate more faithfully?
[ ] Did the same structural remainder recur again?
[ ] Is there now a native morphism or operation?
[ ] Was any prediction confirmed or refuted?
[ ] Did a third independent realization appear?
[ ] Did a theorem become candidate-native rather than translated?
[ ] Should the candidate advance, remain held, or be retired?
```

### Monthly adversarial review

Ask:

```text
1. What is the strongest existing theory that could still absorb this?
2. Which candidate datum is genuinely indispensable?
3. Can that datum be removed without changing theorems?
4. Are the “native theorems” merely imported results with renamed symbols?
5. Has the framework predicted anything outside its construction examples?
6. Does any valid abstract example exist beyond black holes and k-ellipses?
7. What evidence would make us retire the candidate?
```

**[v0.3 standing answers, post-OBJ-004:** Q1 = equivariant definite-pencil
theory (tested; FAIL-005). Q2 = the interpretation layer of `s_phys` plus
the thermodynamic covariant coupling — everything else in R5 proved
representable. Q4 = THM-005a yes (excluded from the count); THM-005b no,
but its abstract form is owed.**]**

---

## 15. Candidate card template

Copy this section for each new candidate.

```markdown
## Candidate card — CAND-___

### Provisional descriptor

### Motivating recurring structure

### Minimal data tuple

### Proposed axioms

### Native morphisms

### Native equivalence

### Invariants and covariants

### Natural operations

### Parent-theory loss matrix links

### Realizations

### Nonrepresentable examples

### Native theorem candidates

### Predictions

### Counterevidence

### Current promotion gates

### Next decisive test

### Current decision
```

---

## 16. Final operating principle

```text
Do not promote a candidate because many theories resemble it.

Promote it when:

1. the same essential datum is lost by every serious reduction;
2. that datum has native morphisms and invariants;
3. the resulting axioms generate new theorems or predictions;
4. the structure survives beyond its founding examples.
```

The ledger is designed to make that decision evidence-driven rather than dependent on how exciting the latest bridge feels. Excitement is allowed to choose the next experiment; it does not get voting rights at the promotion gate.

**[v0.3 footnote:** OBJ-004 is the format working as designed: the
candidate's flagship theorem was deliberately exposed to its strongest
absorber, the absorber took MORE than expected, and the ledger got sharper
for it. The essential datum of principle 1 is now localized — it is the
interpretation layer, and PRED-006 will test whether it recurs.**]**
