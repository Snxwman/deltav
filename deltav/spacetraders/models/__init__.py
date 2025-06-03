from __future__ import annotations

from datetime import date, datetime
from typing import Callable

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


# TODO: Look into the following model config fields for ConfigDict
#   - str_to_upper
#   - str_min_length
#   - str_max_length
#   - use_enum_values
#   - validate_assignment


# Inherited super type used for type annotations
class SpaceTradersAPIReqShape(BaseModel):
    """Base type for all request data sent in an SpaceTraders API request."""

    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        revalidate_instances='always',
    )


# Inherited super type used for type annotations
class SpaceTradersAPIResShape(BaseModel):
    """Base type for all response data received by a SpaceTraders API call."""

    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        alias_generator=to_camel,
        # alias_generator=AliasGenerator(
        #     validation_alias=to_snake,
        #     serialization_alias=to_camel,
        # ),
        revalidate_instances='always',
    )


####################
# Global endpoints #
####################


class StatsShape(SpaceTradersAPIResShape):
    """

    accounts: int
    agents: int
    ships: int
    systems: int
    waypoints: int
    """

    accounts: int
    agents: int
    ships: int
    systems: int
    waypoints: int


class HealthShape(SpaceTradersAPIResShape):
    """

    last_market_update: datetime
    """

    last_market_update: datetime


class CreditsLeaderboardAgentShape(SpaceTradersAPIResShape):
    """

    agent_symbol: str
    credits: int
    """

    agent_symbol: str
    credits: int


class ChartsLeaderboardAgentShape(SpaceTradersAPIResShape):
    """

    agent_symbol: str
    chart_count: int
    """

    agent_symbol: str
    chart_count: int


class LeaderboardsShape(SpaceTradersAPIResShape):
    """

    most_credits: CreditsLeaderboardShape
    most_submitted_charts: ChartsLeaderboardAgentShape
    """

    most_credits: list[CreditsLeaderboardAgentShape]
    most_submitted_charts: list[ChartsLeaderboardAgentShape]


class ServerRestartsShape(SpaceTradersAPIResShape):
    """

    next: datetime
    frequency: str
    """

    next: datetime
    frequency: str


class AnnouncementShape(SpaceTradersAPIResShape):
    """

    title: str
    body: str
    """

    title: str
    body: str


class LinkShape(SpaceTradersAPIResShape):
    """

    name: str
    url: str
    """

    name: str
    url: str


# NOTE: Top level return shape
class ServerStatusShape(SpaceTradersAPIResShape):
    """

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
    """

    status: str
    version: str
    reset_date: date
    description: str
    stats: StatsShape
    health: HealthShape
    leaderboards: LeaderboardsShape
    server_resets: ServerRestartsShape
    announcements: list[AnnouncementShape]
    links: list[LinkShape]


class ErrorCodeShape(SpaceTradersAPIResShape):
    """

    code: int
    name: str
    """

    code: int
    name: str


# NOTE: Top level return shape
class ErrorCodesShape(SpaceTradersAPIResShape):
    """

    error_codes: list[ErrorCodeShape]
    """

    error_codes: list[ErrorCodeShape]
