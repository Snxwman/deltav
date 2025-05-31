from typing import Any, cast

from requests import Response

from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.models.error import ErrorShape


class SpaceTradersAPIError:
    def __init__(self, res: Response):
        data = cast(ErrorShape, res.json()['error'])

        self.code: SpaceTradersAPIErrorCodes = SpaceTradersAPIErrorCodes(data['code'])
        self.message: str = data['message']
        self.data: dict[Any, Any] = data['data']  # pyright: ignore[reportExplicitAny]
        self.request_id: str = data['request_id']

