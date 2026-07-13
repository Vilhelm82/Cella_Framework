# State Canon & Repository Reorganization — Design

**Date:** 2026-07-13
**Status:** Draft for user review
**Scope:** Repository layout, the STATE/ canon, session protocols for claude.ai
R&D sessions, the derivation-first protocol, and the migration plan.

---

## 1. Problem statement

The repo is a research monorepo: an installable program (the Cella engine, its
tests and tools) interleaved with a scientific notebook (campaigns, verification
scripts, benchmarks, reports, papers). Three failures follow from the current
structure:

1. **No authoritative state surface.** A fresh claude.ai session reconstructs
   project state from whatever is cheapest to reach. Today that is thirteen
   root-level markdown files of equal apparent authority, several of them stale
   handoffs. Sessions routinely rederive superseded results or import external
   answers that do not match the corpus.
2. **Unscoped normative prose.** Slogans like "floats are refused" are written
   as universal laws. A session reading one applies the widest possible
   interpretation and silently prunes valid solution space (any approach
   containing the trigger word).
3. **Import laundering.** When a gap is hit, sessions pattern-match a known
   classical solution and either import it directly or reconstruct it from
   corpus blocks — the same failure with the serial numbers filed off. The
   project is a first-principles experiment; derivation must proceed *from* the
   corpus, with external resemblance declared rather than smuggled.

The repo's own re-verification rule ("trust attaches to re-runnable
certificates, never to labels or memory") already states the correct
epistemology for mathematics. This design extends the same rule to **project
state itself** and to **the reasoning protocol of sessions**.

## 2. Design overview

Three coupled layers:

- **Layout** — carve the tree into five top-level regions with distinct
  epistemic status: `STATE/` (canon), `engine/` (program), `research/`
  (notebook), `docs/` (governance), `archive/` (sediment).
- **Canon** — a small, always-current, schema-disciplined `STATE/` directory
  that is the only authoritative surface. Schemas structurally exclude
  rhetoric; every rule carries scope, anti-scope, and an escape hatch.
- **Protocol** — a boot ritual, a close ritual, an openness protocol, and a
  derivation-first protocol, all injected via the claude.ai Project's custom
  instructions so they are guaranteed-seen at session start.

Enforcement principle: with Desktop Commander a session can read anything, so
nothing is fenced by hiding. Instead the correct answer is made *cheaper to
reach than rederivation*, staleness is made *detectable* (status fields,
in-place supersession), and illegitimate moves (silent pruning, undeclared
imports) are made *protocol violations with visible legal alternatives*.

## 3. Target layout

```
Cella-Framework/
├── STATE/                      # THE CANON — small, current, schema-bound
│   ├── CURRENT.md              # entry point: one screen — status, active work, pointers
│   ├── RESULTS.md              # ledger of load-bearing results (R-xxx)
│   ├── CONSTRAINTS.md          # the constraint register (C-xxx) — the ONLY place rules live
│   ├── DEFINITIONS.md          # canonical formulas & notation (D-xxx)
│   ├── GAPS.md                 # open gaps (G-xxx) — cumulative gap work
│   └── sessions/               # dated append-only session logs (narrative lives here)
├── engine/                     # THE PROGRAM
│   ├── src/cella/              # the package (moved intact from /src)
│   ├── tests/                  # gate suite (moved intact from /tests)
│   ├── tools/                  # pathfinder_m2, wreath_engine (moved intact from /tools)
│   └── pyproject.toml          # new: names the package; PYTHONPATH stays primary
├── research/                   # THE NOTEBOOK — historical by default
│   ├── campaigns/              # moved from /campaigns
│   ├── verification/           # moved from /verification
│   ├── benchmarks/             # moved from /benchmarks
│   ├── reports/                # moved from /reports
│   ├── paper/                  # moved from /paper
│   └── derivations/            # new: derivation records (see §7)
├── docs/                       # GOVERNANCE — non-normative unless canon points here
│   ├── architecture/           # CELLA_ARCHITECTURE, PATHFINDER_KERNEL + deltas
│   ├── ADMISSIONS.md           # the admission ledger (still live, still binding
│   │                           #   via C-xxx entry that points to it)
│   ├── ROADMAP.md, CERTIFICATE_SCHEMA.md, POSITIONING.md
│   └── superpowers/            # specs & plans (this doc)
├── archive/                    # SEDIMENT — kept, tracked, explicitly non-normative
│   ├── handoffs/               # BOOT.md, CELLA_SESSION_HANDOFF.md, HANDOFF_2026-07-09.md
│   ├── Reference_Material/     # moved intact (already "claims, not evidence")
│   └── packages/               # .zip artifacts
├── README.md                   # rewritten: what this is + "start at STATE/CURRENT.md"
├── .mcp.json                   # paths updated (§8)
└── .gitignore                  # updated (§8)
```

