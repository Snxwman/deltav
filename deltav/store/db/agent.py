from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, final

from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.account import AccountRecord
    from deltav.store.db.contract import ContractRecord


@final
class AgentRecord(Base):
    __tablename__: str = 'agents'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str | None] = mapped_column(unique=True)
    symbol: Mapped[str] = mapped_column(unique=True)
    credits: Mapped[int] = mapped_column()
    headquarters: Mapped[str] = mapped_column()
    faction: Mapped[str] = mapped_column()
    ship_count: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))

    account: Mapped[list[AccountRecord]] = relationship(back_populates='account')
    contracts: Mapped[list[ContractRecord]] = relationship(back_populates='contracts')
    # ships: Mapped[list[ShipRecord]] = relationship(back_populates='ships')
