from deltav.config import CONFIG
from deltav.spacetraders.account import Account
from deltav.spacetraders.api.client import MAX_PAGE_LIMIT
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.models.agent import RegisterAgentData, AgentShape
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.ship import Ship


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
        # self.ships: list[Ship] = self.my_ships()
        # self.contracts: list[Contract] = self.my_contracts()


    def my_agent(self) -> SpaceTradersAPIRequest:
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_AGENT) \
            .build()
        

    # def my_ships(self) -> SpaceTradersAPIRequest:
    #     return SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS) \
    #     
    #     ships = res.spacetraders['data']
    #
    #     return ships if ships is not None else []
    

    # def my_contracts(self) -> SpaceTradersAPIRequest:
    #     return SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS) \
    #     
    #     contracts = res.spacetraders['data']
    #
    #     return contracts if contracts is not None else []


    @staticmethod
    def register(agent_data: RegisterAgentData) -> SpaceTradersAPIRequest:
        return SpaceTradersAPIRequest() \
            .builder() \
            .endpoint(SpaceTradersAPIEndpoint.REGISTER) \
            .data(agent_data) \
            .build()

        # match res:
        #     case SpaceTradersAPIResponse():
        #         data = res.spacetraders['data'] 
        #     case SpaceTradersAPIErrorCodes():
        #         raise ValueError

        # agent = data['agent']
        # return cls(
        #     data['token'], 
        #     { 
        #         'account_id': agent['accountId'],
        #         'symbol': agent['symbol'],
        #         'headquarters': agent['headquarters'],
        #         'credits': int(agent['credits']),
        #         'starting_faction': FactionSymbol[agent['startingFaction']],
        #         'ship_count': int(agent['shipCount']),
        #     } 
        # )


    @staticmethod
    def get_agent(callsign: str) -> SpaceTradersAPIRequest:
        return SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT) \
            .path_params(callsign) \
            .build()


    # @staticmethod
    # def get_agents(
    #     pages: int | range = -1,
    #     limit: int = MAX_PAGE_LIMIT
    # ) -> SpaceTradersAPIRequest:
    #
    #     paged_req = lambda p=1: SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.GET_AGENTS) \
    #         .page_number(p) \
    #
    #     # Here, -1 implies all pages, think res_pages[:-1]
    #     if pages == -1:
    #         res = paged_req()
    #
    #         pages_remaining: int = int(int(res.spacetraders['meta']['total']) / limit) 
    #
    #         for page in range(2, pages_remaining+1):
    #             res = paged_req(page)
    #
    #     match pages:
    #         case int():
    #             req = paged_req(pages)
    #         case range():
    #             for page in pages:
    #                 req = paged_req(pages)
    #
    #     return []

