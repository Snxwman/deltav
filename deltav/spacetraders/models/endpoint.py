from __future__ import annotations

from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.account import AccountShape
from deltav.spacetraders.models.agent import AgentShape, PublicAgentShape
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.event import EventShape
from deltav.spacetraders.models.faction import FactionShape
from deltav.spacetraders.models.ship import ShipShape


class MyAccountShape(SpaceTradersAPIResShape):
    account: AccountShape


class RegisterShape(SpaceTradersAPIResShape):
    token: str
    agent: AgentShape
    faction: FactionShape
    contract: ContractShape
    ships: list[ShipShape]


class AgentsShape(SpaceTradersAPIResShape):
    agents: list[PublicAgentShape]


class MyAgentEventsShape(SpaceTradersAPIResShape):
    events: list[EventShape]


class MyContractsShape(SpaceTradersAPIResShape):
    contracts: list[ContractShape]

