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
        req = SpaceTradersAPIRequest().builder().endpoint(SpaceTradersAPIEndpoint.MY_SHIPS).with_agent_token().build()

        match res := SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse():
                data: list[ShipShape] = cast(list[ShipShape], res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_ship(shipSymbol: str) -> ShipShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipShape = cast(ShipShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def scan_systems(shipSymbol: str) -> WaypointScanShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_SYSTEMS)
            .path_params(shipSymbol)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: WaypointScanShape = cast(WaypointScanShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def scan_waypoints(shipSymbol: str) -> WaypointScanShape | SpaceTradersAPIError:
        res = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_WAYPOINTS)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(res):
            case SpaceTradersAPIResponse():
                data: WaypointScanShape = cast(WaypointScanShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def scan_ships(shipSymbol: str) -> ShipScanShipsShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_SHIPS)
            .path_params(shipSymbol)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipScanShipsShape = cast(ShipScanShipsShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_nav_status(shipSymbol: str):
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NAV)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipNavShape = cast(ShipNavShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def navigate(shipSymbol: str, waypoint: WaypointNavigateShape) -> NavigateResponseShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP_NAVIGATE)
            .path_params(shipSymbol)
            .data(waypoint)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: NavigateResponseShape = cast(NavigateResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def orbit_ship(shipSymbol: str) -> ShipNavShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_ORBIT)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipNavShape = cast(ShipNavShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def dock_ship(shipSymbol: str) -> ShipNavShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_DOCK)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipNavShape = cast(ShipNavShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def purchase_cargo(shipSymbol: str, purchase: CargoItemShape) -> MarketTransactionShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE_CARGO)
            .path_params(shipSymbol)
            .data(purchase)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: MarketTransactionShape = cast(MarketTransactionShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def sell_cargo(shipSymbol: str, cargo: CargoItemShape) -> MarketTransactionShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SELL)
            .path_params(shipSymbol)
            .data(cargo)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: MarketTransactionShape = cast(MarketTransactionShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def jettison_cargo(shipSymbol: str, cargo: CargoItemShape) -> ShipCargoShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_JETTISON)
            .path_params(shipSymbol)
            .data(cargo)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipCargoShape = cast(ShipCargoShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def extract(shipSymbol: str) -> ShipExtractShape | SpaceTradersAPIError:
        res = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(res):
            case SpaceTradersAPIResponse():
                data: ShipExtractShape = cast(ShipExtractShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def extract_survey(
        shipSymbol: str, survey: ShipExtractSurveyShape
    ) -> ShipExtractSurveyResponseShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT_SURVEY)
            .path_params(shipSymbol)
            .with_agent_token()
            .data(survey)
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipExtractSurveyResponseShape = cast(ShipExtractSurveyResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_cooldown(shipSymbol: str) -> ShipCooldownShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_COOLDOWN)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipCooldownShape = cast(ShipCooldownShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_cargo(shipSymbol: str) -> ShipCargoShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CARGO)
            .path_params(shipSymbol)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipCargoShape = cast(ShipCargoShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def purchase_ship(shape: ShipPurchaseShape) -> SuccessfulShipPurchaseShape | SpaceTradersAPIError:
        request = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE_SHIP)
            .data(shape)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(request):
            case SpaceTradersAPIResponse():
                data: SuccessfulShipPurchaseShape = cast(SuccessfulShipPurchaseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def refuel_ship(shipSymbol: str, refuel: ShipRefuelShape) -> ShipRefuelResponseShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_REFUEL)
            .path_params(shipSymbol)
            .data(refuel)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipRefuelResponseShape = cast(ShipRefuelResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def create_chart(shipSymbol: str) -> ShipCreateChartShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CREATE_CHART)
            .path_params(shipSymbol)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipCreateChartShape = cast(ShipCreateChartShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def negotiate_contract(shipSymbol: str) -> ContractShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NEGOTIATE_CONTRACT)
            .path_params(shipSymbol)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ContractShape = cast(ContractShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def jump_ship(shipSymbol: str, waypoint: ShipJumpWaypointShape) -> ShipJumpShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_JUMP)
            .path_params(shipSymbol)
            .data(waypoint)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipJumpShape = cast(ShipJumpShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def refine(shipSymbol: str, produce: ShipRefineShape) -> ShipRefineResponseShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_REFINE)
            .path_params(shipSymbol)
            .data(produce)
            .with_agent_token()
            .build()
        )

        match res := SpaceTradersAPIClient().call(req):
            case SpaceTradersAPIResponse():
                data: ShipRefineResponseShape = cast(ShipRefineResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

