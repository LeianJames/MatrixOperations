"""Entry point. Run with:  streamlit run app.py"""
import streamlit as st

from core.errors import MatrixError
from core.validation import parse_matrix, parse_number
from operations import (add_subtract, determinant, inverse, multiply, rank, row_ops,
                        scalar, trace, transpose)
from ui.export import show_export
from ui.faq import show_faq
from ui.history import add_to_history, show_history
from ui.matrix_input import matrix_input
from ui.steps_view import show_result

st.set_page_config(page_title="Matrix Calculator", layout="wide")

# name -> (what inputs it needs, function)
OPERATIONS = {
    "Addition (A + B)": ("two", add_subtract.add),
    "Subtraction (A − B)": ("two", add_subtract.subtract),
    "Scalar Multiplication (kA)": ("scalar", scalar.scalar_multiply),
    "Matrix Multiplication (AB)": ("two", multiply.multiply),
    "Transpose (Aᵀ)": ("one", transpose.transpose),
    "Trace": ("one", trace.trace),
    "Determinant": ("one", determinant.determinant),
    "Rank": ("one", rank.rank),
    "Inverse": ("one", inverse.inverse),
    "Row Reduction (RREF)": ("one", row_ops.rref),
}

with st.sidebar:
    st.title("Matrix Calculator")
    op_name = st.selectbox("Operation", list(OPERATIONS))
    if st.button("Clear / Reset"):
        st.session_state.clear()
        st.rerun()
    show_history()

tab_calc, tab_faq = st.tabs(["Calculator", "FAQ"])

with tab_faq:
    show_faq()

with tab_calc:
    kind, func = OPERATIONS[op_name]
    st.header(op_name)

    if kind == "two":
        col_a, col_b = st.columns(2)
        with col_a:
            raw_a = matrix_input("A", "A")
        with col_b:
            raw_b = matrix_input("B", "B")
    else:
        raw_a = matrix_input("A", "A")
        if kind == "scalar":
            raw_k = st.text_input("Scalar k", "2")

    if st.button("Compute", type="primary"):
        try:
            A = parse_matrix(raw_a, "Matrix A")
            if kind == "two":
                result = func(A, parse_matrix(raw_b, "Matrix B"))
            elif kind == "scalar":
                result = func(parse_number(raw_k, "Scalar k"), A)
            else:
                result = func(A)
            st.session_state["last"] = (op_name, result)
            st.session_state["reveal"] = False
            add_to_history(f"{op_name} → {result.answer}")
        except MatrixError as e:
            st.session_state.pop("last", None)
            st.error(str(e))
        except NotImplementedError as e:
            st.session_state.pop("last", None)
            st.warning(f"🚧 {e}")

    # Shown from session_state so the result survives reruns (e.g. clicking "Reveal").
    last = st.session_state.get("last")
    if last and last[0] == op_name:
        show_result(last[1])
        show_export(*last)