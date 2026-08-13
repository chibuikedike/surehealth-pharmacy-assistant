
from __future__ import annotations
from pathlib import Path
import base64
import streamlit as st
from ui.layout import load_css
from models.chat_session import ChatSession



base_dir = Path(__file__).resolve().parent
logo_path = base_dir / "assets" / "surehealth.png"


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

    logo_base64 = base64.b64encode(
        logo_path.read_bytes()
    ).decode()

    with st.sidebar:

        st.markdown(
            f"""
            <div class="sidebar-header">
                <img
                    src="data:image/png;base64,{logo_base64}"
                    class="sidebar-logo"
                >

                <div class="sidebar-title">
                    SureHealth Pharmacy Assistant
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
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
