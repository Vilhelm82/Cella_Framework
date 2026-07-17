# Cella Frontier Research ROI Outlook

## A risk-adjusted programme for extending the corpus through arithmetic, monodromy, string-theoretic geometry, and black-hole structure

**Version:** 1.0  
**Date:** 2026-07-17  
**Author:** Will Lloyd  
**Document class:** corpus-wide research map and investment outlook  
**Evidence status:** demonstrated corpus audit plus explicitly labelled research conjectures  
**DAG snapshot:** `cella-dbp-frontier`, revision `sha256:00ef143b0e00f29f8a8f97ee4583907262db1c829ff6ba8c236cb71a3719fec1`

---

## Abstract

This report evaluates the prospective mathematical reach of the current Cella corpus and ranks research targets by their ability to close existing gaps, strengthen downstream papers, generate reusable mathematics, and open credible bridges between algebraic geometry, Galois theory, period geometry, string theory, and black-hole physics.

The audit finds a corpus with substantial theorem density but uneven external reach. Its strongest reusable assets are the all-​\(k\) weighted multiquadratic monodromy theorem, the local curvature calculus, the role-channel orbit calculus, the native period evaluator, the Kummer-wreath interface, and several large bodies of proved but unpublished work. Its principal weakness is not a shortage of results. It is that many results remain organized around narrow DBP instances, while the invariant structures connecting them—integral lattices, variations of periods, discriminant strata, vanishing cycles, and reduction functors—are not yet isolated as general theorems.

The highest-value frontier programme is therefore a staged **Arithmetic Horizon Variation Programme**:

1. identify the Kummer valuation-parity module with an explicit mod-​2 reduction of an integral intersection or vanishing-cycle lattice;
2. construct the Gauss–Manin/Picard–Fuchs transport of horizon-cover periods and compare it with the proven sheet monodromy;
3. realize collision strata by Picard–Lefschetz or quiver data and derive braid and wall transport from that realization;
4. test whether thermodynamic-curvature valuations are controlled by the same discriminant and degeneration data.

The first two stages have the best risk-adjusted frontier return. The fourth has the largest conceptual upside but must remain a conditional research target: black-hole thermodynamic curvature is known to be representation-sensitive, and curvature singularities do not universally encode critical behaviour. The report therefore separates exact mathematical targets from physical interpretations and assigns each target a minimal falsifier, a stop/go gate, and a concrete deliverable.

The recommended portfolio allocates approximately 20% of effort to immediate corpus consolidation, 45% to the parity/period bridge, 25% to collision and braid geometry, and 10% to speculative curvature/string interpretation. This both upgrades the existing papers and creates repeated opportunities for genuinely new mathematics.

---

## 1. Decision statement

The corpus should not presently invest its main effort in another broad unification paper. It should invest in **bridge theorems with finite certificates**.

The top research target is:

> **Horizon parity–intersection theorem.** Determine whether the valuation-parity matrix controlling the Kummer kernel of the horizon cover is the mod-​2 shadow of a canonical integral intersection, vanishing-cycle, or charge lattice, and prove the exact relationship when it exists.

This target is ranked first because it is simultaneously:

- close to current proof assets;
- capable of closing or materially advancing `DBP:gap:IV3`, `DBP:gap:III6`, `DBP:gap:IV7`, and `DBP:wall:IV_collision`;
- independently interesting as arithmetic geometry;
- naturally adjacent to charge lattices and BPS structures in string theory;
- falsifiable by exact rank and pairing computations;
- a prerequisite for responsibly interpreting the horizon cover as a physical charge or state network.

The second target is:

> **Horizon Gauss–Manin theorem package.** Construct the integral local system and Picard–Fuchs/Gauss–Manin transport for the relevant horizon-cover periods, and compare its monodromy representation with the proven symmetric sheet monodromy.

This is the most powerful route for joining Paper III and Paper IV. It attacks period transport, complex braid transport, Landen structure, and the distinction between permutation monodromy and homological monodromy in one coherent framework.

The third target is a collision/vanishing-cycle or quiver realization. The fourth is a discriminant-to-curvature valuation theorem. The last should not be attempted first: without the first three rungs, it risks being an analogy dressed as a bridge.

---

## 2. Scope and meaning of ROI

“ROI” here means **research return on constrained expert effort**, not financial return or a forecast of citations. It measures how much durable mathematical value a target is expected to produce relative to its cost and proof risk.

The return categories are:

1. **Gap return:** number and importance of existing DAG gaps materially advanced.
2. **Bridge return:** ability to connect previously separate mathematical arms through an exact functor, invariant, comparison theorem, or obstruction.
3. **Downstream leverage:** number of papers, tools, certificates, and future claims upgraded by the result.
4. **Evidence readiness:** proportion of definitions, exact computations, and supporting theorems already present.
5. **Falsifiability:** availability of a finite test capable of killing or sharply restricting the target before a long campaign.
6. **External reach:** relevance beyond DBP notation and the immediate corpus.

Cost and risk are scored separately. A low-cost editorial closeout may outrank a frontier theorem in raw efficiency while offering much less mathematical novelty. The portfolio therefore distinguishes:

- **support ROI** — strengthening and exposing results already substantially proved;
- **frontier ROI** — producing a new bridge or theorem not presently contained in the corpus;
- **option value** — generating reusable data even if the strongest conjecture fails.

No score in this document upgrades an open claim to a theorem.

---

## 3. Audit basis

### 3.1 Corpus scale

The paper-library ledger contains 508 inventoried artifacts. The DAG additionally admits `PAP-0509`, *Generic Symmetric Monodromy of Weighted Multiquadratic Sums*, after the ledger snapshot. The effective research corpus evaluated here therefore contains **509 artifacts**.

At the audited revision, the canonical DAG contains:

| Measure | Count |
|---|---:|
| Nodes | 2,294 |
| Edges | 4,311 |
| Theorem nodes | 1,109 |
| Formula nodes | 349 |
| Definition nodes | 502 |
| Paper nodes | 23 |
| Gap nodes | 57 |
| Explicitly tracked frontier items | 35 |
| Frontier-layer nodes | 59 |
| Ghost deliverables | 19 |
| Validation errors | 0 |
| Validation warnings | 0 |

Of the 57 gap-type nodes, some are proved or refuted boundaries retained for provenance. The live unresolved set comprises **35 explicit open gaps**, plus open ghost deliverables and conjectural walls.

### 3.2 Distribution by principal corpus arm

The artifact ledger is dominated by a few large families:

| Family | Approximate artifacts | Completed-paper artifacts | Strategic reading |
|---|---:|---:|---|
| DBP role, channel, and orbit geometry | 115 | 6 | Deep internal development; high need for invariant reformulation. |
| Cross-program and unclassified | 84 | 0 | Large bridge reservoir; weak publication identity. |
| Galois horizon and Kummer covers | 81 | 6 | Strongest present frontier-facing arm. |
| Cella residue and coupling theory | 62 | 3 | Useful categorical substrate; capstone premature. |
| Local curvature and black-hole metrics | 57 | 6 | Strong reusable calculus; physical interpretation still uneven. |
| Geometric fault localization | 51 | 0 | Several nearly publishable theorem packages hidden in campaign form. |
| DBP periods, Landen, and elliptic structure | 24 | 0 | Small but disproportionately important bridge arm. |
| Precision flow and transfer functions | 24 | 2 | Large external audience; one major manuscript ghost. |

