from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from loguru import logger

from deltav.config.config import Config, StAccountConfig
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.account import AccountShape, MyAccountShape
from deltav.store.db import Session
from deltav.store.db.account import AccountRecord

if TYPE_CHECKING:
    from deltav.spacetraders.token import AccountToken, AgentToken


class Account:
    # Key is the account_id (can be obtained from the account token)
    _ACCOUNTS: dict[str, 'Account'] = {}

    # SpaceTraders API requires an agent token (?) to fetch the account details...
    def __init__(
        self,
        token: AccountToken,
        agent_token: AgentToken,
        data: AccountShape | AccountRecord | None = None,
    ) -> None:
        """A SpaceTraders Account"""

        logger.debug('Initializing new Account')
        logger.trace(f'{token=}')

        self.__synced_api: bool = False
        self.__synced_db: bool = False
        self.__data: AccountRecord
        self.__data_timestamp: datetime
        self.__config: StAccountConfig

        self._account_id: str = token.account_id
        self._created_at: datetime = token.issued_at
        self._email: str | None = None
        self._token: AccountToken = token

        if config := Config.get_account_from_token(token):
            self.__config = config
            self._email = config.email

        match data:
            case AccountShape():
                self.__hydrate_from_shape(data)
            case AccountRecord():
                self.__hydrate_from_record(data)
            case None:
                try:
                    self.__hydrate_from_db()
                except:  # TODO: Make custom db errors
                    self.__hydrate_from_api()

        self.update_account(agent_token)
        Account.__update_cache(self)

    def __hydrate_from_api(self) -> None: ...

    def __hydrate_from_db(self) -> None: ...

    def __hydrate_from_record(self, data: AccountRecord) -> None: ...

    def __hydrate_from_shape(self, data: AccountShape) -> None: ...

    @property
    def id(self) -> str:
        return self._account_id

    @property
    def token(self) -> AccountToken:
        return self._token

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def email(self) -> str | None:
        return self._email

    @staticmethod
    def get_account(token: AccountToken, agent_token: AgentToken) -> 'Account':
        if (account := Account.__from_cache(token.account_id)) is not None:
            return account

        return Account(token, agent_token)

    def update_account(self, token: AgentToken) -> None:
        match self._fetch_account(token):
            case MyAccountShape() as res:
                self.__update_db_from_shape(res)
                self.__synced_api = True
                self.__synced_db = True
                if self.email is None or self.email != res.account.email:
                    self._email = res.account.email

            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_account_err(err)

    def _fetch_account(self, agent_token: AgentToken) -> MyAccountShape | SpaceTradersAPIError:
        msg = f"Attempting to fetch account details for token '{self.token.hash}'"
        logger.debug(msg)

        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[MyAccountShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ACCOUNT)
            .token(agent_token)
            .build()
        ).unwrap()

    def __handle_fetch_account_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f'Failed to fetch account from API. {err}'
        logger.error(log_str)
        return ValueError(log_str)

    @classmethod
    def __update_cache(cls, account: 'Account') -> None:
        cls._ACCOUNTS[account.id] = account

    @classmethod
    def __from_cache(cls, account_id: str) -> 'Account | None':
        return cls._ACCOUNTS.get(account_id, None)

    def __update_db(self, data: AccountShape | None = None) -> None:
        account = AccountRecord(
            account_id=self.id, created_at=self.created_at, email=self.email, token=self.token
        )

        with Session() as session:
            session.add(account)

    def __update_db_from_shape(self, data: MyAccountShape) -> None: ...
