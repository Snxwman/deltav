from __future__ import annotations

from datetime import datetime
from typing import Any

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape


class RegisterAgentData(SpaceTradersAPIReqShape):
    symbol: str
    faction: FactionSymbol


class AgentShape(SpaceTradersAPIResShape):
    account_id: str | None
    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int


class PublicAgentShape(SpaceTradersAPIResShape):
    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int


class AgentEvent(SpaceTradersAPIResShape):
    id: str
    type: str
    message: str
    data: dict[Any, Any]
    created_at: datetime
