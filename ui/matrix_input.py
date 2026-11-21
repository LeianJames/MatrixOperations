"""Matrix size selection + grid input. Returns raw strings; parsing happens in app.py."""
import pandas as pd
import streamlit as st

from core.validation import MAX_SIZE
from data.samples import SAMPLES


def matrix_input(name: str, key: str) -> list[list[str]]:
    st.markdown(f"**Matrix {name}**")
    sample = st.selectbox("Load sample", ["(none)", *SAMPLES], key=f"{key}_sample")
    using_sample = sample != "(none)"

    c1, c2 = st.columns(2)
    rows = c1.number_input("Rows", 1, MAX_SIZE, 2, key=f"{key}_rows", disabled=using_sample)
    cols = c2.number_input("Columns", 1, MAX_SIZE, 2, key=f"{key}_cols", disabled=using_sample)

    if using_sample:
        grid = [[str(v) for v in row] for row in SAMPLES[sample]]
    else:
        grid = [["0"] * int(cols) for _ in range(int(rows))]

    df = pd.DataFrame(grid, columns=[f"C{j + 1}" for j in range(len(grid[0]))])
    # The key includes size + sample so the grid resets when either changes.
    edited = st.data_editor(df, key=f"{key}_grid_{len(grid)}x{len(grid[0])}_{sample}", hide_index=True)
    return edited.values.tolist()