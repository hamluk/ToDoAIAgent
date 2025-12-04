from typing import Sequence
from todoaiagent.adapters.trello.models import TrelloCard
from todoaiagent.domain.models import Todo
from todoaiagent.domain.ports import IProjectManagementClient


class TodoService():
    def __init__(self, pm_client: IProjectManagementClient):
        self.pm_client = pm_client

    def createTodo(self, todo_list: Sequence[Todo], idList: str) -> list[TrelloCard]:
        todos = None
        try:
            todos = self.pm_client.create_tasks(todo_list, idList)
        except Exception:
            raise
        
        return todos