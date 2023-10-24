from fastapi import FastAPI

from .cache import WikiPage
from .pathfinder import PathFinder

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
finder = PathFinder()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/path_by_urls")
async def find_path_by_urls(start: str, end: str):
    """
    Find path from ``start_path`` to ``end_path``.

    :param start: Start URL.
    :param end: End URL.

    :return: Path list if success.
    """

    start_page = WikiPage.from_full_url(start)
    end_page = WikiPage.from_full_url(end)

    print(f"Getting path from {start_page} to {end_page}")
    path = await finder.find_path(start_page, end_page)

    return {"path": path}


@app.get("/path_by_names")
async def find_path_by_names(namespace: str, start: str, end: str):
    """
    Find path from ``start_path`` to ``end_path``.

    :param namespace: Article language (en, ru, etc.).
    :param start: Start name.
    :param end: End name.

    :return: Path list if success.
    """

    start_page = WikiPage(namespace, start.strip())
    end_page = WikiPage(namespace, end.strip())

    print(f"Getting path from {start_page} to {end_page}")
    path = await finder.find_path(start_page, end_page)

    return {"path": path}


@app.get("/explore")
async def explore(start: str, count: int = 10000):
    """
    Explore URLs from start URL.

    :param start: Start URL.
    :param count: Seen URLs count limit.
    """

    await finder.explore(start, count)
    return {"result": "success"}
