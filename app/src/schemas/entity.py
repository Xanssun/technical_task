from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Схема для создания нового пользователя"""
    username: str
    password: str


class UserInDB(BaseModel):
    """Схема для представления пользователя в базе данных"""
    id: UUID
    username: str

    class Config:
        from_attributes = True


class UserSignIn(BaseModel):
    """Схема для аутентификации пользователя"""
    username: str
    password: str


class Result(BaseModel):
    """Схема для ответа сервера"""
    success: bool


class TaskStatus(str, Enum):
    """Статус задачи."""
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(BaseModel):
    """Базовая Схема задачи, содержащая общие поля."""
    title: str
    description: str | None = None
    status: TaskStatus


class TaskCreate(BaseModel):
    """Схема для создания новой задачи."""
    title: str
    description: str | None = None


class TaskUpdate(TaskBase):
    """Схема для обновления существующей задачи."""
    pass


class Task(TaskBase):
    """Схема для представления тасок в базе данных"""
    id: UUID
    # user_id: UUID

    class Config:
        from_attributes = True
