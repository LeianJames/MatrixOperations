"""Copy this to tests/test_<your_operation>.py (filename MUST start with test_).
Write at least: one normal case, one edge case, one invalid-input case."""
import pytest
import sympy as sp

from core.errors import MatrixError
# from operations.transpose import transpose


def test_normal_case():
    A = sp.Matrix([[1, 2], [3, 4]])
    # result = transpose(A)
    # assert result.answer == sp.Matrix([[1, 3], [2, 4]])
    # assert len(result.steps) > 0


def test_edge_case():
    ...  # 1×1 matrix, zero matrix, identity...


def test_invalid_input():
    with pytest.raises(MatrixError):
        ...  # e.g. trace of a non-square matrix