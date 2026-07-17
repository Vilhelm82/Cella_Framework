# P2 — Corrected Direction: the `typed_refine` Kernel (supersedes the gap-bound-lemma)

*Replaces the §4 framing of `certified_precision_spine_P2_briefing.md`. Date 2026-06-05.
Derivation-mode; primary sources checked, not trusted.*

---

## 0. What changed, and why

The gap-bound-lemma draft tried to **generalize a proof** — a per-function lower bound on
`|log x − boundary|`, lifted from Leppälä–Matala-aho–Törmä (LMT, arXiv:1609.07076). I read the actual
PDF and ran the numbers. Two of its three claims are literally correct (the `μ=2` exponent *for fixed
`s/t`*; the factor `8γ²|s|(4tζ(N)+6t+s²)` is verbatim linear in `t`). But the application is a **regime
error, and it's fatal to the `O(p)` headline**:

- Correct rounding forces the midpoint `d = s/t` to be pinned to `~p` bits, so `s ~ 2^p`, `t ~ 2^p`,
  **and** the approximant denominator `N ~ 2^p` — all scaling together. LMT is a *fixed-`s/t`,
  `N→∞`* irrationality measure. In our regime `σ = 4tα/(es²) ~ 2^{-49}`, so `σ logN ~ 2^{-44}`, and the
  factor the draft said `→0` actually `→∞` (`z(y)/y → ∞` as `y→0⁺`). The exponent of `N` is not `≈2`;
  it is `2 + 2^{50}`. Vacuous. And LMT's own hypothesis `N ≥ N₁` needs `log N₁ ~ 2^{51}` — astronomically
  unmet at `log N = 36`. §3's `n* ~ 2^p` explosion was not killed; it reappears as LMT's `n̂ ~ ζ(N) ~ 2^p`.

**Honest standing of the per-function-proof route:**
- A proven finite depth *does* exist via **Bundschuh (1979)** (holds for all `N ≥ 1`, no threshold) —
  but `m(p) = O(p²/log p) ≈ 2240 bits` at `p=53`. Super-linear, not `O(p)`.
- The clean `2p` ("double the bits") is **real but empirical** — Lefèvre–Muller / CORE-MATH *search*,
  not a theorem.
- A from-theory `O(p)` uniform-in-`s` bound appears **genuinely open**.

**Conclusion:** generalizing a *proof* is a treadmill (open for `log`, open again for `exp`, `sin`,
`pow`). **Generalize the refinement *mechanism* instead.** That is the corrected P2.

---

## 1. The object to generalize: `typed_refine` (the Ziv kernel)

Split one conflated question into two:

**(A) Is *this emitted value* correctly rounded?** Compute `f(x)` in an **enclosure** `[lo, hi]` at
working precision `m`. If `[lo, hi]` does not straddle the rounding boundary `d`, the correctly-rounded
result is *determined* (round either endpoint to `p` bits). This is **PROVEN per value, with zero
transcendence input** — the enclosure is a finite composition of substrate operations with rigorous
error propagation. This is the V4-honest core: the primitive *constructs and verifies* each answer, or
it refuses.

**(B) Does the loop provably terminate?** The *only* place a gap bound is needed. **Bundschuh** answers
it: the loop halts by `m = O(p²/log p)`. Ugly, but proven, all-`N`, no threshold.

Together: **the primitive provably emits correctly-rounded `f(x)` or honestly refuses (A), and provably
terminates (B).** That is `proven_refinement = True`, earned — *without* the open `O(p)` problem. And in
practice the enclosure resolves at `~2p` (the true gap is `~2⁻²ᵖ`), so the Bundschuh ceiling is a
worst case the loop essentially never reaches. **Fast in practice, proven in the worst case.**

The open `O(p)`-from-theory bound demotes from *blocker* to *worst-case-ceiling optimization*.

---

## 2. Architecture: one kernel + thin per-function evaluators

```
typed_refine(eval_atom, x, required_precision p) -> TypedResult
    loop m = p + guard, 2p, ... up to Bundschuh ceiling:
        [lo, hi] = eval_atom(x, m)              # rational enclosure, width <= 2^-m
        d        = rounding boundary for p-bit output near [lo,hi]   # via typed_ulp scale
        if hi < d or lo > d:                    # enclosure on one side -> determined
            return  REFINED_CORRECTLY_ROUNDED(round(...), m_used)
        m *= 2                                  # straddles -> refine
    return  REFINED_BUDGET_EXCEEDED              # honest typed refusal (never a guess)
```

