# Design Seed — The Static Fragility Type

> **STATUS: SEED / DESIGN DRAFT — not a warranted campaign, not canonical.** Output
> of a brainstorming pass (2026-06-14, Will + Claude). Awaiting Will's **placement
> ruling** before any brief or build. No substrate touched; spine stays FENCED;
> cella-as-trunk remains the standing frontier untouched by this. File presence here
> is **not** a warrant to execute (see memory: file-presence-is-not-warrant).

**One line.** A forward static analysis that assigns every site of a computation a
**fragility type `⟨recoverability, exposure⟩`** by walking the operation-DAG once at
authoring time — flagging, *before execution*, the handful of sites that actually
need exact treatment. Cost is O(program structure), not O(data) — which is why it
scales where lanes-everywhere cannot.

**Taproot (proven).** WARP's CL-W1 (HR139) proved factorability is *statically
decidable by walking the op-DAG, no exact run required*, and CL-W3 marked the
honest boundary (rational-op class decidable; Richardson-undecidable past the
transcendental wall → refuse). This design generalizes that result; it does not
re-litigate it.

---

## 1. The object

A per-site **product type `⟨recoverability, exposure⟩`**, inferred by a single
**forward pass over the operation-DAG** at authoring time.

- **Axis A (recoverability) generalizes `D_static`** — one bit ("factors?") → a
  richer recoverability grade.
- **Axis B (exposure) is a NEW graft, not part of the `D_static` walk.** It is the
  operand-conditioning/exposure channel that **CL-W2's AST-seam proof specifically
  forbade `D_static`'s verdict path from reading** (that purity was the factorability
  claim's whole point). The fragility type runs the `D_static` walk (axis A)
  *alongside* a second forward pass over the exposure channel (axis B). The exposure
  axis does **not** fall out of the `D_static` walk for free — it is the design's one
  new build.

Cost lives in the program's structure, not its data size.

## 2. Axis A — recoverability (inherited)

Lattice: `exact ⊑ exactly-recoverable ⊑ construct-to-tolerance ⊑ undecidable(refuse)`.
Join = least-recoverable (worst case). Transfer = rooted in the `D_static` `AtomKind`
walk; boundary inherited from CL-W3 (past the transcendental wall → `undecidable →
refuse`, never bluff).

## 3. Axis B — exposure (the one new build)

Qualitative **tiered** lattice:
`inert ⊑ {L1 ⊑ L2 ⊑ L3 ⊑ L4} ⊑ cancelling ⊑ unbounded`. Join = max.

