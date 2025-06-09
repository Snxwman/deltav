from datetime import datetime

from loguru import logger

from deltav.spacetraders.agent import Agent
from deltav.spacetraders.api import MAX_PAGE_LIMIT
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models import ServerStatusShape
from deltav.spacetraders.models.agent import PublicAgentShape, PublicAgentsShape
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.system import System
from deltav.spacetraders.waypoint import Waypoint


class SpaceTradersGame:
    """The current state of the official SpaceTraders public game servers.

    Attributes:
        agents: All known public agents.
        ships: All known ships.
        systems: All known systems.
        waypoints: All knonw waypoints.
    """

    def __init__(self) -> None:
        self.agents: list[PublicAgentShape]
        self.ships: list[Ship]
        self.systems: list[System]
        self.waypoints: list[Waypoint]
        # self.leaderboard_credits: list[tuple[str, int]]
        # self.leaderboard_submitted_charts: list[tuple[str, int]]

        self.next_restart: datetime
        self.restart_freq: str

    @property
    def server_status(self) -> ServerStatusShape | SpaceTradersAPIError:
        return SpaceTradersGame._fetch_server_status()

    def update_server_status(self, status: ServerStatusShape | None = None) -> None:
        if status is None:
            _status = SpaceTradersGame._fetch_server_status()
            print(_status)

    def update_agents(self) -> None:
        match res := self._fetch_public_agents():
            case PublicAgentsShape():
                self.agents = res.agents
            case SpaceTradersAPIError():
                print(res)

    @staticmethod
    def _fetch_public_agents() -> PublicAgentsShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[PublicAgentsShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_ALL_AGENTS)
            .token()
            .all_pages()
            .page_limit(MAX_PAGE_LIMIT)
            .build(),
        ).unwrap()

    @staticmethod
    def _fetch_server_status() -> ServerStatusShape | SpaceTradersAPIError:
        return SpaceTradersAPIClient.call(
            SpaceTradersAPIRequest[ServerStatusShape]()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_SERVER_STATUS)
            .build(),
        ).unwrap()  # fmt: skip


GAME = SpaceTradersGame()
logger.info(f'SpaceTraders server status: {GAME.server_status}')
