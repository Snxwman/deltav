from dataclasses import dataclass
from typing import Optional, Self, TypedDict

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

@dataclass
class AgentInfo():
    account_id: str
    symbol: str
    headquarters: str
    credits: int
    starting_faction: Faction
    ship_count: int

class Agent:

    def __init__(self, token:str, agent_info:AgentInfo|None=None) -> None:
        self.token: str = token

        if agent_info is None:
            agent_info = self.my_agent()

        self.account: Account = Account(agent_info.account_id)
        self.callsign: str = agent_info.symbol 
        self.credits: int = agent_info.credits 
        self.faction: Faction = agent_info.starting_faction 
        self.headquarters: str = agent_info.headquarters 
        self.ship_count: int = agent_info.ship_count 
        self.ships: list[Ship] = self.my_ships()

        print()
        print(self.__dict__)

    
    def my_agent(self) -> AgentInfo:
        endpoint = SpaceTradersAPIEndpoint.MY_AGENT

        req = SpaceTradersAPIRequest(endpoint, agent=self)
        res = SpaceTradersAPI.call(req)
        
        agent = res.spacetraders['data']['agent']
        return AgentInfo(
            account_id=agent['accountId'],
            symbol=agent['symbol'],
            headquarters=agent['headquarters'],
            credits=int(agent['credits']),
            starting_faction=agent['startingFaction'],
            ship_count=int(agent['shipCount']),
        ) 


    def my_ships(self) -> list[Ship]:
        return []
    

    @classmethod
    def register(cls, agent_data: RegisterAgentData) -> Self:
        endpoint = SpaceTradersAPIEndpoint.REGISTER
        
        req = SpaceTradersAPIRequest(endpoint, data=agent_data)
        res = SpaceTradersAPI.call(req)

        match res:
            case SpaceTradersAPIResponse():
                print()
                print(res.__dict__)
                data = res.spacetraders['data'] 
            case SpaceTradersAPIError():
                raise ValueError
            case _:
                raise TypeError

        agent = data['agent']
        return cls(
            data['token'], 
            AgentInfo(
                account_id=agent['accountId'],
                symbol=agent['symbol'],
                headquarters=agent['headquarters'],
                credits=int(agent['credits']),
                starting_faction=agent['startingFaction'],
                ship_count=int(agent['shipCount']),
            )
        )


    @staticmethod
    def get_agent(callsign: str):
        pass


    @staticmethod
    def details(callsign: str) -> dict:
        endpoint = f'https://api.spacetraders.io/v2/agents/{callsign}'
        return {}
