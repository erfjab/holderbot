"""
Database models for the application.

This module defines the SQLAlchemy models for the tokens and settings.
"""

from datetime import datetime
from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base


class Token(Base):
    """Model representing a token."""

    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now, nullable=True
    )


class Setting(Base):
    """Model representing a setting."""

    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(256), primary_key=True)
    value: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now, nullable=True
    )
