import pytest
import sympy as sp

from core.errors import MatrixError
from core.validation import parse_matrix, parse_number, require_multipliable, require_square


def test_parse_number_handles_fractions_and_decimals():
    assert parse_number("1/3") == sp.Rational(1, 3)
    assert parse_number("-2.5") == sp.Rational(-5, 2)


@pytest.mark.parametrize("bad", ["", "abc", None, "1//2"])
def test_parse_number_rejects_bad_input(bad):
    with pytest.raises(MatrixError):
        parse_number(bad)


def test_parse_matrix_reports_cell_position():
    with pytest.raises(MatrixError, match="row 2, column 1"):
        parse_matrix([["1", "2"], ["x", "4"]], "Matrix A")


def test_require_square():
    with pytest.raises(MatrixError):
        require_square(sp.Matrix([[1, 2, 3]]), "Determinant")


def test_require_multipliable():
    require_multipliable(sp.ones(2, 3), sp.ones(3, 1))  # OK, no error
    with pytest.raises(MatrixError):
        require_multipliable(sp.ones(2, 3), sp.ones(2, 3))