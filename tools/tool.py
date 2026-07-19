from dataclasses import dataclass
from typing import Any, Callable


@dataclass(slots=True)
class Tool:
    """
    Represents a tool that the LLM can invoke.
    """

    function: Callable
    schema: dict

    @property
    def name(self) -> str:
        """
        Return the tool name from its schema.
        """
        return self.schema["function"]["name"]

    @property
    def description(self) -> str:
        """
        Return the tool description from its schema.
        """
        return self.schema["function"]["description"]

    def __call__(self, **kwargs) -> Any:
        """
        Execute the underlying tool function.
        """
        return self.function(**kwargs)

    def __repr__(self) -> str:
        return f"Tool(name='{self.name}')"