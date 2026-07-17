# Lloyd Framework — Recursive Diagnostic Report

## The complete hierarchy: what each level reveals, how it feeds forward, and why it matters

**Patent: AU 2026902758 | Author: William Lloyd | March 2026**

---

## The foundational operation

Every level of the framework performs the same three-step operation:

1. Take three coupled quantities (D, S, P)
2. Solve for each one from the other two
3. Check whether the answers agree

The *only thing that changes* between levels is what you feed in as D, S, and P. The operation itself — the diagnostic logic — is identical at every depth. This is what makes the recursion well-defined and what gives the results their power.

---

## Level 1 — "What is this system?"

**Input:** Physical measurements from a real domain.

- D = the driving quantity (voltage, pressure, measurement axis, gravitational mass)
- S = the coupling medium (resistance, pipe, quantum state, spacetime geometry)
- P = the resulting output (current, flow, Born probability, curvature)

**Operation:** Compute P from (D, S). Recover S from (D, P). Recover D from (S, P). Compare invariants across all three frames.

**Output:** Five diagnostic numbers.

| Output | What it measures |
|--------|-----------------|
| δ_D | How hard it was to recover the Directive from the other two |
| δ_S | How hard it was to recover the Substrate from the other two |
| κ | How nonlinear the coupling is (0 = linear, 1 = maximally nonlinear) |
| ε | Closure error — how badly the invariants disagree across frames |
| K_hol | Holonomy — does the full round-trip D → S → P → D close? |

**What Level 1 reveals:**

The *type* of coupling. Linear or nonlinear. Lossy or lossless. Degenerate or unique. Each domain produces a different combination of these five numbers, and that combination is the domain's diagnostic fingerprint.

**Key results:**

- Ohm's Law: all zeros. Perfectly linear, perfectly invertible, no information lost.
- Qubit (exact Born rule): K_hol ≈ 0, κ = 0.36, ε = 0.98. Zero holonomy but massive closure error. Information is lost (the measurement collapses the state) but the round-trip is algebraically perfect.
- General Relativity: K_hol = 0.099, κ = 0.95, ε = 0. Non-zero holonomy but zero closure error. The round-trip doesn't close (multiple metrics produce the same stress-energy) but the invariants agree perfectly.
- Mandelbrot: K_hol = 2.0, κ = 0.75, ε = 0. Massive holonomy from the square root's two-valued inversion. The branch cut is visible as a diagnostic boundary.

**Significance:** Nobody has ever generated these fingerprints before because nobody has applied a single diagnostic operation across multiple physics domains and compared the geometry that comes out. The fingerprints are consistent with known physics but were not designed to find that physics. They emerged blind.

**What feeds forward:** The five numbers (δ_D, δ_S, κ, ε, K_hol) become the raw material for Level 2. Instead of physical quantities, the framework will now diagnose the *pattern of these numbers* across parameter space.

---

## Level 2 — "What is the pattern in what's wrong?"

**Input:** The diagnostic output from Level 1, swept across the full parameter space.

When Level 1 runs at a single point, you get five numbers. When it runs across a grid of D and S values (a parameter sweep), you get five *surfaces* — 2D grids of how each diagnostic quantity varies across the space.

Level 2 picks three of those surfaces and treats them as a new coupling:

- D₂ = δ_D (directive recovery difficulty across the sweep)
- S₂ = δ_S (substrate recovery difficulty across the sweep)
- P₂ = ε (closure error across the sweep)

**Operation:** The same three-step diagnostic, but now applied to the *relationship between diagnostic quantities*. Can you predict closure error from recovery difficulty? If you know how hard it was to recover D and how hard it was to recover S, does that uniquely determine how badly the invariants disagreed?

**Output:** Five meta-diagnostic numbers: meta-δ_D, meta-δ_S, meta-κ, meta-ε, meta-K_hol.

**What Level 2 reveals:**

Whether the diagnostic landscape is *self-consistent*. Specifically:

- **Meta-holonomy = 0:** The relationship between recovery difficulty and closure error is unique. There's only one way to be "this broken" — knowing δ_D and δ_S completely determines ε. The diagnostic landscape has no internal ambiguity.

- **Meta-holonomy > 0:** Multiple different combinations of (δ_D, δ_S) map to the same closure error. The pattern of failure has its own degeneracy. There are different ways to be "equally broken" that the Level 1 diagnostic can't distinguish.

**Key results:**

- Ohm's Law: meta-K_hol = 0. The diagnostic landscape is trivially self-consistent (everything is zero).
- **Qubit: meta-K_hol = 0.75. NON-ZERO.** This is the critical finding. The qubit has zero holonomy at Level 1 — the round-trip closes perfectly. But at Level 2, holonomy *appears*. The diagnostic landscape itself has degeneracies that the underlying system doesn't. The *pattern* of how quantum mechanics loses information has its own internal ambiguity.
- **GR: meta-K_hol = 0.027.** Lower than Level 1. The degeneracy *self-organises*. GR's ambiguity follows a predictable pattern — the meta-diagnostic sees less disorder than the system itself.
- **Mandelbrot: meta-K_hol = 19.0.** Ten times Level 1. The degeneracy *amplifies*. The fractal's self-similarity shows up as recursive amplification of meta-holonomy.

