from datetime import datetime
from uuid import UUID

from db.postgres import get_session
from db.redis import AsyncCacheStorage, get_redis
from fastapi import Depends, HTTPException
from models.entity import RefreshToken, Token, User
from schemas.entity import UserCreate, UserSignIn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tools.user_utils import get_user_by_id, get_user_by_username


class AuthService():
    def __init__(self, db_session: AsyncSession, tokens_cache: AsyncCacheStorage):
        self.db_session = db_session
        self.tokens_cache = tokens_cache

    async def signup(self, user_create: UserCreate):
        """Регистрация нового пользователя"""
        exists_user = await get_user_by_username(self.db_session, user_create.username)
        if not exists_user:
            user = User(**user_create.model_dump())
            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            
            return user
    
    
    async def signin(self, user_signin: UserSignIn, check_pass):
        """Авторизация"""
        user = await get_user_by_username(self.db_session, user_signin.username)
        if user:
            password_ok = user.check_password(user_signin.password)
            if (password_ok and check_pass) or not check_pass:
                user_id = user.id

                refresh_token = await self._create_refresh_token(user_id=user_id)
                token = Token(user_id=user_id)

                return {
                    'user': user,
                    'token': token.token,
                    'refresh_token': refresh_token.refresh_token,
                    'expires': refresh_token.expires.strftime(
                        '%Y-%m-%d %H:%M:%S'
                    ),
                }

    async def refresh_token(self, refresh_token: RefreshToken) -> dict:
        """Обновление рефреш токена"""
        user = await get_user_by_id(self.db_session, refresh_token.user_id)
        if user:
            new_refresh_token = await self._renew_refresh_token(
                refresh_token=refresh_token
            )
  
            token = Token(user_id=user.id)
            return {
                'user': user,
                'token': token.token,
                'refresh_token': new_refresh_token.refresh_token,
                'expires': new_refresh_token.expires.strftime(
                    '%Y-%m-%d %H:%M:%S'
                ),
            }
        
    async def logout(self, refresh_token: RefreshToken) -> bool:
        """Выход"""
        await self._get_revoked_refresh_token_from_cache(
            refresh_token.refresh_token
        )    

        await self._put_revoked_refresh_token_to_cache(
            refresh_token.refresh_token
        )

        return True
    
    async def get_refresh_token(
        self, refresh_token: str
    ):
        """Проверяем рефреш токен, что нет в отозванных и что вообще такой есть"""
        is_revoked = await self._get_revoked_refresh_token_from_cache(
            refresh_token
        )
        if is_revoked:
            return None

        statement = select(RefreshToken).where(
            RefreshToken.refresh_token == refresh_token,
            RefreshToken.expires >= datetime.now(),
        )
        query = await self.db_session.execute(statement)
        return query.scalars().first()

    async def _put_revoked_refresh_token_to_cache(
        self, refresh_token: str
    ) -> None:
        """Сохраняем рефреш токен в кеш как отозваный"""
        await self.tokens_cache.set(refresh_token, '1')

    async def _get_revoked_refresh_token_from_cache(
        self, refresh_token: str
    ) -> bool:
        """Проверяем есть ли такой отозванный рефреш токен"""
        data = await self.tokens_cache.get(refresh_token)
        if data:
            return True
        return False

    async def _create_refresh_token(self, user_id: UUID) -> RefreshToken:
        """Создаем новый refresh_token"""
        refresh_token = RefreshToken(user_id=user_id)
        refresh_token.regenerate()
        self.db_session.add(refresh_token)
        await self.db_session.commit()
        await self.db_session.refresh(refresh_token)
        return refresh_token
    
    async def _renew_refresh_token(
        self, refresh_token: RefreshToken
    ) -> RefreshToken:
        """Обновление токена (замена существующего)"""
        refresh_token.regenerate()
        await self.db_session.commit()
        await self.db_session.refresh(refresh_token)
        return refresh_token


def get_auth_service(
    db_session: AsyncSession = Depends(get_session),
    tokens_cache: AsyncCacheStorage = Depends(get_redis),
):
    return AuthService(db_session=db_session, tokens_cache=tokens_cache)
