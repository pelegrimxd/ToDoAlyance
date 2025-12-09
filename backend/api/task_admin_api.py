from typing import Annotated

from fastapi import APIRouter, HTTPException, Header
from fastapi.params import Depends
from starlette import status
from starlette.requests import Request
from backend.dependencies import task_manager
from backend.models.schemas.task import STask, SCreateTask, SFilterTask, SUpdatedTask

router = APIRouter(prefix="", tags=["tasks_admin"])

@router.post("/update_recalculate_overdue_tasks")
async def update_tasks() -> int:
    return await task_manager.update_recalculate_overdue_tasks()

