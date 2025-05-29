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

    def scan_waypoints(shipSymbol: str) -> list[str]:
        print("pass before res")
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_SCAN_WAYPOINTS) \
            .params(list([shipSymbol])) \
            .call()
        print("pass after res")
        print(data)
        
        data = res.spacetraders['data']
        print("fail after data")

        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                print('value')
                raise ValueError
        print("fail after match")
        return data if data is not None else []
    
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
    
    def purchase_cargo(shipSymbol: str, cargoSymbol: str, units):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS_PURCHASE) \
            .params(list([shipSymbol])) \
            .data({"symbol": cargoSymbol, "units": units}) \
            .call()

        data = res.spacetraders['data']
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError

        return data if data is not None else []
    

