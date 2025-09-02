from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = Field(default="medium")  # TODO: map to trello label
    due: Optional[date] = None
    labels: List[str] = []