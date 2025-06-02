from typing import cast

from deltav.spacetraders.account import Account
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.endpoint import RegisterAgentReqData, RegisterAgentResData
from deltav.spacetraders.ship import Ship


# TODO: Convert token to an actual JWT type
class Agent:
    def __init__(self, token: str, data: AgentShape) -> None:
        self._token: str
        # TODO: Track sold and scrapped ships
        self._ships: list[Ship]
        self._ship_count: int
        self._active_contract: Contract
        self._past_contracts: list[Contract]

        self.account: Account | None
        if data['account_id'] is not None:
            self.account = Account(data['account_id'])
        else:
            self.account = None

        self.symbol: str = data['symbol']
        self.credits: int = data['credits']
        self.faction: Faction = Faction.get_by_symbol(data['starting_faction'])
        self.headquarters: str = data['headquarters']

        self.token = token

    @property
    def ships(self) -> list[Ship]:
        return self._ships

    @ships.setter
    def ships(self, ships: list[Ship]) -> None:
        # TODO: Verify that a ship is actually owned by this agent
        self._ships = ships
        self._ship_count = len(self._ships)

    @property
    def ship_count(self) -> int:
        return self._ship_count

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        # TODO: Verify token is valid
        self._token = token

    def fetch_agent(self, callsign: str | None = None) -> AgentShape | SpaceTradersAPIError:
        """Fetch the details for an agent from the SpaceTrader API.

        If callsign is None, fetch_agent will fetch the details for this Agent instance.

        Args:
            callsign: The callsign of the public agent to get.

        Returns:
            AgentShape | SpaceTradersAPIError
        """
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_AGENT if callsign is None else SpaceTradersAPIEndpoint.GET_AGENT)
            .path_params(callsign or '')
            .with_token()
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(AgentShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def register(
        data: RegisterAgentReqData,
    ) -> RegisterAgentResData | SpaceTradersAPIError:
        """Register a new agent

        Args:
            data (RegisterAgentReqData): The data to be sent in the request

        Returns:
            RegisterAgentReqData | SpaceTradersAPIError
        """
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest().builder().endpoint(SpaceTradersAPIEndpoint.REGISTER).data(data).build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(RegisterAgentResData, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err
