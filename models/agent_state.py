from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    """
    Working memory for the AI agent.
    """

    selected_item: dict | None = None

    last_search_results: list[dict] = field(default_factory=list)

    last_tool_result: Any = None

    current_intent: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)