from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base
from deltav.store.db.system import SystemRecord  # noqa: TC001
from deltav.store.db.waypoint import WaypointRecord  # noqa: TC001

if TYPE_CHECKING:
    from deltav.store.db.agent import AgentRecord
    from deltav.store.db.ship import ShipRecord


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
    system_id: Mapped[int] = mapped_column(ForeignKey('systems.id'))
    trade_good_id: Mapped[int | None] = mapped_column(ForeignKey('trade_goods.id'))
    waypoint_id: Mapped[int] = mapped_column(ForeignKey('waypoints.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='transactions')
    ship: Mapped[ShipRecord] = relationship(back_populates='transactions')
    system: Mapped[SystemRecord] = relationship(back_populates='transactions')
    trade_good: Mapped[TradeGoodRecord] = relationship()
    waypoint: Mapped[WaypointRecord] = relationship(back_populates='transactions')


class TradeGoodRecord(Base):
    __tablename__: str = 'trade_goods'

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
