from typing import Protocol, Sequence

from todoaiagent.domain.models import Todo


class IProjectManagementClient(Protocol):
    def create_tasks(self, todos: Sequence[Todo], with_retry: bool) -> None: ...