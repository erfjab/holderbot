"""
Database models for the application.

This module defines the SQLAlchemy models for the tokens and settings.
"""

from datetime import datetime
from sqlalchemy import Integer, DateTime, String, Boolean, JSON
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
    """
    Model representing application settings.
    Only one record should exist in this table at any time.
    """

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    node_monitoring: Mapped[bool] = mapped_column(Boolean, default=False)
    node_auto_restart: Mapped[bool] = mapped_column(Boolean, default=False)
    node_excluded_monitorings: Mapped[list[str]] = mapped_column(JSON)
