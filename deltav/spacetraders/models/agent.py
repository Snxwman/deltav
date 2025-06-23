# pyright: reportAny=false
from __future__ import annotations

from datetime import datetime
from typing import Any, override

from pydantic import Field

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models import SpaceTradersAPIResShape


def agent__str__(agent: AgentShape | PublicAgentShape) -> str:
    return f'- [{agent.starting_faction.name}] {agent.symbol} ({agent.headquarters}) {agent.ship_count} ships, (${agent.credits})'


class AgentShape(SpaceTradersAPIResShape):
    """Represents an agent's details.

    account_id: str
    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int
    """

    account_id: str
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
    """

    id: str
    type: str
    message: str
    data: dict[Any, Any]
    created_at: datetime


class AgentEventsShape(SpaceTradersAPIResShape):
    """

    events: list[AgentEventShape]
    """

    events: list[AgentEventShape] = Field(alias='data')


class PublicAgentShape(SpaceTradersAPIResShape):
    """Represents a public agent's details.
    The same as AgentShape, but without account_id.

    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int
    """

    symbol: str
    headquarters: str
    credits: int
    starting_faction: FactionSymbol
    ship_count: int

    @override
    def __str__(self) -> str:
        return agent__str__(self)


class PublicAgentsShape(SpaceTradersAPIResShape):
    """

    agents: list[PublicAgentShape]
    """

    agents: list[PublicAgentShape] = Field(alias='data')
