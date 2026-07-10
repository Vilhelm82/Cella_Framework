import pytest

from wreath_engine import f2

# The two matrices from the theorem report (sections 9 and 10).
B_STATIC = [[1, 0], [1, 1]]
B_ROT = [[1, 0, 0], [1, 1, 0], [0, 0, 1]]


def test_static_matrix_invertible():
    assert f2.rank(B_STATIC) == 2
    assert f2.is_invertible(B_STATIC)
    assert f2.kernel_basis(B_STATIC) == []


def test_rotating_matrix_invertible():
    assert f2.rank(B_ROT) == 3
    assert f2.is_invertible(B_ROT)
    assert f2.kernel_basis(B_ROT) == []


def test_orbit_rank_matches_theorem_5_1():
    # rank(B tensor I_d) = d * rank(B)
    assert f2.orbit_rank(B_STATIC, 5) == 10
    assert f2.orbit_rank(B_ROT, 5) == 15


def test_rank_deficient_kernel_is_relation_module():
    # rows 1 and 2 sum to row 3 mod 2 -> one relation
    b = [[1, 0, 1], [0, 1, 1], [1, 1, 0]]
    assert f2.rank(b) == 2
    assert not f2.is_invertible(b)
    kernel = f2.kernel_basis(b)
    assert len(kernel) == 1
    (v,) = kernel
    # verify it really is a kernel vector
    for row in b:
        assert sum(r * c for r, c in zip(row, v)) % 2 == 0
    assert v == [1, 1, 1]


def test_kron_identity_shape_and_content():
    k = f2.kron_identity(B_STATIC, 2)
    assert len(k) == 4 and len(k[0]) == 4
    assert k == [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
    ]


def test_nonsquare_never_invertible():
    assert not f2.is_invertible([[1, 0, 1]])


def test_validation_errors():
    with pytest.raises(ValueError):
        f2.rank([])
    with pytest.raises(ValueError):
        f2.rank([[1, 0], [1]])
    with pytest.raises(ValueError):
        f2.rank([[2]])
    with pytest.raises(ValueError):
        f2.kron_identity(B_STATIC, 0)
