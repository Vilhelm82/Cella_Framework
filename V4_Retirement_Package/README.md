# Lloyd Engine V4 retirement package

This package replaces a loose-file retirement strategy with **44 deterministic package manifests**, readable control copies, and one verified non-Git cold-recovery snapshot.

- Source members: **2406**
- Manifest-packaged members: **2378**
- Individually readable controls: **28**
- Members already represented in the Evidence Store: **1409**
- Cold snapshot: `cold_recovery/Lloyd_Engine_V4_non_git_cold_recovery.tar.gz`
- Snapshot SHA-256: `59ba3325ad05d615a6d61c90b3e2177833287cade2e723398ed24d845d487290`

Package manifests do not duplicate their member payloads. They bind original V4 paths to SHA-256 identities, Evidence Store IDs where available, report IDs, path consequences, and certificate status. The cold snapshot is the single physical reconstruction fallback and preserves the exact non-Git V4 tree as built.

Nothing here promotes V4 results into current Cella authority. Consult `PACKAGE_LEDGER.json`, `ORIGIN_PATH_MAP.csv`, and `SHA256SUMS` before any source retirement.
