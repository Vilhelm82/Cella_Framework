# ADMISSIONS — the introduction ledger

**The standard (Will, 2026-07-06, superseding the sign-off form):** nothing is introduced
from previous work until its record proves it is the correct addition — **why the engine
needs it, and why nothing we hold now, or could derive with bounded additional work,
beats it.** If that cannot be answered, there is more work to do, and the record names
that work. Records **self-ratify when the case is closed** — the answer must be obvious
from the record itself. No sign-off queue exists.

**THE RE-VERIFICATION RULE (Will, 2026-07-06).** No prior result enters on documentary
status. "ACCEPTED", "RATIFIED", "PROVEN", "CERTIFIED" in an origin document are
**claims, never evidence** — statuses hinge on humans, and humans are mistake-prone.
Before any prior mathematical result bears load here, it is **re-proven inside this
repo**: computational claims re-run from fresh code (never copied) against the stated
values, byte-stable ×2; symbolic identities re-derived; analytic theorems re-derived in
fresh notes. Once re-proven, the result carries its own certificate *here*, and future
sessions trust the re-runnable certificate — not the origin label, not memory, not
anyone's acceptance. Re-verification artifacts live in `verification/` and are named in
the consuming record. A result cited anywhere without an in-repo certificate is a
defect. (Case law: the WARP citation of 2026-07-06 — internally ratified, externally
stale; caught by Will, not by process. This rule makes that catch structural.)

**Statuses.**
- **OPEN** — case not yet closed; the missing work is named. A work item, not a request.
- **ESTABLISHED** — case closed; the artifact may be built. Scope stated exactly.
  *Mathematical inputs cited by the record additionally require in-repo
  re-certification before first load-bearing use (re-verification rule above).*
- **DISPLACED** — a better artifact won under the same standard. The record stays
  visible, successor named. Displacement is by evidence only: present the dominating
  alternative and the old record falls. This replaces authority with challenge.

**Record template**

```
ID / Artifact / Origin (reference only, never a dependency)
Need:          why the engine requires this capability at all
Criterion:     the properties that decide what "best" means here
Alternatives:  every live option — held now or derivable with bounded work — and
               why each loses on the criterion
Displacement:  the evidence that would displace this record
Obligations:   what the harness must still certify, and at which gate
Status:        OPEN | ESTABLISHED | DISPLACED
```

---

## A-001 — The cell, the observation map, composable residue

**Origin:** Cella Foundational Design Document v0.1 (2026-06-13). Reference only.
**Need:** the engine's defining output is exact-or-typed-refusal with a reconstructive
account. That requires a result object that carries its own account.
**Criterion:** simultaneously — (1) exact reconstruction of the true object where
possible, (2) typed non-recovery where not, (3) defects compose across chained
operations so a whole pipeline has one derivable account.
**Alternatives and why each loses:**
- *Floats + tolerances* — fails all three; it is the failure mode this engine exists
  against.
- *Interval/ball arithmetic* — enclosure, not reconstruction (fails 1); no typed
  non-recovery semantics (fails 2); widens under dependency where exact residues
  compose without widening on the covered class.
- *Higher precision (arbitrary-precision floats)* — relocates the defect, never
  types or recovers it (fails 1, 2).
- *Fully symbolic computation* — cannot represent the defect of a lossy observation at
  all (measured data has no symbolic truth to hold), unbounded cost (fails 3 in
  practice).
- *Derivable-with-work* — any object satisfying (1)–(3) **is** a cell under another
  name; the criterion forces the definition.
**Displacement:** an account object meeting (1)–(3) with a strictly larger covered class
or strictly lower cost.
**Obligations:** G0.1 — composition certified on the rational-op class. Sum-typed token
form certified or split (G0.4). These are certification targets, not assumptions —
the design doc itself graded them INFERENCE and this record preserves that.
**Status: ESTABLISHED.**

## A-002 — The second residue species (representation defect, R)

**Origin:** the transport law and gauge-normal form. Cited as mathematics.
**Need:** the engine must distinguish *the data changed* from *the representation
changed* — the false-positive taxonomy (recalibration, units, chart choice) that
interference testing exists to untangle.
**Criterion:** type-level separation of information-bearing defect (M) from
zero-information motion (R), losing neither the invariant nor the explanation of what
moved.
**Alternatives and why each loses:**
- *Type gauge motion as measurement error (M)* — provably wrong typing: the transport
  law says invariants are untouched, so gauge motion carries zero information about the
  state; conflation makes every recalibration look like a fault.
