# First-hand repository retrieval and maintenance examples ledger v1.0

**Date:** 2026-07-14

**Purpose:** training and evaluation material for a local model that maintains,
organizes, indexes, and retrieves Cella repository knowledge

**Evidence basis:** direct CLI-agent actions performed during the Cella
Continuation Engine campaign and the subsequent repository-wide recovery pass

**Status:** non-normative training design under `docs/`; repository truth remains
owned by `STATE/`

**Machine-readable companion:**
`docs/agent_training/first_hand_repository_examples_v1.0.jsonl`

**Documentation-maintenance companion:**
`docs/agent_training/DOCUMENT_CONSOLIDATION_PRUNING_AND_CLAIM_REVIEW_LEDGER_v1.0.md`

## 0. Executive finding

The repository has a sound epistemic layout but an incomplete retrieval surface.
`STATE/CURRENT.md` correctly defines the authority order:

```text
STATE/    authoritative canon
engine/   executable behavior
research/ historical notebook unless STATE points into it
docs/     governance and design context
archive/  sediment, never authoritative
```

The difficulty encountered by the agent was not lack of material. It was that
`STATE/RESULTS.md` and `STATE/DEFINITIONS.md` are population-pending while large
amounts of relevant work already exist elsewhere. Therefore a correct maintenance
model needs two distinct abilities:

1. retrieve candidate material comprehensively from non-canonical regions;
2. refuse to confuse discovery with canonical promotion.

This distinction should be the central data signal. A weak model either stops at
the empty canon and reports that no work exists, or trusts polished historical
material as current truth. The desired model reports:

```text
not migrated to canon != absent from repository
found in repository != authorized to bear load
exact implementation != theorem-owned release
index entry != independent evidence
```

## 1. Training-record schema

Every example in the companion JSONL uses these fields:

```text
example_id          stable first-hand example id
task_type           retrieval, authority, scope, maintenance, or validation
user_intent         the practical request being handled
observations        repository facts available to the agent
target_actions      ordered actions the model should take
target_conclusion   concise correct outcome
negative_action     plausible but incorrect behavior to penalize
signals             classification labels for training/evaluation
source_paths        exact repository evidence used by the example
```

For supervised training, `target_actions` and `target_conclusion` are positive
targets. `negative_action` is a contrastive negative. For evaluation, success
requires both correct retrieval and correct authority/scope classification.

## 2. First-hand event ledger

### FH-001 — The agent did not begin with the repository canon

**Task:** Continue a named CCE campaign from a detailed handoff.

**Observed action:** The agent followed the explicit campaign handoff and current
campaign reports without first reading `README.md` and `STATE/CURRENT.md`.

**Pain caused:** The agent learned the campaign-local authority hierarchy before
the repository-global hierarchy. It later had to reconcile “canonical paper” in a
handoff with the root rule that only `STATE/` is authoritative.

**Correct trained behavior:** For every nontrivial repository task, read:

```text
README.md
STATE/CURRENT.md
docs/PROJECT_INSTRUCTIONS.md
```

before interpreting task-local status documents. Explicit user scope still controls
the task, but `STATE/` controls repository truth.

**Desired repository signal:** A machine-readable boot manifest at a fixed path,
plus an automated check that agent-facing task files link back to it.

**Training contrast:** Penalize immediately treating a campaign handoff as the
highest repository authority.

### FH-002 — Empty canon was easy to misread as absent mathematics

**Task:** Determine whether existing work closes CCE-5 through CCE-8 gaps.

**Observed state:** `STATE/RESULTS.md` and `STATE/DEFINITIONS.md` explicitly say
`POPULATION PENDING`.

**Pain caused:** A strict canon-only search would falsely conclude that almost no
load-bearing result exists. A broad search finds substantial candidate material,
but its authority is not yet ratified in `STATE/`.

**Correct trained behavior:** Detect the population-pending marker and emit the
typed state:

```text
CANON_NOT_POPULATED_SEARCH_FALLBACK_REQUIRED
```

Then search `engine/`, `research/`, `docs/`, and finally `archive/`, classifying
everything found as candidate evidence until a canon/admission link is located.

**Desired repository signal:** A `canon_population_status` field in a root manifest
and explicit fallback search roots.

