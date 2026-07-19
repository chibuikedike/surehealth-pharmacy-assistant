from models.chat_message import ChatMessage
from models.agent_state import AgentState


class MemoryService:
    """
    Stores both conversation history and working memory.
    """

    def __init__(self):
        self.clear()

    # =====================================================
    # Conversation History
    # =====================================================

    def add_user_message(self, content: str):

        self._history.append(
            ChatMessage(
                role="user",
                content=content,
            )
        )

    def add_assistant_message(self, content: str):

        self._history.append(
            ChatMessage(
                role="assistant",
                content=content,
            )
        )

    def add_assistant_tool_call(
        self,
        tool_calls: list,
        content: str | None = None,
    ):
        """
        Store the assistant message that contains
        tool calls requested by the LLM.
        """

        self._history.append(
            ChatMessage(
                role="assistant",
                content=content,
                tool_calls=tool_calls,
            )
        )

    def add_tool_message(
        self,
        tool_name: str,
        tool_call_id: str,
        content: str,
    ):

        self._history.append(
            ChatMessage(
                role="tool",
                name=tool_name,
                tool_call_id=tool_call_id,
                content=content,
            )
        )


    def get_history(self):
        return tuple(self._history)

    def get_history_as_dict(self):
        return [
            message.to_dict()
            for message in self._history
        ]

    # =====================================================
    # Working Memory
    # =====================================================

    def get_state(self):
        return self._state

    def set_selected_item(self, item):
        self._state.selected_item = item

    def get_selected_item(self):
        return self._state.selected_item

    def set_last_search_results(self, results):
        self._state.last_search_results = results

    def get_last_search_results(self):
        return self._state.last_search_results

    def set_last_tool_result(self, result):
        self._state.last_tool_result = result

    def get_last_tool_result(self):
        return self._state.last_tool_result

    def set_current_intent(self, intent):
        self._state.current_intent = intent

    def get_current_intent(self):
        return self._state.current_intent

    def set_metadata(
        self,
        key,
        value,
    ):
        self._state.metadata[key] = value

    def get_metadata(
        self,
        key,
        default=None,
    ):
        return self._state.metadata.get(
            key,
            default,
        )

    # =====================================================
    # Utilities
    # =====================================================

    def history_length(self):
        return len(self._history)

    def clear_history(self):
        self._history.clear()

    def clear_state(self):
        self._state = AgentState()

    def clear(self):
        self._history = []
        self._state = AgentState()