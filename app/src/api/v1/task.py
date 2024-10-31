from http import HTTPStatus
from uuid import UUID

from core.tokens import security_access_token
from fastapi import APIRouter, Depends, HTTPException
from schemas.entity import Task, TaskCreate, TaskUpdate
from services.task import TaskService, get_task_service

router = APIRouter()

@router.post(
    "/tasks",
    response_model=Task,
    status_code=HTTPStatus.CREATED,
    summary='Создание новой задачи',
    description='Создает новую задачу.',
    dependencies=[Depends(security_access_token)]
)
async def create_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.create_task(task)

@router.get(
    "/tasks",
    response_model=list[Task],
    status_code=HTTPStatus.OK,
    summary='Получение списка задач',
    description='Возвращает список всех задач с возможностью фильтрации по статусу.',
    # dependencies=[Depends(security_access_token)]
)
async def get_tasks(
    status: str | None = None,
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_tasks(status)

@router.put(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=HTTPStatus.OK,
    summary='Обновление задачи',
    description='Обновляет данные задачи',
    dependencies=[Depends(security_access_token)]
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    task = await task_service.update_task(task_id, task_data)
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete(
    "/tasks/{task_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary='Удаление задачи',
    description='Удаляет задачу по её ID',
    dependencies=[Depends(security_access_token)]
)
async def delete_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    success = await task_service.delete_task(task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
