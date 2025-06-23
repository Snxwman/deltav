from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base
from deltav.store.db.system import SystemRecord
from deltav.store.db.waypoint import WaypointRecord

if TYPE_CHECKING:
    from deltav.store.db.agent import AgentRecord


class FactionRecord(Base):
    __tablename__: str = 'factions'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    headquarters: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    is_recruiting: Mapped[bool] = mapped_column()

    agents: Mapped[list[AgentRecord]] = relationship(back_populates='faction')
    agent_reputations: Mapped[list[FactionReputationRecord]] = relationship(
        back_populates='faction'
    )
    traits: Mapped[list[FactionTraitRecord]] = relationship(back_populates='faction')
    systems: Mapped[list[SystemRecord]] = relationship(back_populates='factions')
    waypoints: Mapped[list[WaypointRecord]] = relationship(back_populates='faction')


class FactionReputationRecord(Base):
    __tablename__: str = 'faction_reputations'

    id: Mapped[int] = mapped_column(primary_key=True)
    faction_symbol: Mapped[str] = mapped_column()
    reputation: Mapped[int] = mapped_column()

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='faction_reputations')
    faction: Mapped[FactionRecord] = relationship(back_populates='agent_reputations')


class FactionTraitTypeRecord(Base):
    __tablename__: str = 'faction_trait_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()


class FactionTraitRecord(Base):
    __tablename__: str = 'faction_traits'

    id: Mapped[int] = mapped_column(primary_key=True)

    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))
    trait_id: Mapped[int] = mapped_column(ForeignKey('faction_trait_types.id'))

    faction: Mapped[FactionRecord] = relationship(back_populates='traits')
    trait: Mapped[FactionTraitTypeRecord] = relationship()
