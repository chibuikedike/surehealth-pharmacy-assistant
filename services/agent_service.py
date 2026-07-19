from services.llm_service import LLMService
from services.memory_service import MemoryService


class AgentService:

    def __init__(
        self,
        llm: LLMService,
        memory: MemoryService,
    ):
        self.llm = llm
        self.memory = memory

    def chat(
        self,
        user_message: str,
    ) -> str:
        """
        Handle one interaction with the user.
        """

        self.memory.add_user_message(
            user_message
        )

        return self.llm.generate_response(
            self.memory
        )

    def reset(self):
        """
        Start a new conversation.
        """

        self.memory.clear()