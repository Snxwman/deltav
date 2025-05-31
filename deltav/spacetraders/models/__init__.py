from __future__ import annotations
from datetime import datetime
from typing import TypedDict


# Inherited super type used for type annotations
class SpaceTradersAPIReqShape(TypedDict):
    pass


# Inherited super type used for type annotations
class SpaceTradersAPIResShape(TypedDict):
    pass


####################
# Global endpoints #
####################

class StatsShape(SpaceTradersAPIResShape):
    accounts: int
    agents: int
    ships: int
    systems: int
    waypoints: int


class HealthShape(SpaceTradersAPIResShape):
    last_market_update: datetime 


class CreditsLeaderboardAgentShape(SpaceTradersAPIResShape):
    agent_symbol: str
    credits: int


class CreditsLeaderboardShape(SpaceTradersAPIResShape):
    most_credits: list[CreditsLeaderboardAgentShape]


class ChartsLeaderboardAgentShape(SpaceTradersAPIResShape):
    agent_symbol: str
    chart_count: int


class ChartsLeaderboardShape(SpaceTradersAPIResShape):
    chart_count: list[ChartsLeaderboardAgentShape]


class LeaderboardsShape(SpaceTradersAPIResShape):
    most_credits: CreditsLeaderboardShape
    most_submitted_charts: ChartsLeaderboardAgentShape


class ServerRestartsShape(SpaceTradersAPIResShape):
    next: datetime
    frequency: str


class AnnouncementShape(SpaceTradersAPIResShape):
    title: str
    body: str


class LinkShape(SpaceTradersAPIResShape):
    name: str
    url: str


# NOTE: Top level return shape
class ServerStatusShape(SpaceTradersAPIResShape):
    status: str
    version: str
    reset_date: str
    description: str
    stats: StatsShape
    health: HealthShape
    leaderboards: LeaderboardsShape
    server_resets: ServerRestartsShape
    announcements: list[AnnouncementShape]
    links: list[LinkShape]


class ErrorCodeShape(SpaceTradersAPIResShape):
    code: int
    name: str


# NOTE: Top level return shape
class ErrorCodesShape(SpaceTradersAPIResShape):
    error_codes: list[ErrorCodeShape]

