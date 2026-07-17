# Evidence Store

This is Cella's immutable, content-addressed evidence layer.

- Address: `SHA-256`
- Object layout: `objects/sha256/<first-two-hex>/<full-digest>`
- Unique objects: **1727**
- Recorded origins: **3017**
- Storage: independent Btrfs reflinks where supported; ordinary copies otherwise

An object records bytes and provenance. It does **not** promote a historical result, campaign conclusion, certificate, or report into current Cella authority. Current claims remain governed by `STATE/`, `BOOT.md`, `ADMISSIONS.md`, and live verification.

Human-readable report paths live in `../Reports_Library` and resolve here through relative symlinks. See `_catalogue/OBJECT_LEDGER.json` for machine-readable origins and bindings.
