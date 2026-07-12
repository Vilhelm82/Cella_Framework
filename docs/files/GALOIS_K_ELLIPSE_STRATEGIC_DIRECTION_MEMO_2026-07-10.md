# Galois–k-Ellipse Horizon Program — Strategic Direction Memo

**Date:** 2026-07-10  
**Status:** Research decision memo. It records a recommended programme and proposed theorem targets; it does **not** promote any evidence row or alter the Mathematical Object Emergence Ledger.

**Source state:** `MATHEMATICAL_OBJECT_EMERGENCE_LEDGER_v0_5.md` and `GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6.md`, together with the current axial-cover, entropy-field, DBP, and Cella records.

---

## 1. Executive decision

The programme should now be organised around one classical mathematical spine:

> **Galois and ramification of Kummer-decorated axial k-ellipse covers.**

The immediate prize is **not** declaring a new autonomous mathematical field, extending precision-flow, or forcing DBP, Cella, and horizon geometry into one manuscript. The prize is to determine the exact closure group of the ordered-horizon tower, identify its inertia generators geometrically, and then study how that tower deforms under rotation and higher charge number.

There are three distinct kinds of work already present:

1. A substantial, bankable theorem package on axial k-ellipses, descent, total reality, spectral selection, and entropy fields.
2. A high-ceiling research programme: closure monodromy, Kummer rank, and ramification of the horizon tower.
3. Supporting systems: Cella as a certificate-producing computational consumer; DBP local geometry as a possible local normal-form engine; the emergence ledger as evidence-only governance.

The second is the main discovery programme. The first should be closed and written cleanly. The third should support the mathematics without being allowed to choose the mathematics.

---

## 2. The central spine

For the four-charge axial norm, let

```text
F  = observable field,
K  = F(u) = F(gamma),
E  = Galois closure of K/F,
Gal(E/F) = S_5.
```

Let `u_1,...,u_5` and `gamma_1,...,gamma_5` denote the conjugates in `E` of the mass-square and entropy-sum elements. The normal closure of the static ordered-horizon field is

```text
H~_0 = E(sqrt(u_1),...,sqrt(u_5), sqrt(gamma_1),...,sqrt(gamma_5)).
```

Therefore the exact closure group must fit into

```text
1 -> (C_2)^r -> Gal(H~_0/F) -> S_5 -> 1,       r <= 10,
```

and admits the natural Kummer-tower embedding

```text
Gal(H~_0/F) -> V_4 wr S_5 = (C_2^2)^5 semidirect S_5.
```

The **headline open theorem** is to determine `r` and the resulting group exactly.

This is sharper than saying "the base is S_5 and the local top is V_4." Those two facts supply only an upper bound. They do not establish a full wreath product. Equality requires a proof that all conjugate Kummer classes have the necessary independence.

If `r = 10`, the group is the full `V_4 wr S_5`. If relations occur, the relations identify the true `S_5`-stable Kummer module and hence the exact proper subgroup. Either outcome is mathematically informative.

### Why this is the programme's natural unifier

```text
axial k-ellipse degree and pencil
            |
            v
base mass cover N_k(u) = 0
            |
       discriminant / wall divisors
            |
            v
base monodromy G_k
            |
       Kummer classes of horizon data
            |
            v
ordered-horizon closure group and inertia
            |
       physical chamber / selected real section
            |
            v
certified computation and thermodynamic interpretation
```

This absorbs R9, R12, R18, the degree-20 crown, field reconstruction, wall norms, and physical-sheet isolation into one theorem programme.

---

## 3. Main proof route for closure monodromy

### 3.1 Establish the Kummer rank

Work in `E^*/E^{*2}` with the ten classes

```text
[u_1],...,[u_5], [gamma_1],...,[gamma_5].
```

Construct the mod-2 valuation matrix of these classes on the relevant prime divisors. The expected divisor families are:

- pullbacks of the signed axial-contact / `u_i = 0` divisors;
- pullbacks of the entropy-branching / `gamma_i = 0` divisors;
- the mass-fibre discriminant strata, which give the base `S_5` braid data;
- their intersections and exceptional loci, treated separately rather than silently discarded.

