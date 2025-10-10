from dataclasses import dataclass
from todoaiagent.services.todo_service import TodoService

@dataclass
class TodoAgentDependencies:
    todo_service: TodoService
    idList: str