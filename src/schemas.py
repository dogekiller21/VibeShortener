from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class URLBase(BaseModel):
    """Base URL schema."""

    original_url: HttpUrl


class URLCreate(URLBase):
    """Schema for creating a new URL."""

    pass


class URLResponse(URLBase):
    """Schema for URL response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    short_code: str
    created_at: datetime
    short_url: str


class URLDTO(BaseModel):
    """DTO for URL objects returned from services."""

    id: int
    original_url: str
    short_code: str
    created_at: datetime


class ClickBase(BaseModel):
    """Base click schema."""

    pass


class ClickCreate(ClickBase):
    """Schema for creating a new click."""

    url_id: int
    ip_address: str | None = None
    user_agent: str | None = None
    referer: str | None = None


class ClickDTO(BaseModel):
    """DTO for Click objects returned from services."""

    id: int
    url_id: int
    ip_address: str | None
    user_agent: str | None
    referer: str | None
    created_at: datetime


class ClickResponse(ClickBase):
    """Schema for click response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    url_id: int
    ip_address: str | None
    user_agent: str | None
    referer: str | None
    created_at: datetime


class URLStatsDTO(BaseModel):
    """DTO for URL statistics returned from services."""

    url_id: int
    short_code: str
    original_url: str
    short_url: str
    total_clicks: int
    created_at: datetime
    last_click: datetime | None = None


class URLStats(BaseModel):
    """Schema for URL statistics API response."""

    model_config = ConfigDict(from_attributes=True)

    url_id: int
    short_code: str
    original_url: str
    short_url: str
    total_clicks: int
    created_at: datetime
    last_click: datetime | None = None
