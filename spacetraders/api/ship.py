from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from spacetraders.api.faction import Faction
from spacetraders.api.api import SpaceTradersAPIRequest, SpaceTradersAPIEndpoint, SpaceTradersAPIResponse, SpaceTradersAPIError


class ShipRole(Enum):
    REFINERY = auto()

@dataclass
class Requirements:
    power: int
    crew: int
    slots: int


@dataclass
class ShipInventory:
    symbol: str
    name: str
    description: str
    units: int


@dataclass
class ShipRegistration:
    name: str
    faction: Faction
    role: ShipRole


# TODO: Consider interaction with other areas of navigation
@dataclass
class Nav:
    system: str


@dataclass
class ShipCrew:
    current: int
    required: int
    capacity: int
    rotation: int
    morale: int
    wages: int


@dataclass
class ShipFrame:
    symbol: str
    name: str
    description: str
    module_slots: int
    mounting_points: int
    fuel_capacity: int
    requirements: Requirements
    condition: int


@dataclass
class ShipReactor:
    symbol: str
    name: str
    description: str
    power_output: str
    requirements: Requirements
    condition: str


@dataclass
class ShipEngine:
    symbol: str
    name: str
    description: str
    speed: int
    requirements: Requirements
    condition: int


@dataclass
class ShipModule:
    symbol: str
    name: str
    description: str
    requirements: Requirements
    capacity: int
    range: int


@dataclass
class ShipMounts:
    symbol: str
    name: str
    description: str
    requirements: Requirements
    strength: int
    deposit: list[str]


@dataclass
class ShipCargo:
    capacity: int
    units: int
    inventory: list[ShipInventory]


@dataclass
class ShipFuel:
    current: int
    capacity: int
    consumed_amount: int
    consumed_timestamp: datetime


@dataclass
class ShipCooldown:
    symbol: str
    total_seconds: int
    remaining_seconds: int
    expiration: datetime


class Ship:

    def __init__(self):
        self.registration: ShipRegistration
        # self.nav
        self.crew: ShipCrew
        self.frame: ShipFrame
        self.reactor: ShipReactor
        self.engine: ShipEngine
        self.modules: ShipModule
        self.mounts: ShipMounts
        self.cargo: ShipCargo
        self.fuel: ShipFuel
        self.cooldown: ShipCooldown

    @staticmethod
    def scan_waypoints(shipSymbol: str) -> list[str]:
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_WAYPOINTS) \
            .params(list([shipSymbol])) \
            .call()
        
        data = res.spacetraders['data']

        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
                if res.spacetraders['error'] is not None:
                    print(f'{shipSymbol} had an error while scanning waypoints.')
                    print(f'Code: {res.spacetraders['error']['code']}, Message: {res.spacetraders['error']['message']}')
                    return []
            case SpaceTradersAPIError():
                raise ValueError
        return data if data is not None else []
    
    @staticmethod
    def get_nav_status(shipSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_NAV) \
            .params(list([shipSymbol])) \
            .call()

        data = res.spacetraders['data']

        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                print('value')
                raise ValueError

        return data if data is not None else []
    
    @staticmethod
    def navigate(shipSymbol: str, waypointSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIP_NAVIGATE) \
            .params(list([shipSymbol])) \
            .data({"waypointSymbol": waypointSymbol}) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    
    @staticmethod
    def orbit_ship(shipSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_ORBIT) \
            .params(list([shipSymbol])) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    
    @staticmethod
    def dock_ship(shipSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_DOCK) \
            .params(list([shipSymbol])) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    
    
    @staticmethod
    def deliver_contract(contract_id: str, shipSymbol: str, tradeSymbol: str, units: int):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.DELIVER_CONTRACT) \
            .params(list([contract_id])) \
            .data({"shipSymbol": shipSymbol.upper(),
                    "tradeSymbol": tradeSymbol.upper(),
                    "units": int(units)}) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    
    @staticmethod
    def purchase_cargo(shipSymbol: str, cargoSymbol: str, units):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE) \
            .params(list([shipSymbol])) \
            .data({"symbol": cargoSymbol,
                   "units": units}) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []

    @staticmethod
    def extract(shipSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_EXTRACT) \
            .params(list([shipSymbol])) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
                # if res.spacetraders['error'] is not None:
                #     print(res.spacetraders['error'])
                #     print(f'{shipSymbol} had an error while extracting.')
                #     # print(f'Code: {res.spacetraders["error"]["code"]}, Message: {res.spacetraders["error"]["message"]}')
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []

    @staticmethod
    def get_cooldown(shipSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_COOLDOWN) \
            .params(list([shipSymbol])) \
            .call()

        # status 200 if successfully fetched cooldowns, 204 if no cooldown
        # its going to return no content body if no cooldown
        
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    
    @staticmethod
    def get_cargo(shipSymbol: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_CARGO) \
            .params(list([shipSymbol])) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    

