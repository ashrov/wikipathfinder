import re
from dataclasses import dataclass, field
from queue import Queue
from urllib import parse

from aiohttp import request

from src.cache import RedisCache, WikiPage
from src.exc import BadUrlError

_WIKI_URL_RE = re.compile(r'href="/wiki/([^:#"]+)"')


@dataclass
class PathCache:
    visited_pages: set[WikiPage] = field(default_factory=set)
    not_visited_pages: Queue[WikiPage] = field(default_factory=Queue)
    paths: dict[WikiPage, WikiPage] = field(default_factory=dict)


class PathFinder:
    def __init__(self):
        self._cache = RedisCache()

    async def find_path(self, start: str, end: str) -> list[str]:
        path_cache = PathCache()

        path_cache.not_visited_pages.put(await self._get_actual_page_info(start))
        while not path_cache.not_visited_pages.empty():
            current = path_cache.not_visited_pages.get()
            children = await self.get_children(current)

            for child in children:
                if child.full_url == end:
                    return self._restore_path(path_cache, start, end)

                if child not in path_cache.visited_pages:
                    path_cache.visited_pages.add(child)
                    path_cache.not_visited_pages.put(child)
                    path_cache.paths[child] = current

    def _restore_path(self, path_cache: PathCache, start: str, end: str) -> list[str]:
        current = WikiPage.from_full_url(end)
        path: list[str] = [end]

        while current != WikiPage.from_full_url(start):
            current = path_cache.paths[current]
            path.insert(0, current.full_url)

        return path

    async def get_children(self, page: WikiPage) -> set[WikiPage]:
        if cached := await self._cache.get(page):
            return cached

        async with request("GET", page.full_url) as response:
            response_text = await response.text()

        children = {
            WikiPage(page.namespace, parse.unquote_plus(href).replace("/wiki/", ""))
            for href in _WIKI_URL_RE.findall(response_text)
        }

        await self._cache.save(page, children)

        return children

    async def _get_actual_page_info(self, url: str) -> WikiPage:
        async with request("GET", url) as response:
            if "no article" in await response.text():
                raise BadUrlError(f"No article at '{url}'")

            return WikiPage.from_full_url(parse.unquote_plus(url))