**Training contrast:** Penalize both “not in STATE, therefore nonexistent” and
“found outside STATE, therefore current.”

### FH-003 — The active campaign was absent from `STATE/CURRENT.md`

**Task:** Identify the current continuation campaign and its live handoff.

**Observed state:** `STATE/CURRENT.md` names MCP rebuild and Pathfinder
self-containment, but not the active CCE-4--8 work supplied by the user.

**Pain caused:** The agent could not resolve whether CCE was current global work,
a user-local branch of work, or a historical campaign by consulting the canonical
entry point.

**Correct trained behavior:** Respect the explicit user handoff as task scope while
reporting that the campaign is not registered in canonical current state. Do not
silently edit `STATE/CURRENT.md`; generate a proposed state delta for maintainer
ratification.

**Desired repository signal:** `STATE/CAMPAIGNS.json` or one
`research/campaigns/<campaign>/CURRENT.json` per campaign, referenced by
`STATE/CURRENT.md`.

### FH-004 — Stage reports became stale after a broader source recovery

**Task:** Explain what truly blocks CCE-5 through CCE-8.

**Observed action:** The first audit prioritized live theorem paths named by the
handoff. Later searches of `docs/files`, production code, derivations, and archive
material found:

```text
CCE-5  an exact absolute K/E connection
CCE-7  an established strict-chamber physical-root selection theorem
CCE-8  a complete role-calculus theorem body plus production implementation
```

**Pain caused:** Existing `CCE_N_STAGE_REPORT` and blocker JSON files remained
syntactically current while their factual summaries had become incomplete.

**Correct trained behavior:** Never overwrite provenance. Create a superseding
finding with explicit field-level corrections, then propose in-place canonical
status updates. Retrieval should rank the newest applicable supersession above the
older report.

**Desired repository signal:** Every report needs:

```text
artifact_id
status
effective_date
supersedes
superseded_by
scope
```

with a validator that forbids two simultaneously current reports for one scope.

### FH-005 — The Encyclopedia helped discovery but was not new evidence

**Task:** Search the Cella repository and Lloyd Mathematics Encyclopedia for work
covering the continuation gaps.

**Observed action:** Subject pages in the Encyclopedia made R5, role-jet, period,
and monodromy material much easier to find.

**Pain caused:** The agent initially described the Encyclopedia as independently
corroborating Cella. The user corrected that it contained the same material.

**Correct trained behavior:** Use the Encyclopedia as an inverted index. Resolve
every entry to its underlying Cella source and deduplicate by artifact id or digest.
Never increase evidence count merely because the same claim appears in two stores.

**Desired repository signal:** Each index entry should carry:

```text
source_repository
source_artifact_id
source_path
source_digest
relationship: index_of | mirror_of | derived_summary_of
```

**Training contrast:** Penalize phrases such as “independent corroboration” when
the source identity is shared.

### FH-006 — `archive/Reference_Material/papers/current` contradicted itself

**Task:** Locate the canonical Paper-I role-cover source.

**Observed state:** The complete role calculus lives at:

```text
archive/Reference_Material/papers/current/dbp_orbit_calculus.tex
```

Production Pathfinder code cites `Reference_Material/papers/current/...`, while
the root repository doctrine says all of `archive/` is sediment and never
authoritative.

**Pain caused:** Filename semantics and region semantics disagreed. The source was
highly relevant and production-linked, but could not legally become authority by
discovery alone.

**Correct trained behavior:** Classify it as:

```text
material_support: yes
production_reference: yes
canonical_authority: no
required_action: admission or migration plus fresh verification
```

**Desired repository action:** Move current source bodies out of `archive/`, or
replace production references with canonical artifact ids resolved through a
registry. A validator should reject production source references into `archive/`.

### FH-007 — Duplicate papers looked like multiple authorities

**Task:** Audit Paper IV and its verification corpus.

**Observed state:** `galois_horizon_cover_v1_0.tex` appears in the theorem tree,
`docs/files`, and a publication package. Copies may be byte-identical.

**Pain caused:** Path-counting makes one theorem look like several mutually
supporting artifacts and forces agents to inspect each copy.

**Correct trained behavior:** Hash candidate duplicates, choose one canonical
artifact id, and classify other locations as declared mirrors or packaged copies.

