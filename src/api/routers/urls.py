from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter
from fastapi import HTTPException, status
from starlette.responses import RedirectResponse

from src.schemas.url import URLResponse, URLCreate
from src.services.url_service import URLService

router = APIRouter(prefix='/api/urls', tags=['urls'])


@router.post('/shorten', response_model=URLResponse)
@inject
async def shorten_url(
        url_create: URLCreate,
        service: FromDishka[URLService]
):
    try:
        short_code = await service.shorten_url(url_create.original_url)
        return URLResponse(short_code=short_code)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/{short_code}')
@inject
async def get_url(
        short_code: str,
        service: FromDishka[URLService]
):
    original = await service.get_original_url(short_code)
    if not original:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='URL не найден')
    return RedirectResponse(url=original)
