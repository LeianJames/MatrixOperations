"""Inverse — owner: Leian.

Gauss-Jordan method: row-reduce [A | I]. If the left half becomes I,
the right half is A⁻¹. If it can't (a zero row appears), A is singular.
"""
import sympy as sp

from core.errors import MatrixError
from core.result import Result
from core.validation import require_square
from operations.row_ops import rref

FORMULA = r"[\,A \mid I\,] \xrightarrow{\text{row ops}} [\,I \mid A^{-1}\,]"


def inverse(A: sp.Matrix) -> Result:
    require_square(A, "Inverse")
    n = A.rows

    result = Result(answer=None, formula=FORMULA)
    augmented = A.row_join(sp.eye(n))
    result.add_step(
        f"Write the augmented matrix [A | I]. The first {n} columns are A, the last {n} are the identity.",
        augmented,
    )

    reduced = rref(augmented, pivot_cols=n)
    result.steps += reduced.steps[1:]  # skip rref's own "Start with the matrix" step

    left, right = reduced.answer[:, :n], reduced.answer[:, n:]
    if left != sp.eye(n):
        raise MatrixError(
            "This matrix is singular (its determinant is 0), so it has no inverse. "
            "Row reduction could not turn the left half into the identity matrix."
        )

    result.add_step("The left half is now the identity, so the right half is A⁻¹.", right)
    result.answer = right
    return result