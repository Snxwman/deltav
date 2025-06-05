from __future__ import annotations

from deltav.spacetraders.enums.faction import FactionSymbol, FactionTraitSymbol
from deltav.spacetraders.models import SpaceTradersAPIResShape


class FactionShape(SpaceTradersAPIResShape):
    """

    symbol: FactionSymbol
    name: str
    description: str
    headquarters: str
    traits: list[FactionTraitShape]
    is_recruiting: bool
    """

    symbol: FactionSymbol
    name: str
    description: str
    headquarters: str
    traits: list[FactionTraitShape]
    is_recruiting: bool


class FactionSymbolShape(SpaceTradersAPIResShape):
    """

    symbol: FactionSymbol
    """

    symbol: FactionSymbol


class FactionTraitShape(SpaceTradersAPIResShape):
    """

    symbol: FactionTraitSymbol
    name: str
    description: str
    """

    symbol: FactionTraitSymbol
    name: str
    description: str
