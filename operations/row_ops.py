"""Row Operations — owner: Leian.

The three elementary row operations, plus Gauss-Jordan elimination (RREF) built
only from them. Rank (Hollie) and Inverse use rref().
All functions return NEW matrices; the input is never changed.
"""
import sympy as sp

from core.errors import MatrixError
from core.result import Result

FORMULA = r"R_i \leftrightarrow R_j,\quad R_i \to kR_i\ (k \neq 0),\quad R_i \to R_i + kR_j"


def _fmt(k) -> str:
    """Show a number nicely in step text: 3 → '3', 1/2 → '(1/2)', -2 → '(-2)'."""
    text = str(k)
    return f"({text})" if ("/" in text or text.startswith("-")) else text


def _check_row(A: sp.Matrix, i: int) -> None:
    if not 0 <= i < A.rows:
        raise MatrixError(f"Row {i + 1} does not exist. The matrix has {A.rows} rows.")


def swap_rows(A: sp.Matrix, i: int, j: int) -> sp.Matrix:
    """R_i ↔ R_j (0-based indexes)."""
    _check_row(A, i)
    _check_row(A, j)
    M = A.copy()
    M[i, :], M[j, :] = A[j, :], A[i, :]
    return M


def scale_row(A: sp.Matrix, i: int, k) -> sp.Matrix:
    """R_i → k·R_i. k = 0 is not allowed (it would destroy information)."""
    _check_row(A, i)
    if k == 0:
        raise MatrixError("Cannot multiply a row by 0. That is not an elementary row operation.")
    M = A.copy()
    M[i, :] = k * A[i, :]
    return M


def add_row_multiple(A: sp.Matrix, target: int, source: int, k) -> sp.Matrix:
    """R_target → R_target + k·R_source."""
    _check_row(A, target)
    _check_row(A, source)
    if target == source:
        raise MatrixError("Target and source rows must be different.")
    M = A.copy()
    M[target, :] = A[target, :] + k * A[source, :]
    return M


def rref(A: sp.Matrix, pivot_cols: int | None = None) -> Result:
    """Reduced row echelon form by Gauss-Jordan elimination.

    pivot_cols: only look for pivots in the first `pivot_cols` columns.
    Inverse uses this on [A | I] so it only pivots in the A half.
    """
    M = A.copy()
    rows = M.rows
    limit = M.cols if pivot_cols is None else pivot_cols
    result = Result(answer=None, formula=r"A \xrightarrow{\text{row operations}} \operatorname{RREF}(A)")
    result.add_step("Start with the matrix.", M)

    pivot_row = 0
    for col in range(limit):
        if pivot_row >= rows:
            break

        # 1. Find a row (at or below pivot_row) with a non-zero entry in this column.
        found = next((r for r in range(pivot_row, rows) if M[r, col] != 0), None)
        if found is None:
            result.add_step(f"Column {col + 1} has no non-zero entry from row {pivot_row + 1} down, so skip it.")
            continue

        # 2. Move it up into the pivot position.
        if found != pivot_row:
            M = swap_rows(M, found, pivot_row)
            result.add_step(
                f"R{pivot_row + 1} ↔ R{found + 1}  (bring a non-zero pivot into column {col + 1})", M
            )

        # 3. Make the pivot equal to 1.
        pivot = M[pivot_row, col]
        if pivot != 1:
            k = 1 / pivot
            M = scale_row(M, pivot_row, k)
            result.add_step(f"R{pivot_row + 1} → {_fmt(k)}·R{pivot_row + 1}  (make the pivot 1)", M)

        # 4. Make every other entry in this column 0.
        for r in range(rows):
            if r != pivot_row and M[r, col] != 0:
                k = -M[r, col]
                M = add_row_multiple(M, r, pivot_row, k)
                sign, size = ("−", -k) if k < 0 else ("+", k)
                result.add_step(
                    f"R{r + 1} → R{r + 1} {sign} {_fmt(size)}·R{pivot_row + 1}  (clear column {col + 1})", M
                )

        pivot_row += 1

    if len(result.steps) == 1:
        result.add_step("The matrix is already in reduced row echelon form.")
    result.answer = M
    return result