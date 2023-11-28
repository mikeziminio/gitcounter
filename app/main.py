from fastapi import FastAPI
from starlette.responses import HTMLResponse
import services

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def get_all_stat():
    return HTMLResponse(content=services.get_all_stat())


@app.get('/{repo_name}', response_class=HTMLResponse)
async def get_repo_stat(repo_name: str):
    return HTMLResponse(content=services.get_repo_stat(repo_name))
