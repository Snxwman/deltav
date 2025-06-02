from __future__ import annotations

from deltav.spacetraders.models import SpaceTradersAPIResShape
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


class RegisterShape(SpaceTradersAPIResShape):


class AgentsShape(SpaceTradersAPIResShape):
    agents: list[PublicAgentShape]


class MyAgentEventsShape(SpaceTradersAPIResShape):
    events: list[EventShape]


class MyContractsShape(SpaceTradersAPIResShape):
    contracts: list[ContractShape]


class AcceptContractShape(SpaceTradersAPIResShape):
    contract: ContractShape
    agent: AgentShape


class MarketTransactionShape(SpaceTradersAPIResShape):
    cargo: ShipCargoShape
    transaction: TransactionShape
    agent: AgentShape


class ContractSuccessfulDeliveryShape(SpaceTradersAPIResShape):
    contract: ContractShape
    cargo: ShipCargoShape


class NavigateResponseShape(SpaceTradersAPIResShape):
    nav: ShipNavShape
    fuel: ShipFuelShape
    event: EventShape | None


class WaypointScanShape(SpaceTradersAPIResShape):
    cooldown: ShipCooldownShape
    waypoints: list[WaypointShape]

