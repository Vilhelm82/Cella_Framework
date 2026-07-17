# root-closure-atlas — surprise ledger (campaign-level; append-only; §1.4)

Anything anomalous lands here the moment it is seen; entries are never
edited or removed, only appended.

---

*(no entries — Stage-0 bench construction produced no anomalous signal;
three even-crossing bracket pins were caught by the pre-freeze wall-sign
check and corrected before any pin existed — recorded in the Stage-0
report as authoring corrections, not surprises)*

---

## Entry 1 — 2026-06-11, Stage-0 battery: oracle probe-tree ordering is session-unstable

- **What:** P0.1's first ×2 comparison failed on 46 I2 records — every
  difference confined to the `probe_tree.children` list ORDER inside the
  verbatim oracle payload; every value (closed_value, drift, status,
  candidates) cross-session byte-stable. The V3 server emits tree
  children in hash-dependent order.
- **Action:** declared instrument-transfer normalization (children lists
  sorted lexically at recording; nothing graded reads the tree); P0.1
  re-run from scratch ×2. The pre-flight stability test had sampled one
  multi_start call only — insufficient; recorded as a probe-coverage
  lesson.
- **Class:** oracle instrument quirk (atlas-relevant: an undeclared
  nondeterminism in the comparison instrument), not substrate.
