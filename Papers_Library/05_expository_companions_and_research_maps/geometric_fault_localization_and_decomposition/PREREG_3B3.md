# STAGE 3b.3 — SPLIT-LAW MINIATURE MODEL (FROZEN pre-battery, S-2026-07-05b; Will: "ratify, go 3b.3")
Successor stage (ARM_CLOSE §5; A3's 3b.3 design line). Goal: the smallest
chassis analogue where the elimination is symbolically visible, to hunt the
FORMULA-LEVEL origin of the certified laws: N(D1·D2) = +□ (9/9 slices),
per-denominator +□ (3b.2/A6), even Galois split 352+352, D-borne
square-lead law. Mechanism candidates on record (HUNT_ADDENDUM §5): the
quadratic-extension involution ι [PLAUSIBLE, not constructed]; deck
structure of the y = 1/(D1·D2) covering.

## Miniature construction (frozen; exact parallel of the real chassis)
Real chassis verbatim source: `stage2_build.D_polys` + HB.1pp saturation.
Miniature: witness data (g, H) and slate vectors FROZEN LITERALS below;
perp(w) = w − (⟨w,g⟩/|g|²)g applied to all slate vectors as in the real
pipeline; A_i = U_i v_iᵀ − v_i U_iᵀ; R_i (numerator) = (I−A_i)·adj(I+A_i),
denominator D_i = det(I+A_i) = 1 + |U_i|²|v_i|² − ⟨U_i,v_i⟩²; conjugated
H(t) = RᵀHR with R = R1·R2 (denominator (D1·D2)²); O = gauge-normal
coordinates (witness_battery O_of formula); ties = m2_X(O_num(t)) −
m2_X(O_base)·(D1·D2)⁴ for the isotypic X present at that n; each tie
divided exactly by D1, D2 to maximal powers (remainder MUST be 0,
multiplicities recorded — HB.1pp discipline); Rabinowitsch y·(D1·D2) − 1
adjoined, y last. Engine: pinned msolve; grader: banked anyrur_grade.py.
- **M-0 (control, n=3, single Cayley):** R = R1 only, D2 ≡ 1; params
  (t1,t2) with U1 = pu1 + t1·pe + t2·pv2 (2 params, 2 ties); rab y·D1 − 1.
  Separates product-level structure from per-factor structure.
- **M-A (n=3, two-Cayley):** U1 = pu1 + t1·pe; U2 = pu2 + t2·pe; ties
  (m2_triv, m2_std) (shape absent at n=3); vars (t1,t2,y).
- **M-B (n=4, two-Cayley):** U1 = pu1 + t1·pe; U2 = pu2 + t2·pe + t3·pv1
  (full analogue); ties (m2_triv, m2_std, m2_shape); vars (t1,t2,t3,y).
Frozen literals — n=3: g=(3,1,2), H=[[2,1,-1],[1,3,2],[-1,2,1]], slate
u1=(1,2,-1), v1=(2,-1,1), u2=(1,-1,2), v2=(-1,1,1), e=(1,1,-2).
n=4: g=(3,1,2,5), H=[[2,1,-1,1],[1,3,2,-1],[-1,2,1,2],[1,-1,2,-2]], slate
u1=(1,2,-1,1), v1=(2,-1,1,-1), u2=(1,-1,2,1), v2=(-1,1,1,2), e=(1,1,-2,1).

## Predictions (FROZEN; graded mechanically; clauses embedded)
| id | statement | class | prediction |
|---|---|---|---|
| MP.0 | pipeline sanity per rung: saturation divisions exact (remainder 0); msolve returns; anyrur parses; a rung with dim ≠ 0 or empty variety is recorded DEGENERATE (not a kill) and the ladder continues | sanity | MUST HOLD as procedure; all-rungs-degenerate = K-3B3-1 |
| MP.1 | M-0 control: on the single-Cayley tie locus, class(lead(w)·const(w)) trivial up to sign ⟹ N(D1) = ±□ | discriminating | HOLDS — moderate (the 3b.2/A6 per-denominator law suggests per-factor robustness) |
| MP.2a | M-A: lead(w) is a perfect square | discriminating | LOW-moderate (D-borne law; miniature preserves the D-function structure) |
| MP.2b | M-A: class(lead·const) trivial ⟹ N(D1·D2) = ±□ | discriminating | moderate — THE phenomenon-persistence stake |
| MP.2c | M-A: w splits into two equal-degree ℚ-irreducible factors | discriminating | LOW (the even split may be chassis-scale) |
| MP.3 | M-B: same three reads (a/b/c) at n=4 | measurement | record — comparison row for the n-dependence of the laws |
| M4 | mechanism pass: at M-A the eliminant w is ALSO computed symbolically (resultants) and its factorization structure examined against D1, D2, and candidate involutions; deliverable = mechanism memo in the stage report | measurement | exploratory — no pass/fail staked; the memo is the point |

## Kill conditions (armed)
- **K-3B3-0:** saturation remainder nonzero, or grader/probe disagreement ⟹
  HALT (pipeline defect); fix only by versioned addendum.
- **K-3B3-1:** ALL rungs degenerate ⟹ miniature ladder EXHAUSTED at these
  literals; route to Will (fresh literals need a new freeze — no in-session
  slate fishing).
- Envelope 1800 s / 8192 MB per msolve job; exceed = datum. Byte-stable ×2
  on every graded artifact.

## Pins (Rule 1.9) — freeze_pins_3b3.sha256
This file; ../anyrur_grade.py; ../rur_tools.py; the msolve binary. Builder
(m33_build.py) is battery code written post-freeze; its sha is recorded in
the run ledger. role=probe + ledger; referee = anyrur_grade's independent
factorization path + (M-A) the symbolic-resultant cross-check of deg(w) and
factor degrees against msolve's — must agree.

## Status moves (frozen)
Graded reads bank into the split-law mechanism ledger row; any surviving
law at miniature scale upgrades the mechanism hunt from chassis-bound to
model-tractable [STRUCTURAL lead]; losses are equally banked (they localize
the law's scale). Nothing canonical without Will's sign-off.

frozen: true · author Claude-session · substrate [BOX] · S-2026-07-05b