- *Eager quotient (store only invariants, discard the representative)* — loses the
  account: "representation changed, not data" becomes unverifiable, and the
  representative carries the role semantics (the declared frame is the physical
  section, not junk).
- *No typing (incumbent practice)* — the taxonomy collapses; ad hoc normalization.
**Displacement:** none available at the substrate level — the transport law is proven.
If G0.2 refutes single-account composition of M and R, the account splits into two
ledgers *visibly*; the species survives, the algebra bends.
**Obligations: DISCHARGED 2026-07-06.** The composition conjecture was resolved by the
G0.2 campaign (`campaigns/G02_two_species_account/` — Stages 0/A/B/C, frozen preregs,
byte-stable ×2, conjecture DEMONSTRATED on the covered class: order-2 slot,
translations, rational data, fixed/drifting base crossed by F1), and the
implementation certified at gates G0.1/G0.2 (`tests/gate_01.py` 7/7, `tests/gate_02.py`
13/13, both ×2). Key laws now in code: attribution by criterion (`fold_into_m`),
two-epoch boundary guard, owned holonomy (`holonomy_gap`).
**Status: ESTABLISHED — composition resolved positive on the covered class;
outside-class maps remain fenced (T_token territory).**

## A-003 — The exact number tower ℚ ∪ ℚ(√q)

**Origin:** the parity law. Cited as mathematics.
**Need:** no float on any verdict path, across the *entire* invariant tower — including
the odd, bending-sensitive extrinsic sector.
**Criterion:** exact arithmetic covering every invariant the engine emits; minimal
machinery.
**Alternatives and why each loses:**
- *ℚ only* — provably insufficient: odd-order invariants carry √q, and that sector is
  the derived defence to the isometric-bending attack.
- *General algebraic number fields / symbolic radicals* — provably unnecessary: the
  parity law shows nothing beyond one √q ever occurs in the tower. Generality buys
  cost for zero covered objects.
- *Ball arithmetic over ℝ* — enclosure, not exactness (see A-001).
**The parity law is itself the optimality proof: two rungs are necessary (ℚ fails) and
sufficient (nothing above √q occurs).**
**Displacement:** an invariant entering the engine whose value provably leaves ℚ(√q) —
that would be a mathematical finding first and a tower extension second.
**Obligations: DISCHARGED 2026-07-06** — gate G0.3 closed (`tests/gate_03.py`,
14/14 ×2): exact arithmetic, guards, float exclusion, parity retrodiction.
**Status: ESTABLISHED — implemented and certified.**

## A-004 — Stratum-typed refusals

**Origin:** refuse-not-lie discipline; degeneracy-as-stratum leads. Design precedent.
**Need:** degenerate inputs are diagnostic findings (lockstep channels, vanishing
gradients), and the certificate must render every non-result in plain language.
**Criterion:** no silent garbage, no crash paths; every refusal classifiable and
renderable; strata carry their diagnostic content.
**Alternatives and why each loses:**
- *NaN / None / exceptions* — silent garbage or crash; both banned by the engine's
  definition.
- *Flat error codes* — discard the stratum content, which is exactly the diagnostic
  value of a degeneracy.
- *Confidence scores in place of refusal* — smuggles statistics into the computation
  layer; violates the layer separation.
**Displacement:** none — the criterion admits only this form. Vocabulary grows by
new records, each token with its plain rendering.
**Obligations: DISCHARGED 2026-07-06** — gate G0.4 closed (`tests/gate_04.py`,
12/12 ×2): refusals first-class through cells, composition, and certificates; every
token renders plainly; the double-run emission law enforced in code.
**Status: ESTABLISHED — implemented and certified.**

## A-005 — The Validation Programme (Kessler v1.0, 2026-04-07)

**Origin:** `Validation Programme.md`. Reference only.
**Need:** an acceptance harness whose stages are cumulative hard gates, or the engine's
claims are self-graded.
**Criterion:** staged coverage of the forced question sequence — is the maths right →
how small a change is visible → what corrupts it → does it detect real faults → blind →
what breaks it → versus incumbents → self-consistent → deployable.
**Alternatives and why each loses:**
- *Derive a fresh programme* — the nine questions are near-forced by the claim
  structure; a fresh derivation reproduces them at the cost of losing the imported
  cross-domain discipline (interference protocol, LoD, blind protocol, adversarial
  stage) already encoded.
- *Ad hoc per-dataset testing* — no gates, no cumulative validity, no limitation
  disclosure; the incumbent failure mode.
