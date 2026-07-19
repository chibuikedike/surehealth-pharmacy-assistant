from tools.tool import Tool


class ToolRegistry:
    """
    Stores and manages all tools available to the AI agent.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    # ==================================================
    # Registration
    # ==================================================

    def register(self, tool: Tool) -> None:
        """
        Register a tool.
        """

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    # ==================================================
    # Retrieval
    # ==================================================

    def get(self, name: str) -> Tool:
        """
        Retrieve a registered tool by name.
        """

        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        return self._tools[name]

    def get_all_schemas(self) -> list[dict]:
        """
        Return all tool schemas in the format expected by the LLM.
        """

        return [
            tool.schema
            for tool in self._tools.values()
        ]

    # ==================================================
    # Utility
    # ==================================================

    def has_tool(self, name: str) -> bool:
        """
        Check whether a tool is registered.
        """

        return name in self._tools

    def remove(self, name: str) -> None:
        """
        Remove a registered tool.
        """

        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        del self._tools[name]

    def clear(self) -> None:
        """
        Remove all registered tools.
        """

        self._tools.clear()

    # ==================================================
    # Python Special Methods
    # ==================================================

    def __contains__(self, name: str) -> bool:
        """
        Enables:
            "search_inventory" in registry
        """

        return name in self._tools

    def __iter__(self):
        """
        Enables:
            for tool in registry:
                ...
        """

        return iter(self._tools.values())

    def __len__(self) -> int:
        """
        Enables:
            len(registry)
        """

        return len(self._tools)

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        tools = ", ".join(self._tools.keys())
        return f"ToolRegistry([{tools}])"