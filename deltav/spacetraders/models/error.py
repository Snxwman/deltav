from __future__ import annotations

from http import HTTPStatus
from typing import Any

from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.models import SpaceTradersAPIResShape


class SpaceTradersAPIErrorShape(SpaceTradersAPIResShape):
    """

    code: SpaceTradersAPIErrorCodes
    data: dict[str, Any]
    message: str
    request_id: str
    """

    code: SpaceTradersAPIErrorCodes
    data: dict[str, Any]
    message: str
    request_id: str


class HttpErrorShape(SpaceTradersAPIResShape):
    """

    code: HTTPStatus
    error: str
    message: str
    """

    code: HTTPStatus
    error: str
    message: str


class ErrorCodeShape(SpaceTradersAPIResShape):
    """

    code: int
    name: str
    """

    code: int
    name: str


# NOTE: Top level return shape
class ErrorCodesShape(SpaceTradersAPIResShape):
    """

    error_codes: list[ErrorCodeShape]
    """

    error_codes: list[ErrorCodeShape]
