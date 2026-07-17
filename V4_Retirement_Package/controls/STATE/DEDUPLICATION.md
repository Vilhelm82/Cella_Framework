# Exact deduplication summary

Comparison target: `/home/wlloyd/Cella Framework`  
Detailed manifest: `STATE/DEDUPLICATION.json`

## Applied result

| Class | Files removed from Lloyd | Bytes removed |
|---|---:|---:|
| Exact copies already present in Cella | 85 | 826,256 |
| Additional exact duplicates within Lloyd | 926 | 51,650,370 |
| **Total** | **1,011** | **52,476,626** |

Each removed file was non-empty and matched its retained counterpart by byte size and
SHA-256 immediately before deletion. The manifest records the removed Lloyd path, its
hash, and either the canonical Cella path or the retained Lloyd path.

## Retention policy

- Cella was read-only: **0 Cella files modified or removed**.
- For internal Lloyd duplicates, report/derivation/campaign sources outranked attic,
  superseded, package, and legacy-runtime copies.
- `STATE/`, repository entry points, regional README files, and inventory tools were
  protected from removal.
- Empty files were excluded because they carry structure rather than duplicative
  content.

## Cella internal mirrors

Cella contains 43 non-empty exact-duplicate groups representing 1,045,073 potentially
reclaimable bytes. They were deliberately retained because the largest groups are
self-contained publication-package copies, campaign-local verifiers, or active/archive
provenance pairs. Removing those paths would trade a trivial amount of storage for
broken release and verification boundaries—a poor bargain, even by the standards of
aggressive spring cleaning.
