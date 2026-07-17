"""Task 036 serialization round-trip for new companion fields."""

from __future__ import annotations

import json

from lloyd_v4.core.serialization import to_json_safe
from lloyd_v4.observers import directional_alpha_probe


F_VALUES = [1e-4, 1e-3, 1e-2]


def test_serialization_roundtrip_none_and_populated() -> None:
    def sq(f): return f * f

    # None case (default)
    r_none = directional_alpha_probe(sq, F_VALUES, probe_id="ser_none", function_label="sq")
    payload_none = to_json_safe(r_none)
    assert "companion_sweep_signature_observation" in payload_none["value"]
    assert payload_none["value"]["companion_sweep_signature_observation"] is None
    assert payload_none["value"]["companion_sweep_signature_status"] is None

    # Populated
    r_pop = directional_alpha_probe(sq, F_VALUES, probe_id="ser_pop", function_label="sq", companion_sweep_signature=True)
    payload_pop = to_json_safe(r_pop)
    assert payload_pop["value"]["companion_sweep_signature_observation"] is not None
    assert payload_pop["value"]["companion_sweep_signature_status"] in ("sweep_signature_clean", "sweep_signature_cancellation_dominated", None)

    # JSON round-trip does not explode
    json.dumps(payload_pop, allow_nan=False)
    json.dumps(payload_none, allow_nan=False)