An odd valuation on a divisor that is absent from the other columns certifies a new square class. A full-rank matrix proves `r = 10`. A rank defect produces the relation that must be built into the group statement.

### 3.2 Determine inertia and generation

For every generic codimension-one divisor, record:

| Divisor type | Local question | Global role |
|---|---|---|
| signed axial contact | Which square root flips? | Kummer kernel generator |
| entropy branching | Which entropy radical flips? | Kummer kernel generator |
| mass-sheet collision | Which roots exchange? | Base `S_5` branch cycle |
| critical-sheet component | What local cycle occurs off chamber? | Additional global discriminant data |

The physical strict chamber is unramified and selects the least positive real root. It should be treated as a distinguished real section of this global cover, not as evidence that the global monodromy is small.

### 3.3 Alternative certificate route

A carefully chosen good rational specialization can provide an independent route. If a specialized closure group reaches the full permitted upper bound, then—after recording good-specialization hypotheses—it forces generic maximality. This is useful as a certificate, but it does not replace the generic divisor/Kummer explanation.

### 3.4 Non-negotiable stop rule

Do not assert a full wreath product merely from the `S_5` base group, the local `V_4` extension, distinct labels, or numerical continuation. The missing point is independent kernel generation. The corrected self-glue lessons are directly relevant here.

---

## 4. High-value new direction: rotation as a Kummer-rank deformation

The current map treats rotation as difficult because the spectral-selection problem becomes indefinite. That is correct for the **selection** side, but it should not obscure a much more tractable algebraic field-theory problem.

Use normalized entropies

```text
y_J = (S_+ + S_-)/pi,
z_J = (S_+ - S_-)/pi.
```

The four-charge rotating entropy formula gives an entropy sum independent of `J`, hence

```text
y_J^2 = gamma.
```

The universal area product is

```text
S_+ S_- = pi^2 (P + 4 J^2),
```

where `P = N_1 N_2 N_3 N_4` in the program's normalisation. Therefore

```text
z_J^2 = gamma - 4P - 16J^2 =: delta_J.
```

This suggests the rotating ordered-horizon field

```text
H_J = K(J)(sqrt(gamma), sqrt(delta_J)).
```

### Candidate theorem: Kummer-rank jump under generic rotation

This is a **proposed theorem target**, not yet a promoted result.

At `J = 0`, the static identity

```text
gamma (gamma - 4P) = 4u beta^2
```

gives

```text
[delta_0] = [u] + [gamma]  in K^*/K^{*2}.
```

Assume the existing static square-class independence of `[u]` and `[gamma]`. Over the generic `J`-extended field, `delta_J = delta_0 - 16J^2` is an irreducible quadratic in `J`, because `delta_0` is nonsquare. Its own prime divisor has odd valuation while the constant classes `[u]` and `[gamma]` have valuation zero there. This supplies a short Kummer argument that

```text
[u], [gamma], [delta_J]
```

are independent generically. The expected consequences are

```text
[K(J)(sqrt(u), sqrt(gamma), sqrt(delta_J)) : K(J)] = 8,
[H_J : K(J)] = 4,
[H_J : F(J)] = 20,
```

with the combined seed-plus-horizon field generically of degree `40` over the observable base, while the static specialization has only rank two and degree `20`.

This is a clean **Kummer-rank-drop specialization** at `J = 0`:

```text
static:   [delta_0] = [u] + [gamma],
rotating: [delta_J] is a new J-dependent class.
```

### Required proof checks

- Fix the exact rotating observable field and normalisation once.
- Prove the displayed entropy identities directly from the Cvetic–Youm parametrization.
- State the generic exclusions: characteristic not two, nonzero area product, nondegenerate horizon pair, and the existing static square-class gate.
- Separate the entropy-only field from the combined seed-plus-entropy field.
- Do not infer rotating total reality or a rotating least-root spectral rule from this algebraic theorem.

### Research consequence

Split R13 into two fronts:

| Front | Question | Status / role |
|---|---|---|
| R13a | Rotating Kummer field, rank jump, and closure group | Ripe algebraic theorem target |
| R13b | Rotating physical selection and indefinite spectral geometry | High-risk extension; defer until R13a is closed |

