from pydantic import BaseModel


class TodoAgentSettings(BaseModel):
    llm_mistral_model: str
    mistral_api_key: str
    