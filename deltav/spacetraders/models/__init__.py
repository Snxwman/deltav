from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from textwrap import wrap
from typing import Any, TypeVar, override

from deepmerge import always_merger
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from deltav.spacetraders.enums.market import TradeSymbol
from deltav.util.strings import indent

# TODO: Look into the following model config fields for ConfigDict
#   - str_to_upper
#   - str_min_length
#   - str_max_length
#   - use_enum_values
#   - validate_assignment


T = TypeVar('T', bound='SpaceTradersAPIResShape')


# https://github.com/pydantic/pydantic/discussions/3416
def merge_models(base: T, next: T) -> T:
    """Merge two Pydantic model instances.

    The attributes of 'base' and 'nxt' that weren't explicitly set are dumped into dicts
    using '.model_dump(exclude_unset=True)', which are then merged using 'deepmerge',
    and the merged result is turned into a model instance using '.model_validate'.

    For attributes set on both 'base' and 'nxt', the value from 'nxt' will be used in
    the output result.
    """

    base_dict = base.model_dump(exclude_unset=True)
    next_dict = next.model_dump(exclude_unset=True)
    merged_dict = always_merger.merge(base_dict, next_dict)
    print(base.model_validate(merged_dict, by_name=True))
    return base.model_validate(merged_dict, by_name=True)


# Inherited super type used for type annotations
class SpaceTradersAPIReqShape(BaseModel):
    """Base class for all request data sent in an SpaceTraders API request.

    Inherits from pydantic.BaseModel.
    """

    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_camel,
        ),
        revalidate_instances='always',
    )
    
    @override
    def __str__(self) -> str:
        return self._render(self, 0).expandtabs(4)

    def _render(self, value: Any, tabs: int) -> str:  # pyright: ignore[reportAny]
        MAX_WIDTH = 80
        pad = '\t' * tabs

        match value:
            case BaseModel():
                lines = [f'{pad}{value.__class__.__name__}']
                for k, v in value.__dict__.items():  # pyright: ignore[reportAny]
                    lines.append(f'{pad}\t{k}: {self._render(v, tabs + 1).lstrip()}')
                return '\n'.join(lines)
            case list():
                if not value:
                    return '[]'
                inline = f'[{", ".join(self._short(v) for v in value)}]'

                if len(inline) <= MAX_WIDTH:
                    return inline

                return '[\n' + '\n'.join(self._render(v, tabs + 1) for v in value) + f'\n{pad}]'
            case datetime():
                return value.strftime('%Y-%m-%d %H:%M:%S')
            case date():
                return value.strftime('%Y-%m-%d')
            case str():
                if len(pad) + len(value) > MAX_WIDTH:
                    ...
                return value

        return repr(value)  # pyright: ignore[reportAny]

    def _short(self, value: Any) -> str:  # pyright: ignore[reportAny]
        match value:
            case BaseModel():
                return value.__class__.__name__
            case datetime():
                return value.strftime('%Y-%m-%d %H:%M:%S')
            case date():
                return value.strftime('%Y-%m-%d')
            case str():
                return value

        return repr(value)  # pyright: ignore[reportAny]


# Inherited super type used for type annotations
class SpaceTradersAPIResShape(BaseModel):
    """Base class for all response data received by a SpaceTraders API call.

    Inherits from pydantic.BaseModel.
    """

    model_config = ConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        alias_generator=to_camel,
        revalidate_instances='always',
    )

    @override
    def __str__(self) -> str:
        return self._render(self, 0).expandtabs(4)

    def _render(self, value: Any, tabs: int) -> str:  # pyright: ignore[reportAny]
        MAX_WIDTH = 80
        pad = '\t' * tabs

        match value:
            case BaseModel():
                if type(value).__str__ is not SpaceTradersAPIResShape.__str__:
                    return str(value)
                else:
                    lines = [f'{pad}{value.__class__.__name__}']
                    for k, v in value.__dict__.items():  # pyright: ignore[reportAny]
                        lines.append(f'{pad}\t{k}: {self._render(v, tabs + 1).lstrip()}')
                    return '\n'.join(lines)
            case list():
                if not value:
                    return '[]'
                inline = f'[{", ".join(self._render(v, tabs) for v in value)}]'

                if len(inline) <= MAX_WIDTH:
                    return inline

                return '[\n' + '\n'.join(self._render(v, tabs + 1) for v in value) + f'\n{pad}]'
            case datetime():
                return value.strftime('%Y-%m-%d %H:%M:%S')
            case date():
                return value.strftime('%Y-%m-%d')
            case Enum():
                return value.name
            case str():
                if len(value) > MAX_WIDTH:
                    return '...' + ''.join(f'\n{pad}\t{line}' for line in wrap(value, width=MAX_WIDTH))

                return value

        return repr(value)  # pyright: ignore[reportAny]

    def _short(self, value: Any) -> str:  # pyright: ignore[reportAny]
        match value:
            case BaseModel():
                return value.__class__.__name__
            case datetime():
                return value.strftime('%Y-%m-%d %H:%M:%S')
            case date():
                return value.strftime('%Y-%m-%d')
            case str():
                return value

        return repr(value)  # pyright: ignore[reportAny]