**Best shape:** re-authored at Layer 3 with corrected sensors, exactness/statistics
separation per stage, and metamorphic relations MR-3/MR-4 as identity checks (now
theorems).
**Displacement:** stage *structure* — by a demonstrated gap the nine questions miss;
stage *parameters* (thresholds, corpora) — evidence-bound and expected to move.
**Status: ESTABLISHED (structure; parameters evidence-bound).**

## A-006 — The capability contract (origin method inventory)

**Origin:** `Lloyd_Method_Portfolio.xlsx`. Reference only.
**Need:** a clean rebuild's classic failure is silently shipping without capabilities
the old engine had.
**Criterion:** an enumerable checklist the rebuild is graded against; completeness of
inventory.
**Alternatives and why each loses:** *rebuild from memory* — the documented drift
failure mode; *no contract* — silent loss, discovered by users. The origin inventory is
the only complete method census that exists (37 methods + its own gap list).
**Displacement:** a demonstrated inventory error (method missing from the census).
**Obligations:** `CAPABILITY_CONTRACT.md` authored fresh at G3.0; no origin code enters.
**Status: ESTABLISHED.**

## A-007 — The corrected invariant sensor set

**Origin:** post-pivot mathematics (numerator tower; carrier; shape moment; triangle
localization; parity). Cited as mathematics.
**Need:** the engine's sensors, each shipping invariance group + blindness set +
completeness scope.
**Criterion:** recalibration-proof (invariant), complete at declared scope, exactly
computable, blindness derivable.
**Why nothing beats it — the dominance cases, one per sensor:**
- *Carrier O* — the normal-form theorem forces every invariant sensor to factor
  through O. The carrier is not one choice among alternatives; it is the
  coordinatization of **all** invariant sensors at order 2. Competitors are either
  functions of O or provably non-invariant.
- *Numerator tower* — strictly dominates the ratio sensor it corrects: same coupling
  sensitivity, exact (not approximate) self-fault blindness, scale invariance without
  the quotient. Proven.
- *Shape moment* — scalars are provably insufficient at n ≥ 5 (dimension threshold);
  the isotypic moment set captures exactly the invariant content at its degree. A
  better degree-2 sensor cannot exist; it could only be a different basis of the same
  content.
- *Localization channels* — proven support inclusion ({moved} = {S ⊇ e*}); the
  alternative (contribution-style attribution) has no support theorem.
