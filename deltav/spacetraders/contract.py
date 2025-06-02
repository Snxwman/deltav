from datetime import datetime, timedelta
from typing import cast

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.contract import ContractType
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.market import TradeSymbol
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.contract import (
    ContractDeliverResponseShape,
    ContractDeliverShape,
    ContractShape,
    ContractTermsShape,
)
from deltav.spacetraders.models.endpoint import AcceptContractShape


class Contract:
    def __init__(self, data: ContractShape) -> None:
        self.id: str = data['id']
        self.faction: Faction = Faction.get_by_symbol(data['faction_symbol'])
        self.type: ContractType = data['type']
        self.terms: ContractTermsShape = data['terms']
        self.accepted: bool = data['accepted']
        self.fulfilled: bool = data['fulfilled']
        self.deadline_to_accept: datetime = data['deadline_to_accept']

        self._negotiated_at: datetime
        self._accepted_at: datetime
        self._closed_at: datetime
        # self._closed_reason:  # fulfilled, abandonded, expired, ...

    def update(self, data: ContractShape) -> None:
        self.terms = data['terms']
        self.accepted = data['accepted']
        self.fulfilled = data['fulfilled']

    @property
    def deadline(self) -> datetime:
        return self.terms['deadline']

    @property
    def time_to_deadline(self) -> timedelta:
        return self.deadline - datetime.now()

    @property
    def payment_on_accept(self) -> int:
        return self.terms['payment']['on_accepted']

    @property
    def payment_on_fulfilled(self) -> int:
        return self.terms['payment']['on_fulfilled']

    @property
    def deliverables(self) -> list[ContractDeliverShape]:
        return [deliverable for deliverable in self.terms['deliver']]

    def get_deliverable_by_trade_symbol(self, symbol: TradeSymbol) -> ContractDeliverShape | None:
        for deliverable in self.deliverables:
            if deliverable['trade_symbol'] == symbol:
                return deliverable

    # QUESTION: Should this be in Agent?
    def accept(self) -> AcceptContractShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.ACCEPT_CONTRACT)
            .path_params(self.id)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(AcceptContractShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    def deliver(self, symbol: TradeSymbol, units: int = 0) -> ContractDeliverResponseShape | SpaceTradersAPIError:
        # FIX: Move out of this method
        # FIX: Data should be acquired from ship instances
        deliverable: ContractDeliverShape = {
            'ship_symbol': '',
            'trade_symbol': symbol.name,
            'units': units,
        }

        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.DELIVER_CONTRACT)
            .path_params(self.id)
            .with_token()
            .data(deliverable)
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ContractDeliverResponseShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    def fulfill(self) -> ContractShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.FULFILL_CONTRACT)
            .path_params(self.id)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ContractShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    # QUESTION: Should this be in Agent?
    def fetch_contracts(self) -> list[ContractShape] | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS)
            .with_token()
            .build()
        )  # fmt: skip

        match res:
            case SpaceTradersAPIResponse():
                return cast(list[ContractShape], res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def fetch_contract(contract_id: str) -> ContractShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACT)
            .path_params(contract_id)
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(ContractShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err
