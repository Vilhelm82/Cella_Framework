# Toward a Geometric Theory of Coupling Dynamics: Current Results, Open Questions, and the Search for Field Equations on Constraint Surfaces

**William Lloyd**

Coffs Harbour, New South Wales, Australia

**Date:** April 2026

---

## Abstract

The Lloyd Framework diagnoses coupling degradation in multi-variable physical systems by computing the intrinsic geometry of their constraint surfaces. Over a concentrated period of development and validation, the framework has produced a sequence of results that appear to be converging on something larger than any individual finding. A curvature decomposition separates coupling geometry from individual-variable nonlinearity. A coupling graph correspondence connects topology to curvature for bilinear systems. That correspondence breaks at higher polynomial degree and higher dimension, but is recovered as a special case of essential dimension — an algebraic invariant that determines whether a constraint surface carries genuine multi-variable curvature or is reducible to fewer dimensions. A gradient irreducibility theorem establishes that the coupling curvature on a constraint surface is fundamentally entangled with the surface's tangent-plane orientation.

These results, individually, are contributions to applied differential geometry and diagnostic methodology. Collectively, they suggest a direction that this paper attempts to articulate: that coupling between variables in physical systems possesses its own intrinsic geometry, that this geometry is the primary object (not a derived measurement of something else), and that the temporal evolution of this geometry — how coupling curvature changes as systems degrade, age, or transition between regimes — may follow geometric laws analogous to those governing other physical fields.

This paper is not a claim to have discovered such laws. It is an honest account of where the work stands, what the results are pointing toward, and what specific investigations would confirm or refute the conjecture that coupling dynamics has a geometric field theory. The purpose is to map the territory between what has been established and what remains to be explored, with sufficient precision that other researchers can engage with the open questions.

---

## 1. What Has Been Established

The following results are validated, verified by independent computational systems, and documented in companion papers. They constitute the firm ground from which the speculative directions in this paper depart.

### 1.1 The framework and its diagnostic

The Lloyd Framework models any system governed by a constraint equation F(x₁, ..., xₙ) = 0 as an implicit hypersurface in variable space. The Gaussian curvature K_G (for n = 3) or Gauss-Kronecker curvature K (for general n) of this surface provides a coordinate-independent measure of the coupling geometry. Monitoring K over time detects coupling changes — including changes invisible to conventional single-channel or linear multivariate diagnostics. The framework has been validated across bearing fault detection, turbofan degradation, HVAC fault detection, combustion instability, and composite pressure vessel monitoring, with zero false alarms and detection of coupling-only faults that conventional methods miss [Lloyd, 2026a; 2026c].

### 1.2 The curvature decomposition

The scalar curvature K_G decomposes exactly as K_G = κ_c + κ_s + κ_int, where κ_c (coupling curvature) measures curvature from inter-variable coupling, κ_s (self-curvature) measures curvature from individual-variable nonlinearity, and κ_int (interaction curvature) measures their geometric interplay on the tangent plane. The decomposition is derived independently through algebraic classification of the bordered Hessian determinant and through tangent-plane projection via the shape operator; both routes yield identical closed-form expressions, establishing the decomposition's uniqueness [Lloyd, 2026d].

### 1.3 Gradient irreducibility

The gradient of F — which defines the normal to the constraint surface and therefore the tangent plane on which curvature is measured — enters the coupling curvature κ_c as a free variable that cannot be eliminated by any choice of formulation. This is not a computational artifact. It is a geometric fact: the coupling curvature on a surface is the cross-section of the ambient coupling tensor projected onto the tangent plane, and the tangent plane's orientation is an intrinsic part of the measurement. No decomposition, no change of coordinates, and no alternative formulation can separate the "what" (the coupling) from the "where" (the surface orientation) [Lloyd, 2026d, Theorem 4].

### 1.4 Coupling graph correspondence and essential dimension

