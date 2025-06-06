from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.construction import ConstructionSupplyReqShape
from deltav.spacetraders.models.market import MarketShape
from deltav.spacetraders.models.systems import JumpgateShape, ShipyardShape


# TODO: Convert methods to right types
class System:
    @staticmethod
    def extract_system_symbol(waypoint_symbol: str) -> str:
        parts = waypoint_symbol.split('-')
        if len(parts) >= 2:
            return f'{parts[0]}-{parts[1]}'
        return waypoint_symbol

    @staticmethod
    def get_shipyard(waypoint_symbol: str) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest[ShipyardShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIPYARD)
            .path_params(system_symbol, waypoint_symbol)
            .token()
            .build()
        )

    @staticmethod
    def get_market(waypoint_symbol: str) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest[MarketShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_MARKET)
            .path_params(system_symbol, waypoint_symbol)
            .token()
            .build()
        )

    @staticmethod
    def get_jumpgate(waypoint_symbol: str) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest[JumpgateShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_JUMPGATE)
            .path_params(system_symbol, waypoint_symbol)
            .token()
            .build()
        )

    @staticmethod
    def get_systems() -> SpaceTradersAPIRequest:
        return (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_SYSTEMS)
            .token()
            .build()
        )

    @staticmethod
    def get_system(waypoint_symbol: str) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_SYSTEMS)
            .path_params(system_symbol)
            .token()
            .build()
        )

    @staticmethod
    def get_waypoints(system_symbol: str) -> SpaceTradersAPIRequest:
        return (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_SYSTEM_WAYPOINTS)
            .path_params(system_symbol)
            .token()
            .build()
        )

    @staticmethod
    def get_waypoint(waypoint_symbol: str) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_WAYPOINT)
            .path_params(system_symbol, waypoint_symbol)
            .token()
            .build()
        )

    @staticmethod
    def get_construction_site(waypoint_symbol: str) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_CONSTRUCTION_SITE)
            .path_params(system_symbol, waypoint_symbol)
            .token()
            .build()
        )

    @staticmethod
    def supply_construction_site(waypoint_symbol: str, supply: ConstructionSupplyReqShape) -> SpaceTradersAPIRequest:
        system_symbol: str = System.extract_system_symbol(waypoint_symbol)
        return (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.SUPPLY_CONSTRUCTION_SITE)
            .path_params(system_symbol, waypoint_symbol)
            .token()
            .data(supply)
            .build()
        )

