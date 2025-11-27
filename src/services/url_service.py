import secrets
import string

from src.repositories.url_repo import URLRepository
from src.utils.utils import is_valid_url


def _generate_short_code() -> str:
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))


class URLService:
    def __init__(self, repo: URLRepository):
        self.repo = repo

    async def shorten_url(self, original_url: str) -> str:
        if not is_valid_url(original_url):
            raise ValueError("Неправильный URL")

        existing_url = await self.repo.update_click_count_by_one(original_url)
        if existing_url:
            return existing_url.short_url

        short_code = _generate_short_code()

        existing_url = await self.repo.get_by_short_url(short_code)
        if existing_url:
            raise ValueError("Короткий URL уже существует")

        await self.repo.create(original_url, short_code)
        return short_code

    async def get_original_url(self, short_code: str) -> str:
        url_obj = await self.repo.get_by_short_code(short_code)
        if url_obj:
            return url_obj.original_url
        return None
