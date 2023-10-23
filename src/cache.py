import os
from abc import ABC, abstractmethod
from typing import NamedTuple, Self, Optional
from urllib.parse import urlparse

from redis.asyncio import Redis


class WikiPage(NamedTuple):
    namespace: str
    page: str

    @classmethod
    def from_full_url(cls, url: str) -> Self:
        parsed = urlparse(url)
        namespace = parsed.hostname.split(".", 1)[0]
        page = parsed.path.replace("/wiki/", "")

        return cls(namespace, page)

    @property
    def full_url(self):
        return f"https://{self.namespace}.wikipedia.org/wiki/{self.page}"


class AbstractCache(ABC):
    @abstractmethod
    def get(self, page: WikiPage) -> set[WikiPage] | None:
        ...

    @abstractmethod
    def save(self, page: WikiPage, children: set[WikiPage]) -> None:
        ...


class RedisCache(AbstractCache):
    _KEY_PATTERN = "{page.namespace}:{page.page}"

    def __init__(self):
        self._host = os.getenv("REDIS_HOST", "localhost")
        self._port = int(os.getenv("REDIS_PORT", "6379"))
        self._db = int(os.getenv("REDIS_DB", "0"))

        self._redis = Redis(host=self._host, port=self._port, db=self._db, decode_responses=True)

    async def get(self, page: WikiPage) -> set[WikiPage] | None:
        key = self._KEY_PATTERN.format(page=page)
        raw_children = await self._redis.smembers(key)
        return {WikiPage(*raw_page.split(":", 1)) for raw_page in raw_children}

    async def save(self, page: WikiPage, children: set[WikiPage]) -> None:
        key = self._KEY_PATTERN.format(page=page)
        current_members = await self._redis.smembers(key)
        if current_members:
            await self._redis.delete(key)

        raw_children = {self._KEY_PATTERN.format(page=child) for child in children}
        await self._redis.sadd(key, *raw_children)