The imbalance is important. The Galois and curvature arms already possess released papers. The period arm possesses the connective tissue needed to relate them but has no completed-paper count in the ledger category. This is a classic high-leverage bottleneck: comparatively little work in the period/lattice interface can change the interpretation of much larger bodies of work.

### 3.3 Evidence classes used in this report

This outlook distinguishes four classes:

- **Banked:** an exact theorem, proof, or machine certificate already exists.
- **Assembly:** the mathematics is banked, but the released paper or public interface is stale or incomplete.
- **Reachable frontier:** new mathematics is required, but current structure gives a bounded route and a finite falsifier.
- **Wall:** no in-hand method presently bounds the proof, or an essential representation/geometry problem remains.

This classification is more useful than “easy/hard” alone. An assembly target has excellent support ROI but little frontier novelty. A reachable-frontier target can fail yet still return valuable structure. A wall should receive only a small option allocation until an intermediate theorem lowers its risk.

---

## 4. Prospective reach of the current corpus

### 4.1 Strongest reusable assets

#### 4.1.1 Weighted multiquadratic monodromy

The strongest current general-purpose theorem is the released all-​\(k\) weighted multiquadratic monodromy paper. Its natural audience is not limited to black holes or DBP. It addresses a broad algebraic family: weighted sums of square roots, exact map degree, genus, ramification, generic full symmetric monodromy, exceptional loci, and conditional Kummer-wreath lifting.

Its prospective reach includes:

- algebraic covers and monodromy groups;
- inverse Galois and generic-polynomial questions;
- radical-sum geometry;
- arithmetic statistics of specializations;
- branched-cover models in mathematical physics;
- algorithmic certification of Kummer extensions.

This paper should be treated as a bridgehead: future work should cite its general weighted family first and recover DBP as a specialization, not present the result primarily as a black-hole calculation.

#### 4.1.2 Local curvature calculus

The local curvature calculus isolates valuation and cancellation data for Hessian or inverse-channel metrics. Its reusable content can reach:

- singular Hessian geometry;
- information and thermodynamic geometry;
- asymptotic curvature near normal-crossing divisors;
- blow-up analysis and polyhomogeneous expansions;
- black-hole state-space metrics;
- diagnostic geometry for singular statistical models.

Its chief reach limitation is interpretive. Curvature poles can be computed exactly, but their physical meaning is not universal. Existing black-hole thermodynamic geometry contains both positive examples and explicit cautions: state-space curvature is nontrivial for several black-hole families, yet its singularities need not encode critical behaviour. The corpus will gain credibility by proving local valuation theorems without overpromising a universal microscopic interpretation.

#### 4.1.3 Role-channel orbit calculus

The role-channel work contains a reusable pattern: decompose a nonlinear observable after exposing a bilinear or multilinear carrier, then track how the decomposition transforms under a finite role action and recharting. Its prospective audience includes:

- equivariant jet geometry;
- invariant decomposition of Hessian-type observables;
- representation-aware sensitivity analysis;
- geometric diagnostics in multi-channel systems;
- Lovelock and higher-curvature decompositions.

The present notation makes this arm look narrower than it is. General reach will improve when “roles” are recast as labelled factors or subrepresentations and “channels” as canonical components under an explicitly stated group action.

#### 4.1.4 Native period and Landen infrastructure

The period arm is not currently the corpus’s largest publication asset, but it has the greatest **bridge potential per artifact**. It already contains:

- a native relative-period route theorem;
- exact route and sheet semantics;
- Landen-type identities;
- a release evaluator and exact contracts;
- explicit known failures of whole-surface surjectivity;
- a live Smith-form/integral-intersection gap.

These are precisely the ingredients needed to connect analytic periods with algebraic monodromy. This arm should be upgraded from “special integral evaluation” to “relative homology, local systems, and transport.”

#### 4.1.5 Kummer and wreath-product interface

The Kummer module machinery is already general in form. It provides a clean point at which arithmetic, topology, and physical charge parity may meet. Its key reusable object is not merely a large Galois group; it is the square-class module with a computable valuation-parity certificate and a permutation action by base monodromy.

This is why the parity–intersection target ranks above another direct Galois calculation. The module is already there. The missing result is its conceptual identification.

### 4.2 Large hidden publication assets

The DAG records several ghost deliverables whose mathematical content is largely banked:

| Ghost | State | Support ROI |
|---|---|---|
| `GFL:ghost:v4_paper` | Proofs, audits, and broad verification exist; manuscript assembly missing. | Very high |
| `PFT:ghost:rf_paper` | Fourteen theorems proved; skeleton and kill-search exist; prose/IP gate remain. | Very high |
| `GR:ghost:lch_paper` | Complete scaffold, theorem, proof sketch, and 327-point table exist. | High |
| `GFL:ghost:shape_paper` | Arm ratified and certificates banked; write-up/prior-art sweep remain. | High |
| `GFL:ghost:bridge_theorem` | General-​\(n\) triangle-decomposition bridge is unwritten. | Medium-high |
| `PHO:ghost:mzi_theorem` | General theorem proved; specialization trapped in patent prose. | High |

These should not displace frontier work, but leaving them unassembled wastes reach. A small permanent publication lane can convert them into external-facing outputs without consuming the bridge programme.

### 4.3 Reach limits

The present corpus has five structural reach constraints:

1. **Instance-first exposition.** General invariants are often introduced only after DBP-specific formulas.
2. **Multiple sources of authority.** Proved results sometimes remain absent from canonical released papers.
3. **Bridge vocabulary is underdeveloped.** Period, Galois, curvature, and groupoid arms use different local languages for related transport phenomena.
4. **Physical interpretation sometimes arrives before a comparison theorem.** A mathematical resemblance is valuable evidence for a target, not evidence for equivalence.
5. **Large ghost inventory.** Significant results are invisible to a reader who encounters only completed papers.

The strategy below directly addresses these constraints.

---

## 5. External mathematical landscape and novelty boundary

The proposed bridge programme is credible because each ingredient has a strong precedent. It is potentially novel because the exact Cella-specific identifications have not been established merely by citing those precedents.

### 5.1 Periods, monodromy, and charge lattices are established bridges

Seiberg–Witten theory established a central mathematical-physics pattern: a family of algebraic curves, periods of a differential, and monodromy around singular loci encode exact low-energy information. That precedent supports studying horizon covers through periods and integral transport, but it does not imply that the DBP horizon cover is a Seiberg–Witten curve or carries the same physical theory.