Region epistemic status, stated in README and Project instructions:

| Region      | Status                                                        |
|-------------|---------------------------------------------------------------|
| `STATE/`    | Authoritative. If it disagrees with anything else, STATE wins. |
| `engine/`   | The program. Behavior is defined by code + gate tests.        |
| `research/` | Historical record. Load-bearing only where RESULTS.md points. |
| `docs/`     | Governance & design context. Non-normative prose.             |
| `archive/`  | Sediment. Never authoritative, never deleted.                 |

## 4. The canon: STATE/ file schemas

Schemas are the anti-slogan mechanism: there is no field where rhetoric can
live. All ids (`R-`, `C-`, `D-`, `G-`) are stable and never reused.

### 4.1 CURRENT.md — the entry point

One screen maximum. Sections: **Status** (layer/gate summary, one line each),
**Active work** (current campaign/lead, 3 lines max), **Open questions**
(pointers to G-xxx), **Read next** (pointers only). Regenerated at every close
ritual; anything that stops being current is deleted from it, not annotated.

### 4.2 RESULTS.md — the results ledger

```markdown
## R-017 lead7.pole-orders.n3
claim:       <one precise declarative sentence, no adjectives>
status:      current | superseded-by R-023 | refuted (see sessions/2026-07-02.md)
scope:       n=3, DBP metric. Not established for n>3.
certificate: research/verification/lead7_test5_pole_orders_n3.py  (byte-stable ×2)
depends-on:  R-012, D-004
```

Supersession is an **in-place edit** to the old entry's `status` field plus a
new entry — never a new document beside an old one. A result with no
certificate pointer cannot have `status: current`.

### 4.3 CONSTRAINTS.md — the constraint register

Standing rule zero, stated at the top of the file and in Project instructions:
**"If it is not in this register, it is not a constraint."**

```markdown
## C-003 exact-arithmetic-boundary
rule:        Cell values entering the residue accounting layer must be exact
             (ℚ or ℚ(√q)); float input at cell construction → typed refusal.
scope:       engine/src/cella — cell construction and certificate-bearing paths.
not-scope:   research scouting, plotting, numeric hypothesis testing, external
             tool output. Floats are fine there; exactify at the boundary.
why:         certificates must be byte-stable; exactness is the product.
displaced-by: an admitted exact float-embedding, or a certified interval layer.
```

`scope`, `not-scope`, and `displaced-by` are **mandatory**. The three standing
rules from README (standalone/zero-import, admission rule, re-verification
rule) become C-001..C-00x entries; ADMISSIONS.md remains the admission
*ledger*, referenced by the constraint that requires it.

### 4.4 DEFINITIONS.md — canonical objects

```markdown
## D-004 dbp-metric
object:      <the formula / definition, exactly as canonical>
domain:      <where it is defined>
source:      derived research/derivations/2026-07-08-dbp.md | admitted ADMISSIONS §…
used-by:     R-012, R-017
```

The anti-rederivation file: before deriving any quantity, a session checks here
first.

### 4.5 GAPS.md — the gap ledger

```markdown
## G-004 n4-pole-order-formula
gap:         <precise statement of what is missing>
blocks:      D-004, R-012, R-017          # corpus objects believed relevant
attempted:   sessions/2026-07-10.md (via R-012 route — dead-ends at <obstruction>)
known-echo:  resembles classical <X> — declared, quarantined, not the scaffold
status:      open | derived → R-xxx | admitted-import → ADMISSIONS §…
```

### 4.6 sessions/ — session logs

