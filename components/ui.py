from textwrap import dedent

import streamlit as st


def render_html(
    content: str,
):
    """
    Render trusted application HTML.
    """

    st.html(
        dedent(content)
    )