Spectral networks provide a second precedent. They relate flat nonabelian connections on a surface to abelian data on a branched cover and compute BPS information through networks on that cover. This makes branched-cover transport and wall structure a serious research language rather than decorative analogy. Again, the required task is to construct the correspondence for the horizon family, not assume it.

BPS-quiver work shows that intersection-type data associated with surface triangulations can determine quivers and BPS spectra. Bridgeland–Smith and Kontsevich–Soibelman further connect differentials, stability conditions, quivers, and wall crossing. These results justify testing whether the horizon collision graph or parity matrix has a quiver/intersection realization. They do not license calling every incidence matrix a BPS quiver.

### 5.2 Arithmetic black-hole bridges already exist

Arithmetic links to black-hole attractors are not speculative in the broad sense. Gregory Moore’s arithmetic-attractor programme relates supersymmetric black-hole attractor varieties to complex multiplication, class numbers, and fields of definition in important compactifications. Strominger–Vafa derive black-hole entropy by counting BPS bound states for a class of extremal black holes. Ooguri–Strominger–Vafa conjecture a relation between BPS black-hole and topological-string partition functions.

These precedents establish that number theory, string compactification, and black-hole entropy can meet in precise models. They do **not** establish that the Cella horizon-cover Galois group counts microstates or that its Kummer rank is a physical entropy. A valid new bridge must specify the compactification or effective theory, identify charges and moduli, and prove the comparison map.

### 5.3 Higher-curvature corrections are a legitimate but secondary route

String-effective actions produce higher-derivative corrections to black-hole solutions and entropy, and modern work computes such corrections for extremal Kerr and AdS black holes. This makes the corpus’s Gauss–Lovelock channel tower relevant to string-inspired gravity.

However, the channel theorem and the physical effective action are different objects. The safe target is first an invariant decomposition theorem for Lovelock or higher-curvature entropy contributions. Only then should one test whether the decomposition aligns with a specific string-effective action and its charge/moduli data.

### 5.4 Thermodynamic curvature requires an explicit caution

Black-hole state-space curvature is an established subject, but the interpretation of its singularities is not universal. Some families exhibit curvature singularities, while other analyses show that thermodynamic Ricci-scalar singularities do not necessarily reproduce critical behaviour.

Therefore the proposed curvature–discriminant bridge has two levels:

- an exact local theorem comparing valuations of algebraically defined quantities;
- a separate physical interpretation, conditional on ensemble, potential, and model.

This distinction is a strength. It allows the mathematical theorem to survive even if a proposed physical reading fails.

### 5.5 The actual novelty target

The frontier claim is not “Galois theory, strings, and black holes are connected.” That is known in several settings.

The potentially new content is an exact package of the following form:

> For the specific weighted multiquadratic horizon-cover family, identify a canonical integral local system; compare its homological monodromy with the proven symmetric sheet monodromy; express the Kummer valuation-parity module through a mod-​2 intersection or vanishing-cycle pairing; classify collision strata through this structure; and determine whether curvature valuations factor through the same discriminant data.

Every verb in that statement demands a proof. That is precisely why it is a good programme.

---

## 6. Scoring model

Each target receives six benefit scores from 0 to 5:

- \(G\): gap coverage;
- \(B\): bridge novelty;
- \(L\): downstream leverage;
- \(E\): evidence readiness;
- \(F\): falsifiability;
- \(X\): external reach.

The weighted benefit is

\[
W = 2G + 2B + 2L + E + F + X,
\]

with maximum \(45\). Cost \(C\) and proof risk \(R\) are scored from 1 to 5. The risk-adjusted priority index is

\[
P = 100\,\frac{W}{45 + 3(C-1)+3(R-1)}.
\]

This is not a probability. It is a transparent ranking device. It penalizes cost and risk without allowing a cheap but parochial task to dominate purely through a tiny denominator.

Scores are accompanied by a target class:

- **S:** support/assembly;
- **F:** frontier;
- **W:** wall/options research.

### 6.1 Ranked portfolio

| Rank | Target | Class | G | B | L | E | F | X | C | R | Priority |
|---:|---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Immediate paper-integration and ghost-conversion sprint | S | 5 | 1 | 5 | 5 | 5 | 3 | 1 | 1 | 77.8 |
| 2 | Kummer parity as integral intersection/charge lattice | F | 4 | 5 | 5 | 4 | 5 | 4 | 3 | 3 | 71.9 |
| 3 | Horizon Gauss–Manin/Picard–Fuchs transport | F | 5 | 5 | 5 | 3 | 5 | 5 | 4 | 4 | 68.3 |
| 4 | Curvature valuation from horizon discriminant data | F/W | 4 | 5 | 5 | 4 | 5 | 5 | 4 | 4 | 66.7 |
| 5 | Collision strata as vanishing cycles/BPS-type quiver | F/W | 5 | 5 | 5 | 3 | 5 | 5 | 5 | 4 | 65.2 |
| 6 | GFL triangle-decomposition bridge and v4 paper | S/F | 3 | 3 | 4 | 5 | 4 | 3 | 2 | 2 | 62.7 |
| 7 | Role-jet holonomy plus general Lovelock channel tower | F | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 3 | 59.6 |
| 8 | Reduced common skeleton and SQG coherence | F | 4 | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 55.6 |
| 9 | String-effective higher-curvature comparison | W | 3 | 4 | 4 | 3 | 4 | 5 | 4 | 4 | 54.0 |
| 10 | Precision-flow manuscript conversion | S | 1 | 2 | 3 | 5 | 5 | 5 | 2 | 2 | 52.9 |

The support sprint ranks first numerically because it is almost pure conversion of existing value. It is not the main frontier choice. Among frontier targets, the parity/intersection theorem ranks first.

### 6.2 Sensitivity of the ranking

The ordering remains stable under reasonable changes:

- If novelty is weighted more strongly, the Gauss–Manin and collision programmes rise.
- If cost is weighted more strongly, parity/intersection rises further.
- If external reach dominates, the period-monodromy and string/attractor targets rise.
- If only immediate paper count matters, the support sprint, GFL v4, and precision-flow manuscript dominate.

The recommended portfolio deliberately mixes these objectives instead of pretending one scalar captures them all.

---

## 7. Frontier Target A — Kummer parity as an integral intersection or charge lattice

### 7.1 Research question

The current Kummer-wreath theorem controls a conjugate radical extension through square classes and a valuation-parity matrix over \(\mathbf F_2\). The period arm independently exposes an integral relative-homology problem and a Smith-form gap.

The target question is:

> Is the Kummer valuation-parity module canonically obtained from an integral intersection, boundary, or vanishing-cycle lattice after reduction modulo two?

A positive answer would explain the Kummer kernel topologically rather than merely certify it arithmetically. A negative answer would still identify the exact obstruction and prevent a false physical analogy.

### 7.2 Candidate theorem package

Let \(U\) be a regular parameter locus for the horizon-cover family, \(C_u\) the relevant smooth cover over \(u\in U\), \(D\) the divisor supporting valuations of the conjugate Kummer generators, and \(V_u\) a chosen integral relative-homology or vanishing-cycle lattice.

