# SPLIT PROBE — PREDECL (S-2026-07-05)
**Status: FROZEN pre-battery (pin = sha256 of this file at freeze commit).**
**Authorization: Will, this session — "can we investigate the split law completely and then return to this question again?" Scope = the split law of HUNT_ADDENDUM_v2_4 §4. The π-rotation chassis remains fenced and is NOT part of this probe.**
**Prior-wins audit: dashboard, campaign ledgers, hunt records searched S-2026-07-04/05; no prior orbit-structure / eliminant-factorization result exists in the corpus; no struck object (dim-1 curves, T4, deg-3528 screen, composite moduli) is used or cited.**

## Object
The certified 8/8 law: every slice eliminant w_s = f1·f2 (deg 352+352, both
irreducible over Z, content 1); lead(w_s) a perfect square; lead(f1)/lead(f2)
in {1, 3^2, 3^8}. Framing already [PROVEN]: RUR factor degrees = Galois-orbit
sizes of the tie points, independent of separating element, so the 352+352
split is INTRINSIC to the tie scheme. The lead/square-class law is a property
of the pair (ideal, chosen separating element y = 1/(D1·D2)).

## Questions
- **Q1 (Galois structure):** Frobenius statistics for all 16 factors over an
  extended verified-prime chain — cycle types; fixed-point mean/variance
  (variance estimates permutation rank); Frobenius parity per factor
  (all-even <=> disc square <=> G inside A_352); parity-match f1 vs f2 at every
  prime (<=> disc(f1)·disc(f2) square <=> shared quadratic resolvent field);
  lcm-of-cycle-lengths match (evidence toward a common splitting field).
- **Q3 (locate the 3s):** v3 trace through the ACTUAL pipeline objects —
  GG = |g|^2, the perp'd slate coordinates, D1/D2 coefficients, poly_to_ms
  clearing factors, the Rabinowitsch clearing factor — per slice. (Corrects
  the raw-slate-only check of v2.4 §5, which tested the wrong object;
  correction inked there this session.)
- **Q4 (gauge test):** re-run the Rabinowitsch RUR on s1 and s4 with a forced
  generic separating variable s, generator s − (3·t1 + 5·t2 + 7·t3), s last in
  variable order. Split persistence is a PROVEN-must sanity; the discriminating
  readout is whether lead(w_s) remains a perfect square under the new
  separating element.
- **Q2 (the involution, Stage 3):** construction attempt for the
  quadratic-extension iota — Stab(g) slice-preservation audit + deck structure
  of the y-covering. DESIGN DEFERRED BY RULE: Stage 3 opens only after Stage
  1+2 verdicts are graded, with its concrete design appended here as an
  addendum before any derivation runs.

## Predictions (frozen; graded mechanically by the battery)
| id | statement | class | prediction |
|---|---|---|---|
| SP.1 | every good-prime cycle type of every factor sums to 352; ramified primes (repeated factors) excluded and counted | sanity | MUST HOLD (else K-SP1) |
| SP.2 | per-factor mean fixed-point count over the prime sample is near 1 (transitivity; Chebotarev) | sanity | MUST TREND TO 1 (else K-SP1) |
| SP.3 | parity(Frob f1) == parity(Frob f2) at EVERY sampled good prime, every slice (<=> disc(f1)·disc(f2) is a square <=> shared quadratic resolvent) | discriminating | HOLDS (iota-over-quadratic picture) — moderate confidence |
| SP.4 | lcm(cycle lengths f1) == lcm(cycle lengths f2) at every sampled good prime (common splitting field evidence) | discriminating | HOLDS — lower confidence; a clean FAIL is equally informative |
| SP.5 | per-factor fixed-point variance (estimates permutation-group rank: 1 ~ 2-transitive; large ~ imprimitive blocks) | measurement | NO pass/fail — wall-scout convention, record the number |
| SP.6 | v3 anomalies localize in the perp'd pipeline objects for s3/s4 and are absent for the six ratio-1 slices | discriminating | HOLDS — some 3-adic distinction exists between the slice groups |
| SP.7 | under forced separating form s (Q4): 352+352 persists [PROVEN-must sanity]; lead(w_s) perfect-square property | discriminating | square-ness FAILS for generic s (the square law is D-function-specific); if it HOLDS, escalate to variety-level structure |

