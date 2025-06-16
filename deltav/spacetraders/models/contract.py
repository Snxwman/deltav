# pyright: reportAny=false
from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape

if TYPE_CHECKING:
    from datetime import datetime

    from deltav.spacetraders.enums.contract import ContractType
    from deltav.spacetraders.enums.faction import FactionSymbol
    from deltav.spacetraders.enums.market import TradeSymbol
    from deltav.spacetraders.models.agent import AgentShape


class ContractShape(SpaceTradersAPIResShape):
    """

    id: str
    faction_symbol: FactionSymbol
    type: ContractType
    terms: ContractTermsShape
    accepted: bool
    fulfilled: bool
    deadline_to_accept: datetime
    """

    id: str
    faction_symbol: FactionSymbol
    type: ContractType
    terms: ContractTermsShape
    accepted: bool
    fulfilled: bool
    deadline_to_accept: datetime


class ContractsShape(SpaceTradersAPIResShape):
    """

    data: list[ContractShape]
    """

    contracts: list[ContractShape] = Field(alias='data')


class ContractAcceptShape(SpaceTradersAPIResShape):
    """

    contract: ContractShape
    agent: AgentShape
    """

    contract: ContractShape
    agent: AgentShape


class ContractDeliverReqShape(SpaceTradersAPIReqShape):
    """

    ship_symbol: str
    trade_symbol: str
    units: int
    """

    ship_symbol: str
    trade_symbol: str
    units: int


class ContractDeliverResShape(SpaceTradersAPIResShape):
    """

    trade_symbol: TradeSymbol
    destination_symbol: str
    units_required: int
    units_fulfilled: int
    """

    trade_symbol: TradeSymbol
    destination_symbol: str
    units_required: int
    units_fulfilled: int


class ContractPaymentShape(SpaceTradersAPIResShape):
    """

    on_accepted: int
    on_fulfilled: int
    """

    on_accepted: int
    on_fulfilled: int


class ContractTermsShape(SpaceTradersAPIResShape):
    """

    deadline: datetime
    payment: ContractPaymentShape
    deliver: list[ContractDeliverResShape]
    """

    deadline: datetime
    payment: ContractPaymentShape
    deliver: list[ContractDeliverResShape]
