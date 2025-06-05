from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.models import SpaceTradersAPIResShape


class AccountShape(SpaceTradersAPIResShape):
    """

    id: str
    email: str
    token: str  # TODO: Should be a JWT
    created_at: datetime
    """

    id: str
    email: str
    token: str  # TODO: Should be a JWT
    created_at: datetime


class MyAccountShape(SpaceTradersAPIResShape):
    """

    account: AccountShape
    """
    account: AccountShape
