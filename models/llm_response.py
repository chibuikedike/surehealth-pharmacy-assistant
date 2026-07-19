from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LLMResponse:
    """
    Normalized response returned by the language model.
    """

    content: str | None = None

    tool_calls: list[Any] = field(default_factory=list)

    finish_reason: str | None = None

    @property
    def has_tool_calls(self) -> bool:
        """
        True if the model requested tool execution.
        """
        return bool(self.tool_calls)