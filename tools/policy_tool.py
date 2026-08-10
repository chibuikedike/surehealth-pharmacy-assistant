from services.policy_service import PolicyService

from tools.tool import Tool

from schemas.policy_schema import SEARCH_POLICY_SCHEMA


class PolicyTool:
    """
    Exposes policy-related functionality to the AI agent.
    """

    def __init__(self, policy_service: PolicyService):
        self._policy_service = policy_service

    # ==================================================
    # AI Callable Methods
    # ==================================================

    def search_policy(
        self,
        query: str | None = None,
        
    ):
    limit = 5
        """
        Search the pharmacy policy document.
        """

        return [
            chunk.to_dict()
            for chunk in self._policy_service.search_policy(
                query=query,
                limit=limit,
            )
        ]

    # ==================================================
    # Tool Registration
    # ==================================================

    def create_tools(self) -> list[Tool]:
        """
        Create all policy tools.
        """

        return [
            Tool(
                function=self.search_policy,
                schema=SEARCH_POLICY_SCHEMA,
            )
        ]
