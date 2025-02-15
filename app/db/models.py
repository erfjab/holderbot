"""
Database models for the application.

This module defines the SQLAlchemy models for the tokens and settings.
"""

from datetime import datetime
from sqlalchemy import Integer, DateTime, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .base import Base
from app.models.server import ServerTypes
from app.models.user import DateTypes


class BaseTime:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow)


class Server(Base, BaseTime):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    remark: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    node_monitoring: Mapped[bool] = mapped_column(Boolean, default=False)
    node_restart: Mapped[bool] = mapped_column(Boolean, default=False)
    expired_stats: Mapped[bool] = mapped_column(Boolean, default=False)
    types: Mapped[ServerTypes] = mapped_column(String, nullable=False)
    data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    server_access: Mapped["ServerAccess"] = relationship(
        "ServerAccess", uselist=False, lazy="joined"
    )

    @hybrid_property
    def access(self) -> str | None:
        return self.server_access.access if self.server_access else None

    @hybrid_property
    def emoji(self) -> str:
        return "✅ " if self.is_active else "❌ "

    @hybrid_property
    def is_online(self) -> bool:
        if not self.access:
            return False
        last_update = self.server_access.updated_at or self.server_access.created_at
        if last_update is None:
            return False
        return (datetime.utcnow() - last_update).total_seconds() < 86400

    @hybrid_property
    def size_value(self) -> int:
        return 100 if self.types == ServerTypes.MARZNESHIN else 25

    @hybrid_property
    def format_data(self) -> str:
        formatted_data = "\n".join(
            [
                f"     • <b>{key}:</b> <code>{value}</code>"
                for key, value in self.data.items()
            ]
        )
        return (
            f"• <b>ID:</b> <code>{self.id}</code>\n"
            f"• <b>Remark:</b> <code>{self.remark}</code>\n"
            f"• <b>Active:</b> <code>{'Yes' if self.is_active else 'No'}</code>\n"
            f"• <b>Online:</b> <code>{'Yes' if self.is_online else 'No'}</code>\n"
            f"• <b>Node Monitoring:</b> <code>{'Yes' if self.node_monitoring else 'No'}</code>\n"
            f"• <b>Node Auto Restart:</b> <code>{'Yes' if self.node_restart else 'No'}</code>\n"
            f"• <b>Expired Stats:</b> <code>{'Yes' if self.expired_stats else 'No'}</code>\n"
            f"• <b>Types:</b> <code>{self.types}</code>\n"
            f"• <b>Data</b>\n{formatted_data}\n"
            f"• <b>Updated At:</b> <code>{self.updated_at or '➖'}</code>\n"
            f"• <b>Created At:</b> <code>{(datetime.utcnow() - self.created_at).days} days ago</code>\n"
        )


class ServerAccess(Base, BaseTime):
    __tablename__ = "servers_access"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    access: Mapped[str] = mapped_column(String)
    server_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("servers.id"), nullable=False
    )


class Template(Base, BaseTime):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    remark: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    data_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    date_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    date_types: Mapped[DateTypes] = mapped_column(String, nullable=False)

    @hybrid_property
    def emoji(self) -> str:
        return "✅ " if self.is_active else "❌ "

    @property
    def button_remark(self) -> str:
        return (
            f"{self.id} | {self.remark} [{self.data_limit} GB - {self.date_limit} Day]"
        )

    @hybrid_property
    def format_data(self) -> str:
        return (
            f"• <b>Remark:</b> <code>{self.remark}</code>\n"
            f"• <b>Active:</b> <code>{'Yes' if self.is_active else 'No'}</code>\n"
            f"• <b>Data limit:</b> <code>{self.data_limit}</code>\n"
            f"• <b>Date limit:</b> <code>{self.date_limit}</code>\n"
            f"• <b>Date types:</b> <code>{self.date_types}</code>\n"
            f"• <b>Updated At:</b> <code>{self.updated_at or '➖'}</code>\n"
            f"• <b>Created At:</b> <code>{(datetime.utcnow() - self.created_at).days} days ago</code>\n"
        )
