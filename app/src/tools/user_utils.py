from typing import Union
from uuid import UUID

from models.entity import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_username(db_session: AsyncSession, username: str) -> Union[User, None]:
    """Получаем пользователя по usermame"""
    statement = select(User).where(User.username == username)
    query = await db_session.execute(statement)
    return query.scalars().first()

async def get_user_by_id(db_session: AsyncSession, id: UUID) -> User:
    """Получаем пользователя по id"""
    statement = select(User).where(User.id == id)
    query = await db_session.execute(statement)
    return query.scalars().first()
