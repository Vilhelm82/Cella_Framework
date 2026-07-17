# Inventory summary

Generated registry: `STATE/ARTIFACTS.json`  
Registry policy: every file under the five organized regions is hashed except the
registry itself and Python bytecode/cache directories.

## Regional inventory

| Region / family | Files | Content bytes | Intake meaning |
|---|---:|---:|---|
| `STATE/` | 11 | ~0.92 MiB | Staging metadata including the detailed deduplication manifest; the self-excluded registry is not counted |
| `engine/` | 480 | 2,614,177 | Legacy runtime, tests, and demos |
| `research/` | 1,396 | 138,447,724 | Candidate evidence and primary report-consolidation surface |
| `docs/` | 137 | 1,306,753 | Non-normative architecture and governance context |
| `archive/` | 369 | 12,099,197 | Historical, superseded, or packaged material remaining after exact deduplication |

The post-deduplication registry contains **2,393 artifacts**. The registry file itself is deliberately
excluded to avoid self-hashing.

## Artifact kinds

| Kind | Count |
|---|---:|
| Documents | 915 |
| Source code / scripts | 779 |
| Structured data | 541 |
| Other | 139 |
| Packages | 12 |
| Images | 5 |
| Configuration | 2 |

## Research breakdown

| Family | Files | Evaluation role |
|---|---:|---|
| `research/campaigns/` | 749 | Campaign-level claim and evidence extraction |
| `research/reports/` | 397 | Primary consolidation candidates |
| `research/verification/` | 244 | Fresh-run candidates or report-only computational provenance |
| `research/derivations/` | 1 | Intake note; exact derivation copies resolve into Cella through the deduplication manifest |
| `research/paper/` | 4 | Secondary claim sources and publication artifacts |

## Preservation check

Every unique Git blob present at the pre-reorganization Lloyd `HEAD` still exists in
at least one of the two repository working trees after deduplication (**0 missing
unique blobs across Lloyd + Cella**). This proves content preservation at the
cross-repository blob level; it does not certify runtime compatibility, semantic
correctness, or Cella admissibility.
