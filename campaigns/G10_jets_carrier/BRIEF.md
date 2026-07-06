# G1.0 CAMPAIGN — jets and the carrier (Layer 1 opens)

**Status:** CLOSED ALL-PASS 2026-07-06 · `tests/gate_10.py` 42/42 ×2 (`4af1adca`)
against PREREG `45947aa47e22f736`; kills silent; mutants bite; Layer-0 suite green ×2
after the declared gate_04 assertion update (stdout pin unchanged) ·
governed by the three standing rules and the DESIGN FREEZE (ROADMAP). This is an engine gate with a certification battery, not a
discovery campaign: the mathematics is already certified in-repo (RC-1/RC-2/RC-4);
what is certified here is the implementation and its refusal boundaries.

## Campaign goal

The order-2 jet as a first-class engine object and carrier extraction O from H as a
certified, general-n, refusal-typed API — the geometric substrate's ground floor,
built on Layer 0 cells/certificates only.

## Target claim

For a codim-1 constraint block with exact jet (g, H), the engine emits the carrier

```
O_ij = H_ij - g_i*H_jj/(2*g_j) - g_j*H_ii/(2*g_i)     (i < j, lex order)
```

gauge-invariant through the API, with the gauge-normal form H_perp (zero diagonal,
off-diagonal O) canonical; every degenerate input a typed refusal; every certificate
stating its tier (local; codim-1; order 2; jets over Q certified — QSqrt entries flow
structurally but are uncertified at this gate).

## Design-freeze compliance (binding)

1. Constraint inputs typed as BLOCKS; codim-1 refuses len > 1 with `CODIM_UNSUPPORTED`
   (admitted A-009, before this first use).
2. Carrier O read from H directly, general-n formula (RC-2); no n=3 anywhere in the
   extraction pathway.
3. Channel recovery is an n=3 cross-check ONLY (`RC-4` values); the cross-check
   function guards n == 3 as an API contract (ValueError — misuse, not a data
   condition; data conditions refuse).
4. Scoped certificate claims: tier stated in the certificate's `what`.
5. STOP-LINE respected: blocks of length > 1 produce a refusal and no computation.

## Stage 0 — re-verification (the inputs this gate leans on)

All three re-run clean this session, byte-stable ×2, shas matching pins:
RC-1 `4ad5a6eb` (re-pinned from `d370daae`, labels hardened, values unchanged) ·
RC-2 `b21992f3` · RC-4 `3d7ed1bf`.

## The battery — `tests/gate_10.py` against `PREREG.md` (frozen pre-build)

Pins and obligations are in PREREG.md; sha recorded below at freeze. Categories:
block typing and refusal paths; O pins at n = 3, 4, 5 (hand-derived, independently
verified pre-freeze); gauge-invariance sweep through the API; normal-form canonicality
including the Im(G_g) decomposition witness; purity wiring (R-motion leaves O fixed;
M-defect moves it; M-corrected reconstruction recovers truth's O); the labeled n=3
channel cross-check; certificates on value and refusal paths; float/NaN exclusion;
and three mutants that MUST FAIL (Goldman-flatten, dropped-term, label-swap).

## Kill conditions (armed)

- **K-1:** general-n O fails gauge invariance on any generic fixture at n = 4, 5 →
  RC-2's general-n note oversold; HALT, scope shrinks to the certified n, finding
  banked before any close.
- **K-2:** carrier path and n=3 channel cross-check disagree at the keystone →
  RC-2/RC-4 misread; HALT and triage.
- **K-3:** normal-form canonicality fails (gauge changes H_perp, or H − H_perp has no
  gauge preimage) → theorem scope error, not a code bug; HALT.

## Expected failure modes (how this gate could fool us)

Index-order bugs invisible at n=3 (why n=4,5 pins exist); a gauge sweep of only
symmetric/small vectors (rows include negative and fractional components); mutants too
weak to bite (each mutant targets a specific certified property: channel content,
gauge invariance, label identity); pins derived FROM the implementation (pins were
hand-derived and independently verified before any implementation code existed —
see PREREG).

## Stop conditions

Any kill fires → HALT, bank the finding, no close. No partial-credit close: the gate
closes 100% or stays open with the blocker named.

## Output ledger

`campaigns/G10_jets_carrier/` (this BRIEF, PREREG.md + frozen sha) ·
`src/cella/jet.py`, `src/cella/carrier.py` · vocabulary additions in
`src/cella/refusal.py` (A-009) · `tests/gate_10.py` (pin on close) ·
`tests/gate_04.py` count update + re-pin (declared in PREREG) · ROADMAP G1.0 close ·
BOOT current-state · A-008/A-009 obligation updates.

## PREREG freeze

PREREG.md sha256 (first 16 hex) at freeze, before any implementation code:
`45947aa47e22f736` — frozen 2026-07-06, committed ahead of all G1.0 implementation.
