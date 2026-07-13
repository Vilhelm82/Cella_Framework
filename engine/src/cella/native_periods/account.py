"""Machine-checkable local identities for the two fixed binary64 DAGs."""

from __future__ import annotations

import hashlib
from fractions import Fraction

from .eft import division_defect, float_fraction, sqrt_defect, two_prod, two_sum


class AccountMachine:
    def __init__(self):
        self.nodes = []

    def add(self, a, b):
        s, e = two_sum(a, b)
        self.nodes.append(("two_sum", float_fraction(s), e,
                           float_fraction(a)+float_fraction(b)))
        return s

    def sub(self, a, b): return self.add(a, -b)

    def mul(self, a, b):
        p, e = two_prod(a, b)
        self.nodes.append(("two_prod", float_fraction(p), e,
                           float_fraction(a)*float_fraction(b)))
        return p

    def div(self, a, b):
        q, r = division_defect(a, b)
        self.nodes.append(("division", float_fraction(q), r,
                           float_fraction(a), float_fraction(b)))
        return q

    def sqrt(self, a):
        q, d = sqrt_defect(a)
        self.nodes.append(("sqrt", float_fraction(q), d, float_fraction(a)))
        return q

    def replay(self):
        for node in self.nodes:
            if node[0] in ("two_sum", "two_prod") and node[1]+node[2] != node[3]:
                return False
            if node[0] == "division" and node[3]-node[1]*node[4] != node[2]:
                return False
            if node[0] == "sqrt" and node[3]-node[1]*node[1] != node[2]:
                return False
        return True

    def digest(self):
        text = repr(self.nodes).encode()
        return hashlib.sha256(text).hexdigest()


def evaluate_fixed_dag_binary64(kernel_id: str, t: float):
    """Developer/account reading; the certifying value path is multi-limb."""
    a = AccountMachine()
    w = a.sub(1.0, t)
    t2, w2 = a.mul(t, t), a.mul(w, w)
    if kernel_id == "g_plus_v1":
        p = a.add(a.add(a.mul(t2, t2), a.mul(2.0, a.mul(t2, w2))), a.mul(2.0, a.mul(w2, w2)))
        root = a.sqrt(p)
        num = a.mul(16.0, a.sub(t2, a.mul(2.0, w2)))
        den = a.mul(a.add(t2, a.mul(8.0, w2)), root)
    elif kernel_id == "g_minus_v1":
        delta = a.sub(t2, w2)
        p = a.add(a.mul(delta, delta), a.mul(w2, w2))
        root = a.sqrt(p)
        sqrt2 = a.sqrt(2.0)
        num = a.mul(-16.0, t2)
        den = a.mul(root, a.add(a.add(t2, a.mul(2.0, w2)), a.mul(sqrt2, root)))
    else:
        raise ValueError("unknown fixed kernel")
    reading = a.div(num, den)
    return {"reading": reading, "closed": a.replay(), "node_count": len(a.nodes),
            "operation_defect_digest": a.digest(), "nonlinear_remainder": "sqrt identity denominators bounded by compiler witnesses"}
