# pyright: reportImportCycles=false
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.account import AccountRecord
    from deltav.store.db.chart import ChartRecord
    from deltav.store.db.contract import ContractRecord
    from deltav.store.db.faction import FactionRecord, FactionReputationRecord
    from deltav.store.db.ship import ShipRecord
    from deltav.store.db.transaction import TransactionRecord


class AgentRecord(Base):
    __tablename__: str = 'agents'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    credits: Mapped[int] = mapped_column()
    faction_symbol: Mapped[str] = mapped_column()
    headquarters: Mapped[str] = mapped_column()
    ship_count: Mapped[int] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)
    token: Mapped[str] = mapped_column(unique=True)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))

    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))

    account: Mapped[AccountRecord] = relationship(back_populates='agent')
    contracts: Mapped[list[ContractRecord]] = relationship(back_populates='agent')
    events: Mapped[list[AgentEventRecord]] = relationship(back_populates='agent')
    faction: Mapped[FactionRecord] = relationship(back_populates='agents')
    faction_reputations: Mapped[list[FactionReputationRecord]] = relationship(
        back_populates='agent'
    )
    ships: Mapped[list[ShipRecord]] = relationship(back_populates='agent')
    transactions: Mapped[list[TransactionRecord]] = relationship(back_populates='agent')

    @staticmethod
    def get_from_symbol(symbol: str) -> AgentRecord: ...

    @staticmethod
    def get_from_token(token: str) -> AgentRecord: ...


class AgentEventRecord(Base):
    __tablename__: str = 'agent_events'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column()
    data: Mapped[str | None] = mapped_column()
    event_id: Mapped[int] = mapped_column()
    message: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    agent_id: Mapped[AgentRecord] = mapped_column(ForeignKey('agents.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='events')


class PublicAgentRecord(Base):
    __tablename__: str = 'public_agents'

    id: Mapped[int] = mapped_column(primary_key=True)
    credits: Mapped[int] = mapped_column()
    faction_symbol: Mapped[str] = mapped_column()
    headquarters: Mapped[str] = mapped_column()
    ship_count: Mapped[int] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)

    faction_id: Mapped[int] = mapped_column(ForeignKey('factions.id'))

    charts: Mapped[list[ChartRecord]] = relationship(back_populates='agent')
    faction: Mapped[FactionRecord] = relationship(back_populates='agents')
    ships: Mapped[list[ShipRecord]] = relationship(back_populates='agent')
    transactions: Mapped[list[TransactionRecord]] = relationship(back_populates='agent')

    @staticmethod
    def get_from_symbol(symbol: str) -> AgentRecord: ...
