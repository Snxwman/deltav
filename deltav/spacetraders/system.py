from __future__ import annotations

from datetime import datetime

from deltav.spacetraders import Coordinate
from deltav.spacetraders.api import DEFAULT_PAGE_LIMIT
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.system import SystemType
from deltav.spacetraders.enums.waypoint import WaypointTraitSymbol, WaypointType
from deltav.spacetraders.faction import Faction
from deltav.spacetraders.models.systems import SystemShape, SystemWaypointsShape
from deltav.spacetraders.waypoint import Waypoint


# TODO: Convert methods to right types
class System:
    def __init__(self, symbol: str | None = None, data: SystemShape | None = None) -> None:
        self.__synced_api: bool = False
        self.__synced_db: bool = False

        self.__data: SystemShape
        self.__data_timestamp: datetime

        self._coordinate: Coordinate
        self._factions: list[Faction]
        self._waypoints: list[Waypoint]

    @property
    def constellation(self) -> str:
        """The constellation that the system is part of."""
        return self.__data.constellation

    @property
    def factions(self) -> list[Faction]:
        """Factions that control this system."""
        return self._factions

    @property
    def coordinate(self) -> Coordinate:
        """The relative position of the system in the sector.
        ```py
        Coordinate(NamedTuple)
            x: int
            y: int
        ```
        """
        return self._coordinate

    @property
    def sector_symbol(self) -> str:
        """The symbol of the sector."""
        return self.__data.sector_symbol

    @property
    def symbol(self) -> str:
        """The symbol of the system."""
        return self.__data.symbol

    @property
    def type(self) -> SystemType:
        """The type of system."""
        return self.__data.type

    @property
    def waypoints(self) -> list[Waypoint]:
        """Waypoints in this system."""
        return self._waypoints

    def _fetch_system(self) -> SystemShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[SystemShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_SYSTEMS)
            .path_params(self.symbol)
            .token()
            .build()
        ).unwrap()

    def _fetch_systems(self) -> SystemShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[SystemShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_SYSTEMS)
            .token()
            .build()
        ).unwrap()

    def _fetch_waypoints(
        self,
        waypoint_type: WaypointType | None = None,
        waypoint_traits: list[WaypointTraitSymbol] | None = None,
        start_page: int = 1,
        end_page: int | None = None,
        limit: int = DEFAULT_PAGE_LIMIT,
    ) -> SystemWaypointsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[SystemWaypointsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_SYSTEM_WAYPOINTS)
            .path_params(self.symbol)
            .query_params(type=waypoint_type, traits=waypoint_traits)
            .pages(start_page, end_page)
            .page_limit(limit)
            .token()
            .build()
        ).unwrap()

    def __handle_fetch_system_err(self, err: SpaceTradersAPIError) -> ValueError: ...

    def __handle_fetch_systems_err(self, err: SpaceTradersAPIError) -> ValueError: ...

    def __handle_fetch_waypoints_err(self, err: SpaceTradersAPIError) -> ValueError: ...
