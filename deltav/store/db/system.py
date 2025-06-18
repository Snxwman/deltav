from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base
from deltav.store.db.chart import ChartRecord  # noqa: TC001

if TYPE_CHECKING:
    from deltav.store.db.faction import FactionRecord
    from deltav.store.db.waypoint import WaypointRecord


class SystemRecord(Base):
    __tablename__: str = 'systems'

    id: Mapped[int] = mapped_column(primary_key=True)
    constellation: Mapped[str | None] = mapped_column()
    name: Mapped[str | None] = mapped_column()
    sector_symbol: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)
    type: Mapped[str] = mapped_column()
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()

    chart_id: Mapped[int] = mapped_column(ForeignKey('charts.id'))
    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    charts: Mapped[list[ChartRecord]] = relationship(back_populates='system')
    factions: Mapped[list[FactionRecord]] = relationship(back_populates='systems')
    waypoints: Mapped[list[WaypointRecord]] = relationship(back_populates='system')
