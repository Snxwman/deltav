from __future__ import annotations

from datetime import datetime
from typing import Any

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models import SpaceTradersAPIResShape


class AgentShape(SpaceTradersAPIResShape):
    """Represents an agent's details.

    account_id: str | None
    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int

    Inherits `SpaceTradersAPIResShape(TypeDict)`

    Component of types:
        - RegisterAgentResData

    SpaceTraders API endpoints:
        - SpaceTradersAPIEndpoints.MY_AGENT (GET /my/agent)
    """

    account_id: str | None
    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int


class PublicAgentShape(SpaceTradersAPIResShape):
    """Represents a public agent's details.
    The same as AgentShape, but without account_id.

    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int

    Inherits `SpaceTradersAPIResShape(TypeDict)`

    SpaceTraders API endpoint:
        - SpaceTradersAPIEndpoints.GET_AGENT (GET /agents/{agentSymbol})
    """

    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int


class AgentEventShape(SpaceTradersAPIResShape):
    """Represents an agent's event's details.

    id: str
    type: str
    message: str
    data: dict[Any, Any]
    created_at: datetime

    Inherits from `SpaceTradersAPIResShape(TypeDict)`

    SpaceTraders API endpoints:
        - SpaceTradersAPIEndpoints.MY_AGENT_EVENTS (GET /my/agent/events)
    """

    id: str
    type: str
    message: str
    data: dict[Any, Any]
    created_at: datetime
