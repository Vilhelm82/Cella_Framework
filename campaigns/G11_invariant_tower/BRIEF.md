# G1.1 CAMPAIGN — the invariant tower

**Status:** OPEN · drafted 2026-07-06 · engine gate under the three standing rules +
DESIGN FREEZE. Mathematics inputs: RC-1 (channels, cross-route), RC-2 (normal form /
projection identities), gate_03 (QSqrt + the parity retrodiction), A-003 (the parity
law as tower optimality). The parity law itself enters here OPERATIONALLY (type-level
enforcement); its full analytic derivation in-repo remains an obligation noted at
A-003 — this gate certifies the implementation against independently derived pins,
and the two-route pin derivation is recorded in PREREG.

## Campaign goal

The σ tower (elementary symmetric functions of the principal curvatures of the
level hypersurface) as a certified, generic-n, parity-typed, refusal-typed engine
capability on the analytical surface corpus — the first odd-sector (√q) computation
in the engine.

## Target claim

For a codim-1 block with exact jet (g, H), g ≠ 0, the engine emits
σ_1..σ_{n−1} exactly: even orders in ℚ, odd orders in ℚ·√q typed as QSqrt at
radicand q (rational exactly when q is a rational square or the value vanishes);
gauge-invariant identically (P annihilates the gauge image); σ_2 cross-routed
against the labeled channel sum at n=3; certificates tiered.

## Freeze compliance

Blocks refuse len > 1 (`CODIM_UNSUPPORTED`); generic-n linear algebra (projection +
principal minors — no n=3 anywhere); channel comparison uses the G1.0 n=3-fenced
cross-check only; tier stated on certificates. Chart/regularity distinction pinned:
the tower requires only g ≠ 0 — component-zero gradients refuse the CARRIER, not
the tower (PREREG P3 asymmetry row).

## Battery

`tests/gate_11.py` against `PREREG.md` (frozen pre-implementation, sha below):
7-surface corpus incl. one n=4 row; parity typing; cross-route; gauge sweep; purity
wiring; refusals; certificates; three mutants (sign-flip, normalization,
radicand-context) that must fail. Kills K-1..K-3 armed (PREREG).

## Expected failure modes

Sign-convention drift (M1 exists for this — and note the mutant is INVISIBLE to the
even sector by design); pins derived from the implementation (they were not: two
independent routes + geometric sanity + two standing-certificate retrodictions,
all pre-freeze); q-square edge hidden by a corpus of non-square q's (monkey row
exists for this); n=3-only index bugs (sphere4 row exists for this).

## Output ledger

This BRIEF + PREREG (frozen) · `src/cella/tower.py` · `tests/gate_11.py` ·
ROADMAP G1.1 close · BOOT current-state · full-suite green ×2.

## PREREG freeze

PREREG.md sha256 (first 16 hex), frozen before any implementation code:
`b736cfb9d88e6957` — frozen 2026-07-06, committed ahead of all G1.1 implementation.
