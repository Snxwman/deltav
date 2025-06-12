# pyright: reportImportCycles=false
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, final

from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base

if TYPE_CHECKING:
    from deltav.store.db.agent import AgentRecord


@final
class AccountRecord(Base):
    __tablename__: str = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str | None] = mapped_column(unique=True)
    account_id: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))

    agents: Mapped[list['AgentRecord']] = relationship(back_populates='account')
