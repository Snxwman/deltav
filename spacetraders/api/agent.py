from dataclasses import dataclass
import pprint
from typing import TypedDict

from spacetraders.config import CONFIG

from spacetraders.api.account import Account
from spacetraders.api.api import MAX_PAGE_LIMIT, SpaceTradersAPI, SpaceTradersAPIRequest, SpaceTradersAPIResponse
from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.contract import Contract
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint
from spacetraders.api.faction import Faction
from spacetraders.api.ship import Ship

class RegisterAgentData(TypedDict):
    symbol: str
    faction: str
    # email: str | None


@dataclass
class AgentInfo():
    accountId: str | None  # Only available if this is 'our' account.
    callsign: str
    headquarters: str
    credits: int
    starting_faction: Faction
    ship_count: int


class Agent:
    known_agents:list[AgentInfo] = []

    def __init__(self, token: str, agent_info: AgentInfo | None = None) -> None:
        self.token: str = token

        if agent_info is None:
            agent_info = self.my_agent()

        self.account: Account = Account(agent_info.accountId)
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
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_AGENT) \
            .call()
        
        agent = res.spacetraders['data']['agent']
        return AgentInfo(
            accountId=agent['accountId'],
            callsign=agent['symbol'],
            headquarters=agent['headquarters'],
            credits=int(agent['credits']),
            starting_faction=agent['startingFaction'],
            ship_count=int(agent['shipCount']),
        ) 


    def my_ships(self) -> list[Ship]:
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS) \
            .call()
        
        ships = res.spacetraders['data']

        return ships if ships is not None else []
    
    


    def my_contracts(self) -> list[Contract]:
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS) \
            .call()
        
        contracts = res.spacetraders['data']

        return contracts if contracts is not None else []
    
    def accept_contract(contract_id: str) -> Contract:
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.ACCEPT_CONTRACT) \
            .params(list([contract_id])) \
            .call()

        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            
            case SpaceTradersAPIError():
                raise ValueError
        return Contract(**data['contract'])

    @classmethod
    def register(cls, agent_data: RegisterAgentData) -> 'Agent':
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.REGISTER) \
            .data(agent_data) \
            .call()

        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data'] 
            case SpaceTradersAPIError():
                raise ValueError

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
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT) \
            .params(list([callsign])) \
            .call()


        agent = res.spacetraders['data']
        return AgentInfo(
            accountId = 'cmb8ctww5004ctm16gjcvr9qx', #=agent['accountId'],
            callsign=agent['symbol'],
            headquarters=agent['headquarters'],
            credits=int(agent['credits']),
            starting_faction=agent['startingFaction'],
            ship_count=int(agent['shipCount']),
        )


    @staticmethod
    def get_agents(
        pages: int | range = -1,
        limit: int = MAX_PAGE_LIMIT
        ) -> list[AgentInfo] | SpaceTradersAPIError:

        paged_req = lambda p=1: SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENTS) \
            .page_number(p) \
            .call()

        # Here, -1 implies all pages, think res_pages[:-1]
        if pages == -1:
            res = paged_req()

            pages_remaining: int = int(int(res.spacetraders['meta']['total']) / limit) 

            for page in range(2, pages_remaining+1):
                res = paged_req(page)

        match pages:
            case int():
                req = paged_req(pages)
            case range():
                for page in pages:
                    req = paged_req(pages)

        return []

