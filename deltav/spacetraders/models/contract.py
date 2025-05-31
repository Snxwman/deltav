from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.enums.contract import ContractType
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.market import TradeSymbol
from deltav.spacetraders.models import SpaceTradersAPIResShape


class ContractPaymentShape(SpaceTradersAPIResShape):
    on_accepted: int
    on_fulfilled: int


class ContractDeliverShape(SpaceTradersAPIResShape):
    trade_symbol: TradeSymbol
    destination_symbol: str
    units_required: int
    units_fulfilled: int


class ContractTermsShape(SpaceTradersAPIResShape):
    deadline: datetime
    payment: ContractPaymentShape
    deliver: list[ContractDeliverShape]


class ContractShape(SpaceTradersAPIResShape):
    id: str
    faction_symbol: FactionSymbol
    type: ContractType
    terms: ContractTermsShape
    accepted: bool
    fulfilled: bool
    deadline_to_accept: datetime

