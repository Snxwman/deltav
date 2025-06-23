from __future__ import annotations

from datetime import date, datetime
from textwrap import wrap
from typing import override

from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.util.strings import indent


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
        return ''.join(
            [f'\n\tMost credits: {most_credits}', f'\n\tMost submitted charts: {most_charts}']
        )


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
        return '\n\t'.join(
            [
                f'\n\tStatus: {self.status}',
                f'Reset: {self.reset_date} -> {next_reset} ({self.server_resets.frequency})',
                'Stats:',
                f'\t{self.stats.accounts} accounts, {self.stats.agents} agents, {self.stats.ships} ships',
                f'\t{self.stats.systems} systems, {self.stats.waypoints} waypoints',
                f'\tlast market update: {self.health.last_market_update}',
                f'Announcements:\n{indent(announcements, 2)}',
                f'Leaderboards: {indent(str(self.leaderboards), 1)}',
            ]
        ).expandtabs(4)
