from dataclasses import dataclass
from enum import Enum, unique
from http import HTTPMethod
from string import Template

from deltav.spacetraders.enums.token import TokenType
from deltav.spacetraders.models import (
    ErrorCodesShape,
    ServerStatusShape,
    SpaceTradersAPIReqShape,
    SpaceTradersAPIResShape,
)
from deltav.spacetraders.models.account import AccountShape
from deltav.spacetraders.models.agent import (
    AgentEventShape,
    AgentShape,
    PublicAgentShape,
    RegisterAgentReqData,
    RegisterAgentResData,
)
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.endpoint import AcceptContractShape, MarketTransactionShape, NavigateResponseShape
from deltav.spacetraders.models.faction import FactionShape
from deltav.spacetraders.models.market import CargoItemShape, TransactionShape
from deltav.spacetraders.models.ship import ShipCargoShape, ShipCooldownShape, ShipShape
from deltav.spacetraders.models.waypoint import WaypointNavigateShape


@dataclass
class EndpointDataMixin:
    path: Template
    method: HTTPMethod
    token_type: TokenType
    request_shape: type[SpaceTradersAPIReqShape] | None
    response_shape: type[SpaceTradersAPIResShape] | None  # TODO: Remove None from type
    # TODO: Add success response codes in?
    # TODO: Add a paginated: bool field?


@unique
class SpaceTradersAPIEndpoint(EndpointDataMixin, Enum):
    """Enum of all the SpaceTrader API endpoints.

    Mixin:
    path: Template
    method: HTTPMethod
    token_type: TokenType
    request_shape: type[SpaceTradersAPIReqShape] | None
    response_shape: type[SpaceTradersAPIResShape] | None
    """

    SERVER_STATUS = (
        Template('/'),
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        ServerStatusShape,
    )
    """Return the status of the game server. This also includes a few global
    elements, such as announcements, server reset dates and leaderboards.

    Endpoint: GET /
    Required token: TokenType.NONE
    Request shape: none
    Response shape: ServerStatusShape
    """
    ERROR_CODES = (
        Template('/error-codes'),
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        ErrorCodesShape,
    )
    """Return a list of all possible error codes thrown by the game server.

    Endpoint: GET /error-codes
    Required token: TokenType.None
    Request shape: none
    Response shape: ErrorCodesShape
    """
    GET_ACCOUNT = (
        Template('/my/account'),
        HTTPMethod.GET,
        TokenType.ACCOUNT,
        None,
        AccountShape,
    )
    """Fetch your account details.

    Endpoint: GET /my/account
    Required token: TokenType.ACCOUNT
    Request shape: none
    Response shape: AccountShape
    Response codes: 200 Ok
    """
    REGISTER = (
        Template('/register'),
        HTTPMethod.POST,
        TokenType.ACCOUNT,
        RegisterAgentReqData,
        RegisterAgentResData,
    )
    """Creates a new agent and ties it to an account.

    Endpoint: GET /register
    Required token: TokenType.ACCOUNT
    Request shape: RegisterAgentReqData
    Response shape: RegisterAgentResData
    Response codes: 201 Created

    Additional details:
    The agent symbol must consist of a 3-14 character string, and will be used
    to represent your agent. This symbol will prefix the symbol of every ship
    you own. Agent symbols will be cast to all uppercase characters.

    This new agent will be tied to a starting faction of your choice, which
    determines your starting location, and will be granted an authorization
    token, a contract with their starting faction, a command ship that can fly
    across space with advanced capabilities, a small probe ship that can be
    used for reconnaissance, and 175,000 credits.
    """
    GET_AGENTS = (
        Template('/agents?page=$page&limit=$limit'),
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        AgentShape,
    )
    """List all public agent details.

    Endpoint: GET /agents?page={page}&limit={limit}
    Required token: TokenType.NONE
    Request shape: none
    Response shape: ErrorCodesShape
    Response codes: 200 Ok

    Additional details:
    Page - default: 1, min: 1
    Limit - default: 10, min: 1, max: 20
    """
    GET_AGENT = (
        Template('/agents/$param'),
        HTTPMethod.GET,
        TokenType.NONE,
        None,
        PublicAgentShape,
    )
    """Get public details for a specific agent.

    Endpoint: GET /agents/{agentSymbol}
    Required token: TokenType.NONE
    Request shape: none
    Response shape: PublicAgentShape
    Response codes: 200 Ok
    """
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
    """Fetch your agent's details.

    Endpoint: GET /my/agent
    Required token: TokenType.AGENT
    Request shape: none
    Response shape: AgentShape
    Response codes: 200 Ok
    """
    MY_AGENT_EVENTS = (
        Template('/my/agent/events'),
        HTTPMethod.GET,
        TokenType.AGENT,
        None,
        AgentEventShape,
    )
    """Get recent events for your agent.

    Endpoint: GET /my/agent/events
    Required token: TokenType.AGENT
    Request shape: none
    Response shape: AgentEventShape
    Response codes: 200 Ok
    """
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
        None,
    )
    MY_SHIPS_PURCHASE_SHIP = (
        Template('/my/ships'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        MarketTransactionShape,
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
    MY_SHIPS_JETTISON = (
        Template('/my/ships/$param1/jettison'),
        HTTPMethod.POST,
        TokenType.AGENT,
        None,
        None,
    )
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
        WaypointNavigateShape,
        NavigateResponseShape,
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
