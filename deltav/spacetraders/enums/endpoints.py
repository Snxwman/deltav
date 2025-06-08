from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum, unique
from http import HTTPMethod, HTTPStatus
from string import Template
from typing import override

from pydantic import BaseModel

from deltav.spacetraders.models import (
    ErrorCodesShape,
    EventSubscribeReqShape,
    MarketSupplyChainShape,
    NoDataReqShape,
    NoDataResShape,
    ServerStatusShape,
    SpaceTradersAPIReqShape,
    SpaceTradersAPIResShape,
)
from deltav.spacetraders.models.account import AccountShape
from deltav.spacetraders.models.agent import (
    AgentEventShape,
    AgentShape,
    PublicAgentShape,
    PublicAgentsShape,
)
from deltav.spacetraders.models.construction import (
    ConstructionShape,
    ConstructionSupplyReqShape,
    ConstructionSupplyResShape,
)
from deltav.spacetraders.models.contract import (
    ContractAcceptShape,
    ContractDeliverReqShape,
    ContractDeliverResShape,
    ContractShape,
    ContractsShape,
)
from deltav.spacetraders.models.endpoint import (
    AgentRegisterReqData,
    AgentRegisterResData,
    ChartCreateShape,
)
from deltav.spacetraders.models.faction import FactionShape, FactionsShape
from deltav.spacetraders.models.market import MarketShape, TransactionShape
from deltav.spacetraders.models.ship import (
    CargoItemReqShape,
    CargoItemResShape,
    ScanShipsShape,
    ScanSystemsShape,
    ScanWaypointsShape,
    ShipCargoShape,
    ShipCargoTransferReqShape,
    ShipCooldownShape,
    ShipExtractionShape,
    ShipFlightModeShape,
    ShipModifyModuleShape,
    ShipModifyMountShape,
    ShipModuleShape,
    ShipModuleSymbolShape,
    ShipMountShape,
    ShipMountSymbolShape,
    ShipNavigationShape,
    ShipNavShape,
    ShipNavUpdateShape,
    ShipPurchaseReqShape,
    ShipPurchaseResShape,
    ShipRefineReqShape,
    ShipRefineResShape,
    ShipRefuelReqShape,
    ShipRefuelResShape,
    ShipRepairShape,
    ShipScrapShape,
    ShipScrapTransactionShape,
    ShipShape,
    ShipsShape,
    SiphonResShape,
    SurveyCreateShape,
    SurveyReqShape,
)
from deltav.spacetraders.models.systems import (
    JumpgateShape,
    ShipyardShape,
    SystemShape,
    SystemWaypointShape,
    SystemWaypointsShape,
    SystemsShape,
)
from deltav.spacetraders.models.waypoint import (
    WaypointSymbolReqShape,
)
from deltav.spacetraders.token import AccountToken, AgentToken, Token
from deltav.util import generic__repr__


@dataclass
class EndpointDataMixin:
    path: Template
    method: HTTPMethod
    token_type: type[AccountToken] | type[AgentToken] | None
    request_shape: type[SpaceTradersAPIReqShape]
    response_shapes: Mapping[HTTPStatus, type[SpaceTradersAPIResShape]]
    paginated: bool

    @property
    def response_codes(self) -> list[HTTPStatus]:
        return list(self.response_shapes.keys())

    def response_shape(self, status: HTTPStatus) -> type[SpaceTradersAPIResShape]:
        return self.response_shapes[status]

    @override
    def __repr__(self) -> str:
        return generic__repr__(self)

    @override
    def __str__(self) -> str:
        def shape_str(s: type[BaseModel]) -> str:
            fields_str = ''.join(
                f'\n\t\t{f}: {t}'
                for f, t in s.__annotations__.items()  # pyright: ignore[reportAny]
            )
            return f'{s.__name__}{fields_str}'

        request_shape = (
            '\n\t\tnone' if self.request_shape is NoDataReqShape else shape_str(self.request_shape)
        )
        response_shape = '\n'.join(shape_str(shape) for shape in self.response_shapes.values())

        return '\n\t'.join([
            f'{self.__class__.__name__}',
            f'HTTP Method: {self.method}',
            f'Path Template: {self.path.template}',
            f'Required Token: {self.token_type}',
            f'Request Shape: {request_shape}',
            f'Response Shape: {response_shape}',
        ])  # fmt: skip