## Kill conditions (armed)
- **K-SP1:** any SP.1/SP.2 sanity failure => pipeline defect; HALT battery,
  audit before any interpretation. No verdict is graded from a run that
  tripped K-SP1.
- **K-SP2:** if Q3 demonstrates the ENTIRE lead-square law reduces to a
  normalization convention => record, downgrade the lead law to bookkeeping,
  re-scope Stage 3's D-preservation clause. (The 352+352 split is intrinsic
  and survives regardless.)
- **K-SP3 (envelope):** Stage-1 jobs 1800 s / 8192 MB; Q4 re-RUR jobs
  3600 s / 8192 MB. Envelope-exceed = datum, not kill (WALL_SCOUT convention).

## Stages
- **Stage 1 (opens at freeze):** Q1 statistics battery + Q3 v3 trace.
  Banked script `split_probe.py`; byte-stable ×2 on box; prime sample =
  first 120 of the sympy nextprime chain from 576460752303424600, every
  modulus asserted prime.
- **Stage 2 (opens when Stage 1 grades clean):** Q4 forced-separating-form
  re-RUR on s1 and s4, then factorization + Q1 statistics on the new
  eliminants via the banked tools.
- **Stage 3 (gated):** Q2 iota construction; design appended here
  post-Stage-2, before any derivation.

## Deliverables
`split_probe.py` (banked), records + ×2 shas under
`rabinowitsch_records/split_probe/`, `SPLIT_PROBE_REPORT.md`, ledger +
dashboard deltas filed PROPOSED. Nothing canonical without Will's sign-off.

frozen: true · author: Claude-box · substrate [BOX] · session S-2026-07-05

---
## ADDENDUM A1 (S-2026-07-05, frozen post-Stage-1, pre-Stage-1b/2 battery)
**Stage-1 graded: SP.1/2 PASS · SP.3 FAIL · SP.4 FAIL · SP.5 var≈1 (all 16) ·
SP.6 FAIL-informative (3s uniform; sat clearing v3=[0,3,3] chassis-constant).
Mechanism class REVISED: Galois-side pairings are dead (no shared quadratic
resolvent, no common-closure signal, groups 2-transitive ⟹ A/S only at deg
352 ⟹ S_352 with odd Frobenii present). Surviving class: FORMULA-LEVEL
FACTORIZATION — the elimination factors as a polynomial identity of the
chassis (norm-form / determinant–Pfaffian paradigm), producing equal-degree
twins with locked lead arithmetic over generic Galois interiors.**

New frozen predictions:
| id | statement | class | prediction |
|---|---|---|---|
| SP.8 | within-slice lcm-collision rate (8 factor pairs) vs cross-slice baseline (112 pairs), same 120 primes | discriminating | RATES EQUAL (independence); a within≪cross anomaly would mean genuine anti-correlation and reopen point-level coupling |
| SP.9 | per-slice joint parity 2×2 counts vs independence product | measurement | consistent with independence |
| SP.10 | fresh perturbed slate s8 (rational perturbation of SLATE 0, u1[0] += 1/7): Rabinowitsch RUR has dim 0, ideal_deg 704, w = f1·f2 with degrees 352+352, lead(w) a perfect square | discriminating | HOLDS — the formula-level mechanism is slate-generic. FAIL (irreducible w / unequal degrees / non-square lead) ⟹ the 8 slates are fine-tuned and the law is slate-conditional |
| SP.7′ | (sharpens frozen SP.7) forced separating form s = 3t1+5t2+7t3 on s1: msolve lf must select s (else retry with new random form, retry count recorded); split 352+352 persists [PROVEN-must]; lead(w_s) squareness | discriminating | squareness FAILS for generic s (lead law belongs to the D-function) |

