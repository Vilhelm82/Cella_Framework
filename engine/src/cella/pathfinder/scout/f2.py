"""Exact F2 linear algebra for parity-row route evidence.

Native integer implementation; rows are tuples of 0/1.  This mirrors the
mathematics used by the Kummer valuation-parity lower bound (v1.3 §15.2)
without depending on any external module.
"""

from __future__ import annotations


def _echelon(rows: tuple[tuple[int, ...], ...]) -> tuple[list[list[int]], list[int]]:
    """Row-reduce over F2; returns (reduced rows, pivot column indices)."""

    matrix = [[bit % 2 for bit in row] for row in rows]
    if not matrix:
        return [], []
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("parity rows must share one width")
    pivots: list[int] = []
    rank = 0
    for column in range(width):
        pivot_row = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
        if pivot_row is None:
            continue
        matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
        for r in range(len(matrix)):
            if r != rank and matrix[r][column]:
                matrix[r] = [(a ^ b) for a, b in zip(matrix[r], matrix[rank])]
        pivots.append(column)
        rank += 1
        if rank == len(matrix):
            break
    return matrix[:rank], pivots


def f2_rank(rows: tuple[tuple[int, ...], ...]) -> int:
    reduced, _ = _echelon(rows)
    return len(reduced)


def f2_kernel_basis(rows: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    """Basis of the right kernel {v : M v = 0 over F2} of the row matrix."""

    if not rows:
        return ()
    width = len(rows[0])
    reduced, pivots = _echelon(rows)
    pivot_set = set(pivots)
    free_columns = [column for column in range(width) if column not in pivot_set]
    kernel: list[tuple[int, ...]] = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot in zip(reduced, pivots):
            if row[free]:
                vector[pivot] = 1
        kernel.append(tuple(vector))
    return tuple(kernel)


def f2_orbit_rank(rows: tuple[tuple[int, ...], ...], degree: int) -> int:
    """Rank of the block orbit matrix: each parity row acting across sheets."""

    if degree <= 0:
        raise ValueError("cover degree must be positive")
    return f2_rank(rows) * degree
