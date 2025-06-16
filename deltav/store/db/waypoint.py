from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.chart import ChartRecord
    from deltav.store.db.faction import FactionRecord
    from deltav.store.db.system import SystemRecord


class WaypointRecord(Base):
    __tablename__: str = 'waypoints'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(unique=True)
    system_symbol: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()
    orbits: Mapped[str | None] = mapped_column()
    is_under_construction: Mapped[bool] = mapped_column()

    chart_id: Mapped[int] = mapped_column(ForeignKey('charts.id'))
    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))

    chart: Mapped[ChartRecord] = relationship(back_populates='waypoint')
    faction: Mapped[FactionRecord] = relationship(back_populates='waypoints')
    modifiers: Mapped[list[WaypointModifierRecord]] = relationship(back_populates='waypoint')
    orbitals: Mapped[list[WaypointOrbitalRecord]] = relationship(back_populates='waypoint')
    system: Mapped[SystemRecord] = relationship(back_populates='waypoints')
    traits: Mapped[list[WaypointTraitRecord]] = relationship(back_populates='waypoint')


class WaypointModifierTypeRecord(Base):
    __tablename__: str = 'waypoint_modifier_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)


class WaypointModifierRecord(Base):
    __tablename__: str = 'waypoint_modifiers'

    id: Mapped[int] = mapped_column(primary_key=True)

    modifier_id: Mapped[int] = mapped_column(ForeignKey('waypoint_modifier_types.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    modifer: Mapped[WaypointModifierTypeRecord] = relationship()
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='modifers')


class WaypointOrbitalRecord(Base):
    __tablename__: str = 'waypoint_orbitals'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column()

    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    waypoint: Mapped[WaypointRecord] = relationship(back_populates='orbitals')


class WaypointTraitTypeRecord(Base):
    __tablename__: str = 'waypoint_trait_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)


class WaypointTraitRecord(Base):
    __tablename__: str = 'waypoint_traits'

    id: Mapped[int] = mapped_column(primary_key=True)

    trait_id: Mapped[int] = mapped_column(ForeignKey('waypoint_trait_types.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    trait: Mapped[WaypointTraitTypeRecord] = relationship()
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='traits')
