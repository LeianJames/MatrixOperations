import pytest
import sympy as sp

from core.errors import MatrixError
from operations.row_ops import add_row_multiple, rref, scale_row, swap_rows

A = sp.Matrix([[1, 2], [3, 4]])


def test_swap_rows():
    assert swap_rows(A, 0, 1) == sp.Matrix([[3, 4], [1, 2]])
    assert A == sp.Matrix([[1, 2], [3, 4]])  # original unchanged


def test_scale_row():
    assert scale_row(A, 1, sp.Rational(1, 2)) == sp.Matrix([[1, 2], [sp.Rational(3, 2), 2]])


def test_scale_row_by_zero_is_invalid():
    with pytest.raises(MatrixError):
        scale_row(A, 0, 0)


def test_add_row_multiple():
    assert add_row_multiple(A, 1, 0, -3) == sp.Matrix([[1, 2], [0, -2]])


def test_invalid_row_index():
    with pytest.raises(MatrixError):
        swap_rows(A, 0, 5)


@pytest.mark.parametrize("M", [
    sp.Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]),   # invertible
    sp.Matrix([[1, 2], [2, 4]]),                         # singular
    sp.Matrix([[0, 1], [1, 0]]),                         # needs a swap
    sp.Matrix([[1, 2, 3], [4, 5, 6]]),                   # rectangular
    sp.Matrix([[0, 0], [0, 0]]),                         # zero matrix
    sp.Matrix([[0, 2, 4], [0, 1, 3]]),                   # first column all zero
    sp.Matrix([[5]]),                                    # 1x1
])
def test_rref_matches_sympy(M):
    result = rref(M)
    assert result.answer == M.rref()[0]
    assert len(result.steps) >= 2


def test_rref_records_swap_step():
    result = rref(sp.Matrix([[0, 1], [1, 0]]))
    assert "↔" in result.steps[1].description