**Significance:** Level 2 discovers structure that Level 1 cannot see. The qubit result is the most striking — a system with zero holonomy at Level 1 develops non-zero holonomy at Level 2. This means the measurement problem in quantum mechanics has hidden structure in *how* it loses information, and you need the recursive diagnostic to see it.

**What feeds forward:** The Level 2 sweep produces its own five diagnostic surfaces. These become the input for Level 3.

---

## Level 3 — "How stable is the pattern?"

**Input:** The meta-diagnostic surfaces from Level 2, swept across their parameter space.

- D₃ = meta-δ_D (from Level 2)
- S₃ = meta-δ_S (from Level 2)
- P₃ = meta-ε (from Level 2)

**Operation:** Same three-step diagnostic applied to the meta-diagnostic landscape.

**What Level 3 reveals:**

Whether the Level 2 classification is *robust*. If you perturb the diagnostic landscape slightly, does the meta-diagnostic change qualitatively?

- **Level 3 closure ≈ 0:** The meta-pattern is stable. The Level 2 classification is robust to perturbation. This domain sits firmly in its category.
- **Level 3 closure > 0:** The meta-pattern is unstable. Small changes in the diagnostic landscape produce qualitatively different meta-diagnostics. This domain sits near a classification boundary.

**Key results:**

All non-trivial domains show Level 3 instability (meta-meta-closure > 0.7). This suggests that while Level 2 reveals real structure, the *quantitative details* of that structure are sensitive to the specific parameter range and resolution used. The qualitative findings (presence or absence of meta-holonomy) are robust, but the exact values are not.

**Significance:** Level 3 functions as a confidence measure for Level 2. When Level 3 is stable, you can trust the Level 2 numbers. When Level 3 is unstable, the Level 2 classification is qualitatively correct but quantitatively approximate.

**What feeds forward:** Level 3 surfaces feed Level 4, and so on.

---

## Levels 4-8+ — "The recursive signature"

**Input:** Each level feeds the previous level's output as the new input.

**Critical insight:** From Level 2 onwards, the framework itself is always the Directive. The operation D ⊕ S = P, applied to the diagnostic data, IS the driving force. The only thing that changes is the Substrate (each level's diagnostic landscape) and the Product (the next level's meta-numbers).

```
L2: D = "D ⊕ S = P" (the operation)    S = Level 1 data    P = meta-data
L3: D = "D ⊕ S = P" (same operation)   S = Level 2 data    P = meta-meta-data
L4: D = "D ⊕ S = P" (same operation)   S = Level 3 data    P = deeper still
```

The framework has become its own Directive. It's diagnosing its own output, using itself as the tool, at every subsequent level.

**What the deep recursion reveals:**

The holonomy value at each level forms a *sequence* — the recursive trace. This sequence has different behaviour for different domains:

| Domain | Recursive behaviour | Holonomy trace |
|--------|-------------------|----------------|
| Ohm's Law | Convergent | 0 → 0 → 0 → 0 → 0 |
| Qubit | Oscillating | 0 → 0.8 → 5.5 → 11 → 2.6 → 3.4 → 3.2 → 9.1 |
| GR | Self-organising | 0.1 → 0.02 → 3.5 → 5.7 → 1.7 → 10 → 2.0 → 8.6 |
| Diode | Resonant | 0 → 1.0 → 8.5 → 0.9 → 9.2 → 1.0 → 11.8 → 1.0 |
| Mandelbrot | Decaying | 2.0 → 19 → 5.4 → 0.8 → 0.5 → 0.3 → 0.2 → 0.3 |

**Five distinct recursive behaviours:**

