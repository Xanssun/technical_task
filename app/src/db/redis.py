from abc import ABC, abstractmethod
from typing import Optional

from redis.asyncio import Redis

# Глобальная переменная для объекта Redis
redis: Optional[Redis] = None

async def get_redis() -> Redis:
    if redis is None:
        raise ValueError("Cache storage (tokens_cache) не инициализирован")
    return redis

class AsyncCacheStorage(ABC):
    """Абстрактный базовый класс для кэширования с использованием Redis"""
    @abstractmethod
    async def get(self, key: str, **kwargs):
        """Получает значение по ключу из кэша"""
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        """Устанавливает значение в кэш с указанным временем истечения"""
        pass
