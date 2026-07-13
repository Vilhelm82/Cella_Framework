# RESULTS — ledger of load-bearing results

Schema per entry: `## R-NNN <slug>` then `claim / status / scope / certificate /
depends-on`. The `claim` is one precise declarative sentence, no adjectives.
Supersession edits the old entry's `status` field **in place** (never a new
document beside an old one). A result with no certificate pointer may not be
`status: current`.

> **POPULATION PENDING.** Load-bearing results are migrated here from
> docs/ROADMAP.md (the certified gate record), research/reports/, and
> research/verification/ **interactively — each ratified by the maintainer**
> before it gains `status: current` (per the re-verification rule, C-003:
> documentary status is a claim, not evidence). Until an entry exists here,
> absence means "not yet migrated", NOT "no such result". For certified gate
> status right now, read `docs/ROADMAP.md`.

<!-- template — copy, do not delete:
## R-001 <slug>
claim:       <one precise declarative sentence, no adjectives>
status:      current                 # | superseded-by R-NNN | refuted (see sessions/<date>.md)
scope:       <where it holds; where it explicitly does not>
certificate: research/verification/<file>.py  (byte-stable ×2, <hash>)
depends-on:  <R-/D- ids>
-->
