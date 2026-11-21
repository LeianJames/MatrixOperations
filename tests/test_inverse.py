import pytest
import sympy as sp

from core.errors import MatrixError
from operations.inverse import inverse


def test_2x2():
    A = sp.Matrix([[4, 7], [2, 6]])
    assert inverse(A).answer == sp.Matrix([[sp.Rational(3, 5), sp.Rational(-7, 10)],
                                           [sp.Rational(-1, 5), sp.Rational(2, 5)]])


def test_3x3_times_inverse_is_identity():
    A = sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    assert A * inverse(A).answer == sp.eye(3)


def test_needs_row_swap():
    A = sp.Matrix([[0, 1], [1, 0]])
    assert inverse(A).answer == A.inv()


def test_identity():
    assert inverse(sp.eye(3)).answer == sp.eye(3)


def test_singular():
    with pytest.raises(MatrixError, match="singular"):
        inverse(sp.Matrix([[1, 2], [2, 4]]))


def test_not_square():
    with pytest.raises(MatrixError):
        inverse(sp.Matrix([[1, 2, 3], [4, 5, 6]]))