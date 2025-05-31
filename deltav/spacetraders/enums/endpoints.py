from dataclasses import dataclass
from enum import Enum, unique
from http import HTTPMethod
from string import Template

from deltav.spacetraders.enums.token import TokenType
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models import ServerStatusShape
from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.faction import FactionShape
from deltav.spacetraders.models.ship import ShipCargoShape, ShipCooldownShape, ShipShape


@dataclass
class EndpointDataMixin:
    path: Template
    method: HTTPMethod
    token_type: TokenType
    request_shape: type[SpaceTradersAPIReqShape] | None
    response_shape: type[SpaceTradersAPIResShape] | None  # TODO: Remove None from type


@unique
class SpaceTradersAPIEndpoint(EndpointDataMixin, Enum):
    SERVER_STATUS = (
        Template('/'),
        HTTPMethod.GET,
        TokenType.NONE,
        None, 
        ServerStatusShape,
    )
    GET_AGENTS = (
        Template('/agents?page=$page&limit=$limit'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        AgentShape,
    )
    GET_AGENT = (
        Template('/agents/$param'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        AgentShape,
    )
    GET_FACTIONS = (
        Template('/factions'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        None,
    )
    GET_FACTION = (
        Template('/factions/$param'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        FactionShape,
    )
    MY_AGENT = (
        Template('/my/agent'), 
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        None,
    )
    MY_CONTRACTS = (
        Template('/my/contracts'), 
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        None,
    )
    MY_CONTRACT = (
        Template('/my/contracts/$param'), 
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        ContractShape,
    )
    ACCEPT_CONTRACT = (
        Template('/my/contracts/$param1/accept'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    DELIVER_CONTRACT = (
        Template('/my/contracts/$param1/deliver'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    FULFILL_CONTRACT = (
        Template('/my/contracts/$param1/fulfill'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS = (
        Template('/my/ships'), 
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        ShipShape,
    )
    MY_SHIP = (
        Template('/my/ships/$param'), 
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS_PURCHASE_SHIP = (
        Template('/my/ships'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS_CARGO = (
        Template('/my/ships/$param1/cargo'),
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        ShipCargoShape,
    )
    # Template('/my/ships/$param1/chart')
    MY_SHIPS_COOLDOWN = (
        Template('/my/ships/$param1/cooldown'),
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        ShipCooldownShape,
    )
    MY_SHIPS_DOCK = (
        Template('/my/ships/$param1/dock'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS_EXTRACT = (
        Template('/my/ships/$param1/extract'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    # Template('/my/ships/$param1/extract/survey')
    # Template('/my/ships/$param1/jettison')
    # Template('/my/ships/$param1/jump')
    # Template('/my/ships/$param1/mounts')
    # Template('/my/ships/$param1/mounts/install')
    # Template('/my/ships/$param1/mounts/remove')
    MY_SHIPS_NAV = (
        Template('/my/ships/$param1/nav'),
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIP_NAVIGATE = (
        Template('/my/ships/$param1/navigate'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    # Template('/my/ships/$param1/negotiate/contract')
    MY_SHIPS_ORBIT = (
        Template('/my/ships/$param1/orbit'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS_PURCHASE_CARGO = (
        Template('/my/ships/$param1/purchase'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    # Template('/my/ships/$param1/refine')
    # Template('/my/ships/$param1/refuel')
    MY_SHIPS_SCAN_SHIPS = (
        Template('/my/ships/$param1/scan/ships'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS_SCAN_SYSTEMS = (
        Template('/my/ships/$param1/scan/systems'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    MY_SHIPS_SCAN_WAYPOINTS = (
        Template('/my/ships/$param1/scan/waypoints'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
    # Template('/my/ships/$param1/sell')
    # Template('/my/ships/$param1/siphon')
    # Template('/my/ships/$param1/survey')
    # Template('/my/ships/$param1/transfer')
    # Template('/my/ships/$param1/warp')
    REGISTER = (
        Template('/register'), 
        HTTPMethod.POST,
        TokenType.NONE,
        None,
        None,
    )
    GET_SYSTEMS = (
        Template('/systems'), 
        HTTPMethod.POST,
        TokenType.NONE,
        None,
        None,
    )
    GET_SYSTEM = (
        Template('/systems/$param'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        None,
    )
    GET_WAYPOINTS = (
        Template('/systems/$param1/waypoints'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        None,
    )
    GET_WAYPOINT = (
        Template('/systems/$param1/waypoints/$param2'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        None,
    )
    # Template('/systems/$param1/waypoints/$param2/construction')
    # Template('/systems/$param1/waypoints/$param2/construction/supply')
    # Template('/systems/$param1/waypoints/$param2/jump-gate')
    # Template('/systems/$param1/waypoints/$param2/market')
    # Template('/systems/$param1/waypoints/$param2/shipyard')


    def with_params(self, params: list[str]) -> str:
        mapping = dict(zip(self.path.get_identifiers(), params))
        return self.path.substitute(mapping)


    def with_paging(self, page: int, limit: int) -> str:
        return self.path.substitute(page=page, limit=limit)

