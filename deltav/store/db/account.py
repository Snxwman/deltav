# pyright: reportImportCycles=false
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, final

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base, Session

if TYPE_CHECKING:
    from deltav.store.db.agent import AgentRecord


@final
class AccountRecord(Base):
    __tablename__: str = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    email: Mapped[str] = mapped_column()
    token: Mapped[str] = mapped_column(unique=True)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))

    agents: Mapped[list['AgentRecord']] = relationship(back_populates='account')

    @staticmethod
    def get_token(account_id: str) -> str | None:
        query = (
            select(AccountRecord)
            .where(AccountRecord.account_id == account_id)
        )  # fmt: skip

        with Session() as session:
            account = session.scalar(query)
            if account is not None:
                return account.token
            return None

    @staticmethod
    def get_from_token(token: str) -> AccountRecord | None: ...
