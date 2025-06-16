# pyright: reportAny=false
from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from deltav.spacetraders.models import SpaceTradersAPIResShape

if TYPE_CHECKING:
    from deltav.spacetraders.enums.faction import FactionSymbol, FactionTraitSymbol


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


class FactionsShape(SpaceTradersAPIResShape):
    """

    factions: list[FactionsShape] = Field(alias='data')
    """

    factions: list[FactionShape] = Field(alias='data')


class FactionReputationShape(SpaceTradersAPIResShape):
    """

    symbol: FactionSymbol
    reputation: int
    """

    symbol: FactionSymbol
    reputation: int


class FactionReputationsShape(SpaceTradersAPIResShape):
    """

    factions: list[FactionReputationShape] = Field(alias='data')
    """

    factions: list[FactionReputationShape] = Field(alias='data')


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
