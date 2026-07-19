import streamlit as st
from bootstrap.service_container import get_container
from ui.layout import render_layout, render_footer
from ui.session import (
    get_chat_session,
    reset_chat_session,
)
from ui.chat import render_chat
from ui.sidebar import render_sidebar


def main() -> None:
    """
    Run the Pharmacy AI Assistant.
    """

    # ------------------------------------------
    # Common page layout
    # ------------------------------------------

    render_layout()

    # ------------------------------------------
    # Services
    # ------------------------------------------

    container = get_container()

    # ------------------------------------------
    # Current conversation
    # ------------------------------------------

    session = get_chat_session(container)

    # ------------------------------------------
    # Sidebar
    # ------------------------------------------

    actions = render_sidebar(session)

    if actions["new_chat"]:

        reset_chat_session(container)

        st.rerun()

    if actions["selected_example"]:

        session.chat(
            actions["selected_example"],
        )

        st.rerun()
    # ------------------------------------------
    # Main chat interface
    # ------------------------------------------

    render_chat(session)

    # ------------------------------------------
    # Footer
    # ------------------------------------------

    render_footer()


if __name__ == "__main__":
    main()