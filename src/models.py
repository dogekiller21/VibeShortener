from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import DateTime, Integer, String, Text, ForeignKey, func
from sqlalchemy.orm import mapped_column, relationship

from src.database import Base


class ServerDefaults(Enum):
    """Server-side default values."""

    UTC_NOW = func.timezone("UTC", func.now())


class URL(Base):
    """URL model for storing shortened URLs."""

    __tablename__ = "urls"

    id = mapped_column(Integer, primary_key=True, index=True)
    original_url = mapped_column(Text, nullable=False)
    short_code = mapped_column(String(20), unique=True, index=True, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=ServerDefaults.UTC_NOW.value,
        nullable=False,
    )

    # Relationship
    clicks = relationship("Click", back_populates="url", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<URL(id={self.id}, short_code='{self.short_code}')>"


class Click(Base):
    """Click model for storing URL click metrics."""

    __tablename__ = "clicks"

    id = mapped_column(Integer, primary_key=True, index=True)
    url_id = mapped_column(Integer, ForeignKey("urls.id"), nullable=False, index=True)
    ip_address = mapped_column(String(45), nullable=True)  # IPv6 compatible
    user_agent = mapped_column(Text, nullable=True)
    referer = mapped_column(Text, nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=ServerDefaults.UTC_NOW.value,
        nullable=False,
        index=True,
    )

    # Relationship
    url = relationship("URL", back_populates="clicks")

    def __repr__(self):
        return f"<Click(id={self.id}, url_id={self.url_id})>"
