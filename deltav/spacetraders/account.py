from datetime import datetime

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.account import AccountShape


class Account:
    def __init__(self, id: str, email: str | None = None):
        self.id: str = id
        self.email: str | None = email
        self.token: str = ''
        self.created_at: datetime = datetime.now()

    def my_account(self) -> AccountShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_ACCOUNT)
            .token()
            .build(),
            AccountShape
        ).unwrap()
