
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from todoaiagent.config import LLMSettings
from todoaiagent.types.llm import LLMProviderName


def get_llm_chat_provider(llm_settings: LLMSettings):
    """
    Factory class to return LLM Chat Provider depending on current settings
    Args:
        llm_settings: llm specific settings

    Returns: LLM Langchain Chat Provider

    """
    if llm_settings.provider == LLMProviderName.MISTRAL:
        return ChatMistralAI(
            model_name=llm_settings.mistral.mistral_model,
            api_key=llm_settings.mistral.api_key
        )
    elif llm_settings.provider == LLMProviderName.OPENAI:
        return ChatOpenAI(
            temperature=llm_settings.openai.temperature,
            model=llm_settings.openai.api_model,
            api_key=llm_settings.openai.openai_api_key
        )

    raise ValueError(f"Unknown LLM Chat Provider {llm_settings.provider}. Provider currently not implemented")
