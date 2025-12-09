from datetime import datetime
from enum import Enum
from typing import Protocol, Optional
from backend.models.db_models.task import Task
from backend.models.static import TaskStatus


class ITaskRepository(Protocol):

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        ...

    async def get_all(
            self,
            status: TaskStatus = None,
            start_search_date: datetime = None,
            end_search_date: datetime = None,
            owner_id: int = None,
            page: int = None,
            offset: int = 0,
            page_size: int = 10,
    ) -> list[Task]:
        ...

    async def create(self, **values) -> Task:
        ...

    async def update(self, task_id: int, **values) -> Optional[Task]:
        ...

    async def delete(self, task_id: int) -> bool:
        ...

    async def exists(self, **filters) -> Optional[Task]:
        ...