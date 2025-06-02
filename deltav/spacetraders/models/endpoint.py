from __future__ import annotations

from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models.account import AccountShape
from deltav.spacetraders.models.agent import AgentShape, PublicAgentShape
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.event import EventShape
from deltav.spacetraders.models.faction import FactionShape
from deltav.spacetraders.models.market import TransactionShape
from deltav.spacetraders.models.ship import ShipCargoShape, ShipCooldownShape, ShipFuelShape, ShipNavShape, ShipShape
from deltav.spacetraders.models.waypoint import WaypointShape


class MyAccountShape(SpaceTradersAPIResShape):
    account: AccountShape


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


class AgentsShape(SpaceTradersAPIResShape):
    """

    agents: list[PublicAgentShape]
    """

    agents: list[PublicAgentShape]


class MyAgentEventsShape(SpaceTradersAPIResShape):
    """

    events: list[EventShape]
    """

    events: list[EventShape]


class MyContractsShape(SpaceTradersAPIResShape):
    """

    contracts: list[ContractShape]
    """

    contracts: list[ContractShape]


class AcceptContractShape(SpaceTradersAPIResShape):
    """

    contract: ContractShape
    agent: AgentShape
    """

    contract: ContractShape
    agent: AgentShape


class MarketTransactionShape(SpaceTradersAPIResShape):
    """

    cargo: ShipCargoShape
    transaction: TransactionShape
    agent: AgentShape
    """

    cargo: ShipCargoShape
    transaction: TransactionShape
    agent: AgentShape


class NavigateResponseShape(SpaceTradersAPIResShape):
    """

    nav: ShipNavShape
    fuel: ShipFuelShape
    event: EventShape | None
    """

    nav: ShipNavShape
    fuel: ShipFuelShape
    event: EventShape | None


class WaypointScanShape(SpaceTradersAPIResShape):
    """

    cooldown: ShipCooldownShape
    waypoints: list[WaypointShape]
    """

    cooldown: ShipCooldownShape
    waypoints: list[WaypointShape]


class ShipJumpWaypointShape(SpaceTradersAPIResShape):
    """

    waypointSymbol: str
    """

    waypointSymbol: str
