# RESULT_TYPES amendment proposal — TypedResult composition law for dual (exact-jet) arithmetic

**Status:** PROPOSAL v1, 2026-06-10 — drafted for Will's approval at the Phase 1 stop of
`CAMPAIGN_EXACT_JET_PRIMITIVE.md` (Option B per Will's ruling). The normative
`RESULT_TYPES.md` is NOT modified by this document; on approval, this text (or its
approved revision) is applied there as a dated amendment, and the campaign tests
enforce it. Until then it binds the campaign only.

**Scoreboard rows served:** A6 (primary), A4 (indirect). Driver: HR130 FD floor.

---

## 1. The Membrane Rule (Will's ruling, condition 1 — verbatim contract)

> **Internal floats are lawful iff every dual operation feeds the accumulator and the
> boundary emits exactly one TypedResult — nothing crosses the membrane untyped.**

Operationally:

- The dual-number class (`_JetNum`) is **private** to the module. No public API
  accepts or returns it; `__all__` exposes only `exact_jet`, the value/status types,
  and declared constants.
- Every arithmetic operation on `_JetNum` (binary ⊕ ⊖ ⊗ ÷, unary sin cos exp log
  sqrt abs, pow-by-constant) reports to the evaluation's **event accumulator**
  before returning. There is no operator that bypasses it (enforced by test:
  the per-evaluation `n_ops` must equal the analytic operation count of a frozen
  battery expression, and the event stream must be byte-deterministic).
- The single boundary object is `ExactJetResult = TypedResult[ExactJetValue,
  ExactJetStatus]`. Lanes (value, gradient, Hessian), events, and condition
  diagnostics all live inside it. No second channel, no module-level state,
  no exceptions escaping (Design Principle 2: degenerate cases are typed
  refusals; the OG try/except-swallow pattern is the documented anti-pattern).

## 2. The dual algebra (what is being typed)

Second-order forward AD over n inputs: each node carries
`(v, g[0..n), H[0..n)×[0..n) symmetric)` in float64. Composition rules are the
standard truncated-Taylor laws (recorded here so the tests pin them):

- `a ± b`: lanes add/subtract componentwise.
- `a · b`: `v=va·vb; g=va·gb+vb·ga; H=va·Hb+vb·Ha+ga⊗gb+gb⊗ga`.
- `a / b`: `a · recip(b)`; `recip(b)`: `v=1/vb; g=−gb/vb²; H=−Hb/vb²+2(gb⊗gb)/vb³`.
- unary `u(a)`: `v=u(va); g=u′(va)·ga; H=u′(va)·Ha+u″(va)·(ga⊗ga)`.
- `pow(a, c)` restricted to **constant real c** (general `a^b` is written explicitly
  by the consumer as `exp(b·log a)`, so its event trail is visible, not hidden).
  **Note (Will's ruling 3):** the integer-power route and the `exp(c·log a)` route
  produce equal values with **distinct event fingerprints** — expected
  route-dependence (the B4 pattern: more routes, more fingerprints), not a defect.

## 3. Event taxonomy (the accumulator's alphabet — deterministic triggers)

Recorded events are facts about operations; the grading thresholds in §4 are a
separate, declared mapping. Recording is deliberately more sensitive than grading.

| event | deterministic trigger | payload |
|---|---|---|
| `CANCELLATION` | binary add/sub on any lane component where both operands are finite, nonzero, and `binade(max(|x|,|y|)) − binade(result) ≥ 2` (result nonzero), or the result is exactly 0 from nonzero operands (recorded as `binades_lost = "total"`/1075) | `op_index`, `lane ∈ {value, grad, hess}`, `binades_lost` (max over the lane's components) |
| `DIV_AMPLIFICATION` | division/reciprocal where the **measured lane amplification** `amp = binade(max output derivative-lane magnitude) − binade(max input jet magnitude across both operands)` satisfies `amp ≥ 2` (same record floor as CANCELLATION) | `op_index`, `lane` (grad/hess, whichever is worst), `amplification_binades = amp` — the severity IS the trigger quantity |

> **PRE-FREEZE AMENDMENT (Will's approval ruling 1, 2026-06-10, before freeze/pin):**
> the original draft triggered DIV_AMPLIFICATION on an absolute denominator
> threshold (`binade(|vb|) ≤ −20`). That is regime-bound to O(1) operands — a
> computation living uniformly at scale 2⁻³⁰ would false-trigger on healthy
> divisions, and one at scale 2⁺³⁰ would miss genuine amplification: the exact
> HR130 E-rule failure pattern (an absolute-magnitude gate masquerading as a
> conditioning signal). Replaced by the measured, scale-free lane amplification
> (output-vs-input binade growth, invariant under uniform operand rescaling),
> which was already the event's severity quantity — trigger and grading now share
> one currency, graded against the unchanged 60/150 strata.
| `DOMAIN_REFUSAL` | `log(v ≤ 0)`; `sqrt(v < 0)`; division by exact 0; `pow(v ≤ 0, non-integer c)`; **derivative-kink/pole at a defined value:** `abs(0)` (kink), `sqrt(0)` (g pole) — value exists, jet does not | `op_index`, `kind` — **terminal**: evaluation stops deterministically |
| `NONFINITE` | any lane component becomes inf/nan with no prior `DOMAIN_REFUSAL` (overflow / 0·∞ propagation) | `op_index`, `lane` — **terminal** |

Accumulator state = the ordered event tuple (evaluation order is deterministic) +
summary scalars: `n_ops`, `max_cancellation_binades` (per lane), `max_hess_amplification_binades`.
If more than `MAX_RECORDED_EVENTS = 64` events fire, the first 32 and worst 32 are
kept with an explicit `events_truncated_count` — truncation is itself recorded,
never silent.

## 4. Deterministic mapping: events → (status, validity, conditioning)

**Status** (module-local `ExactJetStatus`, eval-layer; registered into
`core/status.py` + LAYER_MANIFEST only at promotion):

| condition (checked in this order) | status | lanes emitted |
|---|---|---|
| `DOMAIN_REFUSAL` of kink/pole-at-defined-value kind (`abs0`, `sqrt0`) | `JET_DERIVATIVE_UNDEFINED` | `value` kept; `gradient`/`hessian` = None; `TypedRefusal` attached |
| any other `DOMAIN_REFUSAL` | `JET_DOMAIN_REFUSED` | all lanes None; `TypedRefusal` attached |
| `NONFINITE` | `JET_NONFINITE` | all lanes None; `TypedRefusal` attached; offending op/lane in the event |
| otherwise | `JET_OBSERVED` | all lanes present |

**Validity** (Axiom 4 — multi-field, mapped not vacuous):

| field | rule |
|---|---|
| `defined` | no `DOMAIN_REFUSAL` of the non-kink kinds |
| `finite` | no `NONFINITE`; all emitted lane components finite |
| `selectable` | `defined ∧ finite ∧ status == JET_OBSERVED` |
| `advanceable` | `= selectable` (jets feed downstream reconstruction directly) |
| `observable` | `= selectable` — deliberately NOT gated on conditioning (APPROVED, Will 2026-06-10). Rationale: HR130 measured the E-unsafe observability-style gate firing ~10 decades early; the quality signal belongs in the conditioning channel and the consumer's attribution layer, not in a validity hard-gate. **Consumer obligation (Will's ruling 2): consumers MUST consult `conditioning` before claim-grade use of any jet lane; `observable` ≠ endorsed.** |

**Conditioning** (the P3 channel — graded from the summary scalars; thresholds are
declared constants justified against the mantissa and the Quiet tolerance):

| `ConditioningStatus` | rule | justification |
|---|---|---|
| `WELL_CONDITIONED` | `max_cancellation_binades < 26` and `max_lane_amplification_binades < 60` (measured, per the pre-freeze amendment) | ≥ half the mantissa survives (rel floor < 2⁻²⁶ ≈ 1.5e-8) |
| `WARNING` | `26 ≤ cancel < 40` or `60 ≤ amp < 150` | less than half the mantissa survives but the remaining ≥13 bits still support the Quiet tol 1e-3 with margin |
| `ILL_CONDITIONED` | `cancel ≥ 40` or `amp ≥ 150` | ≤13 surviving bits → rel floor ≥ 2⁻¹³ ≈ 1.2e-4, within an octave of tol — the reading can no longer be trusted at the campaign's pre-registered tolerance |
| `SINGULAR` | set alongside any refusal status | — |

`Conditioning.notes` carry the deterministic strings
`max_cancellation_binades=<K>@op<N>:<lane>`, `max_hess_amplification_binades=<K>@op<N>`,
`n_ops=<N>`, `events_truncated_count=<N>` (when nonzero). The **quantitative** P3
channel is `ExactJetValue.condition_diagnostics` (per-lane numeric maxima + op
indices) — continuous, not just the three strata. On the F1a ladder the
`1 − 2/r` cancellation grows ≈ 3.32·k + 1 binades with rung k, so the channel is
predicted to stratify the ladder WELL → WARNING (k≈8) → ILL (k≈12); P3's mechanical
grading (manifest) keys on this.

**Provenance:** `inputs = the operating-point tuple`, `expression_path =
"exact_jet_forward_ad2_v1/<function_label>"` *(corrected 2026-06-10, addendum A4:
the original tag carried the token "hyperdual" — generic mathematics, but also
the OG class name, and the campaign's own frozen source-audit grep rightly flags
it; renamed for vocabulary hygiene before the records were finalized)*; the event
tuple lives in the value (it is data, not metadata commentary).

## 5. External schema — the stable contract (Will's ruling, condition 2)

```python
@dataclass(frozen=True)
class ExactJetValue:
    value: float | None
    gradient: tuple[float, ...] | None          # length n
    hessian: tuple[tuple[float, ...], ...] | None  # n×n, symmetric
    n_inputs: int
    n_ops: int
    events: tuple[JetEvent, ...]                # §3, bounded per MAX_RECORDED_EVENTS
    condition_diagnostics: JetConditionDiagnostics  # per-lane numeric maxima

ExactJetResult = TypedResult[ExactJetValue, ExactJetStatus]

def exact_jet(fn, values, *, function_label: str) -> ExactJetResult: ...
# fn: Callable[[tuple[_JetNum, ...]], _JetNum] — authored against the private
# algebra inside the membrane; values: the float64 operating point.
```

Consumers may depend on exactly: `(value, gradient, hessian, n_inputs, n_ops,
events, condition_diagnostics)` + the TypedResult envelope (status / validity /
conditioning / provenance / refusal). **Option-A migration path:** replacing the
internal float algebra with per-op typed scalars changes nothing above — the
`events` tuple is the designated extension slot (Option A enriches each event with
a per-op TypedResult reference; existing consumers ignore unknown payload fields).
**Option-A re-open trigger (recorded here and in the campaign report):** a consumer
demonstrating per-op granularity need — candidate: separator M2 per-route
provenance (`CAMPAIGN_SEPARATING_ESTIMATOR_DRAFT.md`).

## 6. What this amendment adds to RESULT_TYPES.md (on approval)

One section: "Composed-algebra results (membrane pattern)" — the Membrane Rule
(§1 verbatim), the event-accumulator requirement, the deterministic
events→(status/validity/conditioning) mapping obligation, and the rule that
module-local status families used at eval-layer must be registered into
`core/status.py` + LAYER_MANIFEST at promotion time. The exact-jet tables (§3–§4)
attach as the first instance.

## 7. Enforcement (tests, per brief)

`test_jet_typed_composition.py` asserts: the mapping table §4 case-by-case
(constructed inputs for each event kind and each threshold boundary ±1 binade);
membrane integrity (`n_ops` equals the frozen battery's analytic op counts;
private `_JetNum` not exported; no exception escapes — every degenerate battery
case returns a typed refusal); determinism of the event stream (byte-identical
across runs, `test_jet_determinism.py`).
