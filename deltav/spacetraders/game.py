from datetime import datetime

from deltav.spacetraders.agent import Agent
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.system import System
from deltav.spacetraders.waypoint import Waypoint


class SpaceTradersGame():

    def __init__(self) -> None:
        self.agents: list[Agent]
        self.ships: list[Ship]
        self.systems: list[System]
        self.waypoints: list[Waypoint]
        # self.leaderboard_credits: list[tuple[str, int]]
        # self.leaderboard_submitted_charts: list[tuple[str, int]]

        self.next_restart: datetime
        self.restart_freq: str


    @staticmethod
    def fetch_game_state() -> SpaceTradersAPIResponse | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest() \
            .builder() \
            .endpoint(SpaceTradersAPIEndpoint.GAME) \
            .build()

        return SpaceTradersAPIClient.call(req)


