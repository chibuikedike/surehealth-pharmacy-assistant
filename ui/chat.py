from __future__ import annotations
import streamlit as st
from models.chat_session import ChatSession
from ui.layout import render_welcome


# ==========================================================
# History
# ==========================================================

def display_history(
    session: ChatSession,
) -> None:
    """
    Display the current conversation.
    """

    for message in session.history:

        # Internal tool messages are not shown.
        if message.role == "tool":
            continue

        # Skip assistant tool-call placeholders.
        if (
            message.role == "assistant"
            and not message.content
        ):
            continue

        if message.role == "user":
            avatar = "assets/user.png"

        elif message.role == "assistant":
            avatar = "assets/surehealth.png"

        else:
            avatar = None

        with st.chat_message(
            message.role,
            avatar=avatar,
        ):
            if message.content:
                st.markdown(message.content)


# ==========================================================
# Welcome
# ==========================================================

def display_welcome_screen(
    session: ChatSession,
) -> None:
    """
    Display the welcome screen for a new conversation.
    """

    if session.is_empty:
        render_welcome()


# ==========================================================
# User Input
# ==========================================================

def get_user_prompt() -> str | None:
    """
    Display the chat input widget.
    """

    return st.chat_input(
        "Ask about inventory or pharmacy policies "
    )


# ==========================================================
# Error Handling
# ==========================================================

def display_error(
    error: Exception,
) -> None:
    """
    Display unexpected errors.
    """

    st.error(
        f"An unexpected error occurred.\n\n{error}"
    )


# ==========================================================
# Prompt Processing
# ==========================================================

def process_prompt(
    session: ChatSession,
    prompt: str,
) -> None:
    

    if not prompt:
        return

    try:

        with st.spinner("Thinking..."):

            session.chat(prompt)

        st.rerun()

    except Exception as error:

        display_error(error)


# ==========================================================
# Main Chat
# ==========================================================

def render_chat(
    session: ChatSession,
) -> None:
    """
    Render the complete chat interface.
    """

    # ------------------------------------------
    # Existing conversation
    # ------------------------------------------

    display_history(session)

    # ------------------------------------------
    # Welcome screen
    # ------------------------------------------

    display_welcome_screen(session)

    # ------------------------------------------
    # Wait for user input
    # ------------------------------------------

    prompt = get_user_prompt()

    if prompt:

        process_prompt(
            session=session,
            prompt=prompt,
        )
