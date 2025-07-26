from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ClickCreate
from src.services import get_url_by_short_code, create_click
from src.database import get_db

router = APIRouter()


@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    url_dto = await get_url_by_short_code(db, short_code)
    if not url_dto:
        raise HTTPException(status_code=404, detail="URL not found")
    
    click_data = ClickCreate(
        url_id=url_dto.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer"),
    )
    await create_click(db, click_data)
    return RedirectResponse(url_dto.original_url) 