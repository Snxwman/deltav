from __future__ import annotations

from typing import TYPE_CHECKING

from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape

if TYPE_CHECKING:
    from deltav.spacetraders.enums.market import TradeSymbol
    from deltav.spacetraders.models.ship import ShipCargoShape


class ConstructionShape(SpaceTradersAPIResShape):
    """

    symbol: str
    materials: list[ConstructionMaterialShape]
    is_complete: bool
    """

    symbol: str
    materials: list[ConstructionMaterialShape]
    is_complete: bool


class ConstructionMaterialShape(SpaceTradersAPIResShape):
    """

    trade_symbol: TradeSymbol
    required: int
    fulfilled: int
    """

    trade_symbol: TradeSymbol
    required: int
    fulfilled: int


class ConstructionSupplyReqShape(SpaceTradersAPIReqShape):
    """

    ship_symbol: str
    trade_symbol: TradeSymbol
    units: int
    """

    ship_symbol: str
    trade_symbol: TradeSymbol
    units: int


class ConstructionSupplyResShape(SpaceTradersAPIResShape):
    """

    construction: ConstructionShape
    cargo: ShipCargoShape
    """

    construction: ConstructionShape
    cargo: ShipCargoShape
