import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.api.routers.urls import router as urls_router
from src.di.container import container

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ЗАПУСК ПРИЛОЖЕНИЯ...")
    yield
    container.close()
    logger.info("ЗАВЕРШЕНИЕ ПРИЛОЖЕНИЯ...")


app = FastAPI(
    title="Сервис сокращение ссылок",
    description="Сервис по сокращению URL-адресов",
    version="1.0.0",
    lifespan=lifespan
)
setup_dishka(container=container, app=app)

app.include_router(urls_router)

app.mount("/", StaticFiles(directory="frontend/static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run('src.main:app', host="0.0.0.0", port=8000, reload=True)
