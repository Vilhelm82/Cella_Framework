"""GF(2) linear algebra for parity matrices.

Matrices are lists of rows; each row is a list of 0/1 ints. All arithmetic is
mod 2. These functions implement the linear-algebra half of the wreath-lift
theorem: rank of the sheet-level matrix B, the kernel (the square-class
relation module when nonzero), and the orbit matrix B tensor I_d.
"""

from __future__ import annotations

Matrix = list[list[int]]


def _validate(m: Matrix) -> None:
    if not m or not m[0]:
        raise ValueError("empty matrix")
    width = len(m[0])
    for row in m:
        if len(row) != width:
            raise ValueError("ragged matrix")
        for x in row:
            if x not in (0, 1):
                raise ValueError(f"entry {x!r} is not 0 or 1")


def _row_echelon(m: Matrix) -> tuple[Matrix, list[int]]:
    """Return (reduced row-echelon form, pivot column indices)."""
    _validate(m)
    a = [row[:] for row in m]
    rows, cols = len(a), len(a[0])
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(rows):
            if i != r and a[i][c]:
                a[i] = [(x ^ y) for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return a, pivots


def rank(m: Matrix) -> int:
    return len(_row_echelon(m)[1])


def kernel_basis(m: Matrix) -> list[list[int]]:
    """Basis of the right kernel {c : m @ c = 0 over F2}.

    For a parity matrix on conjugate radicands, a nonzero kernel vector is an
    explicit multiplicative square-class relation (theorem report section 8).
    """
    echelon, pivots = _row_echelon(m)
    cols = len(m[0])
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for r, p in enumerate(pivots):
            if echelon[r][f]:
                v[p] = 1
        basis.append(v)
    return basis


def is_invertible(m: Matrix) -> bool:
    _validate(m)
    return len(m) == len(m[0]) and rank(m) == len(m)


def kron_identity(m: Matrix, d: int) -> Matrix:
    """The orbit matrix m tensor I_d (theorem 5.1, equation 5.3)."""
    _validate(m)
    if d < 1:
        raise ValueError("d must be positive")
    rows, cols = len(m), len(m[0])
    out = [[0] * (cols * d) for _ in range(rows * d)]
    for i in range(rows):
        for j in range(cols):
            if m[i][j]:
                for k in range(d):
                    out[i * d + k][j * d + k] = 1
    return out


def orbit_rank(m: Matrix, d: int) -> int:
    """rank(m tensor I_d) = d * rank(m); computed directly for auditability."""
    return rank(kron_identity(m, d))
