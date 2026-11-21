"""Input parsing and checks shared by every operation."""
import sympy as sp

from core.errors import MatrixError

MAX_SIZE = 6


def parse_number(text, where: str = "Value") -> sp.Rational:
    """Turn user text like '3', '-2.5' or '1/3' into an exact SymPy number."""
    if text is None or str(text).strip() == "":
        raise MatrixError(f"{where} is empty.")
    text = str(text).strip()
    try:
        return sp.Rational(text)
    except (TypeError, ValueError, SyntaxError):
        raise MatrixError(f"{where}: '{text}' is not a number. Use e.g. 3, -2.5 or 1/3.") from None


def parse_matrix(rows: list[list], name: str = "Matrix") -> sp.Matrix:
    """Turn a grid of strings into a SymPy Matrix, with a clear error for the first bad cell."""
    if not rows or not rows[0]:
        raise MatrixError(f"{name} is empty.")
    return sp.Matrix([
        [parse_number(v, f"{name}, row {i + 1}, column {j + 1}") for j, v in enumerate(row)]
        for i, row in enumerate(rows)
    ])


def require_square(A: sp.Matrix, operation: str) -> None:
    if A.rows != A.cols:
        raise MatrixError(f"{operation} needs a square matrix, but this one is {A.rows}×{A.cols}.")


def require_same_shape(A: sp.Matrix, B: sp.Matrix, operation: str) -> None:
    if A.shape != B.shape:
        raise MatrixError(
            f"{operation} needs matrices of the same size, but A is {A.rows}×{A.cols} and B is {B.rows}×{B.cols}."
        )


def require_multipliable(A: sp.Matrix, B: sp.Matrix) -> None:
    if A.cols != B.rows:
        raise MatrixError(
            f"Cannot multiply: A has {A.cols} columns but B has {B.rows} rows. They must be equal."
        )