**Desired repository signal:** A mirror manifest containing canonical digest,
mirror paths, packaging purpose, and whether byte identity is required.

**Evaluation:** Given three paths with one digest, the model must return one claim,
one authority, and two mirrors—not three evidence items.

### FH-008 — Claim granularity mattered more than keyword presence

**Task:** Decide whether the recovered Legendre connection closes CCE-5.

**Observed material:** `E_ATOM_DERIVATION.md` and `legendre_native.py` derive the
absolute rank-2 `(K,E)` Picard--Fuchs connection and a bilinear invariant.

**Pain caused:** A keyword search for “exact connection” could incorrectly mark
CCE-5 complete, even though CCE-5 needs a relative third-kind/inhomogeneous system,
divisor/exponent ledger, integral basis calibration, and compact-period corrections.

**Correct trained behavior:** Compare theorem input/output signatures, not titles or
shared nouns. Return `PARTIAL_SUPPORT` and enumerate the exact missing extension.

**Desired data signal:** Train scope entailment pairs:

```text
source claim: absolute rank-2 K/E system
target claim: relative third-kind basis-compatible continuation
relation: strict_subproblem_of
```

### FH-009 — A verifier partially succeeded before failing on a missing import

**Task:** Determine whether `legendre_native.py` is replayable evidence.

**Observed run:** Stages 1 and 2 completed exactly; Stage 3 failed with:

```text
ModuleNotFoundError: No module named 'verify_local_curvature_calculus'
```

`research/derivations/README.md` does disclose that the helper came from a
non-portable session path.

**Pain caused:** The derivation is useful, but “script exists” and “machine checked”
do not imply repository-self-contained replay.

**Correct trained behavior:** Record per-stage execution status and classify the
artifact as `PARTIAL_REPLAY_ONLY`. Never discard successful exact stages, and never
promote the whole script as clean.

**Desired repository action:** A dependency-health gate that imports or dry-runs
every verifier and records `self_contained`, `partial`, or `broken`.

### FH-010 — Planning providers were easy to mistake for executors

**Task:** Determine how much CCE-7 and CCE-8 runtime code already exists.

**Observed material:** Pathfinder `recognize/real.py`, `cover.py`, `wreath.py`, and
`curvature.py` contain exact admission logic, route steps, and certificate
obligations. Several contracts name `external.*_executor` modules that are not the
continuation runtime.

**Pain caused:** Rich route construction can look like an implemented adapter even
when execution, checkpointing, and independent replay are absent.

**Correct trained behavior:** Classify each capability independently:

```text
recognizer_present
planner_present
native_scout_present
executor_present
certificate_builder_present
independent_verifier_present
```

**Desired repository signal:** Capability manifests generated from provider
registration and import resolution, not prose summaries.

### FH-011 — Endpoint surface geometry was not corridor-wide clearance

**Task:** Decide whether Stage 2 closes CCE-6 surface admission.

**Observed material:** The Stage-2 surface dossier derives explicit fibre/angular
equations and shows a fixed dual contour avoids two finite discriminants. Its checker
passes 17/17 gates.

**Pain caused:** Those strong local results are close in language to the CCE-6
requirement, but CCE-6 needs positive exact bounds over the entire
`corridor x angular cover x fibre sweep`, including polar, norm, and boundary
collision loci.

**Correct trained behavior:** Preserve the endpoint theorem as reusable support and
return `DOMAIN_EXTENSION_UNPROVED` for the full sweep.

**Desired data signal:** Examples must train quantifier and domain comparison, not
only formula matching.

### FH-012 — Promoted theorem status and fresh in-repo authority are different

**Task:** Use R5 physical-root selection in CCE-7.

**Observed material:** `docs/files/LOG_ENTRY_R5_total_reality_v2.md` says promoted
and established after audit/counter-audit. `STATE/RESULTS.md` has not yet migrated
the result, and C-003 says documentary status is a claim until freshly certified
in-repo.

**Pain caused:** The mathematical result is strong support, but the repository's
current authority protocol does not permit a maintenance model to silently insert
it into canon.

**Correct trained behavior:** Report two axes separately:

