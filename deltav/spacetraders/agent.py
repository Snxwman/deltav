from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import final

from loguru import logger

from deltav.config.config import Config, StAgentConfig
from deltav.spacetraders.account import Account
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.agent import AgentEventShape, AgentEventsShape, AgentShape, PublicAgentShape
from deltav.spacetraders.models.contract import ContractsShape
from deltav.spacetraders.models.endpoint import AgentRegisterReqData, AgentRegisterResData
from deltav.spacetraders.models.faction import FactionReputationsShape
from deltav.spacetraders.models.market import TransactionShape
from deltav.spacetraders.models.ship import ShipsShape
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.token import AccountToken, AgentToken


class AgentABC(ABC):
    """Abstract base class for Agent and PublicAgent"""

    def __init__(self, data: AgentShape | PublicAgentShape) -> None:
        self._symbol: str = data.symbol
        self._credits: int = data.credits
        self._faction: Faction = Faction.get_faction(data.starting_faction)
        self._headquarters: str = data.headquarters
        self._ship_count: int = data.ship_count

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def credits(self) -> int:
        return self._credits

    @property
    def faction(self) -> Faction:
        return self._faction

    @property
    def headquarters(self) -> str:
        return self._headquarters

    @property
    def ship_count(self) -> int:
        return self._ship_count


