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
    CANONICAL_RE = re.compile(r"<link rel=\"canonical\" href=\"(?P<true_url>[^\"]+)\">")
    YEAR_RE = re.compile(r"\d{4}(_.+)?")

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

    async def find_path(self, start: WikiPage, end: WikiPage) -> list[str]:
        if not start.page or not end.page:
            raise BadUrlError("Empty page")

        start_page: WikiPage = await self._get_actual_page_info(start.full_url)
        end_page: WikiPage = await self._get_actual_page_info(end.full_url)

        if start == end:
            raise BadUrlError("Equal start and end pages are not allowed")

        print(f"Getting path between validated urls {start_page} - {end_page}")

        path_cache = PathCache()
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
        print(f"Restoring path between {start} and {end}")
        while current != start:
            current = path_cache.paths.get(current)
            path.insert(0, current.full_url)

        return path

    async def get_children(self, page: WikiPage) -> set[WikiPage]:
        children = await self._cache.get(page)

        if not children:
            async with request("GET", page.full_url) as response:
                response_text = await response.text()

            children = {
                WikiPage(page.namespace, parse.unquote_plus(href).replace("/wiki/", ""))
                for href in _WIKI_URL_RE.findall(response_text)
            }
            await self._cache.save(page, children)

        children = {child for child in children if not self.YEAR_RE.match(child.page)}

        return children

    async def _get_actual_page_info(self, url: str) -> WikiPage:
        async with request("GET", url) as response:
            if "noarticle" in await response.text():
                raise BadUrlError(f"No article at '{url}'")

            text = await response.text()
            true_url = self.CANONICAL_RE.findall(text)
            if true_url and true_url[0]:
                return WikiPage.from_full_url(parse.unquote_plus(true_url[0]))
            else:
                raise BadUrlError(f"Cannot get wiki article for URL '{url}'")
