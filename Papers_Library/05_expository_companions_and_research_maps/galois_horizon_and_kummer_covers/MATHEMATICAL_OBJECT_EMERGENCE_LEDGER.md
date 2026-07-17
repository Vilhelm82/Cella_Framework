# Mathematical Object Emergence Ledger

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
| CAND-001 | Finite algebraic cover with physical chamber, branch selection, parity, and norm-wall descent | S2 | Four-charge axial k-ellipse, generic reflection descent, S5 obstruction | Native morphisms + third independent family | 2026-07-10 |

### Current program-level judgment

```text
CAND-001 is more than an isolated bridge.

It is not yet an autonomous mathematical object.

The correct current classification is:

    Stage S2 — recurring structure / candidate object under test.
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
| `C` | Distinguished real or hyperbolic chamber | EVIDENCE |
| `s_phys` | Physical branch or section-selection rule | LEAD |
| `Omega` | Thermodynamic differential/covariant data | LEAD |
| `I` | Invariant and covariant observable algebra | EVIDENCE |
| `W` | Norm/discriminant wall structure | EVIDENCE |

### 3.4 Candidate native questions

```text
1. Which observables descend through X/G?
2. Which quantities are invariants, anti-invariants, or mixed covariants?
3. When does G obstruct reconstruction of physical branch data?
4. How is the physical real section selected among algebraic sheets?
5. When is the physical chamber a hyperbolicity or spectrahedral chamber?
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
| Hyperbolic-polynomial/LMI theory | Real-rootedness, rigid convexity, spectrahedral region | Physical sheet and thermodynamic observables | Probably | E-007 | Proof track open |
| Wall-arrangement theory | Signed hyperplanes, chamber intersections | Why walls are seed collapse or horizon degeneration | Probably | E-004 | Structural realization |
| Singularity/ramification theory | Branch divisors, inertia, collision strata | Distinguished physical component | Yes | E-008 | Campaign open |
| Category theory | Possible language for objects and morphisms | No candidate category defined yet | Unknown | — | Premature |

### Repeated remainder

Record a feature here only if at least three parent theories discard it.

| Remainder ID | Recurring lost datum | Parents that lose it | Consequence of loss | Status |
|---|---|---|---|---|
| REM-001 | Distinguished physical branch inside a finite algebraic cover | Galois, k-ellipse, invariant theory | Cannot identify the physical root from algebraic symmetry alone | EVIDENCE |
| REM-002 | Joint interaction of chamber geometry and deck parity | Galois, thermodynamics, wall theory | Total reality and physical selection remain disconnected | EVIDENCE |
| REM-003 | Thermodynamic meaning of invariants and anti-invariants | Galois, k-ellipse, hyperbolic theory | Parity statements can be algebraically correct but physically misidentified | EVIDENCE |
| REM-004 | Norm-wall divisor with both algebraic and physical roles | Galois, wall theory, thermodynamics | Signed walls and physical BPS wall can be conflated | EVIDENCE |

---

## 5. Native structure register

A candidate cannot advance to S3 until the first four rows are at least EVIDENCE and no row marked compulsory is EMPTY.

| Structure ID | Native component | Compulsory for S3? | Current formulation | Status | Next obligation |
|---|---|---:|---|---|---|
| NS-001 | Object | Yes | Tuple `(B,X->B,G,C,s_phys,Omega,I,W)` | LEAD | Remove redundant data; state axioms |
| NS-002 | Morphism | Yes | Must preserve cover, action, chamber, branch rule, and covariants | EMPTY | Define exact commutative diagrams |
| NS-003 | Equivalence | Yes | Isomorphism over base compatible with physical data | LEAD | Decide whether chamber/section preservation is strict or up to homotopy/conjugacy |
| NS-004 | Invariants | Yes | Descended observable algebra, norms, discriminants, parity grading | EVIDENCE | Define functorially |
| NS-005 | Covariants | No | Odd and mixed branch-oriented thermodynamic quantities | EVIDENCE | Define representation type |
| NS-006 | Operations | Yes for S4 | Quotient, pullback/base change, product, restriction to chamber | LEAD | Test closure |
| NS-007 | Subobject/degeneration | No | Wall restriction, branch collision, channel shutoff | LEAD | Formalize |
| NS-008 | Duality | No | Possible relation between cover action and charge/focus dualities | OPEN | Identify one exact operation |
| NS-009 | Reconstruction | Yes for S4 | Recover cover or physical branch from invariant/covariant data | OPEN | State minimal reconstruction problem |
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
| E-007 | 2026-07-10 | LMI/rigid convexity may imply total reality in the physical chamber | Convex algebraic geometry | PROOF-READY | PRED-003 | NPS representation | Needs exact line-restriction proof |
| E-008 | 2026-07-10 | Discriminant has collision and critical-sheet mechanisms | Ramification geometry | OBSERVED | NS-007 | R6/R7 audit | Must separate sub-balance from criticality |

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
| THM-002 | Sheet-oriented thermodynamic data transforms as covariants under the deck action | Candidate-native | EVIDENCE | NS-005 | Kerr–Newman; four-charge static |
| THM-003 | The Galois/monodromy group obstructs radical reconstruction of physical branch data | Candidate-native | EVIDENCE | NS-001, NS-004 | Four-charge static |
| THM-004 | Collapse walls are detected by norms of distinguished cover coordinates | Candidate-native | EVIDENCE | NS-004, NS-007 | Four-charge static |
| THM-005 | Hyperbolicity plus a physical chamber forces total reality of the restricted cover | Candidate-native | PROOF-READY | NS-001, NS-006 | Axial k-ellipse |
| THM-006 | Reflection-fixed branch radicals descend to the quotient field | Currently realization-specific | PROVED | E-005 | General axial k-ellipse family |

