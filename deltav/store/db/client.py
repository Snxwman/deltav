from __future__ import annotations

from sqlalchemy import select

from deltav.spacetraders.token import AccountToken, AgentToken
from deltav.store.db import Session
from deltav.store.db.account import AccountRecord


class DbClient:
    @staticmethod
    def get_account_token(account_id: str) -> AccountToken | None:
        query = (
            select(AccountRecord)
            .where(AccountRecord.account_id == account_id)
        )  # fmt: skip

        with Session() as session:
            account = session.scalar(query)
            if account is not None:
                return AccountToken(account.token)
            return None

    @staticmethod
    def get_agent_token_from_ship() -> AgentToken | None: ...
