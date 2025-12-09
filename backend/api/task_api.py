from typing import Annotated

from fastapi import APIRouter, HTTPException, Header
from fastapi.params import Depends
from starlette import status
from starlette.requests import Request
from backend.dependencies import task_manager
from backend.models.schemas.task import STask, SCreateTask, SFilterTask, SUpdatedTask

router = APIRouter(prefix="", tags=["tasks"])


def get_user_id(
        x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None
) -> int:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ожидается заголовок X-User-Id"
        )

    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-User-Id должен быть валидным числом"
        )

@router.post("/create")
async def create_task(
    new_task: SCreateTask,
    owner_id: Annotated[int, Depends(get_user_id)],
) -> STask:
    return await task_manager.create_task(owner_id=owner_id, new_task=new_task)

@router.post("/get_all")
async def get_tasks(
        filters: SFilterTask,
        owner_id: Annotated[int, Depends(get_user_id)],
) -> list[STask]:
    return await task_manager.get_tasks(owner_id=owner_id, filters=filters)

@router.get("/get_by_id")
async def get_task(
        task_id: int,
        owner_id: Annotated[int, Depends(get_user_id)],
) -> STask:
    return await task_manager.get_task_by_id(owner_id=owner_id, task_id=task_id)

@router.put("/update")
async def update_task(
        updated_task: SUpdatedTask,
        owner_id: Annotated[int, Depends(get_user_id)],
) -> STask:
    return await task_manager.update_task(owner_id=owner_id, update_task=updated_task)

@router.delete("/delete")
async def delete_task(
        task_id: int,
        owner_id: Annotated[int, Depends(get_user_id)],
) -> bool:
    return await task_manager.delete_task(owner_id=owner_id, task_id=task_id)