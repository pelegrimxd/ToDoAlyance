from datetime import datetime
from enum import Enum
from typing import Optional, Type
from sqlalchemy import select, update, delete, Sequence
from sqlalchemy.ext.asyncio import async_sessionmaker
from backend.models.db_models.task import Task
from backend.models.schemas.task import STask
from backend.models.static import TaskStatus
from backend.services.infrastructure.task_database.task_database_interface import ITaskRepository


class TaskRepository(ITaskRepository):

    def __init__(self, model: Type[Task], session_maker: async_sessionmaker):
        self.model = model
        self.session_maker = session_maker

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        async with self.session_maker() as session:
            result = await session.execute(
                select(self.model).where(self.model.id == task_id)
            )
            return result.scalar_one_or_none()

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
        async with self.session_maker() as session:
            query = select(self.model)
            if owner_id:
                query = query.where(self.model.owner == owner_id)
            if status:
                query = query.where(self.model.status == status)
            if start_search_date:
                query = query.where(self.model.due_date >= start_search_date)
            if end_search_date:
                query = query.where(self.model.due_date <= end_search_date)

            query = query.order_by(self.model.created_at.desc())
            query = query.offset(offset).limit(page_size)
            result = await session.execute(query)
            tasks = result.scalars().all()

            return [task for task in tasks]

    async def create(self, **values) -> Task:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    instance = self.model(**values)
                    session.add(instance)
                    await session.commit()
                    return instance
                except Exception as e:
                    await session.rollback()
                    raise e

    async def update(self, task_id: int, **values) -> Optional[Task]:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    new_task = (
                        update(self.model)
                        .where(self.model.id == task_id)
                        .values(**values)
                        .returning(self.model)
                    )
                    result = await session.execute(new_task)
                    await session.commit()
                    return result.scalar_one_or_none()
                except Exception as e:
                    await session.rollback()
                    raise e


    async def delete(self, task_id: int) -> bool:
        async with self.session_maker() as session:
            async with session.begin():
                try:
                    deleted_task = delete(self.model).where(self.model.id == task_id)
                    result = await session.execute(deleted_task)
                    await session.commit()
                    return result.rowcount
                except Exception as e:
                    await session.rollback()
                    raise e


    async def exists(self, **filters) -> Optional[Task]:
        async with self.session_maker() as session:
            query = select(self.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().one_or_none()