The desired package has four levels:

1. **Canonical lattice theorem.** Define \(V_u\) without arbitrary route or sheet choices, or prove the exact dependence on those choices.
2. **Parity comparison theorem.** Construct a natural map
   \[
   V_u/2V_u \longrightarrow \mathbf F_2^{D}
   \]
   whose image or transpose recovers the valuation-parity matrix.
3. **Rank criterion theorem.** Express maximal Kummer rank as nondegeneracy or full rank of an intersection/boundary pairing modulo two.
4. **Monodromy compatibility theorem.** Prove equivariance under the base sheet-monodromy action.

The physical “charge lattice” language should be used only after a model supplies an integral charge interpretation. Until then, “intersection lattice” is the correct term.

### 7.3 Corpus inputs

- `DBP:paper:weighted_multiquadratic_monodromy`;
- `DBP:thm:kummer_wreath_lift`;
- `DBP:gap:IV3`;
- `DBP:gap:III6`;
- `DBP:gap:IV7`;
- `DBP:wall:IV_collision`;
- `DBP:inv:PI-08` and `DBP:inv:PI-09` as correctness boundaries;
- the native relative-period evaluator and its route theorem;
- low-​\(k\) crown certificates and inertia tables.

### 7.4 Minimal falsifiers

Before a general proof attempt, compute for \(k=4,5\), and one \(k=6\) specialization:

1. the integral boundary/intersection matrix on the native image;
2. its Smith normal form;
3. its mod-​2 rank and radical;
4. the valuation-parity matrix for the Kummer generators;
5. equivariance under explicit monodromy generators.

The strong identification is falsified if ranks disagree after all declared quotients, or if no equivariant comparison exists. A rank mismatch is not a failed campaign: it would identify an additional arithmetic summand not visible to topology, itself a useful theorem target.

### 7.5 Gap return

| Gap | Expected effect |
|---|---|
| `III6` | Directly supplies the missing integral-intersection and saturation analysis. |
| `IV3` | Converts the all-​\(k\) Kummer closure from a brute rank task into a structural criterion. |
| `IV7` | Gives a lattice on which complex braid transport can act. |
| `IV_collision` | Supplies candidate vanishing cycles for higher-codimension collision strata. |
| `V2` | Provides one concrete reduced skeleton shared by period and horizon arms. |

### 7.6 ROI verdict

**Highest frontier ROI.** It is exact, finite, and close enough to current certificates to kill quickly if wrong. It also creates the mathematical object most likely to support a later string-theoretic interpretation.

---

## 8. Frontier Target B — Horizon-cover Gauss–Manin and Picard–Fuchs transport

### 8.1 Research question

Paper III studies periods and routes. Paper IV studies sheet monodromy and Kummer extensions. These are presently adjacent rather than unified.

The target is to construct the variation of the relevant homology and periods over a regular parameter locus and compare:

- permutation monodromy of sheets;
- integral monodromy on homology or relative homology;
- analytic continuation of periods;
- route-word transport in the native evaluator;
- Landen or isogeny-type transformations where present.

### 8.2 Candidate theorem package

1. **Smooth-family locus.** Define the maximal practical open set \(U\) on which the horizon curve and selected divisor pair form a smooth algebraic family.
2. **Integral local system.** Construct \(\mathcal H=R_1\pi_*\mathbf Z\) or the correct relative analogue.
3. **Gauss–Manin connection.** Give an explicit differential system for a basis of periods.
4. **Picard–Fuchs closure.** Derive scalar or matrix differential equations for the native period functions.
5. **Transport comparison.** Prove that evaluator route reversal/composition agrees with parallel transport in \(\mathcal H\).
6. **Monodromy comparison.** Give the exact homomorphism from parameter-space fundamental group to both sheet permutations and integral homology automorphisms, then state their relationship.
7. **Landen interpretation.** Determine whether the primary/dual transformation comes from an isogeny, modular correspondence, cycle change, or only an analytic identity.

### 8.3 Why this is a real bridge

The bridge does not rest on shared vocabulary. Both sides already involve analytic continuation around singular loci. A comparison theorem can therefore be written as a commuting diagram and falsified on generators.

The relevant external precedent is strong: Seiberg–Witten periods and monodromy, spectral-network abelianization on branched covers, and variations of periods in string compactifications. But the horizon family’s actual local system, differential, and physical interpretation remain to be constructed.

### 8.4 Corpus inputs

- Paper III and `DBP:gap:III1`–`III7`;
- `DBP:wall:III_landen_pd` and `DBP:wall:III_transcendence`;
- Paper IV and `DBP:gap:IV7`;
- the all-​\(k\) weighted monodromy paper;
- native period evaluator contracts;
- exact route reversal/composition work;
- low-​\(k\) branch and inertia certificates.

### 8.5 Minimal falsifiers and stop/go gates

**Gate B0 — one-parameter slice.** Select a nontrivial regular one-parameter subfamily for \(k=4\). Derive a period basis and numerical/exact monodromy around each discriminant point.

**Go condition:** evaluator continuation matches the integral transport after a declared basis and route convention.

**Stop/reframe condition:** transport closes only after enlarging the cycle space, or the native period is not a period of the proposed family/pair. In that case, the correct output is an obstruction theorem and a revised relative pair.

**Gate B1 — Picard–Fuchs order.** Determine the minimal differential system on the slice and compare its differential-Galois group with the algebraic sheet-monodromy quotient.

**Gate B2 — two-parameter braid.** Test whether the local generators satisfy the predicted braid and intersection relations.

Only after these gates should an all-​\(k\) theorem be attempted.

### 8.6 Gap return

This target directly advances `III4`, `III5`, `III7`, `IV7`, and the Landen walls. In combination with Target A it also advances `III6`, `IV3`, and `IV_collision`.

### 8.7 ROI verdict

**Largest downstream leverage and external reach.** It is more expensive than Target A, but it can transform two separate paper arms into a coherent research programme and create tools usable on arbitrary algebraic families.

---

## 9. Frontier Target C — Collision strata as vanishing cycles and quiver data

### 9.1 Research question

The Galois arm has normalized incidence, an inertia catalogue, real wall typing, and a known warning that an eliminant discriminant is not a complete ramification oracle. The missing content is a geometric realization of higher-codimension collisions and complex braid transport.

The target is:

> Associate explicit vanishing cycles and an integral or signed intersection matrix to horizon collision strata, then determine whether the resulting mutation/braid data admits a quiver or stability interpretation.

### 9.2 Candidate theorem package

1. **Codimension-one Picard–Lefschetz theorem.** Identify the vanishing cycle and transvection for every generic branch divisor type.
2. **Collision compatibility theorem.** Classify which sets of codimension-one cycles can vanish simultaneously and compute their intersection matrix.
3. **Braid presentation.** Present the image of the local braid group on homology and compare it with sheet monodromy.
4. **Quiver extraction.** Where the signed pairing is skew and satisfies the necessary conditions, define a quiver and prove independence from auxiliary choices up to mutation.
5. **Wall-crossing test.** Determine whether crossing a real or complex wall changes stable data by a known mutation or factorization law.