`sessions/YYYY-MM-DD[-slug].md`, append-only, free-form narrative. The **only**
sanctioned home for narrative in STATE/. Each log ends with a delta block:
ids created/edited this session, one line each.

## 5. Canon style law

Enforced at every close ritual; violations are defects to fix on sight:

1. Every universal ("never", "all", "refused", "forbidden") must sit inside a
   constraint entry with `scope` and `not-scope` filled. A bare slogan anywhere
   in STATE/ is a defect.
2. `why` fields are one line of mechanism, not persuasion. Vision/positioning
   prose lives in `docs/`, under a literal `**non-normative**` header marker.
3. Canon points at certificates and derivations; it never paraphrases them
   persuasively.
4. CURRENT.md is pruned, not appended: stale content is removed, and history
   lives in sessions/ and git.

## 6. Session protocol

### 6.1 Boot ritual (guaranteed via Project custom instructions)

1. Read `STATE/CURRENT.md` before anything else.
2. Any mathematical object used must be looked up in DEFINITIONS.md /
   RESULTS.md first. Rederiving something the ledger already holds is a
   protocol violation; so is using a version that contradicts the ledger.
3. Everything outside STATE/ is historical context unless STATE points to it.

### 6.2 Openness protocol

> Constraints exist only in `STATE/CONSTRAINTS.md`. Prose anywhere else —
> old architecture docs, reports, README history — is context, never
> instruction. Before discarding any approach because of a constraint: cite
> the constraint id and check its `scope`. Out of scope → proceed. In scope →
> still present the approach, as a displacement candidate against
> `displaced-by`. Silently narrowing the solution space is a protocol
> violation; visible, cited pruning is the only legal kind.

### 6.3 Close ritual ("wrap up")

1. Update RESULTS/CONSTRAINTS/DEFINITIONS/GAPS: new entries, in-place
   supersessions.
2. **Laundering audit:** for each new result — does every derivation step cite
   corpus parents, and were all external echoes declared? Any "no" downgrades
   the result to a gap entry.
3. **Style-law sweep** over touched canon files (§5).
4. Regenerate CURRENT.md.
5. Write `STATE/sessions/<date>.md` with the delta block.
6. `git add -A && git commit` with a summary message.

### 6.4 Project custom instructions (paste into the claude.ai Project)

The full text lives at `docs/PROJECT_INSTRUCTIONS.md` (created during
migration) so it is versioned; the claude.ai Project instructions field holds a
copy. Contents: the boot ritual, openness protocol, derivation protocol (§7),
close ritual trigger ("when the user says wrap up…"), and the region status
table from §3.

## 7. Derivation-first protocol

The project is a first-principles experiment: gaps are closed by derivation
from corpus building blocks, not by importing classical solutions — including
the laundered form where a classical design is recognized and then rebuilt
from corpus blocks to disguise the import.

Honest physics: an LLM cannot un-know classical mathematics. The protocol
therefore controls which knowledge is **load-bearing**, not which knowledge
exists. The audit question is never "did the model know the classical answer?"
but "does each step follow from its cited parents?"

1. **Affordance survey before candidates.** On any gap: enumerate the relevant
   corpus blocks (D-xxx, R-xxx) and the moves they afford *before* proposing
   any candidate. The survey is written into the G-xxx entry. Candidates must
   trace back to it. (A back-fitted derivation starts from a target and
   manufactures justification; forcing the survey first makes that structurally
   awkward, not merely forbidden.)
2. **The declaration rule.** If a gap or emerging candidate resembles a known
   external design, say so immediately and by name → recorded in `known-echo`,
   quarantined as a comparison object. Hidden resemblance is the offense;
   declared resemblance is data. Convergence stays legal: honestly arriving at
   something classical via licensed steps is a finding, not a violation.
3. **Dead-ends escalate, never smuggle.** If corpus blocks provably cannot
   reach the gap, record the obstruction in the G-xxx entry; the external
   solution may then be proposed only through the front door — an
   ADMISSIONS.md case.

**Derivation records** live in `research/derivations/<date>-<slug>.md`: the
affordance survey, then the derivation with every step citing the ids that
license it (algebra, an admitted lemma, a certified result). A result enters
RESULTS.md only with a derivation record (or certificate) pointer.

## 8. Migration plan

Ordered so the repo is never broken between phases. All moves via `git mv`.

