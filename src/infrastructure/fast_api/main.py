from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

from src.infrastructure.fast_api.views.order import listen_create_queue, router as orders_router


@asynccontextmanager
async def start_background_task():
    background_tasks = BackgroundTasks()
    listen_create_queue(background_tasks)
    yield background_tasks

app = FastAPI()
app.include_router(orders_router, prefix="/orders", tags=["Orders"])

@app.on_event("startup")
async def startup_event():
    async with start_background_task() as bg_tasks:
        pass
