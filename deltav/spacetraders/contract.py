from dataclasses import dataclass
from datetime import datetime
from typing import cast

from deltav.spacetraders.enums.contract import ContractType
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.enums.market import TradeSymbol
from deltav.spacetraders.api.request import SpaceTradersAPIRequest 
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.response import SpaceTradersAPIResponse, SpaceTradersAPIResShape, SpaceTradersAPIResData

from deltav.spacetraders.models.contract import ContractShape

class Contract:

    # def __init__(
    #         self, 
    #         id: str,
    #         type: ContractType, 
    #         terms: dict[Any, Any],
    #         accepted: bool,
    #         fulfilled: bool,
    #         expiration: datetime,
    #         deadlineToAccept: datetime
    #     ) -> None:
    #     self.id: str = id
    #     self.type: ContractType = ContractType.PROCUREMENT if type == 'PROCUREMENT' else ContractType(type)
    #
    #     deliver_term = terms.get('deliver', [{}])[0]
    #
    #     self.terms: ContractTerms = ContractTerms(
    #         deadline=datetime.fromisoformat(terms['deadline'].replace('Z', '+00:00')),
    #         payment_on_accept=terms.get('payment', {}).get('onAccepted', 0),
    #         payment_on_fulfil=terms.get('payment', {}).get('onFulfilled', 0),
    #         deliver_trade_symbol=TradeSymbol[deliver_term.get('tradeSymbol', 'IRON_ORE').upper()], 
    #         deliver_destination=deliver_term.get('destinationSymbol', ''),
    #         deliver_units_required=deliver_term.get('unitsRequired', 0),
    #         deliver_units_fulfilled=deliver_term.get('unitsFulfilled', 0)
    #     )
    #
    #     self.accepted: bool = accepted
    #     self.fulfilled: bool = fulfilled
    #     # TODO: convert these to datetime objects
    #     self.expiration: str = str(expiration)
    #     self.deadlineToAccept: str = str(deadlineToAccept)


    @classmethod 
    def get_contracts(cls) -> list[ContractShape] | SpaceTradersAPIError:
        req =  SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS) \
            .with_agent_token() \
            .build()
         
        match (res := SpaceTradersAPIClient.call(req)):
            case SpaceTradersAPIResponse():
                data: list[ContractShape] = cast(list[ContractShape], res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    
        # match res:
        #     case SpaceTradersAPIResponse():
        #         data = res.spacetraders['data']
        #     case SpaceTradersAPIErrorCodes():
        #         raise ValueError
        # 
        # contracts = []
        # for contract in data:
        #     contracts.append(cls(
        #         id=contract['id'],
        #         type=ContractType[contract['type']],
        #         terms=contract['terms'],
        #         accepted=contract['accepted'],
        #         fulfilled=contract['fulfilled'],
        #         expiration=datetime.fromisoformat(contract['expiration']),
        #         deadlineToAccept=datetime.fromisoformat(contract['deadlineToAccept']),
        #     ))
        # 
        # return contracts if contracts is not None else []
    

    @classmethod 
    def get_contract(cls, contract_id) -> ContractShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACT) \
            .path_params(contract_id) \
            .with_agent_token() \
            .build()
    
        match (res := SpaceTradersAPIClient.call(req)):
            case SpaceTradersAPIResponse():
                data: ContractShape = cast(ContractShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err
        
 



    # @staticmethod
    # def accept(contract_id: str) :
    #     res = SpaceTradersAPIRequest() \
    #         .endpoint(SpaceTradersAPIEndpoint.ACCEPT_CONTRACT) \
    #         .params(list([contract_id])) \
    #         .call()
    #
    #     match res:
    #         case SpaceTradersAPIResponse():
    #             error = res.spacetraders['error']
    #             code = error['code']
    #             message = error['message']
    #             if error is not None:
    #                 print(f"Error accepting contract {contract_id}")
    #                 print(f"\tCode: {code}\n\tMessage: {message}")
    #                 return
    #                 #raise ValueError(error)
    #             data = res.spacetraders['data']
    #
    #             
    #         case SpaceTradersAPIErrorCodes():
    #             print("contract accept error")
    #             raise ValueError
    #     return data if data is not None else []
        

    # def negotiate_contract(self):
    #     pass


    # def reject(self):
    #     pass


    # def deliver(self):
    #     pass


    # def __str__(self) -> str:
    #     status = []
    #     if self.accepted:
    #         status.append("Accepted")
    #     if self.fulfilled:
    #         status.append("Fulfilled")
    #     if not status:
    #         status.append("Not Accepted")
    #     
    #     return (f"Contract ID: {self.id} ({', '.join(status)})\n"
    #             f"  Type: {self.type.name}\n"
    #             # f"  Faction: {self.faction.symbol if hasattr(self.faction, 'symbol') else self.faction}\n" # Assuming Faction has a symbol attribute
    #             f"  Expires: {self.expiration.strftime('%Y-%m-%d %H:%M:%S')}\n"
    #             f"  Deadline to Accept: {self.deadlineToAccept.strftime('%Y-%m-%d %H:%M:%S')}\n"
    #             f"  Terms: Deliver {self.terms.deliver_units_required} {self.terms.deliver_trade_symbol.name} "
    #             f"to {self.terms.deliver_destination} "
    #             f"({self.terms.deliver_units_fulfilled}/{self.terms.deliver_units_required} fulfilled)")