```text
origin_status: established
state_canon_status: not_migrated
fresh_certificate_status: inspect/replay required
```

Then propose a migration record rather than declaring the canon updated.

### FH-013 — Source references were human-readable but not reliably resolvable

**Task:** Follow production code from a Pathfinder contract to its theorem source.

**Observed material:** Source references such as
`Reference_Material/papers/current/dbp_orbit_calculus.tex#thm:orbit` omit the
current top-level `archive/` prefix and use a TeX anchor that filesystem tools cannot
validate directly.

**Pain caused:** Agents must guess repository roots and manually search for basename
matches.

**Correct trained behavior:** Resolve references through artifact ids first, then
verify the path and theorem anchor. If resolution requires basename guessing, report
the reference as degraded.

**Desired repository action:** Replace free-form source strings with:

```json
{
  "artifact_id": "RC-ACTIVE-ROLE-ORBIT",
  "path": "research/paper/.../paper_i.tex",
  "anchor": "thm:orbit",
  "sha256": "..."
}
```

### FH-014 — Dirty migration state obscured intentional moves

**Task:** Record repository identity and preserve user work while adding campaign
artifacts.

**Observed state:** `git status` showed many deleted old paths, untracked moved
trees, and modified provider registration files.

**Pain caused:** An agent cannot safely infer whether a missing file was deleted,
moved but untracked, intentionally retired, or temporarily absent.

**Correct trained behavior:** Never repair or stage unrelated migration changes.
Record HEAD plus relevant file digests, and consult a migration manifest before
classifying path absence.

**Desired repository signal:** A temporary `STATE/MIGRATION.json` while a reorg is
in flight, listing old path, new path, intended status, and completion state. Remove
it only when the migration commits cleanly.

### FH-015 — A valid alternate implementation was mistaken for the primary path

**Task:** Continue the Cella campaign from a handoff.

**Observed event:** The handoff accidentally pointed to the valid campaign-local
`research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/pathfinder_m1_scout.py`
when the task required the primary typed Pathfinder under `engine/src/cella/pathfinder/`.

**Pain avoided:** Without the correction, the agent could have analyzed or modified
the wrong implementation for the task despite both implementations being valid.

**Correct trained behavior:** Validate every handoff path against region status,
production imports, source references, and current registry membership before use.
Classify alternate implementations by role and task scope; do not infer that a
non-primary path is stale, forbidden, or deprecated.

**Desired repository action:** A handoff linter that rejects references to deprecated
artifact ids or non-production paths unless explicitly marked historical context.

### FH-016 — “New task in the same folder” required deterministic task discovery

**Task:** Locate successive handoffs created in one campaign directory.

**Observed state:** Several task files existed with versioned names, but no
machine-readable pointer identified the active one.

**Pain caused:** Filesystem modification time, lexical version order, and user intent
can disagree. Guessing the newest filename is unsafe.

**Correct trained behavior:** Look for a current-task manifest. If absent, inventory
candidate task files and use explicit user direction; do not infer authority from
mtime alone.

**Desired repository signal:** `agent_tasks/CURRENT.json` containing task id, path,
version, status, prerequisites, supersedes, and expected outputs.

### FH-017 — Large handoffs mixed stable doctrine with fast-changing state

**Task:** Read the CCE-4--8 completion handoff.

**Observed material:** The handoff exceeds one thousand lines and combines stable
protocol, exact stage definitions, frozen digests, current blockers, and output
templates.

**Pain caused:** Every agent pays the full parsing cost, while the fast-changing
blocker section can become stale minutes after source recovery.

**Correct trained behavior:** Parse stable policy and task delta separately, and
never assume a dated blocker statement overrides newer evidence.

**Desired repository action:** Split handoffs into:

```text
CAMPAIGN_PROTOCOL.md       stable doctrine and schemas
CURRENT_TASK.json         active task, sources, prerequisites, outputs
CURRENT_STATE.json        completed stages, blockers, supersessions
```

### FH-018 — Reports must say what is extracted, not merely what was found

**Task:** Compile existing work supporting campaign continuation.

**Observed requirement:** The user specifically asked for the source plus what the
agent would extract.

**Why it matters:** A search report listing filenames creates another passive index.
An extraction report maps source content to a downstream state field, theorem lemma,
implementation primitive, certificate field, or remaining gap.

