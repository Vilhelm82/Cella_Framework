import json
from pathlib import Path

import pytest

from wreath_engine import spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def load_example(name):
    with open(EXAMPLES / name) as f:
        return json.load(f)


def test_static_example_validates():
    ps = spec.validate(load_example("horizon_static.json"))
    assert ps.s == 2 and ps.d == 5
    assert ps.base_cover.group.name == "S5"
    assert [list(d.claimed_parity_row) for d in ps.divisors] == [[1, 0], [1, 1]]
    assert ps.content_hash()


def test_rotating_example_validates():
    ps = spec.validate(load_example("horizon_rotating.json"))
    assert ps.s == 3 and ps.d == 5
    assert ps.divisors[2].gens == ("delta",)


def test_channel_shadowing_ring_variable_rejected():
    doc = load_example("horizon_static.json")
    doc["channels"][0]["radicand"] = "u+1"  # channel named u must be exactly u
    with pytest.raises(spec.SpecError, match="/channels/0/radicand"):
        spec.validate(doc)


def test_unknown_identifier_rejected():
    doc = load_example("horizon_static.json")
    doc["divisors"][0]["gens"] = ["zeta-1"]
    with pytest.raises(spec.SpecError, match="unknown identifier 'zeta'"):
        spec.validate(doc)


def test_parity_row_length_enforced():
    doc = load_example("horizon_static.json")
    doc["divisors"][0]["claimed_parity_row"] = [1, 0, 0]
    with pytest.raises(spec.SpecError, match="claimed_parity_row"):
        spec.validate(doc)


def test_group_order_consistency():
    doc = load_example("horizon_static.json")
    doc["base_cover"]["group"]["order"] = 121  # does not divide 5!
    with pytest.raises(spec.SpecError, match="does not divide"):
        spec.validate(doc)


def test_channel_forward_reference_rejected():
    doc = load_example("horizon_rotating.json")
    # delta refers to gamma; swap them so the reference is forward
    doc["channels"][1], doc["channels"][2] = doc["channels"][2], doc["channels"][1]
    with pytest.raises(spec.SpecError, match="unknown identifier 'gamma'"):
        spec.validate(doc)


def test_slice_values_must_be_integers():
    doc = load_example("horizon_static.json")
    doc["slices"][0]["assignments"]["N1"] = 4.5
    with pytest.raises(spec.SpecError, match="/slices/0/assignments/N1"):
        spec.validate(doc)
