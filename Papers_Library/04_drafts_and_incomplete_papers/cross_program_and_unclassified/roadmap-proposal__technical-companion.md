# Road-Map Technical Companion — Mathematician (v2)

**Companion to:** `roadmap-proposal-v2.md` (same outbox).
**Purpose:** the depth the roadmap proper deliberately doesn't carry — the technical content
absorbed since v1, with explicit grades and fences. Not the north-star document; the layer beneath
it, for Will and the field specialists to merge against during roadmap authoring.
**Grade markers:** `[ESTABLISHED]` (theorem / verified) · `[WELL-SUPPORTED]` (measured, multi-source)
· `[PLAUSIBLE]` (one good piece of evidence) · `[CONJECTURE]` (no result yet, navigation target).

---

## A. Q3 — the refusal envelope (peer of Q1/Q2)

The question my v1 missed. *Does the observation map Φ admit a refinement law — sharp,
conservative, or none — that tells us when to stop honestly?* Q1 grants the right to certify a
point; Q2 names the shape of reconstruction; Q3 grants the right to stop. Without Q3 the engine
certifies cell-by-cell beautifully and never knows when its samples went blind — the precise
false-certainty pathology Cella exists to refuse.

**Inhabitation ladder** for any Φ:
- **sharp** — the refinement law is solved and absorbing (dyadic death is the example: `e_q = 0 ⟺
  q ≥ L` `[ESTABLISHED]`); a single deviation is a reliable boundary signal.
- **conservative** — a bound on the law, not the law itself; refuses no later than the boundary,
  possibly earlier; lossy but honest.
- **cannot-inhabit-honestly** — dynamics undecidable, no conservative bound; outside Cella's reach
  until someone proves its boundary theorem.

Q3 is the architecture of refusal made into a foundational question; Tier A Stage A3 is the
campaign that delivers a typed classification on the c002 test maps.

---

## B. Three signatures, not one (keep the primitives separate)

The technical heart of the fold. The probe insisted, and the Stage B Frobenius find sharpens: a
boundary in Cella's world reads at *three distinct arithmetic addresses*, and conflating them by
notation buys the conical blind spot back.

| Signature | Reads | Address | Status |
|---|---|---|---|
| **Coupling-degeneracy** | curvature diverges / discriminant vanishes / roots collide / variables decouple | archimedean (analytic) + algebraic | `[ESTABLISHED]` per-class via D⊕S=P over `F=0`; **discriminant=fold** for polynomials is a theorem, not analogy `[ESTABLISHED]` |
| **Representation-exhaustion** | the observation runs out of resolution | 2-adic (the valuation `v_2`) — the *place* | `[ESTABLISHED]` for floats (HR133); per-substrate, *not* liftable off floats; *also* the one axis where my earlier "two-place shadow" critique still stands |
| **Periodicity** | the orbit of the base in the residue group `(ℤ/b₀)*` | Galois / cyclotomic — the order of Frobenius₂ across `ℚ(ζ_p)` for every odd prime `p` | `[ESTABLISHED]` per Stage B's 132/132 + the cyclotomic factorisation check; the *first* place every odd prime acquires real computational meaning |

Three things in the record about this:

- **Coupling-degeneracy is per-class universal `[ESTABLISHED]`.** D⊕S=P equips the entire `F=0`
  class with one boundary law — compute the intrinsic geometry, the curvature announces the cliff
  from a safe distance. The branch-classifier mechanism reproduces on demand. Q3 *collapses from
  per-map to per-class* for every system expressible as an equality constraint — which is most of
  physics, every equilibrium, every conservation law. Large achievement, named.
- **Discriminant = fold `[ESTABLISHED]`** — the load-bearing bridge. For polynomial `F`, the
  discriminant locus equals the projection of the geometric fold (elimination theory; resultant of
  `F`, `∂F`). Analytic and algebraic coupling are not analogous — they are the **same object** read
  in two languages. This is the bridge from c001 (analytic instance) to the algebraic/discriminant
  instance as one future campaign.
