from pathlib import Path
import base64
import streamlit as st

base_dir = Path(__file__).resolve().parent
logo_path = base_dir / "assets" / "surehealth.png"

# ==========================================================
# Page Configuration
# ==========================================================

def configure_page() -> None:
    """
    Configure the Streamlit page.
    """

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
      
        
        .app-header {
            display: flex;
            align-items: center;
            gap: 18px;
            width: 100%;
        }
        
        .app-logo {
            width: 70px;
            height: 70px;
            object-fit: contain;
            flex-shrink: 0;
        }
        
        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 0;
            padding: 0;
        }
        
        @media (max-width: 768px) {
        
            .app-header {
                gap: 12px;
                align-items: center;
            }
        
            .app-logo {
                width: 60px;
                height: 60px;
            }
        
            .app-title {
                font-size: 1.7rem;
                line-height: 1.15;
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
    logo_base64 = base64.b64encode(
        logo_path.read_bytes()
    ).decode()

    st.markdown(
        f"""
        <div class="app-header">
            <img
                src="data:image/png;base64,{logo_base64}"
                class="app-logo"
            >
            <div class="app-title">
                SureHealth Assistant
            </div>
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
