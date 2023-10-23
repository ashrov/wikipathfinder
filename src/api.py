from fastapi import FastAPI

from .pathfinder import PathFinder


app = FastAPI()
finder = PathFinder()


@app.get("/path")
async def get_path(start_path: str, end_path: str):
    print(f"Getting path from {start_path} to {end_path}")
    path = await finder.find_path(start_path, end_path)

    return {"path": path}
