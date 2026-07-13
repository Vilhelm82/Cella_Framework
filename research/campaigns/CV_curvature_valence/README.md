# Curvature Valence — Local Laws of Collapse and Divisors

Campaign id: **CV**. Opened 2026-07-08. Self-contained: verify scripts live in
`verify/` here, not in root `verification/` — a deliberate divergence, because
self-containment is the fresh-session guarantee.

## Bootstrap (fresh session, in order)
1. Read this file.
2. Read `LOG.md` top to bottom — it is the append-only spine. Never edit an
   entry; corrections are new entries referencing old ones.
3. Read `CLAIMS.md` for current claim tiers.
4. The **last GATE entry** in the log states where the campaign stands and
   what awaits Will's GO. Nothing advances without it.

## The rig (derived, not house format — each mechanic blocks a named failure)
| Failure blocked | Mechanic |
|---|---|
| post-hoc reframing | PREDICT entry committed **before** battery code exists (git commit order = timestamp + pin) |
| session drift | one append-only LOG.md; every session reads it first |
| self-certification | verify scripts re-derive from first principles (Christoffel/Ricci); probe never calls referee |
| nondeterminism | every battery runs twice; both stdout sha256 hashes pasted in RESULT |
| goalpost-moving | forks pre-named in PREDICT with consequences attached; a FAIL fires its branch, never softens |
| reparameterization | sweep verdicts recorded before Stage C; K5 standing (change-of-variables from a swept result = KNOWN-adjacent, never claimed) |
| status inflation | tiers: proven / symbolic (family stated) / computer-verified (gates stated) / measured; all verdicts scoped "within tested space" |
| ceremony + scope creep | anything outside the charter (new probes, reorderings) needs a GATE entry stating what landed to justify it |

## Entry types
CHARTER (once) · GATE (3–6 lines before any stage: what landed, does the plan
still hold, GO/adjust) · PREDICT (falsifiable statement + decision rule +
pre-named branches, committed before the battery) · RESULT (what ran, twin
hashes, which branch fired, one paragraph) · SWEEP · CLAIM · KILL · CLOSE
(sits on Will's desk until signed) · NOTE.

## Commit discipline
One commit per log entry; the entry commits **before** its artifact.
`git add` is always path-scoped to this folder.

## Sweeps
O1 Varchenko–Kouchnirenko–Khovanskii · O2 Dobarro–Ünal · O3 Kasner + horn
blow-up rates. Verdicts CLEAR / OVERLAP-MINOR / OVERLAP-FUNDAMENTAL /
UNCERTAIN, one file each in `sweeps/`. **Sweeps block Stage C PREDICTs, not
Stage B** (a measurement is a valid datum regardless of the literature).

## Standing kills and fences
See ENTRY 001 in LOG.md — K1–K5 armed; fences explicit. External inputs enter
only by in-campaign re-derivation (fresh code); verbatim import would need an
ADMISSIONS.md case (Will's hand).
