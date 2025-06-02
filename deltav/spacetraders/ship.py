from typing import cast

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.contract import ContractShape
from deltav.spacetraders.models.endpoint import (
    MarketTransactionShape,
    NavigateResponseShape,
    ShipJumpWaypointShape,
    WaypointScanShape,
)
from deltav.spacetraders.models.market import CargoItemShape
from deltav.spacetraders.models.ship import (
    ShipCargoShape,
    ShipCooldownShape,
    ShipCreateChartShape,
    ShipCrewShape,
    ShipEngineShape,
    ShipExtractShape,
    ShipExtractSurveyResponseShape,
    ShipExtractSurveyShape,
    ShipFrameShape,
    ShipFuelShape,
    ShipJumpShape,
    ShipModulesShape,
    ShipMountsShape,
    ShipNavShape,
    ShipPurchaseShape,
    ShipReactorShape,
    ShipRefineResponseShape,
    ShipRefineShape,
    ShipRefuelResponseShape,
    ShipRefuelShape,
    ShipRegistrationShape,
    ShipScanShipsShape,
    ShipShape,
    SuccessfulShipPurchaseShape,
)
from deltav.spacetraders.models.waypoint import WaypointNavigateShape


class Ship:
    def __init__(self):
        self.registration: ShipRegistrationShape
        self.nav: ShipNavShape
        self.crew: ShipCrewShape
        self.frame: ShipFrameShape
        self.reactor: ShipReactorShape
        self.engine: ShipEngineShape
        self.modules: ShipModulesShape
        self.mounts: ShipMountsShape
        self.cargo: ShipCargoShape
        self.fuel: ShipFuelShape
        self.cooldown: ShipCooldownShape

    @staticmethod
    def get_ships() -> list[ShipShape] | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(list[ShipShape], res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_ship(ship_symbol: str) -> ShipShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def scan_systems(ship_symbol: str) -> WaypointScanShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_SYSTEMS)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(WaypointScanShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def scan_waypoints(ship_symbol: str) -> WaypointScanShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_WAYPOINTS)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(WaypointScanShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def scan_ships(ship_symbol: str) -> ShipScanShipsShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_SHIPS)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipScanShipsShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_nav_status(ship_symbol: str):
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NAV)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipNavShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def navigate(ship_symbol: str, waypoint: WaypointNavigateShape) -> NavigateResponseShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP_NAVIGATE)
            .path_params(ship_symbol)
            .data(waypoint)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(NavigateResponseShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def orbit_ship(ship_symbol: str) -> ShipNavShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_ORBIT)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipNavShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def dock_ship(ship_symbol: str) -> ShipNavShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_DOCK)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipNavShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def purchase_cargo(ship_symbol: str, purchase: CargoItemShape) -> MarketTransactionShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE_CARGO)
            .path_params(ship_symbol)
            .data(purchase)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(MarketTransactionShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def sell_cargo(ship_symbol: str, cargo: CargoItemShape) -> MarketTransactionShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SELL)
            .path_params(ship_symbol)
            .data(cargo)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(MarketTransactionShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def jettison_cargo(ship_symbol: str, cargo: CargoItemShape) -> ShipCargoShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_JETTISON)
            .path_params(ship_symbol)
            .data(cargo)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipCargoShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def extract(ship_symbol: str) -> ShipExtractShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipExtractShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def extract_survey(
        ship_symbol: str, survey: ShipExtractSurveyShape
    ) -> ShipExtractSurveyResponseShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT_SURVEY)
            .path_params(ship_symbol)
            .with_token()
            .data(survey)
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipExtractSurveyResponseShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_cooldown(ship_symbol: str) -> ShipCooldownShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_COOLDOWN)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipCooldownShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_cargo(ship_symbol: str) -> ShipCargoShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CARGO)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipCargoShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def purchase_ship(shape: ShipPurchaseShape) -> SuccessfulShipPurchaseShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE_SHIP)
            .data(shape)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(SuccessfulShipPurchaseShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def refuel_ship(ship_symbol: str, refuel: ShipRefuelShape) -> ShipRefuelResponseShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_REFUEL)
            .path_params(ship_symbol)
            .data(refuel)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipRefuelResponseShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def create_chart(ship_symbol: str) -> ShipCreateChartShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CREATE_CHART)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipCreateChartShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def negotiate_contract(ship_symbol: str) -> ContractShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NEGOTIATE_CONTRACT)
            .path_params(ship_symbol)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ContractShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def jump_ship(ship_symbol: str, waypoint: ShipJumpWaypointShape) -> ShipJumpShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_JUMP)
            .path_params(ship_symbol)
            .data(waypoint)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipJumpShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def refine(ship_symbol: str, produce: ShipRefineShape) -> ShipRefineResponseShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_REFINE)
            .path_params(ship_symbol)
            .data(produce)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ShipRefineResponseShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

