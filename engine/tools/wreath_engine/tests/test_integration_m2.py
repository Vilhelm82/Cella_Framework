"""Integration tests against a real Macaulay2 (marked m2)."""

import json
import shutil
import time
from pathlib import Path

import pytest

from wreath_engine import jobs, m2run, pipeline, spec

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

pytestmark = pytest.mark.m2

needs_m2 = pytest.mark.skipif(shutil.which("M2") is None,
                              reason="Macaulay2 not installed")


@pytest.fixture()
def runs_root(tmp_path):
    return tmp_path / "runs"


@needs_m2
def test_toy_verify_certifies(runs_root):
    ps = spec.load(EXAMPLES / "toy_quadratic.json")
    env = pipeline.verify_valuation_matrix(ps, runs_root, timeout=300)
    assert env["status"] == "certified"
    assert env["closure_group"] == "C_2^1 wr S2"
    assert env["closure_order"] == 8
    assert all(g.get("pass") is not False for g in env["gates"])
    # certificate pair exists and is rerunnable content
    script, output = map(Path, env["certificate_files"])
    assert script.exists() and output.exists()
    assert "prime_upstairs" in output.read_text()


@needs_m2
def test_toy_wrong_parity_row_refuted(runs_root):
    doc = json.loads((EXAMPLES / "toy_quadratic.json").read_text())
    doc["divisors"][0]["claimed_parity_row"] = [0]  # wrong: order is 1
    ps = spec.validate(doc)
    env = pipeline.verify_valuation_matrix(ps, runs_root, timeout=300)
    assert env["status"] == "refuted"
    failed = {g["gate"] for g in env["failed_gates"]}
    assert "on_sheet_parity" in failed


@needs_m2
def test_static_horizon_certifies_r9(runs_root):
    """The engine must reproduce the audited R9 static-crown theorem."""
    ps = spec.load(EXAMPLES / "horizon_static.json")
    env = pipeline.verify_valuation_matrix(ps, runs_root, timeout=1200)
    assert env["status"] == "certified"
    assert env["kummer_rank"] == 10
    assert env["closure_group"] == "C_2^2 wr S5"
    assert env["closure_order"] == 122880
    # wreath lift consumes the persisted certificate
    lift = pipeline.compute_wreath_lift(ps, runs_root)
    assert lift["status"] == "certified"
    assert lift["verified_by_run"] == env["run_id"]
    # inertia table certified and correctly signed
    inertia = pipeline.classify_inertia(ps, runs_root)
    assert inertia["status"] == "certified"
    odd = next(r for r in inertia["inertia_table"] if r["divisor"] == "odd_contact")
    assert odd["sign_vector"] == [1, 1]
    assert odd["kummer_inertia_order"] == 2


@needs_m2
def test_toy_realize_poset(runs_root):
    ps = spec.load(EXAMPLES / "toy_quadratic.json")
    env = pipeline.realize_branch_poset(ps, runs_root,
                                        include_decompositions=True, timeout=300)
    assert env["status"] == "certified"
    walls = env["contact_walls"]
    assert walls and all(w["pass"] for w in walls)
    prime_facts = [d for d in env["decompositions"]
                   if d.get("stage") == "channel_primary_decomp"]
    assert prime_facts and prime_facts[0]["is_prime_ideal"] is True


@needs_m2
def test_explore_parity_probe(runs_root):
    ps = spec.load(EXAMPLES / "toy_quadratic.json")
    env = pipeline.suggest_parity_rows(ps, ["x-1"], runs_root, timeout=300)
    assert env["status"] == "exploratory"
    assert env["components"][0]["parity_row"] == [1]


@needs_m2
def test_async_job_roundtrip(runs_root):
    ps = spec.load(EXAMPLES / "toy_quadratic.json")
    start = jobs.start_job(ps, "verify", runs_root, timeout=300)
    job_id = start["job_id"]
    for _ in range(120):
        st = jobs.job_status(job_id, runs_root)
        if st["state"] != "running":
            break
        time.sleep(1)
    assert st["state"] == "done"
    env = jobs.job_result(job_id, runs_root)
    assert env["status"] == "certified"
    assert env["closure_order"] == 8


def test_parse_results_roundtrip():
    text = (f"noise\n{m2run.FENCE_BEGIN}\n"
            '{"kind":"gate","pass":true}\n'
            f"{m2run.FENCE_END}\nmore noise\n")
    assert m2run.parse_results(text) == [{"kind": "gate", "pass": True}]
