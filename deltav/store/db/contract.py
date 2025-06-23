from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.agent import AgentRecord
    from deltav.store.db.transaction import TradeGoodRecord


class ContractRecord(Base):
    __tablename__: str = 'contracts'

    id: Mapped[int] = mapped_column(primary_key=True)
    accepted: Mapped[bool] = mapped_column()
    contract_id: Mapped[str] = mapped_column(unique=True)
    deadline_to_accept: Mapped[datetime | None] = mapped_column()
    deadline_to_fulfill: Mapped[datetime] = mapped_column()
    faction_symbol: Mapped[str] = mapped_column()
    fulfilled: Mapped[bool] = mapped_column()
    payment_on_delivered: Mapped[int] = mapped_column()
    payment_on_fulfilled: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column()

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='contracts')
    deliverables: Mapped[list[ContractDeliverableRecord]] = relationship(back_populates='contract')


class ContractDeliverableRecord(Base):
    __tablename__: str = 'contract_deliverables'

    id: Mapped[int] = mapped_column(primary_key=True)
    trade_symbol: Mapped[str] = mapped_column()
    destination_symbol: Mapped[str] = mapped_column()
    units_requried: Mapped[int] = mapped_column()
    units_Fulfilled: Mapped[int] = mapped_column()

    contract_id: Mapped[int] = mapped_column(ForeignKey('contracts.id'))
    trade_good_id: Mapped[int] = mapped_column(ForeignKey('trade_goods.id'))

    contract: Mapped[ContractRecord] = relationship(back_populates='deliverables')
    trade_good: Mapped[list[TradeGoodRecord]] = relationship()
