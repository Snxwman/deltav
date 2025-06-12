from __future__ import annotations

from datetime import UTC, datetime

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.ship import ShipCrewRotationShape, ShipRole
from deltav.spacetraders.models import NoDataResShape
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.endpoint import ChartCreateShape
from deltav.spacetraders.models.market import TransactionShape
from deltav.spacetraders.models.ship import (
    CargoItemReqShape,
    ScanShipsShape,
    ScanSystemsShape,
    ScanWaypointsShape,
    ShipCargoInventoryShape,
    ShipCargoShape,
    ShipCooldownShape,
    ShipCrewShape,
    ShipEngineShape,
    ShipExtractionShape,
    ShipFrameShape,
    ShipFuelShape,
    ShipJumpResShape,
    ShipModuleShape,
    ShipMountShape,
    ShipNavigationShape,
    ShipNavShape,
    ShipReactorShape,
    ShipRefineReqShape,
    ShipRefineResShape,
    ShipRefuelReqShape,
    ShipRefuelResShape,
    ShipRegistrationShape,
    ShipShape,
    SurveyReqShape,
)
from deltav.spacetraders.models.waypoint import WaypointSymbolReqShape
from deltav.spacetraders.token import AgentToken


class Ship:
    def __init__(self, data: ShipShape):
        self.__synced_api: bool = False
        self.__synced_db: bool = False

        self.__data: ShipShape = data
        self.__data_timestamp = datetime.now(tz=UTC)

        self.__agent_token: AgentToken

        self._cargo: ShipCargoShape = data.cargo
        self._cooldown: ShipCooldownShape = data.cooldown
        self._crew: ShipCrewShape = data.crew
        self._engine: ShipEngineShape = data.engine
        self._frame: ShipFrameShape = data.frame
        self._fuel: ShipFuelShape = data.fuel
        self._modules: list[ShipModuleShape] = data.modules
        self._mounts: list[ShipMountShape] = data.mounts
        self._nav: ShipNavShape = data.nav
        self._reactor: ShipReactorShape = data.reactor
        self._registration: ShipRegistrationShape = data.registration
        self._symbol: str = data.symbol

    @property
    def cargo(self) -> list[ShipCargoInventoryShape]:
        return self._cargo.inventory

    @property
    def cargo_capacity(self) -> int:
        return self._cargo.capacity

    @property
    def cargo_units(self) -> int:
        return self._cargo.units

    @property
    def cargo_units_remaining(self) -> int:
        return self.cargo_capacity - self.cargo_units

    @property
    def has_cargo(self) -> bool:
        return bool(self._cargo.inventory)

    @property
    def cooldown(self) -> ShipCooldownShape:
        return self._cooldown

    @property
    def on_cooldown(self) -> bool:
        return False if self._cooldown.remaining_seconds == 0 else True

    @property
    def crew(self) -> int:
        return self._crew.current

    @property
    def crew_details(self) -> ShipCrewShape:
        return self._crew

    @property
    def crew_required(self) -> int:
        return self._crew.required

    @property
    def crew_rotation(self) -> ShipCrewRotationShape:
        return self._crew.rotation

    @property
    def engine(self) -> ShipEngineShape:
        return self._engine

    @property
    def faction(self) -> FactionSymbol:
        return self._registration.faction_symbol

    @property
    def frame(self) -> ShipFrameShape:
        return self._frame

    @property
    def fuel(self) -> ShipFuelShape:
        return self._fuel

    @property
    def modules(self) -> list[ShipModuleShape]:
        return self._modules

    @property
    def mounts(self) -> list[ShipMountShape]:
        return self._mounts

    @property
    def nav(self) -> ShipNavShape:
        return self._nav

    @property
    def reactor(self) -> ShipReactorShape:
        return self._reactor

    @property
    def registration(self) -> ShipRegistrationShape:
        return self._registration

    @property
    def role(self) -> ShipRole:
        return self._registration.role

    @property
    def symbol(self) -> str:
        return self._symbol

    def fetch_ship(self) -> ShipShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIP)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _scan_ships(self) -> ScanShipsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ScanShipsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SCAN_SHIPS)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _scan_systems(self) -> ScanSystemsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ScanSystemsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SCAN_SYSTEMS)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _scan_waypoints(self) -> ScanWaypointsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ScanWaypointsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SCAN_WAYPOINTS)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _fetch_nav_status(self) -> ShipNavShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipNavShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_NAV_STATUS)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _navigate(self, waypoint: WaypointSymbolReqShape) -> ShipNavigationShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipNavigationShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.NAVIGATE_SHIP)
            .path_params(self.symbol)
            .data(waypoint)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _orbit_ship(self) -> ShipNavShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipNavShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.ORBIT_SHIP)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _dock_ship(self) -> ShipNavShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipNavShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.DOCK_SHIP)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _purchase_cargo(self, purchase: CargoItemReqShape) -> TransactionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[TransactionShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.PURCHASE_CARGO)
            .path_params(self.symbol)
            .data(purchase)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _sell_cargo(self, cargo: CargoItemReqShape) -> TransactionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[TransactionShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SELL_CARGO)
            .path_params(self.symbol)
            .data(cargo)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _jettison_cargo(self, cargo: CargoItemReqShape) -> ShipCargoShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipCargoShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.JETTISON_CARGO)
            .path_params(self.symbol)
            .data(cargo)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _extract(self) -> ShipExtractionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipExtractionShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.EXTRACT_RESOURCES)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _extract_survey(self, survey: SurveyReqShape) -> ShipExtractionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipExtractionShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.EXTRACT_RESOURCES_WITH_SURVEY)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .data(survey)
            .build()
        ).unwrap()

    def _fetch_cooldown(self) -> ShipCooldownShape | NoDataResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipCooldownShape | NoDataResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIP_COOLDOWN)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _fetch_cargo(self) -> ShipCargoShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipCargoShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIP_CARGO)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _refuel_ship(self, refuel: ShipRefuelReqShape) -> ShipRefuelResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipRefuelResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.REFUEL_SHIP)
            .path_params(self.symbol)
            .data(refuel)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _create_chart(self) -> ChartCreateShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ChartCreateShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.CREATE_CHART)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _negotiate_contract(self) -> ContractShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.NEGOTIATE_CONTRACT)
            .path_params(self.symbol)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _jump_ship(self, waypoint: WaypointSymbolReqShape) -> ShipJumpResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipJumpResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.JUMP_SHIP)
            .path_params(self.symbol)
            .data(waypoint)
            .token(self.__agent_token)
            .build()
        ).unwrap()

    def _refine(self, produce: ShipRefineReqShape) -> ShipRefineResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipRefineResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.REFINE_MATERIALS)
            .path_params(self.symbol)
            .data(produce)
            .token(self.__agent_token)
            .build()
        ).unwrap()
