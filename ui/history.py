"""Operation history (lives in st.session_state, lost on refresh).
TODO(owner?): nicer display, click an entry to reload it, clear-history button."""
import streamlit as st


def add_to_history(entry: str) -> None:
    st.session_state.setdefault("history", []).append(entry)


def show_history() -> None:
    st.subheader("History")
    history = st.session_state.get("history", [])
    if not history:
        st.caption("No calculations yet.")
    for entry in reversed(history[-10:]):
        st.text(entry)