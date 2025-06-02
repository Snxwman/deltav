from __future__ import annotations

from deltav.spacetraders.enums.faction import FactionTraitSymbol
from deltav.spacetraders.models import SpaceTradersAPIResShape


class FactionShape(SpaceTradersAPIResShape):
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: list[FactionTraitSymbol]
    is_recruiting: bool
