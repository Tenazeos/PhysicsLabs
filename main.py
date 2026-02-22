import textwrap

import streamlit as st

from labs import pages as lab_pages


def main_page() -> None:
    st.set_page_config(page_title="Info", page_icon=":material/info:", layout="centered")

    st.title("Hey there!")

    st.markdown(
        textwrap.dedent(
            """
            Here you can find **interactive labs** (experiment simulations),
            play with parameters and enjoy immediate results!
            """
        )
    )


pages = {
    "": [st.Page(main_page, title="Info", icon=":material/info:", default=True)],
    **lab_pages,
}

nav = st.navigation(pages, position="sidebar", expanded=True)
nav.run()
