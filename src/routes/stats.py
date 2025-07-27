from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import URLStats
from src.services import get_url_stats, get_url_detailed_stats
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


@router.get("/stats/{short_code}/detailed")
async def get_url_detailed_statistics(
    short_code: str,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed statistics with chart data."""
    detailed_stats = await get_url_detailed_stats(db, short_code)
    if not detailed_stats:
        raise HTTPException(status_code=404, detail="URL not found")
    return detailed_stats
