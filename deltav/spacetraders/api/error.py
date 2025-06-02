from typing import Any, cast

from requests import Response

from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.models.error import ErrorShape, HttpErrorShape


class SpaceTradersAPIError:
    def __init__(self, res: Response):
        data = cast(ErrorShape, res.json()['error'])
        if 'requestId' in data:
            self.code: SpaceTradersAPIErrorCodes = SpaceTradersAPIErrorCodes(data['code'])
            self.message: str = data['message']
            self.data: dict[Any, Any] = data['data']
            self.request_id: str = data['requestId']
        else:
            data = cast(HttpErrorShape, res.json())
            self.status_code: int = data['status_code']
            self.message: str = data['message']
            self.error: str = data['error']
