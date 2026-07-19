from config import settings

from bootstrap.register_tools import register_tools

from services.inventory_service import InventoryService
from services.policy_service import PolicyService
from services.memory_service import MemoryService
from services.llm_service import LLMService
from services.agent_service import AgentService

from tools.tool_registry import ToolRegistry

from models.chat_session import ChatSession


class ServiceContainer:
    """
    Application dependency container.

    Shared (singleton) services:
        - InventoryService
        - PolicyService
        - ToolRegistry
        - LLMService

    Per-conversation services:
        - MemoryService
        - AgentService
        - ChatSession
    """

    def __init__(self):

        self._inventory_service = None
        self._policy_service = None
        self._tool_registry = None
        self._llm_service = None

    # ======================================================
    # Shared Services
    # ======================================================

    @property
    def inventory_service(self) -> InventoryService:

        if self._inventory_service is None:
            self._inventory_service = InventoryService(
                settings.INVENTORY_FILE
            )

        return self._inventory_service

    @property
    def policy_service(self) -> PolicyService:

        if self._policy_service is None:
            self._policy_service = PolicyService(
                settings.POLICY_FILE
            )

        return self._policy_service

    @property
    def tool_registry(self) -> ToolRegistry:

        if self._tool_registry is None:

            self._tool_registry = register_tools(
                inventory_service=self.inventory_service,
                policy_service=self.policy_service,
            )

        return self._tool_registry

    @property
    def llm_service(self) -> LLMService:

        if self._llm_service is None:

            self._llm_service = LLMService(
                settings=settings,
                tool_registry=self.tool_registry,
            )

        return self._llm_service

    # ======================================================
    # Conversation Factory
    # ======================================================

    def create_chat(self) -> ChatSession:
        """
        Create a brand-new conversation.

        Shared services are reused while every
        conversation receives its own memory.
        """

        memory = MemoryService()

        agent = AgentService(
            llm=self.llm_service,
            memory=memory,
        )

        return ChatSession(
            agent=agent,
            memory=memory,
        )

    # ======================================================
    # Maintenance
    # ======================================================

    def reload_documents(self) -> None:
        """
        Reload inventory and policy documents.
        """

        self.inventory_service.reload_inventory()
        self.policy_service.reload_policy()

    # ======================================================
    # Diagnostics
    # ======================================================

    def health(self) -> dict:

        return {
            "inventory_items": len(
                self.inventory_service.get_all()
            ),
            "policy_chunks": self.policy_service.chunk_count,
            "registered_tools": len(
                self.tool_registry
            ),
        }

    def __repr__(self) -> str:

        return (
            "ServiceContainer("
            f"tools={len(self.tool_registry)}, "
            f"inventory={len(self.inventory_service.get_all())}, "
            f"policy_chunks={self.policy_service.chunk_count}"
            ")"
        )


_container: ServiceContainer | None = None


def get_container() -> ServiceContainer:
    """
    Return the application's singleton
    service container.
    """

    global _container

    if _container is None:
        _container = ServiceContainer()

    return _container