The rotating closure of the combined field would then naturally sit inside

```text
(C_2^3) wr S_5,
```

with a Kummer-rank comparison between the static and rotating towers. This is a credible route from one four-charge example to a deformation theory of horizon covers.

---

## 5. Higher-charge programme: use k = 5 as a discriminator

For the axial `k`-ellipse norm, let

```text
d_k = deg_u N_k.
```

The known degree law gives `d_5 = 16`. The first higher-charge experiment should be a fully certified generic-looking strict-chamber specialization of `N_5`.

The question is not merely whether the specialization is irreducible. Determine its Galois group.

| Outcome at k = 5 | What it means | Next programme |
|---|---|---|
| Full `S_16` | Strong evidence for a generic symmetric-group family | Formulate and prove an all-`k` monodromy theorem |
| Proper structured subgroup | Hidden sign/pencil symmetry survives elimination | Classify the resulting family; this may be the more interesting outcome |
| Degenerate specialization | Poor test point | Replace it; do not generalize from it |

Do not begin with an all-`k` proof. A certified `k = 5` group is a bounded, high-information experiment that determines what the general theorem should be.

---

## 6. Priority order

| Work item | Discovery ceiling | Readiness | Decision |
|---|---:|---:|---|
| Degree-20 crown certificate | Moderate, but unlocks everything | Immediate | Close first |
| Rotating Kummer-rank lemma | Very high | High | Write next |
| Static closure monodromy (R9) | Highest expected value | Medium-high | Main campaign |
| Discriminant / inertia stratification (R12) | High | Medium-high | Proof engine for R9 |
| `k = 5` degree-16 group | Very high | Medium | Bounded discriminator |
| Certified spectral selector in Cella | Moderate mathematical novelty; high credibility | High | Supporting consumer |
| DBP curvature of cover divisors (R15) | Conditional | Low-medium | Only if it predicts inertia |
| CAND-001 objecthood gates | Uncertain | Low | Maintenance mode, not a work queue |
| Indefinite rotating selection | Extreme ceiling; extreme risk | Low | Moonshot after R13a |

---

## 7. Proposed paper architecture

### Paper I — the bankable theorem package

**Working scope:** axial `k`-ellipse horizon fibres: degree, descent, total reality, spectral selection, and entropy fields.

Include the established core:

- axial `k`-ellipse identification and degree law;
- generic four-charge `S_5` core;
- incidence normalization and reflection descent;
- definite-pencil chamber theorem, total reality, least-root selection, simplicity, and sensitivity;
- ordered-horizon reconstruction and the degree-20 theorem once its certificate gate is closed;
- ramification parity and the signed-versus-physical wall distinction.

Do **not** make this paper carry Cella architecture, the abstract object-emergence claim, full closure monodromy, or an unproved DBP unification.

### Paper II — the main discovery paper

**Working scope:** Kummer closures and ramification of four-charge horizon fields.

Include:

- the `V_4 wr S_5` upper bound;
- Kummer-rank/valuation proof;
- exact closure group and inertia table;
- discriminant strata and branch-cycle generation;
- rotating Kummer-rank jump and its specialization at `J = 0`.

### Paper III — only after the k = 5 discriminator

**Working scope:** generic Galois groups of axial `k`-ellipse norms.

Its form depends on the `k = 5` result: either an all-`k` symmetric-group theorem or a classification of a structured family.

### Computational companion

Use Cella to certify the extremal generalized eigenvalue and return a rational enclosure for

```text
u_phys = lambda_max^{-2},
```

or a typed refusal. It is a named consumer of an established theorem, not the conceptual centre of the programme.

---

## 8. DBP and Cella: the correct roles

### DBP / active recharting

There is one legitimate unification test:

```text
local recharting-orbit or valuation normal form
        -> local ramification index / inertia conjugacy class
        -> branch-cycle generator
        -> global closure monodromy.
```

The falsifiable question is:

> Does the active-recharting orbit of a generic discriminant germ determine the local inertia conjugacy class?

If yes, prove that map. It would be a real local-to-global theorem and a substantive reason to unite the DBP calculus with the Galois cover work. If no, keep the local curvature calculus as its own mathematically legitimate programme. Shared involutions, labels, or aesthetic resemblance do not establish a common theory.