The word “BPS” should enter only if a physical or categorical stability condition is actually constructed. A quiver-shaped matrix alone is not a BPS spectrum.

### 9.3 External support

Spectral networks show that branched covers, wall data, and BPS degeneracies can be linked in class-​S theories. BPS-quiver constructions show that triangulated surfaces can encode spectra. Kontsevich–Soibelman provide wall-crossing structures for 3-Calabi–Yau categories. Bridgeland–Smith relate quadratic differentials to stability conditions on quiver categories.

Together these make the target plausible and supply comparison standards. They also raise the proof bar: the horizon construction must produce the appropriate differential, category, stability condition, or an honest weaker substitute.

### 9.4 Minimal falsifiers

- Compute intersection numbers for all codimension-one inertia types in the four-charge family.
- Test whether the pairing is invariant under the known sheet action.
- Check whether candidate quiver mutations reproduce computed braid transport.
- Search for collision strata whose local monodromy cannot arise from the proposed cycle configuration.

A failed quiver realization can still yield a complete Picard–Lefschetz collision theorem. That high option value justifies the target despite its risk.

### 9.5 Gap return

Primary targets are `IV7` and `IV_collision`; secondary targets are `III5`, `III6`, `V2`, and `V3`.

### 9.6 ROI verdict

**High upside, high cost.** Start only after Target A produces a candidate lattice and Target B validates monodromy on a one-parameter slice.

---

## 10. Frontier Target D — Curvature valuations from discriminant and degeneration data

### 10.1 Research question

The curvature arm computes local pole orders and cancellation behaviour. The Galois arm computes discriminant, branch, and inertia data. The ambitious bridge asks whether both are shadows of the same degeneration.

The safe target is not “Galois group determines thermodynamic curvature.” That is too coarse and generally implausible. The target is local:

> Along a declared irreducible degeneration divisor, determine whether the valuation of the thermodynamic-curvature scalar is a universal function of the local entropy jet, metric degeneracy, and horizon-cover discriminant/inertia type.

### 10.2 Candidate theorem ladder

1. **Common local parameter theorem.** Express both the horizon discriminant and metric determinant in a common normal parameter \(t\) after normalization or blow-up.
2. **Valuation comparison.** Compute
   \[
   v_t(\Delta_{\mathrm{hor}}),\qquad v_t(\det g),\qquad v_t(R[g])
   \]
   and isolate which parts are determined by leading exponents and which require front-face coefficients.
3. **Inertia-stratified normal form.** Classify curvature valuations by local inertia/collision type under explicit noncancellation hypotheses.
4. **Failure theorem.** Produce examples with identical Galois/inertia data but different curvature valuation, thereby identifying the extra jet data required.
5. **Physical interpretation.** Only for a fixed ensemble and black-hole model, compare the resulting strata with stability, response functions, or microscopic state data.

### 10.3 Why the failure theorem is valuable

The current corpus already knows that mixed front coefficients are not recoverable from the exponent matrix alone (`DBP:wall:II_front`). The most likely correct result is therefore not a pure discriminant formula. It is a **minimal-data theorem**:

\[
\text{curvature valuation}
= F(\text{discriminant order},\text{inertia type},\text{metric jet},\text{front coefficient}).
\]

Determining the smallest sufficient tuple would be a substantial reusable result even if the strongest bridge fails.

### 10.4 Minimal falsifiers

Construct pairs of exact specializations with:

- the same sheet-monodromy conjugacy class;
- the same discriminant multiplicity;
- different front-face coefficients or entropy jets.

If curvature valuations differ, pure Galois control is refuted and the theorem must include the missing jet data. If they agree across a broad exact family, proceed to a proof on the local normal form.

### 10.5 Gap return

| Gap | Expected effect |
|---|---|
| `II2` | Direct target: mixed front coefficient classification. |
| `II3` | Provides a principled curvature–valence experiment. |
| `II4` / `I5` | Forces tensor-level covariance of the local comparison. |
| `IV_collision` | Interprets collision strata through a second invariant. |
| `I4` | Supplies higher-curvature channels for the same valuation analysis. |

### 10.6 ROI verdict

**High conceptual upside, medium confidence.** Run exact falsification experiments early, but do not make this the first proof campaign. It depends on the lattice and collision geometry, and external literature requires caution about physical interpretation.

---

## 11. Frontier Target E — Role-channel holonomy and the Gauss–Lovelock/string-correction tower

### 11.1 Mathematical target

The role-channel arm already proves broad finite-order recurrence machinery, while the Gauss–Lovelock tower is verified only in low orders and a measured higher case. The target is to expose the representation-theoretic reason the split persists.

The theorem should be formulated for a labelled decomposition of the metric or curvature carrier, not only for DBP roles:

> For an invariant polynomial of degree \(k\) in curvature, derive the channel decomposition induced by a direct-sum or labelled-factor splitting, identify its representation content, and prove covariance under allowed rechartings.

The holonomy extension then asks whether higher role jets assemble into a connection or transport functor rather than an order-by-order list.

### 11.2 String-theoretic comparison

