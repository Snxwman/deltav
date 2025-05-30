from spacetraders.api.enums import FactionSymbol
from spacetraders.config import CONFIG

from spacetraders.api.account import Account
from spacetraders.api.api import MAX_PAGE_LIMIT, SpaceTradersAPIRequest, SpaceTradersAPIResponse
from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.data import RegisterAgentData
from spacetraders.api.response import AgentShape
from spacetraders.api.contract import Contract
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint
from spacetraders.api.ship import Ship


class Agent:
    def __init__(self, token: str, agent_info: AgentShape) -> None:
        self.token: str = token

        if agent_info['account_id'] is not None:
            self.account: Account = Account(agent_info['account_id'])

        self.callsign: str = agent_info['symbol']
        self.credits: int = agent_info['credits']
        self.faction: FactionSymbol = agent_info['starting_faction']
        self.headquarters: str = agent_info['headquarters']
        self.ship_count: int = agent_info['ship_count']
        self.ships: list[Ship] = self.my_ships()
        self.contracts: list[Contract] = self.my_contracts()


    def save_to_file(self):
        ...
    

    def my_agent(self) -> AgentShape:
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_AGENT) \
            .call()
        
        agent = res.spacetraders['data']['agent']
        return { 
            'account_id': agent['accountId'],
            'symbol': agent['symbol'],
            'headquarters': agent['headquarters'],
            'credits': agent['credits'],
            'starting_faction': FactionSymbol[agent['startingFaction']],
            'ship_count': agent['shipCount'],
        } 


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
            { 
                'account_id': agent['accountId'],
                'symbol': agent['symbol'],
                'headquarters': agent['headquarters'],
                'credits': int(agent['credits']),
                'starting_faction': FactionSymbol[agent['startingFaction']],
                'ship_count': int(agent['shipCount']),
            } 
        )

    @staticmethod
    def get_agent(callsign: str) -> AgentShape | SpaceTradersAPIError:
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT) \
            .params(list([callsign])) \
            .call()


        agent = res.spacetraders['data']
        return { 
            'account_id': agent['accountId'],
            'symbol': agent['symbol'],
            'headquarters': agent['headquarters'],
            'credits': agent['credits'],
            'starting_faction': FactionSymbol[agent['startingFaction']],
            'ship_count': agent['shipCount'],
        } 

    @staticmethod
    def get_agents(
        pages: int | range = -1,
        limit: int = MAX_PAGE_LIMIT
        ) -> list[AgentShape] | SpaceTradersAPIError:

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

