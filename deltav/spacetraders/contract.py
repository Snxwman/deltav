from typing import cast

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.contract import ContractDeliverResponseShape, ContractDeliverShape, ContractShape
from deltav.spacetraders.models.endpoint import AcceptContractShape


class Contract:
    @classmethod
    def get_contracts(cls) -> list[ContractShape] | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder() \
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS) \
            .with_token() \
            .build()
         
        match SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse() as res:
                data: list[ContractShape] = cast(list[ContractShape], res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def get_contract(contract_id) -> ContractShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACT)
            .path_params(contract_id)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse():
                data: ContractShape = cast(ContractShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def accept(contract_id: str) -> AcceptContractShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.ACCEPT_CONTRACT)
            .path_params(contract_id)
            .with_token()
            .build()
        )

        match res := SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse():
                data: AcceptContractShape = cast(AcceptContractShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def deliver(
        contract_id: str, contract: ContractDeliverShape
    ) -> ContractDeliverResponseShape | SpaceTradersAPIError:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.DELIVER_CONTRACT)
            .path_params(contract_id)
            .with_agent_token()
            .data(contract)
            .build()
        )

        match res := SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse():
                data: ContractDeliverResponseShape = cast(ContractDeliverResponseShape, res.spacetraders.data)
                return data
            case SpaceTradersAPIError() as err:
                return err

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
