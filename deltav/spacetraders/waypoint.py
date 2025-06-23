from __future__ import annotations

from datetime import datetime

from deltav.spacetraders import Coordinate
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.chart import Chart
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.waypoint import (
    WaypointModifierSymbol,
    WaypointTraitSymbol,
    WaypointType,
)
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.construction import ConstructionShape
from deltav.spacetraders.models.market import MarketShape
from deltav.spacetraders.models.ship import ShipyardShape
from deltav.spacetraders.models.systems import JumpgateShape
from deltav.spacetraders.models.waypoint import (
    WaypointModifierShape,
    WaypointShape,
    WaypointTraitShape,
)


class Waypoint:
    def __init__(self, symbol: str | None = None, data: WaypointShape | None = None) -> None:
        self.__synced_api: bool = False
        self.__synced_db: bool = False

        self.__data: WaypointShape
        self.__data_timestamp: datetime

        self._chart: Chart
        self._coordinate: Coordinate
        self._faction: Faction
        self._construction_site: ConstructionShape
        self._modifiers: dict[WaypointModifierSymbol, WaypointModifierShape]
        self._orbitals: list[Waypoint]
        self._orbits: Waypoint | None
        self._traits: dict[WaypointTraitSymbol, WaypointTraitShape]

    @property
    def chart(self) -> Chart:
        """
        The chart of a system or waypoint,
        which makes the location visible to other agents.
        """
        return self._chart

    @property
    def coordinate(self) -> Coordinate:
        """
        Position of the waypoint relative to the system.
        These are not an absolute position in the universe.
        ```py
        Coordinate(NamedTuple)
            x: int
            y: int
        ```
        """
        return self._coordinate

    @property
    def faction(self) -> Faction:
        """The faction that controls the waypoint."""
        return self._faction

    @property
    def is_under_construction(self) -> bool:
        return self._construction_site.is_complete

    @property
    def is_jumpgate(self) -> bool:
        return self.__data.type is WaypointType.JUMP_GATE

    @property
    def modifiers(self) -> list[WaypointModifierShape]:
        """The modifiers of the waypoint."""
        return list(self._modifiers.values())

    @property
    def modifier_symbols(self) -> list[WaypointModifierSymbol]:
        """The modifier symbols of the waypoint."""
        return list(self._modifiers.keys())

    @property
    def has_market(self) -> bool:
        return bool(WaypointTraitSymbol.MARKETPLACE in self.trait_symbols)

    @property
    def orbitals(self) -> list[Waypoint]:
        """Waypoints that orbit this waypoint."""
        return self._orbitals

    @property
    def orbits(self) -> Waypoint | None:
        """
        The symbol of the parent waypoint, if this waypoint is in orbit
        around another waypoint. Otherwise this value is None.
        """
        return self._orbits

    @property
    def has_shipyard(self) -> bool:
        return bool(WaypointTraitSymbol.SHIPYARD in self.trait_symbols)

    @property
    def symbol(self) -> str:
        """The symbol of the waypoint."""
        return self.__data.symbol

    @property
    def system_symbol(self) -> str:
        """The symbol of the system."""
        return self.__data.system_symbol

    @property
    def traits(self) -> list[WaypointTraitShape]:
        """The traits of the waypoint."""
        return list(self._traits.values())

    @property
    def trait_symbols(self) -> list[WaypointTraitSymbol]:
        """The traits symbols of the waypoint."""
        return list(self._traits.keys())

    @property
    def type(self) -> WaypointType:
        """The type of waypoint."""
        return self.__data.type

    def has_modifier(self, modifier: WaypointModifierSymbol) -> bool:
        return bool(modifier in self.modifier_symbols)

    def has_trait(self, trait: WaypointTraitSymbol) -> bool:
        return bool(trait in self.trait_symbols)

    def _fetch_construction_site(self) -> ConstructionShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ConstructionShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_CONSTRUCTION_SITE)
            .path_params(self.system_symbol, self.symbol)
            .build()
        ).unwrap()

    def _fetch_market(self) -> MarketShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[MarketShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_MARKET)
            .path_params(self.system_symbol, self.symbol)
            .build()
        ).unwrap()

    def _fetch_jumpgate(self) -> JumpgateShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[JumpgateShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_JUMPGATE)
            .path_params(self.system_symbol, self.symbol)
            .build()
        ).unwrap()

    def _fetch_shipyard(self) -> ShipyardShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ShipyardShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SHIPYARD)
            .path_params(self.system_symbol, self.symbol)
            .build()
        ).unwrap()

    def _fetch_waypoint(self) -> WaypointShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[WaypointShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_WAYPOINT)
            .path_params(self.system_symbol, self.symbol)
            .build()
        ).unwrap()

    def __handle_fetch_construction_site_err(self, err: SpaceTradersAPIError) -> ValueError: ...

    def __handle_fetch_market_err(self, err: SpaceTradersAPIError) -> ValueError: ...

    def __handle_fetch_jumpgate_err(self, err: SpaceTradersAPIError) -> ValueError: ...

    def __handle_fetch_waypoint_err(self, err: SpaceTradersAPIError) -> ValueError: ...
