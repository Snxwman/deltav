from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from spacetraders.api.faction import Faction
from spacetraders.api.api import SpaceTradersAPIRequest, SpaceTradersAPIEndpoint, SpaceTradersAPIResponse, SpaceTradersAPIError


class ContractType(Enum):
    PROCUREMENT = auto()

class TradeSymbol(Enum):
    IRON_ORE = auto()
    ALUMINUM_ORE = auto()
    COPPER_ORE = auto()


@dataclass
class ContractTerms:
    deadline: datetime
    payment_on_accept: int
    payment_on_fulfil: int
    deliver_trade_symbol: TradeSymbol
    deliver_destination: str
    deliver_units_required: int
    deliver_units_fulfilled: int

    def remaining_units_to_deliver(self):
        return self.deliver_units_required - self.deliver_units_fulfilled

class Contract:

    def __init__(self, id: str,
                 type: ContractType, 
                 terms: dict,
                 accepted: bool,
                 fulfilled: bool,
                 expiration: datetime,
                 deadlineToAccept: datetime):
        self.id: str = id
        self.type: ContractType = ContractType.PROCUREMENT if type == 'PROCUREMENT' else ContractType(type)
        
        deliver_term = terms.get('deliver', [{}])[0]

        self.terms: ContractTerms = ContractTerms(
            deadline=datetime.fromisoformat(terms['deadline'].replace('Z', '+00:00')),
            payment_on_accept=terms.get('payment', {}).get('onAccepted', 0),
            payment_on_fulfil=terms.get('payment', {}).get('onFulfilled', 0),
            deliver_trade_symbol=TradeSymbol[deliver_term.get('tradeSymbol', 'IRON_ORE').upper()], 
            deliver_destination=deliver_term.get('destinationSymbol', ''),
            deliver_units_required=deliver_term.get('unitsRequired', 0),
            deliver_units_fulfilled=deliver_term.get('unitsFulfilled', 0)
        )
        
        self.accepted: bool = accepted
        self.fulfilled: bool = fulfilled
        # TODO: convert these to datetime objects
        self.expiration: str = expiration
        self.accept_deadline: str = deadlineToAccept


    @classmethod 
    def get_contracts(cls, active_agent: str):
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS) \
            .call()
    
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError
        
        contracts = []
        for contract in data:
            contracts.append(cls(
                id=contract['id'],
                type=ContractType[contract['type']],
                terms=contract['terms'],
                accepted=contract['accepted'],
                fulfilled=contract['fulfilled'],
                expiration=datetime.fromisoformat(contract['expiration']),
                deadlineToAccept=datetime.fromisoformat(contract['deadlineToAccept']),
            ))
        
        return contracts if contracts is not None else []
    
    @classmethod 
    def get_contract(cls, contract_id) -> 'Contract':
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACT) \
            .params(list([contract_id])) \
            .call()
    
        match res:
            case SpaceTradersAPIResponse():
                data = res.spacetraders['data']
            case SpaceTradersAPIError():
                raise ValueError
        
        contract = data[0]
        return cls(
            id=contract['id'],
            type=contract['type'],
            terms=contract['terms'],
            accepted=contract['accepted'],
            fulfilled=contract['fulfilled'],
            expiration=datetime.fromisoformat(contract['expiration']),
            accept_deadline=datetime.fromisoformat(contract['deadlineToAccept']),
        )

    @staticmethod
    def accept(contract_id: str) :
        res = SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.ACCEPT_CONTRACT) \
            .params(list([contract_id])) \
            .call()

        match res:
            case SpaceTradersAPIResponse():
                error = res.spacetraders['error']
                code = error['code']
                message = error['message']
                if error is not None:
                    print(f"Error accepting contract {contract_id}")
                    print(f"\tCode: {code}\n\tMessage: {message}")
                    return
                    #raise ValueError(error)
                data = res.spacetraders['data']

                
            case SpaceTradersAPIError():
                print("contract accept error")
                raise ValueError
        return data if data is not None else []
        
    def negotiate_contract(self):
        pass

    def reject(self):
        pass

    def deliver(self):
        pass

    def __str__(self) -> str:
        status = []
        if self.accepted:
            status.append("Accepted")
        if self.fulfilled:
            status.append("Fulfilled")
        if not status:
            status.append("Not Accepted")
        
        return (f"Contract ID: {self.id} ({', '.join(status)})\n"
                f"  Type: {self.type.name}\n"
                # f"  Faction: {self.faction.symbol if hasattr(self.faction, 'symbol') else self.faction}\n" # Assuming Faction has a symbol attribute
                f"  Expires: {self.expiration.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"  Deadline to Accept: {self.accept_deadline.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"  Terms: Deliver {self.terms.deliver_units_required} {self.terms.deliver_trade_symbol.name} "
                f"to {self.terms.deliver_destination} "
                f"({self.terms.deliver_units_fulfilled}/{self.terms.deliver_units_required} fulfilled)")
