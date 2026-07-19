import streamlit as st

from bootstrap.service_container import ServiceContainer
from models.chat_session import ChatSession


SESSION_KEY = "chat_session"


def get_chat_session(
    container: ServiceContainer,
) -> ChatSession:
    """
    Return the current chat session.

    Creates one if it does not already exist.
    """

    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = container.create_chat()

    return st.session_state[SESSION_KEY]


def clear_chat_session() -> None:
    """
    Clear the current conversation.
    """

    if SESSION_KEY in st.session_state:
        st.session_state[SESSION_KEY].clear()


def reset_chat_session(
    container: ServiceContainer,
) -> ChatSession:
    """
    Start a brand new conversation.
    """

    st.session_state[SESSION_KEY] = container.create_chat()

    return st.session_state[SESSION_KEY]


def has_chat_session() -> bool:
    """
    Returns True if a chat session exists.
    """

    return SESSION_KEY in st.session_state


def remove_chat_session() -> None:
    """
    Remove the chat session from Streamlit.
    """

    st.session_state.pop(
        SESSION_KEY,
        None,
    )