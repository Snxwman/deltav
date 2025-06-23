from __future__ import annotations

from abc import ABC
from datetime import UTC, datetime
from typing import TYPE_CHECKING, final

from loguru import logger

from deltav.config.config import Config, StAgentConfig
from deltav.spacetraders.account import Account
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.enums.ship import ShipType
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.agent import (
    AgentEventShape,
    AgentEventsShape,
    AgentShape,
    PublicAgentShape,
)
from deltav.spacetraders.models.contract import ContractsShape
from deltav.spacetraders.models.endpoint import AgentRegisterReqShape, AgentRegisterResShape
from deltav.spacetraders.models.faction import FactionReputationsShape
from deltav.spacetraders.models.ship import ShipPurchaseReqShape, ShipPurchaseResShape, ShipsShape
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.token import AccountToken, AgentToken
from deltav.store.db.agent import AgentEventRecord, AgentRecord
from deltav.store.db.faction import FactionReputationRecord
from deltav.store.db.waypoint import TransactionRecord

if TYPE_CHECKING:
    from deltav.spacetraders.models.transaction import TransactionShape


class AgentABC(ABC):  # noqa: B024
    """Abstract base class for Agent and PublicAgent"""

    def __init__(self, data: AgentRecord) -> None:
        self._symbol: str = data.symbol
        self._credits: int = data.credits
        self._faction: Faction = Faction.get_faction(FactionSymbol[data.faction_symbol])
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
        token(AgentToken)
        ```

        Properties:
        ```
        account(Account)
        token(AgentToken)
        contracts(list[Contract])
        active_contract(Contract)
        past_contracts(list[Contract])
        events(list[AgentEventShape])
        faction_reputations(dict[FactionSymbol, FactionReputationShape])
        ships(list[Ship])
        transactions(list[TransactionShape])
        ```
        """

        logger.debug('Initializing new Agent')
        logger.trace(f'Input: {token=}')

        now = datetime.now(tz=UTC)

        self.__synced_api: bool = False
        self.__synced_db: bool = False
        self.__synced_db_timestamp: datetime = now
        self.__synced_api_timestamp: datetime = now

        self.__config: StAgentConfig
        self.__data: AgentRecord
        self.__data_timestamp: datetime = now

        self.__contracts_timestamp: datetime = now
        self.__events_timestamp: datetime = now
        self.__faction_reputation_timestamp: datetime = now
        self.__ships_timestamp: datetime = now

        self._account: Account
        self._token: AgentToken = token
        self._active_contract: Contract | None = None
        self._past_contracts: list[Contract] = []
        self._events: list[AgentEventRecord] = []
        self._faction_reputations: dict[FactionSymbol, int] = {}
        self._ships: list[Ship] = []
        self._transactions: list[TransactionRecord] = []

        if config := Config.get_agent_from_token(self.token):
            self.__config = config
        else:
            msg = f'No agent with token {self.token} in config.'
            raise ValueError(msg)

        self.__check_handle_token_expired()

        # All agents MUST belong to an account.
        # If account_config is None, the user's config is invalid.
        account_config = Config.get_account_from_agent_token(self.token)
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

    def __check_handle_token_expired(self) -> None:
        token = self.token

        if token.is_expired and self.__config.autocreate:
            logger.trace('Token is expired and "autocreate = true"')
            self.register()  # TODO: Overwrite agent token in config file
        elif token.is_expired and not self.__config.autocreate:
            logger.error('Token is expired and "autocreate = false"')
            msg = f'Agent token expired {token.expiration}, and "autocreate = false"'
            raise ValueError(msg)

    def __hydrate_from_api(self) -> None: ...

    def __hydrate_from_db(self) -> None: ...

    def __hydrate_from_record(self) -> None: ...

    def __hydrate_from_shape(self) -> None: ...

    def __hydrate_transactions(self) -> None: ...

    @property
    def account(self) -> Account:
        return self._account

    @property
    def contracts(self) -> list[Contract]:
        if self.active_contract:
            return [self.active_contract, *self.past_contracts]
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
    def events(self) -> list[AgentEventRecord]:
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
    def transactions(self) -> list[TransactionRecord]:
        return self._transactions

    def add_transaction(self, transaction: TransactionRecord) -> None:
        self._transactions.append(transaction)

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
        ...  # noqa: PIE790

    def update_agent(self, data: AgentShape | None = None, *, from_api: bool = False) -> None:
        if isinstance(data, AgentShape):
            _data = data
        else:
            _data = self._fetch_agent()
            from_api = True

        match _data:
            case AgentShape():
                timestamp = self.__data_timestamp
                self.__synced_api = from_api
                self.__data = _data
                self.__data_timestamp = datetime.now(tz=UTC) if from_api else timestamp

                self._credits = _data.credits
                self._ship_count = _data.ship_count

            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_agent_err(err)

    def update_contracts(self, data: ContractsShape | None = None) -> None:
        _data = data if isinstance(data, ContractsShape) else self._fetch_contracts()

        match _data:
            case ContractsShape():
                self.__contracts_timestamp = datetime.now(tz=UTC)

                for contract in [Contract(_) for _ in _data.contracts]:
                    if contract.is_closed:
                        logger.trace(f'Adding contract {contract.id} to past contracts')
                        self._past_contracts.append(contract)
                    else:
                        logger.trace(f'Setting active contract to {contract.id}')
                        self._active_contract = contract

            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_contracts_err(err)

    def update_events(self, data: AgentEventsShape | None = None) -> None:
        _data = data if isinstance(data, AgentEventsShape) else self._fetch_events()

        match _data:
            case AgentEventsShape():
                self.__events_timestamp = datetime.now(tz=UTC)
                self._events = list(_data.events)

            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_events_err(err)

    def update_faction_reputations(self, data: FactionReputationsShape | None = None) -> None:
        _data = (
            data if isinstance(data, FactionReputationsShape) else self._fetch_faction_reputations()
        )

        match _data:
            case FactionReputationsShape():
                self.__faction_reputation_timestamp = datetime.now(tz=UTC)

                for faction in _data.factions:
                    self._faction_reputations[faction.symbol] = faction.reputation

            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_faction_reputations_err(err)

    def update_ships(self, data: ShipsShape | None = None) -> None:
        _data = data if isinstance(data, ShipsShape) else self._fetch_ships()

        match _data:
            case ShipsShape() as res:
                self.__ships_timestamp = datetime.now(tz=UTC)
                self._ships = [Ship(ship) for ship in res.ships]

            case SpaceTradersAPIError() as err:
                raise self.__handle_fetch_ships_err(err)

    # TODO: Make a type to represent a failed action
    def purchase_ship(
        self, ship_type: ShipType, waypoint: str | None = None
    ) -> Ship | None | SpaceTradersAPIError:
        """Attempts to purchase a ship of the given type.
        Will search all ships owned by this agent to find possible transactions.

        If multiple matches are found... todo

        Args:
            ship_type - The type of ship to be purchased.
            waypoint - Attempt to buy the ship from this waypoint.

        Returns:
            Ship - A ship was purchased
            () - Purchasing this ship_type is not possible
            SpaceTradersAPIError

        SpaceTraders Docs:
        Purchase a ship from a Shipyard.
        In order to use this function, a ship under your agent's ownership must
        be in a waypoint that has the Shipyard trait, and the Shipyard must sell
        the type of the desired ship.
        """
        # TODO: Checks
        #   - Ship in waypoint with Shipyard trait
        #   - Shipyard sells the desired shiptype

        waypoint = ''
        purchase_data = ShipPurchaseReqShape(
            ship_type=ship_type,
            waypoint_symbol=waypoint
        )  # fmt: skip

        match self._purchase_ship(purchase_data):
            case ShipPurchaseResShape() as res:
                self.update_agent(res.agent)
                self.add_transaction(res.transaction)
                return Ship(res.ship)
            case SpaceTradersAPIError() as err:
                raise self.__handle_purchase_ship_err(err)

    def register(self) -> None:
        register_data = AgentRegisterReqShape(
            symbol=self.__config.symbol,
            faction=self.__config.faction,
        )  # fmt: skip

        account_config = Config.get_account_from_agent_token(self.token)
        assert account_config is not None

        match self._register(register_data, account_config.token):
            case AgentRegisterResShape() as res:
                record = AgentRecord.insert(res)
                assert record is not None
                self.__data = record
                self.__data_timestamp = datetime.now(tz=UTC)
                self._token = AgentToken(self.__data.token)
                self._active_contract = Contract(res.contract)
                self._ships = [Ship(ship) for ship in res.ships]
                logger.info(f'Acquired new agent token {res.token}')
            case SpaceTradersAPIError() as err:
                raise self.__handle_register_err(err)

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
            .build()
        ).unwrap()

    def _fetch_contracts(self) -> ContractsShape | SpaceTradersAPIError:
        """Fetch the details of this agent's contracts from the SpaceTrader API.

        Returns:
            Contracts | SpaceTradersAPIError
        """
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ContractsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_CONTRACTS)
            .all_pages()
            .token(self.token)
            .build(),
        ).unwrap()  # fmt: skip

    def _fetch_events(self) -> AgentEventsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AgentEventsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENT_EVENTS)
            .token(self.token)
            .build()
        ).unwrap()

    def _fetch_faction_reputations(self) -> FactionReputationsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[FactionReputationsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_FACTION_REPUTATIONS)
            .token(self.token)
            .build()
        ).unwrap()

    def _fetch_ships(self) -> ShipsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIPS)
            .all_pages()
            .token(self.token)
            .build()
        ).unwrap()

    def _purchase_ship(
        self, shape: ShipPurchaseReqShape
    ) -> ShipPurchaseResShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipPurchaseResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.PURCHASE_SHIP)
            .data(shape)
            .token(self.token)
            .build()
        ).unwrap()

    def _register(
        self, data: AgentRegisterReqShape, account_token: AccountToken
    ) -> AgentRegisterResShape | SpaceTradersAPIError:
        """Register a new agent

        Args:
            data (RegisterAgentReqShape): The data to be sent in the request

        Returns:
            RegisterAgentReqShape | SpaceTradersAPIError
        """
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[AgentRegisterResShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.REGISTER_AGENT)
            .data(data)
            .token(account_token)
            .build()
        ).unwrap()

    def __handle_fetch_agent_err(self, err: SpaceTradersAPIError) -> ValueError:
        # TODO: Check for spacetraders errors that can be solved.
        log_str = f"Got an error while fetching agent's data. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def __handle_fetch_contracts_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's contracts. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def __handle_fetch_events_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's events. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def __handle_fetch_faction_reputations_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's faction reputations. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def __handle_fetch_ships_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching agent's ships. {err}"
        logger.error(log_str)
        return ValueError(log_str)

    def __handle_purchase_ship_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f'Got an error while purchasing ship. {err}'
        logger.error(log_str)
        return ValueError(log_str)

    def __handle_register_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f'Got an error while registering agent. {err}'
        logger.error(log_str)
        return ValueError(log_str)

    def __from_db(self) -> None:
        record: AgentRecord = AgentRecord.get_from_token(self.token.encoded)

        account_token = AccountToken(record.account.token)
        self._token = AgentToken(record.token)
        self._account = Account(account_token, self.token, record.account)

        for event_record in record.events:
            self._events.append(event)

        for contract_record in record.contracts:
            contract = ContractShap
            self.update_contracts()

    def __sync_db(self) -> None:
        self.__synced_db = True
        self.__synced_db_timestamp = datetime.now(tz=UTC)


@final
class PublicAgent(AgentABC):
    def __init__(self, symbol: str | None = None, data: PublicAgentShape | None = None) -> None:
        logger.debug('Initializing new PublicAgent')
        logger.trace(f'Input: symbol={"None" if symbol is None else symbol}')
        logger.trace(f'Input: data={"None" if data is None else data}')

        if symbol is None and data is None:
            msg = 'Must provide either symbol or data.'
            raise ValueError(msg)

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
            .build()
        ).unwrap()

    def __handle_fetch_agent_err(self, err: SpaceTradersAPIError) -> ValueError:
        log_str = f"Got an error while fetching public agent's data. {err}"
        logger.error(log_str)
        return ValueError(log_str)
