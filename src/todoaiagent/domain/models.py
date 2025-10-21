from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str = Field(description="Titles must be short, imperative, action-oriented (max ~60 chars).\n")
    description: Optional[str] = Field(description="The accuarte description of the task", default=None)
    priority: Optional[str] = Field(
        description="Priority of the task."
                    "Priority mapping (only 'low','medium','high'):"
                    "- 'must', 'ASAP', 'urgent', 'by tomorrow' => 'high'"
                    "- 'should', 'please', 'this week' => 'medium'"
                    "- 'optional', 'sometime', 'no rush' => 'low'",
    )  # TODO: map to trello label
    due: Optional[date] = Field(
        description="Due date with Date format: use ISO 8601 (YYYY-MM-DD)",
        default=None
    )
    labels: Optional[List[str]] = Field(
        description="Labels: infer 1-3 short keywords from context (e.g., 'marketing','design','invoice')")

    def __str__(self):
        return (f"Title: {self.title} with description: {self.description} and priority: {self.priority} "
                f"is due to: {self.due}")

    @property 
    def due_trello_format(self) -> Optional[str]:
        """Returns the due date in Trello's expected format (ISO 8601) or None if no due date is set."""
        return self.due.strftime("%m/%d/%Y") if self.due else None
