import os
import re
from abc import ABC, abstractmethod
from typing import NamedTuple
from urllib import parse
from urllib.parse import urlparse

from redis.asyncio import Redis

from src.exc import BadUrlError

_WIKI_URL_RE = re.compile(r"^(https://|http://)?"
                          r"[a-z]+\.(m\.)?wikipedia\.org"
                          r"/wiki/.+$")


class WikiPage(NamedTuple):
    namespace: str
    page: str

    @staticmethod
    def from_full_url(url: str) -> "WikiPage":
        if not _WIKI_URL_RE.match(url):
            raise BadUrlError(f"URL does not match wiki url")

        parsed = urlparse(parse.unquote_plus(url))
        namespace = parsed.hostname.split(".", 1)[0]
        page = parsed.path.replace("/wiki/", "")

        return WikiPage(namespace, page)

    @property
    def full_url(self):
        return f"https://{self.namespace}.wikipedia.org/wiki/{self.page}"


class RedisCache:
    _KEY_PATTERN = "{page.namespace}:{page.page}"

    def __init__(self):
        self._host = os.getenv("REDIS_HOST", "localhost")
        self._port = int(os.getenv("REDIS_PORT", "6379"))
        self._db = int(os.getenv("REDIS_DB", "0"))

        self._redis = Redis(host=self._host, port=self._port, db=self._db, decode_responses=True)

    async def get(self, page: WikiPage) -> set[WikiPage] | None:
        key = self._KEY_PATTERN.format(page=page)

        return {
            WikiPage(*raw_page.split(":"))
            for raw_page in await self._redis.smembers(key)
        }

    async def save(self, page: WikiPage, children: set[WikiPage]) -> None:
        key = self._KEY_PATTERN.format(page=page)

        await self._redis.delete(key)

        raw_children = {self._KEY_PATTERN.format(page=child) for child in children}
        await self._redis.sadd(key, *raw_children)