### Cella

Cella is best deployed as a certificate layer:

- exact/rational interval enclosure of the extremal generalized eigenvalue;
- certified sign and branch-selection decisions;
- condition/sensitivity studies near wall or collision strata;
- typed refusal when the theorem's hypotheses do not warrant a verdict.

It should not be asked to discover the closure group, and the precision-flow record should not be made a new central realization. Its lasting contribution here is the X/Y correction: a state cover and an output-selection map must be kept distinct.

---

## 9. What should be paused or protected

### Keep CAND-001 at S2

The current ledger judgment is right. The candidate cover–chamber descent system has real recurring structure, but no native morphisms and no faithful third realization. Do not spend the next research phase inventing a category merely to satisfy its own gate.

The ledger remains evidence-only. It may record consequences of the closure and rotation work, but it must not choose the research queue.

### Do not over-import generic k-ellipse singularity results

The Jiang–Han work is an essential external anchor for generic planar k-ellipses, but it explicitly assumes generic non-collinear foci. The axial family is collinear, so the programme's discriminant and ramification analysis remains a specialized task.

### Do not let the self-glue draft supply unverified fullness

Its per-cover and layer distinctions are useful methodological lessons. Its general wreath assertions require the independent-kernel and exceptional-divisor proofs demanded by the current unification proof-stop ledger.

### Do not claim a new autonomous field yet

The current mathematical achievement is already substantial without that claim. A standalone field becomes warranted only if the closure/rotation/higher-`k` programme yields intrinsic morphisms, classifications, or examples not naturally representable as marked real algebraic covers with Kummer data.

---

## 10. Immediate sequence

1. **Close the degree-20 crown certificate.** Reconcile the research-map prose so generic degree-20 status is stated uniformly and the certificate is archived.
2. **Write the rotating Kummer lemma.** Treat it as a short, formal theorem note with every field and square-class hypothesis explicit.
3. **Build the static closure proof dossier.** Define `E`, list the ten classes, freeze the divisor register, and state the exact Kummer-rank proposition to be proved.
4. **Run the `k = 5` certified Galois experiment.** Use it to choose between an all-`k` symmetric-group programme and a structured-subgroup programme.
5. **Only then build the Cella consumer.** The target is a certified spectral-selection artifact, not another exploratory campaign.

After Steps 1–3, the external mathematical ask becomes precise enough for a focused arithmetic-geometry or computational-Galois review: verify the Kummer-rank/fullness argument, not the whole corpus at once.

---

## 11. External anchors and scope ceilings

- Nie, Parrilo, and Sturmfels, *Semidefinite Representation of the k-Ellipse*, arXiv:math/0702005. Licenses the planar degree law and symmetric determinantal representation; it does not supply horizon semantics or the closure group.
- Barquero-Sanchez and Calvo-Monge, *On the embedding of Galois groups into wreath products*, arXiv:2306.14386. Licenses the relevant Kummer/wreath embedding; it does not prove fullness in this tower.
- Jiang and Han, *Singularities and Genus of the k-Ellipse*, arXiv:1908.01414. Licenses generic planar k-ellipse singularity context; its generic non-collinearity hypothesis does not settle the axial specialization.
- Cvetic and Youm, *Entropy of Non-Extreme Charged Rotating Black Holes in String Theory*, hep-th/9603147. Source for the rotating four-charge entropy parametrization.
- Cvetic, Gibbons, and Pope, *Universal Area Product Formulae for Rotating and Charged Black Holes in Four and Higher Dimensions*, arXiv:1011.0008. Source for the universal rotating area-product structure.

---

## 12. Bottom line

The strongest next identity is not a new label. It is a theorem programme:

```text
axial k-ellipse monodromy
    + Kummer horizon lifts
    + ramification divisors and inertia
    + static-to-rotating Kummer-rank deformation.
```

Close the degree-20 gate, formalize the rotating rank-jump theorem, and make exact closure monodromy the principal target. That is the direction with the best combination of mathematical coherence, discovery potential, and leverage over the existing corpus.