**Correct trained behavior:** For every source, emit:

```text
authority status
exact supported claim
exact extraction target
scope exclusions
verification state
remaining obligation
```

**Desired training signal:** Reward actionable source-to-consumer mappings over
document summaries.

## 3. Repository changes with the highest retrieval impact

The following actions would most materially reduce CLI-agent search cost.

| Priority | Action | First-hand reason | Acceptance test |
|---:|---|---|---|
| P0 | Populate `STATE/RESULTS.md` and `STATE/DEFINITIONS.md` claim by claim | The correct canon exists structurally but is empty, forcing broad historical recovery | A query for R5, role orbit, DBP corridor, or Legendre connection returns a stable R/D id before any historical path |
| P0 | Add `STATE/ARTIFACTS.json` as the canonical artifact registry | Paths, copies, authority, code, and verifiers are currently joined manually | Every load-bearing artifact resolves by id to one canonical path, digest, scope, implementation, and verifier |
| P0 | Add campaign and task current manifests | “Same folder” and dated handoffs do not identify active work deterministically | `CURRENT.json` resolves active task without mtime or filename guessing |
| P0 | Eliminate production references into `archive/` | Paper-I material was relevant but legally non-authoritative | Validation fails if production source metadata resolves under `archive/` |
| P0 | Encode supersession in machine-readable fields | Stale blocker reports remained apparently current | Exactly one current report per `(artifact_id, scope)`; predecessor points to successor |
| P1 | Generate the Encyclopedia from canonical artifact ids | It is useful for discovery but risks double-counting and drift | Every subject entry resolves to Cella artifact id and digest; no orphan entries |
| P1 | Add mirror/package manifests | Duplicate Paper-IV copies looked independent | Hash-equivalent copies are automatically grouped and labelled |
| P1 | Validate theorem/code source references | Free-form relative strings required basename searches | Every source reference resolves to an existing artifact id, path, anchor, and digest |
| P1 | Add verifier dependency-health gates | `legendre_native.py` was only partially runnable | All verifiers classified clean/partial/broken with exact failure reason |
| P1 | Add capability manifests for providers | Planner contracts looked like executors | Query returns recognizer/planner/scout/executor/certificate/verifier booleans separately |
| P1 | Add scope signatures to artifacts | Similar words hid strict domain differences | Source and target claims can be compared by domain, carrier, coefficient field, quantifiers, and output type |
| P2 | Add aliases and theorem-family tags | CCE ids, paper numbers, R5, RC, and filenames use different vocabularies | Searching any known alias returns the same artifact id |
| P2 | Add an in-flight migration manifest | Dirty moves made missing paths ambiguous | Every intended delete/move has a declared destination and state |
| P2 | Split stable protocol from current task state | Large handoffs are expensive and rapidly stale | Stable protocol digest remains unchanged when only blockers or task status change |

## 4. Proposed canonical artifact record

The minimum useful record is:

```json
{
  "artifact_id": "RC-ACTIVE-ROLE-ORBIT",
  "title": "Active Role-Jet Orbit Theorem",
  "kind": "theorem",
  "status": "candidate_for_migration",
  "canonical_path": null,
  "candidate_paths": [
    "archive/Reference_Material/papers/current/dbp_orbit_calculus.tex"
  ],
  "sha256": "f045a92762f68cd1ddfc83e243e76eb4739d720f8097bc6736e29195c88d2d01",
  "region_authority": "archive_non_authoritative",
  "scope": {
    "domain": "regular active-role locus",
    "coefficient_domain": "exact rational after localization",
    "jet_order": [1, 2],
    "exclusions": ["global gluing", "cross-adapter equivalence"]
  },
  "implementations": [
    "engine/src/cella/reference_lift.py",
    "engine/src/cella/pathfinder/recognize/curvature.py"
  ],
  "verifiers": [
    "research/verification/recert_role_channels.py"
  ],
  "mirrors": [],
  "supersedes": [],
  "superseded_by": null,
  "state_ids": [],
  "open_actions": [
    "fresh certificate review",
    "maintainer-ratified migration into STATE",
    "canonical theorem path assignment"
  ]
}
```

