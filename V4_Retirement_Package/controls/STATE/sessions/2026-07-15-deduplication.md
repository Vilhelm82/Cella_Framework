# Exact deduplication — 2026-07-15

Both repositories were hashed and compared. Cella was treated as the active read-only
successor, while Lloyd V4 was the only deletion target.

The pass removed 85 Lloyd files already present byte-for-byte in Cella and 926
additional redundant Lloyd copies after retaining one preferred source for each hash.
Every deletion was recorded in `STATE/DEDUPLICATION.json` before unlinking.

## Delta

- created: `STATE/DEDUPLICATION.json`, `STATE/DEDUPLICATION.md`
- created: `docs/tools/deduplicate_against_successor.py`
- removed: 1,011 exact duplicate files from Lloyd V4 (52,476,626 bytes)
- modified in Cella Framework: none
