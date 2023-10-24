from fastapi import FastAPI

from .pathfinder import PathFinder


app = FastAPI()
finder = PathFinder()


@app.get("/path")
async def find_path(start: str, end: str):
    """
    Find path from ``start_path`` to ``end_path``.

    :param start: Start URL
    :param end: End URL

    :return: Path list if success.
    """

    print(f"Getting path from {start} to {end}")
    path = await finder.find_path(start, end)

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
