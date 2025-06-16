from __future__ import annotations

from typing import TYPE_CHECKING

from deltav.spacetraders.models import SpaceTradersAPIResShape

if TYPE_CHECKING:
    from datetime import datetime


class AccountShape(SpaceTradersAPIResShape):
    """

    id: str
    email: str
    token: str  # TODO: Should be a JWT
    created_at: datetime
    """

    id: str
    email: str = ''
    token: str = ''
    created_at: datetime


class MyAccountShape(SpaceTradersAPIResShape):
    """

    account: AccountShape
    """

    account: AccountShape
