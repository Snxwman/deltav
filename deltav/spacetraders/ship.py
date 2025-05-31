from datetime import datetime
from typing import cast

from httpx import request

from deltav.spacetraders.api.request import SpaceTradersAPIRequest, SpaceTradersAPIEndpoint
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.models.contract import ContractDeliverShape
from deltav.spacetraders.models.endpoint import ContractSuccessfulDeliveryShape, NavigateResponseShape, MarketTransactionShape, WaypointScanShape
from deltav.spacetraders.models.market import CargoItemShape
from deltav.spacetraders.models.ship import ShipPurchaseShape, ShipRefuelResponseShape, ShipRefuelShape, ShipShape, ShipRegistrationShape, ShipNavShape, ShipCrewShape, ShipFrameShape, ShipReactorShape, ShipEngineShape, ShipModulesShape, ShipMountsShape, ShipCargoShape, ShipFuelShape, ShipCooldownShape, ShipCargoInventoryShape, ShipExtractShape, SuccessfulShipPurchaseShape
from deltav.spacetraders.models.waypoint import  WaypointNavigateShape, WaypointShape, WaypointChartShape



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
        ...


    @staticmethod
    def get_ships() -> list[ShipShape] | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS) \
            .with_agent_token() \
            .build()
    
        match (res := SpaceTradersAPIClient.call(req)):
            case SpaceTradersAPIResponse():
                data: list[ShipShape] = cast(list[ShipShape], res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err
            
    @staticmethod
    def get_ship(shipSymbol: str) -> ShipShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipShape = cast(ShipShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;

    @staticmethod
    def scan_waypoints(shipSymbol: str) -> WaypointScanShape | SpaceTradersAPIError:
        res = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_WAYPOINTS) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(res)):
            case SpaceTradersAPIResponse():
                data: WaypointScanShape = cast(WaypointScanShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;


    @staticmethod
    def get_nav_status(shipSymbol: str):
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NAV) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipNavShape = cast(ShipNavShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
    

    @staticmethod
    def navigate(shipSymbol: str, waypoint: WaypointNavigateShape) -> NavigateResponseShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP_NAVIGATE) \
            .path_params(shipSymbol) \
            .data(waypoint) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: NavigateResponseShape = cast(NavigateResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
    

    @staticmethod
    def orbit_ship(shipSymbol: str) -> ShipNavShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_ORBIT) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipNavShape = cast(ShipNavShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
    

    @staticmethod
    def dock_ship(shipSymbol: str) -> ShipNavShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_DOCK) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipNavShape = cast(ShipNavShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
    
    
    @staticmethod
    def deliver_contract(contract_id: str, deliver: ContractDeliverShape) -> ContractSuccessfulDeliveryShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.DELIVER_CONTRACT) \
            .path_params(contract_id) \
            .data(deliver) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ContractSuccessfulDeliveryShape = cast(ContractSuccessfulDeliveryShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
    

    @staticmethod
    def purchase_cargo(shipSymbol: str, purchase: CargoItemShape) -> MarketTransactionShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE_CARGO) \
            .path_params(shipSymbol) \
            .data(purchase) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: MarketTransactionShape = cast(MarketTransactionShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;

    @staticmethod
    def sell_cargo(shipSymbol: str, cargo: CargoItemShape) -> MarketTransactionShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SELL) \
            .path_params(shipSymbol) \
            .data(cargo) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: MarketTransactionShape = cast(MarketTransactionShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
        

    @staticmethod
    def jettison_cargo(shipSymbol: str, cargo: CargoItemShape) -> ShipCargoShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_JETTISON) \
            .path_params(shipSymbol) \
            .data(cargo) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipCargoShape = cast(ShipCargoShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;

    @staticmethod
    def extract(shipSymbol: str) -> ShipExtractShape | SpaceTradersAPIError:
        res = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(res)):
            case SpaceTradersAPIResponse():
                data: ShipExtractShape = cast(ShipExtractShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;


    @staticmethod
    def get_cooldown(shipSymbol: str) -> ShipCooldownShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_COOLDOWN) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipCooldownShape = cast(ShipCooldownShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;

    
    @staticmethod
    def get_cargo(shipSymbol: str) -> ShipCargoShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CARGO) \
            .path_params(shipSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipCargoShape = cast(ShipCargoShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;

    @staticmethod
    def purchase_ship(shape: ShipPurchaseShape) -> SuccessfulShipPurchaseShape | SpaceTradersAPIError:
        request = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE_SHIP) \
            .data(shape) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(request)):
            case SpaceTradersAPIResponse():
                data: SuccessfulShipPurchaseShape = cast(SuccessfulShipPurchaseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;
        

    @staticmethod
    def refuel_ship(shipSymbol: str, refuel: ShipRefuelShape) -> ShipRefuelResponseShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_REFUEL) \
            .path_params(shipSymbol) \
            .data(refuel) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipRefuelResponseShape = cast(ShipRefuelResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err;