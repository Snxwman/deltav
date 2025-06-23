# pyright: reportImportCycles=false
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import insert, select, text

from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.endpoint import AgentRegisterResShape
from deltav.spacetraders.token import AgentToken
from deltav.store.db import Base, Session
from deltav.store.db.contract import ContractRecord
from deltav.store.db.ship import ShipRecord
from deltav.store.db.waypoint import ChartRecord

if TYPE_CHECKING:
    from deltav.store.db.account import AccountRecord
    from deltav.store.db.faction import FactionRecord, FactionReputationRecord
    from deltav.store.db.waypoint import TransactionRecord


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

    account: Mapped[AccountRecord] = relationship(back_populates='agents')
    charts: Mapped[ChartRecord] = relationship(back_populates='agent')
    contracts: Mapped[list[ContractRecord]] = relationship(back_populates='agent')
    events: Mapped[list[AgentEventRecord]] = relationship(back_populates='agent')
    faction: Mapped[FactionRecord] = relationship(back_populates='agents')
    faction_reputations: Mapped[list[FactionReputationRecord]] = relationship(
        back_populates='agent'
    )
    ships: Mapped[list[ShipRecord]] = relationship(back_populates='agent')
    transactions: Mapped[list[TransactionRecord]] = relationship(back_populates='agent')

    @staticmethod
    def insert(data: AgentRegisterResShape) -> AgentRecord | None:
        with Session() as session:
            _ = session.execute(text('PRAGMA foreign_keys = ON;'))

            account = session.scalar(
                select(AccountRecord)
                .where(AccountRecord.account_id == data.agent.account_id)
            )  # fmt: skip
            assert account is not None

            faction = session.scalar(
                select(FactionRecord)
                .where(FactionRecord.symbol == data.agent.starting_faction)
            )  # fmt: skip
            assert faction is not None

            agent_record = session.scalar(
                insert(AgentRecord)
                .values(
                    **data.agent.model_dump(exclude=set('starting_faction')),
                    faction_symbol=data.agent.starting_faction,
                    token=data.token,
                    account_id=account.id,
                    faction_id=faction.id,
                )
                .returning(AgentRecord),
            )

            session.commit()

        assert agent_record is not None
        return agent_record

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
