
from __future__ import annotations

import streamlit as st

from models.chat_session import ChatSession




# ==========================================================
# Sidebar
# ==========================================================

def render_sidebar(
    session: ChatSession,
) -> dict[str, bool | str | None]:

    actions = {
        "new_chat": False,
        "selected_example": None,
    }

    with st.sidebar:

        st.title("⚕️ SureHealth Pharmacy Assistant")

        st.caption(
            "Inventory • Policies • References"
        )

        st.divider()

        # --------------------------------------
        # Conversation
        # --------------------------------------

        st.subheader("Conversation")

        st.metric(
            label="Messages",
            value=session.message_count,
        )

        if st.button(
            "New Conversation",
            use_container_width=True,
        ):
            actions["new_chat"] = True

        st.divider()

       

        # --------------------------------------
        # About
        # --------------------------------------

        st.subheader("About")

        st.caption(
            "Powered by Groq "
        )

        st.caption(
            "Version 1.0.0"
        )

    return actions
