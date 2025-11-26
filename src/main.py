import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.di.container import container

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ЗАПУСК ПРИЛОЖЕНИЯ...")
    yield
    logger.info("ЗАВЕРШЕНИЕ ПРИЛОЖЕНИЯ...")


app = FastAPI(
    title="Сервис сокращение ссылок",
    description="Сервис по сокращению URL-адресов",
    version="1.0.0",
    lifespan=lifespan
)
setup_dishka(container=container, app=app)


@app.get("/")
def root():
    return {"message": "Сокращение ссылок"}


if __name__ == "__main__":
    uvicorn.run('src.main:app', host="0.0.0.0", port=8000, reload=True)