### Promotion rule for native theorems

Do not count a theorem toward S4 if it is merely an existing theorem with symbols renamed. It must do at least one of:

```text
1. Relate structures imported from two or more parent theories.
2. Make a prediction in a realization not used to formulate it.
3. Explain an obstruction that no single parent formulation states.
4. Classify candidate objects or morphisms intrinsically.
```

---

## 8. Prediction register

A prediction must be written before the confirming computation or proof.

| Prediction ID | Date registered | Prediction | Falsifier | Target family | Status | Outcome/evidence |
|---|---|---|---|---|---|---|
| PRED-001 | 2026-07-10 | Four independent charges are the first generic nonsolvable mass inversion | Solvable generic four-charge group | Charge ladder | CONFIRMED | S5 quintic |
| PRED-002 | 2026-07-10 | Five-charge mass-square norm has degree 16 | Degree other than 16 | General `k=5` mass fiber | CONFIRMED GENERICALLY | E-006 |
| PRED-003 | 2026-07-10 | All generic mass-square roots are real/nonnegative in the strict physical chamber | One certified nonreal root in the chamber | Axial k-ellipse | OPEN | LMI proof pending |
| PRED-004 | 2026-07-10 | Full static ordered-horizon field has degree 20 | Dependent square classes or lower field equality | Four-charge static | CONDITIONAL | Entry 4 + field identification |
| PRED-005 | 2026-07-10 | The same cover/chamber/parity/norm structure occurs in a third independent family | Failure to define one candidate datum | Third-family search | OPEN | Required for S3/S4 |

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

### Failed-reduction template

| Failure ID | Parent theory tested | Proposed reduction | Exact point of failure | Essential or repairable? | Decision | Date |
|---|---|---|---|---|---|---|
| FAIL-___ |  |  |  |  |  | YYYY-MM-DD |

---

## 11. Promotion gates

### 11.1 S2 -> S3: recurring structure to candidate object

| Gate | Requirement | Current status | Evidence or blocker |
|---|---|---|---|
| G3-01 | Minimal native data tuple | LEAD | NS-001 |
| G3-02 | Native morphisms | EMPTY | NS-002 |
| G3-03 | Native equivalence | LEAD | NS-003 |
| G3-04 | Intrinsic invariant/covariant algebra | EVIDENCE | NS-004, NS-005 |
| G3-05 | At least three independent realizations | BLOCKED | Only two closely related black-hole realizations |
| G3-06 | Same structural remainder in at least three parent theories | EVIDENCE | REM-001 to REM-004 |
| G3-07 | One theorem stated natively | LEAD | THM-001 to THM-005 |

**Current decision:**

```text
Do not promote CAND-001 to S3 yet.
```

### 11.2 S3 -> S4: candidate object to native theory

| Gate | Requirement | Current status |
|---|---|---|
| G4-01 | Closure under at least two natural operations | EMPTY |
| G4-02 | Three native theorems | LEAD |
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

| Priority | Task ID | Task | Gate changed if successful | Stop condition | Status |
|---:|---|---|---|---|---|
| 1 | OBJ-001 | Define native morphisms and equivalence for CAND-001 | G3-02, G3-03 | Definition collapses to a standard existing category without remainder | OPEN |
| 2 | OBJ-002 | Find and formalize a third independent realization | G3-05, G4-05 | Candidate data cannot be defined faithfully | OPEN |
| 3 | OBJ-003 | State and prove one genuinely native descent theorem | G3-07, G4-02 | The statement reduces verbatim to one parent theorem | OPEN |
| 4 | OBJ-004 | Prove total reality from chamber/LMI data | G4-02 | Counterexample in strict physical chamber | OPEN |
| 5 | OBJ-005 | Test closure under base change and quotient | G4-01 | Physical-section data is not preserved | OPEN |
| 6 | OBJ-006 | Search for non-black-hole realizations | G4-05, G5-01 | No candidate object survives outside founding examples | OPEN |
| 7 | OBJ-007 | Attempt a representation theorem | G4-03 | Data tuple is too weak or redundant | OPEN |

### Queue rule

If a task does not change a gate, correct a false claim, or test a falsifier, it belongs in an ordinary campaign plan rather than this emergence ledger.

---

## 13. Decision log

Append decisions; never rewrite old entries.

| Decision ID | Date | Candidate | Decision | Evidence considered | Revisit trigger |
|---|---|---|---|---|---|
| DEC-001 | 2026-07-10 | CAND-001 | Hold at S2 | Two realizations, strong remainder, no native morphisms or third family | OBJ-001 and OBJ-002 complete |

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

