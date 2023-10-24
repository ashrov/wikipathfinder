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

    async def explore(self, start: str, count: int):
        path_cache = PathCache()

        start_page = await self._get_actual_page_info(start)
        print(f"Exploring urls from {start_page}. Limit: {count}")
        path_cache.not_visited_pages.put(start_page)
        while (not path_cache.not_visited_pages.empty() and
               len(path_cache.visited_pages) - path_cache.not_visited_pages.qsize() < count):
            current = path_cache.not_visited_pages.get()
            children = await self.get_children(current)

            for child in children:
                if child not in path_cache.visited_pages:
                    path_cache.visited_pages.add(child)
                    path_cache.not_visited_pages.put(child)

    async def find_path(self, start: str, end: str) -> list[str]:
        path_cache = PathCache()
        start_page = await self._get_actual_page_info(start)
        end_page = await self._get_actual_page_info(end)

        path_cache.not_visited_pages.put(start_page)
        while not path_cache.not_visited_pages.empty():
            current = path_cache.not_visited_pages.get()
            children = await self.get_children(current)

            for child in children:
                if child not in path_cache.visited_pages:
                    path_cache.visited_pages.add(child)
                    path_cache.not_visited_pages.put(child)
                    path_cache.paths[child] = current

                if child == end_page:
                    return self._restore_path(path_cache, start_page, end_page)

    def _restore_path(self, path_cache: PathCache, start: WikiPage, end: WikiPage) -> list[str]:
        path: list[str] = [end.full_url]
        current = end
        print(f"Finding path between {end} and {start}")
        while current != start:
            current = path_cache.paths.get(current)
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
