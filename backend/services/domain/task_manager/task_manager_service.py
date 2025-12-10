from dataclasses import asdict
from typing import Optional
from datetime import datetime
from backend.models.schemas.task import SCreateTask, STask, SUpdatedTask, SFilterTask
from backend.models.static import TaskStatus
from backend.services.domain.task_manager.exception import AccessUserToTaskError, TaskWithThisNameAlreadyExistException
from backend.services.domain.task_manager.task_manager_interface import ITaskManager
from backend.services.infrastructure.task_database.task_database_interface import ITaskRepository


class TaskManager(ITaskManager):

    def __init__(self, task_repo: ITaskRepository):
        self.task_repo = task_repo

    async def update_task(self, owner_id: int, update_task: SUpdatedTask) -> Optional[STask]:
        task = await self.task_repo.exists(id=update_task.id)
        if owner_id != task.owner:
            raise AccessUserToTaskError
        if update_task.status == TaskStatus.done:
            update_task.due_date = datetime.now()
        task = await self.task_repo.update(task_id=update_task.id, **update_task.model_dump())
        return STask.model_validate(task)

    async def create_task(self, owner_id: int, new_task: SCreateTask) -> STask:
        if await self.task_repo.exists(title=new_task.title):
            raise TaskWithThisNameAlreadyExistException
        task = await self.task_repo.create(owner=owner_id, **new_task.model_dump())
        return STask.model_validate(task)

    async def delete_task(self, owner_id: int, task_id: int) -> bool:
        task = await self.task_repo.exists(id=task_id)
        if owner_id == task.owner:
            return await self.task_repo.delete(task_id)
        raise AccessUserToTaskError

    async def get_tasks(self, owner_id: int, filters: SFilterTask) -> list[STask]:
        offset = (filters.page - 1) * filters.page_size
        tasks = await self.task_repo.get_all(owner_id=owner_id, offset=offset, **filters.model_dump())
        return [STask.model_validate(task) for task in tasks]

    async def get_task_by_id(self, task_id: int, owner_id: int):
        task = await self.task_repo.exists(id=task_id)
        if owner_id == task.owner:
            return await self.task_repo.get_by_id(task_id)
        raise AccessUserToTaskError

    async def update_recalculate_overdue_tasks(self) -> int:
        tasks = await self.task_repo.get_all()
        c = 0
        for task in tasks:
            if task.due_date:
                if task.due_date < datetime.now() and task.status != "done":
                    task.status = TaskStatus.overdue
                    updated_task = SUpdatedTask(
                        id = task.id,
                        title = task.title,
                        description = task.description,
                        status = TaskStatus.overdue,
                        due_date = task.due_date
                    )
                    await self.task_repo.update(task_id=task.id, **updated_task.model_dump())
                    c+=1
        return c