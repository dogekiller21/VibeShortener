import secrets
import string
from datetime import datetime, timedelta
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import URL, Click
from src.schemas import (
    URLCreate,
    ClickCreate,
    URLDTO,
    ClickDTO,
    URLStatsDTO,
    DetailedURLStats,
)
from src.config import settings
from src.geolocation import geolocation_service


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


async def get_url_detailed_stats(
    db: AsyncSession, short_code: str
) -> DetailedURLStats | None:
    """Get detailed statistics with chart data for a URL."""
    url = await get_url_by_short_code(db, short_code)
    if not url:
        return None

    # Get basic stats
    result = await db.execute(
        select(func.count(Click.id)).where(Click.url_id == url.id)
    )
    total_clicks = result.scalar()

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

    # Get daily clicks for last 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    daily_clicks_query = text("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as clicks
        FROM clicks 
        WHERE url_id = :url_id 
        AND created_at >= :seven_days_ago
        GROUP BY DATE(created_at)
        ORDER BY date
    """)

    result = await db.execute(
        daily_clicks_query, {"url_id": url.id, "seven_days_ago": seven_days_ago}
    )
    daily_clicks = [{"date": str(row.date), "clicks": row.clicks} for row in result]

    # Get hourly distribution
    hourly_query = text("""
        SELECT 
            EXTRACT(HOUR FROM created_at) as hour,
            COUNT(*) as clicks
        FROM clicks 
        WHERE url_id = :url_id
        GROUP BY EXTRACT(HOUR FROM created_at)
        ORDER BY hour
    """)

    result = await db.execute(hourly_query, {"url_id": url.id})
    hourly_distribution = [
        {"hour": int(row.hour), "clicks": row.clicks} for row in result
    ]

    # Get top referers
    referer_query = text("""
        SELECT 
            referer,
            COUNT(*) as clicks
        FROM clicks 
        WHERE url_id = :url_id 
        AND referer IS NOT NULL 
        AND referer != ''
        GROUP BY referer
        ORDER BY clicks DESC
        LIMIT 10
    """)

    result = await db.execute(referer_query, {"url_id": url.id})
    top_referers = [{"referer": row.referer, "clicks": row.clicks} for row in result]

    # Get top user agents
    user_agent_query = text("""
        SELECT 
            user_agent,
            COUNT(*) as clicks
        FROM clicks 
        WHERE url_id = :url_id 
        AND user_agent IS NOT NULL 
        AND user_agent != ''
        GROUP BY user_agent
        ORDER BY clicks DESC
        LIMIT 10
    """)

    result = await db.execute(user_agent_query, {"url_id": url.id})
    top_user_agents = [
        {"user_agent": row.user_agent, "clicks": row.clicks} for row in result
    ]

    # Get regional clicks with real geolocation
    regional_query = text("""
        SELECT 
            ip_address,
            COUNT(*) as clicks
        FROM clicks 
        WHERE url_id = :url_id 
        AND ip_address IS NOT NULL 
        AND ip_address != ''
        GROUP BY ip_address
        ORDER BY clicks DESC
        LIMIT 20
    """)

    result = await db.execute(regional_query, {"url_id": url.id})
    regional_clicks = []

    # Используем реальную геолокацию для каждого IP
    for row in result:
        ip = row.ip_address
        if ip:
            # Получаем реальную геолокацию
            location = await geolocation_service.get_location(ip)

            regional_clicks.append(
                {
                    "country": location.get("country", "Неизвестно"),
                    "region": location.get("region", "Неизвестно"),
                    "city": location.get("city", "Неизвестно"),
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                    "clicks": row.clicks,
                    "ip": ip,
                }
            )

    return DetailedURLStats(
        url_id=url.id,
        short_code=url.short_code,
        original_url=url.original_url,
        short_url=short_url,
        total_clicks=total_clicks,
        created_at=url.created_at,
        last_click=last_click.created_at if last_click else None,
        daily_clicks=daily_clicks,
        hourly_distribution=hourly_distribution,
        top_referers=top_referers,
        top_user_agents=top_user_agents,
        regional_clicks=regional_clicks,
    )