Higher-derivative corrections to black-hole entropy are a genuine string-effective phenomenon. The corpus can contribute if it first produces a clean general decomposition theorem and then applies it to a declared effective action—such as Gauss–Bonnet, Lovelock, or a specific \(\alpha'\)-corrected model.

The comparison deliverable must contain:

- the action and dimension;
- the black-hole solution or perturbative family;
- the Iyer–Wald entropy functional;
- the exact role/channel carrier;
- the order in the correction parameter;
- a statement of which pieces are invariant and which are chart/ensemble dependent.

### 11.3 Gap return

Primary targets: `I4`, `I5`, `I6`, and `II4`. Secondary targets: `II5` and the general-curvature ghost papers.

### 11.4 ROI verdict

**Good mid-tier frontier target.** It is valuable and externally legible but less likely than the parity/period programme to unify the current Galois breakthrough with the rest of the corpus.

---

## 12. Frontier Target F — Reduced common skeleton and SQG coherence

### 12.1 Current boundary

The full unreduced carrier equivalence among role, horizon, and elliptic arms is refuted. The AC-fold reduction is not faithful. Any valid unification must therefore use explicit reductions and keep their kernels visible.

This is not a defeat. It specifies the correct category-theoretic target:

> Construct reduction functors from two concrete arms into a common skeleton, compute their kernels and essential images, and prove only the coherence that survives those quotients.

### 12.2 Recommended order

Do not begin with three-way coherence (`V3`). Begin with the period and horizon arms after Targets A and B produce a shared lattice/local-system object. Then:

1. define the two reductions;
2. compute kernels;
3. prove a universal property of the common skeleton;
4. test base change and fibre products;
5. add the role-channel realization only if it meets the independence criterion `PI-12`.

### 12.3 ROI verdict

**Strategically important but downstream.** It should formalize bridges after they are constructed, not substitute category language for the missing construction.

---

## 13. Immediate support programme

Frontier work benefits from a clean published base. The following work should run as a bounded support lane.

### 13.1 Paper integration sprint

Close the assembly gaps whose mathematics is already banked:

- `I1`: reconcile the general \(n=3\) converse with the symbolic theorem;
- `I2`: write the all-finite-order induction explicitly;
- `I3`: insert the ambient-​\(n\) channel grid;
- `III1`: insert the calibrated \(\lambda\);
- `III2`: remove stale “not claimed” language;
- `III3`: insert the CCE-6 clearance lemma;
- `III4`: expose reversal and composition in the public route API;
- `IV2`: fold the all-​\(k\) base-monodromy theorem into Paper IV;
- `V1`: refresh the SQG citation.

This lane produces immediate downstream improvement with negligible theorem risk.

### 13.2 Ghost conversion order

1. `GFL:ghost:v4_paper` — pure assembly and already broadly verified.
2. `GR:ghost:lch_paper` — complete scaffold and finite data table.
3. `GFL:ghost:shape_paper` — strong banked campaign, needs prior-art sweep.
4. `PFT:ghost:rf_paper` — largest external-reach ghost, subject to its IP gate.
5. `GFL:ghost:bridge_theorem` — use the manuscript work to isolate the general-​\(n\) theorem.
6. `PHO:ghost:mzi_theorem` — extract a citable specialization without weakening patent boundaries.

### 13.3 Why support work belongs in the frontier portfolio

Every new bridge will depend on stable theorem citations. If the corpus leaves proof authority scattered across campaign files, a future paper must spend pages re-establishing provenance rather than developing new mathematics. A 20% support allocation is therefore infrastructure, not distraction.

---

## 14. Recommended integrated programme: Arithmetic Horizon Variation

### 14.1 Programme thesis

The most promising reusable object in the corpus is not the black-hole formula itself. It is the **family of branched algebraic covers together with its integral, mod-​2, analytic, and singular geometric data**.

The programme should organize the following layers:

| Layer | Object | Existing strength | Missing comparison |
|---|---|---|---|
| Algebraic | weighted multiquadratic horizon cover | exact degree, genus, ramification, generic \(S_d\) | relation to homological monodromy |
| Arithmetic | Kummer square-class module | exact conditional wreath criterion | relation to integral/mod-​2 lattice |
| Topological | relative homology and routes | native route theorem, obstruction to whole-surface claim | canonical lattice and full transport |
| Analytic | period functions | evaluator, Landen identities | Picard–Fuchs/Gauss–Manin system |
| Singular | collision and inertia strata | normalized incidence and inertia catalogue | vanishing cycles and braid action |
| Geometric | thermodynamic metric curvature | local valuation calculus | minimal data shared with discriminant strata |
| Physical | black-hole/string interpretation | authentic black-hole origin and external precedents | explicit charge/moduli/effective-theory map |

The research value comes from proving vertical maps between adjacent layers. Attempting to jump from the algebraic layer directly to the physical layer is the least reliable route.

### 14.2 Central conjecture ladder

The programme may be guided by the following conjectures, each strictly weaker than the next.

#### Conjecture AHV-1 — parity realization

For the regular horizon-cover family, the conjugate valuation-parity module is an equivariant quotient or subquotient of the mod-​2 reduction of a canonical relative-homology or vanishing-cycle lattice.

#### Conjecture AHV-2 — transport compatibility

The native relative-period route action agrees, after an explicit basis choice and quotient, with Gauss–Manin parallel transport on the lattice from AHV-1.

#### Conjecture AHV-3 — collision control

Generic collision inertia is induced by Picard–Lefschetz transformations on the same lattice, and higher-codimension realizability is characterized by the intersection pattern of simultaneously vanishing cycles.

#### Conjecture AHV-4 — minimal curvature data

On a declared regular degeneration stratum, the curvature valuation is determined by the discriminant/inertia type together with a finite metric-jet and front-coefficient datum.

#### Conjecture AHV-5 — physical charge interpretation

In a specified string-effective or supergravity model, the lattice or a controlled quotient embeds into the physical charge lattice, and a declared subset of its period/monodromy data controls a black-hole observable.

AHV-5 must not be used to justify AHV-1–4. The proof direction runs upward from exact geometry.

### 14.3 Discovery value under failure

| Conjecture outcome | Durable result still obtained |
|---|---|
| AHV-1 false | Exact mismatch theorem separating arithmetic square classes from topology. |
| AHV-2 false | Obstruction identifying missing cycles, coefficients, or route data. |
| AHV-3 false | Collision catalogue showing which inertia patterns are not Picard–Lefschetz. |
| AHV-4 false in strong form | Minimal counterexample pair and enlarged sufficient-data theorem. |
| AHV-5 false | Clean separation of mathematical cover invariants from physical charge data. |

This is why the programme has strong research ROI. Its intermediate failures are publishable structural boundaries rather than dead ends.

---

## 15. Execution portfolio

### 15.1 Allocation

| Workstream | Allocation | Purpose |
|---|---:|---|
| Corpus consolidation and ghost conversion | 20% | Stabilize proof authority and release banked value. |
| Parity/intersection and low-​\(k\) exact lattice work | 25% | Highest frontier ROI; finite falsifiers. |
| Gauss–Manin/Picard–Fuchs transport | 20% | Main Paper III–IV bridge. |
| Collision/vanishing-cycle geometry | 15% | Unlock braid transport and higher strata. |
| Curvature/discriminant comparison | 10% | High-upside exact experiments and minimal-data theorem. |
| Higher-curvature/string and SQG options | 10% | Maintain option value without consuming the core programme. |

### 15.2 Phase 0 — foundation closeout

**Goal:** remove stale released-paper boundaries and prepare exact inputs.

Deliverables:

- Paper III updated with CCE-5 and CCE-6;
- Paper IV updated with the all-​\(k\) weighted theorem;
- public route reversal/composition API;
- a single declared \(k=4\) and \(k=5\) benchmark family for all bridge tests;
- a canonical notation crosswalk: sheet, route, cycle, divisor, valuation, and role.

Exit gate: every later campaign cites a released proof authority and the benchmark families have exact reproducible certificates.

### 15.3 Phase 1 — parity and lattice probe

Deliverables:

- integral chain/relative-homology basis for benchmark families;
- Smith normal forms;
- mod-​2 intersection and boundary matrices;
- valuation-parity matrices;
- exact equivariance tests;
- verdict on AHV-1 for \(k=4,5\).

Exit gate: either a proved low-​\(k\) comparison or a precise mismatch theorem.

### 15.4 Phase 2 — one-parameter period transport

Deliverables:

- smooth one-parameter horizon family;
- period basis and differential system;
- singular-point and local-exponent table;
- analytic and integral monodromy matrices;
- evaluator-route comparison;
- differential-Galois versus sheet-Galois comparison.

Exit gate: a commuting transport diagram on explicit generators.

### 15.5 Phase 3 — collision and braid geometry

Deliverables:

- codimension-one vanishing-cycle catalogue;
- higher-collision realizability table;
- braid-group presentation on homology;
- quiver/mutation verdict;
- proof or counterexample for AHV-3 in the four-charge family.

Exit gate: `IV7` closed or reduced to a single named obstruction; `IV_collision` reclassified with exact evidence.

### 15.6 Phase 4 — curvature comparison

Deliverables:

- common local parameters for selected degeneration strata;
- exact valuation tuples \((v(\Delta),v(\det g),v(R))\);
- same-inertia/different-jet counterexample search;
- minimal-data theorem or refutation;
- second-surface realization for the local curvature calculus.

Exit gate: a theorem whose mathematical statement does not depend on speculative microscopic physics.

### 15.7 Phase 5 — physical model selection

Only after Phases 1–4 should the programme choose a string or supergravity model. Selection criteria:

1. the horizon-cover family must arise from or map naturally into the model;
2. charge and moduli spaces must be explicit;
3. periods or central charges must be computable;
4. the relevant entropy/curvature observable must be defined in a fixed ensemble;
5. the comparison must produce a falsifiable numerical or algebraic statement.

The likely first candidates are an extremal or near-extremal family with a tractable attractor mechanism, or a higher-derivative model where the entropy functional is explicit. A generic “string theory” label is not a model.

---

## 16. Research outputs and publication architecture

### 16.1 Core paper sequence

#### Paper A — Parity Lattices of Multiquadratic Horizon Covers

Minimum result: low-​\(k\) exact comparison plus general obstruction/criterion.  
Strong result: all-​\(k\) equivariant parity–intersection theorem.  
Audience: arithmetic geometry, algebraic topology, Galois modules.

#### Paper B — Gauss–Manin Transport for Weighted Multiquadratic Horizon Periods

Minimum result: one-parameter Picard–Fuchs system and monodromy.  
Strong result: multi-parameter local system, route comparison, and all-​\(k\) structure.  
Audience: algebraic geometry, special functions, mathematical physics.

#### Paper C — Collision Inertia, Vanishing Cycles, and Braid Transport

Minimum result: codimension-one Picard–Lefschetz catalogue.  
Strong result: higher-collision classification and quiver/stability realization.  
Audience: singularity theory, braid groups, representation theory, mathematical physics.

#### Paper D — Discriminant-Stratified Curvature Valuations

Minimum result: counterexamples to pure discriminant control and a minimal-data formula.  
Strong result: inertia-stratified normal-form theorem with applications to black-hole state spaces.  
Audience: singular differential geometry, thermodynamic geometry, general relativity.

#### Paper E — Arithmetic Horizon Variation in a Specified String Model

This paper is conditional. It should be written only after an explicit physical comparison is proved.  
Audience: string theory, black-hole microphysics, arithmetic geometry.

### 16.2 Supporting releases

- revised Paper III;
- revised Paper IV;
- GFL decomposition v4;
- lifted-compatibility singularity paper;
- precision-flow manuscript;
- a reusable exact lattice/monodromy software and certificate package.

### 16.3 Generalization rule for every paper

Each paper should be written in the following order:

1. abstract family and invariant;
2. exact theorem;
3. proof;
4. finite certificate or falsifier;
5. DBP/horizon specialization;
6. physical interpretation, if any;
7. explicit nonclaims.

This reverses the narrowness problem without erasing the motivating cases.

---

## 17. Targets not recommended as primary investments

### 17.1 Full unreduced role/horizon/elliptic equivalence

This is refuted by fibre, dimension, isotropy, and monodromy mismatches. Pursuing it would ignore a proved boundary. Work only with explicit reductions and visible kernels.

### 17.2 Immediate three-way SQG coherence

The shared object has not yet been constructed. Category language cannot supply the missing lattice or transport theorem. Defer until the two-arm horizon/period reduction is real.

### 17.3 Transcendence of special values as the first period target

Transcendence has high prestige but poor present tractability and weak gap coverage relative to Gauss–Manin transport. First derive the differential system, monodromy, and cycle comparison; they may reveal the correct arithmetic target.

### 17.4 General singular-strata classification for role calculus

This is a genuine wall. It should receive option work only after tensor covariance and the general mixed-bidegree representation are understood.

### 17.5 Physical microstate claims from Galois-group order

No current theorem identifies the order of the horizon Galois group or Kummer kernel with black-hole entropy or microstate count. Such a claim should be treated as unsupported until a physical Hilbert space, charge lattice, and counting map are constructed.

### 17.6 Curvature singularity as a universal phase-transition oracle

External black-hole thermodynamic geometry gives countervailing evidence. The corpus should prove local curvature statements and make ensemble-specific interpretations only.

---

## 18. Bridge-discovery protocol for future work

The corpus’s strongest discoveries have come from recognizing structural analogies. To convert that talent into a reliable frontier engine, every proposed bridge should pass the following protocol.

### Step 1 — object match

List the objects on both sides with types:

- set, scheme, manifold, stack, group, module, category, local system, differential equation, or physical state space.

If the types differ, name the functor or reduction needed to compare them.

### Step 2 — invariant match

Identify the exact invariant on each side:

- rank, discriminant, monodromy, intersection form, period, curvature valuation, entropy, or stability index.

Shared words are not invariant matches.

### Step 3 — comparison map

Write the proposed map and its domain/codomain. State whether it is expected to be injective, surjective, faithful, full, equivariant, or only numerical.

### Step 4 — commuting test

Choose at least one operation—transport, specialization, base change, quotient, braid, or degeneration—and demand a commuting diagram.

### Step 5 — minimal falsifier

Find the smallest exact case that can refute the map. Prefer rank, parity, determinant, or monodromy-generator mismatches over large numerical scans.

### Step 6 — kernel and loss ledger

If a reduction is involved, record what is forgotten. A bridge that loses even winding, orientation, or sheet data can still be useful, but it is not an equivalence.

### Step 7 — physical interpretation gate

For physics claims, name the model, ensemble, observable, and approximation order. Do not transfer interpretation solely through formal resemblance.

### Step 8 — general theorem extraction

Write the strongest theorem for the abstract family before the motivating specialization.

This protocol should become the standard campaign template for bridge research.

---

## 19. Success metrics

### 19.1 Twelve-month mathematical metrics

A successful programme should achieve at least four of the following:

- one exact parity/intersection theorem or mismatch theorem;
- one explicit Picard–Fuchs system with certified monodromy;
- closure or sharp reduction of `III5`, `III6`, `IV3`, and `IV7`;
- one collision/vanishing-cycle classification;
- one discriminant/curvature minimal-data theorem;
- Paper III and Paper IV integrated with already proved successors;
- three major ghost manuscripts converted into released papers;
- one reusable software/certificate package for lattice and monodromy computation;
- one externally legible paper whose main theorem does not require DBP notation.

### 19.2 Frontier success

The strongest outcome is not a sweeping narrative. It is a new commuting structure connecting at least three of:

\[
\text{square classes}
\longleftrightarrow
\text{integral cycles}
\longleftrightarrow
\text{period transport}
\longleftrightarrow
\text{collision monodromy}
\longleftrightarrow
\text{curvature valuations}.
\]

If that structure then embeds into a specified string-theoretic charge/period system, the corpus will have produced a genuine Galois–string–black-hole bridge rather than a thematic juxtaposition.

### 19.3 Stop conditions

Pause or reframe a workstream when:

- two benchmark ranks disagree with the proposed identification;
- route transport cannot be made functorial after declaring all sheet/orientation data;
- collision monodromy violates the proposed Picard–Lefschetz presentation;
- curvature valuation changes while every proposed controlling datum is fixed;
- a physical interpretation requires an unspecified compactification or ensemble;
- a reduction’s kernel destroys the invariant the bridge was meant to preserve.

Stop conditions are part of ROI. They prevent a beautiful analogy from becoming a long, expensive non-theorem.

---

## 20. Final recommendation

The corpus is ready for a frontier programme, but the frontier is not another isolated black-hole formula. The frontier is the invariant geometry of the horizon-cover family.

The recommended order is:

1. **Run the support sprint** to integrate banked results into Papers I, III, and IV and convert the strongest ghost manuscripts.
2. **Open the parity/intersection campaign** with exact \(k=4,5,6\) rank and equivariance tests.
3. **Build the one-parameter Gauss–Manin/Picard–Fuchs model** and prove transport compatibility.
4. **Use the resulting lattice to classify collision and braid geometry.**
5. **Test the curvature/discriminant bridge through counterexample-first exact experiments.**
6. **Only then select a concrete string/supergravity model** and attempt a physical charge or attractor interpretation.

The first “gem” to hunt is therefore the parity–intersection theorem. It is close enough to be real, deep enough to reorganize the corpus, and general enough to survive even if every proposed black-hole interpretation is later removed. That is the correct standard for frontier mathematics.

---

## 21. Primary literature anchors

The following sources are used as mechanism precedents, not as evidence that the proposed Cella-specific bridges are already proved.

1. N. Seiberg and E. Witten, [*Electric-Magnetic Duality, Monopole Condensation, and Confinement in N=2 Supersymmetric Yang–Mills Theory*](https://arxiv.org/abs/hep-th/9407087).
2. D. Gaiotto, G. W. Moore, and A. Neitzke, [*Spectral Networks*](https://arxiv.org/abs/1204.4824).
3. M. Alim, S. Cecotti, C. Cordova, S. Espahbodi, A. Rastogi, and C. Vafa, [*BPS Quivers and Spectra of Complete N=2 Quantum Field Theories*](https://arxiv.org/abs/1109.4941).
4. T. Bridgeland and I. Smith, [*Quadratic Differentials as Stability Conditions*](https://arxiv.org/abs/1302.7030).
5. M. Kontsevich and Y. Soibelman, [*Stability Structures, Motivic Donaldson–Thomas Invariants and Cluster Transformations*](https://arxiv.org/abs/0811.2435).
6. F. Denef, [*Supergravity Flows and D-Brane Stability*](https://arxiv.org/abs/hep-th/0005049).
7. A. Strominger and C. Vafa, [*Microscopic Origin of the Bekenstein–Hawking Entropy*](https://arxiv.org/abs/hep-th/9601029).
8. G. Moore, [*Arithmetic and Attractors*](https://arxiv.org/abs/hep-th/9807087).
9. H. Ooguri, A. Strominger, and C. Vafa, [*Black Hole Attractors and the Topological String*](https://arxiv.org/abs/hep-th/0405146).
10. J. Åman, I. Bengtsson, and N. Pidokrajt, [*Geometry of Black Hole Thermodynamics*](https://arxiv.org/abs/gr-qc/0304015).
11. B. P. Dolan, [*The Intrinsic Curvature of Thermodynamic Potentials for Black Holes with Critical Points*](https://arxiv.org/abs/1504.02951).
12. P. A. Cano and M. David, [*The Extremal Kerr Entropy in Higher-Derivative Gravities*](https://arxiv.org/abs/2303.13286).
13. A. Giveon, D. Gorbonos, and M. Stern, [*Fundamental Strings and Higher Derivative Corrections to d-Dimensional Black Holes*](https://arxiv.org/abs/0909.5264).

---

## 22. Corpus handles

### Core papers

- `DBP:paper:I` — *Active Role-Jet Orbit Calculus*.
- `DBP:paper:III` — *DBP Curvature Periods of the DBP Quadric*.
- `DBP:paper:IV` — *Galois Theory of the Horizon Cover*.
- `DBP:paper:weighted_multiquadratic_monodromy` — *Generic Symmetric Monodromy of Weighted Multiquadratic Sums*.
- `DBP:paper:V` — selected quotient groupoids, held capstone.

### Highest-priority live gaps

- `DBP:gap:III5` — full regular-plane relative-transport groupoid.
- `DBP:gap:III6` — Smith form/integral intersection of the native inclusion.
- `DBP:gap:III7` — generic DAG analytic evaluator semantics.
- `DBP:gap:IV3` — all-​\(k\) Kummer/crown wreath closure.
- `DBP:gap:IV7` — generic complex braid/wall transport.
- `DBP:wall:IV_collision` — higher-codimension collision realization.
- `DBP:gap:II2` — mixed front-face coefficient classification.
- `DBP:gap:I4` — general Gauss–Lovelock channel tower.
- `DBP:gap:I5` / `DBP:gap:II4` — tensor-level rechart covariance.
- `DBP:gap:V2` — two-arm reduction into a common skeleton.

### Correctness boundaries

- `DBP:wall:III_wholesurface` — whole-surface native-image claim refuted.
- `DBP:wall:IV_eliminant` — eliminant discriminant is not a complete ramification oracle.
- `DBP:wall:II_front` — exponent matrix alone does not determine mixed front coefficient.
- `DBP:wall:V_carrier` — unreduced full-carrier equivalence refuted.
- `DBP:wall:V_faithful` — AC-fold reduction not faithful.
- `DBP:inv:PI-08`, `PI-09`, and `PI-12` — integral obstruction, native-image, and independence requirements.

---

## 23. Claim boundary

This report demonstrates a corpus audit and a risk-adjusted research prioritization. It does not prove AHV-1 through AHV-5, does not identify the current horizon cover with a Seiberg–Witten or spectral curve, does not establish a BPS quiver, does not derive black-hole microstate counts from a Galois group, and does not assert that thermodynamic curvature universally detects physical criticality.

Its strongest positive conclusion is strategic and evidence-backed:

> The current corpus has enough exact algebraic, arithmetic, analytic, and local-geometric structure to support a staged bridge programme. The parity/intersection and Gauss–Manin targets offer the best combination of tractability, gap coverage, external relevance, and option value.
