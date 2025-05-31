from typing import cast

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.ship import ShipShape


class Ship:

    def __init__(self):
        # self.registration: ShipRegistration
        # # self.nav
        # self.crew: ShipCrew
        # self.frame: ShipFrame
        # self.reactor: ShipReactor
        # self.engine: ShipEngine
        # self.modules: ShipModule
        # self.mounts: ShipMounts
        # self.cargo: ShipCargo
        # self.fuel: ShipFuel
        # self.cooldown: ShipCooldown
        ...


    def my_ships(self) -> ShipShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS) \
            .with_agent_token() \
            .build()
    
        match (res := SpaceTradersAPIClient.call(req)):
            case SpaceTradersAPIResponse():
                data: ShipShape = cast(ShipShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err
        

    # @staticmethod
    # def scan_waypoints(shipSymbol: str) -> list[str]:
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_WAYPOINTS) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #     
    #     data = res.spacetraders['data']
    #
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #             if res.spacetraders['error'] is not None:
    #                 print(f'{shipSymbol} had an error while scanning waypoints.')
    #                 print(f'Code: {res.spacetraders['error']['code']}, Message: {res.spacetraders['error']['message']}')
    #                 return []
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #     return data if data is not None else []
    

    # @staticmethod
    # def get_nav_status(shipSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NAV) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             print('value')
    #             raise ValueError
    #
    #     return data if data is not None else []
    

    # @staticmethod
    # def navigate(shipSymbol: str, waypointSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIP_NAVIGATE) \
    #         .params(list([shipSymbol])) \
    #         .data({"waypointSymbol": waypointSymbol}) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []
    

    # @staticmethod
    # def orbit_ship(shipSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_ORBIT) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []
    

    # @staticmethod
    # def dock_ship(shipSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_DOCK) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []
    
    
    # @staticmethod
    # def deliver_contract(contract_id: str, shipSymbol: str, tradeSymbol: str, units: int):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.DELIVER_CONTRACT) \
    #         .params(list([contract_id])) \
    #         .data({"shipSymbol": shipSymbol.upper(),
    #                 "tradeSymbol": tradeSymbol.upper(),
    #                 "units": int(units)}) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []
    

    # @staticmethod
    # def purchase_cargo(shipSymbol: str, cargoSymbol: str, units):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE) \
    #         .params(list([shipSymbol])) \
    #         .data({"symbol": cargoSymbol,
    #                "units": units}) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []


    # @staticmethod
    # def extract(shipSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #             # if res.spacetraders['error'] is not None:
    #             #     print(res.spacetraders['error'])
    #             #     print(f'{shipSymbol} had an error while extracting.')
    #             #     # print(f'Code: {res.spacetraders["error"]["code"]}, Message: {res.spacetraders["error"]["message"]}')
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []


    # @staticmethod
    # def get_cooldown(shipSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_COOLDOWN) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #
    #     # status 200 if successfully fetched cooldowns, 204 if no cooldown
    #     # its going to return no content body if no cooldown
    #     
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []

    
    # @staticmethod
    # def get_cargo(shipSymbol: str):
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CARGO) \
    #         .params(list([shipSymbol])) \
    #         .call()
    #
    #     data = res.spacetraders['data']
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             data = res.spacetraders['data']
    #         case SpaceTradersAPIErrorCodes():
    #             raise ValueError
    #
    #     return data if data is not None else []

