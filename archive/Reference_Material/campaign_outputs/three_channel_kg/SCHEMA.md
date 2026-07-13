# c001 · three_channel_kg — SCHEMA (FROZEN)

Record type: **`three_channel_kg_record_v1`**. Transcribed from the ratified merged committed spec
§3.3 / §3.5 / §6. Frozen — schema, role gate, and closure identities do not change without a
versioned manifest bump.

## Role gate (covenant #7)

A closure verdict requires a **ledger AND `role=probe`** — a verdict without an account is rejected
as the untraceable belief this project types against. The probe **never imports the referee**; the
referee truth path is computed on an independent code path.

## Per-row closure identities (exact ℚ, no tolerance — a near-miss is a FAIL)

Each evaluated row is graded by **all** of:

1. `got.(K_G, κ_c, κ_s, κ_int) == expected`
2. `got.K_G == Σ channels`  (`κ_c + κ_s + κ_int`)
3. `got.K_G == Path-B total`  (`−det(H_b)/q²`, √q-free)
4. `got.channels == Path-B′ channels`  (split shape-operator `det₂`, code-disjoint)
5. `det(H_b) == Δ_c + Δ_s + Δ_m`

## Referee separation (no check certifies itself — §3.3/§3.5)

- **Path A** — monomial channel read-off.
- **Path B** — independent *total* referee (`det(H_b)` from a generic determinant, not DBP channel
  formulas; √q-free).
- **Path B′** — independent *channel* referee (split shape-operator from `PHP` + trace identities;
  disjoint source).
- **Path C** — frozen external fixture oracle (exact fractions).

Any DBP-copied formula is hypothesis input until independently reduced.

## Preconditions (run-void on failure)

- **P-self-cert** — the oracle must be external to A/B/B′, or the run is void.
- **P-frame** — every channel fixture must carry its frame annotation, or it is rejected.

## Type gates

- **√q-leak** — a total/channel referee returning a radical/float instead of `Fraction` → hard fail.
- **tolerance-leak** — any injected mismatch that passes/warns instead of hard-failing → fail.
- **singular-lie** — `q=0` / cone-apex / `gᵢ=0` returning `0`/`NaN`/placeholder instead of typed
  `REFUSED` → fail (refuse-not-lie).

Bench code (`schema.py` enforcing this record type + role gate) is built by Dev/CLI to this freeze
and pinned in each stage prereg before that stage runs (Rule 1.9).