- **Periodicity is a third signature `[ESTABLISHED]`.** Stage B's monsters cycle at periods 906 /
  940 / 946 — exactly `p−1` for the primes 907 / 941 / 947 — because 2 is a primitive root mod each.
  The full battery is consistent: maximal cycle ⟺ prime where 2 is a primitive root (7 and 23 are
  primes that *don't* hit max; 255 = `2⁸−1` cycles at 8). `ord_2(p)` is the residue degree / order
  of Frobenius₂ in `Gal(ℚ(ζ_p)/ℚ)`, verified by factoring `Φ_p` mod 2 — every irreducible factor has
  degree `ord_2(p)`. **Every odd prime carries computational meaning** through the Galois axis.

This *does not* collapse into a single primitive by writing one F-equation. Putting representation-
exhaustion into the F-slot is a type error (dyadic length is the 2-adic valuation, nowhere
continuous in the real topology; no derivative, no curvature) — the documented pull-up in the probe.
Stratification keeps them as distinct stratum families on one substrate; the blind spot is their
intersection.

---

## C. The deep unification — corrected address, kept fenced

v1 reached toward an adelic / product-formula unification (one primitive at different places of ℚ).
Will's Stage-B question forced the correction.

**Withdraw:** the product-formula framing. Place norms `|r|_v` measure how a *fixed rational* sits
across completions and multiply to one. `ord_2(p)` is not a norm and enters no product; it lives on
a different axis.

**Adopt the right address `[CONJECTURE]` — Frobenius / Chebotarev / Artin.**
- `ord_2(p) = ` order of Frobenius₂ in `Gal(ℚ(ζ_p)/ℚ) ≅ (ℤ/p)*` `[ESTABLISHED]`.
- "2 inert in `ℚ(ζ_p)`" ⟺ "2 primitive root mod p" ⟺ Stage B's maximal cycle `p−1` `[ESTABLISHED]`.
- *How often this happens* is **Artin's primitive-root conjecture** — open unconditionally, a theorem
  under GRH with density ≈ 0.374. So the monster-cycle pattern bottoms out in a genuinely unsolved
  problem. The right amount of humility to write in.

**The fence — kept strict, just moved to the right wall.** "Periodicity is governed by Frobenius
across cyclotomic fields" is `[ESTABLISHED]`. "This Frobenius structure is the unification the two
boundary primitives were reaching for" is `[CONJECTURE]`, and needs the same work the product-
formula version needed: a specific object whose valuation data and Galois data are these two
functors, and a precise sense in which "the books balance" is its reconciliation law. Until that's
built, Frobenius/Artin is the navigation target, not a result.

---

## D. Coupling as holonomy, not metric (Axiom 12 in plain words)

The probe's most useful self-correction. The coupling is **holonomy of a connection**, not
Riemannian curvature; it needs a *transport rule*, not a metric. Cella already has the rule.

- A point in length-space is a *spent representation budget* — how much analytic / algebraic /
  symbolic resolution has been allocated. At that budget, Cella holds a cell `(v, ρ)` — a value and
  its exact residue.
- The per-axis refinement laws (first differences of the residue) are the **connection** — how each
  account transports under one more unit of spend.
- The coupling is the **failure to close around a unit plaquette**: spend, spend, un-spend, un-spend;
  any drift in the residue accounts is the curvature `[PLAUSIBLE / WELL-SUPPORTED]`. Already
  measured as route-holonomy in HR132; Cradle Arm M's `plaquette_probe.py` is its multivariate form
  `[ESTABLISHED on the tested class]`.
- "Accounts must balance" — the analytic / algebraic / symbolic readings of *one object* must
  reconcile. That closure replaces the metric. The boundary, locally, is "the books can't close
  within the resolution you've got."

Q3's refusal envelope, in this language, is the typed report that the plaquette failed to close
*and* the residual sits sub-detection — the resolution-floor-meets-coupling-degeneracy event,
typed.

---

## E. Maturity-tier line (what Tier A vs Tier B actually separates)

A consequence of the design doc §4 grading and the new structure: the recoverable region is
favorable on *all three* questions and the frontier is hard on at least one. Don't conflate them.

| Region | Q1 (factoring) | Q2 (⊕) | Q3 (envelope) | Tier |
|---|---|---|---|---|
| EFT recoverable region (`+ − × ÷ √ FMA`, all rounding modes, all widths) | decidable (below Richardson; rational equality is decidable) | additive over ℚ on the tested battery `[ESTABLISHED]` | sharp (dyadic death) `[ESTABLISHED]` | **Tier A — buildable now** |
| Special-value boundary (overflow / NaN / signed zero–infinity / underflow) | decidable (token branch) | token + protocol rule `[PLAUSIBLE]` | sharp by typed transition `[WELL-SUPPORTED]` | **Tier A — buildable now** |
| Multivariate coupling at scale; sub-Nyquist; subnormals; precision × step ladders | open | open (c002) | conservative-or-worse | **Tier B — frontier** |
| Cross-domain coupling (analytic ⊕ algebraic ⊕ symbolic) | open; Richardson localises into the symbolic axis only | one primitive via D⊕S=P `[PLAUSIBLE]` | per-class via D⊕S=P `[ESTABLISHED]`, with the symbolic axis inheriting Richardson | **Tier B — frontier** |

The conclusion the program should take: **the substrate's core arithmetic is the well-founded
near-term build, not blocked on Q2/Q3**. Q2 and Q3 are real and gate the *frontier* of cross-domain
reach. Building the core and chasing the frontier are concurrent, not sequential.

---

## F. c002 enrichments (carry into the campaign spec; not into the roadmap)

Concrete sharpenings for the carrier-experiment / refusal-envelope campaign:

1. **Falsifiability lives in composition.** Single-map reconstruction is trivially additive (set
   `ρ = T − v`); the experiment can only fail when the natural residue *composes*. Design the
   experiment around composing the non-additive map with its *structural* residue (the relative δ
   for a multiplicative map; the truncation cell for a continued-fraction map), never the always-
   available absolute difference.
2. **Name the ℚ-algebra outcome up front.** The likely landing is `[CONJECTURE]` neither additive-
   universal nor per-domain but **graded-universal over a ℚ-algebra** — one carrier, reconstruction
   by `+` *and* `×`. Naming it lets the campaign distinguish one-spine-as-algebra from genuine
   family; not naming it reads "not additive" as "family" and stops short.
3. **Classify composed gates, not just single Φ.** The probe's hardest point: the conical blind spot
   is float × geometry, a *composed* gate. The refusal-envelope arm should classify the composition
   of two gates (e.g. coupling-degeneracy × representation-exhaustion) at least once, because that
   composition is where Cella actually spends its life.
4. **Use c001's signed `K_G` object as the additive control.** Tensor carrier `ℚⁿˣᵐ`; runs beside
   the non-additive probe under the same `value + residue == TRUE` identity; the campaign becomes a
   *contrast* rather than a single shot. (Not "hygiene" — it's the baseline.)
5. **Sequenced first probe: relative-error / multiplicative.** Minimal departure from additive;
   commutative; stays exactly in ℚ; asks the cleanest version of the question. Continued-fraction /
   Möbius second (tests non-commutativity, has repo precedent in the coupling-holonomy CF axis).

---

## G. What this companion explicitly does *not* touch

- **c001.** Frozen-by-design. The discoveries above either confirm c001's existing structure
  (K11 = "refuse on approach, don't certify at the degenerate point"), are at a different tier
  (the refusal envelope), or are out of scope (representation-exhaustion is absent from c001 by
  construction; it runs in exact ℚ with no working-precision floor). No c001 fixture, kill, or
  claim is owed an addition. Holding that line is the discipline working.
- **Stage B / HR133.** Already closed. Cited above as the source of the periodicity signature; not
  reopened.
- **Specific Tier A2 / A3 map choices beyond §F**. The stress-test teams design and select; my
  job is to constrain the design honestly, not to pick the maps.

---

## H. Provenance

The technical content above is sourced from, in order:

- `CELLA_DESIGN_DOCUMENT.md` (v0.1-draft 2026-06-13) — the three primitives, the §4 don't-pay-twice
  argument, Q1/Q2 as originally posed, the coverage envelope.
- `Cella_Dyadic_3_axis_probe` (13 Jun transcript) — Q3, the inhabitation ladder, the two-primitive
  distinction (coupling-degeneracy vs representation-exhaustion), the per-class collapse, the
  discriminant = fold bridge, the connection/holonomy reframe replacing the metric, the type-error
  pull-up against putting dyadic length in the F-slot, the adelic / product-formula `[CONJECTURE]`.
- `Three_Channel_KG_Strong_Spec.md`, `Canonical_Invariant_Reduction_Theorem.md`, c001 merged spec
  — the analytic instance of the coupling-degeneracy primitive; the signed three-channel object as
  the additive control.
- `results/precision_flow/stage_b/STAGE_B_REPORT.md` + manifest — the periodicity signature; the
  `ord_2(p) = p − 1` pattern at 907 / 941 / 947; cross-checked against the full 15-denominator
  battery and the cyclotomic factorisation in my own engine, both confirming the Frobenius
  interpretation.
- The branch-classifier reproduction on a clean √-branch (this conversation) — confirming the
  structural detection mechanism.

Every grade marker above is mine and traceable to one of these sources or to an independent exact-ℚ
verification I ran.

---

*Charter line, carried: Cella maps where the classical world has been confidently wrong — and the
probe is only ever allowed to be uncertainly right.*
