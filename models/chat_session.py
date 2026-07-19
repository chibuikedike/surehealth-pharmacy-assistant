from dataclasses import dataclass
from services.agent_service import AgentService
from services.memory_service import MemoryService


@dataclass(slots=True)
class ChatSession:
    """
    Represents a single conversation.

    Attributes
    ----------
    agent:
        Coordinates the interaction between the user,
        LLM and tools.

    memory:
        Stores the conversation history and working state.
    """

    agent: AgentService
    memory: MemoryService

    @property
    def history(self):
        """
        Shortcut to the conversation history.
        """

        return tuple(self.memory.get_history())

    @property
    def message_count(self) -> int:
        """
        Number of messages in the conversation.
        """

        return self.memory.history_length()

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no conversation exists.
        """

        return self.message_count == 0

    def chat(self, prompt: str) -> str:
        """
        Send a message to the AI assistant.

        This delegates the interaction to the AgentService,
        keeping the UI independent of the underlying services.
        """

        return self.agent.chat(prompt)

    def clear(self) -> None:
        """
        Clear the current conversation.
        """

        self.memory.clear()

    def reset(self) -> None:
        """
        Reset the conversation.

        Alias for clear() to provide a more expressive API.
        """

        self.clear()

    def __repr__(self) -> str:
        return (
            "ChatSession("
            f"messages={self.message_count}"
            ")"
        )