from pathlib import Path
import streamlit as st

# ==========================================================
# Page Configuration
# ==========================================================


def configure_page() -> None:
    """
    Configure the Streamlit page.
    """

    base_dir = Path(__file__).resolve().parent.parent
    logo_path = base_dir / "assets" / "surehealth.png"

    st.set_page_config(
        page_title="SureHealth Pharmacy Assistant",
        page_icon=str(logo_path),
        layout="wide",
        initial_sidebar_state="expanded",
    )

# ==========================================================
# Styling
# ==========================================================

def load_css() -> None:
    """
    Inject custom CSS.
    """

    st.markdown(
        """
        <style>

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }


        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0;
        }

        .app-subtitle {
            color: gray;
            font-size: 1rem;
            margin-top: -8px;
            margin-bottom: 30px;
        }

        .footer {
            text-align: center;
            color: gray;
            padding-top: 25px;
            padding-bottom: 10px;
            font-size: 0.85rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# Header
# ==========================================================

def render_header() -> None:
    """
    Display application header.
    """
    col1, col2 = st.columns([1, 10])

    with col1:
        st.image(
            str(logo_path),
            width=55,
        )

    with col2:
        st.markdown(
            """
            <div class="app-title">
                SureHealth Assistant
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="app-subtitle">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()


# ==========================================================
# Welcome Screen
# ==========================================================

def render_welcome() -> None:
    """
    Display the welcome message when there
    is no conversation yet.
    """

    st.info(
        """
👋 Welcome!

What do you need help with:

• Drugs, Inventory search, pricing or policy?
"""
    )


# ==========================================================
# Footer
# ==========================================================

def render_footer() -> None:
    """
    Render the application footer.
    """

    st.markdown(
        """
        <div class="footer">
           SureHealth Pharmacy Ltd • Powered by Groq  
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# Complete Layout
# ==========================================================

def render_layout() -> None:
    """
    Render the common application layout.
    """

    configure_page()

    load_css()

    render_header()
