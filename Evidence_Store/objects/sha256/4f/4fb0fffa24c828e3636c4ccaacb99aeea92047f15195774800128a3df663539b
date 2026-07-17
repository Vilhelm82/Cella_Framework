# STAGE B — SEQUENTIAL PREDICTION LADDER PREDECL (under PREREG v2, pin 96b3e09c)
**Status: FROZEN at commit. Governs all witness-arm rungs k >= 3.** Date 2026-07-02.

## Protocol (the ladder rule)
1. Rung k runs ONLY after its extent window is frozen in this file's ledger (committed,
   pinned) using data from rungs < k exclusively.
2. Grading: measured half-width w(k) := max{|u| : u in grid, rung-k witnesses exist at u}.
   IN-WINDOW => SP-L(k) PASS. OUT-OF-WINDOW => law-revision event: banked loudly, routed
   to Will, ladder pauses. (Exploratory class: a miss revises the law, it does not halt
   the stage; PB.1'/KB.1 remain the only stage-halting kills.)
3. Window rule for k >= 4: [0.85, 1.15] * A3 * k^2 / 4000, where A3 := 4000*w(3)/9
   measured at rung 3; each window committed BEFORE its rung runs.
4. Per rung, unchanged from v2/predecl-2: PB.1' with margin-tier clause, PB.2 backward
   match, boundary-lemma point expected (PROVEN for all k), byte-stable x2 on the box,
   motion schedule B_mot(j) = 2*(20*(j-1)+10)*h^2 per chain step.

## Grid schedule (frozen)
Fine grid: u in {n/4000 : |n| <= 4*k^2 + 16}; medium grid n/40, 1 <= |n| <= 20, unchanged.
Theta1 scan: 720 uniform samples, secant refinement, acceptance |s2(k)| < 1e-40, c2(k) < 0.

## Window ledger (append-only; each row committed before its rung runs)
| k | window (|u| max, /4000) | source | pin ref | verdict |
|---|---|---|---|---|
| 3 | [32, 40] | k=1,2 ballistic fit (banked in STAGEB_rung2.md before any k=3 run) | 7dfe1b65 | **PASS — w(3)=39/4000**, x2 sha c6b62f6d |
| 4 | [58, 80] | frozen rule: A3=39/9, k^2 window [0.85,1.15] | prev commit | **PASS — w(4)=70/4000** |
| 4-sharp (bonus clause, does not replace the rule) | exactly 70 | interpolation w(k)*4000 = k(9k-1)/2 through k=1,2,3 (Level-1 raw fit; graded, not trusted) | prev commit | **HIT EXACTLY — w(4)=70/4000**, x2 sha b34ed2c4; law upgraded to EMPIRICAL |
| 5 | [92, 125] | frozen rule A3-window | prev commit | **PASS — w(5)=108/4000**, x2 sha b9a449a0 |
| 5-sharp | exactly 110 | k(9k-1)/2, now 4-for-4 | prev commit | **REFUTED — 108 != 110**; no quadratic floors all five rungs (constraint system empty); law = 4.5k^2 leading + negative higher-order correction |
