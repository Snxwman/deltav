from __future__ import annotations

from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.enums.faction import FactionSymbol, FactionTraitSymbol


class FactionTrait(SpaceTradersAPIResShape):
    symbol: FactionTraitSymbol
    name: str
    description: str


class FactionShape(SpaceTradersAPIResShape):
    symbol: FactionSymbol
    name: str
    description: str
    headquarters: str
    traits: list[FactionTrait]
    is_recruiting: bool