This record makes the correct conclusion cheap: useful source material exists,
exact code and verification exist, and canonical promotion is still pending.

## 5. Training task families

### 5.1 Retrieval ranking

Given a query, rank sources in this order:

1. matching `STATE/` R/D/G/C entry;
2. exact production code and gate named by that entry;
3. current campaign manifest and source-bound report;
4. research derivation or verifier candidate;
5. governance/audit context;
6. archive material;
7. external or mirrored index.

The model must still search lower ranks when the higher rank explicitly says
population pending or points to them.

### 5.2 Authority classification

Train the model to output independent dimensions instead of one vague status:

```text
repository_region
origin_claim_status
state_canon_status
fresh_verification_status
production_usage_status
release_status
```

This prevents “established in origin paper” from being collapsed into “current
Cella authority.”

### 5.3 Scope entailment

Examples should pair near-matching claims and require one of:

```text
equivalent_scope
strict_subproblem_of
strict_extension_of
overlapping_non_entailing
disjoint_carrier
contradictory
```

First-hand pairs include:

```text
absolute K/E connection        vs relative third-kind connection
fixed dual contour avoidance   vs corridor-wide surface sweep clearance
root-count planner             vs labelled-root continuation executor
order-2 role theorem           vs order-3 production operation
Encyclopedia subject page      vs underlying Cella theorem source
```

### 5.4 Maintenance decisions

Train explicit actions:

```text
index_only
propose_canon_migration
mark_mirror
mark_superseded
repair_reference
repair_verifier_dependency
create_gap_entry
create_campaign_manifest
no_write_without_ratification
```

### 5.5 Validation and hostile cases

The model should be tested against:

- a polished theorem in `archive/` with no STATE entry;
- an empty STATE ledger carrying `POPULATION PENDING`;
- two byte-identical papers with different filenames;
- a report whose blocker is contradicted by newer implementation evidence;
- a verifier that passes early stages then fails import;
- a provider with a recognizer but an external executor;
- an index entry pointing to the same underlying artifact;
- a deleted path that appears in an in-flight migration manifest;
- a user handoff naming a deprecated scout;
- a source whose theorem domain is strictly smaller than the requested domain.

## 6. Evaluation rubric

A repository-maintenance model should be scored separately on:

| Dimension | Required behavior |
|---|---|
| Retrieval recall | Finds all materially relevant underlying artifacts, including aliases and moved paths |
| Deduplication | Counts claims/artifacts by identity, not by path occurrence |
| Authority accuracy | Distinguishes STATE authority, production behavior, research candidates, and archive sediment |
| Scope accuracy | States exactly what transfers and what remains unproved |
| Verification honesty | Runs or inspects verifiers and records partial/broken status precisely |
| Mutation discipline | Proposes canon changes when ratification is required; does not silently promote |
| Supersession handling | Preserves provenance while ranking the applicable successor |
| Actionability | Maps each source to an extraction, consumer, validation, or gap action |
| Search efficiency | Uses manifests/ids first and broad filesystem search only as fallback |
| Explanation quality | Gives concise evidence paths, digests, and exact failure strings |

A single aggregate “found the right file” score is inadequate. The first recovery
pass found many right files but initially misclassified independence and understated
existing work. The training objective must reward epistemic correctness after
retrieval, not retrieval alone.

## 7. Recommended first dataset tranche

Start with a balanced set of examples:

```text
20 boot/canon-routing examples
30 artifact identity and mirror examples
40 authority classification examples
50 scope-entailment examples
30 verifier-health examples
30 supersession and stale-report examples
20 campaign/task-manifest examples
20 safe maintenance mutation examples
```

For each positive example, include at least one hard negative that shares most
keywords but differs in authority, scope, or execution status. The high-value signal
is the distinction, not the noun match.

## 8. Final design rule

Make the correct repository answer cheaper than a broad search, but train the model
to perform the broad search when the canon explicitly declares itself incomplete.

The ideal maintenance model should be able to answer every repository question in
this form:

```text
Canonical state says: ...
Candidate material found: ...
Identity/deduplication result: ...
Exact supported scope: ...
Verification state: ...
Required maintenance action: ...
No claim made beyond: ...
```

That output shape would have prevented every material retrieval or classification
error recorded in this ledger.
