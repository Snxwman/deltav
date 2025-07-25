from __future__ import annotations

from typing import TYPE_CHECKING

from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models.ship import ShipTransactionShape

if TYPE_CHECKING:
    from deltav.spacetraders.enums.faction import FactionSymbol
    from deltav.spacetraders.models.agent import AgentShape
    from deltav.spacetraders.models.chart import ChartShape
    from deltav.spacetraders.models.contract import ContractShape
    from deltav.spacetraders.models.faction import FactionShape
    from deltav.spacetraders.models.market import MarketTransactionShape
    from deltav.spacetraders.models.ship import ShipCargoShape, ShipShape
    from deltav.spacetraders.models.systems import SystemWaypointShape


class AgentContractsShape(SpaceTradersAPIResShape):
    """

    contracts: list[ContractShape]
    """

    contracts: list[ContractShape]


class AgentRegisterReqData(SpaceTradersAPIReqShape):
    """Represents the request data sent when registering an agent.

    symbol: str
    faction: FactionSymbol

    Inherits `SpaceTradersAPIReqShape(TypeDict)`

    SpaceTraders API endpoints:
        - SpaceTradersAPIEndpoints.REGISTER (POST /register)
    """

    symbol: str
    faction: FactionSymbol


class AgentRegisterResData(SpaceTradersAPIResShape):
    """Represents the response data returned when registering an agent.

    token: AgentToken
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


class ChartCreateShape(SpaceTradersAPIResShape):
    """

    chart: ChartShape
    waypoint: SystemWaypointShape
    transaction: ShipTransactionShape
    agent: AgentShape
    """

    chart: ChartShape
    waypoint: SystemWaypointShape
    transaction: ShipTransactionShape
    agent: AgentShape


class MarketTransactionResShape(SpaceTradersAPIResShape):
    """

    cargo: ShipCargoShape
    transaction: MarketTransactionShape
    agent: AgentShape
    """

    cargo: ShipCargoShape
    transaction: MarketTransactionShape
    agent: AgentShape


class EventSubscribeReqShape(SpaceTradersAPIReqShape):
    action: str  # TODO: Make enum
    system_symbol: str
