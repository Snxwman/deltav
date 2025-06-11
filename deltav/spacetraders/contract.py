from __future__ import annotations

from datetime import UTC, datetime, timedelta

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.contract import ContractType
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.market import TradeSymbol
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.contract import (
    ContractAcceptShape,
    ContractDeliverReqShape,
    ContractDeliverResShape,
    ContractShape,
    ContractTermsShape,
)


class Contract:
    def __init__(self, data: ContractShape) -> None:
        self.id: str = data.id
        self.faction: Faction = Faction.get_faction(data.faction_symbol)
        self.type: ContractType = data.type
        self.terms: ContractTermsShape = data.terms
        self.accepted: bool = data.accepted
        self.fulfilled: bool = data.fulfilled
        self.deadline_to_accept: datetime = data.deadline_to_accept

        self._negotiated_at: datetime | None = None
        self._accepted_at: datetime | None = None
        self._closed_at: datetime | None = None
        # self._closed_reason:  # fulfilled, abandonded, expired, ...

    def update(self, data: ContractShape) -> None:
        self.terms = data.terms
        self.accepted = data.accepted
        self.fulfilled = data.fulfilled

    @property
    def deadline(self) -> datetime:
        return self.terms.deadline

    @property
    def is_expired(self) -> bool:
        now = datetime.now(tz=UTC)

        if self.accepted and self.deadline <= now:
            self._closed_at = self.deadline
            return True
        elif not self.accepted and self.deadline_to_accept <= now:  # noqa: RET505
            self._closed_at = self.deadline_to_accept
            return True
        else:
            return False

    @property
    def is_closed(self) -> bool:
        return True if self._closed_at is not None else False

    @property
    def time_to_deadline(self) -> timedelta:
        return self.deadline - datetime.now(tz=UTC)

    @property
    def payment_on_accept(self) -> int:
        return self.terms.payment.on_accepted

    @property
    def payment_on_fulfilled(self) -> int:
        return self.terms.payment.on_fulfilled

    @property
    def deliverables(self) -> list[ContractDeliverResShape]:
        return self.terms.deliver

    def get_deliverable_by_symbol(self, symbol: TradeSymbol) -> ContractDeliverResShape | None:
        for deliverable in self.deliverables:
            if deliverable.trade_symbol == symbol:
                return deliverable
        return None

    def _accept(self) -> ContractAcceptShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractAcceptShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.ACCEPT_CONTRACT)
            .path_params(self.id)
            .token()
            .build(),
        ).unwrap()

    def _deliver(self, symbol: TradeSymbol, units: int = 0) -> ContractDeliverResShape | SpaceTradersAPIError:
        # FIX: Move out of this method
        # FIX: Data should be acquired from ship instances
        deliverable = ContractDeliverReqShape(
            ship_symbol='',
            trade_symbol=symbol.name,
            units=units,
        )

        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractDeliverResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.DELIVER_CONTRACT)
            .path_params(self.id)
            .token()
            .data(deliverable)
            .build(),
        ).unwrap()

    def _fulfill(self) -> ContractShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.FULFILL_CONTRACT)
            .path_params(self.id)
            .token()
            .build(),
        ).unwrap()

    @staticmethod
    def fetch_contract(contract_id: str) -> ContractShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_CONTRACT)
            .path_params(contract_id)
            .token()
            .build(),
        ).unwrap()
