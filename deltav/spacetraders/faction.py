from typing import cast

from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.models.faction import FactionShape, FactionTrait


class Faction:
    DEFAULT: str = 'COSMIC'
    # TODO: Track when we last updated a faction
    _FACTIONS: dict[FactionSymbol, 'Faction'] = {}

    def __init__(self, data: FactionShape):
        self.symbol: FactionSymbol = data.symbol
        self.name: str = data.name
        self.description: str = data.description
        self.headquarters: str = data.headquarters
        self.traits: list[FactionTrait] = data.traits
        self.is_recruiting: bool = data.is_recruiting

    @classmethod
    def hydrate_factions(cls) -> None | SpaceTradersAPIError:
        # WARN: This might clog the ratelimits as is
        factions = Faction._fetch_factions()

        match factions:
            case list():
                for faction in factions:
                    Faction._add_faction_to_cache(faction)
            case SpaceTradersAPIError() as err:
                return err

    @classmethod
    def get_by_symbol(cls, symbol: FactionSymbol) -> 'Faction':
        """Get the Faction instance for the given symbol from the class' cache

        Args:
            symbol (FactionSymbol): The faction's symbol

        Retuns:
            Faction

        Raises:
            ValueError: If the faction is not in the cache and cannot be fetched
                from the SpaceTraders API. Factions are predefined by the game,
                so not being able to fetch the faction is irrecoverable.
        """
        faction: Faction | None = cls._FACTIONS.get(symbol, None)

        if faction is not None:
            return faction
        else:  # This faction hasn't been added to _FACTIONS yet
            _faction = Faction._fetch_faction(symbol)

            match _faction:
                case SpaceTradersAPIError() as err:
                    # CRIT: Irrecoverable (not apparant from signature)
                    raise ValueError(err)
                case _:  # Default case because python doesn't allow TypeDicts in match arms
                    Faction._add_faction_to_cache(_faction)
                    return cls._FACTIONS[symbol]

    @classmethod
    def _add_faction_to_cache(cls, data: FactionShape) -> None:
        symbol, faction = data.symbol, Faction(data)
        cls._FACTIONS[symbol] = faction

    @staticmethod
    def _fetch_faction(name: FactionSymbol) -> FactionShape | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_FACTION)
            .path_params(name.name)
            .build()
        )

        match res:
            case SpaceTradersAPIResponse():
                return cast(FactionShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def _fetch_factions() -> list[FactionShape] | SpaceTradersAPIError:
        res = SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_FACTIONS)
            .with_token()
            .all_pages()
            .build()
        )

        # FIX: Needs pagination handling to be built
        match res:
            case SpaceTradersAPIResponse():
                return cast(list[FactionShape], res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err
