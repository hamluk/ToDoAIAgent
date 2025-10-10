from typing import Optional
from pydantic import BaseModel, Field

from todoaiagent.adapters.trello.models import TrelloCard

class AgentResponseModel(BaseModel):
    """Structured response from the agent"""

    response: str = Field(description="Final answer to the user's question")
    todos: Optional[list[TrelloCard]] = Field(default=None, description="List of created Trello cards, if any")
    success: bool = Field(description="Indicates if the operation was successful")