- **Axiom-3-native (the design's spine).** A site is classified **against a declared
  contract / provable protection condition** — it never *infers* a magnitude. Absent
  a covering declaration, the site lands conservatively at `cancelling`. This is the
  same epistemic as the rest of Cella (classify against a declared budget, refuse
  beyond it); the opposite move (propagate an inferred numeric loss bound) is what
  Daisy/FPTaylor do, imports the conservative-bound blow-up, and needs widening that
  turns the trivially-terminating `join=max` into a soundness-delicate fixpoint.
  **Rejected by design.**
- **The middle tiers are the HR134 protection predicate (L1–L4)** — already proven,
  already CFS-consumed: a *graft point*, not an invention.
- **Refine by adding tiers, never numbers.** If `cancelling` over-flags (the known
  soft spot of `join=max`), the response is to split `bounded` into more
  declared-envelope tiers (≤1-binade / ≤k-binade / Sterbenz-class), each still
  qualitative, still `join=max`, still terminating, still Axiom-3-native — never to
  slide into a propagated magnitude. The tiering hooks are designed in from day one.
- **Quantitative bound (the rejected option) is pushed out to the consumer's cost
  projection**, never into the certified type.

## 4. The product, the join, and the interaction

Site type `⟨rec, exp⟩`; join is **per-axis** (the axes are independent:
rec → least-recoverable, exp → max).

The axes **interact** to de-flag exposure's over-approximation — but the de-flag is a
**relaxation**, and relaxations are never free (see §6 for the obligation it carries):
- `cancelling × exactly-recoverable` → routed to the cheaper **account-lane** rung
  instead of full-exact (the UNDERFLOW-WITNESS-ULP case: `(x+1)−x`, total float
  cancellation, residue recovers TRUE exactly).
- `cancelling × not-recoverable` (or `× undecidable`) → the **genuine** "treat
  exactly / refuse" site.

**The de-flag is the one seam where under-flagging can sneak in.** Routing a
`cancelling` site to the cheap lane is sound **only if** the `exactly-recoverable`
verdict is itself trustworthy — i.e. **iff CL-W2 holds at that site** (the
recoverability verdict is the pure structural `D_static` classification with CL-W1's
zero-false-verdicts property, not a data-dependent guess). This is a
**verify-not-assume** obligation per site, **not** a free antidote: if the
recoverability axis ever falsely marks a not-recoverable site recoverable, the policy
ships a genuinely-fragile site to the cheap lane and produces exactly the silent wrong
answer §6 forbids.

## 5. Consumers (the in-scope set)

Both static, authoring-time, **engineering-track**; Covenant 3 holds — the type
certifies *where* float is unsafe, **never** speed. (Out of scope by Will's choice:
CFS rewrite-safety, and cella-as-trunk conditioning-as-projection.)

1. **Standalone fragility verifier** — annotates each site's `⟨rec, exp⟩` and
   surfaces the handful of `cancelling × not-recoverable` sites: "where it breaks,
   before you run it."
2. **Selective-precision policy** — emits a **graded upgrade ladder**, not a binary:

   | `⟨rec, exp⟩` | policy |
   |---|---|
   | low exposure (`inert`/bounded tiers) | **bare float** — provably accurate enough |
   | `cancelling × exactly-recoverable` | **account / residue lane** — cheap; the residue recovers TRUE |
   | `cancelling × not-recoverable` | **full exact** |
   | `× undecidable` (past the wall) | **refuse** |

   The scaling claim holds because the type *proves how few sites reach the expensive
   top of the ladder*.

   Soundness contract: **a site the type marks safe is genuinely safe to float.**

## 6. Soundness stance

Soundness is **two-axis, and the axes round in OPPOSITE directions** — this is the
contract, and §4's de-flag is sound *only* because of the second half:

- **Exposure rounds UP toward `cancelling`** (over-approximate loss; when unsure,
  *more* fragile). Sound-but-not-complete, like the HR134 predicate: marked-low ⇒
  genuinely low; marked-cancelling ⇒ *maybe*.
- **Recoverability rounds DOWN toward `not-recoverable`/`undecidable`**
  (under-approximate recoverability; when unsure, *less* recoverable). It must
  **never** mark a not-recoverable site `exactly-recoverable` — that single false
  positive is what would route a fragile site to the cheap lane (§4).

Both directions serve one goal: **a site the type marks safe — low exposure, *or*
recoverable — is genuinely so.** The static type lives on the *exposure* axis (it
sees exposure, never *realized* loss — bigraded-jet Stage-B, glossary §13).
Over-flagging is the acceptable error; under-flagging (a silent wrong answer) is the
one it must never make — and the **only** place it can enter is the §4 de-flag, which
is why that seam is a verify-not-assume obligation, not a free antidote.

## 7. Placement & relationship (for Will's ruling)

- **Own engineering-track seed** (verifier + precision-policy). The consumer choice
  settled this: it is not CFS and not cella-as-trunk.
- **Sibling to CFS, not its owner.** They share the forward-static-analysis idea, but
  CFS's rewrite-admissibility (protection type ⟶ region-guard coverage) is out of
  scope here. CFS could later consume this engine; this design does not absorb CFS,
  and the two must not build the same forward-static-analysis twice under two names.
- **cella-as-trunk untouched**; spine stays FENCED; no spine claim, no G-claim.
- HR131 Option-A trigger watch (per the CFS brief): the analysis is authoring-time
  and symbolic, so it does **not** pull the per-op-typed-scalar promotion — *unless* a
  real guard set turns out to need runtime per-op witnesses. Re-evaluate at brief
  time. Will rules.

## 8. Open — deferred to brief-time (not blocking the placement ruling)

1. **The declared-contract / precondition language** — how a site's input envelope /
   region guard is declared so the exposure transfer can classify against it.
2. **The per-op transfer table.** Note (Will's §2 nit): the recoverability transfer
   is rooted in the `AtomKind` walk, but `AtomKind` only separates the rational-op
   class from the wall — the **exact** (float op itself exact, residue == 0) vs
   **exactly-recoverable** (residue ≠ 0 but ∈ `R_exact`) split needs the
   **residue-preservation check**, and is partly data-dependent (so likely
   contract/exposure-mediated). It is not a clean `AtomKind` read.
3. **The L1–L4 graft mechanics** — wiring the protection predicate in as the exposure
   middle tiers.
4. **A tightness campaign — falsifiable, with an armed kill** (NOT open-ended
   tier-counting, which can only confirm and never refute). Pre-declare, on a *real*
   pipeline, thresholds the apparatus can MISS — e.g. (a) the verifier flags ≤ **X%**
   of sites as `cancelling × not-recoverable` (the triage is genuinely selective),
   AND (b) the precision-policy recovers ≥ **Y%** of the exact-everywhere cost (the
   scaling thesis pays off). X and Y frozen pre-run. **Miss either → REFUTED:** the
   qualitative-tier type is too coarse to be useful on real workloads and the central
   bet (structural triage beats lanes-everywhere) fails. This is the row that can land
   in the empty REFUTED column.

---

*Brainstorm provenance: 2026-06-14. Axes (recoverability × exposure, cost
consumer-derived), exposure representation (qualitative tiered, Axiom-3-native,
`join=max`, refine-by-tiers), and the consumer set (verifier + precision-policy) were
Will's calls in session; the L1–L4 graft, the cross-axis de-flagging, and the graded
ladder are the synthesis. Next step is Will's placement ruling, then (on GO) a brief.*
