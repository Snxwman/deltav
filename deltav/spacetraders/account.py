from datetime import datetime

from loguru import logger

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.account import AccountShape
from deltav.spacetraders.token import AccountToken


class Account:
    def __init__(self, token: AccountToken):
        logger.debug('Initializing new Agent')
        logger.trace(f'{token=}')

        self.id: str = token.account_id
        self.email: str | None = ''
        self.token: AccountToken = token
        self.created_at: datetime = token.issued_at

    def my_account(self) -> AccountShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AccountShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_ACCOUNT)
            .token()
            .build(),
        ).unwrap()