Kill/envelope unchanged; K-SP1 applies to SP.8/9 sanity; s8 + s-form msolve
jobs ride the 3600 s / 8192 MB envelope, exceed = datum.

---
## ADDENDUM A2 — STAGE 3a DESIGN (S-2026-07-05, frozen pre-battery; Will: "GO on 3a")
**Stage-2 graded: SP.7' HOLDS (square-lead law is D-borne; split persists under
separating-form change), SP.10 HOLDS (fresh slate s8: 704 = 352+352, square
lead, ratio 1/1, rational-point-free — law and obstruction slate-generic 9/9).**

Bookkeeping made exact before testing: with M(x) = primitive minpoly of the
D1·D2-values, the reciprocal relation gives lead(w) = ±lead(M)·N(D1D2)... more
precisely lead(w) = ±const(M) and const(w) = ±lead(M), hence
class(N(D1D2)) = class(lead(w)·const(w)) in Q*/(Q*)². The CERTIFIED law
(lead(w) square) therefore fixes class(N(D1D2)) = class(const(w)) =
class(const(f1)·const(f2)) — measured by SP.12 below.

**3a core reduction [PROVEN]:** on the Rabinowitsch scheme the separating
value is θ = 1/(D1·D2). D1D2 is a square in component field K_i = Q[θ]/(f_i)
⟺ θ is a square in K_i ⟺ f_i(z²) is REDUCIBLE (splits as m(z)·±m(−z),
degrees 352+352, m = minpoly of √θ generating K_i). f_i(z²) IRREDUCIBLE
(deg 704) ⟺ √θ generates a proper quadratic extension ⟺ no h exists on
that component. Binary readout; one exact flint factorization per component.

| id | statement | class | prediction |
|---|---|---|---|
| SP.11 | f_i(z²) irreducible for both components of s1 AND s8 (θ not a square in any component field; the naive h-mechanism fails) | discriminating | HOLDS — moderate confidence, via lead-parity heuristic (component-square structure forces lead(f_i) = ±lead(V)²; s0 f1 has v5 = 69 odd) [PLAUSIBLE, content caveats noted] |
| SP.12 | class(const(f1)·const(f2)) per slice, all 9 (⟹ class of N(D1D2)) | measurement | if square 9/9 ⟹ N(D1D2) ∈ ±(Q*)² is the true identity; if not ⟹ the certified law is specifically denominator-content, restate target |

Battery: `s3a_ztest.py` (banked) — modes ztest (s1+s8, 4 factorizations) and
constclass (all 9 slices, free from banked factors). ×2, envelope 1800 s/8 GB.
Kill: K-SP1 inherits (any degree-bookkeeping violation halts grading).
If SP.11 HOLDS: 3b = miniature symbolic model of the elimination (design
returns to Will). If SP.11 FAILS on any component: h exists — extract it,
h becomes the Stage-3b object.

---
## ADDENDUM A3 — STAGE 3a GRADED (S-2026-07-05, ×2: ztest `f2f6bb40`, const `69932306`)
**SP.11 HOLDS [CERTIFIED ×2]:** f_i(z²) IRREDUCIBLE (deg 704) for both
components of s1 AND s8 — θ = 1/(D1·D2) is not a square in any component
field; the pointwise h-mechanism (D1D2 = h² on the quotient) is REFUTED.
The lead-parity heuristic delivered.

**SP.12 [CERTIFIED ×2, 9/9]:** |const(f1)·const(f2)| is a perfect square on
every slice. Combined with the certified lead law:
```
class(N_T(D1·D2)) = class(lead(w)·const(w)) = trivial (up to sign)
==>  N_T(D1·D2) = ± (perfect rational square)   on all nine slices
```
So the norm is square WITHOUT the element being a square: the square class
of D1·D2 lies in ker(corestriction K*/K*² → Q*/Q*²) on BOTH components,
every slice. Sharpener: each K has NO proper subfields (Galois closure
S_352; point stabilizer S_351 is maximal) — no subfield-norm explanation
can exist. The identity is genuinely norm-level.