For bilinear constraint equations in three variables, K_G = 0 if and only if the coupling graph has open topology (the coupling polynomial factors). Graph closure is necessary and sufficient for nonzero curvature. At higher polynomial degree and in dimensions n > 3, this graph correspondence breaks: factorable polynomials can have nonzero curvature, and connected coupling graphs can have zero curvature. The true invariant is the essential dimension of the constraint polynomial — the minimum number of independent linear combinations of variables needed to express it. Conjecture: K = 0 at generic points if and only if the essential dimension is strictly less than n. This conjecture holds on all twenty-one tested surfaces across n = 3 and n = 4 with zero exceptions [Lloyd, 2026d].

### 1.5 The S₃ group structure

The centrifuge operation evaluates K_G under all permutations of variable roles. For three variables, this produces six values whose pattern of degeneracies and ratios encodes coupling topology. The permutation group S₃ acts on the coupling equivalence classes, and the coupling kernel factorises under this action (Theorem 8.1 in [Lloyd, 2026a]). The relationship between the centrifuge invariants and the curvature decomposition is partially explored; whether the centrifuge spectrum contains geometric information beyond scalar K_G remains an open question.

---

## 2. What the Results Are Pointing Toward

### 2.1 Coupling as geometry, not measurement

The standard interpretation of the framework is operational: K_G is a diagnostic tool. You compute it, track it, and raise an alarm when it changes. The constraint surface is a mathematical convenience — a way of organising the variables into a shape whose curvature you can measure.

But the results resist this interpretation. Consider what the established findings actually say:

The Whole Fish principle says the curvature of the whole cannot be recovered from the curvatures of the parts. Each pairwise coupling surface (xy = 1, yz = 1, zx = 1) is intrinsically flat (K_G = 0). Their union (xy + yz + zx = 3) has K_G = 1/12. The curvature is an emergent property of the closed coupling — it exists only in the whole and cannot be attributed to any component.

The essential dimension result says curvature IS irreducibility. A system that can be separated into independent pieces has K = 0 (the surface is a cylinder, and the free direction is the direction of separability). A system that cannot be separated has K ≠ 0. The curvature isn't measuring coupling strength — it's measuring whether the coupling is *real*, in the sense of being irreducible to lower-dimensional interactions.

The gradient irreducibility theorem says the coupling curvature and the surface orientation are fundamentally entangled. You cannot measure the coupling without also measuring the geometry of the space you're measuring it in. The coupling is not a property of the variables that happens to be visible on a surface. The coupling IS the surface, and the surface IS the coupling.

Taken together, these results suggest that the constraint surface is not a computational tool for measuring coupling. It is the coupling itself, expressed as geometry. The curvature is not a diagnostic reading — it is the intrinsic geometric structure of the inter-variable relationship.

This interpretive shift — from "curvature measures coupling" to "curvature IS coupling" — is precisely the shift that has preceded every major geometrisation of a physical theory.

### 2.2 Historical precedent for geometrisation

The pattern is well-established in physics:

**Electromagnetism.** Faraday observed that electric and magnetic effects propagate through space with detectable structure — field lines, regions of influence, geometric patterns of force. Maxwell formalised these observations into field equations: four equations describing how the electromagnetic field behaves in space and time. The critical conceptual step was recognising that the field is not a mathematical convenience for computing forces between charges. The field is a physical thing with its own dynamics, its own energy, its own geometric structure. Charges and currents are sources and sinks; the field is the primary object.

