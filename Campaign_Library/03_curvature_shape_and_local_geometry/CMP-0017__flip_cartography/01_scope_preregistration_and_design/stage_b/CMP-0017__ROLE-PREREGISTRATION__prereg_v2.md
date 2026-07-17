# STAGE B PREREG v2 — principal-branch amendment (flip_cartography)
**Status: FROZEN — grounding gate cleared S-2026-07-02 (Will: "Go" on the four-sentence statement: v2 adds the principal-branch discipline DF-7, restates PB.1 over the physical sheet, adds the ghost-sheet census; needed because KB.1 proved the v1 object was the 32-branch correspondence while the energy proof binds only the physical sheet; contributes the correct definition of the campaign deliverable). Immutable; amendments = new version.**
**Date:** 2026-07-02 · **Substrate:** [CONTAINER]+[BOX] · **Supersedes:** PB.1 of PREREG v1 (pin `c4875c25fb95a9dd`) per KB1_AUDIT.md D2 (REFUTED-BY-DERIVATION). v1 remains frozen as the record. Everything not named here is inherited from v1 unchanged: PB.2, PB.3, PB.4, KB.2, KB.3, primes (1073741789 / 1073741783 / 1073741741), object definitions, route, fences, discipline line.

## DF-7 — principal-branch discipline (new definition freeze)
```
Principal continuation of x0 on the rest slice: the solution q1 of the UNPINNED
one-step system {hG1, hG2, Phi1(q1), Phi2(q1)} obtained by Newton (mpmath, dps=60)
seeded at q1 = q0, subject to three armed gates:
  (g1) residual:     max |system(q1)| <= 1e-45
  (g2) motion:       ||q1 - q0||_inf <= B_mot := 20*h^2   (from rest, ||qdd|| <= 2g = 20;
                     bound is 2x the physical ceiling)     = 1/80 at h = 1/40
  (g3) contraction:  final Newton step <= 1e-20
Gate failure => point classified UNRESOLVED (banked in the census; never dropped).

Classification margin: mu(x0) := || (C2,S2)_principal - (-1,0) ||_inf.
  PRINCIPAL-FLIP  iff  mu <= g_class := 1e-20
  GHOST-SHEET     iff  mu >= 1e-6
  otherwise UNRESOLVED.  Separation ledger required: min(ghost mu) / max(principal mu)
  >= 1e10, else the whole classification is UNRESOLVED and the rung halts for audit.

Physical T_k := honest T_k restricted to PRINCIPAL-FLIP-classified points.
```
Tier discipline: classification verdicts are [gated-numeric, dps 60] with banked
margins; energy verdicts on witnesses remain exact (algebraic sign evaluation).

## Saturation rule (D1 fix, definition-level)
Honest eliminant := resultant with (i) the (1+x^2)-class corner ghosts stripped
(v1 PB.3 unchanged) and (ii) every factor dividing lc_t1(E1)*lc_t1(E2) removed —
BUT each removed lc-factor gets a fiber check in the flipped terminal chart
(terminal circle-1 pinned at (-1,0)); verdict per factor {pure artifact | carries
chart-infinity solutions} banked in the census. Silent removal is forbidden.

## Chart completeness (new, forced by the Weierstrass chart)
The initial-torus chart x_i = tan(theta_i/2) misses theta_i = pi. The principal
flip tongue at small k lives exactly there. Second chart, frozen:
```
(c2, s2) = ((u^2-1)/(u^2+1), 2u/(u^2+1)),   u = cot(theta2/2),  u = 0 <=> theta2 = pi
```
Every rung computes the honest eliminant in BOTH charts (x1,x2) and (x1,u);
components are matched on the overlap.

## PB.1' (replaces PB.1; same exact test, same kill)
Every PRINCIPAL-FLIP witness of every computed Physical T_k satisfies
`2*c1 + c2 <= 1` exactly. **KB.1 unchanged: any principal violation => HALT,
route to Will, audit.** Ghost-sheet violations do NOT fire KB.1 — they are PB.5 data.

## PB.5 (new instrument — measure, don't kill): ghost-sheet census
Per rung, per chart, per component: #real witnesses, #principal, #ghost,
#unresolved, margin extremes, ghost energy-violation count, removed-lc-factor
ledger with fiber-check verdicts.

## SP-1 (stated prediction, graded this rung — verify-before-assert)
(a) Every finite-grid witness on the (14,24) any-branch curve classifies GHOST;
(b) principal T_1 is nonempty and appears in the u-chart near u = 0;
(c) it respects the energy gate exactly (PB.1' passes non-vacuously).
Any clause failing is banked loudly; (a) or (c) failing routes to Will.

## Run discipline
Byte-stable x2 (independent runs, sha256 over the canonical results block must
match), suite exit 0, logs + script committed same session.
