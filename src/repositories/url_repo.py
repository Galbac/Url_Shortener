from typing import Optional, Any, Coroutine

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.url import URL
import logging

logging = logging.getLogger(__name__)


class URLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, original_url: str, short_url: str) -> URL:
        url = URL(original_url=original_url, short_url=short_url)
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)
        return url

    async def get_by_short_code(self, short_code: str) -> Optional[URL]:
        stmt = select(URL).where(URL.short_url == short_code)
        result = await self.session.execute(stmt)
        url_obj = result.scalar_one_or_none()

        return url_obj

    async def update_click_count_by_one(self, original_url: str) -> URL | None:
        stmt = select(URL).where(URL.original_url==original_url)
        result =  await self.session.execute(stmt)
        url_obj = result.scalar_one_or_none()

        if url_obj:
            url_obj.click_count += 1
            await self.session.commit()
            await self.session.refresh(url_obj)
            logging.info(f'URL уже имеется в базе данных, увеличиваем счетчик кликов на 1 = {url_obj.click_count}')
            logging.info('Оригинальный URL уже имеется в БД')
            return url_obj
        return None