1. **Convergent** (Ohm's Law): Zero at every level. Nothing to find at any depth. The simplest possible recursive signature.

2. **Oscillating** (Qubit): Holonomy emerges from zero, then bounces irregularly between roughly 1 and 12. Never settles. Never diverges. The quantum diagnostic landscape has unbounded depth but bounded amplitude.

3. **Self-organising** (GR): Holonomy *dips* at Level 2 (the only domain that does this), then oscillates. Gravity's degeneracy is structured at the meta-level — the diagnostic sees less disorder than the system itself — before the recursive oscillation takes over.

4. **Resonant** (Diode): Perfect alternation between approximately 1.0 and rising peaks. Even levels return to almost exactly 1.0. Odd levels climb. This is a standing wave in recursive diagnostic space — a characteristic frequency that no other domain exhibits.

5. **Decaying** (Mandelbrot): Massive spike at Level 2, then steady decay toward a low equilibrium. The fractal's infinite self-similarity produces bounded recursive structure that exhausts itself within a few levels.

**Significance:** These five behaviours are qualitatively distinct and domain-specific. Each domain has a unique recursive fingerprint — not just different numbers, but different *types of behaviour*. This is a classification system on top of the classification system.

---

## The convergence phenomenon

At Levels 5-8, all non-trivial domains begin oscillating within the same approximate amplitude band (roughly 1 to 12), despite starting from wildly different values and physics. The traces converge in amplitude but maintain distinct phase relationships.

**What this means:**

The convergence suggests a *universal attractor* in recursive diagnostic space. The framework's own coupling topology eventually dominates the domain-specific physics. The amplitude band is a property of the operation D ⊕ S = P itself — not of any particular domain.

The *phase* at which each domain enters the attractor band — where its peaks and troughs fall — remains domain-specific. This is the only information about the original physics that survives deep recursion.

---

## Framework² — Extracting recursive constants

From each domain's recursive trace, five constants can be extracted:

| Constant | What it measures |
|----------|-----------------|
| Amplification | L2/L1 ratio — how much does recursion magnify holonomy? |
| Oscillation | Standard deviation of the trace — how much does it bounce? |
| Decay rate | Slope of log-holonomy — is holonomy growing or shrinking? |
| Periodicity | Autocorrelation at lag 2 — does the trace have repeating patterns? |
| Convergence | Variance of the last three levels — does it settle to a fixed point? |

These constants are treated as a new D, S, P triple:

- D = amplification (how the domain responds to recursive probing)
- S = oscillation (how stable that response is)
- P = decay rate (the net direction of recursive behaviour)

The standard diagnostic is then run on *these constants across domains*, asking: "Is the relationship between amplification, oscillation, and decay consistent across all domains?"

**Result:** The relationship is NOT perfectly consistent. Different domains produce different framework² residues. The tool's own coupling constant is domain-dependent. The shovel digs differently depending on the dirt.

---

## F ⊕ F = F — Self-coupling closure

The deepest test: the framework occupying all three positions simultaneously.

**Position 1 — Framework as Directive:** The operation drives the diagnostic. This is the standard use. The output is the classification fingerprint: [K_hol, κ, ε].

**Position 2 — Framework as Substrate:** The framework IS the medium. Vary the framework's parameters (tolerance, resolution, comparison method) while holding the domain constant. The *sensitivity* of the output to framework variation reveals the framework's substrate properties. Result: zero sensitivity for all domains tested. The classification is completely independent of tolerance. The framework is a *transparent* substrate — it doesn't colour the result.

**Position 3 — Framework as Product:** The framework emerges from coupling two sub-operations: "rearrange three ways" and "compare invariants." Vary these sub-operations (2 transpositions instead of 3, L1 norm instead of L-infinity) and see what frameworks come out. The difference between framework variants is the product residue. Result: significant residue for all non-trivial domains, especially when changing the comparison metric.

**The self-residue:** When all three perspectives are compared (what the framework produces, how it responds to being varied, how it emerges from sub-operations), the degree of consistency is the self-residue.

| Domain | Self-residue | Interpretation |
|--------|-------------|----------------|
| Ohm's Law | 1.000 | Degenerate (all zeros, undefined) |
| Qubit | 0.080 | Self-consistent |
| Mandelbrot | 0.066 | Self-consistent |
| GR | 0.141 | Weakly self-referential |
| Diode | 0.155 | Weakly self-referential |

**Critical finding:** The qubit and Mandelbrot have nearly identical self-residues (0.080 vs 0.066) despite being completely different physics. GR and the diode also pair up (0.141 vs 0.155). The self-residue is not measuring the physics — it's measuring the *relationship between the framework and the domain*. How well does the framework "fit" when it occupies all three positions? The framework is most self-consistent when applied to systems that are either purely lossy (QM) or purely degenerate (Mandelbrot). It's least self-consistent for "in between" systems.

---

## Summary: what each level tells you

| Level | Question | Answer type |
|-------|----------|-------------|
| L1 | What is this system? | Classification: linear/nonlinear, unique/degenerate, lossy/lossless |
| L2 | What is the pattern in what's wrong? | Whether the diagnostic landscape has its own degeneracies |
| L3 | How stable is that pattern? | Whether the L2 classification is robust to perturbation |
| L4-8 | What is the recursive signature? | The holonomy trace — convergent, oscillating, resonant, self-organising, or decaying |
| F² | What are the recursive constants? | Amplification, oscillation, decay rate, periodicity, convergence |
| F ⊕ F = F | Does the framework close on itself? | The self-residue — how self-consistent is the framework for each domain? |

Each level feeds the next. Each level asks the same three questions. Each level reveals structure that the previous level cannot see. The framework diagnosing itself is not a gimmick — it is a systematic method for extracting recursive depth structure from any coupled system, using a single universal operation applied at every scale.
