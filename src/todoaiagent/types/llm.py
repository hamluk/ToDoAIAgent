from enum import Enum


class LLMProviderName(str, Enum):
    """
    LLM Provider Names
    """
    MISTRAL = "MISTRAL"
    OPENAI = "OPENAI"