**Phase 1 — program.** Create `engine/`; `git mv src tests tools engine/`.
The test suite's `sys.path.insert(0, …parent.parent / "src")` survives intact
(engine/tests/../src = engine/src) — no test edits required. Update
`.mcp.json`: `PYTHONPATH: engine/src`; wreath-engine `--directory
engine/tools/wreath_engine`. Add minimal `engine/pyproject.toml` (name,
version, src-layout package dir); PYTHONPATH remains the primary run mechanism
(works for Desktop Commander sessions without a venv).
**Verify:** full gate suite runs green from `engine/tests/`; `python3 -m
cella.mcp_server --help` (or equivalent smoke) works with the new PYTHONPATH.

**Phase 2 — research.** Create `research/`; `git mv campaigns verification
benchmarks reports paper research/`; create `research/derivations/` and move
root `legendre_native.py` into it (fix its sys.path line — the one code edit
in the migration). Grep for hardcoded `campaigns/`, `verification/`, `benchmarks/`, `reports/`
paths in engine + tests and fix hits.
**Verify:** gate suite still green; spot-run one verification script.

**Phase 3 — docs & archive.** Create `archive/{handoffs,packages}` and
`docs/architecture/`. Move: architecture docs + deltas → `docs/architecture/`;
ADMISSIONS, ROADMAP, CERTIFICATE_SCHEMA, POSITIONING → `docs/`; BOOT.md, both
handoff files → `archive/handoffs/`; Reference_Material →
`archive/Reference_Material/` (stays tracked; .gitignore paths updated); zips →
`archive/packages/`; `docs/m2_out_2026-07-10` + `docs/files` + publication
package → `research/` or `archive/packages/` by content (outputs → research,
frozen artifacts → archive). Untrack `tmp/`; add `tmp/` to .gitignore.

**Phase 4 — canon extraction.** Create `STATE/` and populate by mining, in
order: README (three standing rules → C-001..), LEADS.md, LEVER_AUDIT.md,
E_ATOM_DERIVATION.md, the handoffs, ROADMAP status claims. Facts → R/C/D/G
entries in schema form; each mined doc gets a header line "superseded by
STATE/ (2026-07-13) — non-normative" and moves to `archive/` (LEADS,
LEVER_AUDIT, E_ATOM_DERIVATION included, after extraction; the E-atom
derivation content becomes the first `research/derivations/` record alongside
`legendre_native.py`). Rewrite README to ~1 screen pointing at STATE/CURRENT.md.
This phase is interactive: extraction of *mathematical* claims into R/D entries
is proposed by Claude and ratified by the user before entries gain
`status: current`.

**Phase 5 — protocol.** Write `docs/PROJECT_INSTRUCTIONS.md`; user pastes into
the claude.ai Project. First real R&D session exercises boot + close rituals;
defects found feed back into the instruction text.

**Verification (whole migration):** gate suite green; both MCP servers start;
`git ls-files` shows no path outside the five top-level regions +
README/.mcp.json/.gitignore/.github/.claude; STATE/ files pass the style law
(§5) by inspection.

## 9. Future work (explicitly out of scope now)

- **MCP read-only state layer**: `current_state()`, `lookup_result(id)`,
  `lookup_constraint(id)` as thin views over STATE/ files — only after the
  ledger format has survived several real sessions. Write-path tools
  (`register_result`) only if the close ritual proves unreliable.
- Mechanical style-law linter (a small script the close ritual can run).
- CI check that every `status: current` result has a resolvable certificate
  path.

## 10. Success criteria

1. A fresh claude.ai session, given only the Project instructions, reaches the
   current status of any named result in ≤2 file reads (CURRENT → RESULTS).
2. No session rederives a ledgered result or uses a superseded one without the
   contradiction being visible (ledger id cited).
3. An approach touching a constraint's trigger topic but outside its `scope`
   is pursued, not pruned — verified by the "float" litmus: a research-side
   numeric scouting proposal must not be discarded on C-003 grounds.
4. Gap work resumes from G-xxx entries across sessions instead of restarting.
5. Every result entering RESULTS.md after migration has a derivation record or
   certificate with fully-cited steps; external echoes appear in `known-echo`
   fields, not in scaffolding.
