"""Formula display, step-by-step solution, reveal final answer."""
import sympy as sp
import streamlit as st

from core.result import Result


def show_result(result: Result) -> None:
    st.subheader("Formula")
    st.latex(result.formula)

    st.subheader("Step-by-step solution")
    if not result.steps:
        st.info("No steps were recorded for this operation.")
    for n, step in enumerate(result.steps, start=1):
        st.markdown(f"**Step {n}.** {step.description}")
        if step.latex:
            st.latex(step.latex)
        if step.matrix is not None:
            st.latex(sp.latex(step.matrix))

    if st.toggle("Reveal final answer", key="reveal"):
        st.success("Final answer")
        st.latex(sp.latex(result.answer))