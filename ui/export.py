"""Copy / download results. st.code already has a copy button in its top-right corner.
TODO(owner?): nicer text format, maybe CSV or LaTeX download options."""
import streamlit as st

from core.result import Result


def result_to_text(operation: str, result: Result) -> str:
    lines = [f"Operation: {operation}", "", "Steps:"]
    lines += [f"{n}. {s.description}" for n, s in enumerate(result.steps, start=1)]
    lines += ["", f"Answer: {result.answer}"]
    return "\n".join(lines)


def show_export(operation: str, result: Result) -> None:
    text = result_to_text(operation, result)
    with st.expander("Copy / Download"):
        st.code(text, language=None)
        st.download_button("Download as .txt", text, file_name="matrix_result.txt")