
from pydantic import BaseModel, SecretStr

from todoaiagent.types.llm import LLMProviderName


class Mistral(BaseModel):
    mistral_model: str
    api_key: SecretStr


class OpenAI(BaseModel):
    temperature: float
    api_model: str
    
    
class PromptSettings(BaseModel):
    system_prompt_file: str
    prompt_dir: str
    max_prompt_tokens: int


class LLMSettings(BaseModel):
    provider: LLMProviderName
    mistral: Mistral
    openai: OpenAI
    prompt: PromptSettings



