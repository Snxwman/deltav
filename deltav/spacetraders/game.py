from datetime import datetime
from typing import cast

from deltav.spacetraders.agent import Agent
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models import ServerStatusShape
from deltav.spacetraders.models.agent import PublicAgentShape
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.system import System
from deltav.spacetraders.waypoint import Waypoint


class SpaceTradersGame:
    """The current state of the official SpaceTraders public game servers.

    Attributes:
        agents (list[Agent]): A list containing all known public agents.
        ships (list[Ship]): A list containing all known ships.
        systems (list[System]): A list containing all known systems.
        waypoints (list[Waypoint]): A list containing all knonw waypoints.
    """

    def __init__(self) -> None:
        self.agents: list[Agent]
        self.ships: list[Ship]
        self.systems: list[System]
        self.waypoints: list[Waypoint]
        # self.leaderboard_credits: list[tuple[str, int]]
        # self.leaderboard_submitted_charts: list[tuple[str, int]]

        self.next_restart: datetime
        self.restart_freq: str

    @classmethod
    def update_server_status(cls, server_status: ServerStatusShape) -> None: ...

    @classmethod
    def update_agents(cls) -> SpaceTradersAPIError | None:
        req = (
            SpaceTradersAPIRequest()
            .builder()
            .endpoint(SpaceTradersAPIEndpoint.GET_AGENTS)
            .with_account_token()
            .all_pages()
            .build()
        )

        match res := SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse():
                data: PublicAgentShape = cast(PublicAgentShape, res.spacetraders.data)
            case SpaceTradersAPIError() as err:
                return err

    @staticmethod
    def fetch_server_status(
        game_instance: 'SpaceTradersGame | None' = None,
    ) -> ServerStatusShape | SpaceTradersAPIError:
        req = SpaceTradersAPIRequest().builder().endpoint(SpaceTradersAPIEndpoint.SERVER_STATUS).build()

        match res := SpaceTradersAPIClient.call(req):
            case SpaceTradersAPIResponse():
                server_status: ServerStatusShape = cast(ServerStatusShape, res.spacetraders.data)

                if game_instance is not None:
                    game_instance.update_server_status(server_status)

                return server_status
            case SpaceTradersAPIError() as err:
                return err
