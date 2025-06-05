from http import HTTPStatus
from typing import Any

from pydantic import ValidationError
from requests import Response

from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.models.error import HttpErrorShape, SpaceTradersAPIErrorShape


# TODO: Implement
#  - Handle HTTP 429 (and possibly others) errors (sent unmodified from spacetraders cloud infra)
#  - Handle HTTP 502 errors (recommended to wait a few minutes for retry)
class SpaceTradersAPIError:
    def __init__(self, res: Response):
        self.__res: Response = res
        self.__data: SpaceTradersAPIErrorShape | HttpErrorShape
        self.code: SpaceTradersAPIErrorCodes | HTTPStatus
        self.message: str
        self.data: Any  # TODO: Type could be improved
        self.request_id: str | None

        try:
            data = SpaceTradersAPIErrorShape.model_validate(res.json()['error'])
            self.__init_spacetraders_error(data)
        except ValidationError:
            data = HttpErrorShape.model_validate(res.json())
            self.__init_http_error(data)

    def unwrap(self) -> 'SpaceTradersAPIError':
        return self

    def __init_spacetraders_error(self, err: SpaceTradersAPIErrorShape) -> None:
        self.code = err.code
        self.message = err.message
        self.data = err.data
        self.request_id = err.request_id

    def __init_http_error(self, err: HttpErrorShape) -> None:
        self.code = err.code
        self.message = err.message
        self.data = err.error  # Actually the 'error' field
        self.request_id = None
