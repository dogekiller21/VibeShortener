from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import URLCreate, URLResponse, ClickCreate
from src.services import create_url, get_url_by_short_code, create_click
from src.config import settings
from src.database import get_db

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
async def shorten_url(
    url_data: URLCreate,
    db: AsyncSession = Depends(get_db),
):
    url_dto = await create_url(db, url_data)
    if not url_dto:
        raise HTTPException(
            status_code=500,
            detail="Failed to create short URL due to collision. Please try again.",
        )
    
    return URLResponse(
        id=url_dto.id,
        original_url=url_dto.original_url,
        short_code=url_dto.short_code,
        created_at=url_dto.created_at,
        short_url=f"{settings.domain}/{url_dto.short_code}",
    )



