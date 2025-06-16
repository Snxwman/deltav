from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from loguru import logger

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.faction import FactionSymbol, FactionTraitSymbol
from deltav.spacetraders.models.faction import FactionShape, FactionsShape
from deltav.store.db.faction import FactionRecord


@dataclass(frozen=True)
class FactionTrait:
    symbol: FactionTraitSymbol
    name: str
    description: str


class Faction:
    _FACTIONS: dict[FactionSymbol, 'Faction'] = {}
    __FACTIONS_TIMESTAMPS: dict[FactionSymbol, datetime] = {}

    def __init__(self, data: FactionShape | FactionRecord) -> None:
        self.__synced_api: bool = False
        self.__synced_db: bool = False
        self.__synced_api_timestamp: datetime
        self.__synced_db_timestamp: datetime

        self.__data: FactionRecord

        self._symbol: FactionSymbol
        self._traits: list[FactionTrait] = []

        match data:
            case FactionShape():
                self.__hydrate_from_shape(data)
            case FactionRecord():
                self.__hydrate_from_record(data)

        Faction.__update_cache(self)

    def __hydrate_from_record(self, record: FactionRecord) -> None:
        self.__synced_db = True
        self.__synced_db_timestamp = datetime.now(tz=UTC)
        self.__data = record
        self._symbol = FactionSymbol[record.symbol]
        for trait_record in record.traits:
            trait = FactionTrait(
                symbol=FactionTraitSymbol[trait_record.trait.symbol],
                name=trait_record.trait.name,
                description=trait_record.trait.description,
            )
            self._traits.append(trait)

    def __hydrate_from_shape(self, data: FactionShape) -> None:
        self.__synced_api = True
        self.__synced_api_timestamp = datetime.now(tz=UTC)
        self._symbol = data.symbol
        for trait_shape in data.traits:
            trait = FactionTrait(
                symbol=trait_shape.symbol,
                name=trait_shape.name,
                description=trait_shape.description,
            )
            self._traits.append(trait)

    @property
    def symbol(self) -> FactionSymbol:
        return self._symbol

    @property
    def name(self) -> str:
        return self.__data.name

    @property
    def description(self) -> str:
        return self.__data.description

    @property
    def headquarters(self) -> str:
        return self.__data.headquarters

    @property
    def traits(self) -> list[FactionTrait]:
        return self._traits

    @property
    def is_recruiting(self) -> bool:
        return self.__data.is_recruiting

    @classmethod
    def get_faction(cls, symbol: FactionSymbol) -> 'Faction':
        if (faction := Faction.__from_cache(symbol)) is not None:
            return faction

        match Faction._fetch_faction(symbol):
            case FactionShape() as res:
                faction = Faction(res)
                Faction.__update_cache(faction)
                return faction
            case SpaceTradersAPIError() as err:
                # CRIT: Irrecoverable (not apparant from signature)
                raise Faction.__handle_fetch_faction_err(err)

    @classmethod
    def get_factions(cls) -> None | SpaceTradersAPIError:
        # WARN: This might clog the ratelimits as is
        match Faction._fetch_factions():
            case FactionsShape() as res:
                for _faction in res.factions:
                    faction = Faction(_faction)
                    Faction.__update_cache(faction)
            case SpaceTradersAPIError() as err:
                raise Faction.__handle_fetch_factions_err(err)

    @staticmethod
    def _fetch_faction(symbol: FactionSymbol) -> FactionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[FactionShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_FACTION)
            .path_params(symbol.name)
            .build()
        ).unwrap()

    @staticmethod
    def _fetch_factions() -> FactionsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[FactionsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_FACTIONS)
            .token()
            .all_pages()
            .build()
        ).unwrap()

    @staticmethod
    def __handle_fetch_faction_err(err: SpaceTradersAPIError) -> ValueError:
        log_str = f'Got an error while fetching faction. {err}'
        logger.error(log_str)
        return ValueError(log_str)

    @staticmethod
    def __handle_fetch_factions_err(err: SpaceTradersAPIError) -> ValueError:
        log_str = f'Got an error while fetching factions. {err}'
        logger.error(log_str)
        return ValueError(log_str)

    @classmethod
    def __update_cache(cls, faction: 'Faction') -> None:
        """Adds or updates the factions cache"""
        cls._FACTIONS[faction.symbol] = faction
        cls.__FACTIONS_TIMESTAMPS[faction.symbol] = datetime.now(tz=UTC)

    @classmethod
    def __from_cache(cls, symbol: FactionSymbol) -> 'Faction | None':
        """Get the Faction instance, for the given symbol, from the class' cache

        Args:
        ```
        symbol(FactionSymbol)
        ```
        """
        return cls._FACTIONS.get(symbol, None)
