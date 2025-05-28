from dataclasses import dataclass
from typing import Optional, Self, TypedDict

from spacetraders.api.account import Account
from spacetraders.api.api import MAX_PAGE_LIMIT, PagingData, SpaceTradersAPI, SpaceTradersAPIRequest, SpaceTradersAPIResponse
from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.contract import Contract
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint
from spacetraders.api.faction import Faction
from spacetraders.api.ship import Ship

class RegisterAgentData(TypedDict):
    symbol: str
    faction: str
    email: Optional[str]

@dataclass
class AgentInfo():
    account_id: Optional[str]  # Only available if this is 'our' account.
    callsign: str
    headquarters: str
    credits: int
    starting_faction: Faction
    ship_count: int

class Agent:
    known_agents:list[AgentInfo] = []

    def __init__(self, token:str, agent_info:Optional[AgentInfo]=None) -> None:
        self.token: str = token

        if agent_info is None:
            agent_info = self.my_agent()

        self.account: Account = Account(agent_info.account_id)
        self.callsign: str = agent_info.callsign
        self.credits: int = agent_info.credits 
        self.faction: Faction = agent_info.starting_faction 
        self.headquarters: str = agent_info.headquarters 
        self.ship_count: int = agent_info.ship_count 
        self.ships: list[Ship] = self.my_ships()
        self.contracts: list[Contract] = self.my_contracts()

        print()
        print(self.__dict__)


    def save_to_file(self):
        ...
    

    def my_agent(self) -> AgentInfo:
        endpoint = SpaceTradersAPIEndpoint.MY_AGENT

        req = SpaceTradersAPIRequest(endpoint, agent=self)
        res = SpaceTradersAPI.call(req)
        
        agent = res.spacetraders['data']['agent']
        return AgentInfo(
            account_id=agent['accountId'],
            callsign=agent['symbol'],
            headquarters=agent['headquarters'],
            credits=int(agent['credits']),
            starting_faction=agent['startingFaction'],
            ship_count=int(agent['shipCount']),
        ) 


    def my_ships(self) -> list[Ship]:
        return []
    

    def my_contracts(self) -> list[Contract]:
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
                callsign=agent['symbol'],
                headquarters=agent['headquarters'],
                credits=int(agent['credits']),
                starting_faction=agent['startingFaction'],
                ship_count=int(agent['shipCount']),
            )
        )


    @staticmethod
    def get_agent(callsign: str) -> AgentInfo | SpaceTradersAPIError:
        endpoint = SpaceTradersAPIEndpoint.GET_AGENT
        req = SpaceTradersAPIRequest(endpoint, params=list(callsign))
        res = SpaceTradersAPI.call(req)

        res = SpaceTradersAPI.call(
            SpaceTradersAPIRequest(
                SpaceTradersAPIEndpoint.GET_AGENT,
                params=list(callsign)
            )
        )

        res = SpaceTradersAPIRequest()
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT)
            .params(list(callsign))
            .call()


        agent = res.spacetraders['data']
        return AgentInfo(
            account_id=agent['accountId'],
            callsign=agent['symbol'],
            headquarters=agent['headquarters'],
            credits=int(agent['credits']),
            starting_faction=agent['startingFaction'],
            ship_count=int(agent['shipCount']),
        )


    @staticmethod
    def get_agents(pages:int|range=-1, limit:int=MAX_PAGE_LIMIT) -> list[AgentInfo] | SpaceTradersAPIError:
        endpoint = SpaceTradersAPIEndpoint.GET_AGENTS
        paged_req = lambda p=1: SpaceTradersAPIRequest(endpoint, paging=PagingData(p, limit))

        # Here, -1 implies all pages, think res_pages[:-1]
        if pages == -1:
            req = paged_req()
            res = SpaceTradersAPI.call(req)

            pages_remaining: int = int(int(res.spacetraders['meta']['total']) / limit) 

            for page in range(2, pages_remaining+1):
                req = paged_req(page)
                res = SpaceTradersAPI.call(req)

        match pages:
            case int():
                req = paged_req(pages)
            case range():
                for page in pages:
                    req = paged_req(pages)

        return []

