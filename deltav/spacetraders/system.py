from typing import cast

from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.systems import JumpgateShape, MarketShape, ShipyardShape, SupplyConstructionSiteResponseShape, SupplyConstructionSiteShape, SystemShape, SystemWaypointShape

class System:

    @staticmethod
    def extract_system_symbol(waypointSymbol: str) -> str:
        parts = waypointSymbol.split('-')
        if len(parts) >= 2:
            return f"{parts[0]}-{parts[1]}"
        return waypointSymbol
    

    @staticmethod
    def get_shipyard(waypointSymbol: str) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIPYARD) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()


    @staticmethod
    def get_market(waypointSymbol: str) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_MARKET) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        
        
    @staticmethod
    def get_jumpgate(waypointSymbol: str) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_JUMPGATE) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        

    @staticmethod
    def get_systems() -> SpaceTradersAPIRequest:
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.SYSTEM_GET_SYSTEMS) \
            .with_agent_token() \
            .build()
        
        
    @staticmethod
    def get_system(waypointSymbol: str) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.SYSTEM_GET_SYSTEMS) \
            .path_params(systemSymbol) \
            .with_agent_token() \
            .build()
        

    @staticmethod
    def get_waypoints(systemSymbol: str) -> SpaceTradersAPIRequest:
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.SYSTEM_GET_WAYPOINTS) \
            .path_params(systemSymbol) \
            .with_agent_token() \
            .build()
        

    @staticmethod
    def get_waypoint(waypointSymbol: str) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.SYSTEM_GET_WAYPOINT) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        
     
    @staticmethod
    def get_construction_site(waypointSymbol: str) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.SYSTEM_GET_CONSTRUCTION_SITE) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        
 
    @staticmethod
    def supply_construction_site(waypointSymbol: str, supply: SupplyConstructionSiteShape) -> SpaceTradersAPIRequest:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.SYSTEM_SUPPLY_CONSTRUCTION_SITE) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .data(supply) \
            .build()   