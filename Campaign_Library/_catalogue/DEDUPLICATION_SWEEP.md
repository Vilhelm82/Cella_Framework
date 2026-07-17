# Campaign deduplication sweep

Completed: `2026-07-15T13:07:38+10:00`

## Result

- Campaign artifacts examined: **952** across **39** campaigns.
- Unique campaign SHA-256 digests: **952**.
- Within-campaign exact duplicates: **0**.
- Cross-campaign exact duplicates: **0**.
- Exact overlaps with `Papers_Library`: **176**, already deduplicated using relative symlinks.
- Campaign-only unique artifacts: **776**.
- Safe source deletions: **0**.

No similarity-based or filename-based deletion was permitted. Distinct bytes remain
distinct artifacts even where names or subjects resemble one another.

## Excluded source candidates

Only two campaign origins are untracked or ignored: the Lloyd `pi_rotation` Stage-0
predeclaration and its Python harness. Neither is isolated:

- `Lloyd_Engine_V4/STATE/ARTIFACTS.json` records both exact paths.
- `PI_STAGE0_PREDECL.md` names `pi_stage0.py` as a deliverable.
- `pi_stage0.py` names the predeclaration and supplies the campaign execution logic.

They remain in place as a coupled campaign package. Deleting either would create a path
and provenance consequence, so the sweep correctly performed no source deletion.
