from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = Field(default="medium")  # TODO: map to trello label
    due: Optional[date] = None
    labels: List[str] = []

    @property 
    def due_trello_format(self) -> Optional[str]:
        """Returns the due date in Trello's expected format (ISO 8601) or None if no due date is set."""
        return self.due.strftime("%m/%d/%Y") if self.due else None