@unique
class SpaceTradersAPIEndpoint(EndpointDataMixin, Enum):
    """Enum of all the SpaceTrader API endpoints.

    EndpointDataMixin:
    ```
    path: Template
    method: HTTPMethod
    token_type: type[AccountToken] | type[AgentToken] | None
    request_shape: type[SpaceTradersAPIReqShape]
    response_shapes: Mapping[HTTPStatus, type[SpaceTradersAPIResShape]]
    paginated: bool

    (property) response_codes: list[HTTPStatus]

    response_shape(HTTPStatus) -> type[SpaceTradersAPIResShape]
    ```
    """

    MY_ACCOUNT = (
        Template('/my/account'),
        HTTPMethod.GET,
        AccountToken,
        NoDataReqShape,
        {HTTPStatus.OK: AccountShape},
        False,
    )
    """Fetch your account details.

    ```
    Template('/my/account'),
    HTTPMethod.GET,
    AccountToken,
    NoDataReqShape,
    {HTTPStatus.OK: AccountShape},
    False,
    ```
    """
    REGISTER_AGENT = (
        Template('/register'),
        HTTPMethod.POST,
        AccountToken,
        AgentRegisterReqData,
        {HTTPStatus.CREATED: AgentRegisterResData},
        False,
    )
    """Creates a new agent and ties it to an account.

    ```
    Template('/register'),
    HTTPMethod.POST,
    AccountToken,
    RegisterAgentReqData,
    {HTTPStatus.CREATED: RegisterAgentResData},
    False,
    ```
    """
    GET_ALL_AGENTS = (
        Template('/agents'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: PublicAgentsShape},
        False,
    )
    """List all public agent details.

    ```
    Template('/agents'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: list[PublicAgentShape]},
    False,
    ```
    """
    GET_PUBLIC_AGENT = (
        Template('/agents/$agent_symbol'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: PublicAgentShape},
        False,
    )
    """Get public details for a specific agent.

    ```
    Template('/agents/$agent_symbol'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: PublicAgentShape},
    False,
    ```
    """
    GET_AGENT = (
        Template('/my/agent'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: AgentShape},
        False,
    )
    """Fetch your agent's details.

    ```
    Template('/my/agent'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: UnknownResShape},
    False,
    ```
    """
    MY_AGENT_EVENTS = (
        Template('/my/agent/events'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: AgentEventShape},
        False,
    )
    """Get recent events for your agent.

    ```
    Template('/my/agent/events'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: AgentEventShape},
    False,
    ```
    """
    MY_CONTRACTS = (
        Template('/my/contracts'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ContractsShape},
        True,
    )
    """Return a paginated list of all your contracts.

    ```
    Template('/my/contracts'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ContractsShape},
    True,
    ```
    """
    GET_CONTRACT = (
        Template('/my/contracts/$contract_id'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ContractShape},
        False,
    )
    """Get the details of a specific contract.

    ```
    Template('/my/contracts/$contract_id'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ContractShape},
    False,
    ```
    """
    ACCEPT_CONTRACT = (
        Template('/my/contracts/$contract_id/accept'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ContractAcceptShape},
        False,
    )
    """Accept a contract by ID.

    ```
    Template('/my/contracts/$contract_id/accept'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: AcceptContractShape},
    False,
    ```
    """
    FULFILL_CONTRACT = (
        Template('/my/contracts/$contract_id/fulfill'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ContractShape},  # FIX: shape
        False,
    )
    """Fulfill a contract.

    ```
    Template('/my/contracts/$contract_id/fulfill'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: UnknownResShape},  # FIX: shape
    False,
    ```
    """
    DELIVER_CONTRACT = (
        Template('/my/contracts/$contract_id/deliver'),
        HTTPMethod.POST,
        AgentToken,
        ContractDeliverReqShape,
        {HTTPStatus.OK: ContractDeliverResShape},
        False,
    )
    """Deliver cargo to a contract.

    ```
    Template('/my/contracts/$contract_id/deliver'),
    HTTPMethod.POST,
    AgentToken,
    ContractDeliverReqShape,
    {HTTPStatus.OK: ContractDeliverResShape},
    False,
    ```
    """
    NEGOTIATE_CONTRACT = (
        Template('/my/ships/$ship_symbol/negotiate/contract'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: ContractShape},
        False,
    )
    """Negotiate a new contract with the HQ.

    ```
    Template('/my/ships/$ship_symbol/negotiate/contract'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: ContractShape},
    False,
    ```
    """
    GET_ALL_FACTIONS = (
        Template('/factions'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: FactionsShape},
        True,
    )
    """Return a paginated list of all the factions in the game.

    ```
    Template('/factions'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: FactionsShape},
    True,
    ```
    """
    GET_FACTION = (
        Template('/factions/$faction_symbol'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: FactionShape},
        False,
    )
    """View the details of a faction.

    ```
    Template('/factions/$faction_symbol'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: FactionShape},
    False,
    ```
    """
    MY_FACTION = (
        Template('/my/faction'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: FactionShape},
        False,
    )
    """Retrieve factions with which the agent has reputation.

    ```
    Template('/my/faction'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: FactionShape},
    False,
    ```
    """
    MY_SHIPS = (
        Template('/my/ships'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipsShape},
        True,
    )
    """Return a paginated list of all of ships under your agent's ownership.

    ```
    Template('/my/ships'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipsShape},
    True,
    ```
    """
    PURCHASE_SHIP = (
        Template('/my/ships'),
        HTTPMethod.POST,
        AgentToken,
        ShipPurchaseReqShape,
        {HTTPStatus.CREATED: ShipPurchaseResShape},
        False,
    )
    """Purchase a ship from a Shipyard.

    ```
    Template('/my/ships'),
    HTTPMethod.POST,
    AgentToken,
    ShipPurchaseReqShape,
    {HTTPStatus.CREATED: ShipPurchaseResShape},
    False,
    ```
    """
    MY_SHIP = (
        Template('/my/ships/$ship_symbol'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipShape},
        False,
    )
    """Retrieve the details of a ship under your agent's ownership.

    ```
    Template('/my/ships/$ship_symbol'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipShape},
    False,
    ```
    """
    CREATE_CHART = (
        Template('/my/ships/$ship_symbol/chart'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: ChartCreateShape},
        False,
    )
    """Command a ship to chart the waypoint at its current location.

    ```
    Template('/my/ships/$ship_symbol/chart'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: ShipCreateChartShape},
    False,
    ```
    """
    # INFO: Duplicate
    #
    # NEGOTIATE_CONTRACT = (
    #     Template('/my/ships/$ship_symbol/negotiate/contract'),
    #     AgentToken,
    #     {HTTPMethod.POST: NoDataReqShape},
    #     {HTTPStatus.CREATED: ContractShape},
    #     False,
    # )
    # """Negotiate a new contract with the HQ.
    #
    # ```
    # Template('/my/ships/$ship_symbol/negotiate/contract'),
    # AgentToken,
    # {HTTPMethod.POST: NoDataReqShape},
    # {HTTPStatus.CREATED: ContractShape},
    # False,
    # ```
    # """
    GET_SHIP_COOLDOWN = (
        Template('/my/ships/$ship_symbol/cooldown'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {
            HTTPStatus.OK: ShipCooldownShape,
            HTTPStatus.NO_CONTENT: NoDataResShape,
        },
        False,
    )
    """Retrieve the details of your ship's reactor cooldown.

    `HTTPStatus.OK`: Sucessfully fetched ship's cooldown.
    `HTTPStatus.NO_CONTENT`: No cooldown.

    ```
    Template('/my/ships/$ship_symbol/cooldown'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {
        HTTPStatus.OK: ShipCooldownShape,
        HTTPStatus.NO_CONTENT: NoDataResShape,
    },
    False,
    ```
    """
    DOCK_SHIP = (
        Template('/my/ships/$ship_symbol/dock'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipNavShape},
        False,
    )
    """Attempt to dock your ship at its current location.

    ```
    Template('/my/ships/$ship_symbol/dock'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipNavShape},
    False,
    ```
    """
    EXTRACT_RESOURCES = (
        Template('/my/ships/$ship_symbol/extract'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: ShipExtractionShape},
        False,
    )
    """Extract resources from a waypoint that can be extracted, such as
    asteroid fields, into your ship.

    ```
    Template('/my/ships/$ship_symbol/extract'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: ShipExtractionShape},
    False,
    ```
    """
    EXTRACT_RESOURCES_WITH_SURVEY = (
        Template('/my/ships/$ship_symbol/extract/survey'),
        HTTPMethod.POST,
        AgentToken,
        SurveyReqShape,
        {HTTPStatus.CREATED: ShipExtractionShape},
        False,
    )
    """Use a survey when extracting resources from a waypoint.

    ```
    Template('/my/ships/$ship_symbol/extract/survey'),
    HTTPMethod.POST,
    AgentToken,
    SurveyReqShape,
    {HTTPStatus.CREATED: ExtractionShape},
    False,
    ```
    """
    JETTISON_CARGO = (
        Template('/my/ships/$ship_symbol/jettison'),
        HTTPMethod.POST,
        AgentToken,
        CargoItemReqShape,
        {HTTPStatus.OK: ShipCargoShape},
        False,
    )
    """Jettison cargo from your ship's cargo hold.

    ```
    Template('/my/ships/$ship_symbol/jettison'),
    HTTPMethod.POST,
    AgentToken,
    CargoItemReqShape,
    {HTTPStatus.OK: ShipCargoShape},
    False,
    ```
    """
    JUMP_SHIP = (
        Template('/my/ships/$ship_symbol/jump'),
        HTTPMethod.POST,
        AgentToken,
        WaypointSymbolReqShape,
        {HTTPStatus.OK: TransactionShape},
        False,
    )
    """Jump your ship instantly to a target connected waypoint.

    ```
    Template('/my/ships/$ship_symbol/jump'),
    HTTPMethod.POST,
    AgentToken,
    WaypointNavigateReqShape,
    {HTTPStatus.OK: TransactionShape},
    False,
    ```
    """
    SCAN_SYSTEMS = (
        Template('/my/ships/$ship_symbol/scan/systems'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: ScanSystemsShape},
        False,
    )
    """Scan for nearby systems, retrieving information on the systems' distance
    from the ship and their waypoints.

    ```
    Template('/my/ships/$ship_symbol/scan/systems'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: ScanSystemsShape},
    False,
    ```
    """
    SCAN_WAYPOINTS = (
        Template('/my/ships/$ship_symbol/scan/waypoints'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: ScanWaypointsShape},
        False,
    )
    """Scan for nearby waypoints, retrieving detailed information on each
    waypoint in range.

    ```
    Template('/my/ships/$ship_symbol/scan/waypoints'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: WaypointScanShape},
    False,
    ```
    """
    SCAN_SHIPS = (
        Template('/my/ships/$ship_symbol/scan/ships'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: ScanShipsShape},
        False,
    )
    """Scan for nearby ships, retrieving information for all ships in range.

    ```
    Template('/my/ships/$ship_symbol/scan/ships'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: ScanShipsShape},
    False,
    ```
    """
    SCRAP_SHIP = (
        Template('/my/ships/$ship_symbol/scrap'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipScrapShape},
        False,
    )
    """Scrap a ship, removing it from the game and receiving a portion of the
    ship's value back in credits.

    ```
    Template('/my/ships/$ship_symbol/scrap'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipScrapedShape},
    False,
    ```
    """
    GET_SHIP_SCRAP_VALUE = (
        Template('/my/ships/$ship_symbol/scrap'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipScrapTransactionShape},
        False,
    )
    """Get the value of scrapping a ship.

    ```
    Template('/my/ships/$ship_symbol/scrap'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipTransactionShape},
    False,
    ```
    """
    NAVIGATE_SHIP = (
        Template('/my/ships/$ship_symbol/navigate'),
        HTTPMethod.POST,
        AgentToken,
        WaypointSymbolReqShape,
        {HTTPStatus.OK: ShipNavigationShape},
        False,
    )
    """Navigate to a target destination.

    ```
    Template('/my/ships/$ship_symbol/navigate'),
    HTTPMethod.POST,
    AgentToken,
    WaypointSymbolReqShape,
    {HTTPStatus.OK: ShipNavigationShape},
    False,
    ```
    """
    WARP_SHIP = (
        Template('/my/ships/$ship_symbol/warp'),
        HTTPMethod.POST,
        AgentToken,
        WaypointSymbolReqShape,
        {HTTPStatus.OK: ShipNavigationShape},
        False,
    )
    """Warp your ship to a target destination in another system.

    ```
    Template('/my/ships/$ship_symbol/warp'),
    HTTPMethod.POST,
    AgentToken,
    WaypointSymbolReqShape,
    {HTTPStatus.OK: ShipNavigationShape},
    False,
    ```
    """
    ORBIT_SHIP = (
        Template('/my/ships/$ship_symbol/orbit'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipNavShape},
        False,
    )
    """Attempt to move your ship into orbit at its current location.

    ```
    Template('/my/ships/$ship_symbol/orbit'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipNavShape},
    False,
    ```
    """
    PURCHASE_CARGO = (
        Template('/my/ships/$ship_symbol/purchase'),
        HTTPMethod.POST,
        AgentToken,
        CargoItemReqShape,
        {HTTPStatus.CREATED: TransactionShape},
        False,
    )
    """Purchase cargo from a market.

    ```
    Template('/my/ships/$ship_symbol/purchase'),
    HTTPMethod.POST,
    AgentToken,
    CargoItemReqShape,
    {HTTPStatus.CREATED: MarketTransactionShape},
    False,
    ```
    """
    REFINE_MATERIALS = (
        Template('/my/ships/$ship_symbol/refine'),
        HTTPMethod.POST,
        AgentToken,
        ShipRefineReqShape,
        {HTTPStatus.CREATED: ShipRefineResShape},
        False,
    )
    """Attempt to refine the raw materials on your ship.

    ```
    Template('/my/ships/$ship_symbol/refine'),
    HTTPMethod.POST,
    AgentToken,
    ShipRefineReqShape,
    {HTTPStatus.CREATED: ShipRefineResShape},
    False,
    ```
    """
    REFUEL_SHIP = (
        Template('/my/ships/$ship_symbol/refuel'),
        HTTPMethod.POST,
        AgentToken,
        ShipRefuelReqShape,
        {HTTPStatus.OK: ShipRefuelResShape},
        False,
    )
    """Refuel your ship by buying fuel from the local market.

    ```
    Template('/my/ships/$ship_symbol/refuel'),
    HTTPMethod.POST,
    AgentToken,
    ShipRefuelReqShape,
    {HTTPStatus.OK: ShipRefuelResShape},
    False,
    ```
    """
    REPAIR_SHIP = (
        Template('/my/ships/$ship_symbol/repair'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipRepairShape},
        False,
    )
    """Repair a ship, restoring the ship to maximum condition.

    ```
    Template('/my/ships/$ship_symbol/repair'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipRepairShape},
    False,
    ```
    """
    GET_SHIP_REPAIR_COST = (
        Template('/my/ships/$ship_symbol/repair'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipScrapTransactionShape},
        False,
    )
    """Get the cost of repairing a ship.

    ```
    Template('/my/ships/$ship_symbol/repair'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipTransactionShape},
    False,
    ```
    """
    SELL_CARGO = (
        Template('/my/ships/$ship_symbol/sell'),
        HTTPMethod.POST,
        AgentToken,
        CargoItemReqShape,
        {HTTPStatus.CREATED: TransactionShape},
        False,
    )
    """Sell cargo in your ship to a market that trades this cargo.

    ```
    Template('/my/ships/$ship_symbol/sell'),
    HTTPMethod.POST,
    AgentToken,
    CargoItemReqShape,
    {HTTPStatus.CREATED: MarketTransactionShape},
    False,
    ```
    """
    SIPHON_RESOURCES = (
        Template('/my/ships/$ship_symbol/siphon'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: SiphonResShape},
        False,
    )
    """Siphon gases or other resources from gas giants.

    ```
    Template('/my/ships/$ship_symbol/siphon'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: SiphonResShape},
    False,
    ```
    """
    CREATE_SURVEY = (
        Template('/my/ships/$ship_symbol/survey'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.CREATED: SurveyCreateShape},
        False,
    )
    """Create surveys on a waypoint that can be extracted such as asteroid
    fields.

    ```
    Template('/my/ships/$ship_symbol/survey'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.CREATED: CreateSurveyShape},
    False,
    ```
    """
    TRANSFER_CARGO = (
        Template('/my/ships/$ship_symbol/transfer'),
        HTTPMethod.POST,
        AgentToken,
        ShipCargoTransferReqShape,
        {HTTPStatus.OK: CargoItemResShape},
        False,
    )
    """Transfer cargo between ships.

    ```
    Template('/my/ships/$ship_symbol/transfer'),
    HTTPMethod.POST,
    AgentToken,
    CargoTransferReqShape,
    {HTTPStatus.OK: CargoItemResShape},
    False,
    False,
    ```
    """
    GET_SHIP_CARGO = (
        Template('/my/ships/$ship_symbol/cargo'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipCargoShape},
        False,
    )
    """Retrieve the cargo of a ship under your agent's ownership.

    ```
    Template('/my/ships/$ship_symbol/cargo'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipCargoShape},
    False,
    ```
    """
    GET_SHIP_MODULES = (
        Template('/my/ships/$ship_symbol/modules'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipModuleShape},
        False,
    )
    """Get the modules installed on a ship.
    ```
    Template('/my/ships/$ship_symbol/modules'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipModuleShape},
    False,
    """
    INSTALL_MODULE = (
        Template('/my/ships/$ship_symbol/modules/install'),
        HTTPMethod.POST,
        AgentToken,
        ShipModuleSymbolShape,
        {HTTPStatus.CREATED: ShipModifyModuleShape},
        False,
    )
    """Install a module on a ship.

    ```
    Template('/my/ships/$ship_symbol/modules/install'),
    HTTPMethod.POST,
    AgentToken,
    ModuleSymbolShape,
    {HTTPStatus.CREATED: ShipModifyModuleShape},
    False,
    ```
    """
    REMOVE_MODULE = (
        Template('/my/ships/$ship_symbol/modules/remove'),
        HTTPMethod.POST,
        AgentToken,
        ShipModuleSymbolShape,
        {HTTPStatus.CREATED: ShipModifyModuleShape},
        False,
    )
    """Remove a module from a ship.

    ```
    Template('/my/ships/$ship_symbol/modules/remove'),
    HTTPMethod.POST,
    AgentToken,
    ModuleSymbolShape,
    {HTTPStatus.CREATED: ShipModifyModuleShape},
    False,
    ```
    """
    GET_MOUNTS = (
        Template('/my/ships/$ship_symbol/mounts'),
        HTTPMethod.POST,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipMountShape},
        False,
    )
    """Get the mounts installed on a ship.

    ```
    Template('/my/ships/$ship_symbol/mounts'),
    HTTPMethod.POST,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipMountsShape},
    False,
    ```
    """
    INSTALL_MOUNT = (
        Template('/my/ships/$ship_symbol/mounts/install'),
        HTTPMethod.POST,
        AgentToken,
        ShipMountSymbolShape,
        {HTTPStatus.CREATED: ShipModifyMountShape},
        False,
    )
    """Install a mount on a ship.

    ```
    Template('/my/ships/$ship_symbol/mounts/install'),
    HTTPMethod.POST,
    AgentToken,
    ShipMountSymbolShape,
    {HTTPStatus.OK: ShipModifyMountShape},
    False,
    ```
    """
    REMOVE_MOUNT = (
        Template('/my/ships/$ship_symbol/mounts/remove'),
        HTTPMethod.POST,
        AgentToken,
        ShipMountSymbolShape,
        {HTTPStatus.CREATED: ShipModifyMountShape},
        False,
    )
    """Remove a mount from a ship.

    ```
    Template('/my/ships/$ship_symbol/mounts/install'),
    HTTPMethod.POST,
    AgentToken,
    ShipMountSymbolShape,
    {HTTPStatus.OK: ShipModifyMountShape},
    False,
    ```
    """
    GET_NAV_STATUS = (
        Template('/my/ships/$ship_symbol/nav'),
        HTTPMethod.GET,
        AgentToken,
        NoDataReqShape,
        {HTTPStatus.OK: ShipNavShape},
        False,
    )
    """Get the current nav status of a ship.

    ```
    Template('/my/ships/$ship_symbol/nav'),
    HTTPMethod.GET,
    AgentToken,
    NoDataReqShape,
    {HTTPStatus.OK: ShipNavShape},
    False,
    ```
    """
    UPDATE_NAV_STATUS = (
        Template('/my/ships/$ship_symbol/nav'),
        HTTPMethod.PATCH,
        AgentToken,
        ShipFlightModeShape,
        {HTTPStatus.OK: ShipNavUpdateShape},
        False,
    )
    """Update the nav configuration of a ship.

    ```
    Template('/my/ships/$ship_symbol/nav'),
    HTTPMethod.PATCH,
    AgentToken,
    ShipFlightModeShape,
    {HTTPStatus.OK: ShipNavUpdateShape},
    False,
    ```
    """
    GET_ALL_SYSTEMS = (
        Template('/systems'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: SystemsShape},
        True,
    )
    """Return a paginated list of all systems.

    ```
    Template('/systems'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: SystemsShape},
    True,
    ```
    """
    GET_SYSTEM = (
        Template('/systems/$system_symbol'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: SystemShape},
        False,
    )
    """Get the details of a system. Requires the system to have been visited or
    charted.

    ```
    Template('/systems/$system_symbol'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: SystemShape},
    False,
    ```
    """
    GET_ALL_SYSTEM_WAYPOINTS = (  # TODO: More query parameters than page and limit
        Template('/systems/$system_symbol/waypoints'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: SystemWaypointsShape},
        True,
    )
    """Return a paginated list of all of the waypoints for a given system.

    ```
    Template('/systems/$system_symbol/waypoints'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: SystemWaypointsShape},
    True,
    ```
    """
    GET_WAYPOINT = (
        Template('/systems/$system_symbol/waypoints/$waypoint_symbol'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: SystemWaypointShape},
        False,
    )
    """View the details of a waypoint.

    ```
    Template('/systems/$system_symbol/waypoints/$waypoint_symbol'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: SystemWaypointShape},
    False,
    ```
    """
    GET_CONSTRUCTION_SITE = (
        Template('/systems/$system_symbol/waypoints/$waypoint_symbol/construction'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: ConstructionShape},
        False,
    )
    """Get construction details for a waypoint.

    ```
    Template('/systems/$system_symbol/waypoints/$waypoint_symbol/construction'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: ConstructionSiteShape},
    False,
    ```
    """
    SUPPLY_CONSTRUCTION_SITE = (
        Template('/systems/$system_symbol/waypoints/$waypoint_symbol/construction/supply'),
        HTTPMethod.POST,
        AgentToken,
        ConstructionSupplyReqShape,
        {HTTPStatus.CREATED: ConstructionSupplyResShape},
        False,
    )
    """Supply a construction site with the specified good.

    ```
    Template('/systems/$system_symbol/waypoints/$waypoint_symbol/construction/supply'),
    HTTPMethod.POST,
    AgentToken,
    SupplyConstructionSiteReqShape,
    {HTTPStatus.CREATED: SupplyConstructionSiteResShape},
    False,
    ```
    """
    GET_MARKET = (
        Template('/systems/$system_symbol/waypoints/$waypoint_symbol/market'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: MarketShape},
        False,
    )
    """Retrieve imports, exports and exchange data from a marketplace.

    ```
    Template('/systems/$system_symbol/waypoints/$waypoint_symbol/market'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: MarketShape},
    False,
    ```
    """
    GET_JUMPGATE = (
        Template('/systems/$system_symbol/waypoints/$waypoint_symbol/jumpgate'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: JumpgateShape},
        False,
    )
    """Get jump gate details for a waypoint.

    ```
    Template('/systems/$system_symbol/waypoints/$waypoint_symbol/jumpgate'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: JumpgateShape},
    False,
    ```
    """
    GET_SHIPYARD = (
        Template('/systems/$system_symbol/waypoints/$waypoint_symbol/shipyard'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: ShipyardShape},
        False,
    )
    """Get the shipyard for a waypoint.

    ```
    Template('/systems/$system_symbol/waypoints/$waypoint_symbol/shipyard'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: ShipyardShape},
    False,
    ```
    """
    GET_TRADE_RELATIONSHIPS = (
        Template('/market/supply-chain'),
        HTTPMethod.GET,
        None,  # TODO: Verify
        NoDataReqShape,
        {HTTPStatus.OK: MarketSupplyChainShape},
        True,
    )
    """Describes which import and exports map to each other.

    ```
    Template('/market/supply-chain'),
    HTTPMethod.GET,
    None,  # TODO: Verify
    NoDataReqShape,
    {HTTPStatus.OK: MarketSupplyChainShape},
    True,
    ```
    """
    SUBSCRIBE_TO_EVENTS = (
        Template('/my/socket.io'),
        HTTPMethod.GET,
        None,  # TODO: Verify
        EventSubscribeReqShape,
        {HTTPStatus.OK: NoDataResShape},
        True,
    )
    """Subscribe to departure events for a system.

    The following events are available:
      - `systems.{systemSymbol}.departure`: A ship has departed from the system.

    ```
    Template('/my/socket.io'),
    HTTPMethod.GET,
    None,  # TODO: Verify
    EventSubscribeReqShape,
    {HTTPStatus.OK: NoDataResShape},
    True,
    ```
    """
    GET_SERVER_STATUS = (
        Template('/'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: ServerStatusShape},
        False,
    )
    """Return the status of the game server. This also includes a few global
    elements, such as announcements, server reset dates and leaderboards.

    ```
    Template('/'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: ServerStatusShape},
    False,
    ```
    """
    GET_ERROR_CODES = (
        Template('/error-codes'),
        HTTPMethod.GET,
        None,
        NoDataReqShape,
        {HTTPStatus.OK: ErrorCodesShape},
        True,
    )
    """Return a list of all possible error codes thrown by the game server.

    ```
    Template('/error-codes'),
    HTTPMethod.GET,
    None,
    NoDataReqShape,
    {HTTPStatus.OK: ErrorCodesShape},
    True,
    ```
    """

    def with_paging(self, page: int, limit: int) -> str:
        paging_query_fragment = f'?page={page}&limit={limit}'
        return self.path.substitute()

    def with_query_params(self, **params: str) -> str: ...

    def get_path_params(self) -> list[str]:
        return self.path.get_identifiers()
