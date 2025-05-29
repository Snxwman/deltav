from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from spacetraders.api.faction import Faction
from spacetraders.api.api import SpaceTradersAPIRequest, SpaceTradersAPIEndpoint, SpaceTradersAPIResponse, SpaceTradersAPIError


class ContractType(Enum):
    PROCUREMENT = auto()

class TradeSymbol(Enum):
    IRON_ORE = auto()

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

    def __init__(self):
        self.id: str
        self.faction: Faction
        self.type: ContractType
        self.terms: dict
        self.accepted: bool
        self.fulfilled: bool
        self.expiration: datetime
        self.accept_deadline: datetime

    def accept(self):
        pass

    def reject(self):
        pass

    def deliver(self):
        pass