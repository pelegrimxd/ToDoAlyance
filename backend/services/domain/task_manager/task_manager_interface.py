from typing import Protocol, Optional
from backend.models.schemas.task import SUpdatedTask, SCreateTask, SFilterTask, STask


class ITaskManager(Protocol):
    async def update_task(self, owner_id: int, update_task: SUpdatedTask) -> Optional[STask]:
        ...

    async def create_task(self, owner_id: int, new_task: SCreateTask) -> STask:
        ...

    async def delete_task(self, owner_id: int, task_id: int) -> bool:
        ...

    async def get_tasks(self, owner_id: int, filters: SFilterTask) -> list[STask]:
        ...

    async def get_task_by_id(self, task_id: int, owner_id: int):
        ...

    async def update_recalculate_overdue_tasks(self) -> int:
        ...