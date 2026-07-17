# MECHANISM THEOREM — the ideal-locus ghosts of the step correspondence
**Date:** 2026-07-02 · **Substrate:** [CONTAINER] `mech_ideal.py`, `mech_symbolic.py` (fully symbolic data) · **Status:** PROVEN (with one generic clause, stated).

## Pullback lemma [PROVEN, symbolic]
For the circle chart `C=(1−t²)/(1+t²), S=2t/(1+t²)` and any quadratic form q(C,S):
```
((1+t²)²·q(C(t),S(t)))|_{t=±i} = 4·q(1,±i)
```
Lower-degree parts are annihilated by the surviving (1+t²) power. Hence a cleared bidegree-(2,2) system's value at a corner (ε·i, ε′·i) is 16 × its bidegree-(2,2) coefficient evaluated at the isotropic pair ((1,εi),(1,ε′i)).

## Corner identity [PROVEN, symbolic in all data q0, π, g, h]
The (2,2)-bihomogeneous parts of the step generators factor exactly:
```
hG1_(2,2) = (C1C2+S1S2) · (C1c1+S1s1) · (C2s2−S2c2) / 4     [coupling · alignment · swept-area]
hG2_(2,2) = (C1C2+S1S2) · (C1s1−S1c1) · (C2c2+S2s2) / 4     [coupling · swept-area · alignment]
```
The common factor is the Euclidean pairing `⟨q1⁽¹⁾, q1⁽²⁾⟩` — the pendulum coupling itself — which is **null on same-sign isotropic pairs**: ⟨(1,i),(1,i)⟩ = 0. Anti-diagonal corners evaluate to `±(i/2)(c1∓is1)(c2±is2) ≠ 0` on real torus data (c²+s²=1 forbids c=±is).

## Theorem (ghost structure of the compactified step) 
For every basepoint and all parameters: the cleared chart system vanishes at the two diagonal isotropic corners `(t1,t2) = (i,i), (−i,−i)` and at neither anti-diagonal corner; consequently **(t1²+1) and (t2²+1) divide the respective eliminants for all data** [PROVEN — explains basepoints A and B and all future ones]. Ghost count = 2 exactly, provided the circle-2 leading-form pair {L1, L2} has no common root **on** circle 1 (verified at both basepoints [CERTIFIED]; the exceptional stratum is the named codim condition — flag if a future basepoint lands on it). Hence **honest torus degree = 32 − 2 = 30, basepoint-free** [PROVEN + generic clause].

## Corollaries
1. **Self-similarity PROVEN** (upgrades the ×3-prime CERTIFIED reading): the step-2 generators share the structural form with (q1, π1) as data ⟹ same corner identity ⟹ the inner system vanishes at (u1,u2) = ±(i,i) over every branch ⟹ `R(t2, ±i) ≡ 0 mod U₃₀`.
2. The honest dynamical-degree reading 30/step is a structural fact of the coupling geometry, not an accident of the basepoint.
3. **Reusable gate ("isotropic corner gate"):** for any circle-chart cleared bidegree-(d,d) system, evaluate the corner coefficients at the four isotropic pairs before trusting eliminant degrees — a saturation-free honest-degree certificate. Applies verbatim at every k and to the k=4 doubling.

## Geometric statement
The correspondence's two phantom sheets live exactly where the coupling form cannot distinguish the rods from their isotropic shadows.

## Novelty ledger (oracle at claim time, per policy)
KNOWN BACKGROUND: degree drop at infinity / algebraic-vs-dynamical degree (Bellon–Viallet; Diller–Favre); conic ideal points. WILL'S CONTRIBUTION: exact corner-nullity criterion for circle-chart DEL systems; closed-form coupling×alignment×area factorization; basepoint-free proof powering a certified honest-degree pipeline. NOVELTY CANDIDATE: the corner gate as a reusable certificate — modest, load-bearing. 