# WARN: Developmental placeholder
class UnknownReqShape(SpaceTradersAPIReqShape):
    """⚠  FOR DEVELOPMENT ONLY ⚠

    An unknown shape to use as a placeholder for fields requiring a SpaceTradersAPIReqShape

    data: any
    """

    data: Any = {}  # pyright: ignore[reportAny]


# WARN: Developmental placeholder
class UnknownResShape(SpaceTradersAPIResShape):
    """⚠  FOR DEVELOPMENT ONLY ⚠

    An unknown shape to use as a placeholder for fields requiring a SpaceTradersAPIResShape

    data: any
    """

    data: Any = {}  # pyright: ignore[reportAny]


class NoDataReqShape(SpaceTradersAPIReqShape):
    pass


class NoDataResShape(SpaceTradersAPIResShape):
    pass


class MarketSupplyChainAdditionalPropertiesShape(SpaceTradersAPIResShape):
    ANY_ADDITIONAL_PROPERTY: list[str]


class MarketSupplyChainShape(SpaceTradersAPIResShape):
    export_to_import_map: Mapping[TradeSymbol, list[TradeSymbol]]  # TODO: Verify


class EventSubscribeReqShape(SpaceTradersAPIReqShape):
    action: str  # TODO: Make enum
    system_symbol: str


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

    @override
    def __str__(self) -> str:
        return f'{self.agent_symbol.ljust(14)} ${self.credits:,}'


class ChartsLeaderboardAgentShape(SpaceTradersAPIResShape):
    """

    agent_symbol: str
    chart_count: int
    """

    agent_symbol: str
    chart_count: int

    @override
    def __str__(self) -> str:
        return f'{self.agent_symbol.ljust(14)} {self.chart_count:,}'


class LeaderboardsShape(SpaceTradersAPIResShape):
    """

    most_credits: CreditsLeaderboardShape
    most_submitted_charts: ChartsLeaderboardAgentShape
    """

    most_credits: list[CreditsLeaderboardAgentShape]
    most_submitted_charts: list[ChartsLeaderboardAgentShape]

    @override
    def __str__(self) -> str:
        most_credits = ''.join(f'\n\t\t{agent}' for agent in self.most_credits)
        most_charts = ''.join(f'\n\t\t{agent}' for agent in self.most_submitted_charts)
        return ''.join([
            f'\n\tMost credits: {most_credits}',
            f'\n\tMost submitted charts: {most_charts}',
        ])


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

    @override
    def __str__(self) -> str:
        body = ''.join(f'\n\t{line}' for line in wrap(self.body, width=80))
        return f'{self.title}{body}'


class LinkShape(SpaceTradersAPIResShape):
    """

    name: str
    url: str
    """

    name: str
    url: str

    @override
    def __str__(self) -> str:
        return f'\t\t{self.name}: {self.url}'


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

    @override
    def __str__(self) -> str:
        announcements = '\n'.join(str(ann) for ann in self.announcements)
        next_reset = self.server_resets.next.strftime('%Y-%m-%d %H:%M:%S')
        return '\n\t'.join([
            f'\n\tStatus: {self.status}',
            f'Reset: {self.reset_date} -> {next_reset} ({self.server_resets.frequency})',
            'Stats:',
            f'\t{self.stats.accounts} accounts, {self.stats.agents} agents, {self.stats.ships} ships',
            f'\t{self.stats.systems} systems, {self.stats.waypoints} waypoints',
            f'\tlast market update: {self.health.last_market_update}',
            f'Announcements:\n{indent(announcements, 2)}',
            f'Leaderboards: {indent(str(self.leaderboards), 1)}',
        ]).expandtabs(4)


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
