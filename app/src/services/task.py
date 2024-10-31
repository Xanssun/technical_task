from uuid import UUID

from db.postgres import get_session
from fastapi import Depends
from models.entity import Task
from schemas.entity import TaskCreate, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class TaskService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_task(self, task: TaskCreate):
        """Создание новой задачи."""
        db_task = Task(**task.model_dump())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_tasks(self, status: str | None = None):
        """Получение списка задач."""
        query = await self.db.execute(select(Task))
        tasks = query.scalars().all()

        if status:
            tasks = [task for task in tasks if task.status == status]
        return tasks

    async def update_task(self, task_id: UUID, task_update: TaskUpdate):
        """Обновление задачи по идентификатору."""
        query = await self.db.execute(select(Task).where(Task.id == task_id))
        task = query.scalar_one_or_none()

        if task is None:
            return None  # Возврат None для обработки в обработчике

        # Обновляем поля задачи
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: UUID):
        """Удаление задачи по идентификатору."""
        query = await self.db.execute(select(Task).where(Task.id == task_id))
        task = query.scalar_one_or_none()

        if task is None:
            return False  # Возврат False для обработки в обработчике

        await self.db.delete(task)
        await self.db.commit()
        return True 



def get_task_service(
    db_session: AsyncSession = Depends(get_session),
):
    return TaskService(db_session=db_session)
