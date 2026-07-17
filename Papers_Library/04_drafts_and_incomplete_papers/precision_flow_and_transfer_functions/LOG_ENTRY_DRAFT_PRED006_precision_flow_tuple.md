# RESEARCH_LOG ENTRY — PRED-006 / OBJ-002: Precision-Flow Rounding Tuple

**Test:** whether the CAND-001 tuple `(B, X→B, G, C, s_phys, Ω, I, W)` has a faithful realization on the HR133 precision-flow / rounding structure (the pre-registered third-realization attempt for OBJ-002).

**Result (audited against the HR133 archive — `AUDIT_REPORT_PRED006_PRECISION_FLOW_TUPLE.md`):** the structure splits into two objects, not one — an account-orientation cover (`t ↦ −t`, carrying the flow, C2 covariance, and death norm) and a separate candidate-output bundle (the two adjacent representable values) on which round-to-nearest chooses. A single map cannot carry both deck covariance and branch selection. So the one-cover tuple is not realized here; the correct structure is the two-cover form.

**Outcome:** the founding tuple conflated a *state cover* with an *output/selection map*; the corrected form separates them (`X` state cover, `R:X→Y` output map, physical section = the case `Y=X`).

**Banked in the ledger (v0.5):** FAIL-004 (one-cover realization does not hold); E-014 (HR133 = certified cover + covariant transport); E-015 (two-cover obstruction); NS-001 revised to the X/Y split; NS-002 gains the quotient-transport square as a morphism lead; CAND-001 held at S2.

*The construction below is the working draft of the attempt. Its cell-offset residual quadratic and valuation section were early formulations later corrected against the archive; the audited result above is authoritative.*

