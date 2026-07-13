# CV HANDOFF — 2026-07-09
## Curvature Valence — resume state (read after README.md + LOG.md)

Durable doctrine is in Claude's memory (master quadric, intrinsic gauge, the
engine-ladder). This file is perishable STATE only. Bootstrap order for a fresh
session: README.md (the rig) -> LOG.md (append-only spine, last GATE = where we
stand) -> this file -> CLAIMS.md.

---

## CURRENT POSITION: chartered, Stage-0 scripts written, NOTHING RUN UNDER GO

- ENTRY 001 CHARTER signed (Will, 2026-07-08). Log clean at 001.
- CLAIMS.md empty — nothing graded, correct.
- Stage-0 verify scripts exist but have NOT been run under GO:
  - verify/cv_e1_lame_formula.py — E1 Lame diagonal scalar-curvature formula.
    **BLOCKER:** the E1.2 n=4 fixture is computationally OBESE (quadratic Lame
    coefficients -> Christoffel/Ricci expansion swells for minutes then
    collapses). Lighten to LINEAR coefficients before running. This is the
    ruling Will still owes. E1.1 (n=3, general) is fine.
  - verify/cv_e2_canonical_gauge.py — E2 boundary robustness + metric-distance
    gauge (parity R·d^2 = -m(m+5)/4 pure number; generic rate 3/2).
- No RESULT / CLAIM / GATE entries beyond the charter. First real action is a
  GATE entry, then Stage-0 batteries (twice, sha256 hashes into a RESULT).

## THE MATH SPINE (verified in-session, independent of the scripts)

- **Master quadric** C(p) = -1/2( sum p_a^2 + sum_{a<b} p_a p_b - (p0+2) sum p_a ).
  ONE object doing three jobs: single-face monomial coefficient; both corner
  vertex coefficients (per-face evaluation); the cancellation condition (its
  vanishing locus). Derived twice independently (single-face germs; Will's
  pfc_test3 corner rule) — verified identical. C(2,-2,...) = -m(m+5).
- Vanishing locus contains: generic faces (p_a=0), flat cones, and scalar-flat
  isotropic exponents p_a = 4/(m+1) (metric dr^2 + sum r^(4/(m+1)) dy^2 is
  R≡0 exactly, verified — not just leading order).
- Intrinsic gauge (Lemma E2): parity faces R·d^2 = -m(m+5)/4 (pure number, B
  absorbed); generic faces intrinsic rate d^(-3/2). This is the coordinate-free
  form that kills the "pole order is a chart artifact" criticism by definition.
- Cross-checks (Cella MCP, validated): corner_newton reproduces KN wedge
  max(4a-2, 4-2a), vertex coeffs A=-84 / B=-12, spectator non-polar.

## PENCIL ORDER (reorder allowed with a GATE entry + stated reason)

0 -> GATE -> B1 -> GATE -> (B2/B3 | A per gate) -> A(+tower, gated) -> C -> D -> CLOSE
Sweeps O1-O3 (Varchenko/Kouchnirenko, Dobarro-Unal, Kasner/horns) block Stage C
PREDICTs ONLY, not Stage B.

## B1 — THE CROWN EXPERIMENT (pre-named fork, do not run until frozen)

Question: across the KN spectator fan wall at a=1, does the measured wedge-edge
leading coefficient follow SECTOR weights or BALANCED weights?
- Sector (-6,0) one side, (-2,-4) other -> quadric gives -84 vs -28 (=2·-14).
- **P-A** follows sector weights (-28 family) -> would mean the PFC note's -84
  assignment is sector-mismatched (V1 edge lives in a>1).
- **P-B** follows balanced weights (-84 family).
- **P-C** neither -> KILL K2: conjectured composition law dies, the MEASURED
  law becomes the object. Every branch is a finding.
B2 = tunable-wall synthetic binomial spectator (wall at a=c; coefficient
transition tracking c = a real phenomenon). B3 = polar-spectator extra-facet
probe.

## KILLS (armed): K1 oracle OVERLAP-FUNDAMENTAL -> pivot to extension.
K2 B1=P-C -> composition law dead. K3 nondegeneracy statable only as tautology
-> classification retreats to case list. K4 tower level-2 non-universal -> tower
dies, counterexample recorded. K5 theorem = change of variables from a swept
result -> KNOWN-adjacent, never claimed.

## NEW THIS SESSION — the two-scale bridge (worth a NOTE entry when resumed)

CV's valuation calculus and CCAF are ONE geometry at two scales: valuation =
residual order, intrinsic gauge = ULP, deletion walls = dyadic crossings. The
CV instruments (curvature_valuation tool: germ -> order/coefficient/Newton
support with deletion walls, rational exponents, spectator-refusal) ARE what
CCAF needs to read the dyadic wall on computation surfaces. CV Stage A/C tooling
and CCAF share a bench. Caution: the residual-flow half of that bridge is banked
as precision_flow HR133 — cite, don't re-derive (see root HANDOFF §10).

## FIRST ACTIONS ON RESUME (all need Will's GO)
1. Rule on the E1.2 fixture (lighten to linear) -> run Stage-0 x2 -> RESULT
   entry -> promote E1/E2 to computer-verified in CLAIMS.md.
2. OR skip straight to B1 per the pencil (it's a measurement, valid regardless
   of Stage-0) — but B1 needs its PREDICT entry committed BEFORE the battery.
Nothing canonical until Will signs. Repo discipline: no execute/commit without GO.
