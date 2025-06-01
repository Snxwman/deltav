from dataclasses import dataclass
from enum import Enum, unique
from http import HTTPMethod
from string import Template

from deltav.spacetraders.enums.token import TokenType
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape
from deltav.spacetraders.models import ServerStatusShape
from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.endpoint import AcceptContractShape, MarketTransactionShape, NavigateResponseShape, ShipJumpWaypointShape, WaypointScanShape
from deltav.spacetraders.models.faction import FactionShape
from deltav.spacetraders.models.market import CargoItemShape, TransactionShape
from deltav.spacetraders.models.ship import ShipCreateChartShape, ShipExtractSurveyResponseShape, ShipExtractSurveyShape, ShipJumpShape, ShipPurchaseShape, ShipCargoShape, ShipCooldownShape, ShipRefineResponseShape, ShipRefineShape, ShipRefuelResponseShape, ShipRefuelShape, ShipShape
from deltav.spacetraders.models.systems import ConstructionSiteShape, JumpgateShape, MarketShape, ShipyardShape, SupplyConstructionSiteResponseShape, SupplyConstructionSiteShape, SystemShape, SystemWaypointShape
from deltav.spacetraders.models.waypoint import WaypointNavigateShape


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
        AcceptContractShape,
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
        ShipShape,
    )
    MY_SHIPS_PURCHASE_SHIP = (
        Template('/my/ships'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        ShipPurchaseShape,
    )
    MY_SHIPS_CARGO = (
        Template('/my/ships/$param1/cargo'),
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        ShipCargoShape,
    )
    MY_SHIPS_CREATE_CHART = (
        Template('/my/ships/$param1/chart'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        ShipCreateChartShape,
    )
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
        CargoItemShape,
    )
    MY_SHIPS_EXTRACT_SURVEY = (
        Template('/my/ships/$param1/extract/survey'),
        HTTPMethod.POST,
        TokenType.AGENT,
        ShipExtractSurveyShape,
        ShipExtractSurveyResponseShape,
    )
    MY_SHIPS_JETTISON = (
        Template('/my/ships/$param1/jettison'),
        HTTPMethod.POST,
        TokenType.AGENT,
        CargoItemShape,
        None,
    )
    MY_SHIPS_JUMP = (
        Template('/my/ships/$param1/jump'),
        HTTPMethod.POST,
        TokenType.AGENT,
        ShipJumpWaypointShape,
        ShipJumpShape,
    )
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
        WaypointNavigateShape,
        NavigateResponseShape,
    )
    MY_SHIPS_NEGOTIATE_CONTRACT = (
        Template('/my/ships/$param1/negotiate'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
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
        CargoItemShape,
        MarketTransactionShape,
    )
    MY_SHIPS_REFINE = (
        Template('/my/ships/$param1/refine'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        ShipRefineShape,
        ShipRefineResponseShape,
    )
    MY_SHIPS_REFUEL = (
        Template('/my/ships/$param1/refuel'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        ShipRefuelShape,
        ShipRefuelResponseShape,
    )
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
        WaypointScanShape,
    )
    MY_SHIPS_SELL = (
        Template('/my/ships/$param1/sell'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        CargoItemShape,
        TransactionShape,
    )
    
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
    SYSTEM_GET_SYSTEMS = (
        Template('/systems'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        None,
    )
    SYSTEM_GET_SYSTEM = (
        Template('/systems/$param'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        SystemShape,
    )
    SYSTEM_GET_WAYPOINTS = (
        Template('/systems/$param1/waypoints'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        None,
    )
    SYSTEM_GET_WAYPOINT = (
        Template('/systems/$param1/waypoints/$param2'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        SystemWaypointShape,
    )
    SYSTEM_GET_CONSTRUCTION_SITE = (
        Template('/systems/$param1/waypoints/$param2/construction'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        ConstructionSiteShape,
    )
    SYSTEM_SUPPLY_CONSTRUCTION_SITE = (
        Template('/systems/$param1/waypoints/$param2/construction/supply'), 
        HTTPMethod.POST,
        TokenType.AGENT,
        SupplyConstructionSiteShape,
        SupplyConstructionSiteResponseShape,
    )
    GET_JUMPGATE = (
        Template('/systems/$param1/waypoints/$param2/jumpgate'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        JumpgateShape,
    )
    GET_MARKET = (
        Template('/systems/$param1/waypoints/$param2/market'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        MarketShape,
    )
    GET_SHIPYARD = (
        Template('/systems/$param1/waypoints/$param2/shipyard'), 
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        ShipyardShape,
    )


    def with_params(self, params: list[str]) -> str:
        mapping = dict(zip(self.path.get_identifiers(), params))
        return self.path.substitute(mapping)


    def with_paging(self, page: int, limit: int) -> str:
        return self.path.substitute(page=page, limit=limit)

