from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.agent import PublicAgentRecord
    from deltav.store.db.waypoint import WaypointRecord


class ChartRecord(Base):
    __tablename__: str = 'charts'

    id: Mapped[int] = mapped_column(primary_key=True)
    waypoint_symbol: Mapped[str] = mapped_column()
    submitted_by: Mapped[str] = mapped_column()
    submitted_on: Mapped[datetime] = mapped_column()

    agent_id: Mapped[int] = mapped_column(ForeignKey('public_agents.id'))
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    agent: Mapped[PublicAgentRecord] = relationship(back_populates='charts')
    system: Mapped[WaypointRecord] = relationship(back_populates='charts')
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='chart')
