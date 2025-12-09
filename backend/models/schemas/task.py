from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.models.static import TaskStatus


class STask(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    title: str
    description: str
    status: TaskStatus
    due_date: Optional[datetime] = None
    owner: int
    created_at: datetime
    updated_at: datetime


class SCreateTask(BaseModel):
    title: str
    description: str
    status: TaskStatus

class SUpdatedTask(BaseModel):
    id: int
    title: str = None
    description: str = None
    status: TaskStatus = None

class SFilterTask(BaseModel):
    status: Optional[TaskStatus] = None
    start_search_date: Optional[datetime] = None
    end_search_date: Optional[datetime] = None
    page: int = 1
    page_size: int = 20