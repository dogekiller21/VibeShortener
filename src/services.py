import secrets
import string
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import URL, Click
from src.schemas import URLCreate, ClickCreate, URLDTO, ClickDTO, URLStatsDTO
from src.config import settings


def generate_short_code(length: int = 8) -> str:
    """Generate a random short code."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


async def create_url(db: AsyncSession, url_data: URLCreate) -> URLDTO | None:
    """Create a new shortened URL."""
    # Generate unique short code with retry limit
    max_retries = 100
    for attempt in range(max_retries):
        short_code = generate_short_code()
        result = await db.execute(select(URL).where(URL.short_code == short_code))
        existing_url = result.scalar_one_or_none()
        if not existing_url:
            break
    else:
        # If we've exhausted all retries, return None
        return None

    db_url = URL(
        original_url=str(url_data.original_url),
        short_code=short_code,
    )
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    
    return URLDTO(
        id=db_url.id,
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        created_at=db_url.created_at,
    )


async def get_url_by_short_code(db: AsyncSession, short_code: str) -> URLDTO | None:
    """Get URL by short code."""
    stmt = select(URL).where(URL.short_code == short_code)
    result = await db.execute(stmt)
    url = result.scalar_one_or_none()
    
    if not url:
        return None
    
    return URLDTO(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        created_at=url.created_at,
    )


async def create_click(db: AsyncSession, click_data: ClickCreate) -> ClickDTO:
    """Create a new click record."""
    db_click = Click(**click_data.model_dump())
    db.add(db_click)
    await db.commit()
    await db.refresh(db_click)
    
    return ClickDTO(
        id=db_click.id,
        url_id=db_click.url_id,
        ip_address=db_click.ip_address,
        user_agent=db_click.user_agent,
        referer=db_click.referer,
        created_at=db_click.created_at,
    )


async def get_url_stats(db: AsyncSession, short_code: str) -> URLStatsDTO | None:
    """Get statistics for a URL."""
    url = await get_url_by_short_code(db, short_code)
    if not url:
        return None

    # Get total clicks
    result = await db.execute(
        select(func.count(Click.id)).where(Click.url_id == url.id)
    )
    total_clicks = result.scalar()

    # Get last click
    result = await db.execute(
        select(Click)
        .where(Click.url_id == url.id)
        .order_by(Click.created_at.desc())
        .limit(1)
    )
    last_click = result.scalar_one_or_none()

    # Generate short URL using settings
    protocol = "https" if settings.environment == "production" else "http"
    short_url = f"{protocol}://{settings.domain}/{url.short_code}"

    return URLStatsDTO(
        url_id=url.id,
        short_code=url.short_code,
        original_url=url.original_url,
        short_url=short_url,
        total_clicks=total_clicks,
        created_at=url.created_at,
        last_click=last_click.created_at if last_click else None,
    )
