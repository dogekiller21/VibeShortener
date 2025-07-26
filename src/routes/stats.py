from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import URLStats
from src.services import get_url_stats
from src.database import get_db

router = APIRouter()


@router.get("/stats/{short_code}", response_model=URLStats)
async def get_url_statistics(
    short_code: str,
    db: AsyncSession = Depends(get_db),
):
    stats_dto = await get_url_stats(db, short_code)
    if not stats_dto:
        raise HTTPException(status_code=404, detail="URL not found")
    return stats_dto
