from typing import cast

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.systems import JumpgateShape, MarketShape, ShipyardShape

class System:

    @staticmethod
    def extract_system_symbol(waypointSymbol: str) -> str:
        parts = waypointSymbol.split('-')
        if len(parts) >= 2:
            # Join the first two parts with a hyphen
            return f"{parts[0]}-{parts[1]}"
        return waypointSymbol
    
    @staticmethod
    def get_shipyard(waypointSymbol: str) -> ShipyardShape | SpaceTradersAPIError:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIPYARD) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: ShipyardShape = cast(ShipyardShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err
            
    @staticmethod
    def get_market(waypointSymbol: str) -> MarketShape | SpaceTradersAPIError:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_MARKET) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: MarketShape = cast(MarketShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err
            
    @staticmethod
    def get_jumpgate(waypointSymbol: str) -> JumpgateShape | SpaceTradersAPIError:
        systemSymbol: str = System.extract_system_symbol(waypointSymbol)
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_JUMPGATE) \
            .path_params(systemSymbol, waypointSymbol) \
            .with_agent_token() \
            .build()
        
        match (res := SpaceTradersAPIClient().call(req)):
            case SpaceTradersAPIResponse():
                data: JumpgateShape = cast(JumpgateShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err
