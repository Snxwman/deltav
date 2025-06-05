from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.endpoint import ChartCreateShape
from deltav.spacetraders.models.market import TransactionShape
from deltav.spacetraders.models.ship import (
    CargoItemReqShape,
    ScanShipsShape,
    ScanWaypointShape,
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
    ShipPurchaseReqShape,
    ShipPurchaseResShape,
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


class Ship:
    def __init__(self):
        self.registration: ShipRegistrationShape
        self.nav: ShipNavShape
        self.crew: ShipCrewShape
        self.frame: ShipFrameShape
        self.reactor: ShipReactorShape
        self.engine: ShipEngineShape
        self.modules: ShipModuleShape
        self.mounts: ShipMountShape
        self.cargo: ShipCargoShape
        self.fuel: ShipFuelShape
        self.cooldown: ShipCooldownShape

    @staticmethod
    def fetch_ships() -> list[ShipShape] | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS)
            .token()
            .build(),
            list[ShipShape],
        ).unwrap()

    @staticmethod
    def fetch_ship(ship_symbol: str) -> ShipShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipShape,
        ).unwrap()

    @staticmethod
    def scan_systems(ship_symbol: str) -> ScanWaypointShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SCAN_SYSTEMS)
            .path_params(ship_symbol)
            .token()
            .build(),
            ScanWaypointShape,
        ).unwrap()

    @staticmethod
    def scan_waypoints(ship_symbol: str) -> ScanWaypointShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SCAN_WAYPOINTS)
            .path_params(ship_symbol)
            .token()
            .build(),
            ScanWaypointShape,
        ).unwrap()

    @staticmethod
    def scan_ships(ship_symbol: str) -> ScanShipsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SCAN_SHIPS)
            .path_params(ship_symbol)
            .token()
            .build(),
            ScanShipsShape,
        ).unwrap()

    @staticmethod
    def fetch_nav_status(ship_symbol: str) -> ShipNavShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_NAV_STATUS)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipNavShape,
        ).unwrap()

    @staticmethod
    def navigate(
        ship_symbol: str, waypoint: WaypointSymbolReqShape
    ) -> ShipNavigationShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.NAVIGATE_SHIP)
            .path_params(ship_symbol)
            .data(waypoint)
            .token()
            .build(),
            ShipNavigationShape,
        ).unwrap()

    @staticmethod
    def orbit_ship(ship_symbol: str) -> ShipNavShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.ORBIT_SHIP)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipNavShape,
        ).unwrap()

    @staticmethod
    def dock_ship(ship_symbol: str) -> ShipNavShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.DOCK_SHIP)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipNavShape,
        ).unwrap()

    @staticmethod
    def purchase_cargo(
        ship_symbol: str, purchase: CargoItemReqShape
    ) -> TransactionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.PURCHASE_CARGO)
            .path_params(ship_symbol)
            .data(purchase)
            .token()
            .build(),
            TransactionShape,
        ).unwrap()

    @staticmethod
    def sell_cargo(
        ship_symbol: str, cargo: CargoItemReqShape
    ) -> TransactionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SELL_CARGO)
            .path_params(ship_symbol)
            .data(cargo)
            .token()
            .build(),
            TransactionShape,
        ).unwrap()

    @staticmethod
    def jettison_cargo(
        ship_symbol: str, cargo: CargoItemReqShape
    ) -> ShipCargoShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.JETTISON_CARGO)
            .path_params(ship_symbol)
            .data(cargo)
            .token()
            .build(),
            ShipCargoShape,
        ).unwrap()

    @staticmethod
    def extract(ship_symbol: str) -> ShipExtractionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.EXTRACT_RESOURCES)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipExtractionShape,
        ).unwrap()

    @staticmethod
    def extract_survey(
        ship_symbol: str, survey: SurveyReqShape
    ) -> ShipExtractionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.EXTRACT_RESOURCES_WITH_SURVEY)
            .path_params(ship_symbol)
            .token()
            .data(survey)
            .build(),
            ShipExtractionShape,
        ).unwrap()

    @staticmethod
    def fetch_cooldown(ship_symbol: str) -> ShipCooldownShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIP_COOLDOWN)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipCooldownShape,
        ).unwrap()

    @staticmethod
    def fetch_cargo(ship_symbol: str) -> ShipCargoShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIP_CARGO)
            .path_params(ship_symbol)
            .token()
            .build(),
            ShipCargoShape,
        ).unwrap()

    @staticmethod
    def purchase_ship(shape: ShipPurchaseReqShape) -> ShipPurchaseResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.PURCHASE_SHIP)
            .data(shape)
            .token()
            .build(),
            ShipPurchaseResShape,
        ).unwrap()

    @staticmethod
    def refuel_ship(
        ship_symbol: str, refuel: ShipRefuelReqShape
    ) -> ShipRefuelResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.REFUEL_SHIP)
            .path_params(ship_symbol)
            .data(refuel)
            .token()
            .build(),
            ShipRefuelResShape,
        ).unwrap()

    @staticmethod
    def create_chart(ship_symbol: str) -> ChartCreateShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.CREATE_CHART)
            .path_params(ship_symbol)
            .token()
            .build(),
            ChartCreateShape,
        ).unwrap()

    @staticmethod
    def negotiate_contract(ship_symbol: str) -> ContractShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.NEGOTIATE_CONTRACT)
            .path_params(ship_symbol)
            .token()
            .build(),
            ContractShape,
        ).unwrap()

    @staticmethod
    def jump_ship(
        ship_symbol: str, waypoint: WaypointSymbolReqShape
    ) -> ShipJumpResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.JUMP_SHIP)
            .path_params(ship_symbol)
            .data(waypoint)
            .token()
            .build(),
            ShipJumpResShape,
        ).unwrap()

    @staticmethod
    def refine(
        ship_symbol: str, produce: ShipRefineReqShape
    ) -> ShipRefineResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.REFINE_MATERIALS)
            .path_params(ship_symbol)
            .data(produce)
            .token()
            .build(),
            ShipRefineResShape,
        ).unwrap()
