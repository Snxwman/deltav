from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.agent import AgentRecord
    from deltav.store.db.faction import FactionRecord
    from deltav.store.db.system import SystemRecord


class ChartRecord(Base):
    __tablename__: str = 'charts'

    id: Mapped[int] = mapped_column(primary_key=True)
    waypoint_symbol: Mapped[str] = mapped_column()
    submitted_by: Mapped[str] = mapped_column()
    submitted_on: Mapped[datetime] = mapped_column()

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='charts')
    system: Mapped[SystemRecord] = relationship(back_populates='charts')
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='chart')


class TransactionRecord(Base):
    __tablename__: str = 'transactions'

    # NOTE: agent_symbol is not a part of any transaction shape except ShipyardTransactionShape,
    # but since ship_symbol is a part of all the others, we can get the agent symbol for every
    # transaction from the ship symbol.

    # Used by all transaction shapes
    id: Mapped[int] = mapped_column(primary_key=True)
    agent_symbol: Mapped[str] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column()
    waypoint_symbol: Mapped[str] = mapped_column()
    # Used by: all transaction shapes except ShipyardTransactionShape
    ship_symbol: Mapped[str] = mapped_column(nullable=True)
    # Used by: MarketTransactionShape, ShipModifyTransactionShape, ShipRefuelTransactionShape
    trade_symbol: Mapped[str] = mapped_column(nullable=True)
    # Used by: MarketTransactionShape and ShipRefuelTransactionShape
    type: Mapped[str] = mapped_column(nullable=True)
    units: Mapped[int] = mapped_column(nullable=True)
    # Used by: MarketTransactionShape
    price_per_unit: Mapped[int] = mapped_column(nullable=True)
    # Used by: ShipyardTransactionShape
    ship_type: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)

    # Derived columns
    # One of: create chart, market, ship repair, ship scrap, ship modify, ship refuel, shipyard.
    transaction_class: Mapped[str] = mapped_column()

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))
    trade_good_id: Mapped[int | None] = mapped_column(ForeignKey('trade_goods.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='transactions')
    trade_good: Mapped[TradeGoodRecord] = relationship()
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='transactions')


class TradeGoodRecord(Base):
    __tablename__: str = 'trade_goods'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


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

    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))

    chart: Mapped[ChartRecord] = relationship(back_populates='waypoint')
    faction: Mapped[FactionRecord] = relationship(back_populates='waypoints')
    modifiers: Mapped[list[WaypointModifierRecord]] = relationship(back_populates='waypoint')
    orbitals: Mapped[list[WaypointOrbitalRecord]] = relationship(back_populates='waypoint')
    system: Mapped[SystemRecord] = relationship(back_populates='waypoints')
    traits: Mapped[list[WaypointTraitRecord]] = relationship(back_populates='waypoint')
    transactions: Mapped[list[TransactionRecord]] = relationship(back_populates='waypoint')


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
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='modifiers')


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