- **`typed_refine`** is function-agnostic. Built once.
- **`eval_atom`** is the only per-function part: "evaluate me at precision `m` with a proven error
  bound." The *easy, constructive* half. `log`, `exp`, `sin`, `pow` are all instances.
- `typed_log = typed_refine(log_eval, x, p)`; `typed_exp = typed_refine(exp_eval, …)`; etc. The whole
  CONSTRUCT_TO_TOLERANCE class collapses to one kernel + thin evaluators.

Status family (new, `RefineStatus`): `REFINED_CORRECTLY_ROUNDED`, `REFINED_BUDGET_EXCEEDED`
(and the input-domain refusals inherited from the evaluator: e.g. `log` of `x ≤ 0`).

---

## 3. The V4-native `log_eval` — and why AX11-002 closes *for real*

The evaluator must NOT call `math.log` (that is the AX11-002 drift, and it would re-import
named-mathematical content under Axiom 11). Build the enclosure from scratch in **exact rational
arithmetic** (`Fraction`) — already standard in V4 eval-layer (the dial, W(k), subnormal-C all use it):

- Argument-reduce `x = m·2^e`, `m ∈ [1,2)`. `log x = log m + e·log2`.
- `log m = 2·atanh(z) = 2(z + z³/3 + z⁵/5 + …)`, `z = (m−1)/(m+1) ∈ [0, 1/3)`. Geometric-rate
  convergence (`ratio z² ≤ 1/9`), so `~m/3` exact-rational terms reach width `2⁻ᵐ`.
- Partial sum `S_k` (exact rational, all positive terms) + **proven remainder bound**
  `R_k ≤ 2·z^{2k+3} / ((2k+3)(1−z²))` ⇒ enclosure `[S_k, S_k + R_k]`.
- `log2` precomputed once to the working enclosure (same series at a fixed point), a CONSTRUCTED
  constant — not a hardcoded literal.

This makes `log_eval` a **finite construction with a certified remainder** — exactly what
CONSTRUCT_TO_TOLERANCE *means*. No `math.log`, no `mpmath`. So `typed_log` built this way **closes
AX11-002 for real** (removes the 5 raw `math.log` substrate sites by giving them a constructive typed
log to consume), where the witnessed-libm wrapper would only have relabelled the drift.

Bonus: the earlier "hard-to-round of a *sum* (`log m + e·log2`) doesn't decompose" worry **dissolves** —
the enclosure is on the *final* value; the loop just narrows `[lo,hi]` of `log x` until the boundary is
resolved. No decomposition of hardness required.

---

## 4. Scope against the substrate we already have

**Reuse (no new derivation):**
- `typed_ulp` — locate the rounding boundary `d` and the output ulp scale.
- `required_precision.py` (P1) — `typed_refine`'s termination ceiling *is* the composition-floor link:
  required output `p` → working `m` via the (Bundschuh) gap bound. A CONSTRUCT_TO_TOLERANCE atom with a
  registered proven termination ceiling sets `proven_refinement = True` → the P1 terminal predicate
  fires **PROVEN**.
- `closure_grade.py` (P0) — `typed_log`'s lineage (`typed_refine` + `log_eval` + rational ops, all
  CONSTRUCTED) grades the closure **PROVEN**.
- `AtomKind` / `LeafKind` — `log_eval`: `atom_kind = CONSTRUCT_TO_TOLERANCE`, `leaf_kind = CONSTRUCTED`
  (it is built from substrate, not a measured/witnessed table).
- Exact `Fraction` enclosure — consistent with established V4 eval-layer practice.

**New, to build:**
- `typed_refine` kernel (the loop + rounding test + `RefineStatus`).
- `log_eval(x, m)` — rational `atanh`-series enclosure with proven remainder.
- A registered **termination ceiling** for `log` (Bundschuh constant — see open items).

