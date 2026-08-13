import json
from pathlib import Path
from groq import Groq
from config import Settings
from models.chat_message import ChatMessage
from models.llm_response import LLMResponse
from tools.tool_registry import ToolRegistry
from services.memory_service import MemoryService
from tools.tool_validator import ToolValidator


class LLMService:
    """
    Handles all interactions with the language model.

    Responsibilities:
        - Load the system prompt
        - Build messages
        - Call the LLM
        - Parse LLM responses
        - Execute tool calls (Part 2)
    """

    def __init__(
        self,
        settings: Settings,
        tool_registry: ToolRegistry,
    ):
        self.settings = settings
        self.registry = tool_registry
        self.validator = ToolValidator()

        self.client = Groq(
            api_key=self.settings.GROQ_API_KEY
        )

        self.system_prompt = self._load_system_prompt()

    # =====================================================
    # Prompt Loading
    # =====================================================

    def _load_system_prompt(self) -> str:
        """
        Load the system prompt from disk.
        """

        prompt_path = Path(
            self.settings.SYSTEM_PROMPT
        )

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"System prompt not found: {prompt_path}"
            )

        return prompt_path.read_text(
            encoding="utf-8"
        )

    # =====================================================
    # Message Construction
    # =====================================================

    def _build_messages(
        self,
        history: list[ChatMessage],
    ) -> list[dict]:
        """
        Build the conversation sent to the LLM.
        """

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        messages.extend(
            message.to_dict()
            for message in history
        )

        return messages

    # =====================================================
    # LLM Communication
    # =====================================================

    def _call_llm(
        self,
        messages: list[dict],
        use_tools: bool = True,
    ):
        """
        Send a request to the language model.
        """

        request = {
            "model": self.settings.MODEL_NAME,
            "messages": messages,
            "temperature": self.settings.TEMPERATURE,
            "max_tokens": self.settings.MAX_TOKENS,
        }

        if use_tools:
            request["tools"] = (
                self.registry.get_all_schemas()
            )
            request["tool_choice"] = "auto"
            

        return self.client.chat.completions.create(
            **request
        )

    # =====================================================
    # Response Parsing
    # =====================================================

    def _parse_response(
        self,
        response,
    ) -> LLMResponse:
        """
        Convert the Groq response into our internal model.
        """

        choice = response.choices[0]

        message = choice.message

        return LLMResponse(
            content=message.content,
            tool_calls=message.tool_calls or [],
            finish_reason=choice.finish_reason,
        )
    # =====================================================
    # Tool Execution
    # =====================================================

    def _execute_tool_calls(
        self,
        response: LLMResponse,
        memory: MemoryService,
    ) -> None:
        """
        Execute every tool requested by the LLM and
        store both the assistant tool-call message and
        the tool responses in memory.
        """

        memory.add_assistant_tool_call(
            tool_calls=response.tool_calls,
            content=response.content,
        )

        for tool_call in response.tool_calls:

            result = self._run_tool(tool_call)

            memory.add_tool_message(
                tool_name=tool_call.function.name,
                tool_call_id=tool_call.id,
                content=self._serialize_tool_result(result),
            )

    # =====================================================
    # Public API
    # =====================================================

    def generate_response(
        self,
        memory: MemoryService,
    ) -> str:
        """
        Generate the assistant's response.

        Workflow:
            1. Build the conversation.
            2. Send it to the LLM.
            3. Execute any requested tools.
            4. Send the updated conversation back.
            5. Store the final assistant response.
        """

        # -----------------------------------------
        # First LLM call
        # -----------------------------------------

        messages = self._build_messages(
            memory.get_history()
        )

        response = self._parse_response(
            self._call_llm(messages)
        )

        # -----------------------------------------
        # No tool calls
        # -----------------------------------------

        if not response.has_tool_calls:

            memory.add_assistant_message(
                response.content or ""
            )

            return response.content or ""

        # -----------------------------------------
        # Execute tools
        # -----------------------------------------

        self._execute_tool_calls(
            response,
            memory,
        )

        # -----------------------------------------
        # Second LLM call
        # -----------------------------------------

        messages = self._build_messages(
            memory.get_history()
        )

        final_response = self._parse_response(
            self._call_llm(
                messages,
                use_tools=False,
            )
        )

        memory.add_assistant_message(
            final_response.content or ""
        )

        return final_response.content or ""

   def _run_tool(
    self,
    tool_call,
):
    tool_name = tool_call.function.name

    tool = self.registry.get(tool_name)

    arguments = self._parse_tool_arguments(
        tool_call
    )

    is_valid, reason = self.validator.validate(
        tool_name,
        arguments,
    )

    if not is_valid:
        return {
            "success": False,
            "error": reason,
            "tool": tool_name,
        }

    result = tool(**arguments)

    return {
        "success": True,
        "data": result,
    }

    # -----------------------------------------------------

    def _parse_tool_arguments(
        self,
        tool_call,
    ) -> dict:
        """
        Parse the JSON arguments supplied by the LLM.
        """

        arguments = tool_call.function.arguments

        if not arguments:
            return {}

        return json.loads(arguments)

    # -----------------------------------------------------

    def _serialize_tool_result(
        self,
        result,
    ) -> str:
        """
        Convert tool output into JSON that can be
        returned to the language model.
        """

        if result is None:
            return ""

        if isinstance(result, str):
            return result

        if hasattr(result, "to_dict"):
            return json.dumps(
                result.to_dict(),
                indent=2,
                default=str,
            )

        if isinstance(result, list):

            serialized = []

            for item in result:

                if hasattr(item, "to_dict"):
                    serialized.append(
                        item.to_dict()
                    )
                else:
                    serialized.append(item)

            return json.dumps(
                serialized,
                indent=2,
                default=str,
            )

        if isinstance(result, dict):

            return json.dumps(
                result,
                indent=2,
                default=str,
            )

        return json.dumps(
            str(result)
        )
