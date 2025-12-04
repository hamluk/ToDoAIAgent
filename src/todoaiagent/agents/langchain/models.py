from pydantic import BaseModel, Field

from todoaiagent.domain.models import Todo


class TrelloTask(BaseModel):
    name: str = Field(description="The titel of the task")
    desc: str | None = Field(description="The accuarte description of the task", default=None)
    due: str | None = Field(description="Due date in ISO 8601 format", default=None)


    def __str__(self):
        return f"""Todo with '{self.name}' and description '{self.desc}' is due at {self.due} """
    

class TrelloTaskList(BaseModel):
    tasks: list[Todo] = Field(description="List of todo tasks to be created")
