from __future__ import annotations

from typing import TypeAlias

from deltav.spacetraders.models.market import MarketTransactionShape
from deltav.spacetraders.models.ship import (
    ShipModifyTransactionShape,
    ShipRefuelTransactionShape,
    ShipTransactionShape,
)
from deltav.spacetraders.models.systems import ShipyardTransactionShape

TransactionShape: TypeAlias = (
    MarketTransactionShape
    | ShipModifyTransactionShape
    | ShipRefuelTransactionShape
    | ShipTransactionShape
    | ShipyardTransactionShape
)
"""Type alias for all different transaction shapes"""
