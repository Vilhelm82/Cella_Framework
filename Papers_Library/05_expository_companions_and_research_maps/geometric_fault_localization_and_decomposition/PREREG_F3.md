# STAGE F3 — CL-F3 FIBER COMPLETENESS AT n=5, LOCAL TIER (FROZEN pre-battery, S-2026-07-05b; Will: "CL-F3 - GO")
Brief-Stage-B proper (re-queued at v4.10, now opened). CL-F3 as staked in
the flagship brief is the summit, deliberately expected PARTIAL. THIS stage
grades the LOCAL (differential) tier only, declared up front: ranks of exact
differentials at pinned generic rational points. The GLOBAL tier (distant
same-fiber points, degenerate strata) is a separate future freeze — banked
context: the P-F3 two-Cayley hunt is EXHAUSTED-NEGATIVE for rational
all-m2-tied witnesses (9/9 slices), so no cheap global witnesses exist on
the tested chassis.

## Objects (imported conventions — witness_battery.py is the authority)
Pair module dim 10 at n=5; gauge quotient O_of (linear; zero-diag section);
σ-detector ê_r(O) := Ê_r(sym_from_pairs(O, diag=0)), r = 1..4 (bordered-
minor sums); conjugation tangents δO_X = O_of(HX − XH), X ∈ Λ²(g^⊥) per the
fixtures rule (6 generators; well-defined on the quotient since Rᵀg = g).
Invariant vector = ALL S₅-invariants of degree ≤ 3 on the pair module:
deg-1 (dim a₁), deg-2 (dim a₂ = 3, CERTIFIED P-F1), deg-3 (dim a₃, measured
in-battery by exact Molien/cycle-index and cross-checked against the
orbit-sum span rank — internal equality is a MUST gate).

## Predictions (FROZEN; graded mechanically; clauses embedded)
| id | statement | class | prediction |
|---|---|---|---|
| PF3.0 | gates: pins; clauses; projector ranks (1,4,5) + idempotency + partition of identity; a₂ = 3 by Molien; a₃(Molien) == rank(orbit-sum span); conj-tangents lie in ker(dê) exactly (σ conj-invariance seen by the differentials), all fixtures | sanity | MUST HOLD (else K-F30, no verdicts) |
| PF3.1 | rank of stacked dê_r (r=1..4) at each fixture = 4 (⟹ σ-fiber smooth of dim 6 locally) | discriminating | HOLDS at all 3 fixtures — moderate-high (generic points); any deficiency = record + route (degenerate stratum sighting) |
| PF3.2 | rank of the 6 conjugation tangents δO_X at each fixture = 6 (⟹ conj-orbits generically OPEN in σ-fibers — the brief §4 banked side-question) | discriminating | HOLDS — moderate (dim so(4) = 6 = expected fiber dim); rank < 6 = structural surprise, record + route |
| PF3.3 | THE LOCAL SUMMIT CLAUSE: rank of the degree-≤3 invariant differentials restricted to the fiber tangent (ker dê, dim per PF3.1) = 6 at each fixture ⟹ the invariant vector is locally separating on the σ-fiber at the pinned strata | discriminating | OPEN — this is the discovery clause; PASS ⟹ CL-F3 local tier CERTIFIED-at-points; rank < 6 ⟹ the deliberately-expected PARTIAL: deficit = 6 − rank NAMED per fixture, feeds the degree-ladder decision (brief §10 B3) |
| PF3.4 | deficit of the degree-≤2 layer: rank of deg-≤2 invariant differentials on the fiber tangent, per fixture (upper bound 4 by count: 1 + 3 rows) | measurement | record-only — quantifies degree-2 insufficiency exactly (Part III sibling number) |

## Kill conditions (armed)
- **K-F30:** any PF3.0 gate fails ⟹ HALT, no verdicts.
- **K-F31:** conj-tangent outside ker(dê) at any fixture ⟹ theory/pipeline
  defect (σ conj-invariance is PROVEN) ⟹ HALT.
- PF3.1/PF3.2/PF3.3 sub-threshold ranks: NOT kills — recorded verdicts
  routed to Will (PARTIAL-with-named-deficit is a designed outcome of this
  stage). No widening, no post-hoc basis changes.
- Envelope 1200 s / 8192 MB; byte-stable ×2 mandatory.

## Pins (Rule 1.9) — freeze_pins_f3.sha256
This file; fixtures_f3.json; ../witness_battery.py (object-convention
authority, read-conformed); evals/dbp_involution/rep_utils.py. Battery
refuses on sha mismatch (REFUSE_MISMATCH) or clause drift (CLAUSE_DRIFT).
role=probe + ledger. Probe: ranks by exact Fraction Gaussian elimination.
Referee (independent): same matrices ranked by sympy; must agree, every
matrix.

## Status moves (frozen)
PF3.0–PF3.3 all PASS ⟹ CL-F3 → **LOCAL COMPLETENESS CERTIFIED at pinned
generic strata** (ledger move NOT_YET_PROBED → PARTIAL-by-scope: local tier
closed, global tier open by design); PF3.2 PASS additionally closes the
brief §4 side-question (orbits open in fibers) at the certified points.
PF3.3 rank < 6 ⟹ CL-F3 → PARTIAL with deficit named; degree-ladder
(climb to 4) decision routes to Will with the wall data. PF3.4 always
recorded. Nothing canonical without Will's sign-off.

frozen: true · author Claude-session · substrate [BOX] · S-2026-07-05b