**Gravity.** Newton observed that gravitational effects obey an inverse-square law. Einstein recognised that the inverse-square law is a consequence of something deeper: mass curves spacetime, and objects follow geodesics (straightest paths) in the curved geometry. The gravitational field IS the curvature of spacetime. The field equations (Einstein's equations) describe how matter determines curvature and how curvature determines motion. The critical step was recognising that geometry is not a background stage on which physics happens — geometry is what physics IS.

**Information.** Fisher observed that statistical models have a natural notion of distance: how distinguishable are two nearby parameter values given the data? Rao formalised this as a Riemannian metric on the parameter space. The curvature of this metric measures the complexity of the statistical model — how much information the data carries about the parameters. Information geometry treats the information content of a statistical model as an intrinsic geometric property of its parameter manifold.

**Gauge theory.** Yang and Mills observed that the internal symmetries of particle physics (rotations in isospin space, colour rotations in QCD) have a geometric structure: they define connections on fibre bundles over spacetime. The gauge fields ARE the connections. The field strength IS the curvature of the connection. The gauge field equations describe how the geometry of the fibre bundle interacts with matter.

In each case, the progression followed the same arc:

1. An observable quantity is noticed to have structure (Faraday's field lines, Newton's inverse square, Fisher's distance, Yang's internal rotations).
2. The structure is formalised as geometry (Maxwell's fields, Einstein's metric, Fisher's metric, gauge connections).
3. The geometry is recognised as the primary object — not a description of something else, but the thing itself.
4. The dynamics of the geometry are described by field equations (Maxwell's equations, Einstein's equations, information-geometric flows, Yang-Mills equations).

The Lloyd Framework is, at present, at step 2 for coupling geometry. The constraint surface and its curvature have been formalised. The decomposition has identified the geometric components. The essential dimension has connected the geometry to algebraic structure. Step 3 — recognising coupling geometry as the primary object — is the interpretive shift suggested by the results in Section 2.1. Step 4 — the field equations — is the open question.

### 2.3 What "field equations of coupling geometry" would mean

If coupling geometry follows dynamical laws, what form would those laws take?

In general relativity, the field equations relate the curvature of spacetime (the Einstein tensor) to the distribution of matter and energy (the stress-energy tensor). The equations say: "here is how matter determines curvature, and here is how curvature determines motion."

An analogous statement for coupling geometry would say: "here is how the physical properties of a system determine the curvature of its constraint surface, and here is how the curvature evolves as the system degrades."

The first half of this statement is already implicit in the framework. The constraint equation F(x₁, ..., xₙ) = 0 encodes the physics. The curvature follows from the equation. What is not known is whether the *temporal evolution* of the curvature — how K_G changes as a bearing wears, as fouling progresses, as a blade cracks — follows a law.

Specifically, the question is: given the curvature at time t, can you predict the curvature at time t + dt from the geometry alone, without knowing the specific physical mechanism of degradation?

If the answer is yes, coupling degradation follows a geometric flow. The field equations describe that flow, and prediction becomes a geometric computation rather than a statistical extrapolation.

---

## 3. Where the Evidence Points

### 3.1 Curvature trajectories in degradation data

The framework has been applied to run-to-failure datasets where the temporal evolution of K_G is directly observable:

- **C-MAPSS turbofan degradation:** K_G tracked from healthy operation through progressive degradation to failure. The trajectory shows characteristic structure — not monotonic decline but a signature that varies with degradation mode.

- **CWRU bearing fault progression:** K_G shifts when faults are introduced, with different fault types (ball, inner race, outer race) producing different K_G signatures.

- **ASHRAE HVAC faults:** K_G responds to fouling, refrigerant leak, and compressor faults with geometrically distinct signatures.

In all cases, the curvature changes follow structured paths — they are not random walks. Whether that structure is sufficiently regular to constitute a law is the empirical question that the next phase of investigation must answer.

### 3.2 Curvature flow as a candidate framework

Differential geometry provides a well-studied toolkit for describing how curvature evolves: geometric flows. The Ricci flow, introduced by Hamilton and famously used by Perelman to prove the Poincaré conjecture, describes how the metric of a Riemannian manifold evolves to smooth out curvature irregularities. Mean curvature flow describes how embedded surfaces evolve to minimise area.

For constraint surfaces, a relevant flow would describe how the surface deforms as the underlying physical system changes. If a bearing degrades, the constraint equation F changes (because the physical coupling changes), and the surface deforms. The curvature evolves as a consequence of the deformation.

The question is whether the curvature evolution is *determined* by the curvature itself (as in Ricci flow, where the metric evolves according to its own Ricci curvature), or whether it requires external information about the physical degradation mechanism.

If the curvature evolution is self-determined — if knowing K_G(t) and its spatial derivatives on the constraint surface suffices to predict K_G(t + dt) — then coupling degradation has a geometric field equation. If external physical information is required, the geometry is descriptive but not predictive.

The distinction matters enormously for practical application. Self-determined curvature evolution would enable model-free prognostics: predicting remaining useful life from the geometry alone, without training data, without physical models, without knowing what specific mechanism is causing the degradation. The geometry would tell you not just "something is wrong" but "here is where it's going and when it will arrive."

### 3.3 Curvature as information

The essential dimension result suggests a connection to information theory. A constraint surface with essential dimension d < n can be described using d variables instead of n. The remaining (n − d) variables are redundant — they carry no information about the coupling. Curvature, in this view, measures the irreducible information content of the coupling: the amount of structure that cannot be compressed into fewer dimensions.

This resonates with information geometry, where the Fisher information metric's curvature measures the statistical distinguishability of nearby parameter values. On a constraint surface, the coupling curvature may play an analogous role: measuring how much the coupling structure changes as you move along the surface. High coupling curvature means the coupling is highly sensitive to the operating point. Low coupling curvature means the coupling is robust. Zero coupling curvature means the coupling is degenerate (reducible).

If coupling curvature is indeed an information-theoretic quantity, then coupling degradation is information loss — the progressive destruction of the geometric structure that encodes the relationship between variables. A healthy system has rich, curved constraint geometry. A degraded system has flatter, simpler geometry. Failure is the point where the essential dimension drops — where a coupling that was irreducibly three-variable becomes effectively two-variable because one relationship has broken.

This interpretation would connect the framework to the second law of thermodynamics (degradation as increasing entropy / decreasing geometric complexity) and to the theory of phase transitions (failure as a topological change in the constraint surface). Both connections are speculative but testable.

### 3.4 The centrifuge as probe of internal symmetry

The centrifuge operation — evaluating curvature under all permutations of variable roles — bears a structural resemblance to the role of gauge transformations in field theory. In gauge theory, the physical content of a field is what remains invariant under gauge transformations. The gauge-dependent components are mathematical artifacts; the gauge-invariant combinations are the physical observables.

The centrifuge performs an analogous operation: it evaluates the coupling geometry under all possible role assignments. Some permutations produce the same K_G (degeneracies). Some produce different values. The pattern of degeneracies and distinct values is invariant under coordinate transformations (because K_G at each permutation is individually invariant). The centrifuge spectrum is therefore a richer invariant than scalar K_G — it encodes how the coupling structure responds to relabelling of roles.

Whether this analogy with gauge theory is superficial or substantive depends on whether the S₃ action on the centrifuge spectrum has algebraic properties that parallel the structure of gauge groups. Theorem 8.1 establishes that the coupling kernel factorises under the S₃ action, which is a necessary condition for the analogy to be substantive. Whether it is sufficient — whether the centrifuge invariants form a representation-theoretic structure that admits a connection or curvature interpretation — is an open question.

---

## 4. Specific Open Questions

### 4.1 Does coupling curvature evolution follow a geometric flow?

**The question.** Given K_G(t) on a degrading system's constraint surface, can K_G(t + dt) be predicted from K_G(t) and its spatial derivatives alone?

**How to test it.** Using the C-MAPSS run-to-failure data (100+ units with known failure times), compute K_G trajectories for each unit. Fit the trajectories to candidate geometric flows (e.g., dK/dt = f(K, ∇K, ΔK) for various f). Evaluate whether a single flow equation predicts the trajectories across units, degradation modes, and operating conditions. If a universal flow law fits, that is evidence for geometric field equations. If different degradation modes require different flow laws, the dynamics are mechanism-dependent and the field equation conjecture is weakened.

**What success looks like.** A single ordinary or partial differential equation in K_G that predicts remaining useful life within ±20% on held-out units, without any physical model of the degradation mechanism.

### 4.2 Is there a coupling action principle?

**The question.** Physical field equations typically arise from an action principle: the system evolves to extremise (usually minimise) a functional of the field. Is there a functional of the coupling curvature whose extremisation yields the observed curvature evolution?

**How to test it.** If the curvature trajectory K_G(t) follows a smooth path, check whether it is a geodesic in some metric on the space of constraint surfaces. Geodesics are the paths that extremise arc length — if coupling degradation follows a geodesic, it evolves along the "shortest path" in surface space, which would imply a least-action principle.

**What success looks like.** A functional S[K_G] whose Euler-Lagrange equation reproduces the observed curvature flow from Question 4.1.

### 4.3 Does failure correspond to a geometric singularity?

**The question.** When a physical system fails, does the constraint surface develop a geometric singularity (a point where curvature diverges, the gradient vanishes, or the topology changes)?

**How to test it.** Track the gradient magnitude |∇F|, the curvature K_G, and the essential dimension through the run-to-failure trajectory. Check whether failure corresponds to: (a) |∇F| → 0 (the surface develops a singularity), (b) K_G → ±∞ (curvature blowup), (c) essential dimension dropping (a coupling relationship breaks, reducing the irreducible dimension), or (d) a sign change in K_G (the coupling topology transitions from bowl to saddle or vice versa).

**What success looks like.** A consistent geometric signature of failure across multiple datasets and domains. If failure always corresponds to the same type of geometric event (e.g., essential dimension drop), that would be a universal geometric characterisation of system failure.

### 4.4 What are the conserved quantities?

**The question.** In every field theory, conservation laws arise from symmetries (Noether's theorem). The coupling geometry has symmetries: K_G is invariant under coordinate transformations, the decomposition has internal structure, the centrifuge has S₃ symmetry. Do these symmetries produce conserved quantities — geometric properties that remain constant even as the system degrades?

**How to test it.** Compute candidate conserved quantities (total curvature ∫K dA, centrifuge symmetric polynomials, ratios like κ_c/K_G) along degradation trajectories. Check whether any of them are approximately constant over time while individual curvature values change.

**What success looks like.** A geometric quantity that is conserved during degradation. Such a quantity would be the coupling analogue of energy in mechanics — a property of the coupling that is redistributed but not destroyed as the system evolves.

### 4.5 Does the decomposition predict fault mechanism?

**The question.** The decomposition separates K_G into coupling, self, and interaction components. Does a coupling-dominated K_G shift (κ_c changing, κ_s stable) reliably correspond to a physically distinct fault mechanism from a self-dominated shift?

**How to test it.** Apply the decomposition to CWRU bearing data with labelled fault types (inner race, outer race, ball) and severities. Classify each fault by which decomposition component it affects. Determine whether fault mechanism correlates with the dominant curvature component.

**What success looks like.** A mapping: coupling faults → κ_c shifts, sensor/component faults → κ_s shifts, operating-point changes → κ_int shifts. If this mapping holds across datasets, the decomposition provides fault mechanism classification from geometry alone.

---

## 5. What This Is Not

This paper is not a claim to have discovered the field equations of coupling geometry. It is not a claim that coupling dynamics necessarily follows a geometric law. It is not an assertion that the analogies with general relativity, information geometry, or gauge theory are anything more than structural parallels that motivate investigation.

The results established in Section 1 are rigorous and verified. The directions outlined in Sections 2–4 are honest speculation guided by those results. The distinction is maintained throughout, and the open questions in Section 4 are formulated as testable hypotheses with specific falsification criteria.

The framework originated from applied diagnostics — the practical problem of detecting coupling faults in physical systems. The theoretical directions discussed here emerged from the validation process itself. The Whole Fish principle was discovered during a metamorphic test. The essential dimension conjecture was discovered while investigating why the coupling graph correspondence fails at higher degree. The gradient irreducibility theorem fell out of the attempt to separate coupling from self-curvature. None of these results were anticipated. They emerged from rigorous testing, honest documentation of unexpected findings, and the discipline to follow the mathematics wherever it led.

If the deeper theory exists, it will be found the same way — not by postulating field equations and fitting data to them, but by continuing to test, to document, and to follow. The field equations, if they are there, will emerge from the geometry the same way the decomposition and the essential dimension emerged: as something the mathematics was always saying, once someone asked the right question.

---

## 6. A Note on Method

The development described in this paper and its companions was conducted by a sole researcher without a university affiliation, using AI computational tools (Anthropic Claude and Google Gemini) for independent mathematical verification, and a framework built from first principles over a period of approximately two weeks. The theoretical content, physical interpretation, and all conceptual advances originated with the author. The AI tools provided verification, stress-testing, and symbolic computation — the functions traditionally served by collaborators, referees, and computer algebra systems.

This methodological note is included not as a disclaimer but as a data point. The results demonstrate that rigorous mathematical research is achievable outside traditional institutional structures when the researcher has genuine structural intuition, maintains intellectual honesty, subjects every claim to pre-committed falsification criteria, and uses available tools — including AI — for independent verification rather than confirmation.

Novel discoveries emerge from applied deduction, not qualifications. The geometry of coupling does not care who computes it.

---

## 7. Conclusion

The Lloyd Framework has produced, in a compressed period, a sequence of results that individually contribute to applied differential geometry and collectively suggest a direction: that coupling between variables in physical systems is itself a geometric object with intrinsic structure, irreducible properties, and possibly its own dynamics.

The curvature decomposition separates what is measured. The essential dimension identifies what is irreducible. The gradient irreducibility theorem establishes what is fundamental. The question that remains — the question that would transform this framework from a diagnostic tool into a geometric theory — is whether the temporal evolution of coupling curvature follows a law.

The data to investigate this question already exists. The mathematical tools are built. The validation architecture is in place. The next step is to look at the curvature trajectories of degrading systems and ask: is there a pattern? And if there is — does that pattern follow from the geometry?

If it does, coupling has field equations. And if coupling has field equations, then the way we understand, predict, and maintain coupled physical systems changes fundamentally. Not because we have a better diagnostic tool, but because we have recognised that the coupling between things — the way variables depend on each other, constrain each other, and evolve together — is itself a geometric structure with its own laws.

That recognition, if it proves correct, is the deeper discovery that this work has been converging toward.

---

## References

Einstein, A. (1915). Die Feldgleichungen der Gravitation. *Sitzungsberichte der Preussischen Akademie der Wissenschaften*, 844–847.

Fisher, R. A. (1925). Theory of statistical estimation. *Mathematical Proceedings of the Cambridge Philosophical Society*, 22(5), 700–725.

Hamilton, R. S. (1982). Three-manifolds with positive Ricci curvature. *Journal of Differential Geometry*, 17(2), 255–306.

Lloyd, W. (2026a). Geometric constraint surface diagnostics via Gaussian curvature of coupled systems. Australian Provisional Patent AU 2026902758.

Lloyd, W. (2026b). Coupling curvature decomposition for diagnostic separation on constraint surfaces. Australian Provisional Patent AU 2026902926.

Lloyd, W. (2026c). Lloyd Framework validation programme and benchmark results. Technical Report.

Lloyd, W. (2026d). Intrinsic decomposition of Gaussian curvature on constraint surfaces: from coupling topology to essential dimension. Manuscript in preparation.

Maxwell, J. C. (1865). A dynamical theory of the electromagnetic field. *Philosophical Transactions of the Royal Society of London*, 155, 459–512.

Rao, C. R. (1945). Information and the accuracy attainable in the estimation of statistical parameters. *Bulletin of the Calcutta Mathematical Society*, 37, 81–91.

Yang, C. N., & Mills, R. L. (1954). Conservation of isotopic spin and isotopic gauge invariance. *Physical Review*, 96(1), 191–195.

---

*Manuscript prepared April 2026. Corresponding author: William Lloyd.*
