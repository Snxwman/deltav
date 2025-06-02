from __future__ import annotations

from datetime import datetime
from typing import Any

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.faction import FactionShape
from deltav.spacetraders.models.ship import ShipShape


class RegisterAgentReqData(SpaceTradersAPIReqShape):
    """Represents the request data sent when registering an agent.

    symbol: str
    faction: FactionSymbol

    Inherits `SpaceTradersAPIReqShape(TypeDict)`

    SpaceTraders API endpoints:
        - SpaceTradersAPIEndpoints.REGISTER (POST /register)
    """
    symbol: str
    faction: FactionSymbol


class RegisterAgentResData(SpaceTradersAPIResShape):
    """Represents the response data returned when registering an agent.

    token: str
    agent: AgentShape
    faction: FactionShape
    contract: ContractShape
    ships: list[ShipShape]

    Inherits `SpaceTradersAPIResShape(TypeDict)`

    SpaceTraders API endpoints:
        - SpaceTradersAPIEndpoints.REGISTER (POST /register)
    """
    token: str
    agent: AgentShape
    faction: FactionShape
    contract: ContractShape
    ships: list[ShipShape]


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
