"""FAQ section. TODO(owner?): add real questions and answers."""
import streamlit as st

FAQ = {
    "How do I enter fractions?": "Type them like 1/3 or -5/2. Decimals like 0.5 also work.",
    "Why can't I find the inverse of my matrix?": "Only square matrices with a non-zero determinant have an inverse.",
    "When can two matrices be multiplied?": "When the number of columns of A equals the number of rows of B.",
}


def show_faq() -> None:
    for question, answer in FAQ.items():
        with st.expander(question):
            st.write(answer)