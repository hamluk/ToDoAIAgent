from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str = Field(description="The titel of the task")
    description: Optional[str] = Field(description="The accuarte description of the task", default=None)
    priority: Optional[str] = Field(description="Priority of the task. It can either be low, medium or high", default="medium")  # TODO: map to trello label
    due: Optional[date] = Field(description="Due date in ISO 8601 format", default=None)
    labels: Optional[List[str]] = []

    def __str__(self):
        return (f"Title: {self.title} with description: {self.description} and priority: {self.priority} "
                f"is due to: {self.due}")

    @property 
    def due_trello_format(self) -> Optional[str]:
        """Returns the due date in Trello's expected format (ISO 8601) or None if no due date is set."""
        return self.due.strftime("%m/%d/%Y") if self.due else None
