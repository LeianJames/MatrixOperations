"""Shared contract: every operation returns a Result."""
from dataclasses import dataclass, field
from typing import Any

import sympy as sp


@dataclass
class Step:
    description: str                  # e.g. "R2 → R2 − 3·R1"
    matrix: sp.Matrix | None = None   # state of the matrix after this step (optional)
    latex: str | None = None          # extra math to display with st.latex (optional)


@dataclass
class Result:
    answer: Any                       # sp.Matrix, or a number (det, trace, rank)
    formula: str                      # LaTeX of the general formula
    steps: list[Step] = field(default_factory=list)

    def add_step(self, description: str, matrix: sp.Matrix | None = None, latex: str | None = None) -> None:
        """Record a step. The matrix is copied so later changes don't overwrite earlier steps."""
        self.steps.append(Step(description, None if matrix is None else matrix.copy(), latex))