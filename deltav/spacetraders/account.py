from __future__ import annotations

from datetime import UTC, datetime

from loguru import logger

from deltav.config.config import Config, StAccountConfig
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.account import AccountShape, MyAccountShape
from deltav.spacetraders.token import AccountToken, AgentToken


class Account:
    # Key is the account_id (can be obtained from the account token)
    _ACCOUNTS: dict[str, 'Account'] = {}

    # SpaceTraders API requires an agent token (?) to fetch the account details...
    def __init__(self, token: AccountToken, agent_token: AgentToken) -> None:
        """A SpaceTraders Account

        Fields:
            id (str)
            token (AccountToken)
            created_at (datetime)
            email (str)
        """

        logger.debug('Initializing new Account')
        logger.trace(f'{token=}')

        self.__synced_api: bool = False
        self.__synced_db: bool = False
        self.__data: AccountShape
        self.__data_timestamp: datetime
        self.__config: StAccountConfig
        self.id: str = token.account_id
        self.token: AccountToken = token
        self.created_at: datetime = token.issued_at
        self.email: str | None = None

        if config := Config.get_account_from_token(token):
            self.__config = config
            self.email = config.email

        self.update_account(agent_token)
        Account.__update_cache(self)

    def update_account(self, token: AgentToken) -> None:
        match self._fetch_account(token):
            case MyAccountShape() as res:
                self.__synced_api = True
                self.__data = res.account
                self.__data_timestamp = datetime.now(tz=UTC)
                if self.email is None or self.email != res.account.email:
                    self.email = res.account.email
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

    @staticmethod
    def get_account(token: AccountToken, agent_token: AgentToken) -> 'Account':
        if (account := Account.__from_cache(token.account_id)) is not None:
            return account

        return Account(token, agent_token)

    @classmethod
    def __update_cache(cls, account: 'Account') -> None:
        cls._ACCOUNTS[account.id] = account

    @classmethod
    def __from_cache(cls, account_id: str) -> 'Account | None':
        return cls._ACCOUNTS.get(account_id, None)
