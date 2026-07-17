# Campaign Library terminology and labels

This library normalizes documentary organization only. It does not promote a campaign,
claim, theorem, result, or certificate into Cella canon. `STATE/` remains authoritative.

## Campaign identifiers

- `CMP-####` is a stable library identifier assigned to one canonical campaign slug.
- Original campaign names are aliases retained in the registry and artifact ledger.
- Campaign status is `NOT_ADJUDICATED`; filenames are not evidence of truth or completion.

## Filename grammar

`CMP-####__ROLE-<CONTROLLED_ROLE>__<normalized_original_title>.<extension>`

Campaign-only artifacts are byte-identical clones. When an identical SHA-256 already
exists in `Papers_Library`, the normalized campaign path is a relative symlink to that
paper artifact. The separate trees remain visible while the bytes are stored once.

## Controlled document roles

| Role | Meaning |
|---|---|
| `authority` | charter, authority source, scope lock, or baseline lock |
| `index` | README, index, or catalogue |
| `brief` | campaign/task/build brief or specification |
| `preregistration` | preregistration, predeclaration, or precommitment |
| `design` | plan, protocol, contract, template, or design |
| `prediction` | explicit hypothesis, conjecture, prediction, or stake |
| `method` | methodological or workflow document |
| `source` | executable campaign source |
| `test` | battery, test, mutant, or fixture |
| `record` | raw record, log, observation, factor, or timeline |
| `certificate` | verifier, pin, digest, or certificate |
| `visualization` | campaign plot or diagram |
| `report` | analysis, report, result, census, or gap ledger |
| `audit` | audit, review, correction, reconciliation, or adequacy matrix |
| `claim` | claim ledger, theorem, proof, lemma, or law |
| `closeout` | close, closeout, final report, verdict, or decision sheet |
| `handoff` | handoff, successor, or queued continuation |
| `manifest` | manifest, inventory, or layout |
| `schema` | schema or data contract |
| `reference` | citations, bibliography, or reference values |
| `archive` | packaged archive |
| `historical` | explicitly retired, superseded, old, or historical material |
| `other` | campaign material with no reliable controlled-role marker |

## Lifecycle folders

The numbered role folders encode documentary function, not chronology or claim status.
Stage/facet/CCE labels are normalized as a subordinate `phase_label`; unscoped material
uses `campaign_wide`.

## Campaign-to-paper lineage

An exact digest match to `Papers_Library` creates a mechanical lineage edge recorded in
`CAMPAIGN_PAPER_LINEAGE.json` and `.md`. This proves artifact identity and production
context; it does not by itself prove the mathematical claim inside the artifact.