@final
class Agent(AgentABC):
    # TODO: Better error handling (try not to raise and make custom error types)
    def __init__(self, token: AgentToken) -> None:
        """Class representing a SpaceTraders agent.
        This is an agent that the player's account owns.

        Will attempt to (re)register an agent on __init__() if the token is expired or invalid.

        Args:
        ```
        token (AgentToken)
        ```

        Properties:
        ```
        account (Account)
        token (AgentToken)
        contracts(list[Contract])
        active_contract (Contract)
        past_contracts (list[Contract])
        events (list[AgentEventShape])
        faction_reputations (dict[FactionSymbol, FactionReputationShape])
        ships (list[Ship])
        transactions (list[TransactionShape])
        ```
        """

        logger.debug('Initializing new Agent')
        logger.trace(f'Input: {token=}')

        self.__synced_api: bool
        self.__synced_db: bool

        self.__data: AgentShape
        self.__config: StAgentConfig

        self.__data_timestamp: datetime
        self.__contracts_timestamp: datetime
        self.__events_timestamp: datetime
        self.__faction_reputation_timestamp: datetime
        self.__ships_timestamp: datetime

        self._account: Account
        self._token: AgentToken = token
        self._active_contract: Contract | None = None
        self._past_contracts: list[Contract] = []
        self._events: list[AgentEventShape] = []
        self._faction_reputations: dict[FactionSymbol, int] = {}
        self._ships: list[Ship] = []
        self._transactions: list[TransactionShape] = []  # TODO: Make all transaction shapes a subclass

        if config := Config.get_agent_from_token(self.token):
            self.__config = config
        else:
            raise ValueError(f'No agent with token {self.token} in config.')

        self.__check_handle_token_expired()

        account_config = Config.get_account_from_agent_token(self.token)
        # Any agent MUST belong to an account, so if account_config is none, the user's config is invalid.
        assert account_config is not None
        # SpaceTraders API requires an agent token (?) to fetch the account details...
        self._account = Account.get_account(account_config.token, self.token)

        # self.__data has not been set above by self.__check_handle_token_expired()
        if not hasattr(self, '_Agent__data'):
            self.update_agent()

        super().__init__(self.__data)
        self.update_contracts()
        self.update_events()
        self.update_faction_reputations()
        self.update_ships()
        self.__hydrate_transactions()

    @property
    def account(self) -> Account:
        return self._account

    @property
    def contracts(self) -> list[Contract]:
        if self.active_contract:
            return [self.active_contract, *self.past_contracts]
        else:
            return self.past_contracts

    @property
    def active_contract(self) -> Contract | None:
        if self._active_contract is None:
            return None

        if self._active_contract.is_expired:
            self._past_contracts.append(self._active_contract)
            self._active_contract = None

        return self._active_contract

    @property
    def past_contracts(self) -> list[Contract]:
        return self._past_contracts

    @property
    def events(self) -> list[AgentEventShape]:
        return self._events

    @property
    def faction_reputations(self) -> dict[FactionSymbol, int]:
        return self._faction_reputations

    @property
    def ships(self) -> list[Ship]:
        return self._ships

    @ships.setter
    def ships(self, ships: list[Ship]) -> None:
        # TODO: Verify that a ship is actually owned by this agent
        self._ships = ships
        self._ship_count = len(self._ships)

    @property
    def token(self) -> AgentToken:
        return self._token

    @property
    def transactions(self) -> list[TransactionShape]:
        return self._transactions

    def get_faction_reputation(self, faction: FactionSymbol) -> int:
        return self._faction_reputations[faction]

    # def get_transactions_by_type(self, transaction_type: T) -> list[T]:
    #     ...

    def negotiate_contract(self) -> Contract | Exception:
        """Negotiate a new contract with the HQ.

        In order to negotiate a new contract, an agent must not have ongoing or
        offered contracts over the allowed maximum amount. Currently the maximum
        contracts an agent can have at a time is 1.

        Once a contract is negotiated, it is added to the list of contracts
        offered to the agent, which the agent can then accept.

        The ship must be present at any waypoint with a faction present to
        negotiate a contract with that faction.
        """
        ...

    def update_agent(self) -> None:
        match self._fetch_agent():
            case AgentShape() as res:
                self.__synced_api = True
                self.__data = res
                self.__data_timestamp = datetime.now()
                self._credits = res.credits
                self._ship_count = res.ship_count
            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_agent_err(err)

    def _fetch_agent(self) -> AgentShape | SpaceTradersAPIError:
        """Fetch the details for an agent from the SpaceTrader API.

        Returns:
            AgentShape | SpaceTradersAPIError
        """
        logger.trace(f"Attempting to fetch agent details for '{self.token=}'")
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AgentShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT)
            .token(self.token)
            .build(),
        ).unwrap()

    def __handle_fetch_agent_err(self, err: SpaceTradersAPIError) -> ValueError:
        # TODO: Check for spacetraders errors that can be solved.
        log_str = f"Got an error while fetching agent's data. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def update_contracts(self) -> None:
        match self._fetch_contracts():
            case ContractsShape() as res:
                contracts = [Contract(_contract) for _contract in res.contracts]
                for contract in contracts:
                    if contract.is_closed:
                        logger.trace(f'Adding contract {contract.id} to past contracts')
                        self._past_contracts.append(contract)
                    else:
                        logger.trace(f'Setting active contract to {contract.id}')
                        self._active_contract = contract
            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_contracts_err(err)

    def _fetch_contracts(self) -> ContractsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_CONTRACTS)
            .all_pages()
            .token(self.token)
            .build(),
        ).unwrap()  # fmt: skip

    def __handle_fetch_contracts_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's contracts. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def update_events(self) -> None:
        match self._fetch_events():
            case AgentEventsShape() as res:
                self._events = [event for event in res.events]
            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_events_err(err)

    def _fetch_events(self) -> AgentEventsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AgentEventsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT_EVENTS)
            .token(self.token)
            .build()
        ).unwrap()

    def __handle_fetch_events_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's events. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def update_faction_reputations(self) -> None:
        match self._fetch_faction_reputations():
            case FactionReputationsShape() as res:
                for faction in res.factions:
                    self._faction_reputations[faction.symbol] = faction.reputation
            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_faction_reputations_err(err)

    def _fetch_faction_reputations(self) -> FactionReputationsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[FactionReputationsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_FACTION_REPUTATIONS)
            .token(self.token)
            .build()
        ).unwrap()

    def __handle_fetch_faction_reputations_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's faction reputations. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def update_ships(self) -> None:
        match self._fetch_ships():
            case ShipsShape() as res:
                self._ships = [Ship(ship) for ship in res.ships]
            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_ships_err(err)

    def _fetch_ships(self) -> ShipsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIPS)
            .all_pages()
            .token(self.token)
            .build(),
        ).unwrap()

    def __handle_fetch_ships_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's ships. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def register(self) -> None:
        register_data = AgentRegisterReqData(
            symbol=self.__config.symbol,
            faction=self.__config.faction,
        )

        account_config = Config.get_account_from_agent_token(self.token)
        assert account_config is not None

        match self._register(register_data, account_config.token):
            case AgentRegisterResData() as res:
                self.__data = res.agent
                self.__data_timestamp = datetime.now()
                self._token = AgentToken(res.token)
                self._active_contract = Contract(res.contract)
                self._ships = [Ship(ship) for ship in res.ships]
                logger.info(f'Acquired new agent token {res.token}')
            case SpaceTradersAPIError() as err:
                raise self.__handle_register_err(err)

    def _register(self, data: AgentRegisterReqData, account_token: AccountToken) -> AgentRegisterResData | SpaceTradersAPIError:
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
            .token(account_token)
            .build(),
        ).unwrap()

    def __handle_register_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f'Got an error while registering agent. {err}'
        logger.error(log_str)
        return ValueError(log_str)

    def __check_handle_token_expired(self) -> None:
        token = self.token

        if token.is_expired and self.__config.autocreate:
            logger.trace('Token is expired and "autocreate = true"')
            self.register()  # TODO: Overwrite agent token in config file
        elif token.is_expired and not self.__config.autocreate:
            logger.error('Token is expired and "autocreate = false"')
            raise ValueError(f'Agent token expired {token.expiration}, and "autocreate = false"')

    def __hydrate_transactions(self) -> None: ...


@final
class PublicAgent(AgentABC):
    def __init__(self, symbol: str | None = None, data: PublicAgentShape | None = None) -> None:
        logger.debug('Initializing new PublicAgent')
        logger.trace(f'Input: symbol={"None" if symbol is None else symbol}')
        logger.trace(f'Input: data={"None" if data is None else data}')

        if symbol is None and data is None:
            raise ValueError('Must provide either symbol or data.')

        if data is None:
            match self._fetch_agent(symbol):  # pyright: ignore[reportArgumentType]
                case PublicAgentShape() as res:
                    data = res
                case SpaceTradersAPIError() as err:
                    raise self.__handle_fetch_agent_err(err)

        self._data: PublicAgentShape = data
        super().__init__(data)

    def _fetch_agent(self, symbol: str) -> PublicAgentShape | SpaceTradersAPIError:
        logger.trace(f"Attempting to fetch agent details for '{symbol}'")
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[PublicAgentShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_PUBLIC_AGENT)
            .path_params(symbol)
            .build(),
        ).unwrap()

    def __handle_fetch_agent_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching public agent's data. {err}"
        logger.error(log_str)
        return ValueError(log_str)
