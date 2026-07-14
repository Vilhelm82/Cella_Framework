#!/usr/bin/env python3
"""Direct CCE-5--8 mathematics replay (historical filename retained).

This file deliberately contains no release-bundle or hash-certificate checks.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation.cce5 import (  # noqa: E402
    compact_picard_lefschetz_matrix, corridor_transport_matrix,
    relative_picard_lefschetz_matrix, verify_braid_calibration,
    verify_dbp_connection_identity, verify_dbp_family_identity,
)
from cella.continuation.cce7 import norm_quintic  # noqa: E402
from cella.continuation.cce8 import (  # noqa: E402
    FiniteRoleJet, finite_role_group_laws, finite_tower_naturality,
)

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


check("CCE-5 DBP family identity", verify_dbp_family_identity())
check("CCE-5 K/E/Pi chain rule", verify_dbp_connection_identity())
check("CCE-5 braid calibration", verify_braid_calibration())
check("CCE-5 upper compact PL", compact_picard_lefschetz_matrix("upper") == ((1, 0), (2, 1)))
check("CCE-5 lower compact PL", compact_picard_lefschetz_matrix("lower") == ((1, 0), (-2, 1)))
check("CCE-5 relative rank", len(relative_picard_lefschetz_matrix("upper")) == 4)
check("CCE-5 corridor cancellation", corridor_transport_matrix("Uu") == tuple(tuple(int(i == j) for j in range(4)) for i in range(4)))

package_path = ROOT / "research/campaigns/CELLA_CONTINUATION_ENGINE/07_cce6_surface/CCE_6_COMPLETE_PACKAGE_v1.0/DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_CERTIFICATE_v1.0.json"
package = json.loads(package_path.read_text(encoding="utf-8"))
check("CCE-6 proof witness verdict", package["verdict"] == "PROVED")
check("CCE-6 proof witness scope", package["claim_scope"] == "two_exact_dbp_corridors_on_native_surface_image")
check("CCE-6 both corridors", set(package["nested_corridor_certificates"]) == {"upper", "lower"})

quintic = norm_quintic(Fraction(9, 8))
check("CCE-7 norm polynomial degree", len(quintic) == 6)
check("CCE-7 norm polynomial nonzero", any(quintic))

jet = FiniteRoleJet(4, ((1, 0, Fraction(2)), (0, 1, Fraction(1)), (2, 0, Fraction(3, 2)), (1, 1, Fraction(-1, 3)), (0, 2, Fraction(2, 5)), (3, 0, Fraction(1, 7))))
check("CCE-8 exact S3 laws", all(valid for _law, valid in finite_role_group_laws(jet)))
check("CCE-8 finite tower", finite_tower_naturality(jet, 2, "st").target_order == 2)

print(f"CCE-5--8 direct mathematical replay: {passed} assertions passed")