Bookkeeping note: det(I−S²) = det(I+S)² is a polynomial identity for skew S,
so N(det(I−Sᵢ²)) = N(Dᵢ)² is trivially square; the CONTENT of the law is
that N(D1) and N(D2) share a square class.

**STAGE 3b DESIGN (on Will's desk — not launched):**
- 3b.1 sign refinement: signed const/lead classes (trivial read, fixes ±).
- 3b.2 factor localization: eliminate w.r.t. y1 = 1/D1 alone (and y2 = 1/D2)
  on one slice — is N(D1) individually ±□, or only the product N(D1)·N(D2)?
  One msolve run each; both outcomes structural (individual ⟹ per-denominator
  identity; product-only ⟹ the tie conditions couple the two Cayley factors'
  square classes — a genuine cross-term law).
- 3b.3 miniature symbolic model: smallest chassis analogue where the full
  elimination is symbolically tractable; hunt the identity in the formula.
Probe status: Stages 1/1b/2/3a CLOSED, all frozen predictions graded;
"investigate completely" is discharged at the empirical/structural tier;
remaining OPEN = the proof of the norm identity + the split's formula origin
(Stage 3b, gated).

---
## ADDENDUM A4 — 3b.2 RECLASSIFIED MEASUREMENT (PA-5, S-2026-07-05; frozen pre-battery)
Per PA-5, factor localization is measurement-class and does not wait on the
desk. System: honest Rabinowitsch scheme + adjoined u·D_which − 1, u last
(vars t1,t2,t3,y,u), slice 1, both denominators.
| id | statement | class | prediction |
|---|---|---|---|
| SP.13 | lead(w_u) square-class for u = 1/D1 and u = 1/D2 separately, per the two components | measurement | weak prior: PER-DENOMINATOR (both individually square) — LOW confidence; product-only outcome = cross-term law (raises 3b priority per DESK flip condition) |
Sanity (must): dim 0, ideal_deg 704, split 352+352 persists, lf = u.
Grading: anyrur_grade.py on both outputs, ×2. Kill: K-SP1 inherits.
Envelope: 3600 s / 8192 MB per job; exceed = datum.

---
## ADDENDUM A5 — 3b.2 GRADED (S-2026-07-05b; measurement per A4/SP.13)
Jobs: msolve dloc pair, slice 1, u=1/D1 and u=1/D2 (vars t1,t2,t3,y,u; u last).
Runtime ~732 s / ~813 s (envelope 3600 s — clear; exceed-datum not needed).
Grader anyrur_grade.py ×2, byte-identical per job (grade sha256 b79b0f5c… /
6b445f38…; raw-out sha16 04d06e3510e4b1e0 / 2441aa206506eec4; factors sha16
3a4fc792c83bda20 / 57dc80f9d62176ca). Single msolve run per job, as frozen.

SANITY (must): PASS both jobs — dim 0, ideal_deg 704 = deg(w_u), split
352+352 persists (multiplicities 1,1), lf = u. K-SP1 silent. Build-log note:
pre-patch build_dloc NameError traceback precedes the successful WROTE line
(def-after-main defect, ALREADY IN INK S-2026-07-05, commit 18ad5e6); final
.ms built by patched dispatch — downstream sanity certifies the honest system.

SP.13 VERDICT: PER-DENOMINATOR — the weak prior HELD [lead level, grader ×2
byte-identical]. lead(w_u) is a perfect rational square for u = 1/D1 (7264
digits) AND u = 1/D2 (12135 digits) individually. Per-component mechanism
note: in BOTH jobs the two deg-352 components carry EXACTLY equal leads
(lead_equal=True, reduced ratio 1/1) — product-squareness is realized by
exact lead equality, the strongest form of the shared-square-class law
(same shape as the A3 bookkeeping note: content = shared class, and here
the sharing is equality on the nose).

CONSEQUENCE: no cross-term law at lead level — DESK item-4 flip condition
NOT triggered; split-law proof campaign stays PARKED. Scope fence: slice 1
only, lead level only. NOT MEASURED (not frozen in SP.13): const(w_u)
square-class — the const half of the individual-norm read; banked factors
files make it a cheap follow-up measurement if ruled.

Records: rabinowitsch_records/split_probe/dloc_s1_D{1,2}_grade.log +
_grade_x2.sha + _factors.txt + .ms + _build.log; raw msolve outputs box-only
(40/60 MB), sha256 in dloc_s1_rawout_boxonly.sha. Nothing canonical without
Will's sign-off.

---
## ADDENDUM A6 — CONST-CLASS + SIGNED READ (S-2026-07-05b; frozen PRE-BATTERY; Will ruling: "go" on desk item 3)
Measurement class per PA-5 (= 3b.1 sign refinement + the const half of the
3b.2 individual-norm read). Inputs = banked factors files ONLY (no new
elimination): s0..s8 product systems + dloc_s1_D1/D2. Grader
`a6_sign_const_grade.py` sha256 18f01ba5fb95674f…, input pins in
`rabinowitsch_records/split_probe/A6_INPUT_PINS.sha256` (pinfile sha256
c8b15001900f962d…). Smoke-tested on synthetic fixture only (real inputs
untouched pre-freeze). Envelope 60 s (trivial). Kill: K-SP1 inherits
(sanity_2x352 FAIL on any system = halt, no verdict).
| id | statement | class | prediction |
|---|---|---|---|
| SP.14 | \|const(f1)·const(f2)\| perfect square for dloc u=1/D1 AND u=1/D2 (completes the individual-norm read at s1: N(D_i) individually ±□) | discriminating | HOLDS — moderate confidence (upgraded from SP.13 lead result + SP.12 product result); FAIL = lead/const asymmetry, structural datum |
| SP.15 | signed classes: sign(lead(f_i)), sign(const(f_i)), even-degree norm sign read sign(lead_i·const_i) per component, per system, all 11 systems (fixes ± in N=±□ per slice and per denominator) | measurement | record-only (wall-scout convention); A3 called the read trivial — no prior staked |
Sanity (must): every system parses 2 factors × deg 352 × mult 1; input
sha16s match pinfile. Grading: run ×2, byte-identical required.
frozen: true · author: Claude-session · substrate [BOX] · S-2026-07-05b

---
## ADDENDUM A7 — A6 GRADED (S-2026-07-05b; ×2 byte-identical, grade sha256 df11c53e…)
Sanity: 11/11 systems 2×352 mult 1, content=1, input sha16s == pinfile. PASS.

**SP.14 HOLDS [grader ×2]:** |const(f1)·const(f2)| perfect square for dloc
u=1/D1 AND u=1/D2. Combined with SP.13 (lead squares) and the RUR norm read:
```
N(D1) = +(perfect rational square)   individually, slice 1, both components
N(D2) = +(perfect rational square)   individually, slice 1, both components
```
**SP.15 (recorded):** every sign on every system is +1 — sign(lead(f_i))=+1,
sign(const(f_i))=+1, even-degree norm sign +1, all 11 systems. The ± in the
Stage-3a law resolves to PLUS: **N(D1·D2) = +□ on all nine slices**, and the
per-denominator norms at s1 are +□. 3b.1 sign refinement DISCHARGED.

OBSERVED (unfrozen, flagged for 3b.3): per-component |const(f_i)| is
individually square on 9/11 systems; the two exceptions are the s1 and s8
PRODUCT systems (both components non-square, equal nontrivial class,
cancelling in the product) — while the s1 dloc systems are individually
square. The nontrivial shared const class lives at the product level
(θ=1/(D1·D2)) and vanishes under factor localization; s1 and s8 are exactly
the historically distinguished slices (hard-close slice + fresh slate).
Datum only — no claim staked.

Records: split_probe/a6_grade.log + a6_grade_x2.sha + A6_INPUT_PINS.sha256;
grader banked a6_sign_const_grade.py. Nothing canonical without Will's
sign-off.
