from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.enums.contract import ContractType
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.ship import ShipCargoShape


class ContractPaymentShape(SpaceTradersAPIResShape):
    on_accepted: int
    on_fulfilled: int


class ContractDeliverShape(SpaceTradersAPIResShape):
    ship_symbol: str
    trade_symbol: str
    units: int


class ContractDeliverResponseShape(SpaceTradersAPIResShape):
    contract: ContractShape
    cargo: ShipCargoShape


class ContractTermsShape(SpaceTradersAPIResShape):
    deadline: datetime
    payment: ContractPaymentShape
    deliver: list[ContractDeliverShape]


class ContractShape(SpaceTradersAPIResShape):
    id: str
    factionSymbol: FactionSymbol
    type: ContractType
    terms: ContractTermsShape
    accepted: bool
    fulfilled: bool
    deadlineToAccept: datetime
