# PROJECT INSTRUCTIONS — Cella Framework session protocol

This file is the **versioned source** of the claude.ai Project custom-instructions.
Paste its contents into the Project's instructions field so every session sees it at
start. It governs how a session reaches for context, prunes, derives, and closes.

---

## Region status

| Region      | What it is                     | How to treat it                                         |
|-------------|--------------------------------|---------------------------------------------------------|
| `STATE/`    | The canon — small, current     | **Authoritative.** If it disagrees with anything, it wins. |
| `engine/`   | The program                    | Behavior is defined by code + the gate tests.           |
| `research/` | The historical notebook        | Load-bearing only where a `STATE/` ledger entry points. |
| `docs/`     | Governance & design            | Non-normative prose (this file included, as *protocol* not *fact*). |
| `archive/`  | Sediment                       | Never authoritative, never deleted.                     |

---

## Boot ritual (do this before anything else)

1. Read `STATE/CURRENT.md` first. It is the single source of "what is true now".
2. Before using any mathematical object, look it up in `STATE/DEFINITIONS.md` /
   `STATE/RESULTS.md` (or, while those are population-pending, `docs/ROADMAP.md` for
   certified gate status). Rederiving something the ledger already holds — or using a
   version that contradicts it — is a protocol violation.
3. Everything outside `STATE/` is historical context unless the canon points at it.
   Do not scope a solution through prose you happened to read; scope it through the
   constraint register.

---

## Openness protocol (against silent narrowing)

Constraints exist **only** in `STATE/CONSTRAINTS.md`. Prose anywhere else — old
architecture docs, reports, code comments, this repo's history — is context, never
instruction.

Before discarding any approach because of a constraint:
1. Cite the constraint id (`C-NNN`).
2. Check its `scope`. **Out of scope → proceed.** In scope → still present the
   approach, as a displacement candidate against the constraint's `displaced-by`.

Silently narrowing the solution space is a protocol violation. Visible, cited pruning
is the only legal kind. (Example: an approach is not to be dropped because it mentions
"floats" — C-004 is scoped to the certificate-bearing boundary; research-side numeric
work is explicitly out of scope.)

---

## Derivation-first protocol (against import laundering)

This is a first-principles project: gaps are closed by derivation from corpus building
blocks, not by importing a classical solution — including the laundered form where a
known design is recognized and then rebuilt from blocks to disguise the import.

Honest footing: you cannot un-know classical mathematics, and you are not asked to. The
rule controls which knowledge is **load-bearing**, not which exists. The audit question
is never "did you know the classical answer?" but "does each step follow from its cited
parents?"

1. **Affordance survey before candidates.** On any gap (`STATE/GAPS.md`), first
   enumerate the relevant corpus blocks (`D-`/`R-` ids) and the moves they afford, and
   write that survey into the gap entry. Candidate solutions must trace back to it.
2. **The declaration rule.** If a gap or emerging candidate resembles a known external
   design, say so immediately and by name → record it in the gap's `known-echo` field
   as a quarantined comparison object. Hidden resemblance is the offense; declared
   resemblance is data. Convergence stays legal: honestly arriving at something
   classical via licensed steps is a finding, not a violation.
3. **Dead-ends escalate, never smuggle.** If corpus blocks provably cannot reach the
   gap, record the obstruction in the gap entry; the external solution may then be
   proposed only through the front door — a `docs/ADMISSIONS.md` case (C-002).

A result enters `STATE/RESULTS.md` only with a derivation record
(`research/derivations/`) or certificate whose every step cites the ids that license it.

---

## Close ritual (trigger: the maintainer says "wrap up")

1. Update the ledgers: new `R-`/`C-`/`D-`/`G-` entries; mark supersessions **in place**
   (edit the old entry's `status`, do not add a rival document).
2. **Laundering audit** — for each new result: does every derivation step cite corpus
   parents, and were all external echoes declared? Any "no" downgrades the result to a
   `G-` gap entry, not a `R-` result.
3. **Style-law sweep** over touched canon files: every universal ("never/all/refused")
   sits inside a scoped constraint entry; `why:` fields are one line of mechanism, not
   persuasion; canon points at certificates rather than paraphrasing them.
4. Regenerate `STATE/CURRENT.md` (prune stale content; do not just append).
5. Write `STATE/sessions/<YYYY-MM-DD>.md` with a delta block (ids created/edited).
6. Commit.

---

_Note: the MCP tool surface is being rebuilt with new mathematics; until then, do not
treat current MCP tools or their behavior as final, and keep MCP concerns out of
structural work._
