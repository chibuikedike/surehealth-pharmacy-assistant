from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ChatMessage:
    """
    Represents a single message in the conversation.
    """

    role: str

    content: Optional[str] = None

    tool_call_id: Optional[str] = None

    name: Optional[str] = None

    tool_calls: Optional[list] = None

    def to_dict(self) -> dict:
        """
        Convert to the format expected by Groq/OpenAI.
        """

        message = {
            "role": self.role,
            "content": self.content,
        }

        if self.tool_call_id:
            message["tool_call_id"] = self.tool_call_id

        if self.name:
            message["name"] = self.name

        if self.tool_calls:
            message["tool_calls"] = self.tool_calls

        return message