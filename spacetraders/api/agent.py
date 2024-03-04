from typing import Optional, TypedDict

from spacetraders.api.account import Account
from spacetraders.api.api import SpaceTradersAPI, SpaceTradersAPIRequest, SpaceTradersAPIResponse
from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint
from spacetraders.api.faction import Faction
from spacetraders.api.ship import Ship

class RegisterAgentData(TypedDict):
    symbol: str
    faction: str
    email: Optional[str]

class Agent:

    def __init__(self, account: Account, token: str) -> None:
        self.account: Account = account 
        self.token: str = token 

        agent_details = self.my_details()
        self.callsign: str = agent_details['symbol']
        self.credits: int = agent_details['credits']
        self.faction: Faction = agent_details['faction']
        self.headquarters: str = agent_details['headquarters']
        self.ship_count: int = agent_details['ship_count']
        self.ships: list[Ship] = self.my_ships()

    
    def my_details(self) -> dict:
        return {}


    def my_ships(self) -> list[Ship]:
        return []
    

    @staticmethod
    def register(agent_data: RegisterAgentData) -> str:
        endpoint = SpaceTradersAPIEndpoint.REGISTER
        
        req = SpaceTradersAPIRequest(endpoint, data=agent_data)
        res = SpaceTradersAPI.call(req)

        match res:
            case SpaceTradersAPIResponse():
                return res.spacetraders['data']['token'] 
            case SpaceTradersAPIError():
                raise ValueError
            case _:
                raise TypeError


    @staticmethod
    def details(callsign: str) -> dict:
        endpoint = f'https://api.spacetraders.io/v2/agents/{callsign}'
        return {}