**Program:** Mathematical Object Emergence (CAND-001), third-realization campaign; feeds CCAF/precision-flow (HR133, cited not re-derived).
**Targets:** PRED-006 (faithfulness of the rounding tuple), OBJ-002 (third independent realization), gates G3-05 and G4-05; firing-ledger maturations F-007, plus new firings F-009/F-010.
**Date:** 2026-07-10 (attempt executed on GO, same day the spec's governing rules were enacted)
**Rules in force (announced at execution):** RULE-005 (spec-first: PRED-006 is the frozen full-facet spec, timestamped v0.2, bar raised v0.3, stop condition armed — *no forcing*); RULE-002 (derive before sweep: literature quarantined; recognition events tagged inline; sweep queued as an audit-stage task); RULE-001 (standing: any failed slot gets a salvage pass before a strike); RULE-003 (scope note: HR133 is **banked program material, not an import** — no ceiling required); RULE-004 (whatever the verdict, it moves novelty credit only).


## 0. Purpose and placement

This entry executes the pre-registered PRED-006 attempt: define the
CAND-001 data tuple

```text
T_pf = (B, pi : X -> B, G, C, s_phys, Omega, I, W)
```

on the precision-flow / rounding structure, **from program-native material
only**, and grade each slot against the frozen spec and the v0.3-raised
faithfulness bar (an interpretation datum for `s_phys`, not merely a
selection mechanism). The falsifier of record: *some datum (`Omega` or
`G` most at risk) is only definable vacuously, or no banked theorem
transfers.* The stop condition: if refuted, record FAIL-004 and stop.

**Headline (details and honesty ledger below):** every slot is definable
and non-vacuous; two banked theorems transfer (THM-002, THM-004); the
valuation instrument transfers at instrument level; the falsifier does
NOT trigger; **no FAIL-004**. Two slots required definitional sharpening
(recorded, not forced), and the attempt surfaced two genuinely new
structural facts the founding family could not have shown: a **wall
dichotomy** (free-orbit vs fixed-point walls) and a **selection-transport
obstruction** (the double-rounding anomaly as the failure of
`s_phys`-preserving refinement morphisms near walls).

---

## 1. The frozen spec (restated for the record)

Per PRED-006 (registered v0.2 before any attempt; bar raised v0.3):

```text
pi        = degree-2 dyadic/rounding cover;
C         = binade/representable chamber;
s_phys    = rounding rule (round-to-nearest as branch selection)
            + [v0.3] an interpretation datum beyond the mechanism;
W  ⊇      {ULP/binade walls, dyadic-death locus};
Omega     = Refinement-Law flow;
covariant = signed residual (sign flips under local reflection,
            magnitude descends);
thread    : ord_v(u) parity governs horizon-cover ramification,
            2-adic valuation data governs precision-flow behavior —
            same valuation instrument at the place 2.
```

---

## 2. Setup — the cell, the roles, and the two residuals

Fix an aperture level `n` inside one binade: the representable grid is
uniform with unit `ulp_n`; write `h = ulp_n / 2`. An input `x` sits in a
cell `[g^-, g^+]` with `g^± = mu ± h` (midpoint `mu`). Write the offset

```text
x = mu + s,        s ∈ (-h, h].
```

The two **candidate residuals** — to the near and far neighbor — are

```text
r_near = s - sign(s)·h,        r_far = s + sign(s)·h,
```

and they are the two roots of the monic quadratic

```text
R(rho) = rho^2 - 2s·rho + (s^2 - h^2),
r_near + r_far = 2s,           r_near · r_far = s^2 - h^2 ≤ 0.
```

*(A deliberate echo of the program's founding arc: the ordered horizon
pair as roots of a monic quadratic, with a universal product. Here the
"universal product" `s^2 - h^2` is ≤ 0 — the two residuals straddle zero —
and vanishes exactly on the grid.)*

Normalize `sigma = s/h ∈ (-1, 1]` and set

```text
q = sigma^2 ∈ [0, 1].
```

---

## 3. The tuple, slot by slot

### 3.1 `B` — observable/descended base

`B` = the aperture data plus the **even** (deck-descended) offset data,
fibered over the level index:

```text
B = ⊔_n B_n,    B_n = { (cell {g^-, g^+}, h, q) } = unordered pair
                      + unsigned squared offset.
```

What a float computation *keeps* without instrumentation lives here (plus
the mixed selected value, §3.7). Non-vacuous: `B` carries the error
bounds, the norm (§3.8), and the chamber structure (§3.4).

### 3.2 `pi : X -> B` — the degree-2 rounding cover

`X` adjoins the **role orientation**: which neighbor is NEAR — i.e. the
sign of the offset. Concretely `X = B[sigma]` with

```text
sigma^2 = q        —  the SAME degree-2 map  m ↦ m^2 = u
                       as the horizon cover, in different clothes.
```

Fiber = the two role-assignments (near, far) of the unordered neighbor
pair. **Ramification locus: `q = 0`** — the cell midpoints, i.e. the
round-to-nearest **tie wall**, where the near/far roles coincide.
Degree 2 per level; the refinement tower (§3.6) makes it *dyadic*.
`[RECOGNIZED: the level-tower assembles into a pro-2 inverse limit
resembling the 2-adic odometer — quarantined; recorded as a remark, not a
claim; queued for the post-audit sweep.]`

**Proof note (why this and not the naive neighbor cover).** The unordered
neighbor pair `{g^-, g^+}` is always two distinct points (`h > 0`), so the
*value* cover is split/étale everywhere and carries no branch geometry.
The branch geometry lives in the **role** cover `sigma ↦ sigma^2`, whose
degeneracy is exactly the tie. This mirrors the founding family, where the
ordered-horizon structure (not the bare value pair) carries the cover
geometry, degenerating at extremality `S_+ = S_-`.

### 3.3 `G` — deck action

`G = Z/2`, acting by **local reflection through the cell midpoint**,
`x ↦ 2mu - x`, i.e. `sigma ↦ -sigma`, swapping the near/far roles and the
neighbor labels. Fixed divisor of the base action = the tie wall `q = 0`.

**P1 (covariant law — the spec's covariant clause, proved).** Under
`tau ∈ G`: `s ↦ -s`, neighbors swap, hence

```text
tau(r_near) = -r_near,        tau(r_far) = -r_far,
|r_near| = h - |s|  and  |r_far| = h + |s|   descend to B.
```

The **signed residual is the pure odd covariant; its magnitude descends**
— exactly the frozen spec's clause "sign flips under local reflection,
magnitude descends." *(Two lines; the `Theta = S·T` analogue.)*
`G` is manifestly non-vacuous: it has nontrivial odd covariants, a
nontrivial fixed divisor, and a genuine quotient. **Falsifier limb 1 (G
vacuous): does not fire.**

### 3.4 `C` — binade chamber

`C` = the interior of a binade: the maximal region of **uniform aperture**
(constant `h`), within the normal range. Chamber walls = binade
boundaries, where the metric `h` jumps (the exponent step); outer walls =
normal/subnormal and overflow boundaries. The banked HR133 laws are
chamber-local statements at fixed `h`. Non-vacuous and structurally load-
bearing (the Refinement Law's normalization presumes it).

**Honesty note (recorded, not forced):** post-R5, the founding `C`
acquired a spectral characterization (chamber = pencil definiteness,
E-012). No analogous spectral/definiteness characterization of the binade
chamber is known or claimed here. Whether `C`-as-definiteness is a
founding-family accident or a candidate axiom is now a sharp question for
the loss matrix — either answer is informative. Not a slot failure: the
frozen spec asked for the binade chamber, which is what is delivered.

### 3.5 `s_phys` — selection rule + interpretation datum (the raised bar)

**Mechanism.** Round-to-nearest: select the role/sheet with the smaller
residual magnitude, `|r_near| = h - |s| < h + |s| = |r_far|` off the wall.
*(Cross-realization pattern, recorded: in BOTH realizations the selection
mechanism is extremal — unique least mass-square root there, minimal-
magnitude residual here. Per FAIL-005, an extremal mechanism alone is
absorbable and does NOT meet the bar.)*

**Interpretation datum 1 (theorem-grade): the tie-break is provably extra
structure.** 

**P4 (no equivariant selection on the wall).** At a wall point (`s = 0`,
`x = mu`), `tau` fixes the input and the base point but acts **freely** on
the two neighbor values `{mu - h, mu + h}` (it swaps them; they are
distinct). A `G`-equivariant selector `sel` satisfies
`sel(x) = sel(tau x) = tau(sel(x))` at fixed `x` — impossible on a free
orbit. Hence **no selection rule definable from the cover algebra and the
deck action alone extends over the tie wall**; any total rule must import
extra data. IEEE round-half-to-even imports precisely the **parity of the
last kept bit** — a base-arithmetic datum at the place 2. ∎

So `s_phys` here is: (mechanism: minimal residual) + (wall extension: bit-
parity convention, provably non-derivable) + (normative role: the
selected sheet is *the represented value* — the contract under which the
bookmark identity `x = fl(x) + r`, HR133, makes the instrumented
computation exact: surveyor, not scout). The non-derivability theorem is
the load-bearing interpretation datum; the normative reading is the
semantic role-assignment, the analogue of "this root is the actual black
hole." **Raised bar: met, with the theorem carrying the weight** (audit
may press on whether the normative reading is interpretation or
description; P4 stands either way).

### 3.6 `Omega` — Refinement-Law flow

The flow down the precision tower. With the normalized signed residual
`rho_n = r_n / ulp_n ∈ (-1/2, 1/2]`, one refinement step gives

```text
rho_{n+1} = 2·rho_n - round(2·rho_n)        (centered doubling map)
```

— the **Refinement Law** [HR133, banked; paraphrase-grade here, audit
item #1]. `[RECOGNIZED: the centered doubling map is classical symbolic
dynamics — quarantined; the law is cited from HR133, and only its
tuple-role is constructed here.]` Governing banked laws, cited:

```text
dyadic death        : rho = 0 is absorbing; reached in finite steps
                      iff x is representable at some level (dyadic);
rational periodicity: for rational x with odd-part denominator b0, the
                      flow is eventually periodic with period ord_{b0}(2);
bookmark identity   : x = fl_n(x) + r_n exactly, at every level n —
                      the instrumented flow is lossless.
```

**Slot typing (sharpened, not forced — recorded for NS-001):** the
founding `Omega` is first-law differential data — transport of selected-
branch covariants along physical base directions (`dS_±` against `dM,
dQ`; R5c-3's sensitivity formulas are its transport coefficients). The
rounding `Omega` is transport of the covariant along the **tower**
direction of `B`. Unified reading, proposed for the abstract slot:
`Omega` = *canonical transport of the covariant algebra along
distinguished base directions*. Both realizations instantiate it
non-vacuously. This is a definitional sharpening the third realization
forces — exactly what OBJ-002 was sequenced to do — not a vacuous
definition. **Falsifier limb 1 (Omega vacuous): does not fire.**

### 3.7 `I` — invariant/covariant algebra

```text
even (descends to B): mu, h, q = sigma^2, |r_near|, |r_far|,
                      norm r_near·r_far = s^2 - h^2, error bounds;
odd  (pure covariant): sigma, r, r_near + r_far = 2s;
mixed (sector-valued): fl(x) = mu + sign(sigma)·h — under tau it maps to
                      the OTHER neighbor, exactly as tau(T_+) = T_-.
```

**Transfer of THM-002** (sheet-oriented data transforms as covariants
under the deck): holds — P1 is its verification in this realization, with
the full even/odd/mixed trichotomy present. **Falsifier limb 2 (no banked
theorem transfers): does not fire — first transfer.**

### 3.8 `W` — wall structure

Three wall species, all non-vacuous, matching and extending the spec:

```text
W1  tie walls (q = 0)         : deck-fixed base divisor; ramification of
                                pi; selection convention required (P4);
                                the ULP-half walls of the spec.
W2  grid / death walls (q = 1): zero locus of the cover NORM
                                r_near·r_far = s^2 - h^2; the flow's
                                absorbing set; union over levels = the
                                dyadic-death locus of the spec.
W3  binade walls              : chamber boundary; the aperture metric h
                                jumps.
```

**Transfer of THM-004** (collapse walls are detected by norms of
distinguished cover coordinates): holds — the residual norm vanishes
exactly on W2, where the flow collapses. *(Founding analogue: the wall
norm's sixteen BPS factors; here the norm is quadratic and its zero locus
is the representability wall.)* **Second banked transfer.**

---

## 4. The valuation instrument (the pre-registered thread)

Founding, banked (R18/E-011): ramification of `W/K` iff `ord_v(u)` is
odd — the branch behavior of the degree-2 cover is read off a valuation
of the descended coordinate.

Rounding side, proved here at the same instrument level:

```text
P3 (valuation reads the walls). For x with 2-adic data:
    x lies on the level-n tie wall (W1)  iff  2^{n+1}·x is an odd
        integer  —  i.e. iff ord_2(x) = -(n+1) exactly;
    x lies on the level-n grid (W2)      iff  ord_2(x) >= -n;
    the flow's period, off W2, is ord_{b0}(2) for the odd part b0
        [HR133, banked].
```

**Same instrument** — a valuation at the relevant place reading cover
ramification/termination — **different specific criterion** (odd-parity
of `ord_v(u)` there; exact-level and threshold conditions on `ord_2(x)`
here), **and parity reappears on the rounding side in the wall
convention** (round-half-to-EVEN: bit parity selects on W1). Graded:
instrument-level transfer, criterion-level divergence, honestly recorded.

---

## 5. New structural facts the founding family could not show

**5.1 Wall dichotomy (THM-007 candidate — drafted).** The deck-fixed base
divisor comes in two types, distinguished by the fiber action:

```text
FIXED-POINT wall : the two branch VALUES coincide on the wall
                   (founding extremality: S_+ = S_- at u = 0);
                   selection degenerates trivially — no convention needed.
FREE-ORBIT wall  : the base point is fixed but the fiber is a free
                   G-orbit (rounding tie: the two neighbors stay
                   distinct); NO equivariant selection exists (P4) —
                   a convention importing extra base data is FORCED.
```

Candidate-native statement: *the selection rule's extension over a wall
is obstructed iff the wall is free-orbit; the obstruction class is the
free `G`-action on the wall fiber.* This explains, in one clause, why
IEEE-754 must legislate a tie rule while general relativity needs no
convention at extremality — an obstruction no single parent theory
states. Proved in both realizations; abstract form drafted; per §7
promotion rule it is a genuine G3-07 candidate (audit to grade whether
"no section over a free orbit" is doing all the work or the wall
classification is the content — recorded as the adversarial question).

**5.2 Selection-transport obstruction (feeds NS-002 / OBJ-001).** The
refinement step is a natural candidate **morphism** of tuples: it
preserves the cover, deck, chamber, and maps walls into walls. It does
NOT commute with `s_phys`: `fl_n(x) = fl_n(fl_{n+1}(x))` fails on a
wall-adjacent set — the classical **double-rounding anomaly**
`[RECOGNIZED: double rounding is classical numerical analysis —
quarantined; only the structural reading is claimed]`. Structural
reading, program-native: *`s_phys`-preserving morphisms are obstructed
near wall preimages; strict selection-preservation is too rigid a
morphism axiom.* This is the first hard constraint on NS-002 from
outside the black-hole siblings — precisely the honesty OBJ-002 was
sequenced ahead of OBJ-001 to provide.

---

## 6. Honesty ledger — divergences and the weakest link

```text
D1  Per-level Galois content is TRIVIAL: each level's cover is a split
    real quadratic (the two sheets are globally separated); the founding
    family's fibers carry S_5. The candidate tuple never required
    irreducible covers, and the rounding realization compensates with
    tower/flow structure (pro-2 limit, periodicity laws) — but an
    absorption-minded auditor may ask whether a split double cover with
    a flow is a realization or a degenerate case. RECORDED as the
    weakest link; audit to rule. (Counterpoint on file: degenerate
    Galois + rich dynamics is complementary evidence that CAND-001 is
    not "Galois theory in a hat" — the structure survives where the
    Galois content does not.)
D2  Omega slot re-typed (transport along distinguished base directions)
    to hold both realizations — a sharpening, logged for NS-001.
D3  C has no known spectral/definiteness characterization here (§3.4) —
    a sharp new loss-matrix question either way.
D4  Valuation thread: instrument-level transfer, criterion-level
    divergence (§4).
D5  s_phys interpretation is normative/operational rather than
    ontological; the load-bearing datum is the P4 non-derivability
    theorem (§3.5).
```

**Falsifier disposition:** `G` non-vacuous (P1); `Omega` non-vacuous and
law-governed (§3.6); banked transfers: THM-002, THM-004, valuation
instrument (partial). **The falsifier does not trigger. No FAIL-004.**
Per RULE-005: qualifications recorded above; nothing forced; the
near-miss on `Omega` typing is logged, not laundered.

---

## 7. Proposed deltas — **PENDING AUDIT, NOT ENACTED**

```text
MOEL (v0.4 -> v0.5 candidates):
  E-014  [new] The precision-flow tuple T_pf: all eight slots defined
         non-vacuously; P1-P4; transfers THM-002/THM-004; valuation
         instrument; parity trichotomy (even/odd/mixed incl. the
         tau(fl) = other-neighbor mixed law).      -> PROVED on GO
  E-015  [new] Wall dichotomy (fixed-point vs free-orbit) + P4
         non-derivability; double-rounding as the selection-transport
         obstruction (NS-002 constraint).           -> PROVED on GO
  PRED-006  OPEN -> CONFIRMED (with qualifications D1-D5 attached)
  PRED-005  gains its instance (support recorded)
  G3-05  BLOCKED -> EVIDENCE (third realization structurally independent:
         arithmetic-dynamical; no black holes, no ellipses; D1 attached)
  G4-05  EMPTY -> EVIDENCE (a pre-registered prediction confirmed in a
         family not used to formulate the candidate)
  G3-07  THM-007 (wall dichotomy) registered as the drafted native
         statement; grade on audit
  NS-001 Omega slot re-typed per D2; C-characterization question per D3
  NS-002 first outside constraint recorded (5.2)
  Queue: OBJ-002 first attempt COMPLETE (pending); OBJ-001 becomes the
         live head, now with two structurally different realizations to
         span — as designed
  DEC-005 [draft]: enact the above on GO; HOLD CAND-001 AT S2 (morphisms
         still EMPTY; stage promotion untouched by design); attach D1 as
         the standing adversarial question for the next monthly review
Map (v1.5 firing-ledger candidates, §12.3):
  F-007  matures: RULE-005 pre-compliance paid — the attempt ran under
         the frozen spec, stop condition honored     -> PAID (on GO)
  F-009  [new] RULE-002 in-force: quarantine held; recognition events
         tagged (odometer/pro-2 limit; centered doubling map; double
         rounding); post-audit sweep queued (signed-digit arithmetic,
         beta-shift/odometer dynamics, double-rounding literature) —
         convergences to be banked as validation, divergences triaged
                                                     -> PENDING (sweep)
  F-010  [new] RULE-005 in-force: spec-first execution logged; no
         forcing; qualifications ledger attached     -> PAID (on GO)
  RULE-003 non-firing note: zero imports entered — HR133 is banked
         material; the construction is program-native end to end.
```

## 8. Verification record

```text
Chain state : DRAFT. External audit OWED (focus items: the HR133
              paraphrase cross-check [item #1 — MANDATORY]; P4's free-
              orbit argument; the D1 weakest-link ruling; whether P3's
              valuation criteria are stated at the right generality;
              whether THM-007 clears the renamed-theorem bar).
              Counter-audit OWED. GO for enactment OWED.
No repo action, no commits, no runs. One entry, one commit on GO.
```
