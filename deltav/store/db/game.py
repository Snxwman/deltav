from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from datetime import datetime


class ServerStatusRecord(Base):
    __tablename__: str = 'server_status'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column()
    version: Mapped[str] = mapped_column()
    last_reset_date: Mapped[datetime] = mapped_column()
    next_reset_date: Mapped[datetime] = mapped_column()
    reset_frequency: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    stats_accounts: Mapped[int] = mapped_column()
    stats_agents: Mapped[int] = mapped_column()
    stats_ships: Mapped[int] = mapped_column()
    stats_systems: Mapped[int] = mapped_column()
    stats_waypoints: Mapped[int] = mapped_column()
    last_market_update: Mapped[datetime] = mapped_column()

    announcements: Mapped[list[ServerAnnouncementRecord]] = relationship()


class ServerAnnouncementRecord(Base):
    __tablename__: str = 'server_announcements'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column(default='')

    received_at: Mapped[datetime] = mapped_column()

    status_id: Mapped[int] = mapped_column(ForeignKey('server_status.id'))
