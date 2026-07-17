"""Task 036: layer manifest and cross-layer parent checks still pass after AlphaProbeObservation field addition."""

from __future__ import annotations

import pytest

# The heavy lifting is already done by the task010* and task035* manifest tests.
# We only need a smoke that importing the modified module does not break manifest collection.


def test_alpha_probe_observation_extension_does_not_break_import_or_basic_manifest() -> None:
    # AlphaProbe relocated primitives -> observers (GAP-009 / HR112 observers sub-layer)
    from lloyd_v4.observers import AlphaProbeObservation, directional_alpha_probe
    # If a machine-readable field list existed it would be asserted here; for now just presence.
    assert "companion_sweep_signature_observation" in str(AlphaProbeObservation.__dataclass_fields__)
    # Trigger a normal call so any __post_init__ or protocol side-effects are exercised under the collector
    r = directional_alpha_probe(lambda f: f * f, [1e-4, 1e-3], probe_id="manifest", function_label="sq")
    assert r is not None
