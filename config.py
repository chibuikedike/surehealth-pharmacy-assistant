import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Central application configuration.
    """
   
    # API Keys and LLM

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    MODEL_NAME: str = "llama-3.1-8b-instant"

    TEMPERATURE: float = 0.2

    MAX_TOKENS: int = 1024

    # Prompt Files

    SYSTEM_PROMPT: str = "prompts/system_prompt.txt"

    REFERENCE_PROMPT: str = "prompts/reference_prompt.txt"
   
    # Documents

    INVENTORY_FILE: str = "documents/pharmacy_inventory_2000.csv"

    POLICY_FILE: str = "documents/policy.txt"


settings = Settings()