**Scope stated exactly:** mathematical dominance on the regular locus at declared order/
degree. **Not claimed:** empirical dominance on real data — that question is routed to
armed kill conditions at G3.1 (A/B rerun) and G3.2 (shape-moment wager), and the global
completeness tier remains OPEN as successor work (portfolio priority #2).
**Displacement:** per sensor, by a certified counterexample inside its stated scope, or
by a completed global tier changing the completeness statement.
**Obligations: DISCHARGED 2026-07-06** — G1.2 closed (`tests/gate_12.py`,
`src/cella/sensors.py`): each sensor ships exact reference values + its blindness
statement; numerator tower `kappa_2 == kc`, exact self-fault blindness; four mutants bite.
**Status: ESTABLISHED (mathematical scope); empirical scope gated, kills armed.**

## A-008 — The active role layer at n=3 (role charts, named channels, A_c, faithful fingerprint)

**Origin:** "The Active Role-Jet Orbit Calculus for Constraint-Surface Roles" (W. Lloyd,
2026-06-28, foundational); "Role-Channel Anisotropy of DBP Surfaces" and "Two Geometric
Readings of a Thermodynamic Surface" (companions, 2026-06-28). Reference only, never a
dependency.
**Need:** the Tier-1 fingerprint lever and G1.0's n=3 cross-check need the layer that
says *which chart* a channel was read in, *why* the unordered channel triple is
chart-independent (the orbit theorem), *when* the fingerprint map is faithful, and
*which strata refuse*. Without it, channel values are chart-relative numbers with no
identity semantics.
**Criterion:** chart-independence proven, not assumed; faithfulness with an explicit
closed-form degeneration locus; exact-ℚ computable on the regular locus (a closure
theorem, not hope); every failure a typed stratum.
**Alternatives and why each loses:**
- *Single-chart channels* — provably chart-relative (RC-4 F3: the triple permutes under
  active recharting; any fixed slot moves).
- *Ratio diagnostics* — the refuted ratio law; strictly dominated by the numerator
  tower (A-007).
- *Ad-hoc symmetrization (max/mean over charts)* — loses the faithfulness certificate;
  distinct states can collide with no witness of when.
- *Derivable-with-work* — the orbit theorem forces any invariant of the order-2
  coupling data to factor through this carrier; a competitor is either a function of it
  or provably non-invariant.
**Displacement:** a certified counterexample to faithfulness off the loci Λ_ρ = 0
within the stated scope (order 2, regular locus, n=3), or a witness with strictly
larger domain.
**Obligations:** mathematics DISCHARGED 2026-07-06 —
`verification/recert_role_channels.py` CLEAN 19/19 ×2 (`3d7ed1bf`): active S3
relations, A_c three equivalent forms + telescoping, faithfulness determinant
`8·Λ_P·Λ_D·Λ_S / q0^6`, exact-ℚ closure (t-denominators are pure a-powers), keystone
pins (A_c = 42793/1555848; K_G = −3/49 cross-route against recert_transport_law),
orbit action realized on the channels (t: P↔D, s: D↔S), and both degeneration strata
witnessed. Remaining at gates: G1.0 — DISCHARGED 2026-07-06
(`src/cella/carrier.py::channels_n3_crosscheck`, n=3-fenced, labeled per the
label-convention case law; certified `tests/gate_10.py` P4, keystone triple
retrodicted against RC-1/RC-4); G1.2 — sensor entry with blindness statement, still
gated. **Token naming (A-004
discipline):** this record names `ROLE_CHART_UNAVAILABLE` (role-singular stratum:
a = 0 or b = 0) and `CHANNEL_ISOTROPIC` (Λ_ρ = 0: fingerprint rank drop) for admission
to the closed vocabulary at their first engine use; RC-4 certifies their mathematical
content now.
**Status: ESTABLISHED (mathematics recertified in-repo; engine wiring gated at
G1.0/G1.2).**

## A-009 — Two refusal tokens for Layer 1 entry: `CODIM_UNSUPPORTED`, `ROLE_CHART_UNAVAILABLE`

**Origin:** design freeze rule 3 (ROADMAP) names `CODIM_UNSUPPORTED`; admission A-008
names `ROLE_CHART_UNAVAILABLE` for admission at first engine use. First engine use is
G1.0 (this record precedes that use, per A-004 discipline).
**Need:** G1.0's carrier API has two scope boundaries that are findings, not crashes:
(1) constraint blocks of length > 1 — the API can express what the codim-1 theory
cannot yet compute (stop-line: no invented system semantics); (2) a gradient with a
zero component — the surface cannot be solved for that variable, the corresponding
output chart does not exist (the general-n form of RC-4's F5 locus, where every
t-denominator is a power of the vanishing component).
**Criterion:** A-004's — no silent garbage, no crash paths, every refusal classifiable
and renderable, strata carry their diagnostic content.
**Alternatives and why each loses:**
- *Reuse `SINGULAR_GRADIENT` for the component-zero stratum* — provably wrong typing:
  `SINGULAR_GRADIENT` is ∇F = 0 (no surface direction at all); a component zero with
  ∇F ≠ 0 has a perfectly good surface, just no chart in that direction. Conflating
  them discards exactly the stratum content the token exists to carry.
- *Generic `INDETERMINATE`* — discards which roles failed; the diagnostic value IS the
  named component set.
- *Exceptions / None* — banned by the engine's definition (A-004).
**Plain renderings (closed-vocabulary discipline, no raw token in any plain register):**
- `CODIM_UNSUPPORTED` → "this computation covers a single constraint; a system of
  constraints was given and is not yet supported"
- `ROLE_CHART_UNAVAILABLE` → "the surface cannot be solved for one of its variables
  here, so that reading direction does not exist"
**Deliberately NOT admitted here:** `CHANNEL_ISOTROPIC` (also named by A-008) — its
first engine use is the G1.2 fingerprint sensor, not G1.0's carrier; it enters by its
own record then.
**Displacement:** a certified refinement of either stratum into typed sub-strata with
distinct diagnostic content.
**Obligations: DISCHARGED 2026-07-06** — both tokens exercised through cells and
certificates (`tests/gate_10.py` P5/P7, 42/42 ×2 `4af1adca`); refusal precedence
pinned (block shape before gradient strata; all-zero gradient stays
`SINGULAR_GRADIENT`); `tests/gate_04.py` count assertion updated 5 → 7 per the
declared PREREG P9 — its stdout pin `3775a7fb` proved invariant under the fix, and
the tripwire fired as designed (pre-edit assertion fails under the grown vocabulary).
**Status: ESTABLISHED — implemented and certified.**

## A-010 — Refusal token for the fingerprint rank-drop stratum: `CHANNEL_ISOTROPIC`

**Origin:** admission A-008 names `CHANNEL_ISOTROPIC` (`Λ_ρ = 0`: fingerprint rank drop)
for admission at its first engine use; RC-4 (`verification/recert_role_channels.py`,
`3d7ed1bf`) certifies its mathematical content — faithfulness determinant
`det = 8·Λ_P·Λ_D·Λ_S / q0⁶` and both degeneration strata witnessed. First engine use is
the **G1.2 fingerprint sensor**, not G1.0's carrier (A-009 deliberately deferred it).
Reference only, never a dependency.
**Need:** the fingerprint sensor factors through the role-channel map whose faithfulness
is `det = 8·Λ_P·Λ_D·Λ_S / q0⁶`. Where a role-channel anisotropy `Λ_ρ` vanishes the map
drops rank: distinct states become fingerprint-indistinguishable. The sensor may neither
return a value there (it would certify a separation it cannot make — the false-collision
failure the faithfulness certificate exists to prevent) nor crash. It is a diagnostic
finding: *the fingerprint cannot separate here, and here is which channel went isotropic.*
**Criterion:** A-004's — no silent garbage, no crash, every refusal classifiable and
renderable, the stratum carries its diagnostic content. Sharpened by the named downstream
consumer (the LEAD-2 valuation campaign's Stage-E stratum atlas,
`reports/LEAD2_Role_Singularity_Valuation_Brief.md`): the refusal must be
**content-bearing** — it names *which* `Λ_ρ` vanished (P, D, or S) and carries the
rank-drop witness (the collapsed direction), never a bare flag.
**Alternatives and why each loses:**
- *Reuse `ROLE_CHART_UNAVAILABLE`* — wrong typing: that token is the `a=0`/`b=0`
  role-singular stratum (a reading-direction chart does not exist); `CHANNEL_ISOTROPIC`
  is `Λ_ρ=0` on a perfectly good chart where the *fingerprint* loses faithfulness. RC-4
  witnesses the two loci separately; conflating them discards which failure occurred.
- *Return the rank-deficient value anyway* — certifies separation that does not exist;
  the exact false-negative-on-collision A-008's faithfulness certificate guards against.
- *Generic `INDETERMINATE` / bare flag* — discards which channel went isotropic and the
  rank-drop witness, the content the LEAD-2 atlas consumes; a bare flag makes the stratum
  atlas unbuildable.
- *Exceptions / `None`* — banned by the engine's definition (A-004).
**Plain rendering (closed-vocabulary discipline, no raw token in any plain register):**
`CHANNEL_ISOTROPIC` → "one of the role channels is isotropic here (its anisotropy Λ went
to zero), so the fingerprint cannot tell these states apart; the affected channel and the
collapsed direction are named."
**Displacement:** a certified refinement of the `Λ_ρ=0` stratum into typed sub-strata
(which states collide; or a higher-order fingerprint that separates part of the current
locus) with distinct diagnostic content.
**Obligations:** G1.2 Stage B/C — the token wired at the fingerprint sensor with **both
strata witnessed** (`Λ_ρ=0` rank drop AND the `a=0`/`b=0` `ROLE_CHART_UNAVAILABLE` chart
failure); the refusal names the vanished channel + rank-drop witness through cells and
certificates; the closed vocabulary grows **7 → 8** (`gate_04` count assertion updated in
the same commit, stdout pin `3775a7fb` expected invariant — the count lives in the
assertion, P9 precedent); refusal precedence pinned against the existing strata. Certified
at `tests/gate_12.py`, byte-stable ×2.
**Status: ESTABLISHED — certified. Engine wiring DISCHARGED 2026-07-06:
`CHANNEL_ISOTROPIC` wired at the fingerprint sensor (`src/cella/sensors.py`), both strata
witnessed, the refusal names the isotropic channel; vocabulary grown 7 → 8 (`gate_04`
count assertion updated, stdout pin `3775a7fb` invariant per P9; `gate_10` re-pinned
`372a7f54`); certified `tests/gate_12.py`, byte-stable ×2 (`adf6316f`).**

---

*Ledger discipline: append-only; displaced records stay visible with successors named.
An artifact used anywhere without a record here is a defect. A record that cannot close
its case stays OPEN with its missing work named — OPEN records are the R&D queue.*