**Layering / authorization:**
- `typed_refine` composes an evaluator (higher-order) → it is a *composition*, not an atom. Candidate
  homes: prototype in **harness/eval-layer** first (as we did with `closure_grade` / `required_precision`,
  non-substrate, in-scope), prove the pattern, then promote to a substrate primitive (likely L1.5/L2,
  per GAP-009 composition lives above atomic L1). Promotion = substrate edit → axiom-check + per-edit
  authorization.
- `log_eval` is a CONSTRUCT_TO_TOLERANCE **atom** (L1) → substrate primitive → authorization when promoted.
- Recommend: **build kernel + `log_eval` in eval/harness first, fully tested, then authorize promotion.**

---

## 5. Axiom check (the corrected direction)

- **Axiom 1 / 6** — emits a typed, enclosure-*verified* correctly-rounded value (or refuses); zero is
  measured/proven, correct rounding is proven by the enclosure not the float. ✓
- **Axiom 3** — the rounding-test-or-refuse and the precision budget are explicit, declared. ✓
- **Axiom 11** — the enclosure is **constructive substrate** (rational ops + a certified series
  remainder); transcendence theory (Bundschuh) enters *only* as the termination-ceiling domain
  articulation, graded against literature; CORE-MATH worst cases are the *oracle* that checks practical
  termination, never a design/value source. No `math.log`, no `mpmath`. ✓ (and AX11-002 closes)
- **Axiom 12** — refinement composes registered substrate ops; correctness derives from the enclosure;
  the lineage traces to atoms. ✓

Verdict: the direction *honors* the axioms (it is the constructive, honest realization of
construct-to-tolerance). No conceptual block.

---

## 6. Build order + honest open items

**Order:**
1. `log_eval(x, m)` rational `atanh`-series enclosure + proven remainder bound. Test against a trusted
   high-precision oracle (offline, grading-only) for enclosure validity at many `(x, m)`.
2. `typed_refine` kernel: loop + exact rounding test + `RefineStatus` + budget refusal.
3. `typed_log = typed_refine(log_eval, …)`; verify correctly-rounded vs CORE-MATH/Lefèvre–Muller worst
   cases (oracle: agreement = pass; disagreement = bug in *us*).
4. Wire to P1: register `log`'s termination ceiling; confirm the terminal predicate grades PROVEN.
5. Promote kernel + `log_eval` to substrate (authorized); rewire the 5 AX11-002 `math.log` sites.
6. Replicate for `typed_log2`, then `exp`/`sin`/`pow` as further `eval_atom`s (the generalization payoff).

**Open / to-nail (none of these block the kernel):**
- The Bundschuh **termination ceiling constant** — my `~2240 bits` is a back-of-envelope from the LMT
  comparison formula; nail it properly before it goes in the certificate (same discipline we applied to
  the draft). It is only a *ceiling*; the loop runs at `~2p`.
- The `log_eval` **remainder bound** — write the clean proven tail bound; verify the enclosure never
  excludes the true value (interval-validity tests).
- **Performance** — exact-rational at high `m` is slow; correctness first, optimize later (the structure
  is precision-doubling, so practical `m ≈ 2p` keeps it bounded).
- The tight **`O(p)`-from-theory** bound stays open — now a worst-case-ceiling optimization on an
  already-PROVEN, already-shippable primitive, not a gate.

---

## 7. Status mapping (how `typed_log` earns PROVEN)

| ingredient | grade | basis |
|---|---|---|
| each emitted value correctly rounded | **PROVEN per value** | enclosure rounding-test (constructive) |
| loop terminates | **PROVEN** | Bundschuh ceiling `O(p²/log p)` (all `N`) |
| lineage clean | **PROVEN** | `closure_grade`: all leaves CONSTRUCTED |
| meets required precision | **PROVEN** | P1 terminal predicate, `proven_refinement = True` |
| practical depth | `~2p` | empirical (Ziv resolves at the true `~2⁻²ᵖ` gap); CORE-MATH oracle-checked |

`typed_log` grades **PROVEN**, ships now, and the open Diophantine bound only ever tightens the worst-
case ceiling. The spine's thesis holds end to end: `typed_sqrt → PROVEN` (mandated atom),
`typed_log → PROVEN` (constructed + enclosure-verified + provably terminating), and the type system
decided both.
