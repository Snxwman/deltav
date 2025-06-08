from loguru import logger

from deltav.config.config import Config
from deltav.spacetraders.account import Account
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models.agent import AgentShape, PublicAgentShape
from deltav.spacetraders.models.contract import ContractsShape
from deltav.spacetraders.models.endpoint import AgentRegisterReqData, AgentRegisterResData
from deltav.spacetraders.models.ship import ShipsShape
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.token import AgentToken


# TODO: Convert token to an actual JWT type
class Agent:
    def __init__(self, token: AgentToken | None = None, data: AgentShape | PublicAgentShape | None = None) -> None:
        logger.debug('Initializing new agent')
        logger.trace(f'token={"none" if token is None else token.hash}')
        logger.trace(f'data={"none" if data is None else data}')

        self._account: Account | None = None
        self._token: AgentToken | None = token
        self._account_id: str = ''
        # TODO: Track sold and scrapped ships
        self._ships: list[Ship] = []
        self._ship_count: int = 0
        self._active_contract: Contract
        self._past_contracts: list[Contract] = []
        self.symbol: str = ''
        self.credits: int = 0
        # self.faction: Faction
        self.headquarters: str = ''

        if data is None:
            res = self._fetch_agent()
            if isinstance(res, AgentShape):
                data = res
            else:
                raise TypeError('Agent() failed to get proper shape')

        self.symbol = data.symbol
        self.credits = data.credits
        # self.faction = Faction(data.starting_faction)
        self.headquarters = data.headquarters

        match data:
            case AgentShape():
                res = self._fetch_ships()
                if isinstance(res, ShipsShape):
                    self._ships = [Ship(ship) for ship in res.ships]

                res = self._fetch_contracts()
                if isinstance(res, ContractsShape):
                    for contract in res.contracts:
                        self._past_contracts.append(Contract(contract))
            case PublicAgentShape():
                pass

    @property
    def account(self) -> Account | None:
        return self._account

    @property
    def active_contract(self) -> Contract:
        return self._active_contract

    @property
    def past_contracts(self) -> list[Contract]:
        return self._past_contracts

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
    def token(self) -> AgentToken | None:
        return self._token

    @token.setter
    def token(self, token: AgentToken) -> None:
        self._token = token

    def _fetch_agent(self, symbol: str | None = None) -> AgentShape | PublicAgentShape | SpaceTradersAPIError:
        """Fetch the details for an agent from the SpaceTrader API.

        If callsign is None, fetch_agent will fetch the details for this Agent instance.

        Args:
            callsign: The callsign of the public agent to get.

        Returns:
            AgentShape | SpaceTradersAPIError
        """
        logger.trace(f"Attempting to fetch agent details for '{symbol if symbol is not None else 'my agent'}'")
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AgentShape]()
            .builder()
            .endpoint(
                SpaceTradersAPIEndpoint.GET_AGENT  # fmt: skip
                if symbol is None
                else SpaceTradersAPIEndpoint.GET_PUBLIC_AGENT  # fmt: skip
            )
            .path_params(symbol or '')
            .token(self.token)
            .build(),
        ).unwrap()

    def _fetch_contracts(self) -> ContractsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_CONTRACTS)
            .all_pages()
            .token(self.token)
            .build(),
        ).unwrap()  # fmt: skip

    def _fetch_ships(self) -> ShipsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.MY_SHIPS)
            .all_pages()
            .token(self.token)
            .build(),
        ).unwrap()

    @staticmethod
    def register(
        data: AgentRegisterReqData,
    ) -> AgentRegisterResData | SpaceTradersAPIError:
        """Register a new agent

        Args:
            data (RegisterAgentReqData): The data to be sent in the request

        Returns:
            RegisterAgentReqData | SpaceTradersAPIError
        """
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AgentRegisterResData]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.REGISTER_AGENT)
            .data(data)
            .build(),
        ).unwrap()
