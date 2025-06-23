# pyright: reportImportCycles=false
from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, final

from sqlalchemy import insert, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.config.config import StAccountConfig
from deltav.spacetraders.models.account import AccountShape
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

    agents: Mapped[list[AgentRecord]] = relationship(back_populates='account')

    @staticmethod
    def preload_from_config(accounts: list[StAccountConfig]) -> None:
        with Session() as session:
            _ = session.execute(
                insert(AccountRecord),
                [
                    {
                        'account_id': account.token.account_id,
                        'email': account.email,
                        'token': account.token.encoded,
                    }
                    for account in accounts
                ],
            )

    @staticmethod
    def insert(data: AccountShape) -> AccountRecord:
        with Session() as session:
            ...

    @staticmethod
    def get_token(account_id: str) -> str | None:
        with Session() as session:
            account = session.scalar(
                select(AccountRecord)
                .where(AccountRecord.account_id == account_id)
            )  # fmt: skip

            if account is not None:
                return account.token

            return None

    @staticmethod
    def get_from_token(token: str) -> AccountRecord | None: ...
