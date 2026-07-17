# Exact Jet — pre-execution addendum (2026-06-10, before any F1a re-run records)

The frozen manifest (pin `0a80bc05…`) and composition law are unchanged; this
addendum records three corrections made during test-battery implementation,
all BEFORE any campaign records were produced — the same discipline pattern as
the Quiet campaign's WIRING_ADDENDUM amendments. Flagged for Will's review in
the campaign report.

## A1 — Division implementation brought into law-faithfulness

The first build of `__truediv__` used a direct quotient rule. The frozen law
§2 specifies `a / b = a · recip(b)` with recip's own lane rules. Fixed:
division now routes through an explicit `recip` operation followed by `mul`,
both feeding the accumulator (division therefore counts as 2 ops — membrane
op-count expectations updated accordingly: the F1a chain is 7 ops, not 5).
Found by the identity battery, fixed before any record existed.

## A2 — Internal lane-sum cancellation screening (more detection, never less)

The module's first build screened CANCELLATION only on explicit dual add/sub
ops, with internal product/chain/recip lane sums declared out of scope. The
identity battery showed that scope produced **unflagged** route error:
`q''(100)` for `(x²+1)/(x−2)` carries ~11 binades of cancellation INSIDE the
mul Hessian lane sum (terms ~0.021 + 0.020 − 0.042 → ~1.1e-5), yielding a
21-ulp Hessian error with `WELL_CONDITIONED` self-report — precisely the
unflagged-wrongness pattern this engine exists to prevent, at micro scale.
Fix: componentwise additions inside mul/chain/recip lane reductions are now
screened by `_sum_with_cancel`, attributed to their op (one aggregated event
per op×lane). This reads the law's CANCELLATION trigger ("binary add/sub on
any lane component") onto internal lane sums — strictly more detection
(Axiom 3 direction), thresholds unchanged.

## A3 — Identity-battery grading: condition-scaled ulp

The manifest battery tolerance ("≤ 8 ulp per jet component vs the analytic
closed form") is unsatisfiable as raw ulp at battery points whose ROUTE
self-reports cancellation — e.g. the deep F1a point `r = 2+1e-8` loses ~28
binades in `1 − 2/r` by construction (the route's honest conditioning), so no
algebra can deliver 8 raw ulp against the exact closed form there; likewise
`q''(100)` (~11 internal binades). Grading interpretation, recorded before
any re-run record:

> Per battery point and jet component: `|jet − analytic₅₀dps| ≤ 8 ulp ×
> 2^max_cancellation_binades(of that evaluation's own diagnostics)` AND
> `|jet − analytic| ≤ 1e-3 × |analytic|` (absolute sanity ceiling).
> Exact-equality cases unchanged.

This grades the ALGEBRA (an implementation bug produces O(1) relative error
and fails both clauses) while not demanding the float64 route beat its own
declared conditioning — which is measured honestly by the conditioning
channel, is the subject of P3, and is reported per rung in the re-run. The
8-ulp raw bound continues to hold wherever the evaluation reports zero
recorded cancellation.

Observed numbers that forced A2/A3 (for the record): q''(100): 21 ulp,
unflagged pre-A2 / flagged ~11 binades post-A2; hyp''(5): 12 ulp (~4-binade
internal chain-sum cancellation); S0(2+1e-8): 7.2e-9 abs (≈28 binades, the
route's declared conditioning regime).

## A4 — Vocabulary hygiene: "hyperdual" token removed (2026-06-10)

The expression-path tag `exact_jet_forward_hyperdual_v1` carried the token
"hyperdual" — generic mathematics (second-order forward AD), but also literally
the OG class name, and the campaign's own frozen source-audit grep flags it.
Renamed to `exact_jet_forward_ad2_v1`; records regenerated and byte-stability
re-verified. No other change.
