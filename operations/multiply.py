"""Matrix Multiplication — owner: Leian.

Each entry c_ij is the dot product of row i of A and column j of B.
"""
import sympy as sp

from core.result import Result
from core.validation import require_multipliable

FORMULA = r"(AB)_{ij} = \sum_{k=1}^{n} a_{ik}\, b_{kj}"


def _paren(x) -> str:
    return f"({sp.latex(x)})"


def multiply(A: sp.Matrix, B: sp.Matrix) -> Result:
    require_multipliable(A, B)
    result = Result(answer=None, formula=FORMULA)
    result.add_step(
        f"A is {A.rows}×{A.cols} and B is {B.rows}×{B.cols}. The inner sizes match ({A.cols} = {B.rows}), "
        f"so AB is {A.rows}×{B.cols}."
    )

    C = sp.zeros(A.rows, B.cols)
    for i in range(A.rows):
        for j in range(B.cols):
            products = [A[i, k] * B[k, j] for k in range(A.cols)]
            C[i, j] = sum(products, sp.Integer(0))
            terms = " + ".join(_paren(A[i, k]) + _paren(B[k, j]) for k in range(A.cols))
            result.add_step(
                f"Entry ({i + 1}, {j + 1}): row {i + 1} of A · column {j + 1} of B",
                latex=rf"c_{{{i + 1}{j + 1}}} = {terms} = {sp.latex(C[i, j])}",
            )

    result.add_step("Put all entries together.", C)
    result.answer = C
    return result